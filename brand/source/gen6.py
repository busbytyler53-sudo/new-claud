"""Nove: clean wide-sans identity, nine-o'clock emblem, four line lockups. All text outlined."""
import json, os, sys
OUT = sys.argv[1]
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from svlib import run, bounds, F
HERE = os.path.dirname(os.path.abspath(__file__))

def arch(wght, wdth):
    return instantiateVariableFont(TTFont(os.path.join(F, "archivo.ttf")), {"wght": wght, "wdth": wdth})
AW = arch(600, 125); AWB = arch(700, 125); AR = arch(500, 112); AL = arch(400, 125)

def clock(cx, cy, r, sw):
    """Nine o'clock: ring, hour hand to 9, minute hand to 12."""
    return (f'<g fill="none" stroke="currentColor" stroke-width="{sw:.1f}" stroke-linecap="round">'
            f'<circle cx="{cx}" cy="{cy}" r="{r - sw / 2:.1f}"/>'
            f'<path d="M{cx - r * .5:.1f} {cy}H{cx}V{cy - r * .66:.1f}" stroke-linejoin="round"/></g>')

logos = {}
d, w = run(AW, "NOVE", 100, track=0.26)
b = bounds(AW, "NOVE", 100, track=0.26); ch = -b[1]
logos["wordmark"] = (w + 20, ch + 20, f'<path transform="translate(10 {ch + 10:.2f})" d="{d}"/>')

dn, _ = run(AWB, "N°9", 100, track=0.04)
bn = bounds(AWB, "N°9", 100, track=0.04)
logos["n9"] = (bn[2] - bn[0] + 20, -bn[1] + 20, f'<path transform="translate({10 - bn[0]:.2f} {10 - bn[1]:.2f})" d="{dn}"/>')

logos["clock"] = (200, 200, clock(100, 100, 96, 14))

# Lockup: clock + wordmark
r = ch * .62
logos["lockup"] = (10 + 2 * r + 46 + w + 10, ch + 20,
                   clock(10 + r, 10 + ch / 2, r, r * .15) + f'<path transform="translate({10 + 2 * r + 46:.1f} {ch + 10:.2f})" d="{d}"/>')

# Time stamp lockup: NOVE over 09:00 / 21:00 with rules
W = w + 20; mid = W / 2
dt, wt = run(AL, "09:00  /  21:00", 24, mid, ch + 10 + 54, track=0.3, anchor="middle")
gap = wt / 2 + 20; ry = ch + 10 + 45
logos["stamp"] = (W, ch + 10 + 66,
                  f'<path transform="translate(10 {ch + 10:.2f})" d="{d}"/><path d="{dt}"/>'
                  f'<rect x="10" y="{ry:.1f}" width="{mid - gap - 10:.1f}" height="2"/><rect x="{mid + gap:.1f}" y="{ry:.1f}" width="{mid - gap - 10:.1f}" height="2"/>')

# Line lockups: NOVE + line name, separated by a thin bar
for line in ("SPORT", "GIORNO", "SERA", "STRADA"):
    dl, wl = run(AL, line, 100 * .6, track=0.3)
    bl = bounds(AL, line, 60, track=0.3)
    x2 = 10 + w + 64
    body = (f'<path transform="translate(10 {ch + 10:.2f})" d="{d}"/>'
            f'<rect x="{10 + w + 40:.1f}" y="10" width="3" height="{ch:.1f}"/>'
            f'<path transform="translate({x2 + 22:.1f} {ch + 10:.2f})" d="{dl}"/>')
    logos["line-" + line.lower()] = (x2 + 22 + wl + 10, ch + 20, body)

# Woven label
dw, _ = run(AW, "NOVE", 38, 170, 74, track=0.3, anchor="middle")
ds, _ = run(AR, "09:00  /  21:00", 13, 170, 166, track=0.3, anchor="middle")
logos["label"] = (340, 190, f'<rect x="4" y="4" width="332" height="182" rx="10" fill="none" stroke="currentColor" stroke-width="4"/>'
                  f'<path d="{dw}"/>' + clock(170, 116, 22, 4.5) + f'<path d="{ds}"/>')

json.dump({"logos": {k: {"w": v[0], "h": v[1], "body": v[2]} for k, v in logos.items()}}, open(os.path.join(HERE, "nove.json"), "w"))
os.makedirs(os.path.join(OUT, "logos"), exist_ok=True)
for name, (w_, h_, body) in logos.items():
    for suf, fill in (("black", "#1F1F1D"), ("chalk", "#F1EFEA"), ("stone", "#8C877D")):
        open(os.path.join(OUT, "logos", f"nove-{name}-{suf}.svg"), "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_:g} {h_:g}" fill="{fill}" color="{fill}">{body}</svg>\n')
print("ok", {k: (round(v[0]), round(v[1])) for k, v in logos.items()})
