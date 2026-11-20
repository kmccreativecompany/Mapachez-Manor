"""Browser checks for KNOCK v1: closed guest rooms, knocking with your role, guests caught
mid-activity, Do Not Disturb signs (text first), and asking for a phone number at check-in.

Run: python tests/test_knock.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'knockTest',{get:()=>({
 knock:structuredClone(knock),joy:structuredClone(joy),pins:Object.keys(growth.pins),dnd:dndRooms(),
 play:()=>{state.flags.briefed=true;state.phase='playing';},
 interact:id=>interact(id),lesson:n=>startLesson(n),
 setKnock:o=>{Object.assign(knock,o);storeKnock();},
 seedFor:room=>{for(let s=1;s<2000;s++){state.seed=s;if(dndRooms()[0]===room)return s;}return 0;},
 role:r=>{profile.role=r;},
 normalise:v=>normaliseKnock(v)
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class Knock(base.Growth):
    """Reuses the growth harness but none of its tests."""

    def k(self):
        return self.page.evaluate('window.knockTest')

    def enter_manor(self):
        self.page.locator('#begin').click()
        self.page.wait_for_timeout(300)
        if self.page.locator('#modal').evaluate('m=>m.open'):
            self.page.keyboard.press('Escape')
        self.page.evaluate('window.knockTest.play()')

    def body(self):
        return self.page.locator('#modal-body').inner_text()

    def test_01_knocking_names_your_role_and_the_guest_is_mid_activity(self):
        self.enter_manor()
        self.page.evaluate("window.knockTest.role('house')")
        self.page.evaluate("window.knockTest.interact('r202')")
        self.page.wait_for_selector('#modal-body .knock-strip')
        line = self.page.locator('.knock-line').inner_text()
        self.assertIn('Knock, knock.', line)
        self.assertIn('Housekeeping!', line)
        self.assertIn('Mr. Finch', line)
        self.assertIn('rehearse', self.body())  # the story scene is still there
        k = self.k()['knock']
        self.assertEqual(k['knocks'], 1)
        self.assertEqual(k['doors'], [202])

    def test_02_dining_role_says_in_room_dining_and_empty_rooms_stay_quiet(self):
        self.enter_manor()
        self.page.evaluate("window.knockTest.role('dining')")
        self.page.evaluate("window.knockTest.interact('r205')")
        self.page.wait_for_selector('.knock-line')
        line = self.page.locator('.knock-line').inner_text()
        self.assertIn('In-Room Dining!', line)
        self.assertIn('No answer', line)

    def test_03_no_signs_until_two_knocks_then_one_door_each_shift(self):
        self.enter_manor()
        self.assertEqual(self.k()['dnd'], [])
        self.page.evaluate('window.knockTest.setKnock({knocks:2})')
        dnd = self.k()['dnd']
        self.assertEqual(len(dnd), 1)
        self.assertIn(dnd[0], [202, 203, 204, 206])

    def test_04_do_not_disturb_teaches_text_first_and_a_kind_clear_text(self):
        self.enter_manor()
        self.page.evaluate('window.knockTest.setKnock({knocks:2})')
        room = self.k()['dnd'][0]
        self.page.evaluate(f"window.knockTest.interact('r{room}')")
        self.page.wait_for_selector('[data-how]')
        self.assertIn('Please do not disturb', self.body())
        self.assertEqual(self.page.locator('#knock-how .choice').count(), 3)
        self.page.click('[data-how="call"]')
        self.assertIn('A text waits quietly', self.page.locator('.knock-msg').inner_text())
        self.assertEqual(self.k()['knock']['calls'], 1)
        self.page.click('[data-how="text"]')
        self.page.wait_for_selector('.kp-choice')
        self.assertIn('555-01', self.page.locator('.kp-top').inner_text())
        self.page.click('[data-text="vague"]')
        self.assertIn('Who is this', self.page.locator('#kp-chat').inner_text())
        self.page.click('[data-text="good"]')
        self.page.wait_for_selector('text=Head in')
        k = self.k()
        self.assertEqual(k['knock']['kind'], 1)
        self.assertEqual(k['dnd'], [])
        self.assertEqual(k['joy']['tips'], 3)
        self.assertIn('knock-quiet', k['pins'])
        self.page.click('text=Head in')
        self.page.wait_for_selector('#modal-body .knock-strip')

    def test_05_check_in_needs_phone_with_area_code_email_and_card_before_keys(self):
        self.page.evaluate('window.knockTest.lesson(5)')
        for act in ('tab:bookings', 'booking:juniper', 'checkin:juniper', 'pick:201'):
            self.page.locator(f'#modal-body [data-act="{act}"]').first.click()
        self.page.wait_for_selector('.ci-card')
        card = self.page.locator('.ci-card')
        self.assertIn('Before the keys', card.inner_text())
        self.assertIn('Every HMS looks a little different', card.inner_text())
        self.assertTrue(self.page.locator('.ci-keys').is_disabled())
        self.assertNotIn('201', self.k()['knock']['checked'].get('juniper', ''))
        # Saving the number without its area code is a gentle miss.
        self.page.locator('.ci-step .choice', has_text='Save 555-0117').click()
        self.assertIn('area code', self.page.locator('.ci-step .hms-msg').inner_text())
        self.page.locator('.ci-step .choice', has_text='And the area code').click()
        self.assertIn('(207) 555-0117', card.inner_text())
        self.assertIn('text guests', self.page.locator('.ci-why').inner_text())
        self.page.locator('.ci-step .choice', has_text='exmaple').click()
        self.assertIn('Read it back', self.page.locator('.ci-step .hms-msg').inner_text())
        self.page.locator('.ci-step .choice').filter(has_text='juniper.glow@example.com').click()
        self.assertIn('•••• •••• •••• 4242', self.page.locator('.ci-cc').inner_text())
        self.page.locator('.ci-step .choice', has_text='sticky note').click()
        self.assertIn('Never write a card number down', self.page.locator('.ci-step .hms-msg').inner_text())
        self.page.locator('.ci-step .choice', has_text='Check name and date').click()
        self.assertFalse(self.page.locator('.ci-keys').is_disabled())
        self.page.click('.ci-keys')
        self.page.wait_for_selector('.hms-done')
        k = self.k()
        self.assertEqual(k['knock']['phones']['juniper'], '(207) 555-0117')
        self.assertEqual(k['knock']['emails']['juniper'], 'juniper.glow@example.com')
        self.assertTrue(k['knock']['cards']['juniper'])
        self.assertEqual(k['knock']['checked']['juniper'], '201')
        self.assertIn('knock-number', k['pins'])
        self.page.locator('#modal-body [data-act="guest:juniper"]').first.click()
        profile = self.page.locator('.hms-body .hms-card').inner_text()
        self.assertIn('(207) 555-0117', profile)
        self.assertIn('juniper.glow@example.com', profile)
        self.assertIn('4242', profile)
        self.assertNotIn('4242 4242', profile)

    def test_06_no_number_on_file_gives_a_gentle_lesson_and_a_note_under_the_door(self):
        self.enter_manor()
        self.page.evaluate("window.knockTest.setKnock({knocks:2,checked:{juniper:'201'},phones:{juniper:''}})")
        self.assertTrue(self.page.evaluate('window.knockTest.seedFor(201)'))
        self.page.evaluate("window.knockTest.interact('r201')")
        self.page.click('[data-how="text"]')
        self.page.wait_for_selector('.knock-lesson')
        self.assertIn('ask for a phone number at check-in', self.body())
        self.page.click('text=Slide a note under the door')
        self.assertEqual(self.k()['knock']['notes'], 1)
        self.assertEqual(self.k()['dnd'], [])
        self.page.keyboard.press('Escape')
        self.page.evaluate("window.knockTest.interact('r201')")
        self.page.wait_for_selector('#modal-body .knock-strip')
        self.assertIn('Juniper Glow', self.body())
        self.assertIn('Knock, knock.', self.body())

    def test_07_saves_recover_from_junk(self):
        self.assertEqual(self.page.evaluate("window.knockTest.normalise('nope').knocks"), 0)
        old = self.page.evaluate("window.knockTest.normalise({version:1,phones:{juniper:'555-0117'}})")
        self.assertEqual(old['phones']['juniper'], '(207) 555-0117')
        k = self.page.evaluate("window.knockTest.normalise({version:1,knocks:-4,doors:[202,999],phones:{juniper:'123'},emails:{juniper:'x@y'},cards:{juniper:'yes'},checked:{juniper:'777'}})")
        self.assertNotIn('juniper', k['emails'])
        self.assertNotIn('juniper', k['cards'])
        self.assertEqual(k['knocks'], 0)
        self.assertEqual(k['doors'], [202])
        self.assertEqual(k['phones']['juniper'], '')
        self.assertNotIn('juniper', k['checked'])

    def test_08_phone_layout_fits(self):
        self.context.close()
        self.setUp({'width': 390, 'height': 844})
        self.enter_manor()
        self.page.evaluate('window.knockTest.setKnock({knocks:2})')
        room = self.k()['dnd'][0]
        self.page.evaluate(f"window.knockTest.interact('r{room}')")
        self.page.click('[data-how="text"]')
        self.page.wait_for_selector('.kp')
        width = self.page.evaluate('document.documentElement.scrollWidth')
        self.assertLessEqual(width, 390)


if __name__ == '__main__':
    unittest.main(verbosity=2)
