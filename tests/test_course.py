"""Browser checks for COURSE v1: the Front Desk Check-In e-course (six lessons with a why for
every step, a final check that needs 5 of 6) and the on-device certificate with a LinkedIn link.

Run: python tests/test_course.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import unittest
from urllib.parse import urlparse, parse_qs

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'courseTest',{get:()=>({
 course:structuredClone(course),pins:Object.keys(growth.pins),joy:structuredClone(joy),
 open:()=>openCourse(),hms:()=>openHms(),setName:n=>{profile.name=n;storeProfile();},profileName:()=>profile.name,mod:n=>openCourseModule(n),final:()=>openCourseFinal(),cert:()=>openCourseCert(),
 rights:()=>CO.mods.map(m=>m.opts.find(o=>o[1])[0]),finalRights:()=>CO.final.map(q=>q.opts.find(o=>o[1])[0]),
 allMods:()=>{course.mods=[1,2,3,4,5,6];storeCourse();},
 normalise:v=>normaliseCourse(v),code:n=>courseCode(n),li:n=>courseLinkedIn(n)
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class Course(base.Growth):
    """Reuses the growth harness but none of its tests."""

    def c(self):
        return self.page.evaluate('window.courseTest')

    def answer_final(self, wrong=0):
        rights = self.page.evaluate('window.courseTest.finalRights()')
        for n in range(6):
            self.page.wait_for_selector('#co-choices .choice')
            q = self.page.locator('.co-q').inner_text()
            if n < wrong:
                self.page.locator('#co-choices .choice[data-ok="0"]').first.click()
            else:
                self.page.locator('#co-choices .choice[data-ok="1"]').click()
            self.assertTrue(q)
            self.page.locator('#co-actions .primary-button').click()
        self.assertTrue(rights)

    def test_01_title_and_desk_computer_open_the_course(self):
        self.assertIn('E-courses', self.page.locator('#co-title').inner_text())
        self.page.locator('#co-title').click()
        self.page.locator('#mc-open-chk').click()
        self.assertIn('Front Desk Check-In', self.page.locator('#modal-body').inner_text())
        self.assertEqual(self.page.locator('#co-mods .hms-lesson').count(), 6)
        self.assertTrue(self.page.locator('.co-final').is_disabled())
        self.page.evaluate('courseTest.hms()')
        self.page.locator('#hms-more summary').click()
        self.page.locator('#co-hms').click()
        self.assertIn('LESSONS', self.page.locator('#modal-body').inner_text().upper())

    def test_02_every_lesson_teaches_how_and_why_and_says_every_hms_differs(self):
        self.page.evaluate('courseTest.mod(1)')
        text = self.page.locator('#modal-body').inner_text()
        self.assertIn('Every hotel picks its own hotel management system', text)
        self.assertIn('Why it matters', text)
        self.assertEqual(self.page.locator('.co-path li').count(), 8)
        self.page.locator('#co-choices .choice', has_text='Finding the booking').click()
        self.assertIn('end of the path', self.page.locator('#co-msg').inner_text())
        self.page.locator('#co-choices .choice', has_text='room keys').click()
        c = self.c()
        self.assertEqual(c['course']['mods'], [1])
        self.assertIn('course-first', c['pins'])
        self.assertEqual(c['joy']['tips'], 2)
        rights = self.page.evaluate('courseTest.rights()')
        for n in range(2, 7):
            self.page.locator('#co-actions .primary-button').click()
            self.page.wait_for_selector('.co-why')
            self.assertIn(f'LESSON {n} OF 6', self.page.locator('#modal-body .overline').inner_text())
            self.page.evaluate('r => [...document.querySelectorAll("#co-choices .choice")].find(b => b.querySelector("b").textContent === r).click()', rights[n - 1])
        self.assertEqual(sorted(self.c()['course']['mods']), [1, 2, 3, 4, 5, 6])
        self.assertIn('final check', self.page.locator('#co-actions').inner_text().lower())

    def test_03_lesson_three_needs_the_area_code(self):
        self.page.evaluate('courseTest.mod(3)')
        self.assertIn('area code', self.page.locator('.co-phone').inner_text())
        self.page.locator('#co-choices .choice', has_text='555-0117').filter(has_not_text='(207)').first.click()
        self.assertIn('ten digits', self.page.locator('#co-msg').inner_text())

    def test_04_final_check_needs_five_of_six_and_can_be_retried(self):
        self.page.evaluate("courseTest.setName('Rosa Quill')")
        self.page.evaluate('courseTest.allMods()')
        self.page.evaluate('courseTest.final()')
        self.answer_final(wrong=2)
        self.assertIn('So close', self.page.locator('#modal-body').inner_text())
        c = self.c()['course']
        self.assertEqual(c['passed'], '')
        self.assertEqual(c['best'], 4)
        self.page.locator('#co-actions .primary-button', has_text='Try again').click()
        self.answer_final(wrong=1)
        self.assertIn('You mastered check-in', self.page.locator('#modal-body').inner_text())
        c = self.c()
        self.assertTrue(c['course']['passed'])
        self.assertIn('course-cert', c['pins'])

    def test_05_name_is_asked_before_the_final_check_and_locked_on_the_certificate(self):
        self.page.evaluate('courseTest.allMods()')
        self.page.evaluate('courseTest.open()')
        self.assertIn('Add your first and last name', self.page.locator('.co-remind').inner_text())
        self.page.evaluate('courseTest.final()')
        self.assertIn('Whose certificate is this?', self.page.locator('#modal-heading').inner_text())
        self.page.fill('#co-name', 'Rosa')
        self.page.locator('#co-name-row .primary-button').click()
        self.assertIn('first and last name', self.page.locator('#co-name-msg').inner_text())
        self.page.fill('#co-name', 'Rosa Quill')
        self.page.locator('#co-name-row .primary-button').click()
        self.answer_final()
        self.page.locator('#co-actions .primary-button', has_text='certificate').click()
        self.page.wait_for_selector('#co-cert')
        body = self.page.locator('#modal-body').inner_text()
        self.assertIn('not an accreditation', body)
        self.assertIn('locked', body)
        self.assertEqual(self.page.locator('#co-name').count(), 0)
        self.assertEqual(self.c()['course']['name'], 'Rosa Quill')
        # Changing the profile name later doesn't change the certificate.
        self.page.evaluate("courseTest.setName('Someone Else')")
        self.page.evaluate('courseTest.cert()')
        code = self.page.evaluate("courseTest.code('Rosa Quill')")
        self.assertRegex(code, r'^SKC-CHK-[0-9A-Z]{4}-[0-9A-Z]{4}$')
        href = self.page.locator('.cs-add').get_attribute('href')
        u = urlparse(href)
        self.assertEqual(u.netloc, 'www.linkedin.com')
        q = parse_qs(u.query)
        self.assertEqual(q['startTask'], ['CERTIFICATION_NAME'])
        self.assertEqual(q['certId'], [code])
        self.assertIn('Front Desk Check-In & Guest Registration Fundamentals', q['name'][0])
        self.assertIn('Silver Key Certificate', q['name'][0])
        self.assertEqual(q['organizationName'], ['KMC Creative Company, LLC'])
        with self.page.expect_download() as d:
            self.page.locator('#co-actions .primary-button', has_text='Save the picture').click()
        self.assertTrue(d.value.suggested_filename.endswith('.png'))
        filled = self.page.evaluate("(()=>{const c=document.getElementById('co-cert').getContext('2d').getImageData(600,330,1,1).data;return c[3]})()")
        self.assertGreater(filled, 0)

    def test_05b_passing_without_a_name_lets_you_add_it_once(self):
        self.page.evaluate('courseTest.allMods()')
        self.page.evaluate('courseTest.final()')
        self.page.locator('#co-name-row .secondary-button').click()
        self.answer_final()
        self.page.locator('#co-actions .primary-button', has_text='certificate').click()
        self.assertEqual(self.page.locator('#co-actions', has_text='Save the picture').count(), 0)
        self.page.fill('#co-name', 'June Glowe')
        self.page.locator('#co-name-row .primary-button').click()
        self.page.wait_for_selector('.co-locked')
        self.assertEqual(self.c()['course']['name'], 'June Glowe')
        self.assertEqual(self.page.locator('#co-name').count(), 0)

    def test_06_saves_recover_from_junk(self):
        self.assertEqual(self.page.evaluate("courseTest.normalise('nope').mods"), [])
        c = self.page.evaluate("courseTest.normalise({version:1,mods:[1,2,99,'x',2],best:40,passed:'yesterday',salt:'<b>',name:'Nope Person'})")
        self.assertEqual(c['mods'], [1, 2])
        self.assertEqual(c['best'], 6)
        self.assertEqual(c['passed'], '')
        self.assertEqual(c['salt'], '')
        self.assertEqual(c['name'], '')

    def test_07_phone_layout_fits(self):
        self.context.close()
        self.setUp({'width': 390, 'height': 844})
        self.page.evaluate('courseTest.allMods()')
        for js in ('courseTest.open()', 'courseTest.mod(5)', 'courseTest.final()'):
            self.page.evaluate(js)
            self.page.wait_for_timeout(150)
            w = self.page.evaluate('document.querySelector("#modal").scrollWidth - document.querySelector("#modal").clientWidth')
            self.assertLessEqual(w, 1, js)


if __name__ == '__main__':
    unittest.main()
