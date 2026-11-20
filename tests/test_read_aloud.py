"""Browser checks for READ ALOUD v1: select any text and tap "Read this" to hear it, tap "Stop" to stop.

Run: python tests/test_read_aloud.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py. The browser voice is replaced
with a recorder so the checks are silent and do not depend on which voices the machine has.
"""
import unittest

import test_growth as base

FAKE_VOICE = """
(()=>{const spoken=[];let queue=[];
class FakeUtterance{constructor(text){this.text=text;this.lang='';this.voice=null;this.rate=1;this.onend=null;this.onerror=null;}}
const synth={speak(u){spoken.push(u.text);queue.push(u);},cancel(){queue=[];},getVoices(){return [];},addEventListener(){},
  get speaking(){return queue.length>0;}};
Object.defineProperty(window,'speechSynthesis',{configurable:true,get:()=>synth});
window.SpeechSynthesisUtterance=FakeUtterance;
window.readTest={spoken,finish(){const q=queue;queue=[];q.forEach(u=>u.onend&&u.onend());},clear(){spoken.length=0;}};})();
"""
NO_VOICE = "delete Window.prototype.speechSynthesis;delete window.speechSynthesis;delete window.SpeechSynthesisUtterance;"
SELECT = """sel => { const el = document.querySelector(sel); const r = document.createRange(); r.selectNodeContents(el);
  const s = getSelection(); s.removeAllRanges(); s.addRange(r); return String(s).trim(); }"""


class ReadAloud(base.Growth):
    voice = FAKE_VOICE

    def setUp(self, viewport=None):
        self.context = self.browser.new_context(viewport=viewport or {'width': 1440, 'height': 1000}, reduced_motion='reduce')
        self.context.add_init_script("try{if(!localStorage.getItem('mapachez_profile_v1'))localStorage.setItem('mapachez_profile_v1',JSON.stringify({version:1,mode:'solo',lang:'en',hooked:true}))}catch(e){}")
        self.context.add_init_script(self.voice)
        # The whole manor is open here; night-by-night unlocks are covered in test_nights.py.
        self.context.add_init_script("try{if(!localStorage.getItem('mapachez_nights_v1'))localStorage.setItem('mapachez_nights_v1',JSON.stringify({all:true,seen:10,fresh:[]}))}catch(e){}")
        self.page = self.context.new_page()
        self.errors, self.requests = [], []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        self.page.route('**/*', self.route)
        self.page.goto(self.url)

    def pill(self):
        return self.page.locator('#read-pill')

    def select(self, selector):
        text = self.page.evaluate(SELECT, selector)
        self.page.wait_for_timeout(400)
        return text

    def spoken(self):
        return ' '.join(self.page.evaluate('readTest.spoken'))

    def test_read_01_select_text_then_tap_read_this(self):
        self.assertFalse(self.pill().is_visible(), 'Nothing shows until words are selected')
        text = self.select('#title-screen p, .title-screen p, p')
        self.assertTrue(text)
        self.assertTrue(self.pill().is_visible())
        self.assertIn('Read this', self.pill().inner_text())
        self.pill().click()
        self.assertEqual(self.spoken().split(), text.split())
        self.assertIn('Stop', self.pill().inner_text(), 'While talking the bubble becomes a stop button')

    def test_read_02_stop_is_one_tap_and_finishing_resets(self):
        self.select('p')
        self.pill().click()
        self.pill().click()
        self.assertIn('Read this', self.pill().inner_text())
        self.pill().click()
        self.page.evaluate('readTest.finish()')
        self.assertIn('Read this', self.pill().inner_text(), 'When the voice finishes the stop button goes away')

    def test_read_03_works_inside_a_dialog_and_the_dialog_button_stops(self):
        self.page.locator('#title-quick').click()
        self.page.wait_for_selector('#modal-body .choice')
        self.select('#modal-body .choice')
        self.assertTrue(self.page.evaluate("document.getElementById('read-pill').parentNode.id==='modal'"),
                        'The bubble lives inside the open dialog so it can be tapped')
        self.pill().click()
        self.assertTrue(self.spoken())
        self.page.evaluate('readTest.finish()')
        self.page.evaluate('readTest.clear()')
        self.page.evaluate('getSelection().removeAllRanges()')
        narrate = self.page.locator('#narrate')
        narrate.click()
        self.assertTrue(self.spoken(), 'The dialog speaker button reads the whole card')
        self.assertIn('Stop reading', narrate.inner_text())
        narrate.click()
        self.assertIn('Read this aloud', narrate.inner_text())

    def test_read_04_long_text_is_split_into_short_pieces(self):
        self.page.evaluate("""() => { const p = document.createElement('p'); p.id = 'long-read';
          p.textContent = 'The lily moved again tonight. '.repeat(40); document.body.prepend(p); }""")
        self.select('#long-read')
        self.pill().click()
        pieces = self.page.evaluate('readTest.spoken')
        self.assertGreater(len(pieces), 3)
        self.assertTrue(all(len(p) <= 220 for p in pieces), 'Phones cut off long speech, so pieces stay short')

    def test_read_05_switch_off_in_settings_and_it_is_remembered(self):
        self.page.locator('#title-settings').click()
        switch = self.page.locator('[data-read-setting] input')
        self.assertTrue(switch.is_checked())
        switch.uncheck()
        self.page.keyboard.press('Escape')
        self.page.reload()
        self.select('p')
        self.assertFalse(self.pill().is_visible())
        self.page.locator('#title-settings').click()
        self.assertFalse(self.page.locator('[data-read-setting] input').is_checked())

    def test_read_06_closing_a_dialog_stops_talking(self):
        self.page.locator('#title-quick').click()
        self.page.wait_for_selector('#modal-body .choice')
        self.page.locator('#narrate').click()
        self.page.keyboard.press('Escape')
        self.page.wait_for_timeout(250)
        self.assertFalse(self.page.evaluate('readTest.spoken.length && speechSynthesis.speaking'))
        self.assertFalse(self.pill().is_visible())


class ReadAloudPhone(ReadAloud):
    def setUp(self, viewport=None):
        super().setUp(viewport=viewport or {'width': 390, 'height': 844})

    def test_read_07_bubble_sits_on_screen_and_is_big_enough_to_tap(self):
        self.select('p')
        box = self.pill().bounding_box()
        self.assertGreaterEqual(box['height'], 44)
        self.assertGreaterEqual(box['x'], 0)
        self.assertLessEqual(box['x'] + box['width'], 390)
        self.assertLessEqual(box['y'] + box['height'], 844)


class NoVoice(ReadAloud):
    voice = NO_VOICE

    def test_read_01_select_text_then_tap_read_this(self):
        self.select('p')
        self.assertEqual(self.pill().count(), 0, 'Browsers without a voice never see the bubble')

    test_read_02_stop_is_one_tap_and_finishing_resets = None
    test_read_03_works_inside_a_dialog_and_the_dialog_button_stops = None
    test_read_04_long_text_is_split_into_short_pieces = None
    test_read_06_closing_a_dialog_stops_talking = None

    def test_read_05_switch_off_in_settings_and_it_is_remembered(self):
        self.page.locator('#title-settings').click()
        self.assertTrue(self.page.locator('[data-read-setting] input').is_disabled())


if __name__ == '__main__':
    unittest.main()
