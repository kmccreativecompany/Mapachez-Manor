"""Browser regression tests for twelve character-creator hair shapes.

Run: python tests/test_hair_styles.py
Requires Playwright and Chromium; uses the isolated no-network test_cast harness.
"""
import unittest

import test_cast as base

INSPECTOR = """
Object.defineProperty(window,'hairTest',{get:()=>({
 styles:MIX_HAIR_STYLES,
 tips:MIX_HAIR_TIPS,
 look:(opts,dir)=>pxPaint(mixRecipe({...mixDefault(),...opts,headwear:'none'},'#62465a'),dir||'down',false,0).join('|'),
 pixels:(id,dir)=>pxPaint(mixRecipe({...mixDefault(),hairStyle:id,hairdo:'long',
   hairPattern:(MIX_HAIR_STYLES.find(s=>s.id===id)||{}).texture||'2b',
   headwear:'none'},'#62465a'),dir,false,0).join('|'),
 legacy:()=>pxPaint(mixRecipe({...mixDefault(),hairStyle:'',hairdo:'long',
   headwear:'none'},'#62465a'),'down',false,0).join('|')
})});
"""
base.TEST_HTML = base.TEST_HTML.replace('\n})();\n</script>', '\n' + INSPECTOR + '\n})();\n</script>')


class HairStyles(base.Cast):
    def test_01_exactly_twelve_distinct_styles_in_all_directions(self):
        ids = self.page.evaluate('window.hairTest.styles.map(s=>s.id)')
        self.assertEqual(len(ids), 12)
        self.assertEqual(len(set(ids)), 12)
        for direction in ('down','left','right','up'):
            hashes = self.page.evaluate(
                "(d)=>window.hairTest.styles.map(s=>window.hairTest.pixels(s.id,d))", direction)
            self.assertEqual(len(set(hashes)), 12, f'duplicate sprites in {direction}')

    def test_02_thumbnails_match_sprite_and_live_preview_changes(self):
        self.page.locator('#title-who').click()
        self.page.locator('[data-tab="hair"]').click()
        options = self.page.locator('canvas[data-icon^="hairStyle:"]')
        self.assertEqual(options.count(), 12)
        images = options.evaluate_all('(cs)=>cs.map(c=>c.toDataURL())')
        self.assertEqual(len(set(images)), 12)
        before = self.page.locator('#pp-view').evaluate('(c)=>c.toDataURL()')
        self.page.locator('[data-opt="hairStyle"][data-value="cloud-curls"]').click()
        after = self.page.locator('#pp-view').evaluate('(c)=>c.toDataURL()')
        self.assertNotEqual(before, after)
        self.assertEqual(self.page.locator('[data-opt="hairStyle"][data-value="cloud-curls"]').get_attribute('aria-pressed'), 'true')
        self.page.locator('[data-opt="hairPattern"][data-value="3c"]').click()
        self.assertEqual(self.page.locator('[data-opt="hairStyle"][data-value="cloud-curls"]').get_attribute('aria-pressed'), 'true')

    def test_03_save_reload_and_older_looks(self):
        self.page.locator('#title-who').click()
        self.page.locator('[data-tab="hair"]').click()
        self.page.locator('[data-opt="hairStyle"][data-value="high-puff"]').click()
        self.page.locator('#pp-done').click()
        self.assertEqual(self.page.evaluate('window.castTest.player().hairStyle'), 'high-puff')
        self.page.reload()
        self.assertEqual(self.page.evaluate('window.castTest.player().hairStyle'), 'high-puff')
        self.assertTrue(self.page.evaluate('window.hairTest.legacy().length > 1000'))
        self.page.locator('#title-who').click()
        self.page.locator('[data-tab="hair"]').click()
        self.page.locator('[data-opt="hairdo"][data-value="bald"]').click()
        self.page.locator('#pp-done').click()
        self.assertEqual(self.page.evaluate('window.castTest.player().hairdo'), 'bald')

    def test_04_phone_works_with_hair_picker(self):
        self.context.close()
        self.setUp()
        self.page.set_viewport_size({'width':390,'height':844})
        self.page.locator('#title-who').click()
        self.page.locator('[data-tab="hair"]').click()
        self.assertEqual(self.page.locator('[data-opt="hairStyle"]').count(), 12)
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'),390)
        self.page.locator('[data-opt="hairStyle"][data-value="soft-pixie"]').click()
        self.assertTrue(self.page.locator('#pp-view').is_visible())


    def test_05_no_player_body_shape_choices(self):
        self.page.locator('#title-who').click()
        self.page.locator('[data-tab="body"]').click()
        self.assertEqual(self.page.locator('[data-opt="body"]').count(), 0)
        self.assertNotIn('Body shape', self.page.locator('#pp-mix').inner_text())
        self.assertEqual(self.page.locator('[data-opt="eyes"]').count(), 3)
        self.page.locator('#pp-random').click()
        self.page.locator('#pp-done').click()
        self.assertEqual(self.page.evaluate('window.castTest.player().body'), 'round')


    def test_06_style_lengths_match_hair_names(self):
        tips = self.page.evaluate('window.hairTest.tips')
        names = dict(self.page.evaluate(
            'window.hairTest.styles.map(s=>[s.id,s.label])'))
        self.assertEqual(names['shoulder-straight'], 'Shoulder Straight')
        self.assertLess(tips['sleek-bob'], tips['shoulder-straight'])
        self.assertLess(tips['wavy-bob'], tips['soft-waves'])
        self.assertLess(tips['curly-bob'], tips['long-curls'])
        self.assertLess(tips['soft-waves'], tips['long-waves'])
        self.assertLessEqual(tips['shoulder-straight'], 26,
                             'Shoulder hair must not fall down the torso')
        self.assertLessEqual(max(tips.values()), 33,
                             'Long styles must stop above the feet')


    def test_07_refined_features_remain_visually_distinct(self):
        pairs = [
            ({'ears':'cat'},{'ears':'pointed'}),
            ({'ears':'rabbit'},{'ears':'floppy'}),
            ({'horns':'short'},{'horns':'curled'}),
            ({'glasses':'none'},{'glasses':'round'}),
            ({'eyes':1},{'eyes':3}),
        ]
        for first, second in pairs:
            a = self.page.evaluate('(x)=>window.hairTest.look(x)', first)
            b = self.page.evaluate('(x)=>window.hairTest.look(x)', second)
            self.assertNotEqual(a, b, f'{first} and {second} look identical')

    def test_08_detail_preserves_all_hair_views(self):
        for direction in ('down','left','right','up'):
            drawings = self.page.evaluate(
                '(d)=>window.hairTest.styles.map(s=>window.hairTest.pixels(s.id,d))',
                direction)
            self.assertEqual(len(set(drawings)), 12,
                             f'New detail flattened styles in {direction}')


for name in dir(base.Cast):
    if name.startswith('test_') and name not in HairStyles.__dict__:
        setattr(HairStyles,name,None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
