"""Stamp the stylesheet and script links in site/index.html with a hash of their contents.

The host may let browsers (and its edge) keep styles.css and script.js for hours, while the page
itself is always fetched fresh. A new page with an old stylesheet breaks the art badly, so the
links carry ?v=<hash>: when either file changes, its URL changes, and the old copy is never used.

    python3 tools/stamp_assets.py    # run after editing site/styles.css or site/script.js

tools/art/ribbon.py runs it for you after it rewrites the stylesheet.
"""
import hashlib, re
from pathlib import Path

SITE = Path(__file__).resolve().parents[1] / 'site'
ASSETS = (('href', 'styles.css'), ('src', 'script.js'))


def stamp():
    page = SITE / 'index.html'
    s = page.read_text()
    for attr, name in ASSETS:
        v = hashlib.sha256((SITE / name).read_bytes()).hexdigest()[:10]
        s, n = re.subn(r'%s="%s(\?v=[0-9a-f]*)?"' % (attr, re.escape(name)), '%s="%s?v=%s"' % (attr, name, v), s)
        assert n == 1, name
        print('%s?v=%s' % (name, v))
    page.write_text(s)


if __name__ == '__main__':
    stamp()
