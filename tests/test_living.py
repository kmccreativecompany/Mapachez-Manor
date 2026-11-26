"""Browser checks for LIVING MANOR v1: daily routines, Manor Radio and little surprises.

Run: python tests/test_living.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import re
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'livTest',{get:()=>({
 living:structuredClone(living),tips:joy.tips,pins:Object.keys(growth.pins),text:LIV_TEXT,
 routines:LIV_ROUTINES.map(r=>r.id),surprises:LIV_SURPRISES.map(s=>s.id),
 hour:h=>{livHourOverride=h;return livRoutineNow().id;},
 play:()=>{state.flags.briefed=true;state.phase='playing';return world.options.extras().map(e=>e.id);},
 extras:()=>world.options.extras().map(e=>e.id),
 spawn:()=>{livClockMs=livNextMs;return livSpawn()?.id||null;},
 pending:()=>livPending&&livPending.id,
 go:id=>interact(id),close:()=>closeModal()
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')
SLANG = re.compile(r"\b(yep|yeah|okay|ok|sure|alright|no problem|you guys|gonna)\b", re.I)


class Living(base.Growth):
    """Reuses the growth harness but none of its tests."""

    def L(self):
        return self.page.evaluate('window.livTest')

    def enter(self):
        self.page.locator('#begin').click()
        self.page.wait_for_function('document.getElementById("game-shell").hidden===false')
        self.page.evaluate('livTest.close()')
        return self.page.evaluate('livTest.play()')

    def test_01_a_different_routine_every_three_hours(self):
        self.assertEqual(len(self.L()['routines']), 8)
        seen = [self.page.evaluate(f'livTest.hour({h})') for h in range(24)]
        for k, rid in enumerate(self.L()['routines']):
            self.assertEqual(seen[k * 3:k * 3 + 3], [rid] * 3)
        self.assertEqual(seen[0], 'finch', 'The cello is at midnight')
        self.assertEqual(seen[21], 'ngozi', 'Tea at nine in the evening')

    def test_02_spotting_routines_gives_tips_once_and_a_pin(self):
        ids = self.enter()
        self.assertTrue({'liv-radio', 'liv-routine'} <= set(ids))
        tips = self.L()['tips']
        self.page.evaluate('livTest.hour(21)')
        self.page.evaluate("livTest.go('liv-routine')")
        body = self.page.locator('#modal-body').inner_text()
        self.assertIn('Tea at nine', body)
        self.assertIn('Routine 1 of 8 spotted', body)
        self.assertIn('Someone in the conservatory', body, 'Unseen routines stay a little mystery')
        self.assertEqual(self.L()['tips'], tips + 2)
        self.page.evaluate('livTest.close()')
        self.page.evaluate("livTest.go('liv-routine')")
        self.assertEqual(self.L()['tips'], tips + 2, 'Only the first spot pays')
        for h in range(0, 24, 3):
            self.page.evaluate('livTest.close()')
            self.page.evaluate(f'livTest.hour({h})')
            self.page.evaluate("livTest.go('liv-routine')")
        self.assertEqual(len(self.L()['living']['spotted']), 8)
        self.assertIn('clockwork-manor', self.L()['pins'])

    def test_03_radio_reviews_you_first_then_ads_and_reviews(self):
        self.enter()
        tips = self.L()['tips']
        self.page.evaluate("livTest.go('liv-radio')")
        self.assertIn('first review is about you', self.page.locator('#liv-seg').text_content())
        self.assertEqual(self.L()['tips'], tips + 2)
        kinds = []
        for _ in range(11):
            self.page.locator('#liv-next').click()
            kinds.append(self.page.locator('#liv-seg .liv-seg').get_attribute('class'))
        self.assertIn('liv-seg ad', kinds)
        self.assertIn('liv-seg review', kinds)
        self.assertEqual(self.L()['living']['heard'], 12)
        self.assertIn('loyal-listener', self.L()['pins'])
        self.page.evaluate('livTest.close()')
        self.page.evaluate("livTest.go('liv-radio')")
        self.assertNotIn('about you', self.page.locator('#liv-seg').inner_text(), 'The review about you is once a night')
        self.assertEqual(self.L()['tips'], tips + 2, 'Only the first listen of the night pays')

    def test_04_surprises_pay_for_kind_answers_and_stop_at_three_a_day(self):
        self.enter()
        tips = self.L()['tips']
        sid = self.page.evaluate('livTest.spawn()')
        self.assertIn(sid, self.L()['surprises'])
        self.assertIn('liv-surprise', self.page.evaluate('livTest.extras()'))
        self.page.evaluate("livTest.go('liv-surprise')")
        best = self.L()['text']['en']['surprises'][sid]['opts'][0][0]
        self.page.locator('#modal-body .choice', has_text=best[:40]).click()
        self.assertIn('Best answer', self.page.locator('#liv-res').inner_text())
        self.assertEqual(self.L()['tips'], tips + 3)
        self.assertIsNone(self.page.evaluate('livTest.pending()'))
        for _ in range(2):
            self.page.evaluate('livTest.close()')
            self.assertIsNotNone(self.page.evaluate('livTest.spawn()'))
            self.page.evaluate("livTest.go('liv-surprise')")
            self.page.locator('#modal-body .choice').first.click()
        self.page.evaluate('livTest.close()')
        self.assertIsNone(self.page.evaluate('livTest.spawn()'), 'Three surprises a day at most')
        self.assertEqual(len(set(self.L()['living']['done'])), 3, 'New surprises come before repeats')

    def test_05_spanish_matches_and_staff_speak_in_full_polite_sentences(self):
        text = self.L()['text']
        en, es = text['en'], text['es']
        self.assertEqual(set(en['routines']), set(es['routines']))
        self.assertEqual(set(en['surprises']), set(es['surprises']))
        self.assertEqual(len(en['ads']), len(es['ads']))
        self.assertEqual(len(en['reviews']), len(es['reviews']))
        for rid, r in en['routines'].items():
            self.assertEqual([w for w, _ in r['lines']], [w for w, _ in es['routines'][rid]['lines']], rid)
            for who, line in r['lines']:
                if who == 'you':
                    self.assertIsNone(SLANG.search(line), line)
                    self.assertRegex(line, r'[.?!]$', 'Staff lines are full sentences')
        for sid, s in en['surprises'].items():
            self.assertEqual(len(s['opts']), 3)
            self.assertEqual(len(es['surprises'][sid]['opts']), 3)
            self.assertIsNone(SLANG.search(s['opts'][0][0]), sid)
        rooms = re.findall(r'Room (\d+)', ' '.join(r[1] for r in en['reviews']))
        self.assertTrue(all(201 <= int(n) <= 206 for n in rooms), 'Six guest rooms only')


class LivingNightOne(base.Growth):
    """On night one the manor stays simple: routines, radio and surprises open after the first shift."""
    open_manor = False

    def test_01_hidden_on_night_one(self):
        self.page.locator('#begin').click()
        self.page.wait_for_function('document.getElementById("game-shell").hidden===false')
        self.page.evaluate('livTest.close()')
        ids = self.page.evaluate('livTest.play()')
        self.assertFalse({'liv-radio', 'liv-routine'} & set(ids))


# Do not run the growth tests again here.
for _cls in (Living, LivingNightOne):
    for _name in dir(base.Growth):
        if _name.startswith('test_') and _name not in _cls.__dict__:
            setattr(_cls, _name, None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
