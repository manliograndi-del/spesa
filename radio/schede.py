"""Costruisce le schede delle 10 radio più ascoltate di ogni paese e le scrive in radio/schede.json.

Fonti, in quest'ordine di fiducia (a Wikimedia si fanno poche richieste grandi):
  1. radio-browser.info  (archivio aperto): ascolti, voti, flusso, lingua, generi, sito
  2. Wikidata            (dati liberi CC0): fondazione, proprietà, sede, frequenze, logo, social
  3. Wikipedia           (CC BY-SA, citata con link): il riassunto della voce
  4. il sito della radio : come si presenta (meta description), immagine, social

Uso:  python radio/schede.py            (usa la cache in radio/.cache)
      python radio/schede.py --nuovo    (riscarica tutto)
"""
import concurrent.futures as cf
import html, json, os, re, sys, time, urllib.parse
from datetime import date
import requests

QUI = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(QUI, ".cache")
os.makedirs(CACHE, exist_ok=True)
NUOVO = "--nuovo" in sys.argv
PER_PAESE = 10      # le più ascoltate di ogni paese
MINIMO = 5          # sotto questo numero di radio il paese si lascia stare
UA = {"User-Agent": "EtereRadio/1.0 (schede delle radio; script personale)"}
S = requests.Session(); S.headers.update(UA)


def cache(nome, fn):
    p = os.path.join(CACHE, nome)
    if os.path.exists(p) and not NUOVO:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    v = fn()
    with open(p, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False)
    return v


import threading
_lucchetto, _ultima = threading.Lock(), [0.0]
def cortese(url, params=None, timeout=60, pausa=1.1):
    """Richiesta a Wikimedia: al massimo una ogni `pausa` secondi, e rispetta Retry-After."""
    for tentativo in range(8):
        with _lucchetto:
            attesa = _ultima[0] + pausa - time.time()
            if attesa > 0:
                time.sleep(attesa)
            _ultima[0] = time.time()
        try:
            r = S.get(url, params=params, timeout=timeout)
        except requests.RequestException:
            time.sleep(5 * (tentativo + 1)); continue
        if r.status_code == 429 or r.status_code >= 500:
            ra = r.headers.get("Retry-After")
            dorme = int(ra) + 2 if ra and ra.isdigit() else 20 * (tentativo + 1)
            print(f"    Wikimedia chiede di aspettare {dorme}s")
            with _lucchetto:
                _ultima[0] = time.time() + dorme
            continue
        return r
    raise SystemExit("Wikimedia non risponde: riprova più tardi (la cache dei passi fatti resta).")


def cache_mappa(nome, chiavi, fn):
    """Cache a pezzi: fn(lista_di_chiavi_mancanti) -> dict. Salva quello che ha, rifà solo il resto."""
    p = os.path.join(CACHE, nome)
    v = {}
    if os.path.exists(p) and not NUOVO:
        with open(p, encoding="utf-8") as f:
            v = json.load(f)
    mancanti = [k for k in dict.fromkeys(chiavi) if k not in v]
    for i in range(0, len(mancanti), 100):          # salva a pezzi: se si interrompe, riparte da qui
        v.update(fn(mancanti[i:i + 100]))
        with open(p, "w", encoding="utf-8") as f:
            json.dump(v, f, ensure_ascii=False)
        if len(mancanti) > 100:
            print(f"    {nome}: {min(i + 100, len(mancanti))} di {len(mancanti)}", flush=True)
    return v


def dominio(u):
    try:
        h = urllib.parse.urlsplit(u.strip()).hostname or ""
    except ValueError:
        return ""
    h = h.lower()
    for p in ("www.", "www2.", "m."):
        if h.startswith(p):
            h = h[len(p):]
    return h


def norma(t):
    t = re.sub(r"\(.*?\)|\[.*?\]", " ", (t or "").lower())
    t = re.sub(r"\b(radio|fm|am|live|stream|hd|online|mhz|\d+k|kbps|aac|mp3)\b", " ", t)
    return re.sub(r"[^0-9a-zà-ÿ]+", "", t)


def simile(a, b):
    a, b = norma(a), norma(b)
    if not a or not b:
        return 0
    if a == b:
        return 1
    if a in b or b in a:
        return min(len(a), len(b)) / max(len(a), len(b)) + 0.3
    return 0


# ---------------------------------------------------------------- 1. radio-browser
def scarica_rb():
    r = S.get("https://de1.api.radio-browser.info/json/stations/search",
              params={"limit": 200000, "is_https": "true", "hidebroken": "true",
                      "order": "clickcount", "reverse": "true"}, timeout=240)
    return r.json()

print("1/5 radio-browser…")
rb = cache("radiobrowser_tutte.json", scarica_rb)
per_paese, visti = {}, set()
for s in rb:
    nome = " ".join((s.get("name") or "").split())
    cc = s.get("countrycode") or ""
    k = (norma(nome) or nome.lower(), cc)
    if not nome or not cc or k in visti or not (s.get("clickcount") or 0) > 0:
        continue
    visti.add(k)
    per_paese.setdefault(cc, []).append(s)
scelte, saltati = [], []
for cc, lista in per_paese.items():
    if len(lista) < MINIMO:
        saltati.append(cc)
        continue
    lista.sort(key=lambda s: (-(s.get("clickcount") or 0), -(s.get("votes") or 0)))
    for i, s in enumerate(lista[:PER_PAESE], 1):
        s["_pos_paese"] = i
        scelte.append(s)
scelte.sort(key=lambda s: -(s.get("clickcount") or 0))
print("   ", len(scelte), "radio da", len(per_paese) - len(saltati), "paesi;",
      len(saltati), "paesi lasciati stare (meno di", MINIMO, "radio)")

# ---------------------------------------------------------------- 2. Wikidata (poche query grandi, niente raffiche)
SPARQL_URL = "https://query.wikidata.org/sparql"

def sparql(q):
    for tentativo in range(6):
        try:
            r = S.post(SPARQL_URL, data={"query": q, "format": "json"}, timeout=180,
                       headers={"Accept": "application/sparql-results+json"})
            if r.status_code == 429:
                time.sleep(int(r.headers.get("Retry-After") or 30) + 2); continue
            r.raise_for_status()
            return [{k: v["value"] for k, v in b.items()} for b in r.json()["results"]["bindings"]]
        except Exception as ex:
            dettaglio = getattr(getattr(ex, "response", None), "text", "") or ""
            print("    SPARQL riprovo:", type(ex).__name__, " ".join(dettaglio[:300].split()))
            if getattr(getattr(ex, "response", None), "status_code", 0) == 400:
                raise SystemExit("Query SPARQL non valida: " + " ".join(q[:600].split()))
            time.sleep(10 * (tentativo + 1))
    raise SystemExit("Il servizio di query di Wikidata non risponde: riprova più tardi.")

def qid(uri):
    return uri.rsplit("/", 1)[1]

print("2/5 Wikidata…")
wd_siti = cache("wikidata_siti.json", lambda: [[qid(b["s"]), b["web"]] for b in sparql(
    "SELECT ?s ?web WHERE { ?s wdt:P31/wdt:P279* wd:Q14350 . ?s wdt:P856 ?web . }")])
per_dominio = {}
for q, web in wd_siti:
    d = dominio(web)
    if d:
        per_dominio.setdefault(d, set()).add(q)

nomi_wd = cache("wikidata_nomi.json", lambda: [[qid(b["s"]), b["l"], b["iso"]] for b in sparql(
    """SELECT ?s ?l ?iso WHERE { ?s wdt:P31/wdt:P279* wd:Q14350 ; wdt:P17 ?c . ?c wdt:P297 ?iso .
       { ?s rdfs:label ?l } UNION { ?s skos:altLabel ?l } }""")])
etichette_di, per_nome_paese = {}, {}
for q, l, iso in nomi_wd:
    etichette_di.setdefault(q, set()).add(l)
    n = norma(l)
    if n:
        per_nome_paese.setdefault((n, iso), set()).add(q)

radio_per_dominio = {}
for s in scelte:
    d = dominio(s.get("homepage") or "")
    radio_per_dominio[d] = radio_per_dominio.get(d, 0) + 1

collegati, come = {}, {"sito": 0, "nome": 0}
for s in scelte:
    u, nome, cc = s["stationuuid"], s["name"], s.get("countrycode") or ""
    d = dominio(s.get("homepage") or "")
    cand = sorted(per_dominio.get(d, ())) if d else []
    meglio, vm = None, 0
    if 0 < len(cand) <= 15:
        for q in cand:
            v = max([simile(nome, x) for x in etichette_di.get(q, ())] or [0])
            if len(cand) == 1 and radio_per_dominio.get(d, 0) == 1:
                v = max(v, 0.6)          # una sola radio su quel sito, da entrambe le parti: quasi certamente lei
            if v > vm:
                meglio, vm = q, v
        if vm < 0.6:
            meglio = None
        if meglio:
            come["sito"] += 1
    if not meglio:
        trovati = per_nome_paese.get((norma(nome), cc), set())
        if len(trovati) == 1:            # stesso nome, stesso paese, e non ambiguo
            meglio = next(iter(trovati)); come["nome"] += 1
    if meglio:
        collegati[u] = meglio
print("    collegate a Wikidata:", len(collegati), "(dal sito", come["sito"], "| dal nome", come["nome"], ")")

collegati = {u: q for u, q in collegati.items() if re.fullmatch(r"Q\d+", q)}
QS = sorted(set(collegati.values()))

def a_pezzi(corpo, chiave, pezzo=100):
    """Esegue la query `corpo` (che usa ?s) per tutti i QID, a pezzi di 300, con cache."""
    def fn(qs):
        out = {q: [] for q in qs}
        righe = sparql("SELECT * WHERE { VALUES ?s { " + " ".join("wd:" + q for q in qs) + " } " + corpo + " }")
        for r in righe:
            out[qid(r.pop("s"))].append(r)
        return out
    return cache_mappa(f"wd_{chiave}.json", QS, lambda m: {k: v for i in range(0, len(m), pezzo) for k, v in fn(m[i:i + pezzo]).items()})

LAB = 'rdfs:label ?v . FILTER(LANG(?v) IN ("it","en")) BIND(LANG(?v) AS ?l)'
dati = {
    "nome":      a_pezzi('?s ' + LAB, "nome"),
    "descr":     a_pezzi('?s schema:description ?v . FILTER(LANG(?v) IN ("it","en")) BIND(LANG(?v) AS ?l)', "descr"),
    "fondata":   a_pezzi("?s wdt:P571 ?v", "fondata"),
    "chiusa":    a_pezzi("?s wdt:P576 ?v", "chiusa"),
    "proprieta": a_pezzi("?s wdt:P127|wdt:P749 ?o . ?o " + LAB, "proprieta"),
    "sede":      a_pezzi("?s wdt:P159|wdt:P131 ?o . ?o " + LAB, "sede"),
    "generi":    a_pezzi("?s wdt:P136 ?o . ?o " + LAB, "generi"),
    "lingue":    a_pezzi("?s wdt:P407|wdt:P2936 ?o . ?o " + LAB, "lingue"),
    "logo":      a_pezzi("?s wdt:P154 ?v", "logo"),
    "social":    a_pezzi("VALUES (?p ?k) { (wdt:P2003 'instagram') (wdt:P2013 'facebook') (wdt:P2002 'x') "
                         "(wdt:P2397 'youtube') (wdt:P7085 'tiktok') } ?s ?p ?v", "social"),
    "frequenze": a_pezzi("?s p:P2144 ?st . ?st psv:P2144 ?n . ?n wikibase:quantityAmount ?a ; wikibase:quantityUnit ?u . "
                         "OPTIONAL { ?st pq:P276|pq:P131 ?o . ?o " + LAB.replace("?v", "?dove").replace("?l)", "?ld)") + " }",
                         "frequenze"),
    "wiki":      a_pezzi("?art schema:about ?s ; schema:name ?t ; schema:inLanguage ?l . "
                         "FILTER(CONTAINS(STR(?art), '.wikipedia.org/'))", "wiki", pezzo=25),
}

def preferisci_it(righe, campo="v"):
    """Da righe con ?o (oggetto) ?v (etichetta) ?l (lingua): una etichetta per oggetto, italiano se c'è."""
    per_o = {}
    for r in righe:
        k = r.get("o", r.get(campo))
        if k not in per_o or r.get("l") == "it":
            per_o[k] = r[campo]
    return list(dict.fromkeys(per_o.values()))

def uno_it(righe):
    it = [r["v"] for r in righe if r.get("l") == "it"]
    return (it or [r["v"] for r in righe] or [""])[0]

def anno(v):
    m = re.match(r"-?(\d{4})-", v or "")
    return int(m.group(1)) if m else None

def mhz_di(a, u):
    a = float(a)
    if u.endswith("Q732707"):  return a          # megahertz
    if u.endswith("Q2143992"): return a / 1000   # kilohertz
    if u.endswith("Q39369"):   return a / 1e6    # hertz
    return a if 60 < a < 120 else (a / 1000 if 150 < a < 30000 else None)

info = {}
for q in QS:
    freq, visti = [], set()
    righe_f = sorted(dati["frequenze"].get(q, []), key=lambda r: r.get("ld") != "it")   # prima le etichette italiane
    luoghi_visti = set()
    for r in righe_f:
        chiave_l = (r["a"], r.get("o", ""))
        if chiave_l in luoghi_visti:
            continue
        luoghi_visti.add(chiave_l)
        try:
            m = mhz_di(r["a"], r.get("u", ""))
        except ValueError:
            m = None
        if m is None:
            continue
        f = f"{m:.1f} FM" if m >= 60 else f"{round(m * 1000)} AM"
        dove = r.get("dove", "")
        if (f, dove) in visti:
            continue
        visti.add((f, dove)); freq.append({"f": f, "dove": dove})
    social = {}
    for r in dati["social"].get(q, []):
        social.setdefault(r["k"], ("channel/" + r["v"]) if r["k"] == "youtube" else r["v"])
    info[q] = {
        "nome": uno_it(dati["nome"].get(q, [])),
        "descr": uno_it(dati["descr"].get(q, [])),
        "fondata": min([a for a in (anno(r["v"]) for r in dati["fondata"].get(q, [])) if a] or [None], key=lambda x: x or 9999),
        "chiusa": next((a for a in (anno(r["v"]) for r in dati["chiusa"].get(q, [])) if a), None),
        "proprieta": preferisci_it(dati["proprieta"].get(q, []))[:3],
        "sede": (preferisci_it(dati["sede"].get(q, [])) or [""])[0],
        "generi": preferisci_it(dati["generi"].get(q, []))[:4],
        "lingue": preferisci_it(dati["lingue"].get(q, []))[:3],
        "logo": next((r["v"].replace("http://", "https://") + "?width=256" for r in dati["logo"].get(q, [])), ""),
        "social": social,
        "frequenze": freq[:8],
        "wiki": {r["l"]: r["t"] for r in dati["wiki"].get(q, [])},
    }

# ---------------------------------------------------------------- 3. Wikipedia (riassunti a gruppi di 20)
lavori = {}
for s in scelte:
    q = collegati.get(s["stationuuid"])
    if not q:
        continue
    wk = info[q]["wiki"]
    lr = (s.get("languagecodes") or "").split(",")[0].strip()
    for l in ("it", "en", lr):           # prima ciò che si legge meglio in italiano
        if l and l in wk:
            lavori[q] = (l, wk[l]); break

def scarica_wikipedia(qs):
    out = {q: {} for q in qs}
    per_lingua = {}
    for q in qs:
        l, t = lavori[q]
        per_lingua.setdefault(l, []).append((q, t))
    for l, voci in per_lingua.items():
        for i in range(0, len(voci), 20):
            gruppo = voci[i:i + 20]
            r = cortese(f"https://{l}.wikipedia.org/w/api.php", params={
                "action": "query", "prop": "extracts", "exintro": 1, "explaintext": 1, "exlimit": 20,
                "redirects": 1, "titles": "|".join(t for _, t in gruppo), "format": "json", "formatversion": 2})
            try:
                j = r.json()["query"]
            except Exception:
                continue
            mappa = {}
            for x in j.get("normalized", []) + j.get("redirects", []):
                mappa[x["from"]] = x["to"]
            testi = {p["title"]: p.get("extract", "") for p in j.get("pages", [])}
            for q, t in gruppo:
                tt = mappa.get(mappa.get(t, t), mappa.get(t, t))
                if testi.get(tt):
                    out[q] = {"lingua": l, "titolo": tt, "estratto": testi[tt],
                              "url": f"https://{l}.wikipedia.org/wiki/" + urllib.parse.quote(tt.replace(" ", "_"))}
    return out

print("3/5 Wikipedia…")
wp = cache_mappa("wikipedia_riassunti_it_en.json", list(lavori), scarica_wikipedia)
print("    voci trovate:", sum(1 for q in lavori if (wp.get(q) or {}).get("estratto")))

# ---------------------------------------------------------------- 4. i siti delle radio
SOCIAL = {
    "instagram": r"https?://(?:www\.)?instagram\.com/([A-Za-z0-9_.]{2,30})/?(?=[\"'?#\s])",
    "facebook": r"https?://(?:www\.|[a-z]{2}-[a-z]{2}\.)?facebook\.com/(?!sharer|share|dialog|plugins|tr\b|events|groups/)([A-Za-z0-9_.\-]{2,60})/?(?=[\"'?#\s])",
    "x": r"https?://(?:www\.)?(?:twitter|x)\.com/(?!share|intent|home|search|hashtag)([A-Za-z0-9_]{1,15})/?(?=[\"'?#\s])",
    "youtube": r"https?://(?:www\.)?youtube\.com/((?:channel/|c/|user/|@)[A-Za-z0-9_\-.]{2,60})/?(?=[\"'?#\s])",
    "tiktok": r"https?://(?:www\.)?tiktok\.com/@([A-Za-z0-9_.]{2,30})/?(?=[\"'?#\s])",
}

def meta(htmltxt, *nomi):
    for n in nomi:
        for pat in (r'<meta[^>]+(?:name|property)\s*=\s*["\']%s["\'][^>]*content\s*=\s*["\']([^"\']*)["\']',
                    r'<meta[^>]+content\s*=\s*["\']([^"\']*)["\'][^>]*(?:name|property)\s*=\s*["\']%s["\']'):
            m = re.search(pat % re.escape(n), htmltxt, re.I)
            if m and m.group(1).strip():
                return html.unescape(m.group(1)).strip()
    return ""

def leggi_sito(s):
    url = s.get("homepage") or ""
    if not url.startswith("http"):
        return s["stationuuid"], None
    try:
        r = S.get(url, timeout=12, stream=True, allow_redirects=True,
                  headers={"Accept": "text/html", "Accept-Language": "it,en;q=0.8"})
        if "html" not in (r.headers.get("content-type") or ""):
            return s["stationuuid"], {"stato": r.status_code, "finale": r.url}
        corpo = b""
        for pezzo in r.iter_content(65536):
            corpo += pezzo
            if len(corpo) > 900_000:
                break
        cod = None
        if "charset=" in (r.headers.get("content-type") or "").lower():
            cod = r.encoding
        if not cod:
            m = re.search(rb'<meta[^>]+charset\s*=\s*["\']?([A-Za-z0-9_\-]+)', corpo[:4000], re.I)
            cod = m.group(1).decode() if m else "utf-8"
        try:
            t = corpo.decode(cod, errors="replace")
        except LookupError:
            t = corpo.decode("utf-8", errors="replace")
    except Exception as ex:
        return s["stationuuid"], {"errore": type(ex).__name__}
    tit = re.search(r"<title[^>]*>(.*?)</title>", t, re.I | re.S)
    out = {
        "stato": r.status_code,
        "finale": r.url,
        "titolo": html.unescape(" ".join(tit.group(1).split()))[:160] if tit else "",
        "descrizione": meta(t, "og:description", "description", "twitter:description")[:400],
        "nome_sito": meta(t, "og:site_name", "application-name")[:80],
        "immagine": meta(t, "og:image", "twitter:image"),
        "lingua": (re.search(r"<html[^>]*\blang\s*=\s*[\"']([A-Za-z\-]+)", t, re.I) or [None, ""])[1],
        "social": {},
    }
    if out["immagine"] and not out["immagine"].startswith("http"):
        out["immagine"] = urllib.parse.urljoin(r.url, out["immagine"])
    ic = re.findall(r'<link[^>]+rel\s*=\s*["\'](?:apple-touch-icon|icon)[^"\']*["\'][^>]*>', t, re.I)
    migliore, lato = "", 0
    for tag in ic:
        h = re.search(r'href\s*=\s*["\']([^"\']+)', tag)
        if not h:
            continue
        sz = re.search(r'sizes\s*=\s*["\'](\d+)', tag)
        n = int(sz.group(1)) if sz else (180 if "apple" in tag.lower() else 32)
        if n > lato:
            migliore, lato = urllib.parse.urljoin(r.url, html.unescape(h.group(1))), n
    out["icona"] = migliore
    for nome_s, pat in SOCIAL.items():
        trovati = re.findall(pat, t)
        trovati = [x for x in trovati if x.lower() not in ("p", "reel", "explore", "watch", "embed", "pages", "profile.php")]
        if trovati:
            out["social"][nome_s] = max(set(trovati), key=trovati.count)
    return s["stationuuid"], out

def scarica_siti(uuids):
    per_u = {s["stationuuid"]: s for s in scelte}
    out = {}
    with cf.ThreadPoolExecutor(24) as ex:
        for i, (u, v) in enumerate(ex.map(leggi_sito, [per_u[u] for u in uuids])):
            out[u] = v
            if i % 200 == 0:
                print("    siti letti:", i, "di", len(uuids))
    return out

print("4/5 siti delle radio…")
siti = cache_mappa("siti.json", [s["stationuuid"] for s in scelte], scarica_siti)
print("    siti che rispondono:", sum(1 for v in siti.values() if v and v.get("titolo")))

# ---------------------------------------------------------------- 5. le schede
def frasi(t, n=3, massimo=520):
    parti = re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-Ý0-9«\"])|(?<=[。！？])", (t or "").strip().split("\n")[0])
    out = ""
    for p in parti[:n]:
        if len(out) + len(p) > massimo and out:
            break
        out = (out + " " + p).strip()
    return out

def https(u):
    return u if isinstance(u, str) and u.startswith("https://") else ""

SOCIAL_HOST = ("facebook.com", "instagram.com", "twitter.com", "x.com", "youtube.com", "tiktok.com", "linktr.ee")

def pulisci_descr(d, sito):
    d = " ".join((d or "").split())
    if any(h in dominio(sito or "") for h in SOCIAL_HOST):
        return ""                     # la "descrizione" di una pagina social non è della radio
    if len(d) < 25 or d.lower().startswith(("http", "{", "<")) or "�" in d or re.search(r"Ã.|Ø.", d):
        return ""
    return d

schede, fonti_conte = {}, {"wikidata": 0, "wikipedia": 0, "sito": 0}
for pos, s in enumerate(scelte, 1):          # pos = posto fra tutte le schede, per ascolti
    u = s["stationuuid"]
    q = collegati.get(u)
    e = info.get(q, {}) if q else {}
    w = wp.get(q) if q else None
    si = siti.get(u) or {}
    fonti = ["radio-browser"]
    if e: fonti.append("wikidata"); fonti_conte["wikidata"] += 1
    if w and w.get("estratto"): fonti.append("wikipedia"); fonti_conte["wikipedia"] += 1
    if si.get("titolo") or si.get("descrizione"): fonti.append("sito"); fonti_conte["sito"] += 1

    social = dict(e.get("social") or {})
    for k, v in (si.get("social") or {}).items():
        social.setdefault(k, v)

    sch = {
        "pos": pos,
        "pos_paese": s["_pos_paese"],
        "nome": " ".join(s["name"].split()),
        "nome_ufficiale": e.get("nome", ""),
        "paese": s.get("countrycode") or "",
        "regione": (s.get("state") or "").strip(),
        "sede": e.get("sede", ""),
        "fondata": e.get("fondata"),
        "chiusa": e.get("chiusa"),
        "proprieta": e.get("proprieta", []),
        "generi": e.get("generi", []),
        "tag": [t.strip() for t in (s.get("tags") or "").split(",") if t.strip()][:6],
        "lingue": e.get("lingue") or [l.strip().title() for l in (s.get("language") or "").split(",") if l.strip()][:3],
        "frequenze": e.get("frequenze", []),
        "breve": e.get("descr", ""),
        "wikipedia": {"testo": frasi(w["estratto"]), "url": w["url"], "lingua": w["lingua"]} if w and w.get("estratto") else None,
        "dal_sito": pulisci_descr(si.get("descrizione"), si.get("finale") or s.get("homepage")),
        "sito": s.get("homepage") or "",
        "logo": e.get("logo", ""),
        "immagine": https(si.get("immagine")),
        "icona": https(si.get("icona")) or https(s.get("favicon")),
        "social": social,
        "flusso": {"codec": s.get("codec") or "", "kbps": s.get("bitrate") or 0, "hls": bool(s.get("hls"))},
        "ascolti": s.get("clickcount") or 0,
        "tendenza": s.get("clicktrend") or 0,
        "voti": s.get("votes") or 0,
        "wikidata": q or "",
        "fonti": fonti,
    }
    campi = ["fondata", "sede", "proprieta", "frequenze", "logo", "social", "sito"]
    pieni = sum(1 for c in campi if sch[c]) + (1 if (sch["wikipedia"] or sch["dal_sito"]) else 0) + (1 if (sch["generi"] or sch["tag"]) else 0)
    sch["completezza"] = round(100 * pieni / (len(campi) + 2))
    schede[u] = sch

with open(os.path.join(QUI, "schede.json"), "w", encoding="utf-8") as f:
    json.dump({"aggiornate": date.today().isoformat(), "schede": schede}, f, ensure_ascii=False, separators=(",", ":"))
print("5/5 schede scritte:", len(schede), "| con Wikidata:", fonti_conte["wikidata"],
      "| con Wikipedia:", fonti_conte["wikipedia"], "| con il sito:", fonti_conte["sito"])
print("    completezza media:", round(sum(s["completezza"] for s in schede.values()) / len(schede)), "%")
