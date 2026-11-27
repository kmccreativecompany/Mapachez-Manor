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


GHOST_CHATS = ['tanaka-photos', 'walls']  # added after the lobby chats by the ghost update


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
        # 18 lobby chats (the 'fourth husband' chat was taken out 2026-11-27: grief about husbands can be triggering), then the 2 ghost chats the ghost update adds after them.
        self.assertEqual(len([c for c in en if c['id'] not in GHOST_CHATS]), 18)
        self.assertEqual([c['id'] for c in en if c['id'] in GHOST_CHATS], GHOST_CHATS)
        self.assertEqual([c['id'] for c in en], [c['id'] for c in es])
        for a, b in zip(en, es):
            self.assertEqual([l[0] for l in a['lines']], [l[0] for l in b['lines']], a['id'])
            self.assertGreaterEqual(len(a['lines']), 6, 'A teaser of three, then the rest')
            self.assertTrue(a['end'] and b['end'])
            for chat in (a, b):
                for _, line in chat['lines']:
                    self.assertLessEqual(len(line), 70, 'Lines stay short for phones: ' + line)
        words = json.dumps(text)
        for line in text['en']['byes'] + text['es']['byes']:
            self.assertLessEqual(len(line), 80, 'Goodbyes fit in a toast: ' + line)
        self.assertEqual(len(text['en']['byes']), len(text['es']['byes']))
        for word in ('opossum', 'zarigüeya', 'INFP', '4w5', 'vampire', 'alien', 'monster', 'Room 13'):
            self.assertNotIn(word, words, 'Traits are shown, never named')

    def test_04_all_six_ai_jokes_are_localized_and_butler_thoughts_appear(self):
        text = self.c()['text']
        expected = {'robot-terms', 'beta-romance', 'counselor-conspiracy',
                    'romance-update', 'subscription-marriage', 'wifi-ex'}
        for language in ('en', 'es'):
            entries = [c for c in text[language]['list'] if c['id'] in expected]
            self.assertEqual({c['id'] for c in entries}, expected)
            self.assertTrue(all(c.get('thought') for c in entries))
        language = self.lang
        index = next(i for i, c in enumerate(text[language]['list']) if c['id'] == 'robot-terms')
        self.page.evaluate("""index => localStorage.setItem('mapachez_chats_v1',
            JSON.stringify({version:1,next:index,heard:[],bye:0}))""", index)
        self.page.reload()
        self.enter_manor()
        self.page.evaluate('window.chatTest.listen()')
        self.choose('Seguir escuchando' if language == 'es' else 'Keep listening')
        thought = self.page.locator('.chat-thought').inner_text()
        self.assertIn('mayordomo' if language == 'es' else 'Butler thought', thought)

    def test_05_replacement_jokes_have_clear_punchlines_and_preserve_the_story(self):
        text = self.c()['text']
        original = {'email','bells','toast','time','sunday','muffin',
                    'inbox','blankets','circle','tuesday','photo','duchess'}
        for lang in ('en','es'):
            chats = text[lang]['list']
            self.assertEqual(chats[0]['id'], 'blankets')
            lobby = [c for c in chats if c['id'] not in GHOST_CHATS]
            self.assertEqual(lobby[-1]['id'], 'letter', 'The letter clue closes the lobby chats')
            self.assertTrue(lobby[-1].get('memory'))
            self.assertEqual([c['id'] for c in chats[-len(GHOST_CHATS):]], GHOST_CHATS)
            for chat in chats:
                if chat['id'] in original:
                    self.assertTrue(chat.get('thought'), chat['id'])
        english = {x['id']:x for x in text['en']['list']}
        self.assertIn('Margaret needs to know', english['bells']['lines'][-1][1])
        self.assertIn('DNA test', english['email']['lines'][-1][1])
        self.assertIn('seven videos', english['inbox']['lines'][-1][1])

        # The original memory-book mystery remains functional despite its new position.
        story_index = next(i for i, c in enumerate(text[self.lang]['list']) if c['id'] == 'letter')
        self.page.evaluate("""index => localStorage.setItem('mapachez_chats_v1',
            JSON.stringify({version:1,next:index,heard:[],bye:0}))""", story_index)
        self.page.reload()
        self.enter_manor()
        self.page.evaluate('window.chatTest.listen()')
        self.choose('Seguir escuchando' if self.lang == 'es' else 'Keep listening')
        self.assertTrue(self.c()['fern'], 'Story clue should still unlock its memory')
        self.assertIn('letter', self.c()['chats']['heard'])

    def test_02_hearing_a_chat_fades_the_bubble_and_sends_the_pair_off(self):
        self.enter_manor()
        self.assertIn('lobby-conversation', self.c()['extras'])
        self.page.evaluate('window.chatTest.listen()')
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), 'The secret to a peaceful marriage')
        self.assertEqual(self.page.locator('.chat-lines li').count(), 3)
        self.choose('Keep listening')
        body = self.page.locator('#modal-body').inner_text()
        self.assertIn('very comfortable sofa', body)
        self.assertIn('Butler thought', body)
        self.assertFalse(self.c()['fern'], 'Ordinary jokes should not mark the mystery heard')
        self.assertIn('listening-ear', self.c()['pins'])
        self.choose('Return to your evening')
        self.page.wait_for_function('window.chatTest.phase !== "here"')
        self.assertNotIn('lobby-conversation', self.c()['extras'], 'Nobody to listen to while the chairs are empty')
        toast = self.page.locator('#toast').inner_text()
        self.assertIn(f'Overheard: 1 of {len(self.c()["text"]["en"]["list"])}', toast)
        self.assertIn('Mrs. Calder, getting up: “Sorry, I have a video meeting that really could have been an email.”', toast)
        saved = json.loads(self.page.evaluate("localStorage.getItem('mapachez_chats_v1')"))
        self.assertEqual((saved['next'], saved['heard'], saved['bye']), (1, ['blankets'], 1))
        self.page.wait_for_function('document.getElementById("lobby-chatter").hidden')
        # A new pair settles in after the chairs have been empty a while.
        self.page.evaluate('window.chatTest.skip(40000)')
        self.page.wait_for_function('window.chatTest.phase === "here"', timeout=8000)
        self.page.evaluate('window.chatTest.listen()')
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), "We're like a family")

    def test_03_every_pair_takes_a_turn_and_earns_all_ears(self):
        self.enter_manor()
        total = len(self.c()['text']['en']['list'])
        for n in range(total):
            self.page.evaluate('window.chatTest.listen()')
            self.choose('Keep listening')
            self.choose('Return to your evening')
            self.page.wait_for_function('window.chatTest.phase !== "here"')
            self.page.evaluate('window.chatTest.skip(40000)')
            self.page.wait_for_function('window.chatTest.phase === "here"', timeout=8000)
        c = self.c()
        self.assertEqual(len(c['chats']['heard']), total)
        self.assertEqual(c['chats']['bye'], total, 'Every pair says a tired little goodbye')
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
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), 'El secreto de un matrimonio feliz')
        self.choose('Seguir escuchando')
        self.assertIn('sofá muy cómodo', self.page.locator('#modal-body').inner_text())
        self.choose('Volver a tu noche')
        self.page.wait_for_function('window.chatTest.phase !== "here"')
        self.assertIn(f'Escuchadas: 1 de {len(self.c()["text"]["es"]["list"])}', self.page.locator('#toast').inner_text())
        self.assertIn('podría haber sido un correo', self.page.locator('#toast').inner_text())


if __name__ == '__main__':
    unittest.main()
