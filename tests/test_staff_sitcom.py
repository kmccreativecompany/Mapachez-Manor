"""Browser checks for nine unadvertised, naturally discovered staff conversations.

Run: python tests/test_staff_sitcom.py
Set CHROMIUM_PATH for a custom Chromium installation.
Reuses the isolated offline browser harness from test_growth.py.
"""
import json
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'sitcomTest',{get:()=>({
 catalog:STAFF_SITCOM,
 heard:[...staffSitcomHeard],
 next:()=>openStaffMoment(),
 desk:()=>desk(),
 clock:state?.minute ?? null,
 growthAnswers:growth.answers
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class StaffSitcom(base.Growth):
    """Only this feature's tests, not the inherited growth tests."""

    def test_01_nine_matching_episodes_bilingual_no_golf_cart(self):
        data = self.page.evaluate('window.sitcomTest.catalog')
        en, es = data['en']['episodes'], data['es']['episodes']
        self.assertEqual(len(en), 9)
        self.assertEqual([s['id'] for s in en], [s['id'] for s in es])
        for locale in (en, es):
            for episode in locale:
                self.assertGreaterEqual(len(episode['lines']), 7)
                self.assertTrue(episode['thought'])
                self.assertTrue(episode['thinker'])
        self.assertNotIn('golfcart', json.dumps(data).lower())

    def open_desk(self):
        self.page.locator('#begin').click()
        self.page.wait_for_selector('#game-shell:not([hidden])')
        self.page.evaluate('window.sitcomTest.desk()')

    def test_02_natural_desk_reveal_saved_scenes_and_repeat(self):
        self.assertEqual(self.page.locator('#title-staff-sitcom').count(), 0)
        self.assertNotIn('Staff sitcom', self.page.locator('#title-screen').inner_text())
        self.open_desk()
        self.page.get_by_role('button', name='Check in with the team').click()
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), 'The Five-Minute Meeting')
        self.assertEqual(self.page.locator('.staff-sitcom-lines li').count(), 3)
        self.page.get_by_role('button', name='Keep listening').click()
        self.assertIn('tomorrow', self.page.locator('.staff-sitcom-lines').inner_text().lower())
        self.assertIn('Private thought', self.page.locator('.staff-sitcom-thought').inner_text())
        self.assertIn('meeting', self.page.evaluate('window.sitcomTest.heard'))
        saved = json.loads(self.page.evaluate("localStorage.getItem('mapachez_staff_sitcom_v1')"))
        self.assertEqual(saved, {'version':1,'heard':['meeting']})
        self.assertEqual(self.page.evaluate('window.sitcomTest.growthAnswers'), 0)
        self.page.get_by_role('button', name='Back to the front desk').click()
        self.page.get_by_role('button', name='Check in with the team').click()
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), 'Employee of the Month')
        self.page.reload()
        self.page.locator('#begin').click()
        self.page.evaluate('window.sitcomTest.desk()')
        self.page.get_by_role('button', name='Check in with the team').click()
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), 'Employee of the Month')

    def test_03_corrupt_save_and_story_clock_stays_still(self):
        self.page.evaluate("localStorage.setItem('mapachez_staff_sitcom_v1', '{oops')")
        self.page.reload()
        self.assertEqual(self.page.evaluate('window.sitcomTest.heard'), [])
        self.open_desk()
        before = self.page.evaluate('window.sitcomTest.clock')
        self.page.get_by_role('button', name='Check in with the team').click()
        self.page.get_by_role('button', name='Keep listening').click()
        self.assertEqual(self.page.evaluate('window.sitcomTest.clock'), before)

    def test_04_mobile_surprise_fits(self):
        self.context.close()
        self.setUp({'width':390,'height':844})
        self.open_desk()
        self.page.get_by_role('button', name='Check in with the team').click()
        self.assertEqual(self.page.locator('.staff-sitcom-lines li').count(), 3)
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 390)
        box = self.page.locator('#modal').bounding_box()
        self.assertLessEqual(box['x'] + box['width'], 390)

for name in dir(base.Growth):
    if name.startswith('test_') and name not in StaffSitcom.__dict__:
        setattr(StaffSitcom,name,None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
