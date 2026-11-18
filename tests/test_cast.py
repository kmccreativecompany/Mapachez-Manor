"""Browser checks for the code-drawn character kit and Muffin (Cece's cat).

Run: python tests/test_cast.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Same isolated-storage, no-network harness as the other tests; test-only access is injected into the
HTTP response, never the shipped HTML.
"""
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import threading
import unittest

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')
KIT = HTML[HTML.index('/* CHARACTER KIT v1'):HTML.index('function plant(c,x,y,s=1)')]
INSPECTOR = """
Object.defineProperty(window,'castTest',{get:()=>({
 look:(k,b)=>castLook(k,b||{}),drawPerson,muffin,spot:()=>muffinSpot(0),points:()=>world.options.extras().map(p=>p.id),
 interact:id=>interact(id),player:()=>playerLook().recipe,festival:festivalActive
})});
window.castTestOptions=()=>CAST_OPTIONS;window.deloresWelcomeTest=()=>deloresWelcome();window.profileTestLang=l=>{profile.lang=l;};window.castTestDraw=(c,ch,d)=>drawBeing(c,40,40,castMake(ch),1,d,false,1);
"""
TEST_HTML = HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class Cast(unittest.TestCase):
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
        self.context = self.browser.new_context(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
        self.context.add_init_script("try{if(!localStorage.getItem('mapachez_profile_v1'))localStorage.setItem('mapachez_profile_v1',JSON.stringify({version:1,mode:'solo',lang:'en',hooked:true}))}catch(e){}")
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
        self.assertEqual(requests, [], 'The character kit must work without external requests')

    def test_01_kit_is_small_and_never_names_the_cat(self):
        self.assertLess(len(KIT.encode('utf-8')), 48_500, 'The pixel kit, player picker and cute raccoon moods should stay under 48.5 KB')
        self.assertNotIn('opossum', KIT.lower(), 'Nobody, including the game, says what Muffin is')
        self.assertNotIn('data:image', KIT, 'Characters are drawn with code, never pictures')

    def test_02_family_are_raccoons_and_named_looks_never_change(self):
        t = 'window.castTest'
        self.assertEqual(self.page.evaluate(f"{t}.look('delores').kind"), 'raccoon')
        self.assertEqual(self.page.evaluate(f"{t}.player().kind"), 'raccoon')
        first = self.page.evaluate(f"{t}.look('Mr. Finch')")
        self.page.reload()
        self.assertEqual(self.page.evaluate(f"{t}.look('Mr. Finch')"), first, 'A named character looks the same every visit')
        kinds = self.page.evaluate(f"(()=>{{const c={{}};for(let i=0;i<400;i++){{const k={t}.look('guest#'+i).kind;c[k]=(c[k]||0)+1;}}return c;}})()")
        self.assertLess(kinds.get('raccoon', 0), 60, 'Raccoon guests are a rare treat; Delores and family always are')
        furs = self.page.evaluate(f"(()=>{{let a=0,f=0;for(let i=0;i<400;i++){{const r={t}.look('guest#'+i);if(r.kind==='raccoon'){{a++;if(r.fur)f++;}}}}return [a,f];}})()")
        self.assertTrue(0 < furs[1] < furs[0], 'Some raccoons, not all, have fun fur')
        self.assertFalse(self.page.evaluate(f"{t}.look('delores').fur"), 'Delores keeps her classic grey')
        ok = self.page.evaluate("""(()=>{const c=document.createElement('canvas').getContext('2d');
          for(const rstyle of ['button','plush','fluffy','classic'])for(const fur of [undefined,'#f5b8cf'])for(const d of ['down','up','left','right'])
            castTestDraw(c,{kind:'raccoon',rstyle,fur,specs:rstyle==='plush'},d);return c.getTransform().a===1;})()""")
        self.assertTrue(ok, 'Every raccoon style draws')
        for kind in ['monster', 'alien', 'human', 'fae', 'construct']:
            self.assertGreater(kinds.get(kind, 0), 20, kind)

    def test_06_creator_ready_every_choice_draws(self):
        ok = self.page.evaluate("""(()=>{const c=document.createElement('canvas').getContext('2d'),o=castTestOptions();
          for(const kind of o.kind)for(const extra of o.extra)for(const body of o.body)for(const d of ['down','up','left','right']){
            castTestDraw(c,{kind,extra,body,hairdo:o.hairdo[extra.length%4],outfit:o.outfit[body.length%5],eyes:1+extra.length%3},d);
            const m=c.getTransform();if(m.a!==1||m.e!==0)return 'leak '+kind+extra;}return 'ok';})()""")
        self.assertEqual(ok, 'ok')

    def test_03_every_recipe_draws_cleanly_in_every_direction(self):
        ok = self.page.evaluate("""(()=>{const t=window.castTest,c=document.createElement('canvas').getContext('2d');
          for(let i=0;i<300;i++)for(const d of ['down','up','left','right']){t.drawPerson(c,40,40,{cast:'being '+i},i,d,i%2===0,1.2);
            const m=c.getTransform();if(m.a!==1||m.e!==0||m.f!==0)return 'transform leaked at '+i;}
          t.drawPerson(c,40,40,{cast:'delores'},0,'up');return 'ok';})()""")
        self.assertEqual(ok, 'ok')

    def test_04_muffin_and_cece_are_optional_and_kind(self):
        self.page.evaluate("window.castTest.muffin.force='autumn';window.castTest.muffin.cece=true")
        self.page.locator('#explore-festival').click()
        self.page.wait_for_function('window.castTest.festival')
        self.assertIn('muffin', self.page.evaluate('window.castTest.points()'))
        self.assertIn('cece', self.page.evaluate('window.castTest.points()'))
        self.page.evaluate("window.castTest.interact('muffin')")
        self.assertEqual(self.page.evaluate('window.castTest.muffin.anim'), 'heart')
        for _ in range(3):
            self.page.evaluate("window.castTest.interact('cece')")
        self.page.evaluate("window.castTest.interact('cece')")
        self.page.wait_for_selector('#modal-heading')
        body = self.page.locator('#modal-body').inner_text()
        self.assertIn('Cat (according to owner)', body)
        self.assertIn('Do not question her heritage.', body)

    def test_05_muffin_has_a_spot_for_every_scene(self):
        for scene in ['spring', 'summer', 'autumn', 'winter', 'rain', 'fireflies', 'concert', 'thinking']:
            self.page.evaluate(f"window.castTest.muffin.force='{scene}'")
            spot = self.page.evaluate('window.castTest.spot()')
            self.assertEqual(spot['key'], scene)
            self.assertTrue(70 <= spot['x'] <= 1210 and 200 <= spot['y'] <= 750, spot)


    def test_07_player_picks_what_they_are_and_it_sticks(self):
        self.assertEqual(self.page.evaluate('window.castTest.player().kind'), 'raccoon', 'Existing players stay raccoons')
        self.page.locator('#title-who').click()
        self.page.wait_for_selector('#pp-view')
        self.page.locator('[data-kind="alien"]').click()
        self.page.locator('[data-cycle="eyes"]').click()
        self.page.locator('#pp-random').click()
        self.page.locator('[data-kind="fae"]').click()
        self.page.locator('#pp-done').click()
        self.assertEqual(self.page.evaluate('window.castTest.player().kind'), 'fae')
        self.page.reload()
        self.assertEqual(self.page.evaluate('window.castTest.player().kind'), 'fae', 'The choice is saved')
        self.page.locator('#title-who').click()
        self.page.locator('[data-kind="raccoon"]').click()
        self.page.locator('#pp-done').click()
        self.assertEqual(self.page.evaluate('window.castTest.player().kind'), 'raccoon')

    def test_10_standing_characters_are_cached_and_cheap(self):
        ms = self.page.evaluate("""(()=>{const c=document.createElement('canvas').getContext('2d');c.canvas.width=1280;c.canvas.height=800;const d=window.castTest.drawPerson;
          for(let i=0;i<30;i++)d(c,40+i*40,400,{cast:'b'+i},0,'down',false,1.2);
          const t0=performance.now();for(let f=0;f<100;f++)for(let i=0;i<30;i++)d(c,40+i*40,400,{cast:'b'+i},0,'down',false,1.2);
          const m=c.getTransform();if(m.a!==1||m.e!==0)return -1;return (performance.now()-t0)/100;})()""")
        self.assertGreaterEqual(ms, 0, 'Canvas state leaked')
        self.assertLess(ms, 4, f'30 standing characters took {ms:.2f} ms a frame')

    def welcome(self):
        return self.page.evaluate('deloresWelcomeTest()')

    def test_08_pronouns_are_optional_plural_or_your_own(self):
        self.assertIn('Look after them. Their coat', self.welcome(), 'No choice means they')
        self.page.locator('#title-who').click()
        self.page.locator('[data-pro="she"]').click()
        self.page.locator('[data-pro="they"]').click()
        self.page.locator('#pp-done').click()
        self.assertIn(self.page.locator('#toast').inner_text().split('“')[1][:16], ['Look after her. ', 'Look after them.'])
        self.assertEqual(self.page.evaluate("JSON.parse(localStorage.getItem('mapachez_player_v1')).pronouns"), ['she', 'they'])
        self.page.locator('#title-who').click()
        self.page.locator('[data-pro="she"]').click()
        self.page.locator('[data-pro="they"]').click()
        self.page.locator('#pp-own').fill('xe/xem/xyr')
        self.page.locator('#pp-done').click()
        self.assertIn('Look after xem. Xyr coat', self.welcome())
        others = self.page.evaluate("Object.keys(localStorage).filter(k=>k!=='mapachez_player_v1').map(k=>localStorage.getItem(k)).join(' ')")
        self.assertNotIn('xem', others, 'Pronouns stay in the player save only')

    def test_09_spanish_is_neutral_by_default(self):
        self.page.evaluate("profileTestLang('es')")
        self.assertIn('Cuida de esta persona.', self.welcome())
        self.page.locator('#title-who').click()
        self.assertIn('¿Quién eres esta noche?', self.page.locator('#modal-heading').inner_text())
        self.page.locator('[data-pro="they"]').click()
        self.page.locator('#pp-done').click()
        self.assertIn('Cuida de elle.', self.welcome())


if __name__ == '__main__':
    unittest.main(verbosity=2)
