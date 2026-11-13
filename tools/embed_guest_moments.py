"""Copy the Silver Key scenario moments into index.html as in-world guest moments.

The training file stays the single source of truth for the 52 moments. Run this
after editing `const rounds = [...]` in training/silver-key.html. No dependencies.
"""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
index = root / 'index.html'
training = (root / 'training/silver-key.html').read_text(encoding='utf-8')

match = re.search(r'\n    const rounds = (\[.*?\n    \]);', training, re.S)
if not match:
    raise SystemExit('Could not find `const rounds = [...]` in training/silver-key.html')
source = match.group(1)
source = re.sub(r'(?m)^(\s+)([A-Za-z_]+):', r'\1"\2":', source)  # quote object keys
source = re.sub(r',(\s*[\]}])', r'\1', source)                   # drop trailing commas
rounds = json.loads(source)
moments = [
    {'dept': r['dept'], 'title': r['title'], 'guest': r['guest'], 'tag': r['tag'],
     'avatar': r['avatar'], 'situation': r['situation'],
     'choices': [[c[0], c[1] + c[2] + c[3]] for c in r['choices']],
     'standard': r['standard']}
    for r in rounds
]
encoded = json.dumps(moments, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
pattern = r'(?m)^const GUEST_MOMENTS = \[.*\];$'
html = index.read_text(encoding='utf-8')
result, count = re.subn(pattern, lambda _: 'const GUEST_MOMENTS = ' + encoded + ';', html)
if count != 1:
    raise SystemExit(f'Expected one GUEST_MOMENTS line in index.html, found {count}')
index.write_text(result, encoding='utf-8')
print(f'Embedded {len(moments)} guest moments in index.html.')
