"""Browser regression checks; requires Python Playwright and a Chromium executable.

Run: python tests/test_training_integration.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Every test uses isolated browser storage. Test-only read access to the existing
game closure is injected into the HTTP response, never into the shipped HTML.
"""
import base64
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading
import unittest

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text()
INSPECTOR = """
Object.defineProperty(window,'manorTest',{get:()=>({
 state:structuredClone(state),festivalActive,festivalPosition:{...festivalPosition},
 memories:structuredClone(memoryBook),paused:world.options.paused(),
 points:Object.keys(FESTIVAL_POINTS)
})});
"""
TEST_HTML = HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class TrainingIntegration(unittest.TestCase):
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
        self.context = self.browser.new_context(viewport={'width':1440, 'height':1000}, reduced_motion='reduce')
        # Returning-player fixture: skip the first-visit welcome choice (covered in test_setup.py).
        self.context.add_init_script("try{if(!localStorage.getItem('mapachez_profile_v1'))localStorage.setItem('mapachez_profile_v1',JSON.stringify({version:1,mode:'solo',lang:'en',hooked:true}))}catch(e){}")
        # Returning-player fixture: the whole manor is open (night-by-night unlocks are covered in test_nights.py).
        self.context.add_init_script("try{if(!localStorage.getItem('mapachez_nights_v1'))localStorage.setItem('mapachez_nights_v1',JSON.stringify({all:true,seen:10,fresh:[]}))}catch(e){}")
        self.page = self.context.new_page()
        self.errors = []
        self.requests = []
        self.page.on('pageerror', lambda error:self.errors.append(str(error)))
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
        errors = self.errors[:]
        requests = self.requests[:]
        self.context.close()
        self.assertEqual(errors, [], 'Uncaught browser errors')
        self.assertEqual(requests, [], 'The integration should work without external requests')

    def start_manor(self):
        self.page.locator('#begin').click()
        self.page.wait_for_function('window.manorTest.state !== null')

    def open_training(self, title=False):
        self.page.locator('#title-training' if title else '#training-button').click()
        self.page.wait_for_function("document.getElementById('silver-key-frame')?.contentWindow?.SilverKeyManorBridge")
        return self.page.frame_locator('#silver-key-frame')

    def training_eval(self, code):
        return self.page.locator('#silver-key-frame').element_handle().content_frame().evaluate(code)

    def snapshot(self):
        return self.page.evaluate('window.manorTest')

    def close_training(self):
        self.page.locator('#silver-key-return').click()
        self.page.wait_for_function("!document.getElementById('silver-key-frame')")

    def select(self, text):
        self.page.locator('#modal-body').get_by_role('button', name=text, exact=False).click()

    def quick_travel(self):
        self.page.locator('#settings-button').click()
        self.page.get_by_role('checkbox', name='Quick travel', exact=True).check()
        self.page.locator('#modal-close').click()

    def visit(self, name):
        self.page.locator('#places-button').click()
        self.select(name)
        self.page.wait_for_function("document.getElementById('modal').open")

    def test_01_title_and_world_return_without_moving_or_advancing_story(self):
        self.open_training(title=True)
        self.assertEqual(self.training_eval('rounds.length'), 52)
        self.close_training()
        self.assertTrue(self.page.locator('#title-screen').is_visible())
        self.start_manor()
        self.page.locator('#world').focus()
        self.page.keyboard.down('d')
        self.page.wait_for_timeout(200)
        self.page.keyboard.up('d')
        self.page.wait_for_timeout(300)
        before = self.snapshot()
        self.assertGreater(before['state']['player']['x'], 260)
        self.open_training()
        self.assertTrue(self.snapshot()['paused'])
        self.page.keyboard.press('ArrowDown')
        self.page.wait_for_timeout(150)
        self.close_training()
        after = self.snapshot()
        self.assertEqual(before['state'], after['state'])
        self.assertFalse(after['paused'])

    def test_02_answer_and_unfinished_shift_resume_without_duplicate_awards(self):
        self.start_manor()
        self.open_training()
        self.training_eval("startGame('associate')")
        frame = self.page.frame_locator('#silver-key-frame')
        frame.locator('#choices button[data-source-index="1"]').click()
        before = self.training_eval('({xp:state.xp,round:state.round,results:state.results,order:[...els.choices.children].map(b=>b.dataset.sourceIndex)})')
        self.close_training()
        self.open_training()
        after = self.training_eval('({xp:state.xp,round:state.round,results:state.results,order:[...els.choices.children].map(b=>b.dataset.sourceIndex)})')
        self.assertEqual(before, after)
        self.assertTrue(self.page.frame_locator('#silver-key-frame').locator('#choices button').first.is_disabled())
        self.page.frame_locator('#silver-key-frame').locator('#nextBtn').click()
        self.assertEqual(self.training_eval('state.round'), 1)
        self.close_training()
        self.page.reload()
        self.page.locator('#continue').click()
        self.open_training()
        self.assertEqual(self.training_eval('state.round'), 1)
        self.assertEqual(self.training_eval('state.xp'), before['xp'])

    def test_03_all_rounds_complete_with_varied_answers_and_persistent_career(self):
        self.start_manor()
        self.open_training()
        result = self.training_eval("""() => {
          startGame('associate'); const slots=[];
          for(let i=0;i<rounds.length;i++) {
            const round=rounds[state.round];
            const best=round.choices.reduce((b,c,i,a)=>c[1]+c[2]+c[3]>a[b][1]+a[b][2]+a[b][3]?i:b,0);
            slots.push([...els.choices.children].findIndex(b=>Number(b.dataset.sourceIndex)===best));
            choose(best);
            const correct=[...els.choices.children].filter(b=>b.classList.contains('correct')).map(b=>Number(b.dataset.sourceIndex));
            if(!correct.includes(best)) throw Error('Shuffled feedback points to wrong answer');
            nextRound();
          }
          return {slots,career:{...careerState},banked:state.shiftBanked,saved:localStorage.getItem(MANOR_TRAINING_SESSION)};
        }""")
        self.assertEqual(len(set(result['slots'])), 3)
        self.assertTrue(result['banked'])
        self.assertIsNone(result['saved'])
        self.assertGreater(result['career']['xp'], 1000)
        self.training_eval('endGame()')
        self.assertEqual(self.training_eval('careerState.xp'), result['career']['xp'])
        self.close_training()
        self.page.reload()
        self.page.locator('#continue').click()
        self.open_training()
        self.assertEqual(self.training_eval('careerState.xp'), result['career']['xp'])
        self.assertFalse(self.training_eval('state.started'))

    def test_08_training_sections_and_portraits_stay_inside_the_workspace(self):
        self.open_training(title=True)
        self.assertTrue(self.training_eval("['gameArea','nightDeskTraining','reservationProfiles','hmsGlossary'].every(id=>!!document.getElementById(id).closest('main.main'))"))
        self.assertTrue(self.training_eval("hotelGuests.every(guest=>getGuestPortraitSource(guest).startsWith('data:image/'))"))
        self.training_eval("openPortraitViewer(hotelGuests[0])")
        frame=self.page.frame_locator('#silver-key-frame')
        frame.locator('#portraitDialogImage').wait_for(state='visible')
        self.page.wait_for_function("document.getElementById('silver-key-frame').contentWindow.document.getElementById('portraitDialogImage').naturalWidth>0")

    def test_04_festival_booths_and_memory_book_survive_training(self):
        self.page.locator('#explore-festival').click()
        self.assertTrue(self.snapshot()['festivalActive'])
        self.quick_travel()
        self.page.locator('#festival-directory-shortcut').click()
        self.page.locator('[data-exhibitor="stargazer"]').click()
        self.page.locator('#memory-favorite').click()
        self.page.locator('#modal-close').click()
        self.page.locator('#world').focus()
        self.page.keyboard.down('a')
        self.page.wait_for_timeout(180)
        self.page.keyboard.up('a')
        before = self.snapshot()
        self.open_training()
        self.close_training()
        after = self.snapshot()
        self.assertTrue(after['festivalActive'])
        self.assertEqual(before['festivalPosition'], after['festivalPosition'])
        self.assertEqual(before['memories'], after['memories'])
        self.assertIn('stargazer', after['memories']['favorites'])
        self.assertTrue({'music','gallery','books','stage','welcome'}.issubset(set(after['points'])))
        self.visit('Welcome')
        self.select('Visit the Silver Key practice desk')
        self.page.wait_for_function("document.getElementById('silver-key-frame')?.contentWindow?.SilverKeyManorBridge")
        self.close_training()
        self.assertTrue(self.snapshot()['festivalActive'])

    def test_05_guest_glossary_lab_and_night_board_entry_points(self):
        self.start_manor()
        self.open_training()
        self.page.locator('[data-training-target="guest"]').click()
        self.assertEqual(self.training_eval('hotelGuests.length'), 23)
        self.page.locator('[data-training-target="glossary"]').click()
        self.page.frame_locator('#silver-key-frame').locator('#globalHmsGlossarySearch').fill('folio')
        self.assertIn('folio', self.page.frame_locator('#silver-key-frame').locator('#globalHmsPanel').inner_text().lower())
        self.page.locator('[data-training-target="lab"]').click()
        self.assertEqual(self.training_eval('activeGlobalHmsTool'), 'lab')
        self.page.locator('[data-training-target="night"]').click()
        self.page.frame_locator('#silver-key-frame').locator('#nightBoardRooms button').first.click()
        step = self.training_eval('nightBoardState.rooms[0].step')
        self.close_training()
        self.open_training()
        self.assertEqual(self.training_eval('nightBoardState.rooms[0].step'), step)

    def test_06_front_desk_story_and_training_remain_separate(self):
        self.start_manor()
        self.quick_travel()
        self.visit('Front desk')
        self.select('I’m ready')
        self.visit('Front desk')
        self.select('Practice at the Silver Key desk')
        self.page.wait_for_function("document.getElementById('silver-key-frame')?.contentWindow?.SilverKeyManorBridge")
        self.close_training()
        self.assertTrue(self.snapshot()['state']['flags']['briefed'])
        self.visit('Room 203')
        # Taking an authored story order must still advance the original task flow.
        self.assertIn('pumpkin soup', self.page.locator('#modal-body').inner_text().lower())
        self.select('Before I place the order')
        self.assertIn('quote', self.page.locator('#modal-body').inner_text().lower())

    def test_07_mobile_keyboard_return_and_corrupt_save_recovery(self):
        self.page.set_viewport_size({'width':390,'height':844})
        self.page.evaluate("localStorage.setItem('mapachez_silver_key_active_shift_v1','not-json')")
        self.open_training(title=True)
        self.assertEqual(self.training_eval('state.started'), False)
        self.assertLessEqual(self.page.locator('#modal').bounding_box()['width'], 390)
        self.training_eval("startGame('associate')")
        frame=self.page.frame_locator('#silver-key-frame')
        frame.locator('#choices button[data-source-index="1"]').click()
        frame.locator('#nextBtn').click()
        self.assertEqual(self.training_eval('state.round'), 1)
        self.assertLessEqual(self.training_eval('document.documentElement.scrollWidth'), self.training_eval('innerWidth'))
        self.training_eval('document.body.focus()')
        self.page.locator('#silver-key-frame').focus()
        self.page.keyboard.press('Escape')
        self.page.wait_for_function("!document.getElementById('silver-key-frame')")
        self.assertTrue(self.page.locator('#title-screen').is_visible())


if __name__ == '__main__':
    unittest.main(verbosity=2)
