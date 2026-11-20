"""Browser checks for DRAMAS v1: the "Watch the manor dramas" title button.

Run: python tests/test_dramas.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py.
"""
import unittest

import test_growth as base

EMPTY = 'const MANOR_DRAMAS=[\n];'
ONE = "const MANOR_DRAMAS=[{title:'The Stapler Mystery',url:'https://example.com/shorts/one',where:'YouTube'}];"
MANY = ("const MANOR_DRAMAS=[{title:'The Stapler Mystery',url:'https://example.com/shorts/one',where:'YouTube'},"
        "{title:'Room 13',url:'https://example.com/reel/two'},{title:'Bad',url:'javascript:alert(1)'}];")
SPY = "window.__opened=[];window.open=(u,t,f)=>{window.__opened.push([u,t,f]);return null;};"


class Dramas(base.Growth):
    html = base.TEST_HTML

    def route(self, route):
        if route.request.url == self.url:
            route.fulfill(status=200, content_type='text/html', body=self.html)
        else:
            base.Growth.route(self, route)

    def load(self, links):
        self.assertIn(EMPTY, base.TEST_HTML)
        self.html = base.TEST_HTML.replace(EMPTY, links).replace('<head>', '<head><script>' + SPY + '</script>', 1)
        self.page.goto(self.url)

    def test_01_hidden_until_links_exist(self):
        btn = self.page.locator('#drama-title')
        self.assertEqual(btn.count(), 1)
        self.assertTrue(btn.is_hidden())
        self.assertEqual(self.errors, [])

    def test_02_one_link_opens_new_tab(self):
        self.load(ONE)
        btn = self.page.locator('#drama-title')
        self.assertTrue(btn.is_visible())
        self.assertIn('Watch the manor dramas', btn.inner_text())
        btn.click()
        opened = self.page.evaluate('window.__opened')
        self.assertEqual(opened, [['https://example.com/shorts/one', '_blank', 'noopener']])
        self.assertEqual(self.errors, [])
        self.assertEqual(self.requests, [])

    def test_03_many_links_list_safe_ones_only(self):
        self.load(MANY)
        self.page.locator('#drama-title').click()
        links = self.page.locator('#modal-body .drama-list a')
        self.assertEqual(links.count(), 2)
        self.assertEqual(links.nth(0).get_attribute('target'), '_blank')
        self.assertIn('noopener', links.nth(0).get_attribute('rel'))
        self.assertNotIn('javascript', self.page.inner_html('#modal-body'))
        self.page.locator('#drama-close').click()
        self.assertFalse(self.page.evaluate("document.getElementById('modal').open"))
        self.assertEqual(self.errors, [])


for _name in dir(base.Growth):
    if _name.startswith('test_') and _name not in Dramas.__dict__:
        setattr(Dramas, _name, None)


if __name__ == '__main__':
    unittest.main(verbosity=2)
