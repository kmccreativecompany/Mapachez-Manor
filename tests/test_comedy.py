"""Browser checks for the clean-comedy layer: silly choices, guest quips, running gags,
Delores's shift lines, the comment card of the day and the comedy pins.

Run: python tests/test_comedy.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'comedyTest',{get:()=>({
 growth:structuredClone(growth),moments:GUEST_MOMENTS,comedy:COMEDY,pins:PINS.map(p=>p.id),beat:comedyBeat
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class Comedy(base.Growth):
    """Reuses the growth harness but none of its tests."""

    def growth(self):
        return self.page.evaluate('window.comedyTest.growth')

    def test_01_every_moment_has_jokes_except_the_tender_one(self):
        t = self.page.evaluate('window.comedyTest')
        titles = {m['title'] for m in t['moments']}
        for section in ('silly', 'win'):
            keys = set(t['comedy'][section])
            self.assertEqual(keys - titles, set(), f'{section} keys must match moment titles')
            self.assertEqual(titles - keys, {'The flower that matters'}, f'{section} covers every other moment')
        for pin in ['buffet', 'strategic-retreat', 'room-13', 'fern-whisperer']:
            self.assertIn(pin, t['pins'])

    def test_02_silly_choice_is_kind_counts_as_a_miss_and_shows_the_lesson(self):
        self.page.locator('#title-quick').click()
        self.page.wait_for_selector('#modal-body .gm-silly')
        self.assertEqual(self.page.locator('#modal-body .choice').count(), 4)
        numbers = self.page.locator('#modal-body .choice').evaluate_all('bs => bs.map(b => b.dataset.choice + b.firstElementChild.textContent)')
        self.assertEqual(numbers, ['11', '22', '33', '44'])
        self.page.locator('#modal-body .gm-silly').click()
        result = self.page.locator('.gm-result').inner_text()
        self.assertIn('🦝', result)
        self.assertIn('BEST ANSWER', result)
        self.assertIn('come back soon', result)
        g = self.growth()
        self.assertTrue(g['flags'].get('silly'))
        self.assertIn('strategic-retreat', g['pins'])
        self.assertTrue(next(iter(g['seen'].values()))['miss'])
        self.assertEqual(sum(g['pts'].values()), 1, 'A silly pick scores like a miss')

    def test_03_best_answer_gets_a_quip_and_shifts_end_with_delores_and_a_card(self):
        self.page.locator('#title-quick').click()
        for n in range(5):
            self.answer(best=True)
            self.assertEqual(self.page.locator('.gm-quip').count(), 1)
            self.assertEqual(self.page.locator('.gm-meanwhile').count(), 1 if n in (1, 3) else 0)
            self.next_button()
        self.page.wait_for_selector('.gm-card')
        t = self.page.evaluate('window.comedyTest')
        summary = self.page.locator('#modal-body').inner_text()
        self.assertIn(t['comedy']['deloresPerfect'][0], summary)
        self.assertTrue(any(card in summary for card in t['comedy']['cards']))

    def test_04_running_gag_pays_off_and_awards_a_secret_pin(self):
        t = self.page.evaluate('window.comedyTest')
        gags = len(t['comedy']['gags'])
        beats = len(t['comedy']['gags'][1]['beats'])
        # Answer count right before the Room 13 payoff beat.
        target = 2 * ((beats - 1) * gags + 1 + 1)
        last = self.page.evaluate(f'window.comedyTest.beat({target})')
        self.assertEqual(last['id'], 'room13')
        self.assertTrue(last['last'])
        self.page.evaluate(f"""() => {{
          const g = JSON.parse(localStorage.getItem('mapachez_growth_v1') || 'null') || {{version:1,pts:{{trust:0,care:0,team:0}},seen:{{}},nights:{{}},pins:{{}},story:{{}},flags:{{}}}};
          g.version = 1; g.answers = {target - 1};
          localStorage.setItem('mapachez_growth_v1', JSON.stringify(g));
        }}""")
        self.page.reload()
        self.page.locator('#title-quick').click()
        self.answer(best=True)
        self.assertIn('linen closet', self.page.locator('.gm-meanwhile').inner_text())
        self.assertIn('room-13', self.growth()['pins'])


for name in [n for n in dir(base.Growth) if n.startswith('test_')]:
    setattr(Comedy, name, None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
