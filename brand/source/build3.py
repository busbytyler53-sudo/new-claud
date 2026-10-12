import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(HERE, "agosto.json")))
L, G, CW = J["logos"], J["graphics"], J["colorways"]

def colorize(body, cw):
    for k, v in cw.items():
        body = body.replace(f"var({k})", v)
    return body

def logo(name, cls="", label=""):
    l = L[name]
    return (f'<svg class="logo {cls}" viewBox="0 0 {l["w"]:g} {l["h"]:g}" fill="currentColor" '
            f'role="img" aria-label="{label or "Agosto " + name}">{l["body"]}</svg>')

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
            f'{placed("swallow", 200, 140, 84, ink)}</svg>')

def label(fill, ink):
    return (f'<svg viewBox="0 0 400 420" class="mock" aria-hidden="true">'
            f'<rect x="60" y="160" width="280" height="100" fill="{fill}"/>'
            f'<rect x="72" y="172" width="256" height="76" fill="none" stroke="{ink}" stroke-opacity=".35" stroke-dasharray="3 4"/>'
            f'{placed("lockup", 200, 186, 190, ink)}</svg>')

NAVY, ECRU, INK, WHITE = "#1C2B3F", "#EDE6D6", "#141414", "#F7F5EF"

def keyring(fill, ink):
    l = L["keytag"]; w = 120; h = w * l["h"] / l["w"]
    return (f'<svg viewBox="0 0 400 420" class="mock" aria-hidden="true">'
            f'<circle cx="200" cy="54" r="30" fill="none" stroke="#9A9282" stroke-width="5"/>'
            f'<svg x="140" y="70" width="{w}" height="{h:.1f}" viewBox="0 0 {l["w"]:g} {l["h"]:g}" fill="{ink}" color="{ink}">'
            f'<path d="M72 66C44 124 24 204 24 296C24 366 60 406 100 406C140 406 176 366 176 296C176 204 156 124 128 66A40 40 0 1 0 72 66Z" fill="{fill}"/>'
            f'{l["body"]}</svg></svg>')

def cap2(fill, ink):
    return cap(fill, ink)

core = [
    (tee(WHITE, NAVY, placed("script", 252, 100, 74, NAVY)), "Ospiti tee", "Washed white, script on the chest"),
    (tee(NAVY, ECRU, placed("wordmark", 200, 112, 120, ECRU)), "Ospiti crewneck", "Navy loopback, wordmark centre chest"),
    (cap2(ECRU, NAVY), "Ospiti cap", "Ecru twill, the swallow, nothing else"),
    (keyring(ECRU, NAVY), "Room key", "Camera 12 key tag, comes with every order"),
]
core_html = "\n".join(
    f'<figure class="mock-card"><div class="mock-ground">{s}</div>'
    f'<figcaption><span class="cap-t">{t}</span><span class="cap-s">{d}</span></figcaption></figure>'
    for s, t, d in core)

drops = [
    ("limoni", "01", "Limoni", "Il giardino", "The lemon tree by the terrace, where breakfast is served. Yellow and leaf green on washed white. The opener, and the one that sells through first.", WHITE),
    ("palma", "02", "Palma", "La spiaggia", "The two palms at the end of the beach, where everyone ends up at seven. Navy and apricot on ecru.", ECRU),
    ("rondini", "03", "Rondini", "Il ritorno", "The swallows that nest under the hotel roof and come back every year, like the guests. Navy on sea blue. The last drop of the summer.", ECRU),
]
drops_html = "\n".join(
    f'<article class="drop"><div class="drop-pair">'
    f'<div class="mock-ground">{tee(bg, NAVY, placed("ago", 252, 100, 46, NAVY))}</div>'
    f'<div class="mock-ground">{tee(bg, NAVY, placed_print(k, 200, 66, 176), back=True)}</div></div>'
    f'<div class="drop-text"><p class="drop-no">Souvenir {n} · {place}</p><h3>{name}</h3><p>{desc}</p>'
    f'<p class="cap-s">Front: Ago. on the chest. Back: full print, 28cm wide.</p></div></article>'
    for k, n, name, place, desc, bg in drops)

suite = [
    ("lockup", "The sign", "The swallow over the name, like the painted sign above the door. Labels, packaging, the website.", "wide", False),
    ("script", "The signature", "Small on the chest of the Ospiti range. Reads like it was written on the guest book.", "wide", True),
    ("swallow", "The swallow", "The emblem. Caps, sleeves, socks, buttons. Stands in for the name once people know it.", "", True),
    ("keytag", "Camera 12", "The room key. Hang tags, the keyring in every box, the back neck print.", "", False),
    ("ago", "Ago.", "The short name. Front of every souvenir tee, and the Instagram handle.", "", False),
]
suite_html = "\n".join(
    f'<figure class="tile {cls} {"dark" if dark else ""}"><div class="tile-art">{logo(n, "art-" + n)}</div>'
    f'<figcaption><span class="cap-t">{t}</span><span class="cap-s">{d}</span></figcaption></figure>'
    for n, t, d, cls, dark in suite)

page = open(os.path.join(HERE, "page3.tpl.html")).read()
page = (page.replace("{{CSS}}", open(os.path.join(HERE, "base.css")).read().replace("<style>", "").replace("</style>", ""))
            .replace("{{HERO}}", logo("lockup", "hero-mark", "Agosto"))
            .replace("{{AGO}}", logo("ago", "inline-ago", "Ago."))
            .replace("{{SWALLOW}}", logo("swallow", "inline-swallow", "Agosto swallow"))
            .replace("{{SUITE}}", suite_html).replace("{{CORE}}", core_html).replace("{{DROPS}}", drops_html))
open(sys.argv[1], "w").write(page)
print("built", len(page))
