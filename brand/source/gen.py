"""Generate Sottovoce logo SVGs with text converted to outlines."""
import json, math, os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "fonts")
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

def inst(name, **axes):
    t = TTFont(os.path.join(F, name))
    if "fvar" in t:
        t = instantiateVariableFont(t, axes)
    return t

BOD = inst("bodoni.ttf", wght=500, opsz=96)
BOD_SM = inst("bodoni.ttf", wght=600, opsz=11)
BODI = inst("bodoni-it.ttf", wght=500, opsz=96)
COR = inst("cormorant.ttf", wght=600)
PIN = inst("pinyon.ttf")

def glyph(font, ch):
    return font.getBestCmap()[ord(ch)]

def run(font, text, size, x=0, y=0, track=0.0, anchor="start"):
    """Lay out text on a baseline. Returns (path_d, width)."""
    gs = font.getGlyphSet(); hm = font["hmtx"]; upm = font["head"].unitsPerEm
    s = size / upm
    names = [glyph(font, c) for c in text]
    adv = [hm[n][0] * s for n in names]
    width = sum(adv) + track * size * (len(text) - 1)
    if anchor == "middle": x -= width / 2
    elif anchor == "end": x -= width
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    cx = x
    for n, a in zip(names, adv):
        gs[n].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        cx += a + track * size
    return pen.getCommands(), width

def bounds(font, text, size, track=0.0):
    gs = font.getGlyphSet(); upm = font["head"].unitsPerEm; s = size / upm
    bp = BoundsPen(gs); cx = 0
    for c in text:
        n = glyph(font, c)
        gs[n].draw(TransformPen(bp, (s, 0, 0, -s, cx, 0)))
        cx += font["hmtx"][n][0] * s + track * size
    return bp.bounds  # xmin, ymin, xmax, ymax (y down)

def arc(font, text, size, r, cx, cy, center_deg, track=0.0, inside=False):
    """Text on a circle. center_deg: 0 = top. inside=True reads along the bottom."""
    gs = font.getGlyphSet(); hm = font["hmtx"]; upm = font["head"].unitsPerEm
    s = size / upm
    names = [glyph(font, c) for c in text]
    adv = [hm[n][0] * s + track * size for n in names]
    total = sum(adv) - track * size
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    pos = -total / 2
    for n, a in zip(names, adv):
        g_adv = hm[n][0] * s
        mid = pos + g_adv / 2
        if not inside:
            ang = math.radians(center_deg) + mid / r
            px, py = cx + r * math.sin(ang), cy - r * math.cos(ang)
            rot = ang
            t = (math.cos(rot), math.sin(rot), -math.sin(rot), math.cos(rot))
        else:
            ang = math.radians(center_deg) - mid / r
            px, py = cx + r * math.sin(ang), cy - r * math.cos(ang)
            rot = ang + math.pi
            t = (math.cos(rot), math.sin(rot), -math.sin(rot), math.cos(rot))
        a_, b_, c_, d_ = t
        # glyph local: x from -adv/2, baseline at 0, y flipped
        m = (a_ * s, b_ * s, c_ * -s, d_ * -s, 0, 0)
        ox, oy = -g_adv / 2, 0
        e = px + a_ * ox + c_ * oy
        f = py + b_ * ox + d_ * oy
        gs[n].draw(TransformPen(pen, (m[0], m[1], m[2], m[3], e, f)))
        pos += a
    return pen.getCommands()

def svg(w, h, body, fill):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" '
            f'fill="{fill}">{body}</svg>')

logos = {}

# 1. Primary wordmark
d1, w1 = run(BOD, "SOTTOVOCE", 100, track=0.16)
b = bounds(BOD, "SOTTOVOCE", 100, track=0.16)
cap_h = -b[1]
W = w1 + 40; mid = W / 2
d2, w2 = run(COR, "SOCIAL CLUB", 26, mid, cap_h + 20 + 52, track=0.42, anchor="middle")
rule_y = cap_h + 20 + 43
gap = w2 / 2 + 26
body = (f'<path transform="translate(20 {cap_h + 20:.2f})" d="{d1}"/>'
        f'<path d="{d2}"/>'
        f'<rect x="20" y="{rule_y:.2f}" width="{mid - gap - 20:.2f}" height="1.6"/>'
        f'<rect x="{mid + gap:.2f}" y="{rule_y:.2f}" width="{mid - gap - 20:.2f}" height="1.6"/>')
logos["wordmark"] = (W, cap_h + 20 + 52 + 22, body)

# 2. Short mark: S.V.C
dS, wS = run(BOD, "S", 100); dV, wV = run(BOD, "V", 100); dC, wC = run(BOD, "C", 100)
bS = bounds(BOD, "SVC", 100); ch = -bS[1]
dot = 7; gp = 26
x = 10; parts = []
for dd, ww, last in ((dS, wS, False), (dV, wV, False), (dC, wC, True)):
    parts.append(f'<path transform="translate({x:.2f} {ch + 10:.2f})" d="{dd}"/>')
    x += ww
    if not last:
        parts.append(f'<circle cx="{x + gp / 2:.2f}" cy="{ch + 10 - dot:.2f}" r="{dot:.2f}"/>')
        x += gp
logos["svc"] = (x + 10, ch + 22, "".join(parts))

# 3. Monogram: roman V with italic S woven through it
dVm, wVm = run(BOD, "V", 300, 150, 0, anchor="middle")
bV = bounds(BOD, "V", 300)
Vh = -bV[1]
dSm, wSm = run(BODI, "S", 230, 150, 0, anchor="middle")
bSm = bounds(BODI, "S", 230)
Sh = -bSm[1]
sy = (Vh - Sh) / 2 + Sh
body = (f'<defs><mask id="m-knock" maskUnits="userSpaceOnUse" x="0" y="0" width="300" height="{Vh + 40:.0f}">'
        f'<rect width="300" height="{Vh + 40:.0f}" fill="#fff"/>'
        f'<path transform="translate(0 {sy + 20:.2f})" d="{dSm}" fill="none" stroke="#000" stroke-width="14" stroke-linejoin="round"/>'
        f'</mask></defs>'
        f'<g mask="url(#m-knock)"><path transform="translate(0 {Vh + 20:.2f})" d="{dVm}"/></g>'
        f'<path transform="translate(0 {sy + 20:.2f})" d="{dSm}"/>')
logos["monogram"] = (300, Vh + 40, body)

# 4. Crest
R = 250; C = 260
TOP, BOT = "SOTTOVOCE \u00b7 SOCIAL CLUB", "SAID QUIETLY"
top = arc(COR, TOP, 34, R - 52, C, C, 0, track=0.24)
bot = arc(COR, BOT, 28, R - 30, C, C, 180, track=0.34, inside=True)
top_half = math.degrees(run(COR, TOP, 34, track=0.24)[1] / (R - 52) / 2)
bot_half = math.degrees(run(COR, BOT, 28, track=0.34)[1] / (R - 30) / 2)
dot_ang = (top_half + (180 - bot_half)) / 2
d_star = ""
for ang in (-90 - 52, -90 + 52):  # dots between top & bottom text, left/right
    pass
mono_scale = 0.7
mono = logos["monogram"]
mw, mh = mono[0] * mono_scale, mono[1] * mono_scale
dEst, wEst = run(BOD_SM, "MMXXVI", 17, C, C + mh / 2 + 34, track=0.5, anchor="middle")
dots = "".join(
    f'<circle cx="{C + (R - 40) * math.sin(math.radians(a)):.2f}" cy="{C - (R - 40) * math.cos(math.radians(a)):.2f}" r="4.5"/>'
    for a in (-dot_ang, dot_ang))
body = (f'<circle cx="{C}" cy="{C}" r="{R}" fill="none" stroke="currentColor" stroke-width="5"/>'
        f'<circle cx="{C}" cy="{C}" r="{R - 12}" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        f'<circle cx="{C}" cy="{C}" r="{R - 104}" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        f'<path d="{top}"/><path d="{bot}"/>{dots}'
        f'<g transform="translate({C - mw / 2:.2f} {C - mh / 2 - 8:.2f}) scale({mono_scale})">{mono[2].replace("m-knock", "m-knock-c")}</g>'
        f'<path d="{dEst}"/>')
logos["crest"] = (2 * C, 2 * C, body)

# 5. Script chest mark
dP, wP = run(PIN, "Sottovoce", 150)
bP = bounds(PIN, "Sottovoce", 150)
asc = -bP[1]; desc = bP[3]
W5 = (bP[2] - bP[0]) + 40
ox = 20 - bP[0]
dSub, wSub = run(COR, "SOCIAL CLUB", 22, ox + (bP[0] + bP[2]) / 2 + 30, asc + 20 + desc + 36, track=0.5, anchor="middle")
body = f'<path transform="translate({ox:.2f} {asc + 20:.2f})" d="{dP}"/><path d="{dSub}"/>'
logos["script"] = (W5 + 30, asc + 20 + desc + 50, body)

with open(os.path.join(HERE, "logos.json"), "w") as fh:
    json.dump({k: {"w": v[0], "h": v[1], "body": v[2]} for k, v in logos.items()}, fh)

for name, (w, h, body) in logos.items():
    for suffix, fill in (("green", "#1F3A2E"), ("ecru", "#EDE6D6"), ("black", "#141414")):
        b2 = body.replace('stroke="currentColor"', f'stroke="{fill}"')
        with open(os.path.join(OUT, f"sottovoce-{name}-{suffix}.svg"), "w") as fh:
            fh.write(svg(w, h, b2, fill) + "\n")
print("ok", {k: (round(v[0]), round(v[1])) for k, v in logos.items()})
