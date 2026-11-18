"""Browser checks for EXTRA CUTE v1: raccoons swish, twitch, hop, and light up near a friend.

Run: python tests/test_cute.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import re
import unittest

import test_growth as base

CUTE = """
Object.defineProperty(window,'cuteTest',{get:()=>({
  moods:()=>{const r=castLook('delores');const out=new Set();for(let t=1;t<20000;t+=37)out.add(racMood(r,t,0).mood);return [...out];},
  happyNearDesk:()=>{state.player.x=330;state.player.y=560;return new Promise(ok=>setTimeout(()=>ok(racMood(castLook('delores'),performance.now(),0).happy),300));},
  calmAway:()=>{state.player.x=1000;state.player.y=650;return new Promise(ok=>setTimeout(()=>ok(racMood(castLook('delores'),performance.now(),0).happy),600));},
  differs:()=>{const r=castLook('delores'),a=pxPaint(r,'down',false,0,''),b=pxPaint(r,'down',false,0,'hRt');return a.some((c,i)=>c!==b[i]);}
})});
"""
base.TEST_HTML = base.HTML.replace('\n})();\n</script>', '\n' + base.INSPECTOR + CUTE + '\n})();\n</script>')


class Cute(base.Growth):
    def begin(self):
        self.page.locator('#begin').click()
        self.page.wait_for_timeout(500)
        for _ in range(3):
            self.page.keyboard.press('Escape')
            self.page.wait_for_timeout(150)

    def test_cute_01_happy_face_tail_and_ear_are_real_sprite_changes(self):
        self.assertTrue(self.page.evaluate('cuteTest.differs()'))

    def test_cute_02_idle_raccoons_swish_and_twitch(self):
        moods = ''.join(self.page.evaluate('cuteTest.moods()'))
        for m in 'LRt':
            self.assertIn(m, moods)

    def test_cute_03_delores_lights_up_only_when_you_visit(self):
        self.begin()
        self.assertTrue(self.page.evaluate('cuteTest.happyNearDesk()'))
        self.assertFalse(self.page.evaluate('cuteTest.calmAway()'))

    def test_cute_04_still_code_only(self):
        block = base.HTML[base.HTML.index('/* EXTRA CUTE v1'):base.HTML.index('function racHearts')]
        self.assertNotIn('data:image', block)


if __name__ == '__main__':
    unittest.main()
