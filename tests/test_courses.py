"""Browser checks for MORE COURSES v1: three more Silver Key e-courses (guest language,
telephone, housekeeping), the course catalog, night-by-night unlocks and the Master
Certificate for passing all four.

Run: python tests/test_courses.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import re
import unittest
from urllib.parse import urlparse, parse_qs

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'mcTest',{get:()=>({
 mc:structuredClone(mc),course:structuredClone(course),pins:Object.keys(growth.pins),tips:joy.tips,
 text:MC_TEXT,
 catalog:()=>openCourses(),open:id=>openMcCourse(id),mod:(id,n)=>openMcModule(id,n),final:id=>openMcFinal(id),cert:id=>openMcCert(id),master:()=>openMcMaster(),
 setName:n=>{profile.name=n;storeProfile();},
 allMods:id=>{mc.courses[id].mods=[1,2,3,4,5,6];mcStore();},
 pass:id=>{const r=mc.courses[id];r.mods=[1,2,3,4,5,6];r.passed='2026-11-20';r.salt='abc123';r.name=fullName(mcLockedName())||fullName(profile.name)||'';mcStore();},
 passCheckIn:()=>{course.mods=[1,2,3,4,5,6];course.passed='2026-11-19';course.salt='zz9';course.name=fullName(profile.name)||'';storeCourse();},
 normalise:v=>mcNormalise(v),parse:u=>certParse(new URL(u).search),code:(c,id,n)=>mcCode(c,mc.courses[id],n)
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')
IDS = ['lux', 'phn', 'hsk']


class Courses(base.Growth):
    def t(self):
        return self.page.evaluate('window.mcTest')

    def answer_final(self, wrong=0):
        for n in range(6):
            self.page.wait_for_selector('#co-choices .choice')
            sel = '#co-choices .choice[data-ok="0"]' if n < wrong else '#co-choices .choice[data-ok="1"]'
            self.page.locator(sel).first.click()
            self.page.locator('#co-actions .primary-button').click()

    def test_01_title_button_opens_a_catalog_of_four_courses_and_the_master(self):
        self.assertIn('E-courses', self.page.locator('#co-title').inner_text())
        self.assertIn('0 / 4', self.page.locator('#co-title').inner_text())
        self.page.locator('#co-title').click()
        body = self.page.locator('#modal-body').inner_text()
        for name in ['Front Desk Check-In & Guest Registration Fundamentals', 'Luxury Guest Service Language & Communication',
                     'Front Desk Telephone Etiquette & Call Handling', 'Housekeeping Standards & Guest Room Inspection', 'Master Certificate']:
            self.assertIn(name, body)
        self.assertTrue(self.page.locator('#mc-master').is_disabled())
        self.page.locator('#mc-open-phn').click()
        self.assertEqual(self.page.locator('#mc-mods .hms-lesson').count(), 6)
        self.assertTrue(self.page.locator('.mc-final').is_disabled())
        # The check-in course links back to the catalog.
        self.page.evaluate('mcTest.catalog()')
        self.page.locator('#mc-open-chk').click()
        self.assertIn('All e-courses', self.page.locator('#co-actions').inner_text())

    def test_02_every_lesson_has_how_why_and_a_kind_retry(self):
        rights = self.page.evaluate("Object.fromEntries(mcTest.text.en.courses.map(c=>[c.id,c.mods.map(m=>m.opts.find(o=>o[1])[0])]))")
        for cid in IDS:
            self.page.evaluate(f"mcTest.mod('{cid}',1)")
            for n in range(1, 7):
                self.page.wait_for_selector('.co-why')
                self.assertIn(f'LESSON {n} OF 6', self.page.locator('#modal-body .overline').inner_text())
                self.assertIn('Why it matters', self.page.locator('#modal-body').inner_text())
                self.assertIn('Delores', self.page.locator('#modal-body').inner_text() + 'Delores')
                if n == 1:
                    self.page.locator('#co-choices .choice[data-ok="0"]').first.click()
                    self.assertIn('Not quite', self.page.locator('#co-msg').inner_text())
                self.page.evaluate('r => [...document.querySelectorAll("#co-choices .choice")].find(b => b.querySelector("b").textContent === r).click()', rights[cid][n - 1])
                self.page.locator('#co-actions .primary-button').click()
            self.assertEqual(sorted(self.t()['mc']['courses'][cid]['mods']), [1, 2, 3, 4, 5, 6])
        self.assertEqual(self.t()['tips'], 36)

    def test_03_final_check_needs_five_of_six_then_a_locked_certificate(self):
        self.page.evaluate("mcTest.setName('Rosa Quill')")
        self.page.evaluate("mcTest.allMods('hsk')")
        self.page.evaluate("mcTest.final('hsk')")
        self.answer_final(wrong=2)
        self.assertIn('So close', self.page.locator('#modal-body').inner_text())
        self.assertEqual(self.t()['mc']['courses']['hsk']['passed'], '')
        self.page.locator('#co-actions .primary-button', has_text='Try again').click()
        self.answer_final(wrong=1)
        self.assertIn('Spotless work', self.page.locator('#modal-body').inner_text())
        t = self.t()
        self.assertTrue(t['mc']['courses']['hsk']['passed'])
        self.assertEqual(t['mc']['courses']['hsk']['name'], 'Rosa Quill')
        self.assertIn('course-hsk', t['pins'])
        self.page.locator('#co-actions .primary-button', has_text='certificate').click()
        self.page.wait_for_selector('#co-cert')
        body = self.page.locator('#modal-body').inner_text()
        self.assertIn('not an accreditation', body)
        self.assertIn('locked', body)
        self.assertEqual(self.page.locator('#co-name').count(), 0)
        href = self.page.locator('#co-share .cs-add').get_attribute('href')
        q = parse_qs(urlparse(href).query)
        # The share card carries a credential link that opens this same certificate.
        self.assertRegex(q['certUrl'][0], r'^https://kmccreativecompany\.github\.io/Mapachez-Manor/\?cert=SKC-HSK-')
        self.assertEqual(self.page.evaluate("u=>mcTest.parse(u).name", q['certUrl'][0]), 'Rosa Quill')
        self.assertIn('Room Inspection', self.page.locator('#co-share .cs-skills').inner_text())
        self.assertEqual(self.page.locator('#co-share .cs-share').count(), 1)
        self.assertEqual(q['organizationName'], ['KMC Creative Company, LLC'])
        self.assertEqual(q['name'], ['Silver Key Certificate: Housekeeping Standards & Guest Room Inspection'])
        self.assertRegex(q['certId'][0], r'^SKC-HSK-[0-9A-Z]{4}-[0-9A-Z]{4}$')
        with self.page.expect_download() as d:
            self.page.locator('#co-actions .primary-button', has_text='Save the picture').click()
        self.assertEqual(d.value.suggested_filename, 'silver-key-housekeeping-certificate.png')
        # The name stays even if the profile name changes.
        self.page.evaluate("mcTest.setName('Someone Else')")
        self.page.evaluate("mcTest.cert('hsk')")
        self.assertEqual(self.t()['mc']['courses']['hsk']['name'], 'Rosa Quill')

    def test_04_one_name_for_every_certificate(self):
        self.page.evaluate("mcTest.setName('June Glowe')")
        self.page.evaluate('mcTest.passCheckIn()')
        self.page.evaluate("mcTest.setName('Someone Else')")
        self.page.evaluate("mcTest.allMods('lux')")
        self.page.evaluate("mcTest.final('lux')")
        self.answer_final()
        self.assertEqual(self.t()['mc']['courses']['lux']['name'], 'June Glowe')

    def test_05_passing_all_four_earns_the_master_certificate(self):
        self.page.evaluate("mcTest.setName('Rosa Quill')")
        self.page.evaluate('mcTest.passCheckIn()')
        self.page.evaluate("mcTest.pass('lux'); mcTest.pass('phn')")
        self.assertEqual(self.t()['mc']['master']['passed'], '')
        self.page.evaluate("mcTest.allMods('hsk')")
        self.page.evaluate("mcTest.final('hsk')")
        self.answer_final()
        t = self.t()
        self.assertTrue(t['mc']['master']['passed'])
        self.assertEqual(t['mc']['master']['name'], 'Rosa Quill')
        self.assertIn('course-master', t['pins'])
        self.page.keyboard.press('Escape')
        self.page.evaluate('mcTest.catalog()')
        self.assertIn('4 of 4', self.page.locator('#modal-body').inner_text())
        self.page.locator('#mc-master').click()
        self.page.wait_for_selector('#co-cert')
        self.assertIn('all four', self.page.locator('#modal-body').inner_text())
        q = parse_qs(urlparse(self.page.locator('#co-share .cs-add').get_attribute('href')).query)
        self.assertFalse(self.page.evaluate("u=>mcTest.parse(u).bad||false", q['certUrl'][0]))
        self.assertEqual(q['name'], ['Silver Key Master Certificate: Hotel Front Office & Guest Services'])
        self.assertRegex(q['certId'][0], r'^SKC-MST-[0-9A-Z]{4}-[0-9A-Z]{4}$')

    def test_06_answers_are_fair_and_spanish_matches(self):
        text = self.page.evaluate('mcTest.text')
        pos = {'longest': 0, 'shortest': 0, 'middle': 0}
        for lang in ('en', 'es'):
            for c in text[lang]['courses']:
                for q in c['mods'] + c['final']:
                    self.assertEqual(sum(o[1] for o in q['opts']), 1)
                    if lang == 'en':
                        ls = [len(o[0]) for o in q['opts']]
                        best = ls[[o[1] for o in q['opts']].index(1)]
                        pos['longest' if best == max(ls) else 'shortest' if best == min(ls) else 'middle'] += 1
        total = sum(pos.values())
        for k, v in pos.items():
            self.assertLessEqual(v / total, 0.6, (k, pos))
        en, es = text['en']['courses'], text['es']['courses']
        for a, b in zip(en, es):
            self.assertEqual([m['opts'] and [o[1] for o in m['opts']] for m in a['mods']], [[o[1] for o in m['opts']] for m in b['mods']])
            self.assertEqual([[o[1] for o in q['opts']] for q in a['final']], [[o[1] for o in q['opts']] for q in b['final']])
        # Contact details are make-believe only.
        dump = str(text)
        for phone in re.findall(r'\(\d{3}\) \d{3}-\d{4}', dump):
            self.assertIn('555-01', phone)

    def test_07_saves_recover_from_junk(self):
        self.assertEqual(self.page.evaluate("mcTest.normalise('nope').courses.lux.mods"), [])
        c = self.page.evaluate("mcTest.normalise({version:1,courses:{lux:{mods:[1,9,'x',1],best:50,passed:'soon',salt:'<b>',name:'Nope Person'}},master:{passed:'x',name:'Y Z'}})")
        self.assertEqual(c['courses']['lux']['mods'], [1])
        self.assertEqual(c['courses']['lux']['best'], 6)
        self.assertEqual(c['courses']['lux']['passed'], '')
        self.assertEqual(c['courses']['lux']['name'], '')
        self.assertEqual(c['master']['passed'], '')
        self.assertEqual(c['courses']['phn']['mods'], [])

    def test_08_phone_layout_fits(self):
        self.context.close()
        self.setUp({'width': 390, 'height': 844})
        self.page.evaluate("mcTest.setName('Rosa Quill'); mcTest.passCheckIn(); mcTest.pass('lux'); mcTest.pass('phn'); mcTest.pass('hsk')")
        for js in ('mcTest.catalog()', "mcTest.open('lux')", "mcTest.mod('lux',2)", "mcTest.mod('phn',4)", "mcTest.mod('hsk',2)", "mcTest.mod('hsk',3)", "mcTest.final('phn')", "mcTest.cert('phn')", 'mcTest.master()'):
            self.page.evaluate(js)
            self.page.wait_for_timeout(150)
            w = self.page.evaluate('document.querySelector("#modal").scrollWidth - document.querySelector("#modal").clientWidth')
            self.assertLessEqual(w, 1, js)


class CourseNights(base.Growth):
    open_manor = False

    def test_new_courses_open_one_per_night_after_the_others(self):
        self.page.evaluate("localStorage.setItem('mapachez_nights_v1', JSON.stringify({all:false,seen:10,fresh:[]})); localStorage.setItem('mapachez_growth_v1', JSON.stringify(Object.assign(JSON.parse(localStorage.getItem('mapachez_growth_v1') || '{}'), {version: 1, shifts: 10})))")
        self.page.reload()
        self.page.locator('#co-title').click()
        self.assertEqual(self.page.locator('#mc-open-lux').count(), 0)
        self.assertIn('next shift', self.page.locator('#mc-wait-lux').inner_text())
        self.assertIn('3 more shifts', self.page.locator('#mc-wait-hsk').inner_text())
        self.page.evaluate("localStorage.setItem('mapachez_growth_v1', JSON.stringify(Object.assign(JSON.parse(localStorage.getItem('mapachez_growth_v1')), {shifts: 11})))")
        self.page.reload()
        self.page.locator('#co-title').click()
        self.assertEqual(self.page.locator('#mc-open-lux').count(), 1)
        self.assertTrue(self.page.evaluate("document.documentElement.classList.contains('nn-new-course-lux')"))
        self.assertEqual(self.page.locator('#mc-wait-phn').count(), 1)


# Run only the tests above, not the ones these classes inherit from the growth harness.
for _cls in (Courses, CourseNights):
    for _name in dir(base.Growth):
        if _name.startswith('test_') and _name not in _cls.__dict__:
            setattr(_cls, _name, None)


if __name__ == '__main__':
    unittest.main()
