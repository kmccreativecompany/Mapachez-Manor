"""Refresh the offline training document embedded in index.html. No dependencies."""
import base64
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
index = root / 'index.html'
training = (root / 'training/silver-key.html').read_bytes()
encoded = base64.b64encode(training).decode('ascii')
pattern = r"(?m)^const SILVER_KEY_DOCUMENT_BASE64 = '[A-Za-z0-9+/=]+';$"
result, count = re.subn(pattern, "const SILVER_KEY_DOCUMENT_BASE64 = '" + encoded + "';", index.read_text())
if count != 1:
    raise SystemExit(f'Expected one embedded Silver Key document, found {count}')
index.write_text(result)
print(f'Embedded {len(training):,} bytes of Silver Key training in index.html.')
