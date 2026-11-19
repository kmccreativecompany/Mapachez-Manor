"""Browser checks for STAR SERVICE v1: Little Things (guest preference memory), Magic coins
(fix it on the spot, no manager needed) and the Three-ring phone.

Run: python tests/test_star.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import re
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'starTest',{get:()=>({
 star:structuredClone(star),joy:structuredClone(joy),pins:Object.keys(growth.pins),
 guests:STAR_GUESTS,cases:STAR_CASES,calls:STAR_CALLS,text:STAR_TEXT,
 open:()=>openStar(),little:()=>openLittle(),coins:()=>openCoins(),phone:()=>openPhone(),
 extras:world.options.extras().map(e=>e.id),interact:id=>interact(id),ledger:()=>openLedger(),
 enterPlay:()=>{state.flags.briefed=true;state.phase='playing';return world.options.extras().map(e=>e.id);},
 solved:ids=>{star.coin.solved=ids;storeStar();},side:()=>{renderGrowth();return $('joy-side-star')?.innerText||'';},
 yesterday:()=>{for(const k of Object.keys(star.lt.noted))star.lt.noted[k]='2000-01-01';star.lt.day={key:'',n:0};star.coin.day={key:'',used:0};storeStar();}
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class Star(base.Growth):
    """Reuses the growth harness but none of its tests."""

    def s(self):
        return self.page.evaluate('window.starTest')

    def test_01_title_button_opens_the_hub_with_three_games(self):
        btn = self.page.locator('#star-title')
        self.assertIn('Star service', btn.inner_text())
        btn.click()
        self.page.wait_for_selector('.star-card')
        self.assertEqual(self.page.locator('.star-card').count(), 3)
        text = self.page.locator('#modal-body').inner_text()
        for word in ['Little Things', 'Magic coins', 'Three-ring phone']:
            self.assertIn(word, text)

    def test_02_little_things_listen_then_preview_return(self):
        self.page.evaluate('starTest.little()')
        self.assertEqual(self.page.locator('.lt-opt').count(), 3)
        tips = self.s()['joy']['tips']
        self.page.locator('.lt-opt[data-right="1"]').click()
        st = self.s()
        self.assertIn('amara', st['star']['lt']['noted'])
        self.assertEqual(st['joy']['tips'], tips + 1)
        self.assertIn('Saved to the HMS notes', self.page.locator('#lt-res').inner_text())
        # The very first time, the player gets to see the payoff straight away.
        self.page.locator('#lt-actions button', has_text='a week later').click()
        self.page.locator('#lt-peek').click()
        self.assertIn('fan humming', self.page.locator('#lt-note').inner_text())
        self.page.locator('.star-item[data-right="1"]').click()
        st = self.s()
        self.assertEqual(st['star']['lt']['back'], ['amara'])
        self.assertEqual(st['joy']['tips'], tips + 1 + 3)
        self.assertIn('star-remember', st['pins'])
        self.assertIn('You remembered', self.page.locator('#lt-res').inner_text())

    def test_03_guests_come_back_the_next_night_and_misses_are_gentle(self):
        self.page.evaluate('starTest.little()')
        self.page.locator('.lt-opt[data-right="0"]').first.click()
        self.assertIn('won’t matter', self.page.locator('#lt-res').inner_text())
        self.page.locator('#lt-actions button', has_text='a week later').click()
        self.page.locator('.star-item[data-right="0"]').first.click()
        self.assertEqual(self.s()['star']['lt']['back'], [])
        self.assertIn('They’ll be back', self.page.locator('#lt-res').inner_text())
        # Second guest tonight, then the daily limit.
        self.page.evaluate('starTest.little()')
        self.page.locator('.lt-opt[data-right="1"]').click()
        self.page.evaluate('starTest.little()')
        self.assertIn('Your notebook is ready', self.page.locator('#modal-heading').inner_text())
        # Next night: the guests you noted come back first.
        self.page.evaluate('starTest.yesterday()')
        self.page.evaluate('starTest.little()')
        self.assertIn('Amara is coming back', self.page.locator('#modal-heading').inner_text())
        self.page.locator('.star-item[data-right="1"]').click()
        self.page.evaluate('starTest.little()')
        self.assertIn('Tomás is coming back', self.page.locator('#modal-heading').inner_text())

    def test_04_magic_coins_three_a_night_and_the_free_fix_keeps_its_coin(self):
        self.page.evaluate('starTest.coins()')
        self.assertEqual(self.page.locator('.star-coins span.on').count(), 3)
        self.assertEqual(self.page.locator('.coin-opt').count(), 3)
        tips = self.s()['joy']['tips']
        self.page.locator('.coin-opt[data-right="1"]').click()
        st = self.s()
        self.assertEqual(st['star']['coin']['solved'], ['pizza'])
        self.assertEqual(st['star']['coin']['day']['used'], 1)
        self.assertEqual(st['joy']['tips'], tips + 2)
        self.assertIn('star-coin', st['pins'])
        self.assertIn('Real tip', self.page.locator('#coin-res').inner_text())
        # Skip ahead to the towels moment: the right answer is free, so the coin is kept.
        self.page.evaluate("starTest.solved(['pizza','birthday','teddy','pipes'])")
        self.page.evaluate('starTest.coins()')
        self.assertIn('towels', self.page.locator('#modal-heading').inner_text().lower())
        self.page.locator('.coin-opt[data-right="1"]').click()
        self.assertEqual(self.s()['star']['coin']['day']['used'], 1)
        self.assertIn('kept your coin', self.page.locator('#coin-res').inner_text())
        # Spend the rest; then coins rest until tomorrow.
        for _ in range(2):
            self.page.evaluate('starTest.coins()')
            self.page.locator('.coin-opt[data-right="0"]').first.click()
            self.assertIn('best move', self.page.locator('#coin-res').inner_text())
        self.page.evaluate('starTest.coins()')
        self.assertIn('Coins all spent', self.page.locator('#modal-heading').inner_text())

    def test_05_three_ring_phone_round(self):
        self.page.evaluate('starTest.phone()')
        self.page.check('#ph-relax')  # slower rings keep the timing steady on a busy machine
        self.page.locator('#ph-actions button', has_text='Start the calls').click()
        for n in range(5):
            self.page.wait_for_selector('#ph-answer')
            self.assertIn(f'CALL {n + 1} OF 5', self.page.locator('#modal-body .overline').first.inner_text().upper())
            self.page.locator('#ph-answer').click()
            self.assertIn('Ring 1', self.page.locator('#ph-live').inner_text())
            greet = self.page.locator('#ph-greet .penny-opt[data-right="1"]')
            g = greet.inner_text()
            self.assertTrue(re.search(r'Good evening', g))
            greet.click()
            self.page.locator('#ph-reply .penny-opt[data-right="1"]').click()
            self.page.locator('#ph-actions button').click()
        self.assertIn('15 / 15', self.page.locator('#ph-score').inner_text())
        st = self.s()
        self.assertEqual(st['star']['phone']['best'], 15)
        self.assertIn('star-ring', st['pins'])
        self.assertIn('star-smile', st['pins'])

    def test_06_a_late_answer_is_kind_and_explains(self):
        self.page.evaluate('starTest.phone()')
        self.page.locator('#ph-actions button', has_text='Start the calls').click()
        self.page.wait_for_function("document.querySelector('#ph-ringline')?.innerText.includes('Ring 3')", timeout=6000)
        self.page.locator('#ph-answer').click()
        self.assertIn('They waited a little', self.page.locator('#ph-live').inner_text())

    def test_07_bell_on_the_desk_sidebar_ledger_and_key(self):
        self.page.locator('#begin').click()
        self.page.wait_for_timeout(300)
        if self.page.locator('#modal').evaluate('m=>m.open'):
            self.page.keyboard.press('Escape')
        ids = self.page.evaluate('starTest.enterPlay()')
        self.assertIn('star', ids)
        self.page.evaluate("starTest.interact('star')")
        self.page.wait_for_selector('.star-card')
        self.page.keyboard.press('Escape')
        self.assertIn('Star service', self.page.evaluate('starTest.side()'))
        self.page.evaluate('starTest.ledger()')
        self.assertEqual(self.page.locator('#ledger-star').count(), 1)

    def test_08_spanish_has_every_line_and_no_brand_names(self):
        st = self.s()
        en, es = st['text']['en'], st['text']['es']
        self.assertEqual(set(en), set(es))
        for group in ('guests', 'cases', 'calls'):
            for item in st[group]:
                self.assertIn('es', item)
                self.assertEqual(len(item['es'].get('opts', item['es'].get('pick', []))), len(item['en'].get('opts', item['en'].get('pick', []))))
        page = base.HTML.split('STAR SERVICE v1')[1].lower()
        for word in ['forbes', 'ritz', 'four seasons', 'mandarin oriental', 'peninsula', 'aman']:
            self.assertIsNone(re.search(r'\b' + word + r'\b', page), word)


if __name__ == '__main__':
    unittest.main(verbosity=2)
