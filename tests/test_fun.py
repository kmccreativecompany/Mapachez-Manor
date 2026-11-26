"""Browser checks for the fun list: rush hour, regulars who remember you, the lily
mystery, surprise nights and juicier feedback.

Run: python tests/test_fun.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py. The browser clock is
fixed to a chosen local noon so surprise nights are predictable.
"""
import datetime
import json
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'funTest',{get:()=>({
 fun:structuredClone(fun),growth:structuredClone(growth),tonight:tonight(),pins:PINS.map(p=>p.id),
 moments:GUEST_MOMENTS,guestEn:GUEST_EN
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')

CALM_DAY = datetime.datetime(2026, 11, 13, 12)   # an ordinary night
WEDDING_DAY = datetime.datetime(2026, 11, 15, 12)
STORM_DAY = datetime.datetime(2026, 11, 19, 12)


def growth_save(shifts=0, answers=0):
    return {'version': 1, 'pts': {'trust': 0, 'care': 0, 'team': 0}, 'seen': {}, 'answers': answers, 'run': 0, 'bestRun': 0,
            'missRun': 0, 'nights': {'last': '', 'count': 0, 'best': 0}, 'pins': {}, 'shifts': shifts, 'perfect': 0,
            'story': {}, 'flags': {}, 'look': 'house'}


class Fun(base.Growth):
    """Reuses the growth harness but none of its tests."""
    day = CALM_DAY
    seed = {}

    def setUp(self, viewport=None):
        self.context = self.browser.new_context(viewport=viewport or {'width': 1440, 'height': 1000}, reduced_motion='reduce')
        seed = {'mapachez_profile_v1': {'version': 1, 'mode': 'solo', 'lang': 'en', 'hooked': True}, **self.seed}
        self.context.add_init_script('try{if(!sessionStorage.getItem("seeded")){sessionStorage.setItem("seeded","1");'
                                     + ''.join(f'localStorage.setItem({json.dumps(k)},{json.dumps(v if isinstance(v, str) else json.dumps(v))});' for k, v in seed.items())
                                     + '}}catch(e){}')
        # The whole manor is open here; night-by-night unlocks are covered in test_nights.py.
        self.context.add_init_script("try{if(!localStorage.getItem('mapachez_nights_v1'))localStorage.setItem('mapachez_nights_v1',JSON.stringify({all:true,seen:10,fresh:[]}))}catch(e){}")
        self.page = self.context.new_page()
        self.page.clock.set_fixed_time(self.day)
        self.errors, self.requests = [], []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        self.page.route('**/*', self.route)
        self.page.goto(self.url)

    def fun(self):
        return self.page.evaluate('window.funTest.fun')

    def play_shift(self, pick_first=True):
        for _ in range(5):
            if self.page.locator('#modal-body .fun-rush').count():
                self.page.locator('.fun-rush-card').first.click()
            self.answer(best=True)
            self.next_button()
        self.page.wait_for_selector('.gm-summary')


class CalmNight(Fun):
    def test_01_pins_exist_and_a_first_shift_has_no_rush_but_finds_a_clue(self):
        t = self.page.evaluate('window.funTest')
        self.assertIsNone(t['tonight'])
        for pin in ['rush-hero', 'cool-head', 'lantern-glow', 'storm-keeper', 'wedding-bells', 'candlelight', 'known-by-name', 'lily-detective', 'perfect-pitch']:
            self.assertIn(pin, t['pins'])
        self.assertEqual(len(t['guestEn']), 64)
        self.assertIsNone(self.page.evaluate("localStorage.getItem('mapachez_fun_v1')"), 'Nothing is saved before playing')
        self.page.locator('#title-quick').click()
        for n in range(5):
            self.assertEqual(self.page.locator('.fun-rush').count(), 0, 'New players get calm shifts first')
            self.answer(best=True)
            if n >= 1:
                self.assertIn(f'Combo ×{n + 1}', self.page.locator('.fun-combo').inner_text())
            self.assertEqual(self.page.locator('.fun-wiggle').count(), 1)
            self.assertEqual(self.page.locator('.gm-avatar.fun-cheer.best').count(), 1)
            self.next_button()
        self.page.wait_for_selector('.gm-summary')
        self.assertIn('NEW CLUE · 1 OF 7', self.page.locator('.fun-clue').inner_text())
        self.assertIn('Tomorrow: clue 2', self.page.locator('.fun-tease').inner_text())
        f = self.fun()
        self.assertEqual(f['mystery']['clues'], 1)
        self.assertEqual(f['comboBest'], 5)
        # One clue a night: a second shift the same day finds none and nobody is scolded.
        self.page.locator('#shift-actions').get_by_role('button', name='Another quick shift').click()
        self.play_shift()
        self.assertEqual(self.page.locator('.fun-clue').count(), 0)
        self.assertEqual(self.fun()['mystery']['clues'], 1)
        self.page.locator('#shift-actions').get_by_role('button', name='Manor notebook').click()
        notebook = self.page.locator('#modal-body').inner_text()
        self.assertIn('Who keeps moving the lobby lilies?', notebook)
        self.assertIn('1 of 7 clues found', notebook)
        self.assertIn('A calm, ordinary night', notebook)

    def test_02_regulars_remember_how_you_treated_them_and_warm_up(self):
        self.page.locator('#title-quick').click()
        first = self.page.locator('#modal-heading').inner_text()
        self.assertEqual(first, 'The phone rings at 8:12 PM')
        self.assertEqual(self.page.locator('.fun-remember').count(), 0, 'A stranger the first time')
        self.answer(best=False)
        g = self.fun()['guests']['Dr. Evangeline Merriweather']
        self.assertEqual(g, {'visits': 1, 'best': 0, 'last': 'miss'})
        self.next_button()
        # Her second moment comes up next: she remembers kindly, even after a miss.
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), 'The profile is already telling you')
        remember = self.page.locator('.fun-remember').inner_text()
        self.assertIn('REMEMBERS YOU', remember)
        self.assertIn('plenty of time', remember)
        self.answer(best=True)
        letter = self.page.locator('.fun-letter').inner_text()
        self.assertIn('warms up to you', letter)
        self.assertIn('Thank you for not asking twice', letter)
        self.next_button()
        self.assertIn('You again. Good.', self.page.locator('.fun-remember').inner_text())

    def test_03_corrupt_fun_save_resets_only_the_fun_layer(self):
        self.page.evaluate("localStorage.setItem('mapachez_fun_v1','{oops');localStorage.setItem('mapachez_growth_v1',JSON.stringify({version:1,answers:7,pts:{trust:30,care:0,team:0}}))")
        self.page.reload()
        self.assertEqual(self.fun()['mystery']['clues'], 0)
        self.assertEqual(self.page.evaluate('window.funTest.growth.answers'), 7, 'Growth is untouched')
        self.assertIn('Lilies 0/7', self.page.locator('#growth-notebook').inner_text())


class Rush(Fun):
    seed = {'mapachez_growth_v1': growth_save(shifts=2, answers=10)}

    def test_01_third_shift_brings_three_guests_at_once_with_a_gentle_lantern(self):
        self.page.locator('#title-quick').click()
        for _ in range(2):
            self.answer(best=True)
            self.next_button()
        self.page.wait_for_selector('#modal-body .fun-rush')
        self.assertIn('Three guests need you at once!', self.page.locator('#modal-heading').inner_text())
        self.assertEqual(self.page.locator('.fun-rush-card').count(), 3)
        self.assertEqual(self.page.locator('.fun-lantern[role=timer]').count(), 1)
        moments = self.page.evaluate('window.funTest.moments')
        urgent = ['Guest Ledger', 'Menu Knowledge', 'Wellness Guidance', 'Housekeeping Entry', 'Conservatory Safety', 'Front Office Placement', 'Garden Truth Chain', 'Animal Guest Record']
        cards = self.page.locator('.fun-rush-card small:first-of-type').all_inner_texts()
        depts = [next(m['dept'] for m in moments if m['title'] == c) for c in cards]
        self.assertTrue(any(d in urgent for d in depts), 'Every rush includes a health or safety need')
        # Pick the urgent guest with the keyboard.
        self.page.keyboard.press(str(next(k for k, d in enumerate(depts) if d in urgent) + 1))
        self.assertIn('RUSH HOUR · GUEST 3 OF 5', self.page.locator('.scene-head .overline').inner_text())
        self.answer(best=True)
        self.assertIn('Good call', self.page.locator('.fun-callout').inner_text())
        self.next_button()
        self.page.wait_for_selector('#modal-body .fun-rush')
        self.assertEqual(self.page.locator('.fun-rush-card').count(), 2)
        self.assertIn('Who’s next?', self.page.locator('#modal-heading').inner_text())
        self.page.locator('.fun-rush-card').first.click()
        self.answer(best=True)
        self.next_button()
        self.assertEqual(self.page.locator('.fun-rush').count(), 0, 'The last guest needs no choosing')
        self.answer(best=False)
        self.next_button()
        self.page.wait_for_selector('.gm-summary')
        self.assertIn('Rush hour handled', self.page.locator('.fun-sum').inner_text())
        f = self.fun()
        self.assertEqual(f['rush'], {'relaxed': False, 'done': 1, 'cool': 1, 'fast': 1})
        pins = self.page.evaluate('window.funTest.growth.pins')
        for pin in ['rush-hero', 'cool-head', 'lantern-glow']:
            self.assertIn(pin, pins)

    def test_02_relaxed_rush_has_no_timer_and_is_remembered(self):
        self.page.locator('#title-quick').click()
        for _ in range(2):
            self.answer(best=True)
            self.next_button()
        self.page.wait_for_selector('#modal-body .fun-rush')
        self.page.locator('#fun-relax').click()
        self.assertEqual(self.page.locator('.fun-lantern[role=timer]').count(), 0)
        self.assertIn('no timer', self.page.locator('.fun-lantern').inner_text())
        self.assertTrue(self.fun()['rush']['relaxed'])
        self.play_shift_rest()
        self.assertIn('at your own pace', self.page.locator('.fun-sum').inner_text())
        self.assertEqual(self.fun()['rush']['fast'], 0, 'No timer, no timed pin, no penalty')

    def play_shift_rest(self):
        for _ in range(3):
            if self.page.locator('#modal-body .fun-rush').count():
                self.page.locator('.fun-rush-card').first.click()
            self.answer(best=True)
            self.next_button()
        self.page.wait_for_selector('.gm-summary')


class Wedding(Fun):
    day = WEDDING_DAY
    seed = {'mapachez_growth_v1': growth_save(shifts=3, answers=15)}

    def test_01_wedding_night_changes_the_shift_and_always_brings_a_rush(self):
        self.assertEqual(self.page.evaluate('window.funTest.tonight'), 'wedding')
        self.page.locator('#title-quick').click()
        night = self.page.locator('.fun-night.wedding').inner_text()
        self.assertIn('Wedding night', night)
        self.assertIn('emotional uncle', night)
        self.play_shift()
        self.assertIn('Wedding night', self.page.locator('#modal-body').inner_text())
        self.assertEqual(self.fun()['nights'], {'wedding': 1})
        self.assertIn('wedding-bells', self.page.locator('body').evaluate('() => Object.keys(window.funTest.growth.pins).join(" ")'))
        self.assertEqual(self.fun()['rush']['done'], 1, 'Odd-numbered shifts still rush on a wedding night')


class Mystery(Fun):
    seed = {'mapachez_fun_v1': {'version': 1, 'mystery': {'clues': 5, 'day': '2026-11-12', 'solved': False, 'wrong': []}}}

    def test_01_five_clues_let_you_name_a_suspect_and_wrong_guesses_are_kind(self):
        self.page.locator('#title-quick').click()
        self.play_shift()
        self.assertIn('NEW CLUE · 6 OF 7', self.page.locator('.fun-clue').inner_text())
        self.page.locator('.fun-open-case').click()
        self.page.wait_for_selector('#fun-suspects .choice')
        self.page.locator('#fun-suspects .choice', has_text='Evelyn Hart').click()
        self.assertIn('I put them back', self.page.locator('.fun-callout').inner_text())
        self.assertTrue(self.page.locator('#fun-suspects .choice', has_text='Evelyn Hart').is_disabled())
        self.page.locator('#fun-suspects .choice', has_text='Harold Thistle').click()
        self.assertIn('Case closed', self.page.locator('.fun-solved').inner_text())
        self.assertIn('handoff that never happened', self.page.locator('.fun-solved').inner_text())
        f = self.fun()
        self.assertTrue(f['mystery']['solved'])
        self.assertIn('lily-detective', self.page.evaluate('window.funTest.growth.pins'))


class Storm(Fun):
    day = STORM_DAY
    seed = {'mapachez_profile_v1': {'version': 1, 'mode': 'solo', 'lang': 'es', 'hooked': True}}

    def test_01_storm_night_paints_the_manor_and_speaks_spanish(self):
        self.assertEqual(self.page.evaluate('window.funTest.tonight'), 'storm')
        self.page.locator('#begin').click()
        self.page.wait_for_selector('#fun-sky.storm', state='attached')
        anim = self.page.evaluate("getComputedStyle(document.getElementById('fun-sky')).animationName")
        self.assertEqual(anim, 'none', 'Reduce motion keeps the rain still')
        self.assertIn('Esta noche: Noche de tormenta', self.page.locator('#growth').inner_text())
        self.page.locator('#growth-notebook').click()
        text = self.page.locator('#modal-body').inner_text()
        self.assertIn('¿Quién sigue moviendo los lirios del vestíbulo?', text)
        self.assertIn('Se acerca una tormenta', text)


class Phone(Fun):
    seed = {'mapachez_growth_v1': growth_save(shifts=2, answers=10)}

    def setUp(self):
        super().setUp(viewport={'width': 390, 'height': 844})

    def test_01_rush_board_fits_a_phone(self):
        self.page.locator('#title-quick').click()
        for _ in range(2):
            self.answer(best=True)
            self.next_button()
        self.page.wait_for_selector('#modal-body .fun-rush')
        overflow = self.page.evaluate('document.documentElement.scrollWidth - innerWidth')
        self.assertLessEqual(overflow, 0)
        box = self.page.locator('.fun-rush-card').first.bounding_box()
        self.assertLessEqual(box['x'] + box['width'], 390)


for name in [n for n in dir(base.Growth) if n.startswith('test_')]:
    for cls in (Fun, CalmNight, Rush, Wedding, Mystery, Storm, Phone):
        setattr(cls, name, None)
Fun.test_placeholder = None

if __name__ == '__main__':
    unittest.main(verbosity=2)
