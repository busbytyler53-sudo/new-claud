import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(os.path.join(HERE, "solano8.json")))["logos"]

def tone(hexc, amt):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    t = 0 if amt < 0 else 255; a = abs(amt)
    return "#" + "".join(f"{round(c + (t - c) * a):02X}" for c in (r, g, b))

NEUTRALS = {"chalk": "#F1EFEA", "oat": "#DDD5C6", "stone": "#B5B0A6", "olive": "#7D7E68", "navy": "#232B38", "black": "#1F1F1D"}
DARK = ("olive", "navy", "black")
T = {k: {"bg": v, "ink": tone(v, .3 if k in DARK else -.3)} for k, v in NEUTRALS.items()}
NAMES = {"chalk": "Chalk", "oat": "Oat", "stone": "Stone", "olive": "Olive", "navy": "Navy", "black": "Black"}

def logo(name, cls="", label=""):
    l = L[name]
    return (f'<svg class="logo {cls}" viewBox="0 0 {l["w"]:g} {l["h"]:g}" fill="currentColor" '
            f'role="img" aria-label="{label or "Solano " + name}">{l["body"]}</svg>')

def placed(name, x, y, w, color):
    l = L[name]; h = w * l["h"] / l["w"]
    return (f'<svg x="{x - w / 2:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'viewBox="0 0 {l["w"]:g} {l["h"]:g}" fill="{color}" color="{color}">{l["body"]}</svg>')

def frame(inner):
    return f'<svg viewBox="0 0 400 420" class="mock" aria-hidden="true">{inner}</svg>'

TEE = "M140 30 Q200 62 260 30 L358 62 L392 176 L330 190 L318 150 L318 404 Q200 410 82 404 L82 150 L70 190 L8 176 L42 62 Z"
SEAMS = "M82 150 L82 404 M318 150 L318 404 M42 62 L82 150 M358 62 L318 150"

def tee(c, inner="", collar=True):
    bg, ink = T[c]["bg"], T[c]["ink"]
    neck = f'<path d="M140 30 Q200 62 260 30 Q200 50 140 30 Z" fill="{ink}" opacity=".22"/>' if collar else ""
    return (f'<path d="{TEE}" fill="{bg}"/>{neck}'
            f'<path d="{SEAMS}" stroke="{ink}" stroke-opacity=".14" stroke-width="2" fill="none"/>{inner}')

def polo(c):
    bg, ink = T[c]["bg"], T[c]["ink"]
    return frame(tee(c, collar=False) +
                 f'<path d="M140 30 L200 64 L178 86 L128 42 Z M260 30 L200 64 L222 86 L272 42 Z" fill="{bg}" stroke="{ink}" stroke-opacity=".35" stroke-width="2"/>'
                 f'<path d="M200 64 V140" stroke="{ink}" stroke-opacity=".35" stroke-width="2"/>'
                 f'<circle cx="200" cy="96" r="3.5" fill="{ink}"/><circle cx="200" cy="124" r="3.5" fill="{ink}"/>'
                 + "".join(f'<path d="M86 {y} H314" stroke="{ink}" stroke-opacity=".08" stroke-width="2"/>' for y in range(170, 400, 16)))

def shirt(c):
    bg, ink = T[c]["bg"], T[c]["ink"]
    return frame(tee(c, collar=False) +
                 f'<path d="M140 30 L200 122 L170 128 L118 48 Z M260 30 L200 122 L230 128 L282 48 Z" fill="{tone(bg, .07)}" stroke="{ink}" stroke-opacity=".3" stroke-width="2"/>'
                 f'<path d="M200 122 V404" stroke="{ink}" stroke-opacity=".3" stroke-width="2"/>'
                 + "".join(f'<circle cx="206" cy="{y}" r="3.5" fill="{ink}"/>' for y in (170, 230, 290, 350)))

def shorts(c, mark=True):
    bg, ink = T[c]["bg"], T[c]["ink"]
    m = placed("emblem", 266, 236, 30, ink) if mark else ""
    return frame(f'<path d="M96 70 H304 L330 318 Q264 326 214 318 L200 160 L186 318 Q136 326 70 318 Z" fill="{bg}"/>'
                 f'<path d="M96 70 H304 V100 H96 Z" fill="{ink}" opacity=".25"/>'
                 f'<path d="M200 100 V160" stroke="{ink}" stroke-opacity=".3" stroke-width="2"/>{m}')

def trousers(c):
    bg, ink = T[c]["bg"], T[c]["ink"]
    return frame(f'<path d="M112 14 H288 L314 408 H224 L200 130 L176 408 H86 Z" fill="{bg}"/>'
                 f'<path d="M112 14 H288 V38 H112 Z" fill="{ink}" opacity=".22"/>'
                 f'<path d="M156 38 L150 408 M244 38 L250 408" stroke="{ink}" stroke-opacity=".22" stroke-width="2"/>'
                 f'<path d="M200 38 V130" stroke="{ink}" stroke-opacity=".3" stroke-width="2"/>')

HOODIE = "M140 46 Q200 74 260 46 L350 78 L388 384 L338 390 L318 176 L318 410 Q200 416 82 410 L82 176 L62 390 L12 384 L50 78 Z"
def hoodie_back(c, inner):
    bg, ink = T[c]["bg"], T[c]["ink"]
    return frame(f'<path d="M126 60 Q114 6 200 6 Q286 6 274 60 Q200 84 126 60 Z" fill="{tone(bg, -.06 if c not in DARK else .06)}"/>'
                 f'<path d="{HOODIE}" fill="{bg}"/>'
                 f'<path d="M82 176 V410 M318 176 V410" stroke="{ink}" stroke-opacity=".14" stroke-width="2"/>{inner}')

def cap(c):
    bg, ink = T[c]["bg"], T[c]["ink"]
    return frame(f'<path d="M70 250 Q66 96 200 92 Q334 96 330 250 Z" fill="{bg}"/>'
                 f'<path d="M200 92 L200 250 M134 104 Q120 180 124 250 M266 104 Q280 180 276 250" fill="none" stroke="{ink}" stroke-opacity=".18" stroke-width="2"/>'
                 f'<circle cx="200" cy="94" r="7" fill="{bg}" stroke="{ink}" stroke-opacity=".3"/>'
                 f'<path d="M48 250 Q200 214 352 250 Q370 300 200 318 Q30 300 48 250 Z" fill="{bg}"/>'
                 f'<path d="M48 250 Q200 214 352 250" fill="none" stroke="{ink}" stroke-opacity=".3" stroke-width="2"/>'
                 f'{placed("emblem", 200, 140, 62, ink)}')

def fig(svg, title, sub):
    return (f'<figure class="blank"><div class="ground">{svg}</div>'
            f'<figcaption><span>{title}</span><span class="dim">{sub}</span></figcaption></figure>')

lines = [
    ("sport", "09:00", "Sport", "Activewear",
     "The Solano Club kit. Training tees, shorts and layers that go from the Sunday run straight into the day. Quick-dry, four-way stretch, cut like the rest of the range so nothing looks like gym kit at the coffee shop.",
     [fig(frame(tee("black", placed("line-sport", 250, 92, 84, T["black"]["ink"]))), "Training tee", "Black, tech jersey"),
      fig(shorts("navy"), "Training short", "Navy, 7 inch, lined")]),
    ("giorno", "13:00", "Giorno", "Smart casual",
     "The office, the lunch, the afternoon meeting. Knit polos, pleated trousers, overshirts. Clean enough for a client, relaxed enough for a Friday.",
     [fig(polo("oat"), "Knit polo", "Oat, fine gauge cotton"),
      fig(trousers("stone"), "Pleated trouser", "Stone, relaxed taper")]),
    ("sera", "21:00", "Sera", "Date night",
     "The evening pieces. Camp-collar shirts, dark trousers, no logo on the outside at all. The label inside does the work. This is where the margin is.",
     [fig(shirt("black"), "Camp-collar shirt", "Black, fluid viscose"),
      fig(trousers("navy"), "Evening trouser", "Navy, wool blend")]),
    ("strada", "Any time", "Strada", "Streetwear",
     "Heavyweight hoodies, sweats and caps with the bigger branding. The back print, the emblem on the cap. The pieces that get the brand seen on the street.",
     [fig(hoodie_back("olive", placed("club", 200, 120, 200, T["olive"]["ink"])), "Hoodie, back", "Olive, 480 gsm"),
      fig(cap("chalk"), "Cap", "Chalk, washed twill")]),
]
lines_html = "\n".join(
    f'<article class="line"><div class="line-text"><p class="label">{time}</p>{logo("line-" + k, "line-mark", "Solano " + nm)}'
    f'<p class="line-cat">{cat}</p><p>{desc}</p></div><div class="line-mocks">{"".join(m)}</div></article>'
    for k, time, nm, cat, desc, m in lines)

blanks_html = "\n".join(fig(frame(tee(k, placed("wordmark", 200, 106, 82, t["ink"]))), NAMES[k], t["bg"]) for k, t in T.items())

suite = [("wordmark", "Solano", "The full name."), ("lockup", "Lockup", "Emblem and name together."),
         ("sol", "SOL.", "The short name."), ("emblem", "Sun and wind", "The emblem."),
         ("club", "Solano Club", "The community name."), ("label", "Label", "Inside every piece.")]
suite_html = "\n".join(
    f'<figure class="mark m-{n}"><div class="mark-art">{logo(n)}</div><figcaption><span>{t}</span><span class="dim">{d}</span></figcaption></figure>'
    for n, t, d in suite)

swatch_html = "\n".join(
    f'<div class="sw"><div class="chip" style="background:{t["bg"]}"><span style="color:{t["ink"]}">SOLANO</span></div>'
    f'<span>{NAMES[k]}</span><span class="dim">{t["bg"]}</span></div>' for k, t in T.items())

page = open(os.path.join(HERE, "page8.tpl.html")).read()
for k, v in {"HERO": logo("lockup", "hero-mark", "Solano"), "FOOT": logo("emblem", "foot-mark"),
             "LINES": lines_html, "BLANKS": blanks_html, "SUITE": suite_html, "SWATCHES": swatch_html,
             "N9": logo("sol", "inline-n9"), "CLOCK": logo("emblem", "inline-clock"), "STAMP": logo("club", "inline-stamp")}.items():
    page = page.replace("{{" + k + "}}", v)
open(sys.argv[1], "w").write(page)
print("built", len(page))
