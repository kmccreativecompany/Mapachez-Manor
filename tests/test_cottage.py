"""Browser checks for COTTAGE v1: tips earned for good work buy cosy things for the player's
own little staff cottage on the manor grounds.

Run: python tests/test_cottage.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import re
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'cotTest',{get:()=>({
 cottage:structuredClone(cottage),joy:structuredClone(joy),pins:Object.keys(growth.pins),items:COTTAGE_ITEMS,text:COTTAGE_TEXT,
 visitor:cot.visitor,targets:cotTargets().map(t=>t[0]),
 setTips:n=>{joy.tips=n;storeJoy();renderGrowth();},
 own:ids=>{cottage.owned=ids;storeCottage();},
 open:(tab)=>{if(cottage.live==null&&!tab)cottage.live=true;openCottage(tab||'inside');},tap:id=>cotTap(id),say:()=>document.getElementById('cot-say').textContent,
 motion:on=>{settings.motion=on;applySettings();},
 enterPlay:()=>{state.flags.briefed=true;state.phase='playing';},
 setPts:n=>{growth.pts={trust:n,care:0,team:0};},grade:()=>payGrade(),speed:()=>world.options.speed(),
 setLive:v=>{cottage.live=v;storeCottage();},rides:COT_RIDES.map(r=>r.id),projects:DREAM_PROJECTS.map(p=>p.id),dreamText:DREAM_TEXT,ct2:CT2_TEXT
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class Cottage(base.Growth):
    """Reuses the growth harness but none of its tests."""

    def c(self):
        return self.page.evaluate('window.cotTest')

    def test_01_title_button_opens_a_bare_cottage_with_delores_key(self):
        btn = self.page.locator('#cottage-title')
        self.assertIn('Your little cottage', btn.inner_text())
        btn.click()
        self.page.wait_for_selector('.cot-offer')
        self.assertIn('live on the grounds', self.page.locator('.cot-offer').inner_text())
        self.page.locator('.cot-offer button', has_text='pick a cottage').click()
        self.page.locator('.cot-homes li', has_text='The Toadstool').locator('button').click()
        self.page.wait_for_selector('#cot-room')
        self.assertTrue(self.c()['cottage']['live'])
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), 'Your little cottage')
        self.assertIn('brass key', self.page.locator('#cot-say').inner_text())
        self.assertIn('0 tips to spend', self.page.locator('#cot-wallet').inner_text())
        self.assertIn('Mushroom lamp', self.page.locator('.cot-next').inner_text())
        self.assertIn('10 more tips', self.page.locator('.cot-next').inner_text())
        self.assertEqual(self.page.locator('.cot-shop li').count(), 18)
        self.assertEqual(self.page.locator('.cot-shop .cot-buy:disabled').count(), 18)
        self.assertGreater(self.page.evaluate('document.getElementById("cot-room").width'), 0)

    def test_02_best_answers_earn_tips_and_a_nudge_when_enough_for_the_lamp(self):
        self.page.evaluate('cotTest.setTips(8)')
        self.page.locator('#title-quick').click()
        self.answer(best=True)
        panel = self.page.locator('.gm-result .cot-panel')
        self.assertEqual(panel.count(), 1)
        self.assertIn('Enough tips for the Mushroom lamp', panel.inner_text())
        self.assertIn('after your shift', panel.inner_text())
        self.next_button()
        self.answer(best=True)  # 11 + 4 tips crosses the rug's 15
        self.assertIn('Round rag rug', self.page.locator('.gm-result .cot-panel').inner_text())
        self.next_button()
        self.answer(best=False)
        self.assertEqual(self.page.locator('.gm-result .cot-panel').count(), 0)

    def test_03_buying_spends_tips_places_the_item_and_earns_a_pin(self):
        self.page.evaluate('cotTest.setTips(26)')
        self.page.evaluate('cotTest.open()')
        self.assertEqual(self.page.locator('.cot-shop .cot-buy:not(:disabled)').count(), 4)
        jar = self.c()['joy']['jar']
        self.page.locator('.cot-next .cot-buy').click()
        st = self.c()
        self.assertEqual(st['cottage']['owned'], ['lamp'])
        self.assertEqual(st['joy']['tips'], 16)
        self.assertEqual(st['joy']['jar'], jar, 'spending never empties the tip jar')
        self.assertEqual(st['cottage']['spent'], 10)
        self.assertIn('cottage-home', st['pins'])
        self.assertIn('lamp', st['targets'])
        self.assertIn('Mushroom lamp is home', self.page.locator('#cot-say').inner_text())
        self.assertIn('Home', self.page.locator('.cot-shop li.own').inner_text())
        self.assertIn('16 tips to spend', self.page.locator('#cot-wallet').inner_text())
        self.assertIn('Round rag rug', self.page.locator('.cot-next').inner_text())
        # Any affordable thing can be bought, not only the next one.
        self.assertTrue(self.page.locator('.cot-shop li', has_text='Fern in a teacup').locator('.cot-buy').is_disabled())
        self.page.evaluate('cotTest.setTips(30)')
        self.page.evaluate('cotTest.open()')
        self.page.locator('.cot-shop li', has_text='Patchwork quilt').locator('.cot-buy').click()
        self.assertEqual(self.c()['cottage']['owned'], ['lamp', 'quilt'])
        self.assertEqual(self.c()['joy']['tips'], 5)
        self.assertEqual(self.page.locator('.cot-shop .cot-buy:not(:disabled)').count(), 0)

    def test_04_cannot_buy_without_enough_tips_or_twice(self):
        self.page.evaluate('cotTest.setTips(9)')
        self.page.evaluate('cotTest.open()')
        self.assertTrue(self.page.locator('.cot-shop li', has_text='Mushroom lamp').locator('.cot-buy').is_disabled())
        self.assertEqual(self.page.locator('.cot-next .cot-buy').count(), 0)
        self.page.evaluate('cotTest.setTips(30)')
        self.page.evaluate('cotTest.open()')
        self.page.locator('.cot-next .cot-buy').click()
        self.assertEqual(self.c()['joy']['tips'], 20)
        self.assertEqual(self.page.locator('.cot-shop li', has_text='Mushroom lamp').locator('.cot-buy').count(), 0)

    def test_05_delores_visits_at_two_things_then_penny_at_six(self):
        self.page.evaluate('cotTest.setTips(200)')
        self.page.evaluate('cotTest.open()')
        self.page.locator('.cot-next .cot-buy').click()
        self.assertIsNone(self.c()['visitor'])
        self.page.locator('.cot-next .cot-buy').click()
        st = self.c()
        self.assertEqual(st['visitor'], 'delores')
        self.assertEqual(st['cottage']['met'], ['delores'])
        self.page.wait_for_function('document.getElementById("cot-say").textContent.startsWith("Delores")')
        for _ in range(4):
            self.page.locator('.cot-next .cot-buy').click()
        st = self.c()
        self.assertEqual(len(st['cottage']['owned']), 6)
        self.assertEqual(st['visitor'], 'penny')
        self.assertEqual(st['cottage']['met'], ['delores', 'penny'])
        self.page.evaluate('cotTest.tap("visitor")')
        self.assertIn('Penny Puffwing:', self.page.evaluate('cotTest.say()'))

    def test_06_tapping_things_makes_them_do_something(self):
        self.page.evaluate("cotTest.own(['lamp','fish','record','cushion','clock','scope'])")
        self.page.evaluate('cotTest.open()')
        for tid, words in (('fish', r'Blub|goldfish'), ('clock', r'Cuckoo'), ('scope', r'shooting star'),
                           ('muffin', r'Muffin'), ('me', r'Home|spin|stretch')):
            self.page.evaluate(f'cotTest.tap("{tid}")')
            self.assertRegex(self.page.evaluate('cotTest.say()'), words, tid)
        self.page.evaluate('cotTest.tap("lamp")')
        self.assertFalse(self.c()['cottage']['lamp'])
        self.assertIn('Moonlight', self.page.evaluate('cotTest.say()'))
        self.page.evaluate('cotTest.tap("record")')
        self.assertIn('cottage-concert', self.c()['pins'])
        # A real click on the canvas finds the record player in the front right.
        box = self.page.locator('#cot-room').bounding_box()
        s = box['width'] / 400
        self.page.mouse.click(box['x'] + 318 * s, box['y'] + 228 * s)
        self.assertEqual(self.c()['cottage']['plays'], 2)

    def test_07_moving_box_until_four_things(self):
        self.page.evaluate('cotTest.open()')
        self.assertIn('box', self.c()['targets'])
        self.page.evaluate('cotTest.tap("box")')
        self.assertIn('STUFF', self.page.evaluate('cotTest.say()'))
        self.page.evaluate("cotTest.own(['lamp','rug','plant','quilt'])")
        self.assertNotIn('box', self.c()['targets'])

    def test_08_sidebar_footer_and_c_key(self):
        self.page.locator('#title-quick').wait_for()
        self.page.evaluate('document.querySelector(".title-actions button").click()')
        self.page.evaluate('cotTest.enterPlay()')
        self.page.evaluate('cotTest.setTips(12)')
        self.page.evaluate('cotTest.setLive(true)')
        side = self.page.locator('#joy-side-cottage')
        self.assertIn('Cottage', side.inner_text())
        self.assertIn('ready', side.get_attribute('class'))
        self.assertIn('Your cottage', self.page.locator('#cottage-button').inner_text())
        self.page.keyboard.press('Escape')
        self.page.locator('body').press('c')
        self.page.wait_for_selector('#cot-room')
        self.page.keyboard.press('Escape')
        self.page.locator('#cottage-button').click()
        self.page.wait_for_selector('#cot-room')

    def test_09_all_eighteen_reaches_the_coziest_cottage(self):
        self.page.evaluate('cotTest.setTips(1535)')
        self.page.evaluate('cotTest.open()')
        for _ in range(18):
            self.page.locator('.cot-next .cot-buy').click()
        st = self.c()
        self.assertEqual(len(st['cottage']['owned']), 18)
        self.assertEqual(st['joy']['tips'], 0)
        self.assertEqual(sum(i['price'] for i in st['items']), 1535)
        for pin in ('cottage-home', 'cottage-cozy', 'cottage-all'):
            self.assertIn(pin, st['pins'])
        self.assertIn('coziest cottage', self.page.locator('.cot-next').inner_text())

    def test_10_progress_survives_a_reload_and_bad_saves_start_fresh(self):
        self.page.evaluate('cotTest.setTips(40)')
        self.page.evaluate('cotTest.open()')
        self.page.locator('.cot-next .cot-buy').click()
        self.page.reload()
        self.page.wait_for_selector('#cottage-title')
        st = self.c()
        self.assertEqual(st['cottage']['owned'], ['lamp'])
        self.assertEqual(st['joy']['tips'], 30)
        self.assertIn('🪙 30', self.page.locator('#cottage-title').inner_text())
        self.page.evaluate("localStorage.setItem('mapachez_cottage_v1','{\"version\":1,\"owned\":[\"lamp\",\"rocket\",\"lamp\"],\"spent\":-5}')")
        self.page.reload()
        self.page.wait_for_selector('#cottage-title')
        st = self.c()
        self.assertEqual(st['cottage']['owned'], ['lamp'])
        self.assertEqual(st['cottage']['spent'], 0)
        self.page.evaluate("localStorage.setItem('mapachez_cottage_v1','not json')")
        self.page.reload()
        self.page.wait_for_selector('#cottage-title')
        self.assertEqual(self.c()['cottage']['owned'], [])

    def test_11_every_item_and_line_is_written_in_both_languages(self):
        st = self.c()
        en, es = st['text']['en'], st['text']['es']
        self.assertEqual(set(en), set(es))
        for it in st['items']:
            self.assertEqual(len(it['en']), 2, it['id'])
            self.assertEqual(len(it['es']), 2, it['id'])
            self.assertTrue(all(it['en']) and all(it['es']), it['id'])
        words = ' '.join(str(v) for v in (en, es, st['items'])).lower()
        for banned in ('opossum', 'zarigüeya', 'infp', '4w5', 'rain', 'snow', 'lluvia', 'nieve'):
            self.assertNotIn(banned, words)

    def test_12_reduce_motion_draws_once_and_still_reacts(self):
        self.page.evaluate('cotTest.motion(true)')
        self.page.evaluate("cotTest.own(['lamp','fireplace'])")
        self.page.evaluate('cotTest.open()')
        self.page.evaluate('cotTest.tap("fireplace")')
        self.assertIn('Crackle', self.page.evaluate('cotTest.say()'))

    def test_13_phone_layout_fits(self):
        self.context.close()
        self.setUp(viewport={'width': 375, 'height': 760})
        self.page.evaluate('cotTest.setTips(50)')
        self.page.evaluate('cotTest.open()')
        self.page.wait_for_timeout(150)
        w = self.page.evaluate('document.querySelector("#modal").scrollWidth - document.querySelector("#modal").clientWidth')
        self.assertLessEqual(w, 1)
        cw = self.page.evaluate('document.getElementById("cot-room").getBoundingClientRect().width')
        self.assertGreater(cw, 280)
        btn = self.page.locator('.cot-next .cot-buy').bounding_box()
        self.assertGreaterEqual(btn['height'], 40)
        self.assertEqual(self.errors, [])

    def test_14_living_in_town_is_fine_and_you_can_move_in_later(self):
        self.page.locator('#cottage-title').click()
        self.page.locator('.cot-offer button', has_text='I live in town').click()
        self.assertFalse(self.c()['cottage']['live'])
        self.assertIn('You live in town', self.page.locator('.cot-offer').inner_text())
        self.page.locator('.cot-tab[data-tab="homes"]').click()
        self.assertEqual(self.page.locator('.cot-homes li').count(), 4)
        self.page.locator('.cot-homes li', has_text='The Seashell').locator('button').click()
        st = self.c()['cottage']
        self.assertTrue(st['live'])
        self.assertEqual(st['home'], 'seashell')
        self.assertIn('THE SEASHELL', self.page.locator('#modal-body .overline').first.inner_text().upper())

    def test_15_rides_cost_tips_follow_you_and_change_speed(self):
        self.page.evaluate('cotTest.setTips(100)')
        self.page.evaluate("cotTest.open('rides')")
        self.assertEqual(self.page.locator('.cot-rides li').count(), 9)
        self.page.locator('.cot-rides li', has_text='Bike with a basket').locator('button').click()
        st = self.c()
        self.assertEqual(st['cottage']['rides'], ['bike'])
        self.assertEqual(st['cottage']['ride'], 'bike')
        self.assertEqual(st['joy']['tips'], 40)
        self.assertIn('ride-first', st['pins'])
        self.assertAlmostEqual(self.page.evaluate('cotTest.speed()'), 1.55)
        self.page.locator('.cot-rides li', has_text='Bike with a basket').locator('button', has_text='Walk instead').click()
        self.assertEqual(self.c()['cottage']['ride'], '')
        self.assertEqual(self.page.evaluate('cotTest.speed()'), 1)
        self.assertTrue(self.page.locator('.cot-rides li', has_text='Flying car').locator('button').is_disabled())

    def test_16_the_snail_is_slow_and_the_flying_car_flies(self):
        self.page.evaluate('cotTest.setTips(400)')
        self.page.evaluate("cotTest.open('rides')")
        self.page.locator('.cot-rides li', has_text='Giant snail').locator('button').click()
        self.assertLess(self.page.evaluate('cotTest.speed()'), 1)
        self.assertIn('ride-snail', self.c()['pins'])
        self.page.locator('.cot-rides li', has_text='Flying car').locator('button').click()
        self.assertEqual(self.page.evaluate('cotTest.speed()'), 2)
        self.assertIn('ride-sky', self.c()['pins'])
        # The ride is drawn in the manor without errors.
        self.page.keyboard.press('Escape')
        self.page.evaluate('document.querySelector(".title-actions button").click()')
        self.page.evaluate('cotTest.enterPlay()')
        self.page.wait_for_timeout(300)

    def test_17_raises_add_tips_to_every_best_answer(self):
        self.assertEqual(self.page.evaluate('cotTest.grade()'), 0)
        self.page.evaluate('cotTest.setPts(230)')
        self.page.locator('#title-quick').click()
        self.answer(best=True)
        self.assertIn('+2 raise', self.page.locator('.gm-result .joy-stage').inner_text())
        st = self.c()
        self.assertEqual(st['joy']['tips'], 5)
        self.assertIn('pay-raise', st['pins'])
        self.assertGreaterEqual(st['cottage']['grade'], 2)
        self.page.keyboard.press('Escape')
        self.page.evaluate("cotTest.open('rides')")
        self.assertIn('+2 tips on every best answer', self.page.locator('.cot-pay').inner_text())

    def test_18_dream_house_buy_then_fix_up_then_live_there(self):
        total = 500 + 60 + 80 + 90 + 100 + 120 + 150 + 170 + 200
        self.page.evaluate(f'cotTest.setTips({total})')
        self.page.evaluate("cotTest.open('dream')")
        self.assertIn('Willowbrook House', self.page.locator('.cot-next').inner_text())
        self.page.locator('#dream-buy').click()
        self.assertTrue(self.c()['cottage']['house']['own'])
        self.assertIn('dream-deed', self.c()['pins'])
        for _ in range(8):
            self.page.locator('#dream-shop .cot-buy:not(:disabled)').first.click()
        st = self.c()
        self.assertEqual(len(st['cottage']['house']['done']), 8)
        self.assertEqual(st['joy']['tips'], 0)
        self.assertIn('dream-done', st['pins'])
        self.page.locator('#dream-live').click()
        self.assertEqual(self.c()['cottage']['home'], 'dream')
        self.page.wait_for_selector('#cot-room')

    def test_19_new_words_are_written_in_both_languages(self):
        st = self.c()
        for name in ('ct2', 'dreamText'):
            en, es = st[name]['en'], st[name]['es']
            self.assertEqual(set(en), set(es), name)
        words = (str(st['ct2']) + str(st['dreamText'])).lower()
        for banned in ('opossum', 'infp', 'broken', 'repair bill', 'rent due'):
            self.assertNotIn(banned, words)


if __name__ == '__main__':
    unittest.main(verbosity=2)
