"""Browser checks for HMS FRIENDLY v1: the desk computer home with one glowing next step (and
everything else still there under More), the practice hotel where nothing counts, its big Undo,
and the six-tile colorful room board.

Run: python tests/test_hms_friendly.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
"""
import unittest

import test_hms as hbase

base = hbase.base
# Test-only: evaluate inside the game's closure (injected into the test response, never shipped).
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', "\nwindow.phEval=s=>eval(s);\n})();\n</script>")


class Friendly(hbase.Hms):
    def say(self):
        return self.page.locator('#ph-say').inner_text()

    def hotel(self):
        self.page.evaluate('window.hmsTest.open()')
        self.page.locator('#hms-tile-hotel').click()
        self.page.wait_for_selector('.ph-tile')

    def test_01_home_has_greeting_one_next_step_and_keeps_everything_under_more(self):
        self.page.evaluate('window.hmsTest.open()')
        body = self.page.locator('#modal-body')
        self.assertIn('Delores', body.inner_text())
        self.assertIn('doesn’t bite', body.inner_text())
        self.assertEqual(self.page.locator('.hms-next').count(), 1)
        self.assertIn('Lesson 1 of 5', self.page.locator('.hms-next').inner_text())
        self.assertTrue(self.page.locator('#hms-tile-hotel').is_visible())
        self.assertTrue(self.page.locator('#hms-tile-browse').is_visible())
        self.assertFalse(self.page.locator('.hms-skill').is_visible())
        self.page.locator('#hms-more summary').click()
        self.assertTrue(self.page.locator('.hms-skill').is_visible())
        self.assertEqual(self.page.locator('#hms-lessons .hms-lesson').count(), 5)
        self.assertEqual(self.page.locator('#hms-games .hms-lesson').count(), 3)
        self.assertTrue(self.page.locator('#co-hms').is_visible())
        self.assertTrue(self.page.get_by_role('button', name='Explore on my own').is_visible())
        self.page.locator('#hms-next-go').click()
        self.page.wait_for_selector('#hms-say')
        self.assertIn('DESK COMPUTER LESSON 1', self.page.locator('#modal-body').inner_text().upper())

    def test_02_next_step_moves_on_after_the_lessons(self):
        self.page.evaluate('window.hmsTest.lessonsDone()')
        self.page.evaluate('window.hmsTest.open()')
        self.assertIn('e-course', self.page.locator('.hms-next').inner_text().lower())
        self.page.evaluate("phEval('course.passed=Date.now();hms.time=30;hms.best.build=5;hms.best.bill=5;')")
        self.page.evaluate('window.hmsTest.open()')
        self.assertIn('practice hotel', self.page.locator('.hms-next').inner_text().lower())
        self.page.locator('#hms-next-go').click()
        self.page.wait_for_selector('.ph-tile.hms-glow')
        self.assertIn('Pick a ✨ room', self.say())

    def test_03_room_board_has_six_colorful_tiles_and_tapping_acts(self):
        self.hotel()
        self.assertEqual(self.page.locator('.ph-tile').count(), 6)
        self.assertEqual([t.get_attribute('data-r') for t in self.page.locator('.ph-tile').all()], ['201', '202', '203', '204', '205', '206'])
        for kind in ('tidy', 'clean', 'ready', 'guest'):
            self.assertGreaterEqual(self.page.locator(f'.ph-tile.{kind}').count(), 1, kind)
        self.page.locator('.ph-tile[data-r="203"]').click()
        self.page.get_by_role('button', name='Housekeeping cleans it').click()
        self.assertIn('clean', self.page.locator('.ph-tile[data-r="203"]').get_attribute('class'))
        self.assertIn('supervisor', self.say())
        self.page.get_by_role('button', name='Supervisor inspects it').click()
        self.assertIn('ready', self.page.locator('.ph-tile[data-r="203"]').get_attribute('class'))

    def test_04_check_in_needs_a_ready_room_then_phone_email_card_before_keys(self):
        self.hotel()
        name = self.page.locator('.ph-guest b').first.inner_text()
        self.page.locator('.ph-guest .ph-in').first.click()
        self.page.locator('.ph-tile[data-r="204"]').click()  # cleaned, not inspected
        self.assertIn('not inspected', self.say())
        self.page.locator('.ph-tile[data-r="201"]').click()
        keys = self.page.locator('.ph-keys')
        self.assertTrue(keys.is_disabled())
        for k, word in ((0, 'area code'), (1, 'letter by letter'), (2, 'hold')):
            self.page.locator('.ph-ask').nth(k).click()
            self.assertIn(word, self.say())
        info = self.page.locator('.ph-info').inner_text()
        self.assertRegex(info, r'\(\d{3}\) 555-01\d\d')
        self.assertIn('@example.com', info)
        self.assertIn('••••', info)
        self.assertTrue(keys.is_enabled())
        keys.click()
        self.assertIn('guest', self.page.locator('.ph-tile[data-r="201"]').get_attribute('class'))
        self.assertIn(name.split(' ')[0], self.page.locator('.ph-tile[data-r="201"]').inner_text())

    def test_05_move_checkout_cancel_and_book_then_undo_all_of_it(self):
        self.hotel()
        start = self.page.evaluate("phEval('JSON.stringify({r:ph.rooms,w:ph.waiting.map(g=>g.id)})')")
        self.assertTrue(self.page.locator('#ph-undo').is_disabled())
        self.page.locator('.ph-tile[data-r="202"]').click()
        self.page.get_by_role('button', name='Move to another room').click()
        self.page.locator('.ph-tile[data-r="205"]').click()
        self.assertIn('guest', self.page.locator('.ph-tile[data-r="205"]').get_attribute('class'))
        self.assertIn('tidy', self.page.locator('.ph-tile[data-r="202"]').get_attribute('class'))
        self.page.locator('.ph-tile[data-r="206"]').click()
        self.page.get_by_role('button', name='Check out').click()
        self.assertIn('tidy', self.page.locator('.ph-tile[data-r="206"]').get_attribute('class'))
        self.page.locator('.ph-guest .ph-x').first.click()
        self.assertIn('cancellation policy', self.say())
        self.page.locator('.ph-new').click()
        self.assertIn('Undo (4)', self.page.locator('#ph-undo').inner_text())
        for _ in range(4):
            self.page.locator('#ph-undo').click()
        self.assertEqual(self.page.evaluate("phEval('JSON.stringify({r:ph.rooms,w:ph.waiting.map(g=>g.id)})')"), start)
        self.assertTrue(self.page.locator('#ph-undo').is_disabled())

    def test_06_nothing_counts_in_the_practice_hotel(self):
        before = self.page.evaluate("phEval('JSON.stringify([hms.xp,joy.tips])')")
        self.hotel()
        self.page.locator('.ph-guest .ph-in').first.click()
        self.page.locator('.ph-tile[data-r="201"]').click()
        for k in range(3):
            self.page.locator('.ph-ask').nth(k).click()
        self.page.locator('.ph-keys').click()
        self.assertEqual(self.page.evaluate("phEval('JSON.stringify([hms.xp,joy.tips])')"), before)
        self.assertNotIn('ph', self.page.evaluate('Object.keys(localStorage).join(",")').split(','))

    def test_07_phone_layout_fits(self):
        self.context.close()
        self.setUp(viewport={'width': 375, 'height': 760})
        for open_js in ('hmsTest.open()', "phEval('openPracticeHotel()')"):
            self.page.evaluate(open_js)
            self.page.wait_for_timeout(150)
            w = self.page.evaluate('document.querySelector("#modal").scrollWidth - document.querySelector("#modal").clientWidth')
            self.assertLessEqual(w, 1, open_js)

    def test_08_spanish_words_are_complete(self):
        missing = self.page.evaluate("""phEval(`(()=>{const out=[];const walk=(a,b,p)=>{for(const k of Object.keys(a)){if(!(k in b))out.push(p+k);else if(a[k]&&typeof a[k]==='object')walk(a[k],b[k],p+k+'.');}};walk(HF_TEXT.en,HF_TEXT.es,'');return out;})()`)""")
        self.assertEqual(missing, [])


for _name in [n for n in list(vars(hbase.Hms)) + list(vars(base.Growth)) if n.startswith('test_')]:
    setattr(Friendly, _name, None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
