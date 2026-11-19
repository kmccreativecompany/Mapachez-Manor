"""Browser checks for HMS v1: the desk computer, five guided lessons, guests whose questions only the
HMS can answer, gentle "peek first" hints, three desk mini-games and the HMS pins.

Run: python tests/test_hms.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'hmsTest',{get:()=>({
 hms:structuredClone(hms),joy:structuredClone(joy),pins:Object.keys(growth.pins),
 extras:world.options.extras().map(e=>e.id),qs:HMS_QS.map(q=>q.id),
 open:()=>openHms(),lesson:n=>startLesson(n),ask:id=>openHmsQuestion('world',HMS_QS.find(q=>q.id===id)),
 game:id=>HMS_GAMES[id](),interact:id=>interact(id),since:n=>{hms.since=n;storeHms();},
 lessonsDone:()=>{hms.lessons=[1,2,3,4,5];storeHms();},firstLesson:()=>{hms.lessons=[1];storeHms();},
 rushCall:()=>document.querySelector('.hms-radio p').textContent,
 rushAnswer:()=>{const t=document.querySelector('.hms-radio p').textContent,r=t.match(/\\d{3}/)[0];
   const to=/supervisor/i.test(t)?'ready':/sparkling/.test(t)?'clean':/checked out|fixed/.test(t)?'tidy':/walked/.test(t)?'guest':'fix';return {r,to};},
 billBad:()=>{const n=document.querySelector('.hms-who b').textContent,c=BILL_CASES.find(c=>hL(hmsGuest(c.g)).name===n&&[...document.querySelectorAll('.hms-line span')].map(s=>s.textContent).join('|')===hL(c)[1].map(l=>l[0]).join('|'));return hL(c)[2];},
 buildRight:()=>{const line=document.querySelector('.hms-speech p').textContent,G=BUILD_GUESTS.find(g=>line.includes(hL(g)[0]));const f=document.querySelector('.hms-field.now').dataset.field;
   return f==='name'?G.name[0]:f==='nights'?String(G.n):f==='note'?hL(G)[1][0]:[...document.querySelectorAll('.hms-chips .hms-room.ready')][0].dataset.v;},
 enterPlay:()=>{state.flags.briefed=true;state.phase='playing';return world.options.extras().map(e=>e.id);},
 motion:(on)=>{settings.motion=on;applySettings();},
 rushCalls:()=>rushCalls(),rushStart:()=>({...HMS_ROOMS,'202':'guest','204':'guest'}),
 status:()=>HT.status,pickClean:()=>HT.pickClean
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class Hms(base.Growth):
    """Reuses the growth harness but none of its tests."""

    def h(self):
        return self.page.evaluate('window.hmsTest')

    def tap(self, act):
        self.page.locator(f'#modal-body [data-act="{act}"]').first.click()

    def enter_manor(self):
        self.page.locator('#begin').click()
        self.page.wait_for_timeout(300)
        if self.page.locator('#modal').evaluate('m=>m.open'):
            self.page.keyboard.press('Escape')

    def test_01_title_button_opens_the_desk_computer_with_lessons_games_and_a_login_pin(self):
        btn = self.page.locator('#hms-title')
        self.assertIn('Learn the HMS', btn.inner_text())
        btn.click()
        self.page.wait_for_selector('.hms-skill')
        text = self.page.locator('#modal-body').inner_text()
        self.assertIn('hotel management system', text.lower())
        self.assertEqual(self.page.locator('#hms-lessons .hms-lesson').count(), 5)
        self.assertEqual(self.page.locator('#hms-games .hms-lesson').count(), 3)
        self.assertIn('hms-login', self.h()['pins'])

    def test_02_lesson_glows_the_next_tap_and_ends_with_a_quiz_tips_and_points(self):
        self.page.evaluate('window.hmsTest.lesson(1)')
        self.assertEqual(self.page.locator('[data-act="tab:bookings"].hms-glow').count(), 1)
        self.tap('booking:finch')  # wrong tap: nothing advances
        self.assertIn('Tap Bookings', self.page.locator('#hms-say').inner_text().replace('📅 ', ''))
        self.tap('tab:bookings')
        self.assertEqual(self.page.locator('[data-act="booking:vesper"].hms-glow').count(), 1)
        self.tap('booking:vesper')
        self.page.wait_for_selector('#hms-quiz .choice')
        self.page.locator('#hms-quiz .choice', has_text='1 night').click()
        self.assertIn('Look again', self.page.locator('#hms-quiz .hms-msg').inner_text())
        self.page.locator('#hms-quiz .choice', has_text='2 nights').click()
        self.page.wait_for_selector('.hms-done')
        h = self.h()
        self.assertEqual(h['hms']['lessons'], [1])
        self.assertEqual(h['hms']['xp'], 10)
        self.assertEqual(h['joy']['tips'], 3)
        self.assertIn('hms-lesson', h['pins'])
        self.assertIn('Next lesson', self.page.locator('#hms-l-actions').inner_text())

    def test_03_check_in_lesson_refuses_a_room_that_needs_a_tidy(self):
        self.page.evaluate('window.hmsTest.lesson(5)')
        for act in ('tab:bookings', 'booking:juniper', 'checkin:juniper'):
            self.tap(act)
        self.tap('pick:205')
        self.assertIn('still needs a tidy', self.page.locator('#hms-host .hms-msg').inner_text())
        self.tap('pick:201')
        self.page.wait_for_selector('.hms-done')
        self.assertIn('checked in', self.page.locator('#hms-host').inner_text().lower())

    def test_04_finishing_all_lessons_graduates_with_a_gift_box(self):
        self.page.evaluate('hmsTest.firstLesson()')
        steps = {2: ['tab:rooms', 'room:205'], 3: ['tab:guests', 'guest:vesper'], 4: ['tab:bills', 'bill:vale']}
        answers = {2: 'Not yet', 3: 'sesame', 4: 'Garden tea'}
        for n in (2, 3, 4):
            self.page.evaluate(f'hmsTest.lesson({n})')
            for act in steps[n]:
                self.tap(act)
            self.page.locator('#hms-quiz .choice', has_text=answers[n]).click()
            self.page.wait_for_selector('.hms-done')
        self.page.evaluate('hmsTest.lesson(5)')
        for act in ('tab:bookings', 'booking:juniper', 'checkin:juniper', 'pick:201'):
            self.tap(act)
        self.page.wait_for_selector('.hms-done .joy-open-gift')
        h = self.h()
        self.assertEqual(sorted(h['hms']['lessons']), [1, 2, 3, 4, 5])
        self.assertIn('hms', h['joy']['gifts'])
        self.assertIn('hms-graduate', h['pins'])

    def test_05_look_it_up_question_rewards_looking_first(self):
        self.page.evaluate("hmsTest.ask('ready')")
        self.assertEqual(self.page.locator('#hms-look.hms-glow').count(), 1)
        self.page.locator('#hms-look').click()
        self.assertEqual(self.page.locator('#hms-host [data-act="tab:rooms"].hms-glow').count(), 1)
        self.page.locator('.choices .choice', has_text='tea').click()
        self.page.wait_for_selector('.gm-result.best')
        h = self.h()
        self.assertEqual(h['hms']['looked'], 1)
        self.assertEqual(h['joy']['tips'], 4)

    def test_06_guessing_is_fine_but_looking_is_better_and_misses_come_back(self):
        self.page.evaluate("hmsTest.ask('allergy')")
        self.page.locator('.choices .choice', has_text='sesame').click()
        self.assertIn('peek in the HMS first', self.page.locator('.gm-result.ok').inner_text())
        self.page.evaluate("hmsTest.ask('charge')")
        self.page.locator('.choices .choice', has_text='just a fee').click()
        self.assertIn('Garden tea for two', self.page.locator('.gm-result.miss').inner_text())
        self.assertTrue(self.h()['hms']['q']['charge']['miss'])

    def test_07_every_third_manor_guest_has_an_hms_question(self):
        self.enter_manor()
        self.page.evaluate('hmsTest.enterPlay()')
        self.page.evaluate('hmsTest.since(2)')
        self.page.evaluate("hmsTest.interact('guest-moment')")
        self.page.wait_for_selector('#hms-look')
        self.assertIn('A GUEST HAS A QUESTION', self.page.locator('#modal-body .overline').first.inner_text().upper())

    def test_08_desk_computer_sits_on_the_front_desk(self):
        self.enter_manor()
        self.assertIn('hms', self.page.evaluate('hmsTest.enterPlay()'))
        self.page.evaluate("hmsTest.interact('hms')")
        self.page.wait_for_selector('.hms-skill')

    def test_09_quick_shift_includes_one_hms_guest_after_a_lesson(self):
        self.page.evaluate('hmsTest.firstLesson()')
        self.page.locator('#title-quick').click()
        seen = 0
        for n in range(5):
            self.page.wait_for_selector('#modal-body .choice')
            if self.page.locator('.fun-rush-card').count():
                self.page.locator('.fun-rush-card').first.click()
                self.page.wait_for_selector('#modal-body .choice')
            if self.page.locator('#hms-look').count():
                seen += 1
                self.page.locator('#hms-look').click()
                self.page.locator('.choices .choice').first.click()
                self.page.wait_for_selector('#modal-body .gm-result')
            else:
                self.answer(best=True)
            self.next_button()
        self.page.wait_for_selector('#shift-actions')
        self.assertEqual(seen, 1)

    def test_10_peek_first_hint_on_record_moments_gives_a_bonus_tip(self):
        self.page.locator('#title-quick').click()
        for _ in range(5):
            self.page.wait_for_selector('#modal-body .choice')
            if self.page.locator('.hms-peek button').count():
                self.page.locator('.hms-peek button').click()
                self.assertIn('GUEST RECORD', self.page.locator('.hms-mini').inner_text().upper())
                self.answer(best=True)
                self.assertIn('+1 tip for checking the HMS first', self.page.locator('.gm-result').inner_text())
                self.page.wait_for_function("hmsTest.pins.includes('hms-peek')")
                return
            self.answer(best=True)
            self.next_button()
        self.skipTest('no record moment in the first quick shift')

    def test_11_room_rush_keeps_the_board_true_and_rewards_a_clean_round(self):
        self.page.evaluate('hmsTest.motion(true)')
        self.page.evaluate("hmsTest.game('rush')")
        for _ in range(6):
            self.page.wait_for_selector('.hms-radio')
            a = self.page.evaluate('hmsTest.rushAnswer()')
            self.page.locator(f'[data-room="{a["r"]}"]').click()
            self.page.locator(f'[data-st="{a["to"]}"]').click()
        self.page.wait_for_selector('.hms-done')
        self.assertIn('6 / 6', self.page.locator('.hms-done').inner_text())
        h = self.h()
        self.assertEqual(h['hms']['perfect']['rush'], 1)
        self.assertIn('hms-rush', h['pins'])
        self.assertGreater(h['joy']['tips'], 0)

    def test_12_booking_builder_catches_typos_then_saves(self):
        self.page.evaluate('hmsTest.motion(true)')
        self.page.evaluate("hmsTest.game('build')")
        for g in range(3):
            for f in range(4):
                self.page.wait_for_selector('.hms-field.now')
                v = self.page.evaluate('hmsTest.buildRight()')
                if g == 0 and f == 0:
                    wrong = self.page.locator('.hms-chip').filter(has_not_text=v).first
                    wrong.click()
                    self.assertIn('listen again', self.page.locator('.hms-msg').inner_text())
                self.page.locator(f'[data-v="{v}"]').click()
            self.page.wait_for_timeout(450)
        self.page.wait_for_selector('.hms-done')
        self.assertIn('2 / 3', self.page.locator('.hms-done').inner_text())

    def test_13_bill_detective_stamps_the_wrong_charge_and_fixes_the_total(self):
        self.page.evaluate('hmsTest.motion(true)')
        self.page.evaluate("hmsTest.game('bill')")
        for _ in range(5):
            self.page.wait_for_selector('.hms-line:not(:disabled)')
            k = self.page.evaluate('hmsTest.billBad()')
            self.page.locator(f'.hms-line[data-k="{k}"]').click()
            self.assertEqual(self.page.locator('.hms-stamp').count(), 1)
            self.page.wait_for_timeout(400)
        self.page.wait_for_selector('.hms-done')
        self.assertEqual(self.h()['hms']['caught'], 5)

    def test_14_progress_survives_a_reload(self):
        self.page.evaluate('hmsTest.lesson(1)')
        self.tap('tab:bookings')
        self.tap('booking:vesper')
        self.page.locator('#hms-quiz .choice', has_text='2 nights').click()
        self.page.wait_for_selector('.hms-done')
        self.page.reload()
        self.page.wait_for_selector('#hms-title')
        self.assertEqual(self.h()['hms']['lessons'], [1])
        self.assertIn('1 / 5', self.page.locator('#hms-title').inner_text())

    def test_15_phone_layout_fits(self):
        self.context.close()
        self.setUp(viewport={'width': 375, 'height': 760})
        for open_js in ('hmsTest.open()', 'hmsTest.lesson(5)', "hmsTest.game('rush')", "hmsTest.game('build')", "hmsTest.game('bill')"):
            self.page.evaluate(open_js)
            self.page.wait_for_timeout(150)
            w = self.page.evaluate('document.querySelector("#modal").scrollWidth - document.querySelector("#modal").clientWidth')
            self.assertLessEqual(w, 1, open_js)
        self.assertEqual(self.errors, [])

    def test_16_a_cleaned_room_is_not_ready_until_a_supervisor_inspects_it(self):
        st = self.page.evaluate('hmsTest.status()')
        self.assertEqual(st['ready'][1], 'Clean, inspected & ready')
        self.assertIn('not inspected', st['clean'][1])
        for _ in range(40):
            rooms = self.page.evaluate('hmsTest.rushStart()')
            for c in self.page.evaluate('hmsTest.rushCalls()'):
                if c['to'] == 'ready':
                    self.assertEqual(rooms[c['r']], 'clean', 'a room went to ready without an inspection')
                rooms[c['r']] = c['to']
        self.assertIn('inspected', self.page.evaluate('hmsTest.pickClean()'))
        self.assertEqual(self.errors, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
