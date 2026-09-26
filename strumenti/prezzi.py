# -*- coding: utf-8 -*-
"""L'ARCHIVIO DEI PREZZI: ogni offerta mai letta, e il prezzo più basso di ogni
categoria, settimana per settimana.

Chiesto da Manlio il 2026-09-26: «un database di tutti i prodotti per avere
settimana per settimana i prezzi più bassi a cui sono stati venduti… una cosa
al di fuori di questa pagina». Deciso con lui: si parte dalle categorie del
catalogo, con dentro marca e formato di ogni offerta.

NON SI LEGGE NIENTE DI NUOVO. I prezzi stanno già in git: c'è una copia di
`dati.py` per ogni commit dal 4 settembre 2026, e un volantino scaduto, tolto
dalla pagina, resta nei commit di prima. Di ogni volantino vale l'ULTIMA copia
in cui compare, perché è quella con le correzioni.

Tre file, tutti in storia/, così il giro delle 7 (che aggiunge storia/ al suo
commit) li pubblica senza che nessuno cambi niente:
    storia/prezzi.csv    l'archivio, una riga per offerta
    storia/prezzi.json   fin dove è arrivato, e quando è comparso ogni volantino
    storia/prezzi.html   la pagina: scegli una categoria, vedi le settimane

L'ARCHIVIO CRESCE E BASTA. Un volantino che non si trova più nella storia di
git (un clone fatto a metà) resta com'era nel file. Si rifà da solo alla fine
di `python3 -m storia`; a mano: `python3 -m prezzi` (`--tutto` rilegge ogni
commit da capo).
"""
import csv, datetime, html, io, json, os, re, subprocess, sys, tarfile, tempfile

QUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOVE = os.path.join(QUI, 'storia')
CSV = os.path.join(DOVE, 'prezzi.csv')
META = os.path.join(DOVE, 'prezzi.json')
PAGINA = os.path.join(DOVE, 'prezzi.html')

CAMPI = ['volantino', 'insegna', 'categoria', 'prodotto', 'formato', 'quantita',
         'unita', 'prezzo', 'prezzo_unita', 'dal', 'al', 'note']

# Volantini che sono stati in dati.py ma NON valevano a Torino: edizioni di
# un'altra zona lette per sbaglio e poi sostituite. I loro prezzi sono veri, ma
# non erano in vendita nei nostri negozi: nell'archivio manderebbero uno a
# cercare un prezzo che qui non c'è mai stato.
ESCLUSI = {}

# Righe sbagliate nel dati.py di allora, già scaduto: si tolgono qui invece di
# riscrivere la storia. (volantino, prodotto) -> perché.
RIGHE_SBAGLIATE = {
    ('eurospin10', 'Tovaglioli Space monovelo, 450 pezzi'):
        'tovaglioli contati come rotoli di asciugatutto: 0,01 € «al rotolo»',
}


def git(*argomenti, testo=True):
    try:
        return subprocess.run(('git', '-C', QUI) + argomenti, check=True,
                              capture_output=True, text=testo).stdout
    except Exception:
        return None


def commit_di_dati():
    """I commit che hanno toccato i prezzi, dal PIÙ VECCHIO: [(sigla, data)]."""
    fuori = git('log', '--reverse', '--format=%H %cs', '--', 'strumenti/dati.py') or ''
    return [tuple(r.split()[:2]) for r in fuori.splitlines() if ' ' in r]


# Gira in un processo a parte, dentro la cartella `strumenti/` di quel momento:
# `dati` e `catalogo` di allora devono stare insieme. Tira fuori solo cose
# semplici, che hanno la stessa forma dal primo giorno.
_ESTRAI = r'''
import sys, json, os
os.chdir(sys.argv[1]); sys.path.insert(0, sys.argv[1])
import dati
vol = [[v[0], v[1], v[2], v[4], (v[6] if len(v) > 6 else None)] for v in dati.VOLANTINI]
unita = {k: (u[0] if isinstance(u, (list, tuple)) else u) for k, u in getattr(dati, 'UNITA', {}).items()}
righe = [list(r) for r in dati.PRODOTTI]
json.dump(dict(volantini=vol, unita=unita, righe=righe), sys.stdout, ensure_ascii=False, default=str)
'''


def leggi_cartella(cartella):
    fuori = subprocess.run((sys.executable, '-c', _ESTRAI, cartella), check=True,
                           capture_output=True, text=True).stdout
    return json.loads(fuori)


def leggi_commit(sigla):
    tar = git('archive', sigla, 'strumenti', testo=False)
    if not tar:
        return None
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(fileobj=io.BytesIO(tar)) as t:
            t.extractall(tmp)
        try:
            return leggi_cartella(os.path.join(tmp, 'strumenti'))
        except Exception as e:
            print(f'  prezzi: non riesco a leggere il commit {sigla[:7]}: {e}')
            return None


MESI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio',
        'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
_DAL_AL = re.compile(r"\bdal(?:l['’]|\s+)(\d{1,2})(?:\s+([a-z]+))?\s+al(?:l['’]|\s+)(\d{1,2})\s+([a-z]+)")


def primo_giorno(periodo, fino):
    """«dal 24 settembre al 7 ottobre» -> 2026-09-24. None se non si capisce.

    Serve ai volantini scritti senza `inizio` (vuol dire «già in corso» quando
    sono stati messi): il primo giorno sta scritto nel periodo."""
    if not fino:
        return None
    m = _DAL_AL.search((periodo or '').lower())
    if not m or m.group(4) not in MESI:
        return None
    mese_fine = MESI.index(m.group(4)) + 1
    mese = MESI.index(m.group(2)) + 1 if m.group(2) in MESI else mese_fine
    anno = int(fino[:4]) - (1 if mese > mese_fine else 0)
    try:
        d = datetime.date(anno, mese, int(m.group(1))).isoformat()
    except ValueError:
        return None
    return d if d <= fino else None


def _catalogo():
    sys.path.insert(0, os.path.join(QUI, 'strumenti'))
    import catalogo
    return catalogo


# La carne e il pesce lavorati hanno categorie loro solo dal 23 settembre: nei
# volantini di prima gli hamburger stavano col Manzo. Qui si rimettono al loro
# posto, con le stesse parole del controllo che sta in dati.py; se no il
# «Manzo più economico» di una settimana di inizio settembre sarebbe un
# hamburger surgelato.
_LAVORATI = [
    (('Manzo', 'Vitello', 'Suino', 'Pollo', 'Tacchino'), r'w[üu]rstel', 'Würstel'),
    (('Manzo', 'Vitello', 'Suino', 'Pollo', 'Tacchino'), r'affettat|al forno|arrosto a fette', 'Affettati'),
    (('Manzo', 'Vitello', 'Suino', 'Pollo', 'Tacchino'),
     r'hamburger|burger|polpett|cotolett|cordon|nuggets|spiedin|bombett|kebab|rollé', 'Preparati'),
    (('Salmone',), r'affumicat', 'Salmone affumicato'),
    (('Merluzzo', 'Pesce', 'Calamari', 'Gamberi', 'Salmone'),
     r'panat|impanat|croccol|croccant|burger|pastella|tempura|fritto misto|bastoncin', 'Panati'),
    (('Dentifricio',), r'collutorio', 'Collutorio'),
]
_FRESCHI_OMONIMI = re.compile(r'cotolette e nodini', re.I)


def categoria_di(cat, pro, rinominate):
    cat = rinominate.get(cat, cat)
    if _FRESCHI_OMONIMI.search(pro or ''):
        return cat
    for cats, rx, nuova in _LAVORATI:
        if cat in cats and re.search(rx, pro or '', re.I):
            return nuova
    return cat


def aggiorna(tutto=False):
    """Legge i commit nuovi (e la cartella di adesso) e riscrive i tre file."""
    os.makedirs(DOVE, exist_ok=True)
    cat_mod = _catalogo()
    rinominate = getattr(cat_mod, 'RINOMINATE', {})

    meta = {}
    if os.path.exists(META) and not tutto:
        meta = json.load(open(META, encoding='utf-8'))
    comparsi = meta.get('comparsi', {})          # chiave -> primo giorno visto
    righe = {}                                   # chiave -> [righe CSV]
    if os.path.exists(CSV) and not tutto:
        for r in csv.DictReader(open(CSV, encoding='utf-8', newline='')):
            righe.setdefault(r['volantino'], []).append(r)

    storia = commit_di_dati()
    sigle = [s for s, _ in storia]
    da = sigle.index(meta['ultimo']) + 1 if meta.get('ultimo') in sigle else 0
    versioni = [(s, g, None) for s, g in storia[da:]]
    # Per ultima la cartella com'è adesso: `storia` gira PRIMA del commit, e i
    # prezzi appena letti sono ancora solo lì.
    versioni.append((None, datetime.date.today().isoformat(), os.path.join(QUI, 'strumenti')))

    for sigla, giorno, cartella in versioni:
        try:
            d = leggi_cartella(cartella) if cartella else leggi_commit(sigla)
        except Exception as e:
            print(f'  prezzi: non riesco a leggere la cartella di adesso: {e}')
            d = None
        if not d:
            continue
        vol = {v[0]: v for v in d['volantini']}
        for chiave, (_, ins, periodo, fino, inizio) in vol.items():
            comparsi.setdefault(chiave, giorno)
            if chiave in ESCLUSI:
                righe.pop(chiave, None)
                continue
            dal_vol = inizio or primo_giorno(periodo, fino) or comparsi[chiave]
            nuove = []
            for r in d['righe']:
                if r[2] != chiave:
                    continue
                cat, _, _, _, pro, fmt, qta, prezzo = r[:8]
                if (chiave, pro) in RIGHE_SBAGLIATE:
                    continue
                note = r[10] if len(r) > 10 else ''
                dal = (r[11] if len(r) > 11 and r[11] else None) or dal_vol
                al = (r[12] if len(r) > 12 and r[12] else None) or fino
                try:
                    qta, prezzo = float(qta), float(prezzo)
                except (TypeError, ValueError):
                    continue
                if not qta or not prezzo:
                    continue
                nuove.append(dict(
                    volantino=chiave, insegna=ins,
                    categoria=categoria_di(cat, pro, rinominate), prodotto=pro,
                    formato=fmt, quantita=f'{qta:g}', unita=d['unita'].get(cat, ''),
                    prezzo=f'{prezzo:.2f}', prezzo_unita=f'{prezzo / qta:.3f}',
                    dal=dal, al=al or '', note=note or ''))
            righe[chiave] = nuove
        if sigla:
            meta['ultimo'] = sigla

    tutte = sorted((r for rr in righe.values() for r in rr),
                   key=lambda r: (r['dal'], r['volantino'], r['categoria'], r['prodotto']))
    with open(CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=CAMPI)
        w.writeheader()
        w.writerows(tutte)
    meta['comparsi'] = comparsi
    json.dump(meta, open(META, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    scrivi_pagina(tutte, cat_mod, min(comparsi.values()))
    print(f'prezzi: {len(tutte)} offerte di {len(righe)} volantini in storia/prezzi.csv')
    return tutte


# ------------------------------------------------------------ la pagina

_TESSERA = re.compile(r"Lidl Plus|Buona Spesa Card|Carta Insieme|[Ss]olo titolari|Eurospin Family|"
                      r"EKOM UP|SpesAmica|\bsoci\b|CARTA BENNET|Fidelity Card|PENNY ?Card|F[iì]daty|"
                      r"Perte Plus|\bcon APP\b|\bl'app\b|[Tt]essera", re.I)


def lunedi(d):
    return d - datetime.timedelta(days=d.weekday())


def settimane(tutte, cat_mod, primo, oggi=None):
    """Per ogni categoria del catalogo, settimana per settimana (da lunedì a
    domenica), le offerte più basse per unità valide almeno un giorno di quella
    settimana. Fino alla settimana in corso: le settimane che devono ancora
    venire hanno solo i volantini già usciti, e il «più basso» sarebbe falso."""
    oggi = oggi or datetime.date.today()
    unita = {v['nome']: cat_mod.METRI[v['unita']][0] for v in cat_mod.CATALOGO}
    fuori = {}
    for c, u in unita.items():
        offerte = [r for r in tutte if r['categoria'] == c and r['unita'] == u and r['dal']]
        if not offerte:
            continue
        # Si parte dalla settimana del primo giorno in cui c'è una copia dei
        # prezzi (4 settembre 2026): prima si sa solo dei volantini ancora in
        # corso quel giorno, e il «più basso» di quelle settimane sarebbe finto.
        w = max(lunedi(datetime.date.fromisoformat(min(r['dal'] for r in offerte))),
                lunedi(datetime.date.fromisoformat(primo)))
        fine = lunedi(oggi)
        elenco = []
        while w <= fine:
            dom = w + datetime.timedelta(days=6)
            dentro = [r for r in offerte
                      if r['dal'] <= dom.isoformat() and (r['al'] or '9') >= w.isoformat()]
            dentro.sort(key=lambda r: float(r['prezzo_unita']))
            if dentro:
                elenco.append(dict(w=w.isoformat(), o=[
                    [r['insegna'], r['prodotto'], r['formato'], float(r['prezzo']),
                     float(r['prezzo_unita']), r['dal'], r['al'],
                     1 if _TESSERA.search(r['note']) else 0]
                    for r in dentro[:5]], n=len(dentro)))
            w += datetime.timedelta(days=7)
        if elenco:
            fuori[c] = dict(u=u, s=elenco[::-1])
    return fuori


def scrivi_pagina(tutte, cat_mod, primo):
    dati = settimane(tutte, cat_mod, primo)
    reparti = []
    for v in cat_mod.CATALOGO:
        if v['nome'] not in dati:
            continue
        if not reparti or reparti[-1][0] != v['reparto']:
            reparti.append([v['reparto'], []])
        reparti[-1][1].append(v['nome'])
    try:
        from marche_proprie import MARCHE_PROPRIE
        proprie = {k: sorted(v) for k, v in MARCHE_PROPRIE.items()}
    except Exception:
        proprie = {}
    carico = json.dumps(dict(dati=dati, reparti=reparti, proprie=proprie,
                             offerte=len(tutte), inizio=primo,
                             oggi=datetime.date.today().isoformat()),
                        ensure_ascii=False, separators=(',', ':'))
    # Dentro uno script, «</» chiuderebbe lo script a metà (vincolo 3 di
    # CLAUDE.md): nei dati si scrive «<\/», che per JSON è la stessa cosa.
    carico = carico.replace('</', '<\\/')
    open(PAGINA, 'w', encoding='utf-8').write(MODELLO.replace('/*DATI*/', carico))


MODELLO = r'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#FFFFFF">
<title>Prezzi più bassi</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Asap:wght@400;500;600;700&family=Oswald:wght@500;600;700&display=swap">
<style>
/* Tema chiaro unico, come la Spesa: niente modalità scura automatica. */
:root{--carta:#FFFFFF;--pannello:#F6F5F2;--inchiostro:#1B1B1A;--tenue:#6E6C66;
  --linea:#E5E3DD;--rosso:#D40D2B;--verde:#1E7A4B;--beige:#F3EBDD;--beige-testo:#6B4E16;
  --f-testo:'Asap',system-ui,sans-serif;--f-prezzo:'Oswald','Arial Narrow',sans-serif}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--carta);color:var(--inchiostro);font-family:var(--f-testo);
  font-size:16px;line-height:1.35}
main{max-width:560px;margin:0 auto;padding:18px 16px 40px}
h1{font-family:var(--f-prezzo);font-weight:600;font-size:28px;line-height:1.1;margin:0}
.sotto{color:var(--tenue);font-size:14px;margin:6px 0 16px}
label{display:block;font-weight:600;font-size:14px;margin-bottom:6px}
select{width:100%;font:inherit;font-size:17px;padding:12px;border:1.5px solid var(--rosso);
  border-radius:10px;background:var(--carta);color:var(--inchiostro)}
.settimana{border:1.5px solid var(--linea);border-radius:16px;padding:12px 14px;margin-top:12px}
.settimana.adesso{border-color:var(--verde)}
.quando{display:flex;justify-content:space-between;gap:8px;font-size:13px;color:var(--tenue);
  text-transform:uppercase;letter-spacing:.05em;font-weight:600}
.quando .ora{color:var(--verde)}
.riga{display:flex;align-items:center;gap:12px;margin-top:6px}
.chi{flex:1;min-width:0}
.marca{display:block;font-size:12.5px;font-weight:700;letter-spacing:.07em;text-transform:uppercase}
.nome{display:block;font-weight:500}
.dove{display:block;color:var(--tenue);font-size:14px;margin-top:2px}
.pill{display:inline-block;background:var(--beige);color:var(--beige-testo);font-size:12px;
  font-weight:600;border-radius:99px;padding:2px 9px;margin-top:5px}
.prezzo{text-align:right;white-space:nowrap}
.prezzo b{font-family:var(--f-prezzo);font-size:26px;font-weight:600}
.prezzo span{display:block;color:var(--tenue);font-size:13px}
details{margin-top:8px}
summary{cursor:pointer;color:var(--tenue);font-size:14px}
.altre .riga{border-top:1px solid var(--linea);padding-top:6px}
.altre .prezzo b{font-size:19px}
/* Il grafico: una linea sola, il più basso di ogni settimana. Toccandolo si
   sceglie la settimana, e sotto compare la sua offerta. */
.grafico{margin-top:18px}
.grafico h2{font-size:15px;font-weight:600;margin:0}
.aiuto-g{color:var(--tenue);font-size:13px;margin:2px 0 6px}
#grafico{touch-action:pan-y;-webkit-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent}
#grafico svg{display:block;width:100%;height:auto;overflow:visible;cursor:pointer}
#grafico svg:focus{outline:none}
#grafico svg:focus-visible{outline:2px solid var(--inchiostro);outline-offset:4px;border-radius:8px}
#grafico .asse{font-family:var(--f-testo);font-size:12px;fill:#6E6C66}
#grafico .valore{font-family:var(--f-prezzo);font-size:17px;font-weight:600;fill:#1B1B1A}
#scelta .settimana{margin-top:6px}
.tutte{margin-top:18px}
.tutte > summary{font-weight:600;color:var(--inchiostro);font-size:15px}
.piede{color:var(--tenue);font-size:13px;margin-top:24px}
.piede a{color:var(--inchiostro)}
</style>
</head>
<body>
<main>
<h1>Prezzi più bassi, settimana per settimana</h1>
<p class="sotto" id="sotto"></p>
<label for="cat">Categoria</label>
<select id="cat"></select>
<section class="grafico">
<h2 id="titolo-g"></h2>
<p class="aiuto-g" id="aiuto-g"></p>
<div id="grafico"></div>
</section>
<div id="scelta"></div>
<details class="tutte"><summary>Tutte le settimane, una per una</summary><div id="elenco"></div></details>
<p class="piede">Sono solo i prezzi in offerta dei volantini, non quelli normali dello scaffale,
dei supermercati della Spesa. Per ogni settimana, da lunedì a domenica, c’è l’offerta che costava
meno per unità fra quelle valide almeno un giorno di quella settimana.
<a href="prezzi.csv" download>Scarica tutti i prezzi</a> (per un foglio di calcolo).</p>
</main>
<script>
const D = /*DATI*/;
const MESI = ['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto',
              'settembre','ottobre','novembre','dicembre'];
const giorno = iso => { const [a, m, g] = iso.split('-').map(Number); return new Date(a, m - 1, g); };
const piu = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
function tratto(da, a) {
  return da.getMonth() === a.getMonth()
    ? da.getDate() + '–' + a.getDate() + ' ' + MESI[a.getMonth()]
    : da.getDate() + ' ' + MESI[da.getMonth()] + ' – ' + a.getDate() + ' ' + MESI[a.getMonth()];
}
const eur = x => x.toFixed(2).replace('.', ',');
const UNITA = { 'al kg': '€ al kg', 'al litro': '€ al litro', "all'uovo": '€ a uovo',
                'al rotolo': '€ a rotolo', 'a lavaggio': '€ a lavaggio' };

/* «Nome – Marca, aggiunte» come nella Spesa: la marca sopra, e le marche
   proprie dei discount non si scrivono (Manlio, 2026-09-26). */
function titolo(ins, pro) {
  const i = pro.indexOf(' – ');
  if (i < 0) return { marca: '', nome: pro };
  const resto = pro.slice(i + 3), v = resto.indexOf(', ');
  let marca = v < 0 ? resto : resto.slice(0, v);
  const agg = v < 0 ? '' : resto.slice(v + 2);
  if ((D.proprie[ins] || []).includes(marca)) marca = '';
  return { marca, nome: pro.slice(0, i) + (agg ? ', ' + agg : '') };
}

function riga(o, u, lun) {
  const [ins, pro, fmt, prezzo, pu, dal, al, tessera] = o;
  const t = titolo(ins, pro);
  const d = document.createElement('div');
  d.className = 'riga';
  const chi = document.createElement('div');
  chi.className = 'chi';
  if (t.marca) { const m = document.createElement('span'); m.className = 'marca'; m.textContent = t.marca; chi.appendChild(m); }
  const n = document.createElement('span'); n.className = 'nome'; n.textContent = t.nome; chi.appendChild(n);
  const w = document.createElement('span'); w.className = 'dove';
  /* Le cose sfuse («al kg») hanno già il prezzo per unità: «9,90 € al kg». */
  let testo = ins + ' · ' + eur(prezzo) + ' €' + (/^al /.test(fmt) ? ' ' : ' · ') + fmt;
  /* Se l'offerta non copre tutta la settimana si dice quando valeva. */
  const dom = piu(lun, 6);
  if (giorno(dal) > lun || (al && giorno(al) < dom))
    testo += ' · ' + tratto(giorno(dal) > lun ? giorno(dal) : lun, al && giorno(al) < dom ? giorno(al) : dom);
  w.textContent = testo; chi.appendChild(w);
  if (tessera) { const p = document.createElement('span'); p.className = 'pill'; p.textContent = 'Con tessera o app'; chi.appendChild(p); }
  const p = document.createElement('div');
  p.className = 'prezzo';
  p.innerHTML = '<b></b><span></span>';
  p.querySelector('b').textContent = eur(pu);
  p.querySelector('span').textContent = UNITA[u] || u;
  d.append(chi, p);
  return d;
}

/* Una settimana: il suo più basso e, sotto, le altre. */
function blocco(s, c) {
    const oggi = giorno(D.oggi);
    const lun = giorno(s.w), dom = piu(lun, 6);
    const art = document.createElement('section');
    const ora = oggi >= lun && oggi <= dom;
    art.className = 'settimana' + (ora ? ' adesso' : '');
    art.innerHTML = '<div class="quando"><span></span><span class="ora"></span></div>';
    art.querySelector('.quando span').textContent = tratto(lun, dom);
    if (ora) art.querySelector('.ora').textContent = 'questa settimana';
    art.appendChild(riga(s.o[0], c.u, lun));
    if (s.o.length > 1) {
      const det = document.createElement('details');
      det.innerHTML = '<summary></summary><div class="altre"></div>';
      det.querySelector('summary').textContent = s.n > s.o.length
        ? 'Le altre più basse (' + (s.o.length - 1) + ' di ' + (s.n - 1) + ')'
        : 'Le altre (' + (s.o.length - 1) + ')';
      s.o.slice(1).forEach(o => det.querySelector('.altre').appendChild(riga(o, c.u, lun)));
      art.appendChild(det);
    }
    return art;
}

/* ---- il grafico ----
   Una linea sola (Manlio, 2026-09-26: «grafici settimana per settimana del
   prezzo attuale e di com'era le settimane prima»): il più basso per unità di
   ogni settimana, dalla più vecchia a sinistra a questa a destra. Una scala
   sola, e il valore scritto solo sul punto scelto (all'inizio l'ultimo). */
const SERIE = '#2a78d6';
const NS = 'http://www.w3.org/2000/svg';
const corto = d => d.getDate() + ' ' + MESI[d.getMonth()].slice(0, 3);
let scelta = -1;

function el(nome, attr, padre) {
  const e = document.createElementNS(NS, nome);
  for (const k in attr) e.setAttribute(k, attr[k]);
  if (padre) padre.appendChild(e);
  return e;
}

/* Tre o quattro righe di griglia a numeri tondi, con un po' d'aria sopra e
   sotto la linea. */
function tacche(lo, hi) {
  if (hi - lo < 0.01) { const m = hi || 1; lo = m * 0.85; hi = m * 1.15; }
  const aria = (hi - lo) * 0.15;
  lo = Math.max(0, lo - aria); hi += aria;
  const grezzo = (hi - lo) / 3, p = Math.pow(10, Math.floor(Math.log10(grezzo)));
  const passo = [1, 2, 2.5, 5, 10].map(k => k * p).find(v => v >= grezzo);
  const t = [];
  for (let v = Math.floor(lo / passo) * passo; v < hi + passo - 1e-9; v += passo) t.push(+v.toFixed(6));
  const dec = passo >= 1 ? 0 : (Math.abs(passo * 10 - Math.round(passo * 10)) < 1e-9 ? 1 : 2);
  return { t, dec };
}

function grafico(c, da) {
  const box = document.getElementById('grafico');
  box.textContent = '';
  const pts = c.s.slice().reverse();
  const ys = pts.map(s => s.o[0][4]);
  const W = Math.max(280, box.clientWidth || 340), H = 200;
  const m = { l: 44, r: 52, t: 24, b: 28 };
  const { t, dec } = tacche(Math.min(...ys), Math.max(...ys));
  const y0 = t[0], y1 = t[t.length - 1];
  const X = i => pts.length === 1 ? (m.l + W - m.r) / 2 : m.l + i * (W - m.l - m.r) / (pts.length - 1);
  const Y = v => m.t + (y1 - v) / (y1 - y0) * (H - m.t - m.b);
  const svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, role: 'img', tabindex: 0,
    'aria-label': 'Il più basso di ogni settimana, ' + (UNITA[c.u] || c.u) + ': '
      + pts.map((s, i) => corto(giorno(s.w)) + ' ' + eur(ys[i])).join('; ') }, box);
  t.forEach(v => {
    el('line', { x1: m.l, x2: W - m.r + 8, y1: Y(v), y2: Y(v), stroke: '#E5E3DD', 'stroke-width': 1 }, svg);
    el('text', { x: m.l - 8, y: Y(v) + 4, 'text-anchor': 'end', class: 'asse' }, svg)
      .textContent = v.toFixed(dec).replace('.', ',');
  });
  /* Le date sotto: tutte se ci stanno, se no una ogni tanto, e l'ultima sempre. */
  const ogni = Math.max(1, Math.ceil(pts.length / Math.max(1, Math.floor((W - m.l - m.r) / 56 + 1))));
  pts.forEach((s, i) => {
    if ((pts.length - 1 - i) % ogni) return;
    el('text', { x: X(i), y: H - 6, 'text-anchor': 'middle', class: 'asse' }, svg)
      .textContent = corto(giorno(s.w));
  });
  const croce = el('line', { y1: m.t - 8, y2: H - m.b, stroke: '#CFCCC4', 'stroke-width': 1 }, svg);
  if (pts.length > 1)
    el('polyline', { points: pts.map((s, i) => X(i) + ',' + Y(ys[i])).join(' '), fill: 'none',
      stroke: SERIE, 'stroke-width': 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }, svg);
  const punti = pts.map((s, i) => el('circle', { cx: X(i), cy: Y(ys[i]), r: 4.5, fill: SERIE,
    stroke: '#FFFFFF', 'stroke-width': 2 }, svg));
  const val = el('text', { class: 'valore' }, svg);
  const segna = i => {
    scelta = i;
    croce.setAttribute('x1', X(i)); croce.setAttribute('x2', X(i));
    punti.forEach((p, j) => p.setAttribute('r', j === i ? 7 : 4.5));
    const destra = X(i) + 12 + 44 <= W;
    val.setAttribute('x', destra ? X(i) + 12 : X(i) - 12);
    val.setAttribute('text-anchor', destra ? 'start' : 'end');
    val.setAttribute('y', Math.max(16, Y(ys[i]) - 10));
    val.textContent = eur(ys[i]);
    const box2 = document.getElementById('scelta');
    box2.textContent = '';
    box2.appendChild(blocco(pts[i], c));
  };
  /* Si tocca dove si vuole: vale la settimana più vicina al dito. */
  const vicino = ev => {
    const r = svg.getBoundingClientRect();
    const x = (ev.clientX - r.left) * W / (r.width || W);
    let meglio = 0;
    pts.forEach((s, i) => { if (Math.abs(X(i) - x) < Math.abs(X(meglio) - x)) meglio = i; });
    return meglio;
  };
  svg.addEventListener('pointerdown', ev => segna(vicino(ev)));
  svg.addEventListener('pointermove', ev => {
    if (ev.pointerType === 'mouse' || ev.buttons) { const i = vicino(ev); if (i !== scelta) segna(i); }
  });
  svg.addEventListener('keydown', ev => {
    if (ev.key === 'ArrowLeft' && scelta > 0) { segna(scelta - 1); ev.preventDefault(); }
    if (ev.key === 'ArrowRight' && scelta < pts.length - 1) { segna(scelta + 1); ev.preventDefault(); }
  });
  segna(da >= 0 && da < pts.length ? da : pts.length - 1);
}

function mostra(cat, da) {
  const c = D.dati[cat];
  const box = document.getElementById('elenco');
  box.textContent = '';
  if (!c) return;
  document.getElementById('titolo-g').textContent = 'Il più basso di ogni settimana, ' + (UNITA[c.u] || c.u);
  document.getElementById('aiuto-g').textContent = c.s.length > 1
    ? 'Tocca il grafico per vedere l\u2019offerta di quella settimana.'
    : 'Per ora c\u2019è una settimana sola: ogni lunedì se ne aggiunge una.';
  grafico(c, da);
  c.s.forEach(s => box.appendChild(blocco(s, c)));
}

const sel = document.getElementById('cat');
D.reparti.forEach(([rep, nomi]) => {
  const g = document.createElement('optgroup');
  g.label = rep;
  nomi.forEach(n => { const o = document.createElement('option'); o.value = o.textContent = n; g.appendChild(o); });
  sel.appendChild(g);
});
let prima = '';
try { prima = localStorage.getItem('spesa.prezzi.cat') || ''; } catch (e) {}
if (D.dati[prima]) sel.value = prima;
sel.onchange = () => { try { localStorage.setItem('spesa.prezzi.cat', sel.value); } catch (e) {} mostra(sel.value, -1); };
/* Se il telefono si gira il grafico si rifà, sulla stessa settimana. */
let largo = 0;
addEventListener('resize', () => {
  const w = document.getElementById('grafico').clientWidth;
  if (w && w !== largo) { largo = w; grafico(D.dati[sel.value], scelta); }
});
const ini = giorno(D.inizio);
document.getElementById('sotto').textContent = D.offerte.toLocaleString('it-IT') + ' offerte dal '
  + ini.getDate() + ' ' + MESI[ini.getMonth()] + ' ' + ini.getFullYear() + '. Aggiornato il '
  + giorno(D.oggi).getDate() + ' ' + MESI[giorno(D.oggi).getMonth()] + '.';
mostra(sel.value, -1);
</script>
</body>
</html>
'''


if __name__ == '__main__':
    aggiorna(tutto='--tutto' in sys.argv)
