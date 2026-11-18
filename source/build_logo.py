import math, os, subprocess
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, 'fonts', 'cormorant-garamond-latin-600-normal.woff')
OUT = os.path.join(HERE, '..', 'img')
WORK = HERE

OVERLAP = float(os.environ.get('OVERLAP', 5.0))   # how far W tucks into M
GAP_WE = float(os.environ.get('GAP_WE', 5.0))
SE = float(os.environ.get('SE', 1.22))            # horizontal stretch of the E arms

font = TTFont(FONT)
gs = font.getGlyphSet()
cmap = font.getBestCmap()
cap = font['OS/2'].sCapHeight
S = 100.0 / cap
fmt = lambda v: ('%.2f' % v).rstrip('0').rstrip('.')

def glyph(ch, sx=1.0, tx=0.0):
    g = gs[cmap[ord(ch)]]
    bp = BoundsPen(gs); g.draw(bp)
    xmin, ymin, xmax, ymax = bp.bounds
    pen = SVGPathPen(gs, ntos=fmt)
    g.draw(TransformPen(pen, (S * sx, 0, 0, -S, tx - xmin * S * sx, 100)))
    return pen.getCommands(), (xmax - xmin) * S * sx

# ---- M and W ----
SN, SV = 0.88, 0.88   # condense N and V toward classical Roman proportions
m_d, m_w = glyph('N', SN, 0.0)
w_d, w_w = glyph('V', SV, m_w - OVERLAP)
w_right = m_w - OVERLAP + w_w
print('N', round(m_w, 1), 'V', round(w_w, 1), 'V right', round(w_right, 1))

# ---- the Ionic column that forms the stem of the E ----
COL_X = w_right + GAP_WE          # left edge of the capital
CAP_W, SHAFT_X0, SHAFT_X1 = 53.0, 12.0, 41.0
ARM_END = 96.0                    # right edge of the top and bottom arms, relative to COL_X
top_arm = (0.0, 2.8)
bot_arm = (95.8, 100.0)
right = COL_X + ARM_END

def spiral(cx, cy, r0, r1, turns, flip):
    pts = []
    n = 90
    for i in range(n + 1):
        t = i / n
        a = t * turns * 2 * math.pi * (-1 if flip else 1)
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return 'M' + ' L'.join('%.2f %.2f' % p for p in pts)

def rect(x, y, w, h, rx=0):
    r = f' rx="{rx}"' if rx else ''
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}"{r}/>'

c = []
c.append(rect(0, 0, CAP_W, 3.3))   # abacus
# volutes (scrolls) at both ends, joined by the channel
for cx, flip in ((6.6, False), (CAP_W - 6.6, True)):
    c.append(f'<path d="{spiral(cx, 10.6, 5.3, 1.0, 2.2, flip)}" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"/>')
    c.append(f'<circle cx="{cx}" cy="10.6" r="1.2"/>')
c.append(rect(6.6, 4.0, CAP_W - 13.2, 2.0))                           # channel under the abacus
# egg-and-dart row
for i in range(6):
    c.append(f'<ellipse cx="{15.2 + i * 4.5:.2f}" cy="11.4" rx="1.7" ry="2.5"/>')
c.append(rect(12.5, 15.3, CAP_W - 25, 1.5))                           # echinus lip
c.append(rect(10.5, 17.6, CAP_W - 21, 2.0, 1))                        # neck ring
c.append(rect(11.2, 20.2, CAP_W - 22.4, 1.2, 0.6))
tor2_bottom = bot_arm[0] - 0.7
# fluted shaft: eight bars, seven flutes
n_bars, gap = 8, 1.05
bar_w = ((SHAFT_X1 - SHAFT_X0) - gap * (n_bars - 1)) / n_bars
for i in range(n_bars):
    c.append(rect(SHAFT_X0 + i * (bar_w + gap), 21.6, bar_w, tor2_bottom - 7.6 - 21.6 + 0.2))
c.append(rect(SHAFT_X1 - 0.2, 21.6, 1.4, tor2_bottom - 7.6 - 21.6 + 0.2))                       # solid edge where the arms join
# base: two tori, plinth
c.append(rect(10.5, tor2_bottom - 7.6, CAP_W - 21, 3.2, 1.5))
c.append(rect(8.2, tor2_bottom - 3.8, CAP_W - 16.4, 3.8, 1.8))
c.append(rect(5.2, bot_arm[0], CAP_W - 10.4, 100.0 - bot_arm[0] + max(0, bot_arm[1] - 100)))   # plinth, flush with the bottom arm

arms = (
    # top arm: hairline with a serif dropping at the end
    f'<path d="M{SHAFT_X1 - 1} 0H{ARM_END}V14.5H{ARM_END - 3.2}Q{ARM_END - 4} 8 {ARM_END - 7} {top_arm[1]}H{SHAFT_X1 - 1}Z"/>'
    # middle arm: shorter, with a small tick
    f'<path d="M{SHAFT_X1 - 1} 48.4H84.6V43.8H87.2V55.2H84.6V51.4H{SHAFT_X1 - 1}Z"/>'
    # bottom arm: heavier, serif rising at the end
    f'<path d="M{SHAFT_X1 - 1} 100H{ARM_END}V83.5H{ARM_END - 3.2}Q{ARM_END - 4} 91.5 {ARM_END - 7} {bot_arm[0]}H{SHAFT_X1 - 1}Z"/>'
)
column = f'<g transform="translate({COL_X:.2f} 0)">' + ''.join(c) + arms + '</g>'
clip = ''
inner = f'<path d="{m_d}"/><path d="{w_d}"/>{column}'
pad = 4
vb_w = right + 2 * pad
vb = f'{-pad} {-pad} {vb_w:.1f} {100 + 2 * pad}'
print('viewBox', vb)
open(f'{WORK}/logo_dims.txt', 'w').write(f'{vb_w:.1f} {100 + 2 * pad}')
open(f'{WORK}/logo_symbol.svg', 'w').write(f'<symbol id="nve-mark" viewBox="{vb}">{clip}{inner}</symbol>')

def standalone(fill, bg=None):
    h = 100 + 2 * pad
    bgrect = f'<rect x="{-pad}" y="{-pad}" width="{vb_w:.1f}" height="{h}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{vb_w * 4:.0f}" height="{h * 4}" '
            f'role="img" aria-label="NVE monogram"><title>NVE Wedding &amp; Event Planning monogram</title>'
            f'{bgrect}<g fill="{fill}" color="{fill}">{inner}</g></svg>')

os.makedirs(OUT, exist_ok=True)
open(f'{OUT}/nve-logo-black.svg', 'w').write(standalone('#111111'))
open(f'{OUT}/nve-logo-white.svg', 'w').write(standalone('#f4f3f1', '#111111'))
print('wrote logos')
