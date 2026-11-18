"""Browser checks for JOY v1: sparkle-and-pop feedback with tips, gift boxes after good shifts,
outfits in the closet, and the daily mystery guest whose story unfolds over quick shifts.

Run: python tests/test_joy.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import json
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'joyTest',{get:()=>({
 joy:structuredClone(joy),growth:structuredClone(growth),gifts:GIFTS.map(g=>g.id),guests:MG_GUESTS.map(g=>g.id),
 fxParts:fx.parts.length,extras:world.options.extras().map(e=>e.id),
 give:(reason)=>{joy.gifts.push(reason);storeJoy();},
 setJar:(n)=>{joy.jar=n;storeJoy();},
 mgRight:()=>joyL(mgCurrent()).opts[0],motion:(on)=>{settings.motion=on;applySettings();},
 enterPlay:()=>{state.flags.briefed=true;state.phase='playing';return world.options.extras().map(e=>e.id);},
open:()=>openGift(),close:()=>closeModal()
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class Joy(base.Growth):
    """Reuses the growth harness but none of its tests."""

    def j(self):
        return self.page.evaluate('window.joyTest')

    def shift(self, best_count=5):
        self.page.locator('#title-quick').click()
        n = 0
        while n < 5:
            self.page.wait_for_selector('#modal-body .choice')
            if self.page.locator('.fun-rush-card').count():
                self.page.locator('.fun-rush-card').first.click()
                continue
            self.answer(best=n < best_count)
            self.next_button()
            n += 1
        self.page.wait_for_selector('#shift-actions')

    def test_01_best_answer_pops_with_tips_a_hopping_buddy_and_sparkles(self):
        self.page.evaluate('window.joyTest.motion(false)')
        self.page.locator('#title-quick').click()
        self.answer(best=True)
        stage = self.page.locator('.gm-result .joy-stage.best')
        self.assertEqual(stage.count(), 1)
        self.assertIn('+3 tips', stage.inner_text())
        self.assertGreater(self.page.evaluate('document.querySelector(".joy-buddy").width'), 0)
        self.page.wait_for_function('window.joyTest.fxParts>0')
        self.page.wait_for_function('document.querySelector(".joy-count").textContent==="3"')
        self.next_button()
        self.answer(best=True)
        self.assertIn('+4 tips', self.page.locator('.joy-stage').inner_text())
        self.next_button()
        self.answer(best=False)
        self.assertEqual(self.page.locator('.joy-stage.miss').count(), 1)
        self.assertIn('Best answers earn tips', self.page.locator('.joy-stage').inner_text())
        self.assertEqual(self.j()['joy']['tips'], 7)

    def test_02_good_shift_earns_a_gift_box_that_opens_after_three_taps(self):
        self.shift(best_count=3)
        self.assertEqual(self.j()['joy']['gifts'], ['shift'])
        self.page.locator('.joy-open-gift').click()
        gift = self.page.locator('.joy-gift')
        for _ in range(3):
            gift.click()
        self.page.wait_for_selector('.joy-giftstage.opened')
        j = self.j()
        self.assertEqual(j['joy']['gifts'], [])
        self.assertEqual(len(j['joy']['owned']), 1)
        self.assertIn(self.page.locator('.joy-rar').inner_text().split(' ')[0], ('Lovely', 'Rare', 'Super'))
        self.assertIn('unwrapped', j['growth']['pins'])

    def test_03_weak_shift_gives_no_gift_but_a_kind_hint(self):
        self.shift(best_count=1)
        self.assertEqual(self.j()['joy']['gifts'], [])
        self.assertIn('3 or more best answers', self.page.locator('#modal-body').inner_text())

    def test_04_outfits_can_be_worn_and_drawn_in_the_closet(self):
        self.page.evaluate('window.joyTest.close()')
        for _ in range(12):
            self.page.evaluate('window.joyTest.give("perfect")')
        self.page.evaluate('window.joyTest.open()')
        while self.j()['joy']['gifts']:
            self.page.wait_for_selector('.joy-gift')
            for _ in range(3):
                self.page.locator('.joy-gift').click()
            self.page.wait_for_selector('.joy-giftstage.opened')
            nxt = self.page.locator('#joy-gift-actions button', has_text='Open the next gift')
            if nxt.count():
                nxt.click()
        j = self.j()
        self.assertEqual(len(j['joy']['owned']), 12, 'No duplicates until everything is found')
        self.page.locator('#joy-gift-actions button', has_text='Closet').click()
        self.page.wait_for_selector('#joy-wear')
        worn = self.page.locator('#joy-wear button').first
        worn.click()
        self.assertTrue(self.j()['joy']['wearing'])
        self.assertIn('dressed-up', self.j()['growth']['pins'])
        saved = json.loads(self.page.evaluate("localStorage.getItem('mapachez_joy_v1')"))
        self.assertEqual(saved['wearing'], self.j()['joy']['wearing'])

    def test_05_full_tip_jar_brings_a_gift(self):
        self.page.evaluate('window.joyTest.setJar(38)')
        self.page.locator('#title-quick').click()
        self.answer(best=True)
        self.page.wait_for_selector('.gm-result .joy-open-gift')
        j = self.j()
        self.assertEqual(j['joy']['gifts'], ['jar'])
        self.assertEqual(j['joy']['jar'], 1)
        self.assertIn('full-jar', j['growth']['pins'])

    def test_06_mystery_guest_checks_in_takes_a_guess_and_unfolds_over_shifts(self):
        title = self.page.locator('#joy-title-mg')
        self.assertIn('mystery guest checked in', title.inner_text())
        title.click()
        self.page.wait_for_selector('.joy-parts')
        self.assertEqual(self.page.locator('.joy-parts li.locked').count(), 3)
        guest = self.j()['joy']['mg']['id']
        self.assertIn(guest, self.j()['guests'])
        right = self.page.evaluate('window.joyTest.mgRight()')
        self.assertEqual(self.page.locator('.joy-guess button').count(), 3)
        self.page.locator('.joy-guess button', has_text=right).click()
        self.assertIn('Your guess', self.page.locator('#joy-mg-guess').inner_text())
        self.assertGreaterEqual(self.j()['joy']['mg']['guess'], 0)
        self.page.evaluate('window.joyTest.close()')
        for part in (2, 3, 4):
            self.shift(best_count=5 if part == 2 else 0)
            self.assertEqual(self.j()['joy']['mg']['part'], part)
            self.assertIn(f'PART {part} OF 4', self.page.locator('.joy-panel.mg').inner_text())
            self.page.evaluate('window.joyTest.close()')
        j = self.j()
        self.assertEqual(j['joy']['mg']['solved'], [guest])
        self.assertIn('secret-keeper', j['growth']['pins'])
        self.assertIn('good-instincts', j['growth']['pins'])
        self.assertEqual(j['joy']['gifts'], ['perfect', 'mystery'], 'A perfect shift and a right guess each bring a gift')

    def test_07_mystery_guest_walks_the_manor(self):
        self.page.locator('#begin').click()
        self.page.wait_for_function('document.getElementById("game-shell").hidden===false')
        self.page.evaluate('window.joyTest.close()')
        self.assertIn('mystery-guest', self.page.evaluate('window.joyTest.enterPlay()'))
        self.page.evaluate("document.querySelector('#joy-side-mg').click()")
        self.page.wait_for_selector('.joy-parts')

    def test_08_reduce_motion_opens_the_gift_in_one_tap_with_no_particles(self):
        self.page.evaluate('window.joyTest.motion(true)')
        self.page.locator('#title-quick').click()
        self.answer(best=True)
        self.page.wait_for_function('document.querySelector(".joy-count").textContent==="3"')
        self.assertEqual(self.j()['fxParts'], 0)
        self.page.evaluate('window.joyTest.close()')
        self.page.evaluate('window.joyTest.give("shift")')
        self.page.evaluate('window.joyTest.open()')
        self.page.locator('.joy-gift').click()
        self.page.wait_for_selector('.joy-giftstage.opened')

    def test_09_phone_reward_strip_fits(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.page.locator('#title-quick').click()
        self.answer(best=True)
        width = self.page.evaluate("document.querySelector('.joy-stage').getBoundingClientRect().right")
        self.assertLessEqual(width, 390)


if __name__ == '__main__':
    unittest.main(verbosity=2)
