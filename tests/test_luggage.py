"""Browser checks for LUGGAGE v1: the locked luggage room (master key or code), name + departure
tags (never a room number), bag delivery, the practice clock and 4 PM check-in, impatient guests,
the snag update, and the two make-believe programs.

Run: python tests/test_luggage.py
"""
import unittest

import test_hms_friendly as fbase


class Luggage(fbase.Friendly):
    def first_waiting(self, js):
        self.page.evaluate("phEval(\"ph.waiting[0]." + js + "\")")

    def pick_204(self):
        self.page.locator('.ph-guest .ph-in').first.click()
        self.page.locator('.ph-tile[data-r="204"]').click()
        self.page.wait_for_selector('.rw-card')

    def test_01_clock_shows_4pm_rule_and_time_passes(self):
        self.hotel()
        clock = self.page.locator('#lg-clock')
        self.assertIn('1:00 PM', clock.inner_text())
        self.assertIn('Standard check-in is 4 PM', clock.inner_text())
        self.page.locator('.lg-why').click()
        self.assertIn('housekeeping has the whole day', self.say())
        for _ in range(6):
            self.page.locator('.lg-pass').click()
        self.assertIn('4:00 PM', clock.inner_text())
        self.assertIn('late', clock.get_attribute('class'))
        self.pick_204()
        self.assertIn('past 4 PM', self.page.locator('.lg-note').inner_text())

    def test_02_luggage_room_is_locked_code_opens_and_tags_never_show_room(self):
        self.hotel()
        self.assertIn('Locked', self.page.locator('#lg-room').inner_text())
        self.page.locator('.lg-code').click()
        for d in '123':
            self.page.locator(f'.lg-digit[data-d="{d}"]').click()
        self.assertIn('Not quite', self.say())
        for d in '416':
            self.page.locator(f'.lg-digit[data-d="{d}"]').click()
        self.assertIn('open', self.page.locator('#lg-room').get_attribute('class'))
        self.page.locator('.lg-lock').click()
        self.assertIn('Locked', self.page.locator('#lg-room').inner_text())

    def test_03_store_bags_then_check_in_then_deliver(self):
        self.hotel()
        self.pick_204()
        name = self.page.locator('.ph-guest b').first.inner_text()
        self.page.locator('.rw-opt[data-care="bags"]').click()
        self.assertIn('never the room number', self.say().lower().replace('never the room number', 'never the room number'))
        self.assertIn('Bags stored', self.page.locator('.ph-guest').first.inner_text())
        self.page.locator('.lg-key').click()
        bag = self.page.locator('.lg-bag').first
        self.assertIn(name, bag.inner_text())
        self.assertIn('Departs', bag.locator('.lg-tag').inner_text())
        self.assertNotIn('204', bag.locator('.lg-tag').inner_text())
        self.page.get_by_role('button', name='Radio the housekeeping supervisor').click()
        self.page.wait_for_selector('.ph-info', timeout=9000)
        for k in range(3):
            self.page.locator('.ph-ask').nth(k).click()
        self.page.locator('.ph-keys').click()
        self.assertIn('luggage room', self.say())
        self.page.locator('.lg-deliver').click()
        self.assertIn('Bell service', self.say())
        self.assertEqual(self.page.locator('.lg-bag').count(), 0)

    def test_04_impatient_guest_best_answer_is_empathy_why_and_honest_time(self):
        self.hotel()
        self.first_waiting('imp=1')
        self.pick_204()
        self.page.locator('[data-imp="blame"]').click()
        self.assertIn('Never blame a teammate', self.say())
        self.page.locator('[data-imp="calm"]').click()
        self.assertIn('Thank you for being honest', self.page.locator('.lg-imp').inner_text())

    def test_05_second_inspection_has_a_snag_and_you_update_the_guest(self):
        self.hotel()
        self.page.evaluate("phEval('ph.inspects=1')")
        self.pick_204()
        self.page.get_by_role('button', name='Radio the housekeeping supervisor').click()
        self.page.wait_for_selector('.lg-update', timeout=9000)
        self.assertIn('dripping faucet', self.say())
        self.page.locator('.lg-update').click()
        self.assertIn('fifteen more minutes', self.page.locator('.rw-you').inner_text())
        self.page.wait_for_selector('.ph-info', timeout=9000)
        self.assertIn('faucet is fixed', self.say())

    def test_06_programs_badge_benefits_and_lesson_quiz(self):
        self.hotel()
        self.first_waiting("prog='compass'")
        self.page.locator('.lg-pass').click()  # re-render
        self.page.locator('.lg-pass').click()
        self.assertIn('Compass Circle', self.page.locator('.ph-guest').first.inner_text())
        self.page.locator('.ph-guest .ph-in').first.click()
        self.page.locator('.ph-tile.ready').first.click()
        self.page.locator('.lg-prog').click()
        self.assertIn('travel advisor', self.say())
        self.page.locator('#lg-lesson summary').click()
        text = self.page.locator('#lg-lesson').inner_text()
        self.assertIn('consortia', text)
        self.assertIn('No guaranteed 4 PM late check-out', text)
        self.page.locator('.lg-q').first.locator('.lg-opt').nth(1).click()
        self.assertIn('Not quite', self.page.locator('.lg-q').first.inner_text())
        self.page.locator('.lg-q').first.locator('.lg-opt').nth(0).click()
        self.assertIn('Right', self.page.locator('.lg-q').first.inner_text())


if __name__ == '__main__':
    unittest.main(verbosity=2)
