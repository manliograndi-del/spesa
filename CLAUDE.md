# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"Spesa" is a static, Italian-language PWA that compares supermarket flyer offers near Corso Siracusa (Turin) by **unit price** (per kg, litre, egg, roll, wash…), never by pack price. It is served by GitHub Pages at https://manliograndi-del.github.io/spesa/ (`.nojekyll`, no Pages build). All UI text, identifiers, CSS classes and storage keys are Italian; keep new code and copy in Italian.

## The files are generated output

Every file here is produced by a generator that is **not in this repository**. Each "Aggiornamento" commit rewrites `index.html`, `novita.html`, `storia/prezzi.csv`, `storia/prezzi.html`, `catalogo.pdf` and the cache name in `sw.js` together. Consequences:

- A hand edit to any of these files is lost at the next update unless the same change is made in the generator. Say so when a change only touches the output.
- There is no package.json, build, linter or test suite.

Local preview (the service worker needs http, and localhost works):

```sh
python3 -m http.server 8000   # then open http://localhost:8000/
```

The service worker serves cached assets, so hard-reload or unregister it in DevTools to see edits.

## Architecture

- **`index.html` (~2.4 MB) is the whole app.** The `<head>` holds the CSS, with theme tokens as custom properties on `:root` (`--carta`, `--inchiostro`, `--rosso`, `--verde`…). The body is static markup: header, product grid `#tasti`, search, the "Lista spesa" panel, and the dialogs (`.buio > .finestra`). Near the end, a single ~2.4 MB line holds one inline `<script>`: `const DATI={…}` (~2.3 MB of data), then ~55 KB of minified app code. Don't Read that line. Inspect it with `grep -o` or extract it with `sed -n '<line>p'` and parse it in node.
- **`DATI`**:
  - `offerte`: one record per offer, with fields `ins` store, `cat`/`rep` category/department, `pro` name, `fmt` format, `prezzo` pack price, `unitario` unit price, `inizio`/`fino` ISO dates, `bolli` condition badges, `prima` previous price, `pdf`/`pag`/`url` source flyer page, `marca`/`propria` brand.
  - `volantini`: one record per flyer, with a `modello` URL template for page images (`{n:05d}`).
  - `catalogo`: product entries with their search keywords, grouped by `reparti`.
  - `marche`/`marcheParole`/`marchiMarche`: big-brand grouping (e.g. Coca-Cola also covers Fanta and Sprite).
  - `loghi`: base64 webp store logos.
  - `look`: colour themes.
  - `novita`: the in-app changelog.
  - `letto`: the date the flyers were read.
- **`LISTA_PUBBLICATA`** (right after `DATI`) is the default product grid: `{nome, parole[], cat}`. An offer belongs to a product by keyword match on its name.
- **Navigation between pages:** `novita.html` (updated/upcoming flyers, price changes) links back with `./#vai=<sezione>` (`prodotti`, `marche`, `lista`, `cerca`, `config`). `index.html` reads that hash on load.
- **`storia/prezzi.csv`** holds the price history: `volantino,insegna,categoria,prodotto,formato,quantita,unita,prezzo,prezzo_unita,dal,al,note`, where `prezzo_unita = prezzo / quantita`. `storia/prezzi.html` charts the weekly lows from it.
- **`catalogo.pdf`** is a printable list of catalogue entries and their keywords. The user corrects it by hand to tune keyword matching.
- **`sw.js`**:
  - The cache is named `spesa-<hash>`. Pages are network-first; other same-origin GETs are cache-first. Old `spesa-*` caches are deleted on activate.
  - Change the hash whenever a precached file changes, or installed clients keep stale files.
  - `storia/` and `catalogo.pdf` are not precached.

## Behaviour to preserve

- Offers are ranked by `unitario`. The green "il meno caro valido oggi" card is the cheapest offer already started today. Offers that haven't started yet are faded. Expired offers disappear based on the device date.
- User state lives only in `localStorage`:
  - `spesa.lista.v1`: product list
  - `spesa.visti.v1`: names from `LISTA_PUBBLICATA` already seen, so newly published products get added to an existing list
  - `spesa.negozi.v1`: hidden stores
  - `spesa.personale.v1` / `spesa.personale.negozi.v1`: "Lista spesa" words and stores
  - `spesa.look.v1`: theme
  - `spesa.novita.v1`: changelog already seen

  Bump the `vN` suffix if a stored format changes.
- Some chains are read from one specific store's flyer: Mercatò via Filadelfia 232, Pam corso Orbassano 212, Conad via Cesana 78.
- Umami analytics runs only on `manliograndi-del.github.io`. `?noncontarmi` / `?contami` turns counting off/on for that device.
