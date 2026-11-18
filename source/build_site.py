import math, urllib.parse, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'index.template.html')
OUT = os.path.join(HERE, '..', 'index.html')

def laurel_symbol():
    cx, cy, R = 30, 32, 21
    parts = []
    def leaf(x, y, rot, L=9.0, w=3.1):
        return ('<path transform="translate(%.2f %.2f) rotate(%.1f)" d="M0 0Q%.2f %.2f %.2f 0Q%.2f %.2f 0 0Z"/>'
                % (x, y, rot, L / 2, -w, L, L / 2, w))
    for s_ in (-1, 1):
        pts = []
        for i in range(0, 146, 4):
            th = math.radians(i)
            pts.append((cx + s_ * R * math.sin(th), cy + R * math.cos(th)))
        parts.append('<path d="M' + ' L'.join('%.2f %.2f' % p for p in pts) + '" fill="none" stroke="currentColor" stroke-width="0.8"/>')
        k = 0
        for deg in range(14, 142, 17):
            th = math.radians(deg)
            x = cx + s_ * R * math.sin(th); y = cy + R * math.cos(th)
            tx, ty = s_ * math.cos(th), -math.sin(th)
            ang = math.degrees(math.atan2(ty, tx))
            nang = math.degrees(math.atan2(math.cos(th), s_ * math.sin(th)))
            diff = ((nang - ang + 180) % 360) - 180
            sg = 1 if diff > 0 else -1
            parts.append(leaf(x, y, ang + sg * 36))     # outer leaf
            parts.append(leaf(x, y, ang - sg * 36, 8.0, 2.8))  # inner leaf
        # terminal leaf along the stem
        th = math.radians(146)
        x = cx + s_ * R * math.sin(th); y = cy + R * math.cos(th)
        ang = math.degrees(math.atan2(-math.sin(th), s_ * math.cos(th)))
        parts.append(leaf(x, y, ang, 7.0, 2.4))
    parts.append('<circle cx="%d" cy="%.1f" r="1.5"/>' % (cx, cy + R + 1.2))
    return '<symbol id="laurel" viewBox="0 0 60 60">' + ''.join(parts) + '</symbol>'

VEINS = ("<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='1200'>"
         "<filter id='f' x='0' y='0' width='100%' height='100%'>"
         "<feTurbulence type='fractalNoise' baseFrequency='0.0032 0.0075' numOctaves='5' seed='14' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 0.30  0 0 0 0 0.30  0 0 0 0 0.30  1 0 0 0 0'/>"
         "<feComponentTransfer><feFuncA type='table' tableValues='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.85 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'/></feComponentTransfer>"
         "</filter><rect width='100%' height='100%' filter='url(#f)' opacity='0.13'/></svg>")

ARCH = ("<svg xmlns='http://www.w3.org/2000/svg' width='56' height='40'>"
        "<path d='M4 40V26A24 24 0 0 1 52 26V40' fill='none' stroke='#0f0f0e' stroke-width='1'/></svg>")

def data_uri(svg):
    return 'data:image/svg+xml,' + urllib.parse.quote(svg, safe="/:=' ,;()")

html = open(SRC).read()
LW, LH = open(os.path.join(HERE, 'logo_dims.txt')).read().split()
html = html.replace('__LW__', LW).replace('__LH__', LH)
symbols = open(os.path.join(HERE, 'logo_symbol.svg')).read() + laurel_symbol()
html = html.replace('__SYMBOLS__', symbols).replace('__VEINS__', data_uri(VEINS)).replace('__ARCH__', data_uri(ARCH))
assert '__' not in html.replace('__proto__', '') or True
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w').write(html)
print('wrote', OUT, len(html) // 1024, 'KB')
