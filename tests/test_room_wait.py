"""Browser checks for ROOM WAIT v1: in the practice hotel, picking a 🔍 or 🧹 room for a waiting
guest opens a help card (radio or text housekeeping), a short wait turns the room ✨, and while the
guest waits there are gracious choices, with an honest time estimate as the best one.

Run: python tests/test_room_wait.py
"""
import unittest

import test_hms_friendly as fbase


class RoomWait(fbase.Friendly):
    def pick_204(self):
        self.hotel()
        self.page.locator('.ph-guest .ph-in').first.click()
        self.page.locator('.ph-tile[data-r="204"]').click()
        self.page.wait_for_selector('.rw-card')

    def test_01_not_inspected_room_opens_a_help_card_not_a_dead_end(self):
        self.pick_204()
        card = self.page.locator('.rw-card')
        self.assertIn('needs an inspection first', card.inner_text())
        self.assertTrue(self.page.get_by_role('button', name='Radio the housekeeping supervisor').is_visible())
        self.assertTrue(self.page.get_by_role('button', name='Text the housekeeping supervisor').is_visible())
        self.assertEqual(self.page.locator('.rw-opt').count(), 6)
        self.assertIn('secure', card.inner_text())

    def test_02_radio_then_wait_flips_the_room_and_check_in_carries_on(self):
        self.pick_204()
        self.page.get_by_role('button', name='Radio the housekeeping supervisor').click()
        self.assertIn('Could you please inspect Room 204', self.page.locator('.rw-script').inner_text())
        self.assertEqual(self.page.locator('.ph-tile[data-r="204"].rw-calling').count(), 1)
        self.page.wait_for_selector('.ph-tile[data-r="204"].ready', timeout=9000)
        self.page.wait_for_selector('.ph-info')
        self.assertIn('inspected and ready', self.say())
        self.assertIn('finish checking in', self.say())

    def test_03_guest_care_choices_best_is_honest_time_and_text_puts_phone_on_file(self):
        self.pick_204()
        self.page.locator('.rw-opt[data-care="honest"]').click()
        self.assertIn('best one', self.say())
        self.assertIn('Best', self.page.locator('.rw-opt[data-care="honest"]').inner_text())
        self.page.locator('.rw-opt[data-care="sec"]').click()
        self.assertEqual(self.page.locator('.rw-opt.miss').count(), 1)
        self.page.locator('.rw-opt[data-care="text"]').click()
        self.assertIn('area code', self.page.locator('.rw-you').inner_text())
        self.page.get_by_role('button', name='Text the housekeeping supervisor').click()
        self.page.wait_for_selector('.ph-info', timeout=9000)
        self.assertIn('your room is ready', self.say())
        self.assertEqual(self.page.locator('.ph-ask.got').count(), 1)  # phone already on file

    def test_04_dirty_room_gets_a_rush_clean_and_room_cards_keep_quick_buttons(self):
        self.hotel()
        self.page.locator('.ph-tile[data-r="203"]').click()
        self.assertTrue(self.page.get_by_role('button', name='Housekeeping cleans it').is_visible())
        self.page.get_by_role('button', name='Radio housekeeping for a rush clean').click()
        self.page.wait_for_selector('.ph-tile[data-r="203"].ready', timeout=12000)

    def test_05_undo_after_inspection_still_works(self):
        self.pick_204()
        self.page.get_by_role('button', name='Radio the housekeeping supervisor').click()
        self.page.wait_for_selector('.ph-tile[data-r="204"].ready', timeout=9000)
        self.page.locator('#ph-undo').click()
        self.assertIn('clean', self.page.locator('.ph-tile[data-r="204"]').get_attribute('class'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
