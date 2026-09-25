# -*- coding: utf-8 -*-
"""
Veškerý obsah webu Kulečníkový souboj univerzit.

Po úpravě spusťte:  python3 build.py
Výsledek se vygeneruje do adresáře  dist/
"""

# ---------------------------------------------------------------------------
# Základní metadata
# ---------------------------------------------------------------------------

SITE = {
    "title": "Kulečníkový souboj univerzit",
    "description": (
        "Otevřená série pěti turnajů pro studenty MUNI a VUT ročníku 2025/2026. "
        "Hráči mohou být aktivními členy ČMBS. Na konci série bude vyhlášena "
        "vítězná univerzita. Zároveň se hraje od MVP celé série. Jednotlivcům se "
        "do pořadí série počítají 3 nejelpší výsledky. V každém turnaji budou "
        "ocenění 3 nejlepší hráči."
    ),
    # Obrázek pro sdílení na sociálních sítích — musí být absolutní URL.
    # Po nasazení na vlastní doménu změňte na vlastní URL.
    "og_image": "https://cdn.prod.website-files.com/696f3be1f2e5e2de338f5f92/696f72d4062ee310cc776d2a_KSU-OG.avif",
}

NAV = [
    {"label": "Info", "href": "#info"},
    {"label": "termíny", "href": "#terminy"},
    {"label": "skóre", "href": "#skore"},
    {"label": "kontakt", "href": "#kontakty"},
]

INTRO_HEADING = "bojujte za svou univerzitu"

INTRO_PARAGRAPHS = [
    "Otevřená série pěti turnajů pro studenty MUNI a VUT ročníku 2025/2026. "
    "Hráči mohou být aktivními členy ČMBS.",
    "Do výsledku univerzit se započítávají nejlepší bodové výsledky z každého "
    "turnaje každé z nich. Počet započítaných výsledku se odvíjí od počtu hráčů "
    "z jednotlivé univerzity. Minimální je nula, maximálně tři. Výsledným číslem "
    "je průměr.",
    "Zároveň se hraje od MVP celé série. Jednotlivcům se do pořadí série počítají "
    "3 nejlepší výsledky. V každém turnaji budou ocenění 3 nejlepší hráči.",
]

# ---------------------------------------------------------------------------
# Kde a kdy (sekce s termíny)
# ---------------------------------------------------------------------------

SCHEDULE = {
    "heading": "Kde a kdy",
    "herna": "Sborovna, Botanická 1, Brno",
    "dates": "4/10 • 25/10 • 15/11 • 6/12",
    "start": "start od 17.30",
    "info_link": {"label": "podzim 2026", "href": "https://vysledky.cmbs.cz/tournament-series/825"},
    "results_link": {"label": "jaro 2026", "href": "https://vysledky.cmbs.cz/tournament-series/812"},
    "prizes": [
        "Putovní pohár pro vítěznou univerzitu",
        "Štítek na trofeji pro MVP série a vítěze*ky jednotlivých turnajů",
        "Roční členství v DELTA Billiard Brno a ČMBS v hodnotě 1 200 Kč pro 3 nejlepší hráče*ky série.",
    ],
}

# ---------------------------------------------------------------------------
# Výsledky
# ---------------------------------------------------------------------------
# - Každá sezóna má vlastní tab v sekci výsledky.
# - "rounds" = výsledky po kolech a univerzitách. Z toho jediného zdroje
#   se odvozují desktopové sloupce (vlevo VUT, vpravo MUNI) i mobilní
#   sloučené seznamy.
# - "rounds_on_desktop": uvedené sezóny se na desktopu rozbalují po kolech
#   ve dvou sloupcích; pro aktuálně běžící sezónu stačí false.
# - Pozn.: pro třetí tab by bylo potřeba doplnit CSS pravidlo .tab-link-tab-3
#   (srovnejte s .tab-link-tab-2 v assets/css/main.css).

UNIVERSITIES = {
    "muni": {"label": "MUNI", "color": "muni"},
    "vut": {"label": "vut", "color": "vut"},
}

# Výsledky jednotlivých kol jarní sezóny 2026. Každé kolo odkazuje na
# příslušný turnaj v systému vysledky.cmbs.cz.

JARO_ROUNDS = [
    {
        "name": "1. kolo",
        "url": "https://vysledky.cmbs.cz/tournaments/3225",
        "results": {
            "vut": ["1. Denis Novosád", "2. Daniel Pelánek", "4. Petr Nový"],
            "muni": ["3. Dominik Holiš", "5. Tomáš Kasza", "5. Matej Kubík"],
        },
    },
    {
        "name": "2. kolo",
        "url": "https://vysledky.cmbs.cz/tournaments/3226",
        "results": {
            "vut": ["1. Denis Novosád", "2. Martin Benovič"],
            "muni": ["3. Ciarán O’Tuathail", "9. Zdeněk Vychodil"],
        },
    },
    {
        "name": "3. kolo",
        "url": "https://vysledky.cmbs.cz/tournaments/3227",
        "results": {
            "vut": ["1. Martin Benovič", "3. Viktor Holanec", "3. Matyáš Telecký"],
            "muni": ["2. Erik Smetana", "5. Zdeněk Vychodil", "5. Tomáš Kasza"],
        },
    },
    {
        "name": "4. kolo",
        "url": "https://vysledky.cmbs.cz/tournaments/3228",
        "results": {
            "vut": ["2. Daniel Pelánek", "4. Viktor Holanec", "5. František Roh"],
            "muni": ["1. Ciarán O’Tuathail", "3. Erik Smetana", "7. Matej Drblík"],
        },
    },
    {
        "name": "5. kolo",
        "url": "https://vysledky.cmbs.cz/tournaments/3229",
        "results": {
            "vut": ["1. Daniel Pelánek", "2. Viktor Holanec"],
            "muni": ["5. Ciarán O’Tuathail", "6. Matej Kubík"],
        },
    },
]

# Podzim 2026 zatím neproběhl — jako výplň tabu se zobrazují listiny
# jarní sezóny (bez odkazů). Po odehrání kol nahraďte reálnými daty.

PODZIM_ROUNDS = [{"name": r["name"], "results": r["results"]} for r in JARO_ROUNDS]

SEASONS = [
    {
        "label": "Jaro 2026",
        "scores": {"muni": "543", "vut": "785"},
        "mvp": "Daniel Pelánek (VUT)",
        "rounds": JARO_ROUNDS,
        "rounds_on_desktop": True,
    },
    {
        # Podzim 2026 ještě neproběhl — skóre a MVP jsou zatímní (placeholder).
        "label": "Podzim 2026",
        "scores": {"muni": "0", "vut": "0"},
        "mvp": "tbd",
        "rounds": PODZIM_ROUNDS,  # zatímní data z jarní sezóny
        "rounds_on_desktop": False,
    },
]

# ---------------------------------------------------------------------------
# Kontakty
# ---------------------------------------------------------------------------

CONTACTS = {
    "heading": "kontakty",
    "links": [
        {"label": "vysledky.cmbs.cz", "href": "https://vysledky.cmbs.cz/tournament-series/825"},
        {"label": "Facebook", "href": "https://www.facebook.com/KSUbrno/"},
    ],
    "organizer": {"label": "DELTA Billiard Brno", "href": "https://www.skdeltabilliard.cz/"},
    "venue": {"label": "Sborovna, Botanická 1, Brno", "href": "https://maps.app.goo.gl/g8CgVayHXHxy88f68"},
    "logos": [
        {"image": "images/DELTA.svg", "href": "https://www.skdeltabilliard.cz/", "alt": "Logotyp DELTA Billiard Brno", "css_class": "logo-delta"},
        {"image": "images/MUNI.svg", "href": "https://www.muni.cz/", "alt": "Logotyp MUNI", "css_class": "logo-muni"},
        {"image": "images/VUT.svg", "href": "https://www.vut.cz/", "alt": "Logotyp VUT", "css_class": "logo-vut"},
        {"image": "images/Sborovna.svg", "href": "https://sborovnabrno.cz/", "alt": "Logotyp Sborovna", "css_class": "logo-delta"},
    ],
    "footer": ["© 2026 DELTA Billiard Brno", "Design: Jakub Rendla"],
}

# ---------------------------------------------------------------------------
# Strukturovaná data (JSON-LD) pro vyhledávače
# ---------------------------------------------------------------------------
# Loga musí být absolutní URL — zatím míří na původní Webflow CDN.
# Po nasazení na vlastní doménu je změňte na vlastní.

CDN = "https://cdn.prod.website-files.com/696f3be1f2e5e2de338f5f92"

JSONLD = {
    "@context": "https://schema.org",
    "@type": "SportsEvent",
    "name": "Kulečníkový souboj univerzit",
    "description": (
        "Otevřená série pěti turnajů pro studenty MUNI a VUT ročníku 2025/2026. "
        "Hráči mohou být aktivními členy ČMBS. Na konci série bude vyhlášena "
        "vítězná univerzita."
    ),
    "url": "/",
    "image": [
        f"{CDN}/696f3e8ee52350ac4da98246_KSU-logotype.svg",
        f"{CDN}/696f6c0f51975c7773305a27_KSU-logotype-vertical.svg",
    ],
    "location": {
        "@type": "Place",
        "name": "Sborovna",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Botanická 1",
            "addressLocality": "Brno",
            "addressCountry": "CZ",
        },
    },
    "organizer": {
        "@type": "SportsOrganization",
        "name": "DELTA Billiard Brno",
        "url": "https://www.skdeltabilliard.cz/",
        "logo": {"@type": "ImageObject", "url": f"{CDN}/696f647f82688aabad755029_DELTA.svg"},
    },
    "competitor": [
        {
            "@type": "SportsTeam",
            "name": "MUNI",
            "logo": {"@type": "ImageObject", "url": f"{CDN}/696f647ffb9d3a3ea211724f_MUNI.svg"},
        },
        {
            "@type": "SportsTeam",
            "name": "VUT",
            "logo": {"@type": "ImageObject", "url": f"{CDN}/696f647ff88f0311fd6d6218_VUT.svg"},
        },
    ],
    # Data jednotlivých kol — aktualizujte pro novou sezónu.
    "subEvent": [
        {"name": "Kulečníkový souboj univerzit - 1. kolo", "startDate": "2025-02-22T18:00:00"},
        {"name": "Kulečníkový souboj univerzit - 2. kolo", "startDate": "2025-03-15T18:00:00"},
        {"name": "Kulečníkový souboj univerzit - 3. kolo", "startDate": "2025-04-05T18:00:00"},
        {"name": "Kulečníkový souboj univerzit - 4. kolo", "startDate": "2025-04-26T18:00:00"},
        {"name": "Kulečníkový souboj univerzit - 5. kolo", "startDate": "2025-05-17T18:00:00"},
    ],
    "offers": {
        "@type": "Offer",
        "description": (
            "Putovní pohár pro vítěznou univerzitu, štítek na trofeji pro MVP "
            "série a vítěze jednotlivých turnajů, roční členství v DELTA Billiard "
            "Brno a ČMBS v hodnotě 1 200 Kč pro 3 nejlepší hráče série"
        ),
    },
    "sameAs": [
        "https://vysledky.cmbs.cz/tournament-series/825",
        "https://www.facebook.com/KSUbrno/",
    ],
}
