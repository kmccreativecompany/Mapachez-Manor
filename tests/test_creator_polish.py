"""Browser checks for the creator polish: faces stay visible, eyes vs mouth, true side view,
clearer fur/feathers/scales, robot hair, Spanish hair words and keeping the look on close.

Run: python tests/test_creator_polish.py
Requires Playwright and Chromium; uses the isolated no-network test_cast harness.
"""
import unittest

import test_cast as base

INSPECTOR = """
Object.defineProperty(window,'polishTest',{get:()=>({
 px:(opts,dir)=>pxPaint(mixRecipe({...mixDefault(),headwear:'none',...opts},'#62465a'),dir||'down',false,0),
 player:()=>playerChoice,
 hd:(opts,dir)=>{const r=mixRecipe({...mixDefault(),headwear:'none',...opts},'#62465a');if(!hdWanted(r))return null;
   const o=pxSpriteHD(r,dir||'down',false,0,4),d=o.getContext('2d').getImageData(0,0,o.width,o.height).data,px=pxPaint(r,dir||'down',false,0);
   const at=(x,y)=>{const i=((y*4+2)*o.width+x*4+2)*4;return '#'+[d[i],d[i+1],d[i+2]].map(v=>v.toString(16).padStart(2,'0')).join('');};
   return {eye:at(11,18),eye2:at(20,18),mouth:at(16,23),sum:Array.from(d.filter((_,i)=>i%7===0)).reduce((a,b)=>a+b,0)};},
 hdCast:()=>[hdWanted(castLook('delores',{})),hdWanted(mixRecipe({...mixDefault(),hairdo:'bald',hairStyle:''},'#62465a'))]
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')

K = '#2b2433'


class Polish(base.Cast):
    def px(self, opts, direction='down'):
        return self.page.evaluate('(a)=>window.polishTest.px(a[0],a[1])', [opts, direction])

    def at(self, pixels, x, y):
        return pixels[y * 32 + x]

    def test_01_closing_with_x_keeps_the_new_look(self):
        self.page.locator('#title-who').click()
        self.page.locator('button[data-tab="hair"]').click()
        self.page.locator('[data-opt="hairStyle"][data-value="curls"]').click()
        self.page.keyboard.press('Escape')
        self.assertEqual(self.page.evaluate('window.castTest.player().kind'), 'human')
        self.page.reload()
        self.assertEqual(self.page.evaluate('window.polishTest.player().hairStyle'), 'curls')

    def test_02_hijab_and_coverings_leave_the_face_visible(self):
        for cover in ('hijab', 'scarf', 'wrap', 'turban', 'bandana'):
            for eyes in (1, 2, 3):
                bare = self.px({'eyes': eyes, 'hairdo': 'bald', 'hairStyle': ''})
                covered = self.px({'eyes': eyes, 'headwear': cover})
                for x, y in ((11, 17), (12, 18), (20, 17), (21, 18), (16, 23), (15, 17)):
                    self.assertEqual(self.at(covered, x, y), self.at(bare, x, y), f'{cover} with {eyes} eyes hides the face at {x},{y}')

    def test_03_eye_expressions_change_eyes_and_mouth_is_its_own_choice(self):
        neutral = self.px({'expression': 'neutral'})
        eye_rows = range(14, 21)
        mouth_rows = range(22, 25)
        for ex in ('happy', 'surprised', 'skeptical', 'sleepy', 'wink'):
            other = self.px({'expression': ex})
            self.assertNotEqual([neutral[y * 32 + x] for y in eye_rows for x in range(8, 25)],
                                [other[y * 32 + x] for y in eye_rows for x in range(8, 25)], f'{ex} must change the eyes')
            self.assertEqual([neutral[y * 32 + x] for y in mouth_rows for x in range(12, 22)],
                             [other[y * 32 + x] for y in mouth_rows for x in range(12, 22)], f'{ex} must not change the mouth')
        mouths = {m: tuple(self.px({'mouth': m})[22 * 32:26 * 32]) for m in ('soft', 'smile', 'grin', 'oh', 'cat')}
        self.assertEqual(len(set(mouths.values())), 5)
        self.page.locator('#title-who').click()
        self.page.locator('button[data-tab="body"]').click()
        self.assertEqual(self.page.locator('[data-opt="mouth"]').count(), 5)
        self.assertEqual(self.page.locator('canvas[data-icon^="expression:"]').count(), 6)

    def test_04_side_view_is_a_profile(self):
        front = self.px({})
        side = self.px({}, 'right')
        self.assertEqual(self.at(front, 11, 18), K)
        self.assertNotEqual(self.at(side, 11, 18), K, 'the far eye is hidden in profile')
        self.assertEqual(self.at(side, 21, 18), K, 'one eye near the front')
        self.assertIsNotNone(self.at(side, 26, 20), 'a little nose past the outline')
        left = self.px({}, 'left')
        self.assertEqual(self.at(left, 10, 18), K)

    def test_05_fur_feathers_scales_each_look_different(self):
        base_look = {'hairdo': 'bald', 'hairStyle': '', 'skin': '#a8e0c8'}
        looks = {}
        for surface, texture in (('skin', 'smooth'), ('fur', 'short'), ('fur', 'fluffy'), ('feathers', 'soft'),
                                 ('feathers', 'layered'), ('scales', 'fine'), ('scales', 'plated')):
            pixels = self.px({**base_look, 'surface': surface, 'texture': texture})
            looks[(surface, texture)] = tuple(pixels)
            if surface != 'skin':
                changed = sum(1 for i, c in enumerate(pixels) if c != looks[('skin', 'smooth')][i])
                self.assertGreater(changed, 25, f'{surface} {texture} should be easy to see')
        self.assertEqual(len(set(looks.values())), 7)

    def test_06_robots_can_wear_hair(self):
        bald = self.px({'surface': 'metal', 'texture': 'polished', 'skin': '#c8d3d6', 'hairdo': 'bald', 'hairStyle': ''})
        looks = set()
        for family in ('straight', 'waves', 'curls', 'coils', 'locs', 'twists'):
            pixels = self.px({'surface': 'metal', 'texture': 'polished', 'skin': '#c8d3d6', 'hairStyle': family, 'hairLength': 'long'})
            self.assertNotEqual(pixels, bald)
            looks.add(tuple(pixels))
        self.assertEqual(len(looks), 6)

    def test_07_spanish_hair_words(self):
        self.page.evaluate("window.castTest && window.profileTestLang && window.profileTestLang('es')")
        self.page.locator('#title-who').click()
        self.page.locator('button[data-tab="hair"]').click()
        text = self.page.locator('#pp-mix').inner_text()
        for word in ('Largo del pelo', 'Peinado', 'Liso', 'Ondas', 'Rizos', 'Rastas', 'Medio'):
            self.assertIn(word, text)
        for word in ('Length', 'Medium', 'Straight', 'Waves'):
            self.assertNotIn(word, text)

    def test_09_side_view_hair_is_one_curtain_not_a_mullet(self):
        # Medium and long hair covers the ear in profile; only the Mullet shows the ear with a separate tail.
        for family in ('straight', 'waves', 'curls', 'coils', 'locs', 'twists'):
            for length in ('medium', 'long'):
                side = self.px({'hairStyle': family, 'hairLength': length}, 'right')
                self.assertNotEqual(self.at(side, 14, 19), self.px({'hairdo': 'bald', 'hairStyle': ''}, 'right')[19 * 32 + 14],
                                    f'{family} {length}: hair should fall over the ear')
        mullet = self.px({'hairStyle': 'mullet', 'hairLength': 'long'}, 'right')
        bald = self.px({'hairdo': 'bald', 'hairStyle': ''}, 'right')
        self.assertEqual(self.at(mullet, 14, 19), self.at(bald, 14, 19), 'the mullet shows the ear')
        self.assertIsNotNone(self.at(mullet, 6, 30), 'with a long tail at the back')

    def test_10_add_ons_are_detailed_and_keep_the_face_clear(self):
        self.assertEqual(self.page.evaluate('window.polishTest.hdCast()'), [False, False], 'named cast and plain looks stay pixel art')
        bare = self.page.evaluate("window.polishTest.px({hairdo:'bald',hairStyle:''})")
        looks = set()
        for opts in [{'hairStyle': f, 'hairLength': l} for f in ('straight', 'waves', 'curls', 'coils', 'locs', 'twists', 'mullet') for l in ('short', 'medium', 'long')] + [
                {'hairdo': 'bald', 'hairStyle': '', 'surface': s, 'texture': t} for s, t in (('fur', 'fluffy'), ('feathers', 'soft'), ('scales', 'fine'))] + [
                {'hairdo': 'bald', 'hairStyle': '', 'ears': 'cat', 'wings': 'bat', 'tail': 'fox', 'horns': 'curled'}]:
            hd = self.page.evaluate('(o)=>window.polishTest.hd(o)', opts)
            self.assertIsNotNone(hd, f'{opts} should be drawn in detail')
            self.assertEqual(hd['eye'], K, f'{opts}: the eyes stay visible')
            self.assertEqual(hd['eye2'], K, f'{opts}: the eyes stay visible')
            looks.add(hd['sum'])
        # The mullet's length is its tail at the back, so it shows from the side.
        self.assertEqual(len(looks), 24, 'every style, length and add-on looks different')
        tails = {self.page.evaluate("(l)=>window.polishTest.hd({hairStyle:'mullet',hairLength:l},'right').sum", l) for l in ('short', 'medium', 'long')}
        self.assertEqual(len(tails), 3)

    def test_08_texture_fold_stays_open(self):
        self.page.locator('#title-who').click()
        self.page.locator('button[data-tab="hair"]').click()
        self.page.locator('.pp-hair-details summary').click()
        self.page.locator('[data-opt="hairPattern"][data-value="3c"]').click()
        self.assertTrue(self.page.locator('.pp-hair-details').evaluate('d=>d.open'))


for name in dir(base.Cast):
    if name.startswith('test_'):
        setattr(Polish, name, None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
