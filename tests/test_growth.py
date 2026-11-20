"""Browser checks for guest moments, growth bars, pins, nightly streak and wardrobe.

Run: python tests/test_growth.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Uses the same isolated-storage, no-network harness as test_training_integration.py.
Test-only read access is injected into the HTTP response, never the shipped HTML.
"""
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading
import unittest

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')
INSPECTOR = """
Object.defineProperty(window,'growthTest',{get:()=>({
 growth:structuredClone(growth),moments:GUEST_MOMENTS,state:state?structuredClone(state):null,
 tiers:TIERS,pins:PINS.map(p=>p.id),goGuest:()=>world.go('guest-moment'),available:guestMomentAvailable()
})});
"""
TEST_HTML = HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')
BEST_CLICK = """() => {
  const t = window.growthTest, title = document.getElementById('modal-heading').innerText;
  const m = t.moments.find(x => x.title === title);
  const best = Math.max(...m.choices.map(c => c[1]));
  const text = m.choices.find(c => c[1] >= best)[0];
  [...document.querySelectorAll('#modal-body .choice')].find(b => b.innerText.includes(text)).click();
}"""
WORST_CLICK = BEST_CLICK.replace('Math.max', 'Math.min').replace('c[1] >= best', 'c[1] <= best')


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class Growth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}/index.html'
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(executable_path=os.getenv('CHROMIUM_PATH', '/usr/bin/chromium'), headless=True, args=['--no-sandbox'])

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self, viewport=None):
        self.context = self.browser.new_context(viewport=viewport or {'width': 1440, 'height': 1000}, reduced_motion='reduce')
        # Returning-player fixture: skip the first-visit welcome choice (covered in test_setup.py).
        self.context.add_init_script("try{if(!localStorage.getItem('mapachez_profile_v1'))localStorage.setItem('mapachez_profile_v1',JSON.stringify({version:1,mode:'solo',lang:'en',hooked:true}))}catch(e){}")
        # Returning-player fixture: the whole manor is open (night-by-night unlocks are covered in test_nights.py).
        if getattr(self, 'open_manor', True):
            self.context.add_init_script("try{if(!localStorage.getItem('mapachez_nights_v1'))localStorage.setItem('mapachez_nights_v1',JSON.stringify({all:true,seen:10,fresh:[]}))}catch(e){}")
        self.page = self.context.new_page()
        self.errors, self.requests = [], []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        self.page.route('**/*', self.route)
        self.page.goto(self.url)

    def route(self, route):
        if route.request.url == self.url:
            route.fulfill(status=200, content_type='text/html', body=TEST_HTML)
        elif route.request.url.startswith(f'http://127.0.0.1:{self.server.server_port}/'):
            route.continue_()
        else:
            self.requests.append(route.request.url)
            route.abort()

    def tearDown(self):
        errors, requests = self.errors[:], self.requests[:]
        self.context.close()
        self.assertEqual(errors, [], 'Uncaught browser errors')
        self.assertEqual(requests, [], 'Growth features must work without external requests')

    def growth(self):
        return self.page.evaluate('window.growthTest.growth')

    def answer(self, best=True):
        self.page.wait_for_selector('#modal-body .choice')
        self.page.evaluate(BEST_CLICK if best else WORST_CLICK)
        self.page.wait_for_selector('#modal-body .gm-result')

    def next_button(self):
        self.page.locator('#modal-body .gm-result .action-row .primary-button').click()

    def test_01_perfect_quick_shift_from_title_fills_bars_and_awards_pins(self):
        self.assertEqual(len(self.page.evaluate('window.growthTest.moments')), 52)
        self.page.locator('#title-quick').click()
        for _ in range(5):
            self.answer(best=True)
            self.next_button()
        self.page.wait_for_selector('.gm-summary')
        self.assertIn('5 / 5', self.page.locator('.gm-summary').inner_text())
        g = self.growth()
        self.assertEqual(g['answers'], 5)
        self.assertEqual(sum(g['pts'].values()), 50)
        self.assertEqual(g['shifts'], 1)
        self.assertEqual(g['perfect'], 1)
        self.assertEqual(g['nights']['count'], 1)
        for pin in ['first-hello', 'hat-trick', 'shift-done', 'perfect-shift', 'tier-bronze']:
            self.assertIn(pin, g['pins'])
        self.assertIsNone(self.page.evaluate("localStorage.getItem('mapachez_midnight_rehearsal_v1')"), 'Quick shift must not create a story save')
        self.page.reload()
        self.assertEqual(self.growth()['answers'], 5, 'Growth persists across reloads')

    def test_02_missed_moment_returns_and_earns_second_chance(self):
        self.page.locator('#title-quick').click()
        first = self.page.locator('#modal-heading').inner_text()
        self.answer(best=False)
        self.assertIn('come back soon', self.page.locator('.gm-result').inner_text())
        titles = []
        for _ in range(4):
            self.next_button()
            titles.append(self.page.locator('#modal-heading').inner_text())
            self.answer(best=True)
        self.next_button()
        self.page.locator('#shift-actions').get_by_role('button', name='Another quick shift').click()
        self.assertNotIn(first, titles)
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), first, 'The missed guest comes back first')
        self.assertIn('second chance', self.page.locator('.gm-again').inner_text())
        self.answer(best=True)
        self.assertIn('second-chance', self.growth()['pins'])

    def test_03_guest_in_the_manor_opens_a_moment_without_moving_the_story(self):
        self.page.locator('#begin').click()
        self.page.wait_for_function('window.growthTest.state !== null')
        self.assertFalse(self.page.evaluate('window.growthTest.available'), 'No waiting guest before the briefing')
        self.page.locator('#settings-button').click()
        self.page.get_by_role('checkbox', name='Quick travel', exact=True).check()
        self.page.locator('#modal-close').click()
        self.page.locator('.task-card').first.click()
        for _ in range(8):
            if self.page.evaluate('window.growthTest.state.flags.briefed'):
                break
            self.page.locator('#modal-body .choice').first.click()
        self.page.keyboard.press('Escape')
        self.assertTrue(self.page.evaluate('window.growthTest.available'))
        before = self.page.evaluate('window.growthTest.state')
        self.page.evaluate('window.growthTest.goGuest()')
        self.page.wait_for_selector('#modal-body .choice')
        self.assertIn('A GUEST NEEDS A HAND', self.page.locator('#modal-body .overline').first.inner_text().upper())
        self.answer(best=True)
        self.page.locator('#modal-body').get_by_role('button', name='Back to the manor').click()
        after = self.page.evaluate('window.growthTest.state')
        self.assertEqual(before['minute'], after['minute'], 'Guest moments never advance the story clock')
        self.assertEqual(before['metrics'], after['metrics'])
        self.assertEqual(self.growth()['answers'], 1)
        self.assertIn('1 night', self.page.locator('#growth').inner_text())

    def test_04_level_up_unlocks_an_outfit_and_corrupt_saves_recover(self):
        self.page.evaluate("localStorage.setItem('mapachez_growth_v1','{not json')")
        self.page.reload()
        self.assertEqual(self.growth()['answers'], 0)
        seeded = {'version': 1, 'pts': {'trust': 19, 'care': 19, 'team': 19}, 'seen': {}, 'answers': 0}
        self.page.evaluate("s => localStorage.setItem('mapachez_growth_v1', s)", json.dumps(seeded))
        self.page.reload()
        self.page.locator('#title-quick').click()
        self.answer(best=True)
        self.assertIn('Bronze', self.page.locator('.gm-gain').inner_text())
        self.page.keyboard.press('Escape')
        self.page.locator('#title-memories').click()
        self.page.locator('#memory-tabs').get_by_role('button', name='Pins & wardrobe').click()
        copper = self.page.locator('.look', has_text='Copper coat')
        self.assertTrue(copper.is_enabled())
        self.assertFalse(self.page.locator('.look', has_text='Legend').is_enabled())
        copper.click()
        self.assertEqual(self.growth()['look'], 'copper')
        self.assertIn('Secret pin', self.page.locator('.pin-grid').inner_text())

    def test_05_phone_layout_fits(self):
        self.context.close()
        self.setUp({'width': 390, 'height': 844})
        self.page.locator('#begin').click()
        self.page.wait_for_selector('#growth .growth-bar')
        width = self.page.evaluate('document.documentElement.scrollWidth')
        self.assertLessEqual(width, 390)
        self.page.locator('#growth-shift').click()
        self.answer(best=True)
        box = self.page.locator('#modal').bounding_box()
        self.assertLessEqual(box['x'] + box['width'], 390)


if __name__ == '__main__':
    unittest.main(verbosity=2)
