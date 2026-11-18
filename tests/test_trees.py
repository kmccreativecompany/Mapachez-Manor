"""Browser checks for the talking trees in the Festival Garden (TALKING TREES v1): they live outdoors
only, speak when you walk close or tap them, remember what you have heard, earn two pins, draw in
every season and weather without leaking canvas state, and speak Spanish.

Run: python tests/test_trees.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import json
import unittest

import test_growth as base

INSPECTOR = """
Object.defineProperty(window,'treeTest',{get:()=>({
 text:TREE_TEXT,talk:structuredClone(treeTalk),festival:festivalActive,force:treeForce,
 points:world.options.extras().map(e=>e.id),pins:structuredClone(growth.pins),
 trees:TALKING_TREES.map(t=>({id:t.id,x:t.x,y:t.y})),
 interact:id=>interact(id),walkTo:(x,y)=>{state.player.x=x;state.player.y=y;},
 drawAll:()=>{const c=document.createElement('canvas').getContext('2d');let bad='';
   for(const season of ['spring','summer','autumn','winter'])for(const w of ['','rain','storm','snow','fireflies','petals','leaves'])for(const calm of [false,true]){
     for(const t of TALKING_TREES){t.said=calm?-1e9:performance.now()-300;drawTalkingTree(c,t,performance.now(),calm,season,w,state.player);}
     const m=c.getTransform();if(m.a!==1||m.e!==0||m.f!==0||c.globalAlpha!==1)bad=season+'/'+w;}
   return bad||'ok';},
 close:()=>closeModal()
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class Trees(base.Growth):
    """Reuses the growth harness but none of its tests."""

    def t(self):
        return self.page.evaluate('window.treeTest')

    def enter_festival(self):
        self.page.locator('#explore-festival').click()
        self.page.wait_for_function('window.treeTest.festival')
        self.page.evaluate('window.treeTest.close()')

    def test_01_trees_live_outdoors_only(self):
        self.page.locator('#begin').click()
        self.page.wait_for_function('document.getElementById("game-shell").hidden===false')
        self.page.evaluate('window.treeTest.close()')
        self.assertFalse([p for p in self.t()['points'] if p.startswith('tree-')], 'No talking trees inside the manor')

    def test_02_walking_close_makes_a_tree_speak_once(self):
        self.enter_festival()
        self.assertEqual({p for p in self.t()['points'] if p.startswith('tree-')}, {'tree-oak', 'tree-willow', 'tree-pip'})
        self.page.evaluate("window.treeTest.force.weather='clear'")
        oak = next(t for t in self.t()['trees'] if t['id'] == 'oak')
        self.page.evaluate(f"window.treeTest.walkTo({oak['x'] - 30},{oak['y'] + 20})")
        self.page.wait_for_function("document.getElementById('toast').innerText.includes('Old Oakley')")
        first = self.t()['text']['en']['lines']['oak'][0]
        self.assertIn(first, self.page.locator('#toast').inner_text())
        self.assertIn('Tree talk heard: 1 of 30', self.page.locator('#toast').inner_text())
        self.page.wait_for_timeout(400)
        self.assertEqual(self.t()['talk']['heard']['oak'], [0], 'Standing still does not repeat')

    def test_03_tapping_tells_the_next_thing_and_it_is_remembered(self):
        self.enter_festival()
        self.page.evaluate("window.treeTest.force.weather='clear'")
        for n in range(3):
            self.page.evaluate("window.treeTest.interact('tree-pip')")
            self.page.wait_for_timeout(2600)
        self.assertEqual(self.t()['talk']['heard']['pip'], [0, 1, 2])
        saved = json.loads(self.page.evaluate("localStorage.getItem('mapachez_trees_v1')"))
        self.assertEqual(saved['heard']['pip'], [0, 1, 2])
        self.page.reload()
        self.assertEqual(self.t()['talk']['heard']['pip'], [0, 1, 2])

    def test_04_pins_for_listening(self):
        self.enter_festival()
        self.page.evaluate("window.treeTest.force.weather='clear'")
        for tree in ('oak', 'willow', 'pip'):
            self.page.evaluate(f"window.treeTest.interact('tree-{tree}')")
        self.assertIn('tree-friend', self.t()['pins'])
        self.page.evaluate("""localStorage.setItem('mapachez_trees_v1',JSON.stringify({version:1,heard:{
          oak:[...Array(10).keys()],willow:[...Array(10).keys()],pip:[...Array(9).keys()]}}))""")
        self.page.reload()
        self.enter_festival()
        self.page.evaluate("window.treeTest.force.weather='clear'")
        self.page.evaluate("window.treeTest.interact('tree-pip')")
        self.assertIn('tree-whisperer', self.t()['pins'])

    def test_05_every_season_and_weather_draws_cleanly(self):
        self.enter_festival()
        self.assertEqual(self.page.evaluate('window.treeTest.drawAll()'), 'ok')

    def test_06_words_are_kind_spanish_matches_and_no_room_numbers(self):
        text = self.t()['text']
        for lang in ('en', 'es'):
            for tree in ('oak', 'willow', 'pip'):
                self.assertEqual(len(text[lang]['lines'][tree]), 10)
            self.assertEqual(set(text[lang]['weather']), set(text['en']['weather']))
            for w in text['en']['weather']:
                self.assertEqual(len(text[lang]['weather'][w]), len(text['en']['weather'][w]))
        words = json.dumps(text, ensure_ascii=False)
        for word in ('INFP', '4w5', 'personality', 'opossum', 'zarigüeya', 'stupid', 'dumb'):
            self.assertNotIn(word, words)
        import re
        self.assertFalse(re.search(r'\b(?!20[1-6]\b)\d{3}\b', words), 'No room numbers outside 201 to 206')


class TreesSpanish(Trees):
    def setUp(self, viewport=None):
        super().setUp(viewport)
        self.page.evaluate("localStorage.setItem('mapachez_profile_v1',JSON.stringify({version:1,mode:'solo',lang:'es',hooked:true}))")
        self.page.reload()

    def test_02_walking_close_makes_a_tree_speak_once(self):
        self.enter_festival()
        self.page.evaluate("window.treeTest.force.weather='clear'")
        self.page.evaluate("window.treeTest.interact('tree-willow')")
        toast = self.page.locator('#toast').inner_text()
        self.assertIn('Willa, el sauce', toast)
        self.assertIn(self.t()['text']['es']['lines']['willow'][0], toast)
        self.assertIn('Charlas de árbol escuchadas: 1 de 30', toast)

    test_01_trees_live_outdoors_only = None
    test_03_tapping_tells_the_next_thing_and_it_is_remembered = None
    test_04_pins_for_listening = None
    test_05_every_season_and_weather_draws_cleanly = None
    test_06_words_are_kind_spanish_matches_and_no_room_numbers = None


for name in [n for n in dir(base.Growth) if n.startswith('test_')]:
    setattr(Trees, name, None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
