"""Browser checks for CERT SHARE v1: the credential link, the code-drawn QR code, the share post
and the skills list on the course certificate.

Run: python tests/test_cert_share.py
Set CHROMIUM_PATH if Chromium is not installed at /usr/bin/chromium.
Shares the isolated-storage, no-network harness from test_growth.py. If OpenCV (cv2) is installed,
the QR code is also scanned; otherwise that one check is skipped.
"""
import base64
import unittest
from urllib.parse import urlparse, parse_qs

import test_growth as base

PASSED = ("try{localStorage.setItem('mapachez_course_v1',JSON.stringify({version:1,mods:[1,2,3,4,5,6],"
          "tries:1,best:6,passed:'2026-11-20',salt:'abc123xy',name:'Rosa Quill',asked:true}))}catch(e){}")
HOME = 'https://kmccreativecompany.github.io/Mapachez-Manor/'


class CertShare(base.Growth):
    """Reuses the growth harness but none of its tests."""

    def setUp(self, viewport=None):
        super().setUp(viewport)
        self.context.add_init_script(PASSED)
        self.page.goto(self.url)

    def route(self, route):
        # Credential links add a query string; serve the same test page for them.
        if route.request.url.split('?')[0] == self.url:
            route.fulfill(status=200, content_type='text/html', body=base.TEST_HTML)
        else:
            super().route(route)

    def open_cert(self):
        self.page.locator('#co-title').click()
        # The title button opens the course catalog (MORE COURSES v1); the check-in course is first.
        self.page.locator('#mc-open-chk').click()
        self.page.locator('.co-cert-open').click()
        self.page.wait_for_selector('#co-share .cs-card')

    def links(self):
        add = parse_qs(urlparse(self.page.locator('.cs-add').get_attribute('href')).query)
        share = parse_qs(urlparse(self.page.locator('.cs-share').get_attribute('href')).query)
        return add, share

    def test_01_linkedin_form_gets_the_credential_link_and_names_the_game(self):
        self.open_cert()
        add, _ = self.links()
        self.assertIn('Mapáchez Manor', add['name'][0])
        self.assertIn('Silver Key Certificate', add['name'][0])
        cred = add['certUrl'][0]
        self.assertTrue(cred.startswith(HOME + '?cert=SKC-CHK-'))
        q = parse_qs(urlparse(cred).query)
        self.assertEqual(q['cert'], add['certId'])
        self.assertEqual(q['n'], ['Rosa Quill'])
        self.assertEqual(q['d'], ['2026-11-20'])

    def test_02_share_post_and_skills(self):
        self.open_cert()
        add, share = self.links()
        self.assertEqual(urlparse(self.page.locator('.cs-share').get_attribute('href')).netloc, 'www.linkedin.com')
        post = share['text'][0]
        self.assertIn('Front Desk Check-In & Guest Registration Fundamentals', post)
        self.assertIn(add['certUrl'][0], post)
        skills = self.page.locator('#co-share .cs-skills li').all_inner_texts()
        for s in ('Guest Check-In', 'Hotel Management Systems', 'Guest Service'):
            self.assertIn(s, skills)
        self.assertIn('Copy skills', self.page.locator('#co-share').inner_text())

    def test_03_certificate_carries_a_qr_code_to_the_game(self):
        self.open_cert()
        png = self.page.evaluate("document.getElementById('co-cert').toDataURL('image/png')")
        # A dark QR module sits inside the white QR box at the bottom right.
        dark = self.page.evaluate("(()=>{const d=document.getElementById('co-cert').getContext('2d').getImageData(948,680,112,112).data;let n=0;for(let i=0;i<d.length;i+=4)if(d[i]<80)n++;return n})()")
        self.assertGreater(dark, 2000)
        try:
            import cv2
            import numpy as np
        except ImportError:
            self.skipTest('OpenCV not installed; QR scan skipped')
        img = cv2.imdecode(np.frombuffer(base64.b64decode(png.split(',')[1]), np.uint8), cv2.IMREAD_COLOR)
        self.assertEqual(cv2.QRCodeDetector().detectAndDecode(img)[0], HOME)

    def test_04_credential_link_shows_the_certificate_to_anyone(self):
        self.open_cert()
        cred = self.links()[0]['certUrl'][0]
        page = self.context.new_page()
        page.route('**/*', self.route)
        page.add_init_script("localStorage.clear()")
        page.goto(self.url + '?' + cred.split('?', 1)[1])
        page.wait_for_selector('#cs-cert')
        text = page.locator('#modal-body').inner_text()
        self.assertIn('Rosa Quill completed Front Desk Check-In', text)
        self.assertIn('complete and unchanged', text)
        self.assertIn('not an accreditation', text)
        self.assertIn('Earn yours free', text)
        # Viewing someone's certificate never touches the visitor's own progress.
        self.assertIsNone(page.evaluate("localStorage.getItem('mapachez_course_v1')"))
        page.close()

    def test_05_edited_link_gets_a_gentle_note(self):
        self.open_cert()
        cred = self.links()[0]['certUrl'][0].replace('Rosa', 'Rose')
        self.page.goto(self.url + '?' + cred.split('?', 1)[1])
        self.page.wait_for_selector('#cs-actions .primary-button')
        self.assertIn('incomplete', self.page.locator('#modal-heading').inner_text())
        self.assertEqual(self.page.locator('#cs-cert').count(), 0)

    def test_06_phone_layout_fits(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.open_cert()
        wide = self.page.evaluate("document.getElementById('modal-body').scrollWidth>document.getElementById('modal-body').clientWidth+1")
        self.assertFalse(wide)
        self.assertEqual(self.errors, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
