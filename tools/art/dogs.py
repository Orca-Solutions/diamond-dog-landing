"""The three collar-wearing spot dogs on the landing page: sitting (receipt section), digging
(questions) and resting (closing block).

The bodies are hand-drawn paths in the mark's flat geometry. The collars are computed, so every
edge lines up: a narrow acid band that sits on the neck (a little proud of the outline, as a
strap does) with an ink rim, a ring that disappears under the band, and one lilac diamond tag
hanging straight down from the ring, as the brand book asks.

    python3 tools/art/dogs.py      # rewrites the three dog SVGs in site/index.html

Needs Python 3.9+ and shapely 2 (pip install shapely). The page itself stays buildless: the
output is plain inline SVG, committed with the page.
"""
import math, re
from pathlib import Path
from shapely import affinity
from shapely.geometry import LineString, MultiPolygon, Point, Polygon
from shapely.ops import unary_union

PAGE = Path(__file__).resolve().parents[2] / 'site' / 'index.html'
TOKEN = re.compile(r'[MLHVQCZmlhvqcz]|-?\d*\.?\d+(?:e-?\d+)?')


def f(x):
    s = ('%.2f' % x).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def cbez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])


def path_polys(d, steps=24):
    """Polygons for each closed subpath of an SVG path (M L H V Q C Z, absolute or relative)."""
    toks = TOKEN.findall(d)
    i, cmd = 0, None
    cur = start = (0.0, 0.0)
    rings, pts = [], []

    def num():
        nonlocal i
        i += 1
        return float(toks[i - 1])

    while i < len(toks):
        if re.match(r'[A-Za-z]', toks[i]):
            cmd = toks[i]
            i += 1
        c = cmd.upper()
        ox, oy = cur if cmd.islower() else (0.0, 0.0)
        if c == 'Z':
            if pts:
                rings.append(pts)
            pts, cur = [], start
            continue
        if c == 'M':
            if pts:
                rings.append(pts)
            cur = start = (ox + num(), oy + num())
            pts = [cur]
            cmd = 'l' if cmd.islower() else 'L'
        elif c == 'L':
            cur = (ox + num(), oy + num())
            pts.append(cur)
        elif c == 'H':
            cur = (ox + num(), cur[1])
            pts.append(cur)
        elif c == 'V':
            cur = (cur[0], oy + num())
            pts.append(cur)
        elif c == 'Q':
            p0, p1, p2 = cur, (ox + num(), oy + num()), (ox + num(), oy + num())
            for k in range(1, steps + 1):
                t = k / steps
                u = 1 - t
                pts.append((u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0], u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1]))
            cur = p2
        elif c == 'C':
            p0, p1, p2, p3 = cur, (ox + num(), oy + num()), (ox + num(), oy + num()), (ox + num(), oy + num())
            pts += [cbez(p0, p1, p2, p3, k / steps) for k in range(1, steps + 1)]
            cur = p3
        else:
            raise ValueError(c)
    if len(pts) > 2:
        rings.append(pts)
    return [Polygon(r).buffer(0) for r in rings if len(r) > 2]


def shape(*ds):
    return unary_union([p for d in ds for p in path_polys(d)])


def ellipse(cx, cy, rx, ry):
    return affinity.scale(Point(cx, cy).buffer(1, quad_segs=32), rx, ry)


def to_path(geom):
    """SVG path data for a (multi)polygon, coordinates to two decimals."""
    out = []
    for p in (geom.geoms if isinstance(geom, MultiPolygon) else [geom]):
        for ring in [p.exterior] + list(p.interiors):
            out.append('M' + 'L'.join('%s %s' % (f(x), f(y)) for x, y in list(ring.coords)[:-1]) + 'Z')
    return ''.join(out)


def collar(curve, width, body, proud=1.0, rim=0.9, ring=2.1, ring_w=1.1, tag=(3.6, 4.6), tag_rim=1.0,
           hang_end=False):
    """Markup for a collar, in paint order: ring, rim, band, tag.

    curve: a cubic's four points running past the neck on both sides. body: the silhouette the
    band sits on; the band is clipped to it, grown by `proud`. The ring hangs from the band's
    lowest point (or from the end of the curve, when the rest of the band is out of sight), and
    the band is painted over the ring's top half.
    """
    line = LineString([cbez(*curve, k / 120) for k in range(121)])
    band = line.buffer(width / 2, cap_style='flat', join_style='round', quad_segs=12)
    strap = band.intersection(body.buffer(proud, join_style='round', quad_segs=8)).simplify(0.04)
    edge = strap.buffer(rim, join_style='mitre', mitre_limit=2.0).simplify(0.04)

    hang = curve[3] if hang_end else max(strap.exterior.coords, key=lambda p: p[1])
    rc = (hang[0], hang[1] + ring * 0.45)
    top = (rc[0], rc[1] + ring - ring_w * 0.35)
    hw, hh = tag
    tag_poly = Polygon([top, (top[0] + hw, top[1] + hh), (top[0], top[1] + 2 * hh), (top[0] - hw, top[1] + hh)])
    return ''.join([
        '<circle class="dog-ring" cx="%s" cy="%s" r="%s" stroke-width="%s"/>' % (f(rc[0]), f(rc[1]), f(ring), f(ring_w)),
        '<path class="dog-collar-edge" d="%s"/>' % to_path(edge),
        '<path class="dog-collar" d="%s"/>' % to_path(strap),
        '<path class="dog-tag" d="%s" stroke-width="%s"/>' % (to_path(tag_poly), f(tag_rim)),
    ])


# ---------------------------------------------------------------- sitting dog (paper on ink)
SIT_BODY = 'M40 186 Q30 150 44 114 Q58 86 84 82 L100 84 Q118 112 116 150 Q114 176 104 186 Z'
SIT_NECK = 'M54 100 Q60 80 82 72 L118 80 Q108 90 109 102 Q100 110 60 110 Z'


def sit():
    body = ('<path d="%s"/>' % SIT_BODY +
            '<path d="M30 186 Q24 150 46 136 Q60 134 62 150 Q50 160 48 186 Z"/>'
            '<path d="M58 186 V128 H72 V186 Z M84 186 V128 H98 V186 Z"/>'
            '<path class="dog-line" d="M62 186 V179 M68 186 V179 M88 186 V179 M94 186 V179"/>'
            '<g class="dog-tail" style="transform-origin:30px 176px"><path d="M30 178 Q12 170 6 150 Q10 146 16 152 Q22 166 34 170 Z"/></g>'
            '<path d="%s"/>' % SIT_NECK)
    head = ('<g transform="rotate(-12 92 54)">'
            '<path d="M70 60 Q70 24 102 24 Q134 24 134 60 L134 76 Q134 90 120 94 L84 94 Q70 90 70 76 Z"/>'
            '<path d="M72 38 L52 62 L62 88 L78 70 Z M132 38 L152 62 L142 88 L126 70 Z"/>'
            '<circle class="dog-bg" cx="90" cy="56" r="5.5"/><circle class="dog-bg" cx="114" cy="56" r="5.5"/>'
            '<circle cx="91.5" cy="54.5" r="2.4"/><circle cx="115.5" cy="54.5" r="2.4"/>'
            '<path class="dog-bg" d="M102 72 l8 8 l-8 8 l-8 -8 z"/></g>')
    band = collar(((42, 94), (62, 108), (98, 112), (122, 95)), 4.6, shape(SIT_BODY, SIT_NECK))
    return ('<svg class="dog dog-sit" viewBox="0 0 160 190" width="120" aria-hidden="true" focusable="false">'
            + body + band + head + '</svg>')


# ---------------------------------------------------------------- digging dog (ink on paper)
DIG_BODY = 'M60 128 Q70 104 96 90 Q128 72 162 70 Q194 70 204 92 Q212 116 196 128 L160 128 Q130 126 100 134 Z'
HOLE = (62, 134, 54, 14)


def dig():
    # The band runs from the nape down into the hole and ends at the throat, where the ring is;
    # the tag dangles into the hole.
    band = collar(((62, 100), (70, 112), (80, 124), (92, 136)), 4.4,
                  shape(DIG_BODY).union(ellipse(*HOLE)), hang_end=True)
    parts = ['<ellipse cx="%s" cy="%s" rx="%s" ry="%s"/>' % HOLE,
             '<path d="%s"/>' % DIG_BODY,
             '<path d="M168 122 L164 146 L182 146 L186 122 Z M188 122 L186 146 L204 146 L206 122 Z"/>',
             '<path class="dog-line" d="M170 146 V140 M176 146 V140 M192 146 V140 M198 146 V140"/>',
             '<g class="dog-tail" style="transform-origin:202px 88px"><path d="M200 90 Q206 62 226 48 Q232 52 224 62 Q214 76 212 96 Z"/></g>',
             band,
             '<path d="M16 112 l7 -4 l2 7 z M30 98 l6 -5 l4 7 z M8 126 l6 0 l-1 6 z M44 92 l3 -5 l4 4 z"/>']
    return ('<svg class="dog dog-dig" viewBox="0 0 240 150" width="300" aria-hidden="true" focusable="false">'
            + ''.join(parts) + '</svg>')


# ---------------------------------------------------------------- resting dog (ink on lilac)
REST_BODY = 'M98 118 Q78 118 80 98 Q86 72 128 68 L192 66 Q230 66 238 94 Q242 118 218 118 Z'
REST_CHEST = 'M52 112 Q46 82 62 62 L106 62 Q122 82 116 112 Z'


def rest(tilt=-6, look=1.6):
    """Lying down, head up and a little tilted, watching the button."""
    head = ('<g transform="rotate(%s 84 40)">' % f(tilt) +
            '<path d="M50 44 Q50 10 84 10 Q118 10 118 44 L118 54 Q118 66 104 68 L64 68 Q50 66 50 54 Z"/>'
            '<path d="M52 22 L32 44 L44 68 L58 52 Z M116 22 L136 44 L124 68 L110 52 Z"/>'
            '<circle class="dog-bg" cx="72" cy="38" r="5.5"/><circle class="dog-bg" cx="96" cy="38" r="5.5"/>'
            '<g class="dog-eyes"><circle cx="%s" cy="38.5" r="2.8"/><circle cx="%s" cy="38.5" r="2.8"/></g>' % (f(72 + look), f(96 + look)) +
            '<path class="dog-bg" d="M84 52 l7 7 l-7 7 l-7 -7 z"/></g>')
    parts = ['<path d="%s"/>' % REST_BODY,
             '<path d="M214 118 Q234 114 242 100 Q254 108 248 118 Z"/>',
             '<g class="dog-tail" style="transform-origin:240px 104px"><path d="M238 106 Q252 98 260 82 Q264 86 260 94 Q254 110 242 114 Z"/></g>',
             '<path d="%s"/>' % REST_CHEST,
             collar(((46, 70), (62, 88), (106, 88), (122, 70)), 4.8, shape(REST_CHEST)),
             '<path d="M36 118 L36 110 Q36 102 46 102 L80 102 Q88 102 90 110 L90 118 Z M78 118 L78 110 Q78 102 88 102 L120 102 Q128 102 130 110 L130 118 Z"/>',
             '<path class="dog-line" d="M47 118 V112 M58 118 V112 M69 118 V112 M99 118 V112 M110 118 V112 M121 118 V112"/>',
             head]
    return ('<svg class="dog dog-rest" viewBox="0 0 264 122" width="250" aria-hidden="true" focusable="false">'
            + ''.join(parts) + '</svg>')


if __name__ == '__main__':
    page = PAGE.read_text()
    for cls, svg in (('dog-sit', sit()), ('dog-dig', dig()), ('dog-rest', rest())):
        page, n = re.subn(r'<svg class="dog %s".*?</svg>' % cls, lambda m: svg, page, count=1, flags=re.S)
        assert n == 1, cls
        print(cls, len(svg), 'bytes')
    PAGE.write_text(page)
