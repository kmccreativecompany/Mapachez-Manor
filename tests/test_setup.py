"""Browser checks for play modes, the first-minute guest, role tracks, reports and
certificates, hotel packs, score codes and the team board, Spanish, and the demo copy.

Run: python tests/test_setup.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Same isolated-storage, no-network harness as the other suites. Test-only read access
is injected into the HTTP response, never the shipped HTML.
"""
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import threading
import unittest

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')
INSPECTOR = """
Object.defineProperty(window,'setupTest',{get:()=>({
 profile:structuredClone(profile),pack:structuredClone(pack),growth:structuredClone(growth),core:CORE_MOMENTS,
 moments:GUEST_MOMENTS.map(m=>({title:m.title,dept:m.dept,role:roleOf(m),pack:!!m.pack,best:Math.max(...m.choices.map(c=>c[1]))})),
 pins:PINS.map(p=>p.id),demo:DEMO_BUILD,week:weekKey(),code:scoreCode(),packCode:packCode(),
 readCode:x=>readScoreCode(x),shift:shift?structuredClone(shift):null
})});
"""
TEST_HTML = HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')
DEMO_HTML = TEST_HTML.replace('const DEMO_BUILD=false;', 'const DEMO_BUILD=true;')
def seeded(growth=None, profile=None, pack=None):
    parts = []
    for key, value in (('mapachez_growth_v1', growth), ('mapachez_profile_v1', profile), ('mapachez_pack_v1', pack)):
        if value is not None:
            parts.append(f"localStorage.setItem({json.dumps(key)},{json.dumps(json.dumps(value))});")
    return "if(!sessionStorage.getItem('seeded')){" + ''.join(parts) + "sessionStorage.setItem('seeded','1');}"


def all_best(n=64):
    return {str(i): {'best': 1, 'tries': 1, 'miss': False, 'due': 0, 'at': i + 1} for i in range(n)}


GROWTH = {'version': 1, 'pts': {'trust': 30, 'care': 10, 'team': 5}, 'seen': {}, 'answers': 9, 'run': 0, 'bestRun': 2, 'missRun': 0,
          'nights': {'last': '', 'count': 0, 'best': 1}, 'pins': {}, 'shifts': 1, 'perfect': 0, 'story': {}, 'flags': {}, 'look': 'house'}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class Setup(unittest.TestCase):
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

    def setUp(self):
        self.errors, self.requests, self.contexts = [], [], []

    def open(self, init='', viewport=None, demo=False):
        context = self.browser.new_context(viewport=viewport or {'width': 1440, 'height': 1000}, reduced_motion='reduce')
        context.add_init_script("window.print=()=>{window.__printed=(window.__printed||0)+1;};" + init)
        # The whole manor is open here; night-by-night unlocks are covered in test_nights.py.
        context.add_init_script("try{if(!localStorage.getItem('mapachez_nights_v1'))localStorage.setItem('mapachez_nights_v1',JSON.stringify({all:true,seen:10,fresh:[]}))}catch(e){}")
        self.contexts.append(context)
        page = context.new_page()
        page.on('pageerror', lambda error: self.errors.append(str(error)))
        body = DEMO_HTML if demo else TEST_HTML

        def route(r):
            if r.request.url == self.url:
                r.fulfill(status=200, content_type='text/html', body=body)
            elif r.request.url.startswith(f'http://127.0.0.1:{self.server.server_port}/'):
                r.continue_()
            else:
                self.requests.append(r.request.url)
                r.abort()
        page.route('**/*', route)
        page.goto(self.url)
        page.wait_for_function('window.setupTest')
        return page

    def tearDown(self):
        for context in self.contexts:
            context.close()
        self.assertEqual(self.errors, [], 'Uncaught browser errors')
        self.assertEqual(self.requests, [], 'Setup features must work without external requests')

    def state(self, page):
        return page.evaluate('window.setupTest')

    def test_01_first_visit_just_for_fun_reaches_a_guest_in_one_tap(self):
        page = self.open()
        page.wait_for_selector('#modal[open] #mode-solo')
        self.assertIn('How are you playing?', page.inner_text('#modal-heading'))
        page.click('#mode-solo')
        page.wait_for_selector('#modal-body .choice')
        self.assertIn('YOUR FIRST GUEST', page.inner_text('#modal-body .overline'))
        page.locator('#modal-body .choice').first.click()
        page.wait_for_selector('.gm-result')
        buttons = page.locator('#modal-body .gm-result .action-row button').all_inner_texts()
        self.assertTrue(any('quick shift' in b.lower() for b in buttons), buttons)
        s = self.state(page)
        self.assertEqual(s['profile']['mode'], 'solo')
        self.assertTrue(s['profile']['hooked'])
        self.assertIn('first-hello', s['growth']['pins'])
        self.assertGreater(s['profile']['week']['pts'], 0)
        page.click('#modal-body .gm-result .primary-button')
        # Right after the first guest, Delores offers to put the player's name on certificates (optional).
        page.wait_for_selector('#co-name')
        self.assertIn('gamified e-course', page.inner_text('#modal-body'))
        page.click('#co-name-row .secondary-button')
        page.wait_for_selector('#modal-body .gm-dots i')
        self.assertIsNotNone(self.state(page)['shift'])
        page.reload()
        page.wait_for_function('window.setupTest')
        page.wait_for_timeout(300)
        self.assertFalse(page.evaluate("document.getElementById('modal').open"), 'Welcome choice should not reopen')
        self.assertIn('Playing just for fun', page.inner_text('#play-mode'))

    def test_02_existing_players_keep_progress_and_are_not_interrupted(self):
        page = self.open(seeded(growth=GROWTH))
        page.wait_for_timeout(300)
        self.assertFalse(page.evaluate("document.getElementById('modal').open"))
        s = self.state(page)
        self.assertEqual(s['growth']['answers'], 9)
        self.assertEqual(s['growth']['pts']['trust'], 30)
        self.assertEqual(s['profile']['mode'], '')
        self.assertIn('How are you playing?', page.inner_text('#play-mode'))
        page.click('#play-mode-change')
        page.click('#mode-solo')
        page.wait_for_timeout(200)
        self.assertFalse(page.evaluate("document.getElementById('modal').open"), 'No first-guest detour once already playing')
        self.assertEqual(self.state(page)['profile']['mode'], 'solo')

    def test_03_hotel_role_shapes_quick_shifts_and_certificate_prints(self):
        page = self.open()
        page.click('#mode-hotel')
        page.fill('#setup-name', 'Rosa Delgado')
        page.click('[data-role="dining"]')
        page.fill('#setup-team', 'Night owls')
        page.click('#hotel-setup button[type=submit]')
        page.wait_for_selector('#modal-body .choice')
        s = self.state(page)
        self.assertEqual((s['profile']['mode'], s['profile']['role'], s['profile']['name']), ('hotel', 'dining', 'Rosa Delgado'))
        first = page.inner_text('#modal-heading')
        role = next(m['role'] for m in s['moments'] if m['title'] == first)
        self.assertIn(role, ('dining', 'all'))
        page.keyboard.press('Escape')
        page.click('#title-quick')
        page.wait_for_selector('#modal-body .gm-dots i')
        shift = self.state(page)['shift']
        roles = {s['moments'][i]['role'] for i in shift['list']}
        self.assertTrue(roles <= {'dining', 'all'}, roles)
        page.keyboard.press('Escape')
        # A finished dining track unlocks its certificate.
        seen = {str(i): {'best': 1, 'tries': 1, 'miss': False, 'due': 0, 'at': 1} for i, m in enumerate(s['moments']) if m['role'] in ('dining', 'all')}
        page.evaluate("g => localStorage.setItem('mapachez_growth_v1', JSON.stringify(g))", {**GROWTH, 'seen': seen})
        page.reload()
        page.wait_for_function('window.setupTest')
        self.assertIn('track-dining', self.state(page)['growth']['pins'])
        page.click('#title-report')
        self.assertEqual(page.locator('[data-cert]').count(), 1)
        page.click('[data-cert="dining"]')
        sheet = page.inner_text('#print-sheet')
        self.assertIn('Rosa Delgado', sheet)
        self.assertIn('Certificate of Completion', sheet)
        self.assertIn('Dining', sheet)
        page.click('#report-print')
        self.assertIn('SILVER KEY SKILLS REPORT', page.inner_text('#print-sheet'))
        self.assertEqual(page.evaluate('window.__printed'), 2)

    def test_04_manager_pack_travels_by_code_and_keeps_progress_when_edited(self):
        page = self.open(seeded(profile={'version': 1, 'mode': 'hotel', 'lang': 'en', 'hooked': True}))
        page.click('#title-manager')
        page.fill('#pack-hotel', 'The Seaside Inn')
        page.fill('#pack-manager', 'Dana Ortiz')
        page.fill('#pack-rules', 'Greet every guest within 10 feet.\nOffer an option before a no.')
        page.click('#pack-form button[type=submit]')
        for title in ('A late checkout request', 'Lost room key'):
            page.evaluate("document.querySelector('#modal-body details:has(#scenario-form)').open = true")
            page.fill('#sc-title', title)
            page.fill('#sc-guest', 'Mr. Patel')
            page.select_option('#sc-role', 'desk')
            page.fill('#sc-situation', 'Something happens at the desk: ' + title)
            page.fill('#sc-best', 'The kind and careful answer.')
            page.fill('#sc-wrong', 'The rushed answer.')
            page.click('#scenario-form button[type=submit]')
        s = self.state(page)
        self.assertEqual(s['pack']['hotel'], 'The Seaside Inn')
        self.assertEqual([m['title'] for m in s['moments'][s['core']:]], ['A late checkout request', 'Lost room key'])
        code = s['packCode']
        self.assertTrue(code.startswith('MMPACK1-'))
        # Staff member on another device: paste the code during hotel setup.
        staff = self.open()
        staff.click('#mode-hotel')
        staff.fill('#pack-paste', code)
        staff.click('#pack-paste-go')
        self.assertIn('The Seaside Inn pack ready: 2 scenarios', staff.inner_text('#pack-status'))
        staff.fill('#setup-name', 'Sam')
        staff.click('[data-role="desk"]')
        staff.click('#hotel-setup button[type=submit]')
        staff.keyboard.press('Escape')
        t = self.state(staff)
        second = t['core'] + 1
        self.assertEqual(t['moments'][second]['title'], 'Lost room key')
        self.assertIn('The Seaside Inn', staff.inner_text('#play-mode'))
        # Answer the second scenario, then the manager removes the first one: progress follows the scenario.
        staff.click('#title-manager')
        staff.locator('.scenario .text-button', has_text='Try it').nth(1).click()
        staff.locator('#modal-body .choice', has_text='The kind and careful answer.').click()
        self.assertEqual(self.state(staff)['growth']['seen'][str(second)]['best'], 1)
        staff.keyboard.press('Escape')
        staff.click('#title-manager')
        staff.locator('.scenario .text-button', has_text='Remove').first.click()
        t = self.state(staff)
        self.assertEqual([m['title'] for m in t['moments'][t['core']:]], ['Lost room key'])
        self.assertEqual(t['growth']['seen'][str(t['core'])]['best'], 1)
        self.assertNotIn(str(second), t['growth']['seen'])
        staff.reload()
        staff.wait_for_function('window.setupTest')
        self.assertEqual(self.state(staff)['growth']['seen'][str(t['core'])]['best'], 1)

    def test_05_score_codes_rank_the_team_board_and_reject_typos(self):
        page = self.open(seeded(growth=GROWTH, profile={'version': 1, 'mode': 'hotel', 'name': 'Ana', 'team': 'Night owls', 'role': 'desk', 'lang': 'en', 'hooked': True}))
        s = self.state(page)
        mine = s['code']
        decoded = page.evaluate('c => window.setupTest.readCode(c)', mine)
        self.assertEqual((decoded['n'], decoded['tm'], decoded['r']), ('Ana', 'Night owls', 'desk'))
        broken = mine[:-6] + ('A' if mine[-6] != 'A' else 'B') + mine[-5:]
        self.assertIsNone(page.evaluate('c => window.setupTest.readCode(c)', broken))
        page.click('#title-report')
        page.click('#report-share')
        self.assertEqual(page.input_value('#share-code'), mine)
        page.click('#share-board')
        page.click('#board-me')
        rows = page.locator('table.board tbody tr')
        self.assertEqual(rows.count(), 1)
        self.assertIn('Ana', rows.first.inner_text())
        friend = self.open(seeded(growth={**GROWTH, 'answers': 20, 'seen': all_best(64)}, profile={'version': 1, 'mode': 'hotel', 'name': 'Luis', 'team': 'Early birds', 'role': 'house', 'lang': 'en', 'hooked': True, 'week': {'key': s['week'], 'pts': 90}}))
        friend_code = self.state(friend)['code']
        page.fill('#board-paste', 'from Luis: ' + friend_code + '\nand junk ' + broken)
        page.click('#board-add')
        rows = page.locator('table.board tbody tr')
        self.assertEqual(rows.count(), 2)
        self.assertIn('Luis', rows.first.inner_text(), 'Higher weekly points rank first')
        self.assertEqual(page.locator('.team-race .lead').inner_text().split('\n')[0].strip(), '🏆 Early birds')
        self.assertIn('🛎️🧺🍽️🌙', rows.first.inner_text())
        page.click('#board-print')
        self.assertIn('Who finished which skills', page.inner_text('#print-sheet'))

    def test_06_spanish_moments_menus_and_reports(self):
        page = self.open()
        page.click('[data-lang="es"]')
        page.wait_for_function("window.setupTest && window.setupTest.profile.lang === 'es'")
        page.wait_for_selector('#modal[open] #mode-solo')
        self.assertIn('¿Cómo vas a jugar?', page.inner_text('#modal-heading'))
        page.click('#mode-solo')
        page.wait_for_selector('#modal-body .choice')
        self.assertIn('TU PRIMER HUÉSPED', page.inner_text('#modal-body .overline'))
        self.assertIn('¿Qué haces?', page.inner_text('#modal-body'))
        titles = [m['title'] for m in self.state(page)['moments']]
        self.assertIn('Suena el teléfono a las 8:12 PM', titles)
        self.assertEqual(page.evaluate('document.documentElement.lang'), 'es')
        page.keyboard.press('Escape')
        self.assertIn('Empieza tu noche', page.inner_text('#begin'))

    def test_07_every_word_and_moment_has_a_spanish_version(self):
        words = json.loads((ROOT / 'training/words-es.json').read_text(encoding='utf-8'))
        keys = set(re.findall(r"\bt\('((?:[^'\\]|\\.)*)'", HTML))
        self.assertEqual(sorted(k for k in keys if k not in words), [])
        english = json.loads(re.search(r'const GUEST_MOMENTS = (\[.*\]);\n', HTML).group(1))
        spanish = {m['en']: m for m in json.loads((ROOT / 'training/moments-es.json').read_text(encoding='utf-8'))}
        for m in english:
            self.assertIn(m['title'], spanish)
            self.assertEqual(len(spanish[m['title']]['choices']), len(m['choices']), m['title'])

    def test_08_demo_copy_limits_content_and_offers_the_full_edition(self):
        page = self.open(demo=True)
        s = self.state(page)
        self.assertTrue(s['demo'])
        self.assertEqual(len(s['moments']), 12)
        self.assertIn('FREE DEMO NIGHT', page.inner_text('#play-mode'))
        page.click('#mode-hotel')
        self.assertIn('Part of the full edition', page.inner_text('#modal-heading'))
        page.click('#full-back')
        page.wait_for_selector('#modal-body .choice')
        page.locator('#modal-body .choice').first.click()
        pins = self.state(page)['growth']['pins']
        self.assertNotIn('creature-friend', pins)
        self.assertNotIn('silver-tongue', pins)
        self.assertEqual(page.locator('#title-manager').count(), 0)

    def test_09_phone_screens_fit_one_thumb(self):
        page = self.open(viewport={'width': 390, 'height': 844})
        page.wait_for_selector('#modal[open] #mode-solo')
        box = page.locator('#mode-solo').bounding_box()
        self.assertGreaterEqual(box['height'], 48)
        self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 390)
        page.click('#mode-hotel')
        for sel in ('[data-role="desk"]', '#hotel-setup button[type=submit]'):
            self.assertGreaterEqual(page.locator(sel).bounding_box()['height'], 44, sel)
        page.click('#hotel-setup button[type=submit]')
        page.wait_for_selector('#modal-body .choice')
        heights = [b['height'] for b in (page.locator('#modal-body .choice').nth(i).bounding_box() for i in range(3))]
        self.assertTrue(all(h >= 52 for h in heights), heights)
        page.keyboard.press('Escape')
        page.click('#title-report')
        self.assertLessEqual(page.evaluate("document.getElementById('modal').scrollWidth"), page.evaluate("document.getElementById('modal').clientWidth") + 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
