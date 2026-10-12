import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(HERE, "solano.json")))
L, G, CW = J["logos"], J["graphics"], J["colorways"]

def colorize(body, cw):
    for k, v in cw.items():
        body = body.replace(f"var({k})", v)
    return body

def logo(name, cls="", label=""):
    l = L[name]
    return (f'<svg class="logo {cls}" viewBox="0 0 {l["w"]:g} {l["h"]:g}" fill="currentColor" '
            f'role="img" aria-label="{label or "Solano " + name}">{l["body"]}</svg>')

def placed(name, x, y, w, color):
    l = L[name]; h = w * l["h"] / l["w"]
    return (f'<svg x="{x - w / 2:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'viewBox="0 0 {l["w"]:g} {l["h"]:g}" fill="{color}" color="{color}">{l["body"]}</svg>')

def placed_print(name, x, y, w):
    h = w * 490 / 400
    return (f'<svg x="{x - w / 2:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" viewBox="0 0 400 490">'
            f'{colorize(G[name], CW[name])}</svg>')

TEE = "M138 34 Q200 70 262 34 L352 74 L384 150 L326 172 L314 150 L314 404 Q200 414 86 404 L86 150 L74 172 L16 150 L48 74 Z"
BACK_COLLAR = "M138 34 Q200 50 262 34 Q200 44 138 34 Z"
FRONT_COLLAR = "M138 34 Q200 70 262 34 Q200 56 138 34 Z"

def tee(fill, ink, inner, back=False):
    return (f'<svg viewBox="0 0 400 420" class="mock" aria-hidden="true">'
            f'<path d="{TEE}" fill="{fill}" stroke="{ink}" stroke-opacity=".08" stroke-width="2"/>'
            f'<path d="{BACK_COLLAR if back else FRONT_COLLAR}" fill="{ink}" opacity=".16"/>'
            f'<path d="M86 150 L86 404 M314 150 L314 404" stroke="{ink}" stroke-opacity=".1" stroke-width="2"/>'
            f'{inner}</svg>')

def cap(fill, ink):
    return (f'<svg viewBox="0 0 400 420" class="mock" aria-hidden="true">'
            f'<path d="M70 250 Q66 96 200 92 Q334 96 330 250 Z" fill="{fill}"/>'
            f'<path d="M200 92 L200 250" stroke="{ink}" stroke-opacity=".14" stroke-width="2"/>'
            f'<path d="M134 104 Q120 180 124 250 M266 104 Q280 180 276 250" fill="none" stroke="{ink}" stroke-opacity=".1" stroke-width="2"/>'
            f'<circle cx="200" cy="94" r="7" fill="{fill}" stroke="{ink}" stroke-opacity=".2"/>'
            f'<path d="M48 250 Q200 214 352 250 Q370 300 200 318 Q30 300 48 250 Z" fill="{fill}"/>'
            f'<path d="M48 250 Q200 214 352 250" fill="none" stroke="{ink}" stroke-opacity=".22" stroke-width="2"/>'
            f'{placed("sun", 200, 136, 70, ink)}</svg>')

def label(fill, ink):
    return (f'<svg viewBox="0 0 400 420" class="mock" aria-hidden="true">'
            f'<rect x="60" y="160" width="280" height="100" fill="{fill}"/>'
            f'<rect x="72" y="172" width="256" height="76" fill="none" stroke="{ink}" stroke-opacity=".35" stroke-dasharray="3 4"/>'
            f'{placed("lockup", 200, 186, 190, ink)}</svg>')

GREEN, ECRU, INK, WHITE = "#1F3A2E", "#EDE6D6", "#141414", "#F7F5EF"

core = [
    (tee(WHITE, GREEN, placed("script", 252, 102, 74, GREEN)), "The white tee", "Script mark, left chest, tonal green thread"),
    (tee(GREEN, ECRU, placed("wordmark", 200, 112, 120, ECRU)), "Bottle green crewneck", "Wordmark, centre chest, 12cm wide"),
    (cap(ECRU, GREEN), "Ecru six-panel", "Sun monogram, front"),
    (label(GREEN, ECRU), "Woven neck label", "Lockup, every garment"),
]
core_html = "\n".join(
    f'<figure class="mock-card"><div class="mock-ground">{s}</div>'
    f'<figcaption><span class="cap-t">{t}</span><span class="cap-s">{d}</span></figcaption></figure>'
    for s, t, d in core)

drops = [
    ("limoni", "01", "Limoni", "Amalfi", "Lemon yellow and leaf green on a washed white tee. The opener: easy to wear, and the one that sells through first.",
     WHITE),
    ("palma", "02", "Palma", "Riviera", "Two palms against a low sun, in bottle green and apricot on ecru. The one people screenshot.",
     ECRU),
    ("ibisco", "03", "Ibisco", "Isole", "A hibiscus in coral and deep red on ecru. Late summer, a little louder, cut slightly boxier.",
     ECRU),
]
drops_html = "\n".join(
    f'<article class="drop"><div class="drop-pair">'
    f'<div class="mock-ground">{tee(bg, GREEN, placed("sol", 252, 100, 48, GREEN))}</div>'
    f'<div class="mock-ground">{tee(bg, GREEN, placed_print(k, 200, 66, 176), back=True)}</div></div>'
    f'<div class="drop-text"><p class="drop-no">Drop {n} · {place}</p><h3>{name}</h3><p>{desc}</p>'
    f'<p class="cap-s">Front: Sol. on the chest. Back: full print, 28cm wide.</p></div></article>'
    for k, n, name, place, desc, bg in drops)

suite = [
    ("wordmark", "Wordmark", "The brand at its plainest. Labels, the shop, the website, centre chest on knitwear.", "wide", False),
    ("script", "Script", "Small on the left chest of the core tees. This is the logo people clock across a bar.", "wide", True),
    ("sol", "Sol.", "The short name. Front of every drop tee, sleeve hits, the Instagram handle.", "", False),
    ("sun", "Sun monogram", "An S inside a ring: the sun, and the stamp. Caps, buttons, packaging seals.", "", True),
    ("lockup", "Lockup", "Wordmark with the founding year. Neck labels, hang tags, the lookbook cover.", "", False),
]
suite_html = "\n".join(
    f'<figure class="tile {cls} {"dark" if dark else ""}"><div class="tile-art">{logo(n, "art-" + n)}</div>'
    f'<figcaption><span class="cap-t">{t}</span><span class="cap-s">{d}</span></figcaption></figure>'
    for n, t, d, cls, dark in suite)

page = open(os.path.join(HERE, "page2.tpl.html")).read()
page = (page.replace("{{CSS}}", open(os.path.join(HERE, "base.css")).read().replace("<style>", "").replace("</style>", ""))
            .replace("{{HERO}}", logo("wordmark", "hero-mark", "Solano"))
            .replace("{{SOL}}", logo("sol", "inline-sol", "Sol."))
            .replace("{{SUN}}", logo("sun", "inline-sun", "Solano sun monogram"))
            .replace("{{SUITE}}", suite_html).replace("{{CORE}}", core_html).replace("{{DROPS}}", drops_html))
open(sys.argv[1], "w").write(page)
print("built", len(page))
