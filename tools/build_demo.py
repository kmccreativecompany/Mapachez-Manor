"""Make the free demo night copy: dist/mapachez-demo.html.

The demo is the same game with DEMO_BUILD switched on: the story chapter, the first
12 guest moments and quick shifts are open; hotel training, the manager corner and
certificates show a friendly "full edition" card instead. It is not copy protection;
anyone can read the HTML. Nothing here is uploaded anywhere. No dependencies.
"""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
html = (root / 'index.html').read_text(encoding='utf-8')
flag = 'const DEMO_BUILD=false;'
if html.count(flag) != 1:
    raise SystemExit('Could not find the DEMO_BUILD switch in index.html')
html = html.replace(flag, 'const DEMO_BUILD=true;')
html = html.replace('<title>', '<title>Free demo night · ', 1)
out = root / 'dist' / 'mapachez-demo.html'
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding='utf-8')
print(f'Wrote {out.relative_to(root)} ({out.stat().st_size // 1024} KB).')
