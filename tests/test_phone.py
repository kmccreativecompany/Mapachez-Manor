"""Browser checks for PHONE v1: guest cards read like a chat on phones, the map fills the phone,
keyboard-only hints hide on touch screens, the hint pop-up sits at the top, and every training door
opens the manor's own desk computer instead of a separate practice app.

Run: python tests/test_phone.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'phoneTest',{get:()=>({toast:m=>toast(m),modal:h=>openModal(h)})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')

PHONE = {'viewport': {'width': 390, 'height': 664}, 'device_scale_factor': 1, 'is_mobile': True, 'has_touch': True}


class Phone(base.Growth):
    """Reuses the growth harness but none of its tests."""

    phone = True

    def setUp(self):
        if not self.phone:
            return super().setUp()
        self.context = self.browser.new_context(reduced_motion='reduce', **PHONE)
        self.context.add_init_script("try{if(!localStorage.getItem('mapachez_profile_v1'))localStorage.setItem('mapachez_profile_v1',JSON.stringify({version:1,mode:'solo',lang:'en',hooked:true}))}catch(e){}")
        # Returning-player fixture: the whole manor is open (night-by-night unlocks are covered in test_nights.py).
        self.context.add_init_script("try{if(!localStorage.getItem('mapachez_nights_v1'))localStorage.setItem('mapachez_nights_v1',JSON.stringify({all:true,seen:10,fresh:[]}))}catch(e){}")
        self.page = self.context.new_page()
        self.errors, self.requests = [], []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        self.page.route('**/*', self.route)
        self.page.goto(self.url)

    def open_guest(self):
        self.page.locator('#title-quick').click()
        self.page.wait_for_selector('#modal-body .choice')
        self.page.wait_for_timeout(50)

    def enter_manor(self):
        self.page.locator('#begin').click()
        self.page.wait_for_timeout(300)
        if self.page.locator('#modal').evaluate('m=>m.open'):
            self.page.keyboard.press('Escape')
        self.page.wait_for_timeout(200)

    def test_01_guest_card_is_a_speech_bubble_with_big_buttons_and_details_behind_a_tap(self):
        self.open_guest()
        b = self.page.locator('#modal-body')
        self.assertEqual(b.locator('.pc-bubble').count(), 1)
        self.assertEqual(b.locator(':scope > .scene-copy').count(), 0)
        title = self.page.locator('#modal-heading').inner_text()
        m = next(x for x in self.page.evaluate('window.growthTest.moments') if x['title'] == title)
        self.assertIn(m['situation'].split('"')[0].strip()[:30], b.locator('.pc-bubble').inner_text())
        more = b.locator('details.pc-more')
        self.assertEqual(more.count(), 1)
        self.assertFalse(more.evaluate('d=>d.open'))
        self.assertFalse(b.locator('.pc-more .scene-context').is_visible())
        more.locator('summary').click()
        self.assertTrue(b.locator('.pc-more .scene-context').is_visible())
        self.assertIn(m['guest'], b.locator('.pc-more .scene-context').inner_text())
        self.assertFalse(b.locator('.gm-ask').is_visible())
        heights = b.locator('.choice').evaluate_all('bs=>bs.map(x=>x.getBoundingClientRect().height)')
        self.assertGreaterEqual(len(heights), 3)
        self.assertTrue(all(h >= 56 for h in heights), heights)
        self.assertFalse(b.locator('.choice > span').first.is_visible(), 'Keyboard number badges hide on touch')

    def test_02_answering_on_a_phone_still_counts_and_shows_the_result(self):
        self.open_guest()
        self.answer(best=True)
        self.assertEqual(self.growth()['answers'], 1)
        self.assertTrue(self.page.locator('#modal-body .gm-result .action-row .primary-button').is_visible())
        self.next_button()
        self.page.wait_for_selector('#modal-body .pc-bubble')
        self.assertEqual(self.page.locator('#modal-body .pc-bubble').count(), 1)

    def test_03_map_fills_most_of_the_phone_and_keyboard_hints_hide(self):
        self.enter_manor()
        box = self.page.locator('#canvas-wrap').bounding_box()
        self.assertGreaterEqual(box['height'], 664 * 0.6)
        self.assertGreaterEqual(box['width'], 340)
        self.assertEqual(self.page.evaluate("[...document.querySelectorAll('kbd')].filter(k=>k.getClientRects().length).length"), 0)
        self.page.evaluate("phoneTest.modal('<p>hi</p>')")
        self.assertIn('Esc', self.page.locator('#modal-hint').inner_text())
        self.assertFalse(self.page.locator('#modal-hint').is_visible())

    def test_04_hint_pop_up_sits_at_the_top_not_over_buttons(self):
        self.enter_manor()
        self.page.evaluate("phoneTest.toast('Choose a request to walk there.')")
        self.page.wait_for_timeout(300)
        box = self.page.locator('#toast').bounding_box()
        self.assertLess(box['y'], 120)

    def test_05_training_doors_open_the_manor_desk_computer(self):
        self.assertFalse(self.page.locator('#title-training').is_visible(), 'Title keeps one desk button: Learn the HMS')
        self.enter_manor()
        self.page.locator('#training-button').click()
        self.page.wait_for_selector('.hms-skill')
        self.assertEqual(self.page.locator('iframe').count(), 0)
        self.assertEqual(self.page.locator('#hms-lessons .hms-lesson').count(), 5)
        self.assertEqual(self.page.locator('#hms-games .hms-lesson').count(), 3)
        self.assertNotIn('practice lab', self.page.locator('#modal-body').inner_text().lower())
        self.assertIn('Delores', self.page.locator('#modal-body').inner_text())


class Desktop(Phone):
    phone = False

    def test_01_guest_card_is_a_speech_bubble_with_big_buttons_and_details_behind_a_tap(self):
        self.open_guest()
        self.assertEqual(self.page.locator('#modal-body .pc-bubble').count(), 0)
        self.assertEqual(self.page.locator('#modal-body > .scene-copy').count(), 1)
        self.assertTrue(self.page.locator('#modal-body .gm-ask').is_visible())
        self.assertTrue(self.page.locator('#modal-body .choice > span').first.is_visible())

    def test_02_answering_on_a_phone_still_counts_and_shows_the_result(self):
        pass

    def test_03_map_fills_most_of_the_phone_and_keyboard_hints_hide(self):
        self.enter_manor()
        box = self.page.locator('#canvas-wrap').bounding_box()
        self.assertAlmostEqual(box['width'] / box['height'], 1280 / 880, delta=0.25)
        self.assertGreater(self.page.evaluate("[...document.querySelectorAll('kbd')].filter(k=>k.getClientRects().length).length"), 0)

    def test_04_hint_pop_up_sits_at_the_top_not_over_buttons(self):
        self.enter_manor()
        self.page.evaluate("phoneTest.toast('Hello')")
        self.page.wait_for_timeout(300)
        self.assertGreater(self.page.locator('#toast').bounding_box()['y'], 700)

    def test_06_t_key_opens_the_desk_computer(self):
        self.enter_manor()
        self.page.locator('#world').focus()
        self.page.keyboard.press('t')
        self.page.wait_for_selector('.hms-skill')
        self.assertEqual(self.page.locator('iframe').count(), 0)


for _name in [n for n in vars(base.Growth) if n.startswith('test_')]:
    setattr(Phone, _name, None)  # keep the growth helpers, skip the growth tests (test_growth.py runs them)

if __name__ == '__main__':
    unittest.main()
