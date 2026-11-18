"""Browser checks for the guest-to-guest chats by the lobby chairs (CHATS v1): the scripts,
hearing a chat, the bubble fading, the pair walking off, a new pair arriving, and Spanish.

Run: python tests/test_chats.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import json
import re
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'chatTest',{get:()=>({
 text:CHATS_TEXT,chats:structuredClone(chats),phase:chatMove.phase,
 extras:world.options.extras().map(e=>e.id),fern:!!state?.sideStories?.fern,
 listen:()=>interact(LOBBY_SCENE.id),close:()=>closeModal(),
 skip:ms=>{const o=performance.now.bind(performance);performance.now=()=>o()+ms;},
 pins:growth.pins
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class Chats(base.Growth):
    lang = 'en'

    def setUp(self):
        super().setUp()
        if self.lang != 'en':
            self.page.evaluate("l=>localStorage.setItem('mapachez_profile_v1',JSON.stringify({version:1,mode:'solo',lang:l,hooked:true}))", self.lang)
            self.page.reload()

    def c(self):
        return self.page.evaluate('window.chatTest')

    def enter_manor(self):
        self.page.locator('#begin').click()
        self.page.wait_for_function('window.chatTest && document.getElementById("game-shell").hidden===false')
        self.page.evaluate('window.chatTest.close()')

    def choose(self, text):
        self.page.locator('#modal-body .choice').filter(has_text=text).click()

    def test_01_scripts_are_short_kind_and_match_in_both_languages(self):
        text = self.c()['text']
        en, es = text['en']['list'], text['es']['list']
        self.assertGreaterEqual(len(en), 7)
        self.assertEqual([c['id'] for c in en], [c['id'] for c in es])
        for a, b in zip(en, es):
            self.assertEqual([l[0] for l in a['lines']], [l[0] for l in b['lines']], a['id'])
            self.assertGreaterEqual(len(a['lines']), 6, 'A teaser of three, then the rest')
            self.assertTrue(a['end'] and b['end'])
            for chat in (a, b):
                for _, line in chat['lines']:
                    self.assertLessEqual(len(line), 70, 'Lines stay short for phones: ' + line)
        words = json.dumps(text)
        for word in ('opossum', 'zarigüeya', 'INFP', '4w5', 'vampire', 'alien', 'monster', 'Room 13'):
            self.assertNotIn(word, words, 'Traits are shown, never named')

    def test_02_hearing_a_chat_fades_the_bubble_and_sends_the_pair_off(self):
        self.enter_manor()
        self.assertIn('lobby-conversation', self.c()['extras'])
        self.page.evaluate('window.chatTest.listen()')
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), 'A letter sealed in gold')
        self.assertEqual(self.page.locator('.chat-lines li').count(), 3)
        self.choose('Keep listening')
        body = self.page.locator('#modal-body').inner_text()
        self.assertIn('The same one, twice.', body)
        self.assertIn('the same note', body)
        self.assertTrue(self.c()['fern'], 'The letter chat still fills the Memory Book page')
        self.assertIn('listening-ear', self.c()['pins'])
        self.choose('Return to your evening')
        self.page.wait_for_function('window.chatTest.phase !== "here"')
        self.assertNotIn('lobby-conversation', self.c()['extras'], 'Nobody to listen to while the chairs are empty')
        self.assertIn('Overheard: 1 of 7', self.page.locator('#toast').inner_text())
        saved = json.loads(self.page.evaluate("localStorage.getItem('mapachez_chats_v1')"))
        self.assertEqual((saved['next'], saved['heard']), (1, ['letter']))
        self.page.wait_for_function('document.getElementById("lobby-chatter").hidden')
        # A new pair settles in after the chairs have been empty a while.
        self.page.evaluate('window.chatTest.skip(40000)')
        self.page.wait_for_function('window.chatTest.phase === "here"', timeout=8000)
        self.page.evaluate('window.chatTest.listen()')
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), 'One note, many spoons')

    def test_03_every_pair_takes_a_turn_and_earns_all_ears(self):
        self.enter_manor()
        for n in range(7):
            self.page.evaluate('window.chatTest.listen()')
            self.choose('Keep listening')
            self.choose('Return to your evening')
            self.page.wait_for_function('window.chatTest.phase !== "here"')
            self.page.evaluate('window.chatTest.skip(40000)')
            self.page.wait_for_function('window.chatTest.phase === "here"', timeout=8000)
        c = self.c()
        self.assertEqual(len(c['chats']['heard']), 7)
        self.assertEqual(c['chats']['next'], 0, 'The chairs start over with the first pair')
        self.assertIn('all-ears', c['pins'])


for _name in dir(base.Growth):
    if _name.startswith('test_') and _name not in Chats.__dict__:
        setattr(Chats, _name, None)  # reuse the growth harness, none of its tests


class ChatsSpanish(Chats):
    lang = 'es'

    def test_01_scripts_are_short_kind_and_match_in_both_languages(self):
        pass

    def test_03_every_pair_takes_a_turn_and_earns_all_ears(self):
        pass

    def test_02_hearing_a_chat_fades_the_bubble_and_sends_the_pair_off(self):
        self.enter_manor()
        self.page.evaluate('window.chatTest.listen()')
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), 'Una carta con sello dorado')
        self.choose('Seguir escuchando')
        self.assertIn('La misma, dos veces.', self.page.locator('#modal-body').inner_text())
        self.choose('Volver a tu noche')
        self.page.wait_for_function('window.chatTest.phase !== "here"')
        self.assertIn('Escuchadas: 1 de 7', self.page.locator('#toast').inner_text())


if __name__ == '__main__':
    unittest.main()
