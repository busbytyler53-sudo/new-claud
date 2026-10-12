"""Generate Sottovoce logo SVGs with text converted to outlines."""
import json, math, os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "fonts")
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
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

