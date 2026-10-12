"""Solano: logos and tropical drop graphics, all text outlined."""
import json, math, os, sys
sys.argv = sys.argv[:1] + sys.argv[1:]
OUT = sys.argv[1]
from svlib import run, bounds, BOD, BODI, COR, PIN, BOD_SM

os.makedirs(OUT, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
f2 = lambda v: f"{v:.1f}"

logos = {}

# Wordmark
d, w = run(BOD, "SOLANO", 100, track=0.24)
b = bounds(BOD, "SOLANO", 100, track=0.24); ch = -b[1]
logos["wordmark"] = (w + 20, ch + 20, f'<path transform="translate(10 {ch + 10:.2f})" d="{d}"/>')

# Lockup: wordmark + rule + EST line
W = w + 20; mid = W / 2
de, we = run(COR, "EST. MMXXVI", 22, mid, ch + 10 + 56, track=0.5, anchor="middle")
gap = we / 2 + 22; ry = ch + 10 + 48
body = (f'<path transform="translate(10 {ch + 10:.2f})" d="{d}"/><path d="{de}"/>'
        f'<rect x="10" y="{ry:.2f}" width="{mid - gap - 10:.2f}" height="1.4"/>'
        f'<rect x="{mid + gap:.2f}" y="{ry:.2f}" width="{mid - gap - 10:.2f}" height="1.4"/>')
logos["lockup"] = (W, ch + 10 + 70, body)

# Sol. short mark
ds, ws = run(BODI, "Sol.", 120)
bs = bounds(BODI, "Sol.", 120)
logos["sol"] = (bs[2] - bs[0] + 20, bs[3] - bs[1] + 20,
                f'<path transform="translate({10 - bs[0]:.2f} {10 - bs[1]:.2f})" d="{ds}"/>')

# Sun monogram: italic S inside a ring
dS, _ = run(BODI, "S", 210)
bS = bounds(BODI, "S", 210)
body = (f'<circle cx="150" cy="150" r="138" fill="none" stroke="currentColor" stroke-width="5"/>'
        f'<path transform="translate({150 - (bS[0] + bS[2]) / 2:.2f} {150 - (bS[1] + bS[3]) / 2:.2f})" d="{dS}"/>')
logos["sun"] = (300, 300, body)

# Script chest mark
dP, _ = run(PIN, "Solano", 150)
bP = bounds(PIN, "Solano", 150)
logos["script"] = (bP[2] - bP[0] + 40, bP[3] - bP[1] + 40,
                   f'<path transform="translate({20 - bP[0]:.2f} {20 - bP[1]:.2f})" d="{dP}"/>')

# ---------- tropical drop graphics ----------
def rot(x, y, a):
    c, s = math.cos(a), math.sin(a)
    return x * c - y * s, x * s + y * c

def leaflet(px, py, ang, L, wd):
    tx, ty = px + L * math.cos(ang), py + L * math.sin(ang)
    mx, my = (px + tx) / 2, (py + ty) / 2
    nx, ny = -math.sin(ang) * wd, math.cos(ang) * wd
    return (f"M{f2(px)} {f2(py)}Q{f2(mx + nx)} {f2(my + ny)} {f2(tx)} {f2(ty)}"
            f"Q{f2(mx - nx * .4)} {f2(my - ny * .4)} {f2(px)} {f2(py)}Z")

def frond(bx, by, ang, L, droop, n=12, lf=46):
    a2 = ang + droop
    cx, cy = bx + L * .55 * math.cos(ang), by + L * .55 * math.sin(ang)
    tx, ty = bx + L * math.cos(a2), by + L * math.sin(a2)
    parts = [f'<path d="M{f2(bx)} {f2(by)}Q{f2(cx)} {f2(cy)} {f2(tx)} {f2(ty)}" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>']
    d = ""
    for i in range(n):
        t = .12 + .86 * i / (n - 1)
        px = (1 - t) ** 2 * bx + 2 * (1 - t) * t * cx + t * t * tx
        py = (1 - t) ** 2 * by + 2 * (1 - t) * t * cy + t * t * ty
        dx = 2 * (1 - t) * (cx - bx) + 2 * t * (tx - cx)
        dy = 2 * (1 - t) * (cy - by) + 2 * t * (ty - cy)
        ta = math.atan2(dy, dx)
        ln = lf * (0.35 + 0.9 * math.sin(math.pi * min(t * 1.15, 1))) * (1 - t * .35)
        for side in (1, -1):
            d += leaflet(px, py, ta + side * 0.95 + 0.25 * side * t, ln, 5)
    parts.append(f'<path d="{d}"/>')
    return "".join(parts)

def palm(x, y, h, lean, scale=1.0):
    # tapered curved trunk from (x,y) base to crown
    topx, topy = x + lean, y - h
    cx, cy = x + lean * .15, y - h * .5
    pts_l, pts_r, rings = [], [], []
    for i in range(21):
        t = i / 20
        px = (1 - t) ** 2 * x + 2 * (1 - t) * t * cx + t * t * topx
        py = (1 - t) ** 2 * y + 2 * (1 - t) * t * cy + t * t * topy
        wd = (9 - 4 * t) * scale
        pts_l.append((px - wd, py)); pts_r.append((px + wd, py))
        if 0 < i < 20 and i % 2 == 0:
            rings.append(f"M{f2(px - wd)} {f2(py)}Q{f2(px)} {f2(py + 3)} {f2(px + wd)} {f2(py)}")
    trunk = "M" + "L".join(f"{f2(a)} {f2(b)}" for a, b in pts_l) + "L" + "L".join(f"{f2(a)} {f2(b)}" for a, b in reversed(pts_r)) + "Z"
    out = [f'<path d="{trunk}"/>',
           f'<path d="{"".join(rings)}" fill="none" stroke="var(--bg)" stroke-width="1.4" opacity=".55"/>']
    for a, L, dr in ((-172, 118, -42), (-138, 128, -30), (-96, 100, -12), (-48, 128, 30), (-8, 118, 44)):
        out.append(frond(topx, topy, math.radians(a), L * scale, math.radians(dr) * -1 if a < -90 else math.radians(dr), lf=30 * scale))
    out.append(f'<circle cx="{f2(topx)}" cy="{f2(topy)}" r="{6 * scale:.1f}"/>')
    return "".join(out)

def caption(title, sub, y):
    d1, _ = run(BOD_SM, "SOLANO", 24, 200, y, track=0.42, anchor="middle")
    d2, _ = run(PIN, title, 44, 200, y + 54, anchor="middle")
    d3, _ = run(COR, sub, 15, 200, y + 84, track=0.4, anchor="middle")
    return f'<path d="{d1}"/><path d="{d2}"/><path d="{d3}"/>'

def g_palma():
    sun = '<circle cx="200" cy="210" r="118" fill="var(--a1)"/>'
    sea = "".join(f'<rect x="{82 + i * 6}" y="{262 + i * 14}" width="{236 - i * 12}" height="{5 - i * .6:.1f}" fill="var(--bg)"/>' for i in range(5))
    trees = f'<g fill="var(--ink)" color="var(--ink)">{palm(160, 340, 200, 36)}{palm(268, 340, 140, -14, .75)}</g>'
    ground = '<path d="M60 340Q200 326 340 340L340 346Q200 334 60 346Z" fill="var(--ink)"/>'
    return f'{sun}{sea}{trees}{ground}<g fill="var(--ink)">{caption("Palma", "DROP 02 · RIVIERA", 392)}</g>'

LEMON = "M-46 0C-40 -6 -36 -28 0 -28C36 -28 40 -6 46 0C40 6 36 28 0 28C-36 28 -40 6 -46 0Z"
def leaf(x, y, ang, L, wd):
    a = math.radians(ang)
    tx, ty = x + L * math.cos(a), y + L * math.sin(a)
    mx, my = (x + tx) / 2, (y + ty) / 2
    nx, ny = -math.sin(a) * wd, math.cos(a) * wd
    return (f'<path d="M{f2(x)} {f2(y)}Q{f2(mx + nx)} {f2(my + ny)} {f2(tx)} {f2(ty)}Q{f2(mx - nx)} {f2(my - ny)} {f2(x)} {f2(y)}Z" fill="var(--a2)"/>'
            f'<path d="M{f2(x)} {f2(y)}L{f2(tx)} {f2(ty)}" stroke="var(--ink)" stroke-width="1.6" opacity=".5"/>')

def lemon(x, y, ang, s=1):
    return (f'<g transform="translate({x} {y}) rotate({ang}) scale({s})">'
            f'<path d="{LEMON}" fill="var(--a1)"/>'
            f'<path d="{LEMON}" fill="none" stroke="var(--ink)" stroke-width="2"/>'
            f'<ellipse cx="-12" cy="-12" rx="14" ry="5" fill="var(--bg)" opacity=".55"/></g>')

def g_limoni():
    branch = '<path d="M70 120Q200 70 330 150" fill="none" stroke="var(--ink)" stroke-width="5" stroke-linecap="round"/>'
    leaves = "".join(leaf(*a) for a in (
        (110, 103, -150, 70, 18), (140, 95, -60, 80, 20), (190, 86, -110, 85, 22), (230, 90, -30, 80, 20),
        (270, 108, -80, 70, 18), (300, 128, 20, 70, 18), (160, 92, 160, 60, 16), (250, 100, 200, 60, 16)))
    stems = ('<path d="M150 96L140 170M215 88L222 205M285 118L300 180" fill="none" stroke="var(--ink)" stroke-width="3"/>')
    fruit = lemon(140, 200, 80, 1.05) + lemon(224, 240, 96, 1.2) + lemon(300, 208, 70, .95)
    return f'{stems}{branch}{leaves}{fruit}<g fill="var(--ink)">{caption("Limoni", "DROP 01 · AMALFI", 392)}</g>'

PETAL = "M0 0C-46 -18 -60 -92 -18 -112C-6 -118 6 -116 14 -112C58 -94 46 -20 0 0Z"
def g_ibisco():
    lv = leaf(200, 205, 200, 185, 42) + leaf(200, 205, -20, 185, 42) + leaf(200, 205, 125, 160, 34)
    petals = "".join(f'<path transform="translate(200 200) rotate({i * 72 + 8})" d="{PETAL}" fill="var(--a1)" stroke="var(--ink)" stroke-width="2"/>' for i in range(5))
    veins = "".join(f'<path transform="translate(200 200) rotate({i * 72 + 8 + o})" d="M0 -8L0 -78" stroke="var(--a3)" stroke-width="2" opacity=".7"/>' for i in range(5) for o in (-10, 0, 10))
    eye = '<circle cx="200" cy="200" r="26" fill="var(--a3)"/>'
    stamen = ('<path d="M200 200Q236 170 252 120" fill="none" stroke="var(--a3)" stroke-width="5" stroke-linecap="round"/>' +
              "".join(f'<circle cx="{252 + dx}" cy="{120 + dy}" r="5.5" fill="var(--a2)" stroke="var(--ink)" stroke-width="1.5"/>' for dx, dy in ((0, -6), (-9, 2), (9, 2), (-4, 10), (6, 11))))
    return f'{lv}{petals}{veins}{eye}{stamen}<g fill="var(--ink)">{caption("Ibisco", "DROP 03 · ISOLE", 392)}</g>'

graphics = {"palma": g_palma(), "limoni": g_limoni(), "ibisco": g_ibisco()}
COLORWAYS = {
    "palma":  {"--bg": "#EDE6D6", "--ink": "#1F3A2E", "--a1": "#E39B5B", "--a2": "#1F3A2E", "--a3": "#1F3A2E"},
    "limoni": {"--bg": "#F5F1E6", "--ink": "#1F3A2E", "--a1": "#EBC944", "--a2": "#4F7A4A", "--a3": "#1F3A2E"},
    "ibisco": {"--bg": "#EDE6D6", "--ink": "#1F3A2E", "--a1": "#E0664F", "--a2": "#4F7A4A", "--a3": "#8E2433"},
}

json.dump({"logos": {k: {"w": v[0], "h": v[1], "body": v[2]} for k, v in logos.items()},
           "graphics": graphics, "colorways": COLORWAYS},
          open(os.path.join(HERE, "solano.json"), "w"))

def colorize(body, cw):
    for k, v in cw.items():
        body = body.replace(f"var({k})", v)
    return body

def svg(w, h, body, fill, style=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" fill="{fill}" color="{fill}"{style}>{body}</svg>\n'

os.makedirs(os.path.join(OUT, "logos"), exist_ok=True); os.makedirs(os.path.join(OUT, "drops"), exist_ok=True)
for name, (w, h, body) in logos.items():
    for suf, fill in (("green", "#1F3A2E"), ("ecru", "#EDE6D6"), ("black", "#141414")):
        open(os.path.join(OUT, "logos", f"solano-{name}-{suf}.svg"), "w").write(svg(w, h, body, fill))
for name, body in graphics.items():
    cw = COLORWAYS[name]
    open(os.path.join(OUT, "drops", f"solano-{name}-print.svg"), "w").write(svg(400, 490, colorize(body, cw), cw["--ink"]))
print("ok", {k: (round(v[0]), round(v[1])) for k, v in logos.items()})
