"""Browser checks for the visual polish pass: guest faces on dialog cards, the Plush crest,
room colours, and corners/headings that stay tidy.

Run: python tests/test_polish.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py (reduced motion on).
"""
import re
import unittest

import test_growth as base


def painted(page, selector):
    """True when the canvas has visible pixels (something was really drawn)."""
    return page.evaluate("""s => { const c = document.querySelector(s); if (!c || !c.width) return false;
      const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
      for (let i = 3; i < d.length; i += 4) if (d[i]) return true; return false; }""", selector)


class Polish(base.Growth):
    def test_polish_01_guest_moment_shows_the_guest_chibi(self):
        self.page.locator('#title-quick').click()
        self.page.wait_for_selector('#modal-body .choice')
        self.assertEqual(self.page.locator('.scene-head .gm-avatar.has-face').count(), 1)
        self.assertTrue(painted(self.page, '.scene-head .gm-face'), 'The guest card shows a drawn face, not initials')
        self.assertFalse(self.page.locator('.scene-head .gm-initials').is_visible())

    def test_polish_02_crest_is_delores_drawn_in_code(self):
        self.assertTrue(painted(self.page, '.title-crest .crest-face'))
        self.assertNotIn('data:image', base.HTML[base.HTML.index('/* VISUAL POLISH v1'):base.HTML.index('/* VISUAL POLISH v1') + 4000])

    def test_polish_03_six_rooms_six_colours(self):
        hues = re.search(r'const ROOM_HUES=\{(.*?)\};', base.HTML).group(1)
        rooms = re.findall(r'(\d{3}):\[\'(#[0-9a-f]{6})\'', hues)
        self.assertEqual([r for r, _ in rooms], ['201', '202', '203', '204', '205', '206'], 'Only rooms 201 to 206')
        self.assertEqual(len({c for _, c in rooms}), 6, 'Every room has its own colour')

    def test_polish_04_headings_have_no_box_and_corners_stay_small(self):
        self.page.locator('#title-memories').click()
        self.page.wait_for_selector('#modal-heading')
        self.page.wait_for_timeout(200)
        style = self.page.evaluate("getComputedStyle(document.getElementById('modal-heading')).outlineStyle")
        self.assertEqual(style, 'none')
        size = self.page.evaluate("getComputedStyle(document.getElementById('modal')).backgroundSize")
        self.assertIn('34px', size)


if __name__ == '__main__':
    unittest.main()
