"""Browser checks for the weather layer and the weather button.

Run: python tests/test_weather.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py (reduced motion on).
"""
import time
import unittest

import test_growth as base


class Weather(base.Growth):
    def enter(self):
        self.page.locator('#begin').click()
        self.page.wait_for_selector('.weather-chip')
        self.page.keyboard.press('Escape')
        time.sleep(.6)

    def test_01_button_cycles_and_saves_weather(self):
        self.enter()
        self.page.evaluate("localStorage.removeItem('mapachez_weather_v1')")
        seen = []
        for _ in range(8):
            self.page.locator('.weather-chip').click()
            seen.append(self.page.evaluate("localStorage.getItem('mapachez_weather_v1')"))
        self.assertEqual(seen, ['rain', 'storm', 'leaves', 'petals', 'snow', 'fireflies', 'clear', 'auto'])
        self.page.locator('.weather-chip').click()
        time.sleep(.3)
        self.assertIn('Soft rain', self.page.locator('.world-caption .weather').inner_text())
        self.assertIn('Gentle rain', self.page.locator('.weather-chip').get_attribute('aria-label'))
        self.assertEqual(self.page.evaluate('window.MapachezWeather.kind'), 'rain')

    def test_02_reduced_motion_paints_one_still_picture(self):
        self.page.evaluate("localStorage.setItem('mapachez_weather_v1','storm')")
        self.page.reload()
        self.enter()
        a = self.page.locator('.weather-layer').screenshot()
        time.sleep(1)
        self.assertEqual(a, self.page.locator('.weather-layer').screenshot(), 'Weather must hold still with Reduce motion')
        self.assertTrue(self.page.evaluate("document.getElementById('canvas-wrap').classList.contains('wx-on')"))

    def test_03_clear_night_draws_nothing(self):
        self.page.evaluate("localStorage.setItem('mapachez_weather_v1','clear')")
        self.page.reload()
        self.enter()
        blank = self.page.evaluate("""()=>{const c=document.querySelector('.weather-layer');
          return !c.getContext('2d').getImageData(0,0,c.width,c.height).data.some(v=>v)}""")
        self.assertTrue(blank)


if __name__ == '__main__':
    unittest.main(verbosity=2)
