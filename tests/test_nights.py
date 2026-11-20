"""Browser checks for NEW NIGHTS v1: night one shows one simple loop (a shift, tips and
the cottage), each finished shift opens one more part of the manor, returning players
keep everything, and a setting opens it all at once.

Run: python tests/test_nights.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import unittest

import test_growth as base

FIRST_NIGHT_HIDDEN = ['#title-memories', '#explore-festival', '#hms-title', '#penny-title',
                      '#star-title', '#joy-title-mg', '#title-report']


class Nights(base.Growth):
    open_manor = False  # start like a brand-new player

    def shown(self, selector):
        return self.page.evaluate("q => { const e = document.querySelector(q); return !!e && getComputedStyle(e).display !== 'none'; }", selector)

    def play_shift(self, again=False):
        if again:
            self.page.locator('#shift-actions').get_by_role('button', name='Another quick shift').click()
        else:
            self.page.locator('#title-quick').click()
        for i in range(5):
            self.answer(best=True)
            self.next_button()
        self.page.wait_for_selector('.gm-summary')

    def test_01_night_one_is_one_simple_loop(self):
        for selector in ['#title-quick', '#begin', '#cottage-title']:
            self.assertTrue(self.shown(selector), selector + ' is part of night one')
        for selector in FIRST_NIGHT_HIDDEN:
            self.assertFalse(self.shown(selector), selector + ' waits for a later night')
        self.page.locator('#begin').click()
        self.page.wait_for_selector('#growth-shift')
        for selector in ['#growth-shift', '#joy-side-cottage']:
            self.assertTrue(self.shown(selector), selector)
        for selector in ['#training-button', '#memory-button', '#festival-button', '#joy-side-penny', '#joy-side-hms', '#growth-notebook']:
            self.assertFalse(self.shown(selector), selector)
        self.assertIn('Finish a shift', self.page.locator('#nn-next').inner_text())

    def test_02_each_shift_opens_one_new_thing_and_it_glows(self):
        self.play_shift()
        self.assertIn('New tonight', self.page.locator('#toast').inner_text())
        self.assertTrue(self.shown('#title-memories'), 'The Memory Book opens after night one')
        self.assertFalse(self.shown('#joy-title-mg'), 'Only one new thing per night')
        self.assertTrue(self.page.evaluate("document.documentElement.classList.contains('nn-new-book')"))
        self.play_shift(again=True)
        self.page.keyboard.press('Escape')
        self.assertFalse(self.shown('#hms-title'))
        self.assertEqual(self.page.evaluate("JSON.parse(localStorage.getItem('mapachez_nights_v1')).seen"), 2)
        self.page.reload()
        self.assertTrue(self.shown('#title-memories'), 'Unlocks persist across reloads')

    def test_03_setting_opens_everything_and_returning_players_keep_it_all(self):
        self.page.locator('#title-settings').click()
        self.page.locator('#nn-all').check()
        self.page.keyboard.press('Escape')
        for selector in FIRST_NIGHT_HIDDEN:
            self.assertTrue(self.shown(selector), selector)
        self.assertFalse(self.page.evaluate("[...document.documentElement.classList].some(c => c.startsWith('nn-'))"))
        # A player who already had progress before this update sees everything at once.
        self.page.evaluate("localStorage.removeItem('mapachez_nights_v1'); localStorage.setItem('mapachez_growth_v1', JSON.stringify(Object.assign(JSON.parse(localStorage.getItem('mapachez_growth_v1') || '{}'), {version: 1, answers: 3})))")
        self.page.reload()
        for selector in FIRST_NIGHT_HIDDEN:
            self.assertTrue(self.shown(selector), selector)

    def test_04_hotel_trainees_always_see_their_report(self):
        self.page.evaluate("const p = JSON.parse(localStorage.getItem('mapachez_profile_v1')); p.mode = 'hotel'; localStorage.setItem('mapachez_profile_v1', JSON.stringify(p))")
        self.page.reload()
        self.assertTrue(self.shown('#title-report'))
        self.assertFalse(self.shown('#title-training'))


# Run only the tests above, not the ones this class inherits from the growth harness.
for _name in dir(base.Growth):
    if _name.startswith('test_') and _name not in Nights.__dict__:
        setattr(Nights, _name, None)


if __name__ == '__main__':
    unittest.main()
