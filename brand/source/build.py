import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(os.path.join(HERE, "logos.json")))

def logo(name, cls="", label=""):
    l = L[name]
    return (f'<svg class="logo {cls}" viewBox="0 0 {l["w"]:g} {l["h"]:g}" fill="currentColor" '
            f'role="img" aria-label="{label or "Sottovoce " + name}">{l["body"]}</svg>')

def placed(name, x, y, w, color):
    l = L[name]; h = w * l["h"] / l["w"]
    return (f'<svg x="{x - w / 2:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'viewBox="0 0 {l["w"]:g} {l["h"]:g}" fill="{color}" color="{color}">{l["body"]}</svg>')

TEE = "M138 34 Q200 70 262 34 L352 74 L384 150 L326 172 L314 150 L314 404 Q200 414 86 404 L86 150 L74 172 L16 150 L48 74 Z"
COLLAR = "M138 34 Q200 70 262 34 Q200 56 138 34 Z"

def tee(fill, ink, mark, w, y):
    return (f'<svg viewBox="0 0 400 420" class="mock" aria-hidden="true">'
            f'<path d="{TEE}" fill="{fill}"/><path d="{COLLAR}" fill="{ink}" opacity=".18"/>'
            f'<path d="M86 150 L86 404" stroke="{ink}" stroke-opacity=".12" stroke-width="2"/>'
            f'<path d="M314 150 L314 404" stroke="{ink}" stroke-opacity=".12" stroke-width="2"/>'
            f'{placed(mark, 200, y, w, ink)}</svg>')

def cap(fill, ink):
    return (f'<svg viewBox="0 0 400 420" class="mock" aria-hidden="true">'
            f'<path d="M70 250 Q66 96 200 92 Q334 96 330 250 Z" fill="{fill}"/>'
            f'<path d="M200 92 L200 250" stroke="{ink}" stroke-opacity=".14" stroke-width="2"/>'
            f'<path d="M134 104 Q120 180 124 250 M266 104 Q280 180 276 250" fill="none" stroke="{ink}" stroke-opacity=".1" stroke-width="2"/>'
            f'<circle cx="200" cy="94" r="7" fill="{fill}" stroke="{ink}" stroke-opacity=".2"/>'
            f'<path d="M48 250 Q200 214 352 250 Q370 300 200 318 Q30 300 48 250 Z" fill="{fill}"/>'
            f'<path d="M48 250 Q200 214 352 250" fill="none" stroke="{ink}" stroke-opacity=".22" stroke-width="2"/>'
            f'{placed("monogram", 200, 128, 96, ink)}</svg>')

def label(fill, ink):
    return (f'<svg viewBox="0 0 400 420" class="mock" aria-hidden="true">'
            f'<rect x="40" y="150" width="320" height="120" fill="{fill}"/>'
            f'<rect x="52" y="162" width="296" height="96" fill="none" stroke="{ink}" stroke-opacity=".35" stroke-dasharray="3 4"/>'
            f'{placed("wordmark", 200, 185, 236, ink)}</svg>')

GREEN, ECRU, OX, INK = "#1F3A2E", "#EDE6D6", "#6B1E24", "#141414"

mocks = [
    (tee(ECRU, GREEN, "script", 120, 102), "Ecru heavyweight tee", "Script mark, left chest, tonal embroidery"),
    (tee(GREEN, ECRU, "crest", 170, 120), "Bottle green crewneck", "Crest, centre chest, chain-stitch"),
    (cap(OX, ECRU), "Oxblood six-panel", "VS monogram, front, flat embroidery"),
    (label(INK, ECRU), "Woven neck label", "Wordmark, damask weave"),
]

mock_html = "\n".join(
    f'<figure class="mock-card"><div class="mock-ground">{svg}</div>'
    f'<figcaption><span class="cap-t">{t}</span><span class="cap-s">{s}</span></figcaption></figure>'
    for svg, t, s in mocks)

suite = [
    ("wordmark", "Primary wordmark", "Woven labels, hang tags, the website header, the shop sign. The one that does the heavy lifting.", "wide"),
    ("script", "Script mark", "Left-chest embroidery on tees, polos and knits. This is the Amici move: the logo people clock across a bar.", "wide"),
    ("crest", "Club crest", "Centre chest on sweats, back prints, patches, packaging stickers.", ""),
    ("monogram", "VS monogram", "Caps, buttons, zip pulls, socks, the Instagram avatar. Works at 12mm.", ""),
    ("svc", "S.V.C. short mark", "Spine of a hoodie, sleeve hits, sub-labels, how the regulars will say it.", ""),
]
suite_html = "\n".join(
    f'<figure class="tile {cls} {"dark" if i in (1, 3) else ""}"><div class="tile-art">{logo(n, "art-" + n)}</div>'
    f'<figcaption><span class="cap-t">{t}</span><span class="cap-s">{d}</span></figcaption></figure>'
    for i, (n, t, d, cls) in enumerate(suite))

page = open(os.path.join(HERE, "page.tpl.html")).read()
page = (page.replace("{{HERO}}", logo("wordmark", "hero-mark", "Sottovoce Social Club"))
            .replace("{{SUITE}}", suite_html).replace("{{MOCKS}}", mock_html)
            .replace("{{SVC}}", logo("svc", "inline-svc", "S.V.C."))
            .replace("{{MONO}}", logo("monogram", "inline-mono", "VS monogram")))
open(sys.argv[1], "w").write(page)
print("built", len(page))
