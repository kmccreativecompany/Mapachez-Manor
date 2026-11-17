"""Browser checks for the gentle, dreamy voice (HEART v1): the nightly thought on the title,
warm verdicts, the goodbye line after a quick shift, glimmers, notes, rare keepsakes and the
keepsake journal.

Run: python tests/test_heart.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import json
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'heartTest',{get:()=>({
 heart:structuredClone(heart),text:HEART,growth:structuredClone(growth),
 drop:(kind)=>{const p=state.player;glimmer={x:p.x,y:p.y,kind,born:0};},
 grab:()=>interact('glimmer'),hasGlimmer:!!glimmer,
 extras:world.options.extras().map(e=>e.id),close:()=>closeModal()
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class Heart(base.Growth):
    """Reuses the growth harness but none of its tests."""

    def h(self):
        return self.page.evaluate('window.heartTest')

    def enter_manor(self):
        self.page.locator('#begin').click()
        self.page.wait_for_function('window.heartTest.growth && document.getElementById("game-shell").hidden===false')
        self.page.evaluate('window.heartTest.close()')

    def test_01_title_has_one_gentle_thought_and_no_type_labels(self):
        thought = self.page.locator('#heart-thought').inner_text()
        self.assertTrue(any(t in thought for t in self.h()['text']['thoughts']))
        self.assertEqual(self.page.locator('.heart-motes i').count(), 9)
        words = self.page.evaluate('document.body.innerText') + json.dumps(self.h()['text'])
        for word in ('INFP', '4w5', 'Enneagram', 'Myers', 'personality'):
            self.assertNotIn(word, words, 'The personality is shown, never named')

    def test_02_verdicts_are_warm_and_the_shift_ends_softly(self):
        text = self.h()['text']
        self.page.locator('#title-quick').click()
        for n in range(5):
            self.answer(best=n % 2 == 0)
            verdict = self.page.locator('.gm-result .gm-verdict').inner_text()
            if self.page.locator('.gm-silly-note').count() == 0:
                pool = text['best'] if n % 2 == 0 else text['ok'] + text['miss']
                self.assertTrue(any(line in verdict for line in pool), verdict)
            if n % 2:
                self.assertIn('come back soon', self.page.locator('.gm-result').inner_text())
                self.assertIn('BEST ANSWER', self.page.locator('.gm-result').inner_text())
            self.next_button()
        self.page.wait_for_selector('.gm-heart')
        self.assertTrue(any(line in self.page.locator('.gm-heart').inner_text() for line in text['goodbye']))

    def test_03_glimmers_notes_and_rare_finds_fill_the_journal(self):
        self.enter_manor()
        self.page.evaluate('window.heartTest.drop("light")')
        self.assertIn('glimmer', self.h()['extras'])
        self.page.evaluate('window.heartTest.grab()')
        self.assertIn('Little wonders: 1 of 30', self.page.locator('#toast').inner_text())
        self.page.evaluate('window.heartTest.drop("note")')
        self.page.evaluate('window.heartTest.grab()')
        self.assertIn('Notes found: 1 of 12', self.page.locator('#toast').inner_text())
        self.page.evaluate('window.heartTest.drop("rare")')
        self.page.evaluate('window.heartTest.grab()')
        h = self.h()
        self.assertEqual((len(h['heart']['found']), len(h['heart']['notes']), len(h['heart']['rare'])), (1, 1, 1))
        self.assertFalse(h['hasGlimmer'])
        self.assertIn('one-of-a-kind', h['growth']['pins'])
        saved = json.loads(self.page.evaluate("localStorage.getItem('mapachez_heart_v1')"))
        self.assertEqual(len(saved['rare']), 1)
        self.page.locator('#keepsakes-button').click()
        self.page.wait_for_selector('.heart-journal')
        self.assertEqual(self.page.locator('.heart-list li.found').count(), 3)
        self.assertEqual(self.page.locator('.heart-list li.blank').count(), 30 + 12 + 6 - 3)

    def test_04_welcome_back_after_a_day_away(self):
        self.page.evaluate("localStorage.setItem('mapachez_heart_v1',JSON.stringify({version:1,found:[2,99,'x'],notes:[],rare:[],lastVisit:'2020-01-01'}))")
        self.page.reload()
        self.assertIn('kept a lamp on', self.page.locator('#heart-thought').inner_text())
        self.assertEqual(self.h()['heart']['found'], [2], 'Bad saved data is cleaned up')
        self.page.reload()
        self.assertNotIn('kept a lamp on', self.page.locator('#heart-thought').inner_text())


class HeartPhone(base.Growth):
    enter_manor = Heart.enter_manor

    def setUp(self, viewport=None):
        super().setUp(viewport={'width': 390, 'height': 844})

    def test_05_title_and_journal_fit_a_phone(self):
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 390)
        self.enter_manor()
        self.page.locator('#keepsakes-button').click()
        self.page.wait_for_selector('.heart-journal')
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 390)


for name in [n for n in dir(base.Growth) if n.startswith('test_')]:
    setattr(Heart, name, None)
    setattr(HeartPhone, name, None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
