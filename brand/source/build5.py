import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(HERE, "tenure.json")))
L = J["logos"]

def tone(hexc, amt):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    t = 0 if amt < 0 else 255; a = abs(amt)
    return "#" + "".join(f"{round(c + (t - c) * a):02X}" for c in (r, g, b))

NEUTRALS = {"chalk": "#F1EFEA", "oat": "#DDD5C6", "stone": "#B5B0A6", "moss": "#8F9580", "slate": "#3E4650", "black": "#1F1F1D"}
T = {k: {"bg": v, "ink": tone(v, .3 if k in ("slate", "black") else -.3)} for k, v in NEUTRALS.items()}

def colorize(body, cw):
    for k, v in cw.items():
        body = body.replace(f"var({k})", v)
    return body

def logo(name, cls="", label=""):
    l = L[name]
    return (f'<svg class="logo {cls}" viewBox="0 0 {l["w"]:g} {l["h"]:g}" fill="currentColor" '
            f'role="img" aria-label="{label or "Tenure " + name}">{l["body"]}</svg>')

def placed(name, x, y, w, color):
    l = L[name]; h = w * l["h"] / l["w"]
    return (f'<svg x="{x - w / 2:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'viewBox="0 0 {l["w"]:g} {l["h"]:g}" fill="{color}" color="{color}">{l["body"]}</svg>')

def placed_print(name, x, y, w):
    h = w * 490 / 400
    return (f'<svg x="{x - w / 2:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" viewBox="0 0 400 490">'
            f'{colorize(G[name], CW[name])}</svg>')

# boxy, dropped-shoulder tee
TEE = "M140 30 Q200 62 260 30 L358 62 L392 176 L330 190 L318 150 L318 404 Q200 410 82 404 L82 150 L70 190 L8 176 L42 62 Z"
FRONT_COLLAR = "M140 30 Q200 62 260 30 Q200 50 140 30 Z"
BACK_COLLAR = "M140 30 Q200 44 260 30 Q200 38 140 30 Z"

def tee(fill, ink, inner, back=False):
    return (f'<svg viewBox="0 0 400 420" class="mock" aria-hidden="true">'
            f'<path d="{TEE}" fill="{fill}"/>'
            f'<path d="{BACK_COLLAR if back else FRONT_COLLAR}" fill="{ink}" opacity=".22"/>'
            f'<path d="M82 150 L82 404 M318 150 L318 404 M42 62 L82 150 M358 62 L318 150" stroke="{ink}" stroke-opacity=".14" stroke-width="2"/>'
            f'{inner}</svg>')

def cap(fill, ink):
    return (f'<svg viewBox="0 0 400 420" class="mock" aria-hidden="true">'
            f'<path d="M70 250 Q66 96 200 92 Q334 96 330 250 Z" fill="{fill}"/>'
            f'<path d="M200 92 L200 250 M134 104 Q120 180 124 250 M266 104 Q280 180 276 250" fill="none" stroke="{ink}" stroke-opacity=".18" stroke-width="2"/>'
            f'<circle cx="200" cy="94" r="7" fill="{fill}" stroke="{ink}" stroke-opacity=".3"/>'
            f'<path d="M48 250 Q200 214 352 250 Q370 300 200 318 Q30 300 48 250 Z" fill="{fill}"/>'
            f'<path d="M48 250 Q200 214 352 250" fill="none" stroke="{ink}" stroke-opacity=".3" stroke-width="2"/>'
            f'{placed("tally", 200, 132, 64, ink)}</svg>')

def patch_on(fill, ink):
    return (f'<svg viewBox="0 0 400 420" class="mock" aria-hidden="true">'
            f'<rect x="0" y="0" width="400" height="420" fill="{fill}"/>'
            f'<path d="M0 70 Q200 130 400 70" fill="none" stroke="{ink}" stroke-opacity=".25" stroke-width="3"/>'
            f'<rect x="80" y="160" width="240" height="135" rx="20" fill="{ink}" opacity=".16"/>'
            f'{placed("label", 200, 160, 240, ink)}</svg>')

NAMES = {"chalk": ("Chalk", "Off white"), "oat": ("Oat", "Warm beige"), "stone": ("Stone", "Mid grey"),
         "moss": ("Moss", "Grey green"), "slate": ("Slate", "Blue grey"), "black": ("Black", "Washed")}

blanks_html = "\n".join(
    f'<figure class="blank"><div class="ground">{tee(t["bg"], t["ink"], placed("wordmark", 200, 106, 92, t["ink"]))}</div>'
    f'<figcaption><span>{NAMES[k][0]}</span><span class="dim">{NAMES[k][1]}</span></figcaption></figure>'
    for k, t in T.items())

details = [
    (cap(T["oat"]["bg"], T["oat"]["ink"]), "Cap", "Washed twill, tonal tally"),
    (patch_on(T["black"]["bg"], T["black"]["ink"]), "Year label", "Inside every piece, numbered"),
    (tee(T["stone"]["bg"], T["stone"]["ink"], placed("tnr", 200, 70, 110, T["stone"]["ink"]), back=True), "Back neck", "TNR. under the collar"),
]
details_html = "\n".join(
    f'<figure class="blank"><div class="ground">{s}</div><figcaption><span>{t}</span><span class="dim">{d}</span></figcaption></figure>'
    for s, t, d in details)

suite = [("wordmark", "Tenure", "The full name. Chest, site, shop front."), ("lockup", "Lockup", "Packaging, hang tags, socials."),
         ("tnr", "TNR.", "Short name. Back neck, sleeve, handle."), ("tally", "The tally", "The emblem. Caps, socks, buttons."),
         ("label", "Year label", "Inside every garment.")]
suite_html = "\n".join(
    f'<figure class="mark m-{n}"><div class="mark-art">{logo(n)}</div><figcaption><span>{t}</span><span class="dim">{d}</span></figcaption></figure>'
    for n, t, d in suite)

swatch_html = "\n".join(
    f'<div class="sw"><div class="chip" style="background:{t["bg"]}"><span style="color:{t["ink"]}">TENURE</span></div>'
    f'<span>{NAMES[k][0]}</span><span class="dim">{t["bg"]}</span></div>' for k, t in T.items())

page = open(os.path.join(HERE, "page5.tpl.html")).read()
for k, v in {"HERO": logo("lockup", "hero-mark", "Tenure"), "SWALLOW": logo("tally", "foot-mark"),
             "BLANKS": blanks_html, "DETAILS": details_html, "SUITE": suite_html, "LABEL": logo("label", "big-label"),
             "SWATCHES": swatch_html}.items():
    page = page.replace("{{" + k + "}}", v)
open(sys.argv[1], "w").write(page)
print("built", len(page))
