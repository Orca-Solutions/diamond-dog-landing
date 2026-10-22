"""The long paper receipt that loops through the receipt section, drawn as a 3D ribbon in inline SVG.

Model: the strip bends only around one fixed width direction b3 (paper curls, it does not
stretch), seen in orthographic projection. On screen every cross-section is the same vector
B, the strip's 3D depth follows from b3, and shading depends only on the position along the
paper. The centre line is drawn like a turtle: a list of (length, curvature at start,
curvature at end) pieces.

Because every cross-section is parallel to B, the paper between two folds (where it turns
from front to back on screen) never covers itself, and its shading is a function of the
position across B alone. So each such stretch is one polygon filled with a linear gradient
running perpendicular to B: smooth shading, no seams, few elements. Stretches are painted
far to near wherever they overlap.

The printing is real text in the page's mono face. Receipt lines run across the paper, so
each line is one <text> with an affine transform: x along the width (B, foreshortened) and
y along the paper (the projected tangent). Each line is painted straight after the paper
under it, so nearer paper still covers it. Spaces are no-break spaces, so the columns line up
without relying on white-space handling in SVG text.

    python3 tools/art/ribbon.py                    # rewrites the ribbon in site/index.html and its box in site/styles.css
    python3 tools/art/ribbon.py --preview out.svg  # writes the SVG alone

Needs Python 3.9+ and shapely 2 (pip install shapely). Geometry is in shell pixels at a 1440 px
viewport; the CSS box is written in percentages of the evidence grid, so the ribbon scales with
the layout. The receipt's words live in receipt_text.py.
"""
import math, re, sys
from pathlib import Path
from receipt_text import lines as receipt_lines, COLS

SITE = Path(__file__).resolve().parents[2] / 'site'
SHELL = 1320.0                 # the evidence grid's width at a 1440 px viewport

# ------------------------------------------------------------------ design (shell px at 1440)
START = (168.0, -44.0)         # inside the curled free end
HEADING = -31.4                # degrees; 0 = right, positive turns clockwise on screen
PIECES = [                     # (length px, curvature start, curvature end); curvature in 1/px
    (80, -0.106, -0.025),      # the curled free end unwinding (about -300 degrees)
    (40, -0.025, 0.000),
    (150, 0.000, 0.003),       # a gentle run to the right, above the eyebrow
    (30, 0.003, 0.019),
    (314, 0.019, 0.019),       # one full loop, curling under
    (40, 0.019, 0.004),
    (100, 0.004, 0.006),       # a slow S on the way down, right of the heading
    (100, 0.006, -0.006),
    (100, -0.006, -0.002),
    (60, -0.002, 0.0),
    (230, 0.0, 0.0),           # straight on, under the card
]
B = (-20.0, 40.0)              # the strip's width as seen on screen
BZ = 34.0                      # how much the width leans toward the viewer
STEP = 3.0                     # longest sampling step along the centre line, px
LIGHT = (-0.35, -0.55, 0.76)
PAPER = (0xF4, 0xF0, 0xE8)
BACK = (0xDD, 0xD7, 0xCC)
AMBIENT = 0.80
CARD_EDGE = (713.0, -0.0207)   # the receipt card's left edge: x = a + b * (y + 6)
SHADOW = 26.0                  # how far the card's shadow reaches onto the ribbon, px

W3 = math.sqrt(B[0]**2 + B[1]**2 + BZ**2)    # the paper's true width
MARGIN = 0.08                                 # print margin, fraction of the width
FONT = (1 - 2*MARGIN) * W3 / (COLS * 0.6)     # Plex Mono advances 0.6 em
LEAD = 1.5 * FONT                             # line pitch along the paper
CAP = 0.7 * FONT
MIN_FACING = 0.32                             # no print once the paper turns this edge-on
MAX_BEND = 0.04                               # nor where it curls tighter than this (1/px)
BN = math.hypot(*B)
ACROSS = (B[1] / BN, -B[0] / BN)              # unit vector perpendicular to B on screen


def norm3(v):
    L = math.sqrt(sum(c*c for c in v)) or 1.0
    return tuple(c/L for c in v)


def cross3(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def dot3(a, b):
    return sum(x*y for x, y in zip(a, b))


def centre_line():
    """Points along the centre line and the curvature of each step."""
    pts, ks = [START], []
    th = math.radians(HEADING)
    x, y = START
    for length, k0, k1 in PIECES:
        step = max(1.0, min(STEP, 0.055 / (max(abs(k0), abs(k1)) or 1e-9)))
        n = max(1, int(length / step))
        for i in range(n):
            k = k0 + (k1 - k0) * (i + 0.5) / n
            ds = length / n
            th += k * ds
            x += math.cos(th) * ds
            y += math.sin(th) * ds
            pts.append((x, y))
            ks.append(k)
    return pts, ks


def card_x(y):
    return CARD_EDGE[0] + CARD_EDGE[1] * (y + 6)


def build():
    """Quads along the paper, with their facing, shade and depth."""
    c, ks = centre_line()
    # stop once the whole width is well under the card
    for i, (x, y) in enumerate(c):
        if min(x - abs(B[0])/2, x + B[0]/2) > card_x(y) + 34 and i > len(c) // 2:
            c, ks = c[:i+1], ks[:i]
            break
    b3 = (B[0], B[1], BZ)
    # the u=0 edge (centre line minus half the width) and its depth, so the profile lies in
    # the plane normal to b3
    P = [(x - B[0]/2, y - B[1]/2) for x, y in c]
    Z = [-(B[0]*px + B[1]*py) / BZ for px, py in P]
    S = [0.0]
    for i in range(1, len(P)):
        S.append(S[-1] + math.sqrt((P[i][0]-P[i-1][0])**2 + (P[i][1]-P[i-1][1])**2 + (Z[i]-Z[i-1])**2))
    L = norm3(LIGHT)

    # the printed side is the one facing us where the paper runs to the right
    n0 = norm3(cross3((1.0, 0.0, -B[0] / BZ), b3))
    printed_sign = 1 if n0[2] > 0 else -1

    quads = []
    for i in range(len(P) - 1):
        a, b = P[i], P[i+1]
        n = norm3(cross3((b[0]-a[0], b[1]-a[1], Z[i+1]-Z[i]), b3))
        facing = n[2] > 0
        front = (1 if facing else -1) == printed_sign
        nv = n if facing else tuple(-v for v in n)
        light = AMBIENT + (1 - AMBIENT) * max(0.0, dot3(nv, L)) * 1.25
        light *= 0.82 + 0.18 * min(1.0, abs(n[2]) * 1.6)   # darker as it turns edge-on
        mid = ((a[0]+b[0])/2 + B[0]/2, (a[1]+b[1])/2 + B[1]/2)
        gap = card_x(mid[1]) - mid[0]
        if -SHADOW < gap < SHADOW:                           # the card's shadow, just before it
            light *= 1 - 0.16 * (1 - max(0.0, gap) / SHADOW)
        quads.append(dict(i=i, depth=B[0]*(a[0]+b[0])/2 + B[1]*(a[1]+b[1])/2, facing=facing,
                          front=front, light=light, nz=abs(n[2]), k=ks[i] if i < len(ks) else 0.0))
    return quads, P, S, printed_sign


def overlaps(P):
    """Pairs of quads (not neighbours) that cover each other on screen."""
    from shapely.geometry import Polygon
    from shapely.strtree import STRtree
    polys = [Polygon([P[i], P[i+1], (P[i+1][0]+B[0], P[i+1][1]+B[1]), (P[i][0]+B[0], P[i][1]+B[1])])
             for i in range(len(P) - 1)]
    tree = STRtree(polys)
    pairs = []
    for i, p in enumerate(polys):
        for j in tree.query(p):
            j = int(j)
            if j > i + 1 and p.intersection(polys[j]).area > 0.01:
                pairs.append((i, j))
    return pairs


def stretches(quads, pairs):
    """Split the paper into stretches that face one way and can be painted whole, in an order
    that keeps nearer paper on top. Returns [(lo, hi)] in paint order."""
    n = len(quads)
    # far before near, for every pair that overlaps
    before = [(i, j) if quads[i]['depth'] > quads[j]['depth'] else (j, i) for i, j in pairs]

    def cyclic(owner):
        nodes = set(owner)
        graph = {v: set() for v in nodes}
        for a, b in before:
            if owner[a] != owner[b]:
                graph[owner[a]].add(owner[b])
        state = {}
        def visit(v):
            state[v] = 1
            for w in graph[v]:
                if state.get(w) == 1 or (w not in state and visit(w)):
                    return True
            state[v] = 2
            return False
        return any(v not in state and visit(v) for v in nodes)

    spans = []
    lo = 0
    for i in range(1, n + 1):
        if i < n and quads[i]['facing'] == quads[lo]['facing']:
            # would joining quad i to the current stretch force a painting cycle?
            owner = [None] * n
            for k, (a, b) in enumerate(spans):
                for t in range(a, b + 1):
                    owner[t] = k
            for t in range(lo, i + 1):
                owner[t] = 'cur'
            for t in range(i + 1, n):
                owner[t] = ('q', t)
            if not cyclic(owner):
                continue
        spans.append((lo, i - 1))
        lo = i

    # paint order: far to near where stretches overlap, otherwise along the paper
    owner = [None] * n
    for k, (a, b) in enumerate(spans):
        for t in range(a, b + 1):
            owner[t] = k
    after = {k: set() for k in range(len(spans))}
    for a, b in before:
        if owner[a] != owner[b]:
            after[owner[a]].add(owner[b])
    need = {k: 0 for k in after}
    for k in after:
        for m in after[k]:
            need[m] += 1
    order, ready = [], sorted(k for k in need if need[k] == 0)
    while ready:
        k = ready.pop(0)
        order.append(k)
        for m in sorted(after[k]):
            need[m] -= 1
            if need[m] == 0:
                ready.append(m)
                ready.sort()
    assert len(order) == len(spans)
    return [spans[k] for k in order]


def text_rows(quads, P, S, printed_sign):
    """Receipt lines that land on visible printed paper: (quads under it, transform, text, alpha)."""
    rows = []
    s = 6.0
    gen = receipt_lines()
    while s < S[-1]:
        text, after = next(gen)
        i = next(j for j in range(len(S) - 1) if S[j+1] > s)
        q = quads[i]
        here = s
        s += LEAD * after
        if not text.strip() or not q['front'] or q['nz'] < MIN_FACING or abs(q['k']) > MAX_BEND:
            continue
        # the paper must stay printable under the whole line height
        under = [j for j in range(len(S) - 1) if S[j+1] > here - CAP and S[j] < here + 0.3 * FONT]
        if any(not quads[j]['front'] or quads[j]['nz'] < MIN_FACING for j in under):
            continue
        k = (here - S[i]) / ((S[i+1] - S[i]) or 1)
        o = (P[i][0] + (P[i+1][0]-P[i][0])*k, P[i][1] + (P[i+1][1]-P[i][1])*k)
        ds = (S[i+1] - S[i]) or 1
        e2 = ((P[i+1][0]-P[i][0]) / ds, (P[i+1][1]-P[i][1]) / ds)    # along the paper, per paper px
        u = (-B[0] / W3, -B[1] / W3) if printed_sign > 0 else (B[0] / W3, B[1] / W3)
        start = o if printed_sign < 0 else (o[0] + B[0], o[1] + B[1])  # the u=0 edge of the print
        org = (start[0] + u[0] * MARGIN * W3, start[1] + u[1] * MARGIN * W3)
        if u[0]*e2[1] - u[1]*e2[0] <= 0:      # would read mirrored: we are behind the print
            continue
        alpha = min(1.0, (min(quads[j]['nz'] for j in under) - MIN_FACING) * 2.5)
        rows.append((under, (u[0], u[1], e2[0], e2[1], org[0], org[1]), text, max(0.25, round(alpha * 4) / 4)))
    return rows


def g(x):
    """A compact number: one decimal, no trailing zeros, no leading zero."""
    s = ('%.1f' % x).rstrip('0').rstrip('.')
    if s in ('', '-0'):
        return '0'
    return s.replace('0.', '.', 1) if s.startswith(('0.', '-0.')) else s


def g3(x):
    s = ('%.3f' % x).rstrip('0').rstrip('.')
    if s in ('', '-0'):
        return '0'
    return s.replace('0.', '.', 1) if s.startswith(('0.', '-0.')) else s


def rel(points):
    """Path data through points: an absolute move, then relative lines (rounded positions, so
    the rounding never accumulates)."""
    pts = [(round(x, 1), round(y, 1)) for x, y in points]
    out = 'M%s %s' % (g(pts[0][0]), g(pts[0][1]))
    nums = []
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        nums += [g(bx - ax), g(by - ay)]
    if nums:
        out += 'l' + nums[0]
        for t in nums[1:]:
            out += t if t.startswith('-') else ' ' + t
    return out


def colour(base, k):
    return '#%02x%02x%02x' % tuple(max(0, min(255, round(c * k))) for c in base)


def shade_stops(points, tol=0.0025):
    """Thin (offset, light) samples to the ones a linear gradient needs (1D Douglas-Peucker)."""
    keep = {0, len(points) - 1}
    def split(a, b):
        (oa, la), (ob, lb) = points[a], points[b]
        worst, at = 0.0, None
        for k in range(a + 1, b):
            o, l = points[k]
            t = (o - oa) / ((ob - oa) or 1e-9)
            d = abs(l - (la + (lb - la) * t))
            if d > worst:
                worst, at = d, k
        if at is not None and worst > tol:
            keep.add(at)
            split(a, at)
            split(at, b)
    split(0, len(points) - 1)
    return [points[k] for k in sorted(keep)]


def svg(quads, P, S, printed_sign):
    xs = [p[0] + d for p in P for d in (0, B[0])]
    ys = [p[1] + d for p in P for d in (0, B[1])]
    x0, y0 = math.floor(min(xs)) - 2, math.floor(min(ys)) - 2
    x1, y1 = math.ceil(max(xs)) + 2, math.ceil(max(ys)) + 2
    sh = lambda p: (p[0] - x0, p[1] - y0)
    last = len(P) - 2

    spans = stretches(quads, overlaps(P))
    span_at = {}
    for k, (lo, hi) in enumerate(spans):
        for t in range(lo, hi + 1):
            span_at[t] = k
    rows_after = {}
    for under, m, text, alpha in text_rows(quads, P, S, printed_sign):
        if len({span_at[j] for j in under}) == 1:
            rows_after.setdefault(span_at[under[0]], []).append((m, text, alpha))

    defs, out = [], []
    across = lambda p: p[0] * ACROSS[0] + p[1] * ACROSS[1]
    for k, (lo, hi) in enumerate(spans):
        base = PAPER if quads[lo]['front'] else BACK
        near = [P[t] for t in range(lo, hi + 2)]
        far = [(p[0] + B[0], p[1] + B[1]) for p in near]
        ring = [sh(p) for p in near + far[::-1]]
        # shade along the paper as a gradient across B: one sample per quad, at its middle
        t0, t1 = across(sh(near[0])), across(sh(near[-1]))
        samples = [(0.0, quads[lo]['light'])]
        for q in quads[lo:hi + 1]:
            mid = sh(((P[q['i']][0] + P[q['i'] + 1][0]) / 2, (P[q['i']][1] + P[q['i'] + 1][1]) / 2))
            samples.append(((across(mid) - t0) / ((t1 - t0) or 1e-9), q['light']))
        samples.append((1.0, quads[hi]['light']))
        stops = shade_stops(samples)
        if len({colour(base, l) for _, l in stops}) == 1:
            fill = colour(base, stops[0][1])
        else:
            a = sh(near[0])
            b = (a[0] + ACROSS[0] * (t1 - t0), a[1] + ACROSS[1] * (t1 - t0))
            defs.append('<linearGradient id="rib%d" gradientUnits="userSpaceOnUse" x1="%s" y1="%s" x2="%s" y2="%s">%s</linearGradient>' % (
                k, g(a[0]), g(a[1]), g(b[0]), g(b[1]),
                ''.join('<stop offset="%s" stop-color="%s"/>' % (g3(max(0, min(1, o))), colour(base, l)) for o, l in stops)))
            fill = 'url(#rib%d)' % k
        out.append('<path fill="%s" d="%sz"/>' % (fill, rel(ring)))
        # the long edges and the receipt's cut ends
        e = rel([sh(p) for p in near]) + rel([sh(p) for p in far])
        if lo == 0:
            e += rel([sh(near[0]), sh(far[0])])
        if hi == last:
            e += rel([sh(near[-1]), sh(far[-1])])
        out.append('<path class="rib-edge" d="%s"/>' % e)
        for m, text, alpha in rows_after.get(k, []):
            a_, b_, c_, d_, e_, f_ = m
            op = '' if alpha >= 1 else ' opacity="%s"' % g3(alpha)
            out.append('<text transform="matrix(%s %s %s %s %s %s)"%s>%s</text>' % (
                g3(a_), g3(b_), g3(c_), g3(d_), g(e_ - x0), g(f_ - y0), op, text.rstrip().replace(' ', '\u00a0')))
    w, h = x1 - x0, y1 - y0
    head = '<svg class="receipt-ribbon" viewBox="0 0 %d %d" font-size="%s" aria-hidden="true" focusable="false">' % (w, h, g3(FONT))
    return (x0, y0, w, h), head + '<defs>' + ''.join(defs) + '</defs>' + ''.join(out) + '</svg>', len(spans)


if __name__ == '__main__':
    quads, P, S, ps = build()
    box, markup, nspans = svg(quads, P, S, ps)
    print('box (shell px at 1440):', box, 'bytes:', len(markup), 'stretches:', nspans,
          'lines:', markup.count('<text'), 'font:', round(FONT, 3))
    if sys.argv[1:2] == ['--preview']:
        Path(sys.argv[2]).write_text(markup)
        sys.exit()
    page = SITE / 'index.html'
    s, n = re.subn(r'<svg class="receipt-ribbon".*?</svg>', lambda m: markup, page.read_text(), count=1, flags=re.S)
    assert n == 1
    page.write_text(s)
    x0, y0, w, h = box
    css = SITE / 'styles.css'
    rule = ('.receipt-ribbon { position: absolute; top: 0; left: %.3f%%; width: %.3f%%; margin-top: %.3f%%; '
            'height: auto; pointer-events: none; user-select: none; }' % (100 * x0 / SHELL, 100 * w / SHELL, 100 * y0 / SHELL))
    s, n = re.subn(r'\.receipt-ribbon \{ position: absolute; top: 0; [^}]*\}', lambda m: rule, css.read_text(), count=1)
    assert n == 1
    css.write_text(s)
    print(rule)
