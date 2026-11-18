"""Browser checks for PENNY v1: Penny Puffwing, the manor's baby money dragon who shares one
bite-size hotel business fact at a time, with a gentle coin check, a coin book and four pins.

Run: python tests/test_penny.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import re
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'pennyTest',{get:()=>({
 penny:structuredClone(penny),joy:structuredClone(joy),pins:Object.keys(growth.pins),
 facts:PENNY_FACTS,text:PENNY_TEXT,ledger:()=>openLedger(),open:()=>openPenny(),book:()=>openPennyBook(),
 extras:world.options.extras().map(e=>e.id),interact:id=>interact(id),
 enterPlay:()=>{state.flags.briefed=true;state.phase='playing';return world.options.extras().map(e=>e.id);},
 festival:on=>{festivalActive=on;return world.options.extras().map(e=>e.id);}
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class Penny(base.Growth):
    """Reuses the growth harness but none of its tests."""

    def p(self):
        return self.page.evaluate('window.pennyTest')

    def pick(self, right=True):
        self.page.locator(f'.penny-opt[data-right="{1 if right else 0}"]').first.click()
        self.page.wait_for_selector('#penny-res:not([hidden])')

    def test_01_title_button_opens_a_fact_with_three_choices(self):
        btn = self.page.locator('#penny-title')
        self.assertIn('Penny', btn.inner_text())
        btn.click()
        self.page.wait_for_selector('.penny-card')
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), 'Penny Puffwing')
        self.assertIn('FACT 1 OF 21', self.page.locator('.penny-card small').inner_text().upper())
        self.assertEqual(self.page.locator('.penny-opt').count(), 3)
        self.assertEqual(self.page.locator('.penny-opt[data-right="1"]').count(), 1)

    def test_02_right_answer_collects_the_coin_with_tips_and_a_pin(self):
        self.page.evaluate('pennyTest.open()')
        tips = self.p()['joy']['tips']
        self.pick(True)
        st = self.p()
        self.assertEqual(st['penny']['got'], ['occupancy'])
        self.assertEqual(st['joy']['tips'], tips + 2)
        self.assertIn('penny-first', st['pins'])
        self.assertEqual(self.page.locator('.penny-opt:disabled').count(), 3)
        self.page.locator('#penny-actions button', has_text='Another fact').click()
        self.assertIn('ADR', self.page.locator('.penny-card h3').inner_text())

    def test_03_a_miss_is_gentle_and_the_fact_comes_back(self):
        self.page.evaluate('pennyTest.open()')
        self.pick(False)
        res = self.page.locator('#penny-res').inner_text()
        self.assertIn('About 67%', res)
        self.assertNotRegex(res.lower(), r'wrong|fail|bad')
        self.assertEqual(self.p()['penny']['got'], [])
        self.page.locator('#penny-actions button', has_text='Another fact').click()
        self.assertIn('Occupancy', self.page.locator('.penny-card h3').inner_text())

    def test_04_three_new_facts_a_night_then_reviews(self):
        self.page.evaluate('pennyTest.open()')
        for _ in range(3):
            self.pick(True)
            if self.page.locator('#penny-actions button', has_text='Another fact').count():
                self.page.locator('#penny-actions button', has_text='Another fact').click()
        self.assertEqual(len(self.p()['penny']['got']), 3)
        self.assertEqual(self.page.locator('#penny-actions button', has_text='Another fact').count(), 0)
        self.page.locator('#penny-actions button', has_text='Quick review').click()
        self.assertIn('REVIEW', self.page.locator('.penny-card small').inner_text().upper())
        tips = self.p()['joy']['tips']
        self.pick(True)
        self.assertEqual(self.p()['joy']['tips'], tips + 1)
        self.assertEqual(len(self.p()['penny']['got']), 3)

    def test_05_penny_sits_in_the_manor_but_not_at_the_festival(self):
        self.page.locator('#begin').click()
        self.page.wait_for_timeout(300)
        if self.page.locator('#modal').evaluate('m=>m.open'):
            self.page.keyboard.press('Escape')
        self.assertIn('penny', self.page.evaluate('pennyTest.enterPlay()'))
        self.assertNotIn('penny', self.page.evaluate('pennyTest.festival(true)'))
        self.page.evaluate('pennyTest.festival(false)')
        self.page.evaluate("pennyTest.interact('penny')")
        self.page.wait_for_selector('.penny-card')
        self.assertGreaterEqual(self.p()['penny']['visits'], 1)

    def test_06_coin_book_and_ledger_tab(self):
        self.page.locator('#begin').click()
        self.page.wait_for_timeout(300)
        if self.page.locator('#modal').evaluate('m=>m.open'):
            self.page.keyboard.press('Escape')
        self.page.evaluate('pennyTest.open()')
        self.pick(True)
        self.page.evaluate('pennyTest.book()')
        self.assertEqual(self.page.locator('.penny-coin').count(), 21)
        self.assertEqual(self.page.locator('.penny-coin.got').count(), 1)
        self.assertIn('not tax advice', self.page.locator('.penny-note').inner_text())
        self.page.keyboard.press('Escape')
        self.page.evaluate('pennyTest.ledger()')
        self.page.wait_for_selector('#ledger-penny')
        self.page.locator('#ledger-penny').click()
        self.page.wait_for_selector('.penny-book')

    def test_07_every_fact_is_complete_in_both_languages_and_stays_neutral(self):
        st = self.p()
        self.assertEqual(len(st['facts']), 21)
        self.assertEqual(len({f['id'] for f in st['facts']}), 21)
        for f in st['facts']:
            for lang in ('en', 'es'):
                t, fact, q, opts = f[lang]
                self.assertTrue(t and fact and q, f['id'] + lang)
                self.assertEqual(len(opts), 3, f['id'] + lang)
                self.assertEqual(len(set(opts)), 3, f['id'] + lang)
        self.assertEqual(set(st['text']['en'].keys()), set(st['text']['es'].keys()))
        blob = str(st['facts']) + str(st['text'])
        for word in ('Trump', 'Biden', 'Republican', 'Democrat', 'Beautiful Bill', 'Congress'):
            self.assertNotIn(word.lower(), blob.lower(), word)

    def test_08_secret_smoke_ring_pin_after_seven_visits(self):
        for _ in range(7):
            self.page.evaluate('pennyTest.open()')
            self.page.keyboard.press('Escape')
        self.assertIn('penny-puff', self.p()['pins'])

    def test_09_progress_survives_a_reload(self):
        self.page.evaluate('pennyTest.open()')
        self.pick(True)
        self.page.reload()
        self.page.wait_for_selector('#penny-title')
        self.assertEqual(self.p()['penny']['got'], ['occupancy'])
        self.assertIn('1 / 21', self.page.locator('#penny-title').inner_text())
        self.assertIn('Penny · 1/21', self.page.locator('#joy-side-penny').inner_text())

    def test_10_phone_layout_fits(self):
        self.context.close()
        self.setUp(viewport={'width': 375, 'height': 760})
        for js in ('pennyTest.open()', 'pennyTest.book()'):
            self.page.evaluate(js)
            self.page.wait_for_timeout(150)
            w = self.page.evaluate('document.querySelector("#modal").scrollWidth - document.querySelector("#modal").clientWidth')
            self.assertLessEqual(w, 1, js)
        self.assertEqual(self.errors, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
