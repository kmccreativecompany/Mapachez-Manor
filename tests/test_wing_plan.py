"""Browser checks for WING PLAN v1: the six guest rooms face a sea view, a stair and elevator at
each end of the east wing, and two small meeting rooms with names of our own, each with a quick lesson.

Run: python tests/test_wing_plan.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
"""
import unittest

import test_cast as cbase


class WingPlan(unittest.TestCase):
    setUpClass = classmethod(cbase.Cast.setUpClass.__func__)
    tearDownClass = classmethod(cbase.Cast.tearDownClass.__func__)
    setUp = cbase.Cast.setUp
    route = cbase.Cast.route
    tearDown = cbase.Cast.tearDown

    def enter_manor(self):
        self.page.locator('#begin').click()
        self.page.wait_for_function('window.castTest && document.getElementById("game-shell").hidden===false')
        self.page.evaluate("document.querySelectorAll('dialog[open]').forEach(d=>d.close())")

    def test_01_still_six_rooms_and_every_spot_is_on_the_map(self):
        self.assertIn("const rooms=[270,430,590,750,910,1070];", cbase.HTML, 'Six guest rooms, 201 to 206')
        self.enter_manor()
        points = self.page.evaluate('window.castTest.points()')
        for spot in ('wing-west', 'wing-east', 'willow', 'iris', 'luggage', 'valet'):
            self.assertIn(spot, points)

    def test_02_meeting_room_lesson_has_a_quick_question(self):
        self.enter_manor()
        self.page.evaluate("window.castTest.interact('willow')")
        body = self.page.locator('#modal-body')
        self.assertIn('Willow Room', body.inner_text())
        self.assertIn('thirty minutes', body.inner_text())
        self.page.locator('#modal-body .choice', has_text='Boardroom').click()
        self.assertIn('Try the other one', self.page.locator('.wing-out').inner_text())
        self.page.locator('#modal-body .choice', has_text='Theater').click()
        self.assertIn('That’s it', self.page.locator('.wing-out').inner_text())

    def test_03_stairs_not_the_elevator_in_a_fire(self):
        self.enter_manor()
        self.page.evaluate("window.castTest.interact('wing-east')")
        self.assertIn('We offer, we never assume', self.page.locator('#modal-body').inner_text())
        self.page.locator('#modal-body .choice', has_text='The stairs').click()
        self.assertIn('safe way down', self.page.locator('.wing-out').inner_text())

    def test_04_names_are_our_own(self):
        block = cbase.HTML[cbase.HTML.index('/* ==== WING PLAN v1'):cbase.HTML.index('/* ==== end WING PLAN v1')]
        for word in ('Lodge', 'Atlantic', 'Simons', 'Spalding', 'Plantation', 'King Room', 'Page Room'):
            self.assertNotIn(word, block)


if __name__ == '__main__':
    unittest.main()
