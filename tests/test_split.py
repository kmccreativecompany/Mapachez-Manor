"""Browser checks for SPLIT v1: the manor and the desk computer (HMS) side by side.
On every screen the HMS slides up as a drawer over the bottom half, with the manor above. Room changes in the HMS show up on the matching manor room.

Run: python tests/test_split.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Set SPLIT_SHOTS=<folder> to also save screenshots.
"""
import os
import unittest

import test_hms as hbase

base = hbase.base
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', "\nwindow.splitEval=s=>eval(s);\n})();\n</script>")
SHOTS = os.getenv('SPLIT_SHOTS')


class Split(hbase.Hms):
    def ev(self, s):
        return self.page.evaluate(f'window.splitEval({s!r})')

    def shot(self, name):
        if SHOTS:
            self.page.wait_for_timeout(250)
            self.page.screenshot(path=os.path.join(SHOTS, ('phone-' if isinstance(self, PhoneSplit) else 'desk-') + name))

    def manor_open_hms(self):
        self.enter_manor()
        self.page.evaluate('window.hmsTest.open()')
        self.page.wait_for_selector('#hms-next-go')
        self.page.wait_for_timeout(150)

    def boxes(self):
        return self.page.evaluate("""()=>{const m=document.getElementById('modal').getBoundingClientRect(),
          c=document.getElementById('canvas-wrap').getBoundingClientRect();return {m:[m.left,m.top,m.right,m.bottom],c:[c.left,c.top,c.right,c.bottom],w:innerWidth,h:innerHeight};}""")

    def test_01_hms_slides_up_as_a_drawer_with_the_manor_above(self):
        self.manor_open_hms()
        self.assertTrue(self.ev('split.on'))
        b = self.boxes()
        self.assertAlmostEqual(b['m'][3], b['h'], delta=2)               # drawer sits on the bottom edge
        self.assertAlmostEqual(b['m'][1], b['h'] * .44, delta=12)        # and covers about half
        self.assertLessEqual(b['m'][2] - b['m'][0], 862)                 # never stretched too wide
        self.assertAlmostEqual(b['m'][0], b['w'] - b['m'][2], delta=2)   # centered
        self.assertLess(b['c'][1], 2)                                    # the manor fills the top
        self.assertGreater(b['m'][1] - b['c'][1], 300)
        self.assertTrue(self.page.locator('#split-tag').is_visible())
        self.assertTrue(self.page.locator('#split-handle').is_visible())
        # Nothing removed: every lesson, game and the next step are still there.
        self.assertEqual(self.page.locator('#hms-lessons .hms-lesson').count(), 5)
        self.assertEqual(self.page.locator('#hms-games .hms-lesson').count(), 3)
        self.assertEqual(self.page.locator('.hms-next').count(), 1)
        self.shot('01-drawer-home.png')
        self.page.locator('#split-handle').click()
        self.page.wait_for_timeout(400)
        self.assertAlmostEqual(self.boxes()['m'][1], b['h'] * .14, delta=12)
        self.page.locator('#split-handle').click()
        self.page.wait_for_timeout(400)
        self.assertAlmostEqual(self.boxes()['m'][1], b['h'] * .44, delta=12)

    def test_02_practice_hotel_room_changes_light_up_the_manor_room(self):
        self.manor_open_hms()
        self.page.locator('#hms-tile-hotel').click()
        self.page.wait_for_selector('.ph-tile')
        self.page.wait_for_timeout(100)
        board = self.ev('split.board')
        self.assertEqual(board, self.ev("Object.fromEntries(Object.entries(ph.rooms).map(([r,R])=>[r,R.st]))"))
        self.page.locator('.ph-tile[data-r="203"]').click()
        self.page.wait_for_timeout(100)
        self.assertEqual(self.ev('split.sel'), '203')
        self.page.locator('#ph-panel .primary-button').first.click()  # housekeeping cleans it
        self.page.wait_for_timeout(100)
        self.assertEqual(self.ev('split.board["203"]'), 'clean')
        self.assertEqual(self.ev('split.pings.map(p=>p.r+":"+p.st).join()'), '203:clean')
        self.shot('02-practice-hotel-cleaned-203.png')
        self.page.locator('#ph-panel .primary-button').first.click()  # supervisor inspects it
        self.page.wait_for_timeout(100)
        self.assertEqual(self.ev('split.board["203"]'), 'ready')
        # Undo puts the manor badge back, too.
        self.page.locator('#ph-undo').click()
        self.page.wait_for_timeout(100)
        self.assertEqual(self.ev('split.board["203"]'), 'clean')

    def test_03_check_in_sends_a_key_to_the_room(self):
        self.manor_open_hms()
        self.page.locator('#hms-tile-hotel').click()
        self.page.wait_for_selector('.ph-tile')
        self.page.locator('.ph-guest .ph-in').first.click()
        self.page.locator('.ph-tile[data-r="201"]').click()
        for k in range(3):
            self.page.locator('.ph-ask').nth(k).click()
        self.page.locator('.ph-keys').click()
        self.page.wait_for_timeout(120)
        self.assertEqual(self.ev('split.board["201"]'), 'guest')
        self.assertIn('201:guest', self.ev('split.pings.map(p=>p.r+":"+p.st).join()'))
        self.shot('03-checked-in-201.png')

    def test_04_real_hms_rooms_and_room_rush_show_on_the_manor(self):
        self.manor_open_hms()
        self.page.locator('#hms-tile-browse').click()
        self.tap('tab:rooms')
        self.tap('room:205')
        self.page.wait_for_timeout(100)
        self.assertEqual(self.ev('split.sel'), '205')
        self.assertEqual(self.ev('split.board["205"]'), 'tidy')
        self.page.evaluate("window.hmsTest.game('rush')")
        self.page.wait_for_selector('.hms-radio')
        self.page.wait_for_timeout(100)
        self.assertTrue(self.ev('split.on'))
        a = self.page.evaluate('window.hmsTest.rushAnswer()')
        self.assertEqual(self.ev('split.sel'), a['r'])  # the radioed room glows
        self.page.locator(f'[data-room="{a["r"]}"]').click()
        self.page.locator(f'[data-st="{a["to"]}"]').click()
        self.page.wait_for_timeout(100)
        self.assertEqual(self.ev(f'split.board["{a["r"]}"]'), a['to'])
        self.shot('04-room-rush.png')

    def test_05_closing_brings_back_the_normal_manor_and_other_windows_stay_centered(self):
        self.manor_open_hms()
        self.page.keyboard.press('Escape')
        self.page.wait_for_timeout(100)
        self.assertFalse(self.ev('split.on'))
        self.assertFalse(self.ev("document.body.classList.contains('hms-split')"))
        self.assertEqual(self.page.locator('#canvas-wrap').evaluate('e=>getComputedStyle(e).position'), 'relative')
        self.ev("openModal('<h2 id=\"modal-heading\">Hi</h2>')")
        self.assertFalse(self.ev("modal.classList.contains('split')"))

    def test_06_title_screen_hms_walks_into_the_manor_and_opens_the_drawer(self):
        self.page.locator('#hms-title').click()
        self.page.wait_for_selector('#hms-next-go')
        self.page.wait_for_timeout(150)
        self.assertTrue(self.ev('split.on'))
        self.assertTrue(self.ev('!titleVisible'))
        self.assertTrue(self.page.locator('#split-tag').is_visible())
        self.shot('08-from-title.png')

    def test_07_title_screen_hms_keeps_a_saved_evening(self):
        self.enter_manor()
        self.ev("state.flags.splitMarker=true;save()")
        self.page.locator('#home').click()
        self.page.wait_for_timeout(200)
        self.page.locator('#hms-title').click()
        self.page.wait_for_selector('#hms-next-go')
        self.assertTrue(self.ev('split.on'))
        self.assertTrue(self.ev('state.flags.splitMarker===true'), 'The saved evening is continued, not replaced')


class PhoneSplit(Split):
    def setUp(self, viewport=None):
        super().setUp(viewport=viewport or {'width': 390, 'height': 844})

    def test_02_practice_hotel_room_changes_light_up_the_manor_room(self):
        super().test_02_practice_hotel_room_changes_light_up_the_manor_room()
        if SHOTS:
            self.page.locator('.ph-tile[data-r="203"]').click()
            self.page.locator('#ph-panel .primary-button').first.click()
            self.page.wait_for_timeout(150)
            self.page.screenshot(path=os.path.join(SHOTS, 'phone-06-practice-hotel-ready-203.png'))

    def test_03_check_in_sends_a_key_to_the_room(self):
        super().test_03_check_in_sends_a_key_to_the_room()
        self.shot('07-checked-in-201-key.png')


# Only run this file's own checks (the HMS checks run in test_hms.py).
for _cls in (Split, PhoneSplit):
    for _name in dir(hbase.Hms):
        if _name.startswith('test_') and not any(_name in k.__dict__ for k in _cls.__mro__ if k in (Split, PhoneSplit)):
            setattr(_cls, _name, None)

if __name__ == '__main__':
    unittest.main()
