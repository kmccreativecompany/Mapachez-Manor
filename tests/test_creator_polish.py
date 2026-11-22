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
 player:()=>playerChoice
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
