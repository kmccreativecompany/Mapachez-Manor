"""Browser checks for the first minutes of play, from the 2026-11-26 review.

- After the first guest, "Explore the manor" asks for a name once, and Skip goes straight in
  (it used to ask twice, then ask a brand-new player whether to start over).
- On phones, the next thread sits right under the map.
- A returning player with an evening in progress sees "Continue" as the big gold button.
- Adding new core guest moments keeps a hotel pack's saved progress with the right scenario.

Run: python tests/test_first_minute.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
"""
import json
import unittest

import test_growth as base

PACK = {'version': 1, 'hotel': 'Test Inn', 'manager': 'Sam', 'rules': [], 'moments': [
    {'id': 'p1', 'title': 'House towel rule', 'guest': 'A guest', 'situation': 'A guest asks for pool towels.',
     'choices': [['Hand over two towels.', 44], ['Say no.', -20]], 'standard': 'Towels go out from the desk.'}]}


class FirstMinute(base.Growth):
    def setUp(self, viewport=None, fresh=True, init=None):
        self.context = self.browser.new_context(viewport=viewport or {'width': 1440, 'height': 1000}, reduced_motion='reduce')
        if init:
            self.context.add_init_script(init)
        self.page = self.context.new_page()
        self.errors, self.requests = [], []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        self.page.route('**/*', self.route)
        self.page.goto(self.url)

    def heading(self):
        return self.page.evaluate("document.querySelector('#modal[open]')?document.getElementById('modal-heading').innerText:null")

    def first_guest_then_explore(self):
        self.page.locator('#mode-solo').click()
        self.answer(best=True)
        self.page.locator('#modal-body button', has_text='Explore the manor').click()

    def test_01_explore_asks_for_a_name_once_and_skip_goes_straight_in(self):
        self.first_guest_then_explore()
        self.assertEqual(self.heading(), 'Your name, for your certificates')
        self.page.locator('#modal-body button', has_text='Skip for now').click()
        self.page.wait_for_timeout(300)
        self.assertIsNone(self.heading(), 'no second name box and no "A fresh evening?" question')
        self.assertTrue(self.page.locator('#game-shell').is_visible())

    def test_02_saving_a_name_also_goes_straight_in(self):
        self.first_guest_then_explore()
        self.page.locator('#co-name').fill('Ada Lovelace')
        self.page.locator('#modal-body button', has_text='Save my name').click()
        self.page.wait_for_timeout(300)
        self.assertIsNone(self.heading())
        self.assertTrue(self.page.locator('#game-shell').is_visible())

    def test_03_phone_next_step_sits_under_the_map(self):
        self.context.close()
        self.setUp(viewport={'width': 390, 'height': 664})
        self.first_guest_then_explore()
        self.page.locator('#modal-body button', has_text='Skip for now').click()
        step = self.page.locator('#next-step')
        step.wait_for(state='visible')
        box = step.bounding_box()
        self.assertLessEqual(box['y'] + box['height'], 664, 'the next step is on the first screen')
        self.assertIn('Take the night briefing', step.inner_text())
        step.click()
        self.page.wait_for_function("document.querySelector('#modal[open]')", timeout=8000)

    def test_04_desktop_keeps_the_sidebar_threads_only(self):
        self.first_guest_then_explore()
        self.page.locator('#modal-body button', has_text='Skip for now').click()
        self.assertFalse(self.page.locator('#next-step').is_visible())
        self.assertTrue(self.page.locator('#tasks .task-card').first.is_visible())

    def test_05_returning_player_sees_continue_as_the_main_button(self):
        self.first_guest_then_explore()
        self.page.locator('#modal-body button', has_text='Skip for now').click()
        self.page.wait_for_timeout(300)
        self.page.reload()
        self.page.locator('#continue').wait_for(state='visible')
        cls = self.page.evaluate("[...document.querySelectorAll('.title-actions > button:not([hidden])')].slice(0,2).map(b=>b.id+':'+b.className)")
        self.assertEqual(cls, ['continue:primary-button', 'begin:glass-button'])

    def test_06_new_player_still_sees_begin_as_the_main_button(self):
        self.page.locator('#mode-solo').click()
        self.page.keyboard.press('Escape')
        self.assertIn('primary-button', self.page.locator('#begin').get_attribute('class'))
        self.assertFalse(self.page.locator('#continue').is_visible())

    def test_07_hotel_pack_progress_follows_new_core_moments(self):
        self.context.close()
        seed = {'version': 1, 'pts': {'trust': 0, 'care': 0, 'team': 0}, 'answers': 2,
                'seen': {'3': {'best': 44, 'tries': 1, 'miss': False, 'due': 0, 'at': 0},
                         '52': {'best': 44, 'tries': 1, 'miss': False, 'due': 0, 'at': 0}}}
        profile = {'version': 1, 'mode': 'hotel', 'lang': 'en', 'hooked': True, 'packIds': ['p1']}
        self.setUp(init="try{if(!sessionStorage.getItem('seeded')){sessionStorage.setItem('seeded','1');"
                        f"localStorage.setItem('mapachez_growth_v1',{json.dumps(json.dumps(seed))});"
                        f"localStorage.setItem('mapachez_pack_v1',{json.dumps(json.dumps(PACK))});"
                        f"localStorage.setItem('mapachez_profile_v1',{json.dumps(json.dumps(profile))});}}}}catch(e){{}}")
        g = self.growth()
        core = len(self.page.evaluate('window.growthTest.moments')) - 1
        self.assertEqual(core, 64)
        self.assertIn('3', g['seen'], 'core progress stays put')
        self.assertIn(str(core), g['seen'], 'the pack scenario moved along with the new core moments')
        self.assertNotIn('52', g['seen'])
        self.assertEqual(json.loads(self.page.evaluate("localStorage.getItem('mapachez_growth_v1')"))['core'], 64)


# Reuse the growth harness, but none of its tests.
for _name in dir(base.Growth):
    if _name.startswith('test') and _name not in FirstMinute.__dict__:
        setattr(FirstMinute, _name, None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
