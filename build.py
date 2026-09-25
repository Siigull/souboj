#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kulečníkový souboj univerzit — minimalistický generátor statického webu.

Použití:
    python3 build.py              # vygeneruje web do ./dist
    python3 build.py --serve      # vygeneruje a spustí server na :8000
    python3 build.py --serve -p 3000

Obsah webu se edituje v souboru data.py. Bez externích závislostí —
pouze standardní knihovna Pythonu.
"""

import argparse
import html
import json
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import data

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
ASSETS = ROOT / "assets"


def e(text):
    """Oescapuje text pro bezpečné vložení do HTML."""
    return html.escape(str(text), quote=True)


# ---------------------------------------------------------------------------
# Pomocné renderovací funkce
# ---------------------------------------------------------------------------

def render_head():
    s = data.SITE
    return f"""<meta charset="utf-8"/>
<title>{e(s['title'])}</title>
<meta name="description" content="{e(s['description'])}"/>
<meta property="og:title" content="{e(s['title'])}"/>
<meta property="og:description" content="{e(s['description'])}"/>
<meta property="og:image" content="{e(s['og_image'])}"/>
<meta name="twitter:title" content="{e(s['title'])}"/>
<meta name="twitter:description" content="{e(s['description'])}"/>
<meta name="twitter:image" content="{e(s['og_image'])}"/>
<meta property="og:type" content="website"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<link href="css/main.css" rel="stylesheet" type="text/css"/>
<link href="images/KSU-favicon.png" rel="shortcut icon" type="image/x-icon"/>
<link href="images/KSU-webclip.png" rel="apple-touch-icon"/>
<script type="application/ld+json">
{render_jsonld()}
</script>"""


def render_jsonld():
    doc = dict(data.JSONLD)
    location = doc["location"]
    # Struktura schema.org vyžaduje u subEvent také místo konání.
    doc["subEvent"] = [
        {**sub, "location": location} for sub in doc.get("subEvent", [])
    ]
    return json.dumps(doc, ensure_ascii=False, indent=2)


def render_nav():
    links = "".join(
        f'<a href="{e(item["href"])}" class="nav-link w-inline-block">'
        f'<div class="text-block-2">{e(item["label"])}</div></a>'
        for item in data.NAV
    )
    return f"""<div role="banner" class="navbar w-nav">
<header class="nav-wrapper w-container"><div class="nav-flex"><nav role="navigation" class="nav-menu w-nav-menu">{links}</nav></div></header>
</div>"""


def render_intro():
    return f"""<section id="intro" class="intro-section bgr-color dark"><div class="section-bgr"><img src="images/KSU-logotype.svg" loading="lazy" alt="Logo: Kulečníkový souboj univerzit" class="hero-image"/><img src="images/KSU-logotype-vertical.svg" loading="lazy" alt="Logotyp: kulečníkový souboj univerzit" class="hero-image mobile"/></div></section>"""


def render_info():
    text = "<br/><br/>".join(e(p) for p in data.INTRO_PARAGRAPHS)
    return f"""<section class="section"><div id="info" class="section-anchor"></div><div class="container"><div class="flex-v max-w-640"><h2 class="display-1">{e(data.INTRO_HEADING)}</h2><p class="text-500">{text}</p></div></div></section>"""


def render_schedule():
    sc = data.SCHEDULE
    prizes = "".join(f'<p class="text-500 txt-color white">{e(p)}</p>' for p in sc["prizes"])
    return f"""<section class="section bgr-color dark"><div id="terminy" class="section-anchor"></div><div class="container"><div class="flex-v max-w-640"><h2 class="display-1 txt-color white">{e(sc['heading'])}</h2><div class="flex-v tight"><h3 class="display-2 txt-color white">herna</h3><p class="text-500 txt-color white">{e(sc['herna'])}</p></div><div class="flex-v tight"><h3 class="display-2 txt-color white">termíny</h3><p class="text-500 txt-color white">{e(sc['dates'])}</p><p class="text-500 txt-color white">{e(sc['start'])}</p></div><div class="flex-v tight"><h3 class="display-2 txt-color white">podrobné info</h3><a href="{e(sc['info_link']['href'])}" target="_blank" class="link-block w-inline-block"><p class="text-500 txt-color white">{e(sc['info_link']['label'])}</p></a></div><div class="flex-v tight"><h3 class="display-2 txt-color white">výsledky</h3><a href="{e(sc['results_link']['href'])}" target="_blank" class="link-block w-inline-block"><p class="text-500 txt-color white">{e(sc['results_link']['label'])}</p></a></div><div class="flex-v tight"><h3 class="display-2 txt-color white">ceny</h3>{prizes}</div></div></div></section>"""


def mobile_rows(round_):
    """Sloučí výsledky obou univerzit do jedné listiny seřazené dle umístění."""
    rows = []
    for uni in ("vut", "muni"):
        label = data.UNIVERSITIES[uni]["label"].upper()
        for result in round_["results"].get(uni, []):
            rank = int(result.split(".", 1)[0])
            rows.append((rank, f"{result} ({label})"))
    rows.sort(key=lambda item: item[0])
    return [text for _, text in rows]


def render_score_block(uni_key, season):
    uni = data.UNIVERSITIES[uni_key]
    return (
        f'<div class="flex-v"><div class="flex-v supertight">'
        f'<div class="display-0 txt-color {uni["color"]}">{e(uni["label"])}</div>'
        f'<div class="display-0 score txt-color {uni["color"]}">{e(season["scores"][uni_key])}</div>'
        f"</div></div>"
    )


def round_heading(round_):
    """Nadpis kola — pokud kolo má URL, je to odkaz na turnaj."""
    if round_.get("url"):
        return f'<a href="{e(round_["url"])}" target="_blank" class="round-link">{e(round_["name"])}</a>'
    return e(round_["name"])


def render_round_block(round_, uni_key):
    rows = "".join(f'<p class="text-300">{e(r)}</p>' for r in round_["results"][uni_key])
    return (
        f'<div class="flex-v tight desktop"><h3 class="display-2 txt-color dark">{round_heading(round_)}</h3>'
        f'<div class="flex-v supertight">{rows}</div></div>'
    )


def render_mobile_block(round_):
    rows = "".join(f'<p class="text-300">{e(r)}</p>' for r in mobile_rows(round_))
    return (
        f'<div class="flex-v tight mobile"><h3 class="display-2 txt-color dark">{round_heading(round_)}</h3>'
        f'<div class="flex-v supertight">{rows}</div></div>'
    )


def render_season_pane(season, index):
    # Pořadí v DOM určuje rozložení mřížky (CSS auto-placement):
    # desktop = [vut | MUNI] a pod tím řádky [VUT | MUNI] pro každé kolo,
    # mobil (<= 479 px) = vše pod sebou, desktopové bloky se skryjí.
    grid_blocks = [
        render_score_block("vut", season),
        render_score_block("muni", season),
    ]
    if season.get("rounds_on_desktop"):
        for round_ in season["rounds"]:
            grid_blocks.append(render_round_block(round_, "vut"))
            grid_blocks.append(render_round_block(round_, "muni"))
    grid_blocks.extend(render_mobile_block(round_) for round_ in season["rounds"])
    grid = "".join(grid_blocks)
    active = " w--tab-active" if index == 0 else ""
    return f"""<div id="tab-{index}" role="tabpanel" class="w-tab-pane{active}"><div class="flex-v"><div class="subheader-wrapper"><h3 class="display-2 txt-color dark">skóre univerzit (AVG)</h3></div><div class="grid-2">{grid}</div></div><div class="flex-v"><div class="subheader-wrapper"><h3 class="display-2 txt-color dark">MVP série</h3></div><div class="flex-v supertight"><p class="text-500">{e(season['mvp'])}</p></div></div></div>"""


def render_results():
    links = "".join(
        '<a href="#tab-{i}" data-tab="{i}" role="tab" aria-selected="{sel}" class="tab-link-tab-{n} w-inline-block w-tab-link{cur}"><div>{label}</div></a>'.format(
            i=i,
            n=i + 1,
            sel="true" if i == 0 else "false",
            cur=" w--current" if i == 0 else "",
            label=e(season["label"]),
        )
        for i, season in enumerate(data.SEASONS)
    )
    panes = "".join(render_season_pane(season, i) for i, season in enumerate(data.SEASONS))
    return f"""<section class="section"><div id="skore" class="section-anchor"></div><div class="container"><div class="flex-v max-w-640"><h2 class="display-1">výsledky</h2><div data-tabs class="tabs w-tabs"><div class="tabs-menu w-tab-menu" role="tablist">{links}</div><div class="tabs-content w-tab-content">{panes}</div></div></div></div></section>"""


def render_contacts():
    c = data.CONTACTS
    links = "".join(
        f'<a href="{e(l["href"])}" target="_blank" class="link-block w-inline-block">'
        f'<p class="text-500 txt-color white">{e(l["label"])}</p></a>'
        for l in c["links"]
    )
    logos = "".join(
        f'<a href="{e(l["href"])}" target="_blank" class="image-link w-inline-block">'
        f'<img src="{e(l["image"])}" loading="lazy" alt="{e(l["alt"])}" class="{e(l["css_class"])}"/></a>'
        for l in c["logos"]
    )
    footer = "".join(f'<div class="text-300 txt-color white">{e(t)}</div>' for t in c["footer"])
    return f"""<section class="section bgr-color dark"><div id="kontakty" class="section-anchor"></div><div class="container"><div class="flex-v loose"><div class="flex-v max-w-640"><h2 class="display-1 txt-color white">{e(c['heading'])}</h2><div class="flex-v tight"><h3 class="display-2 txt-color white">info a kontakt</h3><div class="flex-h-stack kontakt">{links}</div></div><div class="grid-2 max-w-640"><div class="flex-v tight"><h3 class="display-2 txt-color white">pořádá</h3><a href="{e(c['organizer']['href'])}" target="_blank" class="link-block w-inline-block"><p class="text-500 txt-color white">{e(c['organizer']['label'])}</p></a></div><div class="flex-v tight"><h3 class="display-2 txt-color white">herna</h3><a href="{e(c['venue']['href'])}" target="_blank" class="link-block w-inline-block"><p class="text-500 txt-color white">{e(c['venue']['label'])}</p></a></div></div></div><div class="flex-h-stack">{logos}</div><div class="flex-h footer">{footer}</div></div></div></section>"""


# ---------------------------------------------------------------------------
# Sestavení stránky
# ---------------------------------------------------------------------------

def render_page():
    return f"""<!DOCTYPE html>
<html lang="cs">
<head>
{render_head()}
</head>
<body>
<div class="page-wrapper">
{render_nav()}
<div class="main-wrapper">
{render_intro()}
{render_info()}
{render_schedule()}
{render_results()}
{render_contacts()}
</div>
</div>
<script src="js/tabs.js" defer></script>
</body>
</html>
"""


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copytree(ASSETS, DIST, dirs_exist_ok=True)
    (DIST / "index.html").write_text(render_page(), encoding="utf-8")
    print(f"OK: web vygenerován do {DIST}/")


def serve(port):
    build()

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(DIST), **kwargs)

    with HTTPServer(("", port), Handler) as httpd:
        print(f"Serving {DIST}/ at http://localhost:{port} (Ctrl+C to stop)")
        httpd.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Generátor statického webu KSU")
    parser.add_argument("--serve", action="store_true", help="po sestavení spustit lokální server")
    parser.add_argument("-p", "--port", type=int, default=8000, help="port lokálního serveru")
    args = parser.parse_args()
    if args.serve:
        serve(args.port)
    else:
        build()


if __name__ == "__main__":
    main()
