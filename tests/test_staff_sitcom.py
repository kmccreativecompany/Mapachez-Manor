"""Browser checks for nine optional Mapáchez Manor staff sitcom scenes.

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
 menu:()=>openStaffSitcomMenu(),
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

    def test_02_title_menu_reveal_saved_episodes_and_replay(self):
        self.page.locator('#title-staff-sitcom').click()
        self.assertEqual(self.page.locator('.staff-sitcom-episode').count(), 9)
        self.page.locator('.staff-sitcom-episode').first.click()
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), 'The Five-Minute Meeting')
        self.assertEqual(self.page.locator('.staff-sitcom-lines li').count(), 3)
        self.page.get_by_role('button', name='Keep listening').click()
        self.assertIn('tomorrow', self.page.locator('.staff-sitcom-lines').inner_text().lower())
        self.assertIn('Private thought', self.page.locator('.staff-sitcom-thought').inner_text())
        self.assertIn('meeting', self.page.evaluate('window.sitcomTest.heard'))
        saved = json.loads(self.page.evaluate("localStorage.getItem('mapachez_staff_sitcom_v1')"))
        self.assertEqual(saved, {'version':1,'heard':['meeting']})
        self.assertEqual(self.page.evaluate('window.sitcomTest.growthAnswers'), 0)
        self.page.get_by_role('button', name='Back to staff room').click()
        self.assertIn('Heard', self.page.locator('.staff-sitcom-episode').first.inner_text())
        self.page.reload()
        self.page.locator('#title-staff-sitcom').click()
        self.assertIn('Heard', self.page.locator('.staff-sitcom-episode').first.inner_text())

    def test_03_desk_access_and_corrupt_save_recovery(self):
        self.page.evaluate("localStorage.setItem('mapachez_staff_sitcom_v1', '{oops')")
        self.page.reload()
        self.assertEqual(self.page.evaluate('window.sitcomTest.heard'), [])
        self.page.locator('#begin').click()
        self.page.wait_for_selector('#game-shell:not([hidden])')
        self.page.evaluate('window.sitcomTest.desk()')
        self.page.get_by_role('button', name='Overhear the staff room').click()
        self.assertEqual(self.page.locator('.staff-sitcom-episode').count(), 9)

    def test_04_mobile_menu_is_usable(self):
        self.context.close()
        self.setUp({'width':390,'height':844})
        self.page.locator('#title-staff-sitcom').click()
        self.assertEqual(self.page.locator('.staff-sitcom-episode').count(), 9)
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 390)
        box = self.page.locator('#modal').bounding_box()
        self.assertLessEqual(box['x'] + box['width'], 390)

for name in dir(base.Growth):
    if name.startswith('test_') and name not in StaffSitcom.__dict__:
        setattr(StaffSitcom,name,None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
