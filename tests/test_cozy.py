"""Browser checks for the cozy foyer test room (COZY FOYER v1).

Run: python tests/test_cozy.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py (reduced motion on).
"""
import re
import unittest

import test_growth as base

BLOCK = base.HTML[base.HTML.index('/* COZY FOYER v1 (test room)'):base.HTML.index('let LABELS=true;')]


class Cozy(base.Growth):
    def test_cozy_01_drawn_in_code_only(self):
        self.assertNotIn('data:image', BLOCK)
        self.assertNotIn('http', BLOCK)
        self.assertNotIn('new Image', BLOCK)

    def test_cozy_02_green_stays_the_main_colour(self):
        self.assertIn("green:'#2f5f4a'", BLOCK)
        self.assertIn("sage:", BLOCK)

    def test_cozy_03_can_switch_back_to_the_old_foyer(self):
        self.assertIn('cozy=0', BLOCK)
        self.assertIn("else roomFloor(g,{x:60,y:479,w:369,h:268}", base.HTML)

    def test_cozy_04_chunky_dialogue_box_in_the_foyer(self):
        self.page.locator('#begin').click()
        self.page.wait_for_timeout(300)
        for _ in range(5):
            self.page.keyboard.press('Escape')
            self.page.wait_for_timeout(150)
        self.assertIn('cozy', self.page.get_attribute('#lobby-chatter', 'class'))
        border = self.page.evaluate("getComputedStyle(document.getElementById('lobby-bubble')).borderTopWidth")
        self.assertEqual(border, '3px')
        self.assertEqual(self.errors, [])

    def test_cozy_07_beige_floor_kept(self):
        self.assertIn("rect(c,r.x,r.y,r.w,r.h,'#e8d8b6');c.fillStyle=floorTile();", BLOCK)

    def test_cozy_05_no_weather_or_network_added(self):
        self.assertNotIn('MapachezWeather', BLOCK)
        self.assertEqual(self.requests, [])


if __name__ == '__main__':
    unittest.main()
