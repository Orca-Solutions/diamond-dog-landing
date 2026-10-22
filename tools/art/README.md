# Art generators

Optional tools that draw two pieces of the landing page's spot art. Their output is plain inline
SVG committed in `site/index.html`, so the site stays buildless and nobody needs these to
preview or deploy it. Run them only to change the drawings.

Needs Python 3.9+ and shapely 2 (`pip install shapely`). Run from the repository root:

| Command | What it rewrites |
| --- | --- |
| `python3 tools/art/dogs.py` | The sitting, digging and resting dogs (`.dog-sit`, `.dog-dig`, `.dog-rest`) in `site/index.html` |
| `python3 tools/art/ribbon.py` | Both looping receipts (`.receipt-ribbon` for wide screens, `.receipt-ribbon-stacked` for 740–1000 px) in `site/index.html` and their boxes in `site/styles.css` |
| `python3 tools/art/ribbon.py --preview out.svg` | Nothing; writes the receipt SVG alone |

- `dogs.py` holds the three dogs' bodies and computes their collars: a narrow acid band that
  sits on the neck, an ink rim, a ring tucked under the band and one lilac diamond tag, as the
  brand book's illustration rules ask. The other dogs on the page (hanging, peeking, paws) are
  hand-written SVG in `index.html`; the two peeking dogs show their collar as an acid band in
  the gap at the neck.
- `ribbon.py` draws the receipt as a curled 3D paper strip in flat cartoon tones with an ink
  outline: shape, the coil's sideways drift, light, tones, the card's shadow and the placement
  are constants at the top of the file. `receipt_text.py` holds what the receipt
  says: the dog's activity records, 18 characters a line in IBM Plex Mono.

Check the receipt section at 1440 px and around 1100 px after changing either file: the ribbon
should clear the copy and slide under the card. Below 1000 px, where the card sits under the
copy, a smaller receipt hangs from the space right of the copy into the card's top edge; it is
hidden below 740 px.

`ribbon.py` also runs `tools/stamp_assets.py`, because it rewrites the stylesheet; `dogs.py`
only touches `index.html`, so it doesn't need to.
