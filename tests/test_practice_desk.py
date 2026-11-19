"""Browser checks for the tidy practice desk: the HMS quick reference layer sits in
the page (never floating over lessons), the desk has one scroll bar, and record words
stay on one line instead of breaking apart.

Run: python tests/test_practice_desk.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_training_integration.py.
"""
import unittest

import test_training_integration as base

SCROLLERS = """() => [...document.querySelectorAll('body *')].filter(e => {
  const s = getComputedStyle(e);
  return /auto|scroll/.test(s.overflowY) && e.scrollHeight > e.clientHeight + 2 && e.clientHeight > 120;
}).map(e => e.id || e.className)"""


class PracticeDesk(base.TrainingIntegration):
    def open_record(self, width, height):
        self.page.set_viewport_size({'width': width, 'height': height})
        self.open_training(title=True)
        self.page.locator('[data-training-target="lab"]').click()
        frame = self.page.frame_locator('#silver-key-frame')
        frame.locator('.global-hms-tab[data-hms-tool="record"]').click()
        for _ in range(40):
            if self.training_eval('activeGlobalHmsTool') == 'record':
                break
            self.page.wait_for_timeout(100)
        self.assertEqual(self.training_eval('activeGlobalHmsTool'), 'record')
        return frame

    def check_layout(self, width, height):
        self.open_record(width, height)
        panel = self.training_eval("""() => { const p = document.getElementById('globalHmsPanel'); const s = getComputedStyle(p);
          return {position: s.position, overflow: s.overflowY}; }""")
        self.assertEqual(panel, {'position': 'static', 'overflow': 'visible'}, 'The record sits in the page, not over it')
        self.assertEqual(self.training_eval(SCROLLERS), [], 'Only the page itself scrolls')
        broken = self.training_eval("""() => [...document.querySelectorAll('#globalHmsPanel .global-hms-card .glossary-hotterm, #globalHmsPanel .global-hms-tags')]
          .filter(e => e.classList.contains('global-hms-tags') ? getComputedStyle(e).display !== 'flex' : getComputedStyle(e).display !== 'inline').length""")
        self.assertEqual(broken, 0, 'Glossary words stay inside their sentence and chips sit in a row')

    def test_desk_01_desktop_layout(self):
        self.check_layout(1880, 930)

    def test_desk_02_phone_layout(self):
        self.check_layout(390, 844)

    def test_desk_03_opening_far_down_brings_the_record_into_view_and_close_returns(self):
        self.open_record(1440, 1000)
        self.training_eval("() => document.querySelector('[data-hms-close]').click()")
        self.training_eval("() => scrollTo(0, document.scrollingElement.scrollHeight)")
        bottom = self.training_eval('() => scrollY')
        self.assertGreater(bottom, 800)
        self.training_eval("() => openGlobalHmsTool('record')")
        self.page.wait_for_timeout(300)
        top = self.training_eval("() => document.getElementById('globalHmsPanel').getBoundingClientRect().top")
        self.assertTrue(0 <= top < 600, 'The opened record is on screen')
        self.training_eval("() => document.querySelector('[data-hms-close]').click()")
        self.assertLess(abs(self.training_eval('() => scrollY') - bottom), 40, 'Close puts the player back where they were')

    def test_desk_04_delores_helps_only_when_asked(self):
        self.open_training(title=True)
        self.page.locator('[data-training-target="lab"]').click()
        self.assertFalse(self.page.locator('#silver-key-coach').is_visible(), 'Help stays out of the way until asked')
        self.page.locator('#silver-key-help').click()
        self.assertTrue(self.page.locator('#silver-key-coach').is_visible())
        self.assertIn('HMS practice', self.page.locator('#sk-coach-title').inner_text())
        self.assertEqual(self.page.locator('#sk-coach-steps li').count(), 3)
        self.page.locator('[data-training-target="glossary"]').click()
        self.assertIn('Glossary', self.page.locator('#sk-coach-title').inner_text())
        self.page.locator('#sk-coach-lessons').click()
        self.page.wait_for_function("!document.getElementById('silver-key-frame')")
        self.assertEqual(self.page.locator('#modal-heading').inner_text(), 'The desk computer', 'Opens the guided HMS lessons')
        self.assertEqual(self.page.locator('#hms-lessons .hms-lesson').count(), 5)

# Run only this file's checks; the shared harness's own tests live in test_training_integration.py.
for _name in [n for n in dir(base.TrainingIntegration) if n.startswith('test_')]:
    setattr(PracticeDesk, _name, None)

if __name__ == '__main__':
    unittest.main()
