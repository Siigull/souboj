# Kulečníkový souboj univerzit

Statický jednostránkový web — předělán z Webflow na vlastní minimalistický
generátor bez jakýchkoli závislostí (pouze standardní knihovna Pythonu).

## Použití

```bash
python3 build.py          # vygeneruje web do ./dist
python3 build.py --serve  # vygeneruje a spustí lokální server na http://localhost:8000
```

Publikování: obsah adresáře `dist/` nahrajete kamkoliv (GitHub Pages,
Netlify, vlastní hosting…) — je to čistě statické HTML/CSS/JS.

## Struktura

```
build.py      generátor — renderuje stránku a kopíruje assety do dist/
data.py       VEŠKERÝ OBSAH WEBU — editujte tento soubor
assets/       statické soubory (css, js, obrázky, fonty) — kopírují se 1:1
dist/         vygenerovaný web (nevkládat do gitu)
```

## Úprava obsahu

- **výsledky, skóre, MVP** → `data.py` → `SEASONS` a seznamy kol
  (`JARO_ROUNDS` / `PODZIM_ROUNDS`; mobilní seznamy i desktopové sloupce
  se odvozují automaticky z jednoho zdroje dat)
- **kola nadcházející sezóny** → přidejte kolo s `"url"` a prázdnými
  `"results"` — zobrazí se jako odkaz na turnaj; po odehrání doplňte
  `"results"` a listina se zobrazí sama
- **termíny, ceny, texty** → `data.py` → `SCHEDULE`, `INTRO_PARAGRAPHS`
- **odpočet do dalšího turnaje** → `data.py` → `COUNTDOWN` (starty kol
  včetně časové zóny a odkazy na registraci; sekce pod úvodním logem
  přežívá `next` = odpočet + registrace, `live` = „právě se hraje" +
  živé výsledky, `done` = výsledky série — bez JavaScriptu se použije
  stav zjištěný v okamžiku sestavení)
- **odkazy a loga** → `data.py` → `CONTACTS`
- **strukturovaná data pro vyhledávače (JSON-LD)** → `data.py` → `JSONLD`

Nová sezóna = přidat položku do `SEASONS` (pozor: pro třetí tab je potřeba
doplnit CSS pravidlo `.tab-link-tab-3`, srovnejte s `.tab-link-tab-2`
v `assets/css/main.css`).

## Poznámky

- Databáze výsledků na `vysledky.cmbs.cz` zůstává zdrojem pravdy pro
  kolo/sezónu; tady se jen zobrazují vybrané závěrečné listiny.
- `og:image` a loga v JSON-LD musí být absolutní URL — zatím míří na
  původní Webflow CDN. Po nasazení na vlastní doménu je změňte v `data.py`.
- Oproti původnímu webu byly opraveny drobné nekonzistence: překlep v
  `<title>` (soubor → souboj), pravopis "Martin Benovič" a "Matej Kubík"
  v mobilních listinách a pořadí 5. kola (původní web uváděl jiného
  vítěze na desktopu a na mobilu; platí desktopová listina).
- Sekce s odpočtem vychází vizuálně z turnajového plakátu (`poster.svg`
  v kořenu): antracitový pruh s krémovou typografií a výřez ilustrace
  herny (`assets/images/sborovna-scene.svg`, vytvořený z `poster.svg`
  změnou `viewBox` — po změně plakátu jej přegenerujte stejným postupem).
