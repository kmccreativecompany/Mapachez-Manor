"""Browser checks for GHOSTS v1 (friendly ghost guests treated as perfectly normal), gifts that come
from thankful guests rather than the manager, and the dress code (gift outfits are worn at home only).

Run: python tests/test_ghosts.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import json
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'ghostTest',{get:()=>({
 ghosts:structuredClone(ghosts),joy:structuredClone(joy),pins:Object.keys(growth.pins),text:GHOST_TEXT,
 chats:CHAT.list.map(c=>c.id),closetIntro:JT.closetIntro,extras:world.options.extras().map(e=>e.id),
 enterPlay:()=>{state.flags.briefed=true;state.phase='playing';return world.options.extras().map(e=>e.id);},
 open:()=>openTanakas(),close:()=>closeModal(),
 give:(r)=>{joy.gifts.push(r);storeJoy();},openGift:()=>openGift(),
 sender:(r)=>giftSender(r),
 emiko:()=>{const r=castLook('Mrs. Emiko Tanaka');return {ghost:!!r.ghost,skin:r.skin};},
 hiroshi:()=>!!castLook('Mr. Hiroshi Tanaka').ghost,
 alpha:()=>{const r=castLook('Mrs. Emiko Tanaka'),o=pxSprite(r,'down',false,0),g=o.getContext('2d').getImageData(0,0,o.width,o.height).data;
   let top=0,feet=0;for(let y=0;y<o.height;y++)for(let x=0;x<o.width;x++){const a=g[(y*o.width+x)*4+3];if(y<20)top=Math.max(top,a);if(y>=o.height-3)feet=Math.max(feet,a);}return [top,feet];},
 newDay:()=>{ghosts.day='2000-01-01';storeGhosts();},
 hatAtWork:()=>{joy.owned=['crown'];joy.wearing='crown';const c=document.createElement('canvas');c.width=120;c.height=120;const g=c.getContext('2d');
   const r=joyPlayerRecipe();const px=()=>{let n=0;const d=g.getImageData(0,0,120,120).data;for(let i=3;i<d.length;i+=4)if(d[i])n++;return n;};
   g.clearRect(0,0,120,120);drawBeing(g,60,80,r,0,'down',false,1.5);const work=px();
   g.clearRect(0,0,120,120);joyOffClock=true;try{drawBeing(g,60,80,r,0,'down',false,1.5);}finally{joyOffClock=false;}const home=px();
   joy.wearing='';joy.owned=[];return [work,home];}
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class Ghosts(base.Growth):
    """Reuses the growth harness but none of its tests."""

    def g(self):
        return self.page.evaluate('window.ghostTest')

    def test_01_emiko_is_a_soft_floating_ghost_and_hiroshi_is_not(self):
        self.assertTrue(self.page.evaluate('ghostTest.emiko()')['ghost'])
        self.assertFalse(self.page.evaluate('ghostTest.hiroshi()'))
        top, feet = self.page.evaluate('ghostTest.alpha()')
        self.assertLess(top, 255, 'A little see-through')
        self.assertGreater(top, 150, 'Still easy to see')
        self.assertLess(feet, 40, 'Feet fade into a wisp')

    def test_02_tanakas_on_the_corridor_with_a_daily_service_moment(self):
        self.page.locator('#begin').click()
        self.page.wait_for_function('document.getElementById("game-shell").hidden===false')
        self.page.evaluate('ghostTest.close()')
        self.assertIn('tanakas', self.page.evaluate('ghostTest.enterPlay()'))
        self.page.evaluate('ghostTest.open()')
        body = self.page.locator('#modal-body').inner_text()
        self.assertIn('Emiko is a ghost', body)
        self.assertIn('nobody finds this unusual', body)
        tips = self.g()['joy']['tips']
        self.page.locator('#modal-body .choice', has_text='Bring two warm cups').click()
        self.assertIn('Best answer', self.page.locator('#ghost-res').inner_text())
        st = self.g()
        self.assertEqual(st['joy']['tips'], tips + 3)
        self.assertEqual(st['ghosts']['done'], ['cups'])
        # One moment a day: the next visit is just a friendly hello.
        self.page.evaluate('ghostTest.close()')
        self.page.evaluate('ghostTest.open()')
        self.assertEqual(self.page.locator('#modal-body .choice').count(), 0)
        self.assertNotIn('Emiko is a ghost', self.page.locator('#modal-body').inner_text(), 'The intro is only for the first hello')
        for n in range(3):
            self.page.evaluate('ghostTest.newDay()')
            self.page.evaluate('ghostTest.close()')
            self.page.evaluate('ghostTest.open()')
            self.page.locator('#modal-body .choice').first.click()
        self.assertEqual(len(self.g()['ghosts']['done']), 4)
        self.assertIn('party-of-two', self.g()['pins'])

    def test_03_two_ghost_chats_in_the_lobby_and_matching_spanish(self):
        self.assertTrue({'tanaka-photos', 'walls'} <= set(self.g()['chats']))
        text = self.g()['text']
        en, es = text['en'], text['es']
        self.assertEqual([m['id'] for m in en['moments']], [m['id'] for m in es['moments']])
        self.assertEqual(len(en['banter']), len(es['banter']))
        for a, b in zip(en['chats'], es['chats']):
            self.assertEqual([l[0] for l in a['lines']], [l[0] for l in b['lines']])
        words = json.dumps(text).lower()
        for word in ('scary', 'spooky ghost', 'haunt', 'dead', 'died', 'death', 'widow', 'grave', 'funeral', 'muert', 'viud'):
            self.assertNotIn(word, words, 'Sweet and normal, never sad or scary')

    def test_04_gifts_come_from_thankful_guests_never_the_manager(self):
        self.page.evaluate('ghostTest.close()')
        for reason in ('shift', 'jar', 'hms', 'perfect'):
            for _ in range(20):
                self.assertNotIn('Delores', self.page.evaluate(f'ghostTest.sender("{reason}")')['name'])
        self.page.evaluate('ghostTest.give("jar")')
        self.page.evaluate('ghostTest.openGift()')
        self.assertIn('A GIFT FROM A GUEST', self.page.locator('#modal-body').inner_text().upper())
        self.assertIn('From ', self.page.locator('.joy-from').inner_text())
        for _ in range(3):
            self.page.locator('.joy-gift').click()
        self.page.wait_for_selector('.joy-giftstage.opened')
        self.assertIn('— ', self.page.locator('.joy-tag').inner_text())
        html = self.page.evaluate('document.documentElement.outerHTML')
        self.assertNotIn('Delores left you a gift', html)
        self.assertNotIn('housewarming pie', html)

    def test_05_dress_code_uniform_at_work_outfits_at_home(self):
        work, home = self.page.evaluate('ghostTest.hatAtWork()')
        self.assertGreater(home, work, 'The crown only shows off the clock')
        self.assertIn('uniform', self.g()['closetIntro'])


for _name in dir(base.Growth):
    if _name.startswith('test_') and _name not in Ghosts.__dict__:
        setattr(Ghosts, _name, None)


if __name__ == '__main__':
    unittest.main()
