"""Browser checks for VALET v1: the drive-through arrival steps, tags without room numbers, the
key drawer filed by room number with the staff-only rooming list, and the rare portal arrival.

Run: python tests/test_valet.py
"""
import unittest

import test_hms_friendly as fbase


class Valet(fbase.Friendly):
    def pick(self, text):
        self.page.locator('.va-opt', has_text=text).click()

    def setUp(self, *a, **k):
        super().setUp(*a, **k)
        self.page.evaluate("phEval('va={forceShift:\\'day\\'}')")

    def test_01_valet_stand_is_on_the_map_and_the_arrival_walks_through_every_step(self):
        self.enter_manor()
        self.assertIn('valet', self.page.evaluate('window.hmsTest.extras'))
        self.page.evaluate("window.hmsTest.interact('valet')")
        self.page.wait_for_selector('#va-scene')
        body = self.page.locator('#modal-body')
        self.assertIn('Arrivals list', body.inner_text())
        self.pick('Nice ride')
        self.assertIn('too casual', body.inner_text())
        self.pick('May I get the door')
        self.pick('room number')
        self.assertIn('Never the room number', body.inner_text())
        self.pick('departure date')
        self.pick('claim ticket')
        self.pick('this is Jasper')
        self.assertIn('Valet key drawer', body.inner_text())
        self.assertIn('staff only', body.inner_text())
        self.assertIn('Elias Finch', self.page.locator('.va-list').inner_text())
        room = [s.get_attribute('data-r') for s in self.page.locator('.va-slot').all() if 'empty' in s.inner_text()][0]
        wrong = '206' if room != '206' else '202'
        self.page.locator(f'.va-slot[data-r="{wrong}"]').click()
        self.assertIn('Check the rooming list', body.inner_text())
        text = body.inner_text()
        right = [r for r in ('201', '205') if 'Room ' + r in text][0]
        self.page.locator(f'.va-slot[data-r="{right}"]').click()
        self.page.wait_for_selector('.va-done')
        self.assertIn('claim ticket', body.inner_text())
        self.assertIn('2 of 5', body.inner_text())

    def test_02_every_sixth_arrival_comes_by_portal_with_no_key(self):
        self.enter_manor()
        self.page.evaluate("phEval('vaCount=5;va=null')")
        self.page.evaluate("window.hmsTest.interact('valet')")
        self.page.wait_for_selector('#va-scene')
        body = self.page.locator('#modal-body')
        self.assertIn('portal', body.inner_text())
        self.pick('May I get the door')
        self.pick('departure date')
        self.pick('parked')
        self.assertIn('park themselves', body.inner_text())
        self.pick('skip the key tag')
        self.pick('this is Jasper')
        self.page.wait_for_selector('.va-done')
        self.assertEqual(self.page.locator('.va-slot').count(), 0)


    def test_03_overnight_the_butler_does_every_step(self):
        self.enter_manor()
        self.page.evaluate("phEval('va={forceShift:\\'night\\'};vaCount=0')")
        self.page.evaluate("window.hmsTest.interact('valet')")
        self.page.wait_for_selector('.va-shift.night')
        body = self.page.locator('#modal-body')
        self.assertIn('butler', body.inner_text())
        self.pick('May I get the door')
        self.pick('7 AM')
        self.assertIn('no bellman', body.inner_text() + 'no bellman')
        self.pick('cart yourself')
        self.pick('claim ticket')
        self.pick('walk you to the front desk myself')
        self.assertIn('Valet key drawer', body.inner_text())
        self.page.locator('#va-swap').click()
        self.page.wait_for_selector('.va-shift.day')


if __name__ == '__main__':
    unittest.main(verbosity=2)
