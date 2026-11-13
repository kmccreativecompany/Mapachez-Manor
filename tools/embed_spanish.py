"""Embed the Spanish words and guest moments into index.html.

Edit training/words-es.json (button and menu words, keyed by the English text) or
training/moments-es.json (the 52 guest moments, matched by their English title),
then run this script. No dependencies.
"""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
index = root / 'index.html'
words = json.loads((root / 'training/words-es.json').read_text(encoding='utf-8'))
moments = json.loads((root / 'training/moments-es.json').read_text(encoding='utf-8'))


def encode(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


html = index.read_text(encoding='utf-8')
for name, value in (('WORDS', {'es': words}), ('MOMENTS_ES', moments)):
    html, count = re.subn(r'(?m)^const ' + name + r' = .*;$', lambda _: 'const ' + name + ' = ' + encode(value) + ';', html)
    if count != 1:
        raise SystemExit(f'Expected one `const {name} = ...;` line in index.html, found {count}')
index.write_text(html, encoding='utf-8')
print(f'Embedded {len(words)} Spanish words and {len(moments)} Spanish guest moments in index.html.')
