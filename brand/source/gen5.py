"""Tenure: clean wide-sans identity with a tally-mark emblem. All text outlined."""
import json, os, sys
OUT = sys.argv[1]
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from svlib import run, bounds, F
HERE = os.path.dirname(os.path.abspath(__file__))

def arch(wght, wdth):
    return instantiateVariableFont(TTFont(os.path.join(F, "archivo.ttf")), {"wght": wght, "wdth": wdth})
AW = arch(600, 125); AWB = arch(700, 125); AR = arch(500, 112)

def tally(x, y, h, sw=None):
    """Five-bar tally: four uprights and a diagonal. Top-left at (x, y), height h."""
    sw = sw or h * 0.11
    gap = h * 0.27
    bars = "".join(f'<line x1="{x + sw / 2 + i * gap:.1f}" y1="{y + sw / 2:.1f}" x2="{x + sw / 2 + i * gap:.1f}" y2="{y + h - sw / 2:.1f}"/>' for i in range(4))
    w = sw + 3 * gap
    diag = f'<line x1="{x - gap * .45:.1f}" y1="{y + h * .78:.1f}" x2="{x + w + gap * .45:.1f}" y2="{y + h * .22:.1f}"/>'
    return f'<g fill="none" stroke="currentColor" stroke-width="{sw:.1f}" stroke-linecap="round">{bars}{diag}</g>', w + gap * .9

logos = {}
d, w = run(AW, "TENURE", 100, track=0.2)
b = bounds(AW, "TENURE", 100, track=0.2); ch = -b[1]
logos["wordmark"] = (w + 20, ch + 20, f'<path transform="translate(10 {ch + 10:.2f})" d="{d}"/>')

dt, wt = run(AWB, "TNR.", 100, track=0.06)
bt = bounds(AWB, "TNR.", 100, track=0.06)
logos["tnr"] = (bt[2] - bt[0] + 20, -bt[1] + 20, f'<path transform="translate({10 - bt[0]:.2f} {10 - bt[1]:.2f})" d="{dt}"/>')

t, tw = tally(0, 0, 160)
logos["tally"] = (tw + 40, 200, f'<g transform="translate({20 + 160 * .27 * .45:.1f} 20)">{t}</g>')

t2, tw2 = tally(0, 0, ch)
off = ch * .27 * .45
logos["lockup"] = (10 + tw2 + 52 + w + 10, ch + 20,
                   f'<g transform="translate({10 + off:.1f} 10)">{t2}</g><path transform="translate({10 + tw2 + 52:.1f} {ch + 10:.2f})" d="{d}"/>')

# Woven / rubber label: TENURE, tally, serial line
dw, _ = run(AW, "TENURE", 34, 170, 70, track=0.24, anchor="middle")
ds, _ = run(AR, "YEAR 01   N° 0001", 13, 170, 166, track=0.3, anchor="middle")
t3, tw3 = tally(0, 0, 44)
body = (f'<rect x="4" y="4" width="332" height="182" rx="10" fill="none" stroke="currentColor" stroke-width="4"/>'
        f'<path d="{dw}"/><g transform="translate({170 - tw3 / 2 + 44 * .27 * .45:.1f} 92)">{t3}</g><path d="{ds}"/>')
logos["label"] = (340, 190, body)

json.dump({"logos": {k: {"w": v[0], "h": v[1], "body": v[2]} for k, v in logos.items()}}, open(os.path.join(HERE, "tenure.json"), "w"))
os.makedirs(os.path.join(OUT, "logos"), exist_ok=True)
for name, (w_, h_, body) in logos.items():
    for suf, fill in (("black", "#1F1F1D"), ("chalk", "#F1EFEA"), ("stone", "#8C877D")):
        open(os.path.join(OUT, "logos", f"tenure-{name}-{suf}.svg"), "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_:g} {h_:g}" fill="{fill}" color="{fill}">{body}</svg>\n')
print("ok", {k: (round(v[0]), round(v[1])) for k, v in logos.items()})
