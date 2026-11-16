"""Scarica da radio-browser.info (archivio aperto) le radio in https e scrive:
  radio/stazioni.json  quelle con la posizione (le luci sul globo)
  radio/altre.json     quelle senza posizione ma ascoltate (si trovano per paese e con la ricerca)
Uso:  python radio/aggiorna.py"""
import json, os, urllib.request

URL = ("https://de1.api.radio-browser.info/json/stations/search"
       "?limit=200000&is_https=true&hidebroken=true&order=clickcount&reverse=true")
CAMPI = ["nome", "lat", "lng", "url", "paese", "generi", "hls", "uuid", "sito", "icona", "ascolti"]

req = urllib.request.Request(URL, headers={"User-Agent": "EtereRadio/1.0"})
with urllib.request.urlopen(req, timeout=180) as r:
    dati = json.loads(r.read().decode("utf-8"))

visti, conpos, senza = set(), [], []
for s in dati:
    url = (s.get("url_resolved") or s.get("url") or "").strip()
    nome = " ".join((s.get("name") or "").split())
    if not url.startswith("https://") or not nome:
        continue
    geo = s.get("geo_lat") is not None and s.get("geo_long") is not None
    if not geo and not (s.get("clickcount") or 0) > 0:
        continue
    chiave = (nome.lower(), (s.get("countrycode") or ""), url)
    if chiave in visti:
        continue
    visti.add(chiave)
    fav = s.get("favicon") or ""
    sito = s.get("homepage") or ""
    tags = [t.strip() for t in (s.get("tags") or "").split(",") if t.strip()][:3]
    rec = [
        nome[:70],
        round(s["geo_lat"], 3) if geo else None,
        round(s["geo_long"], 3) if geo else None,
        url,
        s.get("countrycode") or "",
        ",".join(tags),
        1 if s.get("hls") else 0,
        s.get("stationuuid") or "",
        sito if sito.startswith("http") else "",
        fav if fav.startswith("https://") else "",
        s.get("clickcount") or 0,
    ]
    (conpos if geo else senza).append(rec)

cartella = os.path.dirname(os.path.abspath(__file__))
for nome_file, righe in (("stazioni.json", conpos), ("altre.json", senza)):
    with open(os.path.join(cartella, nome_file), "w", encoding="utf-8") as f:
        json.dump({"campi": CAMPI, "radio": righe}, f, ensure_ascii=False, separators=(",", ":"))
    print(len(righe), "radio in", nome_file)
