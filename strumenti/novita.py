# -*- coding: utf-8 -*-
"""La pagina delle novità: cos'è cambiato oggi, e volendo negli ultimi 7 giorni.

Chiesta da Manlio il 2026-09-05. Legge i file che `storia.py` lascia in
`storia/` — uno per giorno, scritto solo quando è successo qualcosa — e ne fa
una pagina sola con due viste: **Oggi** e **Ultimi 7 giorni**.

    python3 -m novita        scrive out/novita.html

Si apre da sola in una finestra nuova, col tasto «Novità» in cima alla pagina
dei prezzi. È statica come tutto il resto: nessun server, funziona anche senza
rete se il telefono l'ha già vista.

L'ordine dei blocchi non è casuale. In cima **il più conveniente che cambia
padrone**: è l'unica novità che cambia dove si va a fare la spesa. Sapere che è
comparso un tonno non serve a niente; sapere che il tonno più conveniente
adesso è un altro sì.
"""
import datetime, glob, html, json, os, re

# Una pagina di volantino che è un'immagine si mostra così com'è; tutto il
# resto (il visore del Conad) si apre in un riquadro. Come nella pagina dei
# prezzi.
E_IMMAGINE = re.compile(r'\.(?:jpe?g|png|webp|gif)(?:\?|$)|/thumbor/', re.I)
E_PDF = re.compile(r'\.pdf(?:[?#]|$)|#page=\d', re.I)

QUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORIA = os.path.join(QUI, 'storia')
MESI = ('gennaio febbraio marzo aprile maggio giugno luglio agosto '
        'settembre ottobre novembre dicembre').split()
GIORNI = 'lunedì martedì mercoledì giovedì venerdì sabato domenica'.split()

def in_italiano(iso, oggi):
    d = datetime.date.fromisoformat(iso)
    quanti = (oggi - d).days
    if quanti == 0: return 'Oggi'
    if quanti == 1: return 'Ieri'
    return f'{GIORNI[d.weekday()].capitalize()} {d.day} {MESI[d.month - 1]}'

def eur(n):
    return (f'{n:.3f}' if n < 1 else f'{n:.2f}').replace('.', ',')

def e(s):
    return html.escape(str(s))

def riga(o, unita, prima=None):
    freccia = ''
    if prima is not None:
        giu = o['unitario'] < prima
        freccia = (f'<span class="delta {"giu" if giu else "su"}">'
                   f'{"−" if giu else "+"}{eur(abs(o["unitario"] - prima))}</span>')
    return (f'<li><span class="val">{eur(o["unitario"])} €<em>{e(unita)}</em></span>'
            f'<span class="che"><b>{e(o["pro"])}</b>'
            f'<span class="ins">{e(o["ins"])} · {e(o["fmt"])}</span></span>{freccia}</li>')

def blocco(titolo, righe, classe=''):
    if not righe:
        return ''
    return (f'<h3 class="{classe}">{e(titolo)} <span class="n">{len(righe)}</span></h3>'
            f'<ul class="cose">{"".join(righe)}</ul>')

def giorno_html(d, unita, oggi):
    parti = []

    capovolti = []
    for c in d.get('meno_caro_cambiato', []):
        capovolti.append(
            f'<li><span class="val">{eur(c["unitario"])} €<em>{e(c["unita"])}</em></span>'
            f'<span class="che"><b>{e(c["cat"])}</b>'
            f'<span class="ins">adesso è {e(c["pro"])} — {e(c["ins"])}<br>'
            f'prima {e(c["pro_prima"])} ({e(c["ins_prima"])}), {eur(c["unitario_prima"])} €</span></span></li>')
    if capovolti:
        parti.append(f'<h3 class="cambio">Il più conveniente è cambiato '
                     f'<span class="n">{len(capovolti)}</span></h3>'
                     f'<ul class="cose grosse">{"".join(capovolti)}</ul>')

    # I volantini nuovi e finiti NON si scrivono qui dentro: dal 2026-09-19
    # stanno in cima alla pagina, nel riquadro «Volantini aggiornati», che e la
    # prima cosa che Manlio voleva vedere aprendo le Novita. Scriverli anche
    # qui vorrebbe dire dirli due volte nella stessa schermata.

    scesi = [r for r in d.get('prezzi_cambiati', []) if r['unitario'] < r['prima']]
    saliti = [r for r in d.get('prezzi_cambiati', []) if r['unitario'] > r['prima']]
    parti.append(blocco('Prezzi scesi', [riga(o, unita.get(o['cat'], 'al kg'), o['prima']) for o in scesi], 'giu'))
    parti.append(blocco('Prezzi saliti', [riga(o, unita.get(o['cat'], 'al kg'), o['prima']) for o in saliti], 'su'))
    parti.append(blocco('Offerte nuove', [riga(o, unita.get(o['cat'], 'al kg')) for o in d.get('offerte_nuove', [])]))
    parti.append(blocco('Offerte finite', [riga(o, unita.get(o['cat'], 'al kg')) for o in d.get('offerte_sparite', [])], 'spente'))

    tras = d.get('cambiati_reparto', [])
    if tras:
        voci = ''.join(f'<li>{e(t["pro"])}: da {e(t["cat_prima"])} a {e(t["cat"])}</li>' for t in tras)
        parti.append(f'<h3 class="minore">Spostati di reparto <span class="n">{len(tras)}</span></h3>'
                     f'<ul class="minuta">{voci}</ul>')
    return ''.join(p for p in parti if p)


PAGINA = '''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Novità della spesa</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Asap:wght@400;500;600;700&family=Oswald:wght@500;600;700&display=swap">
<style>
/* Stessa lingua della pagina dei prezzi: tema chiaro fisso, niente blocco
   scuro. Il telefono di Manlio è in modalità notte e una pagina scura gli si
   apre nera. */
:root{
  --carta:#FFFFFF; --pannello:#F6F5F2; --inchiostro:#1B1B1A; --tenue:#6E6C66;
  --linea:#E5E3DD; --linea-forte:#CFCCC4; --rosso:#D40D2B; --su-rosso:#FFFFFF;
  --verde:#1E7A4B; --verde-tenue:#E6F3EC; --ambra:#8A5A08; --ambra-tenue:#FCF2DE;
  --f-testo:'Asap',ui-sans-serif,system-ui,'Segoe UI',sans-serif;
  --f-prezzo:'Oswald','Arial Narrow',ui-sans-serif,sans-serif;
  color-scheme:light;
}
*{box-sizing:border-box}
html{background:var(--carta)}
body{background:var(--carta);color:var(--inchiostro);font-family:var(--f-testo);
  font-size:16px;line-height:1.45;margin:0;-webkit-text-size-adjust:100%}
button{font-family:var(--f-testo);color:inherit}
:focus-visible{outline:3px solid var(--rosso);outline-offset:2px}
.guscio{max-width:800px;margin:0 auto;padding:0 15px 60px}
header{padding:20px 0 2px}
h1{font-family:var(--f-prezzo);font-weight:700;font-size:26px;letter-spacing:.01em;
  line-height:1.05;margin:0;text-transform:uppercase}
h1 span{display:block;color:var(--rosso);font-size:12px;letter-spacing:.16em;margin-bottom:6px}
h1 a.casa{text-decoration:none;color:inherit}
.torna{display:inline-block;margin-top:14px;color:var(--rosso);font-weight:600;font-size:15px;
  text-decoration:underline;text-underline-offset:3px;padding:6px 0;min-height:34px}
.scelta{display:flex;gap:8px;margin:18px 0 0;border-bottom:2px solid var(--inchiostro);
  padding-bottom:12px}
.scelta button{flex:1;background:var(--carta);border:1.5px solid var(--linea-forte);
  border-radius:99px;padding:11px 14px;font-size:15px;font-weight:600;cursor:pointer;
  min-height:46px}
.scelta button[aria-pressed="true"]{background:var(--rosso);border-color:var(--rosso);
  color:var(--su-rosso)}
/* ---- il riquadro dei volantini aggiornati, in cima ---- */
/* Chiesto da Manlio il 2026-09-19: aprendo le Novità la prima cosa da sapere è
   quali volantini sono stati aggiornati, non quale tonno è calato di dieci
   centesimi. */
.aggiornati{margin-top:20px;background:var(--pannello);border-radius:12px;padding:14px 14px 6px}
.aggiornati h2{font-family:var(--f-prezzo);text-transform:uppercase;letter-spacing:.03em;
  font-size:15px;margin:0 0 10px}
.agg{display:flex;gap:10px;align-items:flex-start;padding:10px 0;
  border-top:1px solid var(--linea)}
.agg:first-of-type{border-top:0;padding-top:2px}
.agg .bollo{flex:none;font-size:10.5px;letter-spacing:.05em;text-transform:uppercase;
  font-weight:700;border-radius:5px;padding:3px 7px;margin-top:2px;min-width:5.4em;
  text-align:center}
.agg.nuovo .bollo{background:var(--verde-tenue);color:var(--verde)}
.agg.letto .bollo{background:var(--ambra-tenue);color:var(--ambra)}
.agg.finito .bollo{background:var(--carta);color:var(--tenue);border:1px solid var(--linea-forte)}
.agg .che{flex:1;min-width:0}
.agg .che b{display:block;font-size:15px;line-height:1.25}
.agg .che .sotto{display:block;color:var(--tenue);font-size:12.5px;margin-top:2px}
.agg.finito .che b{color:var(--tenue)}
.niente-agg{color:var(--tenue);font-size:14px;margin:0 0 10px}

/* ---- la tabella di tutti i volantini ---- */
.tuttivol{margin-top:26px}
.tuttivol > h2{font-family:var(--f-prezzo);text-transform:uppercase;letter-spacing:.02em;
  font-size:18px;font-weight:600;margin:0 0 2px}
.tuttivol > .dicoche{color:var(--tenue);font-size:13px;margin:0 0 6px}
.gruppo{margin-top:16px}
.gruppo > h3{margin:0 0 4px}
table.tv{width:100%;border-collapse:collapse;font-size:14px}
table.tv td{padding:9px 0;border-top:1px solid var(--linea);vertical-align:top}
table.tv tr:first-child td{border-top:1.5px solid var(--inchiostro)}
table.tv .chi{width:42%}
table.tv .chi b{font-size:15px}
table.tv .chi .nome{display:block;color:var(--tenue);font-size:12.5px;line-height:1.3}
table.tv .date{width:26%;text-align:right;font-family:var(--f-prezzo);font-size:15px;
  font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;padding-right:10px}
table.tv .quanto{width:32%;text-align:right;font-size:12.5px;color:var(--tenue);
  line-height:1.3}
table.tv .quanto b{display:block;font-size:13px;font-weight:700}
table.tv tr.corre .quanto b{color:var(--verde)}
table.tv tr.stretto .quanto b{color:var(--rosso)}
table.tv tr.dopo .quanto b{color:var(--ambra)}
table.tv tr.spento td,table.tv tr.spento .chi b{color:var(--tenue)}
.nonletto{display:inline-block;margin-top:3px;font-size:11px;letter-spacing:.04em;
  text-transform:uppercase;font-weight:700;color:var(--ambra);
  background:var(--ambra-tenue);border-radius:5px;padding:2px 6px}
/* OGNI VOLANTINO SI SFOGLIA TOCCANDOLO (Manlio, 2026-09-24: «rendi
   interattivo questo elenco, facendo aprire i volantini a un clic»). Il nome
   del negozio diventa un tasto (bordo rosso: qui il rosso vuol dire «premi»),
   ma si può toccare tutta la riga. Quelli finiti no: i loro prezzi non
   valgono più. */
table.tv tr.apribile{cursor:pointer}
table.tv .apri-vol{display:inline-flex;align-items:center;gap:6px;max-width:100%;
  background:var(--carta);border:1.5px solid var(--rosso);color:var(--rosso);
  border-radius:10px;padding:4px 10px 4px 8px;min-height:34px;margin:-3px 0 3px;
  font-size:15px;line-height:1.15;text-align:left;cursor:pointer}
table.tv .apri-vol b{color:inherit}
table.tv .apri-vol svg{flex:none;width:17px;height:17px;fill:none;stroke:currentColor;
  stroke-width:1.5;stroke-linejoin:round;stroke-linecap:round}
table.tv tr.apribile:active .apri-vol,table.tv .apri-vol:active{background:var(--rosso);
  color:var(--su-rosso)}

/* ---- il volantino sfogliato, sopra la pagina ---- */
/* Come la pagina del volantino nella pagina dei prezzi: fondo scuro, la
   pagina in mezzo, il tastone rosso «Chiudi» in basso; in più le due frecce
   ai lati per andare avanti e indietro (o si scorre col dito). L'immagine
   NON è nostra: la pagina la chiede al sito di chi pubblica il volantino. */
.sfoglia[hidden]{display:none}
.sfoglia{position:fixed;inset:0;z-index:70;background:rgba(20,19,18,.94);
  display:flex;flex-direction:column}
.sfoglia .testa-vol{flex:none;display:flex;align-items:center;justify-content:space-between;
  gap:10px;padding:10px 14px;color:#FFFFFF;font-size:14px}
.sfoglia .testa-vol b{font-weight:700}
.sfoglia .testa-vol a{color:#FFFFFF;font-weight:600;text-decoration:underline;
  text-underline-offset:3px;white-space:nowrap}
.sfoglia .foglio{flex:1;min-height:0;overflow:auto;-webkit-overflow-scrolling:touch;
  padding:0 8px 96px}
.sfoglia .foglio img{display:block;width:100%;height:auto;margin:0 auto;max-width:900px;
  background:#FFFFFF;border-radius:6px;min-height:40vh}
.sfoglia .foglio iframe{display:block;width:100%;height:100%;border:0;background:#FFFFFF;
  border-radius:6px}
.sfoglia .avviso-vol{color:#FFFFFF;text-align:center;margin:40px 16px;font-size:15px}
.sfoglia .avviso-vol a{color:#FFFFFF;font-weight:700}
.sfoglia .avviso-vol a.apri-pdf{display:inline-block;margin-top:14px;padding:13px 20px;
  border-radius:14px;background:#FFFFFF;color:#1B1B1A;text-decoration:none;font-size:17px}
.sfoglia .comandi{position:absolute;left:14px;right:14px;display:flex;gap:10px;
  bottom:calc(14px + env(safe-area-inset-bottom,0px))}
.sfoglia .comandi button{min-height:58px;border:0;border-radius:14px;font-family:inherit;
  font-weight:700;cursor:pointer;box-shadow:0 6px 24px rgba(0,0,0,.45)}
.sfoglia .gira{flex:none;width:62px;background:#FFFFFF;color:#1B1B1A;display:flex;
  align-items:center;justify-content:center;padding:0}
.sfoglia .gira svg{width:26px;height:26px;fill:none;stroke:currentColor;stroke-width:2.6;
  stroke-linecap:round;stroke-linejoin:round}
.sfoglia .gira:disabled{opacity:.3;cursor:default}
.sfoglia .chiudi-vol{flex:1;background:var(--rosso);color:var(--su-rosso);font-size:19px;
  letter-spacing:.02em}

.giorno{margin-top:26px}
.giorno > h2{font-family:var(--f-prezzo);text-transform:uppercase;letter-spacing:.02em;
  font-size:21px;font-weight:600;margin:0 0 2px}
.giorno > .quando{color:var(--tenue);font-size:13px;margin:0}
h3{font-family:var(--f-prezzo);text-transform:uppercase;letter-spacing:.06em;font-size:12.5px;
  font-weight:600;color:var(--tenue);margin:20px 0 0;display:flex;align-items:center;gap:8px}
h3 .n{font-family:var(--f-testo);font-size:11px;font-weight:700;letter-spacing:0;
  background:var(--pannello);border-radius:99px;padding:1px 8px;color:var(--inchiostro)}
h3.cambio{color:var(--rosso)}
h3.cambio .n{background:var(--rosso);color:var(--su-rosso)}
h3.giu{color:var(--verde)} h3.giu .n{background:var(--verde-tenue);color:var(--verde)}
h3.su{color:var(--ambra)} h3.su .n{background:var(--ambra-tenue);color:var(--ambra)}
ul.cose{list-style:none;padding:0;margin:6px 0 0}
ul.cose li{display:flex;align-items:baseline;gap:12px;padding:11px 0;
  border-top:1px solid var(--linea)}
ul.cose li:first-child{border-top:1.5px solid var(--inchiostro)}
ul.cose .val{flex:none;min-width:5.6em;text-align:right;font-family:var(--f-prezzo);
  font-size:20px;font-weight:700;color:var(--rosso);font-variant-numeric:tabular-nums;
  line-height:1.1}
ul.cose .val em{display:block;font-family:var(--f-testo);font-style:normal;font-size:10px;
  letter-spacing:.08em;text-transform:uppercase;color:var(--tenue);font-weight:500;margin-top:3px}
ul.cose .che{flex:1;min-width:0}
ul.cose .che b{display:block;font-size:15.5px;font-weight:600;line-height:1.25}
ul.cose .che .ins{display:block;color:var(--tenue);font-size:13px;margin-top:2px}
ul.cose.grosse .val{font-size:24px}
ul.cose.spente .val{color:var(--tenue)}
ul.cose.spente .che b{text-decoration:line-through;text-decoration-color:var(--linea-forte)}
.delta{flex:none;font-family:var(--f-prezzo);font-size:14px;font-weight:600;
  border-radius:6px;padding:2px 7px;font-variant-numeric:tabular-nums}
.delta.giu{background:var(--verde-tenue);color:var(--verde)}
.delta.su{background:var(--ambra-tenue);color:var(--ambra)}
.vol{margin:16px 0 0;border-radius:10px;padding:11px 13px;font-size:14.5px}
.vol.arriva{background:var(--verde-tenue);color:#14512F}
.vol.finito{background:var(--pannello);color:var(--tenue)}
h3.minore{color:var(--tenue)}
ul.minuta{list-style:none;padding:0;margin:6px 0 0;color:var(--tenue);font-size:13.5px}
ul.minuta li{padding:4px 0}
.niente{background:var(--pannello);border-radius:12px;padding:16px;color:var(--tenue);
  font-size:14.5px;margin:22px 0 0}
.niente b{color:var(--inchiostro)}
footer{margin-top:34px;padding-top:14px;border-top:1px solid var(--linea);
  color:var(--tenue);font-size:13px}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<div class="guscio">
<header>
  <!-- Il titolo riporta alla pagina dei prezzi (Manlio, 2026-09-23: «in tutto
       il sito, cliccando sopra Spesa si tornerà alla pagina iniziale»). -->
  <h1><a class="casa" href="https://manliograndi-del.github.io/spesa/"><span>Spesa · Offerte grande distribuzione</span></a>Novità</h1>
  <a class="torna" href="./index.html">← Torna ai prezzi</a>
</header>

<div class="scelta" role="group" aria-label="Quanto indietro guardare">
  <button type="button" id="b-1" aria-pressed="true">Oggi</button>
  <button type="button" id="b-3" aria-pressed="false">3 giorni</button>
  <button type="button" id="b-7" aria-pressed="false">7 giorni</button>
</div>

<!-- PRIMA DI TUTTO I VOLANTINI. Poi la tabella di tutti quanti, poi le
     novità dei prezzi giorno per giorno. -->
<section class="aggiornati">
  <h2 id="titolo-agg">Volantini aggiornati</h2>
  <div id="agg-dentro"></div>
</section>

<section class="tuttivol">
  <h2>Tutti i volantini</h2>
  <p class="dicoche">Quelli che sto leggendo adesso, quelli che arrivano e
  quelli appena finiti. Tocca un volantino per sfogliarlo.</p>
  <div id="tabvol"></div>
</section>

<h2 class="tuttivol" style="margin-top:30px">Novità dei prezzi</h2>
<div id="dentro"></div>

<footer id="pie"></footer>
</div>

<!-- IL VOLANTINO SFOGLIATO, SOPRA LA PAGINA: si apre toccando un volantino
     della tabella. -->
<div class="sfoglia" id="sfoglia" hidden role="dialog" aria-modal="true" aria-labelledby="titolo-sfoglia">
  <div class="testa-vol"><span id="titolo-sfoglia"></span>
    <a id="fuori-sfoglia" target="_blank" rel="noopener noreferrer">Apri sul sito</a></div>
  <div class="foglio" id="foglio-sfoglia"></div>
  <div class="comandi">
    <button type="button" class="gira" id="indietro-sfoglia" aria-label="Pagina prima"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M15 5l-7 7 7 7"></path></svg></button>
    <button type="button" class="chiudi-vol" id="chiudi-sfoglia">Chiudi</button>
    <button type="button" class="gira" id="avanti-sfoglia" aria-label="Pagina dopo"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M9 5l7 7-7 7"></path></svg></button>
  </div>
</div>

<script>
const GIORNI = __GIORNI__;
const TABELLA = __TABELLA__;
const FINITI = __FINITI__;

/* Le date le giudica IL BROWSER DI CHI GUARDA, con la sua data, come nella
   pagina dei prezzi: una pagina lasciata aperta due giorni non deve dire
   «ancora 3 giorni» di un volantino scaduto stanotte. */
const OGGI_ISO = new Date().toLocaleDateString('sv');
const MESI3 = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu',
               'lug', 'ago', 'set', 'ott', 'nov', 'dic'];
function giornoCorto(iso) {
  if (!iso) return '';
  const p = iso.split('-');
  return Number(p[2]) + ' ' + MESI3[Number(p[1]) - 1];
}
function distanza(da, a) {
  if (!da || !a) return null;
  return Math.round((new Date(a + 'T00:00:00') - new Date(da + 'T00:00:00')) / 86400000);
}
function testo(n, uno, tanti) {
  return n + ' ' + (n === 1 ? uno : tanti);
}

/* SI APRE DOVE C'E' QUALCOSA, non per forza su «Oggi».
   E' la stessa lezione dello Storico della Palestra: quel calendario si apriva
   sul mese corrente e il 2026-09-01, con il mese nuovo ancora vuoto, Manlio ha
   creduto di aver perso tutti i dati. Qui capiterebbe piu spesso ancora,
   perche i volantini non cambiano tutti i giorni: aprire su un «Oggi» vuoto
   fa sembrare che la pagina non funzioni. Se oggi non c'e niente si parte da
   tre giorni, e se non basta da sette; i tasti restano tutti e tre. */
function primaFinestra() {
  if (GIORNI.some(g => g.quanti < 1 && (g.roba || (g.agg && g.agg.length)))) return 1;
  if (GIORNI.some(g => g.quanti < 3 && (g.roba || (g.agg && g.agg.length)))) return 3;
  return 7;
}
let finestra = primaFinestra();

const QUANTI = { 1: 'oggi', 3: 'negli ultimi tre giorni', 7: 'negli ultimi sette giorni' };

function scelti() {
  return GIORNI.filter(g => g.quanti < finestra);
}

/* ---------- 1. i volantini aggiornati, in cima ---------- */
function disegnaAggiornati() {
  const box = document.getElementById('agg-dentro');
  box.textContent = '';
  const righe = [];
  scelti().forEach(g => (g.agg || []).forEach(a => righe.push({ a: a, quando: g.titolo })));
  if (!righe.length) {
    const p = document.createElement('p');
    p.className = 'niente-agg';
    p.textContent = 'Nessun volantino aggiornato ' + QUANTI[finestra]
      + '. Vuol dire che sono gli stessi di prima, non che manca qualcosa.';
    box.appendChild(p);
    return;
  }
  righe.forEach(r => {
    const a = r.a;
    const d = document.createElement('div');
    d.className = 'agg ' + a.stato;
    d.innerHTML = '<span class="bollo"></span><span class="che"><b></b><span class="sotto"></span></span>';
    d.querySelector('.bollo').textContent =
      a.stato === 'nuovo' ? 'nuovo' : a.stato === 'finito' ? 'finito' : 'letto';
    d.querySelector('.che b').textContent = a.ins + (a.nome ? ' — ' + a.nome : '');
    const pezzi = [];
    if (a.periodo) pezzi.push(a.periodo);
    if (a.nuove) pezzi.push(testo(a.nuove, 'prezzo nuovo', 'prezzi nuovi'));
    pezzi.push(r.quando.toLowerCase());
    d.querySelector('.sotto').textContent = pezzi.join(' · ');
    box.appendChild(d);
  });
}

/* ---------- 2. la tabella di tutti i volantini ---------- */
/* Chiesta da Manlio il 2026-09-19: «una tabellina nella quale appaiono tutti i
   supermercati e l'intervallo di validità dei loro volantini presenti e di
   quelli che sai anche futuri». Divisa in tre gruppi perche e cosi che si
   guarda: cosa vale adesso, cosa sta per arrivare, cosa e appena finito. */
function statoDi(v) {
  if (v.inizio && v.inizio > OGGI_ISO) return 'dopo';
  if (v.fino && v.fino < OGGI_ISO) return 'spento';
  return 'corre';
}

function quantoManca(v, stato) {
  if (stato === 'dopo') {
    const n = distanza(OGGI_ISO, v.inizio);
    return { forte: n === 1 ? 'da domani' : 'fra ' + testo(n, 'giorno', 'giorni'), fiacco: '' };
  }
  if (stato === 'spento') {
    const n = distanza(v.fino, OGGI_ISO);
    return { forte: n === 1 ? 'finito ieri' : 'finito ' + testo(n, 'giorno fa', 'giorni fa'),
             fiacco: '' };
  }
  if (!v.fino) return { forte: 'in corso', fiacco: '' };
  const n = distanza(OGGI_ISO, v.fino);
  if (n === 0) return { forte: 'ultimo giorno', fiacco: 'finisce stasera' };
  if (n === 1) return { forte: 'finisce domani', fiacco: '' };
  return { forte: 'ancora ' + testo(n, 'giorno', 'giorni'), fiacco: '' };
}

function righeTabella(elenco) {
  return elenco.map(v => {
    const stato = statoDi(v);
    const q = quantoManca(v, stato);
    const stretto = stato === 'corre' && v.fino && distanza(OGGI_ISO, v.fino) <= 1;
    const tr = document.createElement('tr');
    tr.className = stato + (stretto ? ' stretto' : '');
    /* Le date vere restano attaccate alla riga: quello che si legge e
       accorciato («17 → 30 set») e la prova, per controllare che un volantino
       non finisca nel gruppo sbagliato, deve poter guardare le date intere. */
    if (v.inizio) tr.setAttribute('data-inizio', v.inizio);
    if (v.fino) tr.setAttribute('data-fino', v.fino);
    tr.setAttribute('data-letto', v.letto ? 'si' : 'no');
    /* Si sfoglia se ha le pagine e se vale ancora (o deve cominciare): uno
       finito ha prezzi che non valgono più, e aprirlo manderebbe in negozio
       con un volantino scaduto in mano. */
    const apribile = stato !== 'spento' && v.pagine && v.pagine.length > 0;
    tr.innerHTML = '<td class="chi">'
      + (apribile ? '<button type="button" class="apri-vol">' + FOGLIETTO + '<b></b></button>' : '<b></b>')
      + '<span class="nome"></span></td>'
      + '<td class="date"></td><td class="quanto"><b></b><span></span></td>';
    tr.querySelector('.chi b').textContent = v.ins;
    if (apribile) {
      tr.classList.add('apribile');
      tr.querySelector('.apri-vol').setAttribute('aria-label',
        'Sfoglia il volantino ' + v.ins + (v.nome ? ', ' + v.nome : ''));
      tr.onclick = () => apriVolantino(v);
    }
    const nome = tr.querySelector('.chi .nome');
    nome.textContent = v.nome || '';
    if (!v.letto) {
      const av = document.createElement('span');
      av.className = 'nonletto';
      av.textContent = 'prezzi non ancora letti';
      if (v.nome) nome.appendChild(document.createElement('br'));
      nome.appendChild(av);
    }
    /* Senza data d'inizio vuol dire che era gia cominciato quando l'ho preso:
       si scrive solo fin quando vale, che e quello che serve sapere. */
    /* «17 → 30 set» invece di «17 set → 30 set»: se il mese e lo stesso
       scriverlo due volte ruba la riga alla colonna di destra, che va a capo
       in mezzo a «ancora 4 giorni». */
    const stessoMese = v.inizio && v.fino && v.inizio.slice(0, 7) === v.fino.slice(0, 7);
    tr.querySelector('.date').textContent = !v.inizio
      ? 'fino al ' + giornoCorto(v.fino)
      : stessoMese
        ? Number(v.inizio.split('-')[2]) + ' → ' + giornoCorto(v.fino)
        : giornoCorto(v.inizio) + ' → ' + giornoCorto(v.fino);
    tr.querySelector('.quanto b').textContent = q.forte;
    tr.querySelector('.quanto span').textContent = q.fiacco;
    return tr;
  });
}

function gruppo(titolo, elenco, classe) {
  if (!elenco.length) return null;
  const sez = document.createElement('div');
  sez.className = 'gruppo';
  const h = document.createElement('h3');
  h.className = classe || '';
  h.innerHTML = '<span class="testa"></span><span class="n"></span>';
  h.querySelector('.testa').textContent = titolo;
  h.querySelector('.n').textContent = elenco.length;
  sez.appendChild(h);
  const t = document.createElement('table');
  t.className = 'tv';
  righeTabella(elenco).forEach(r => t.appendChild(r));
  sez.appendChild(t);
  return sez;
}

function disegnaTabella() {
  const box = document.getElementById('tabvol');
  box.textContent = '';
  const corso = TABELLA.filter(v => statoDi(v) === 'corre')
    .sort((a, b) => (a.fino || '') < (b.fino || '') ? -1 : 1);
  const dopo = TABELLA.filter(v => statoDi(v) === 'dopo')
    .sort((a, b) => (a.inizio || '') < (b.inizio || '') ? -1 : 1);
  /* Gli appena finiti la tabella se li ricorda dal diario: da dati.py
     spariscono, e senza questo uno non capisce piu dov'e andato un negozio. */
  const visti = {};
  const spenti = TABELLA.filter(v => statoDi(v) === 'spento').concat(FINITI)
    .filter(v => {
      const k = v.ins + '|' + v.periodo;
      if (visti[k]) return false;
      visti[k] = 1;
      return true;
    })
    .sort((a, b) => (a.fino || '') > (b.fino || '') ? -1 : 1);
  [gruppo('In corso adesso', corso), gruppo('In arrivo', dopo),
   gruppo('Appena finiti', spenti, 'minore')]
    .forEach(g => { if (g) box.appendChild(g); });
}

/* ---------- 2b. il volantino sfogliato, sopra la pagina ---------- */
/* Il foglietto con l'orecchia piegata, lo stesso della pagina dei prezzi. */
const FOGLIETTO = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
  + '<path d="M3.2 1.8h5.6l3.4 3.4v9H3.2z"></path>'
  + '<path d="M8.8 1.8v3.4h3.4"></path>'
  + '<path d="M5.6 8.2h4.8M5.6 10.8h3.2"></path></svg>';
/* Le pagine di nove insegne su dieci sono immagini sul sito di chi le
   pubblica e si mostrano così come sono; il Conad ha un visore suo, che si
   apre qui dentro (v.quadro). Se l'immagine non arriva resta scritto come
   aprirla fuori. Il tasto «indietro» del telefono chiude, come «Chiudi». */
let sfoglio = null;
function mostraPagina() {
  const v = sfoglio.v, i = sfoglio.i, url = v.pagine[i], tot = v.pagine.length;
  const foglio = document.getElementById('foglio-sfoglia');
  const tit = document.getElementById('titolo-sfoglia');
  tit.innerHTML = '<b></b> · pagina <span></span>';
  tit.querySelector('b').textContent = v.ins;
  tit.querySelector('span').textContent = (i + 1) + ' di ' + tot;
  document.getElementById('fuori-sfoglia').href = url;
  document.getElementById('indietro-sfoglia').disabled = i === 0;
  document.getElementById('avanti-sfoglia').disabled = i === tot - 1;
  foglio.textContent = '';
  const guasto = () => {
    foglio.innerHTML = '<p class="avviso-vol">La pagina qui non si vede. <a target="_blank" rel="noopener noreferrer">Aprila sul sito</a></p>';
    foglio.querySelector('a').href = url;
  };
  const dove = 'Pagina ' + (i + 1) + ' del volantino ' + v.ins;
  if (v.solopdf) {
    /* Solo PDF (il Bennet «Offerte Extra»): il telefono qui dentro non lo
       mostra; si apre fuori, alla pagina che si sta guardando. */
    foglio.innerHTML = '<p class="avviso-vol">Questo volantino c’è solo in PDF, che qui dentro il telefono non mostra.<br><a class="apri-pdf" target="_blank" rel="noopener noreferrer"></a></p>';
    const a = foglio.querySelector('a');
    a.href = url;
    a.textContent = 'Aprilo alla pagina ' + (i + 1);
  } else if (v.quadro) {
    const f = document.createElement('iframe');
    f.title = dove;
    f.referrerPolicy = 'no-referrer';
    f.src = url;
    foglio.appendChild(f);
  } else {
    const img = document.createElement('img');
    img.alt = dove;
    img.referrerPolicy = 'no-referrer';
    img.onerror = guasto;
    img.src = url;
    foglio.appendChild(img);
    /* La pagina dopo si chiede subito, così girando è già lì. */
    if (i + 1 < tot) {
      const dopo = new Image();
      dopo.referrerPolicy = 'no-referrer';
      dopo.src = v.pagine[i + 1];
    }
  }
  foglio.scrollTop = 0;
}
function apriVolantino(v) {
  sfoglio = { v: v, i: 0 };
  mostraPagina();
  document.getElementById('sfoglia').hidden = false;
  document.documentElement.style.overflow = 'hidden';
  if (!sfoglio.storia) {
    sfoglio.storia = true;
    try { history.pushState({ sfoglia: 1 }, '', location.href); } catch (e) {}
  }
  try { document.getElementById('chiudi-sfoglia').focus({ preventScroll: true }); } catch (e) {}
}
function giraPagina(passo) {
  if (!sfoglio) return;
  const i = sfoglio.i + passo;
  if (i < 0 || i >= sfoglio.v.pagine.length) return;
  sfoglio.i = i;
  mostraPagina();
}
function chiudiVolantino(daIndietro) {
  const box = document.getElementById('sfoglia');
  if (box.hidden || !sfoglio) return;
  box.hidden = true;
  document.getElementById('foglio-sfoglia').textContent = '';
  document.documentElement.style.overflow = '';
  const storia = sfoglio.storia;
  sfoglio = null;
  if (storia && !daIndietro) { try { history.back(); } catch (e) {} }
}
document.getElementById('chiudi-sfoglia').onclick = () => chiudiVolantino(false);
document.getElementById('indietro-sfoglia').onclick = () => giraPagina(-1);
document.getElementById('avanti-sfoglia').onclick = () => giraPagina(1);
addEventListener('popstate', () => { if (sfoglio) chiudiVolantino(true); });
addEventListener('keydown', ev => {
  if (!sfoglio) return;
  if (ev.key === 'Escape') chiudiVolantino(false);
  else if (ev.key === 'ArrowRight') giraPagina(1);
  else if (ev.key === 'ArrowLeft') giraPagina(-1);
});
/* Col dito: una strisciata di lato gira la pagina. Non quando la pagina è
   ingrandita (lì strisciare serve a spostarsi dentro l'immagine), né quando
   la strisciata è più in su o in giù che di lato (è uno scorrimento). */
(function () {
  const foglio = document.getElementById('foglio-sfoglia');
  let x0 = null, y0 = 0;
  foglio.addEventListener('touchstart', ev => {
    if (ev.touches.length !== 1) { x0 = null; return; }
    x0 = ev.touches[0].clientX; y0 = ev.touches[0].clientY;
  }, { passive: true });
  foglio.addEventListener('touchend', ev => {
    if (x0 === null || !ev.changedTouches.length) return;
    const dx = ev.changedTouches[0].clientX - x0, dy = ev.changedTouches[0].clientY - y0;
    x0 = null;
    if (window.visualViewport && window.visualViewport.scale > 1.05) return;
    if (Math.abs(dx) > 60 && Math.abs(dx) > 1.5 * Math.abs(dy)) giraPagina(dx < 0 ? 1 : -1);
  }, { passive: true });
})();

/* ---------- 3. le novità dei prezzi, giorno per giorno ---------- */
function disegna() {
  [1, 3, 7].forEach(n => document.getElementById('b-' + n)
    .setAttribute('aria-pressed', String(n === finestra)));
  disegnaAggiornati();
  disegnaTabella();
  const dentro = document.getElementById('dentro');
  const pieni = scelti().filter(g => g.roba);
  if (!pieni.length) {
    dentro.innerHTML = '<p class="niente"><b>Nessun prezzo cambiato '
      + QUANTI[finestra] + '.</b> ' + (finestra === 7
        ? 'Vuol dire che i volantini sono gli stessi e i prezzi non si sono mossi.'
        : 'Prova con «7 giorni».') + '</p>';
    return;
  }
  dentro.innerHTML = pieni.map(g =>
    '<section class="giorno"><h2>' + g.titolo + '</h2>' +
    '<p class="quando">' + g.data + '</p>' + g.roba + '</section>').join('');
}
[1, 3, 7].forEach(n => {
  document.getElementById('b-' + n).onclick = () => { finestra = n; disegna(); };
});
document.getElementById('pie').textContent = __PIE__;
disegna();
</script>
</body>
</html>
'''

def nome_corto(periodo):
    """«"Un mondo di bellezza", dal 17 al 30 settembre» -> «Un mondo di bellezza».

    Nella tabella le date stanno nella loro colonna: nel nome serve solo quello
    che distingue DUE volantini della stessa insegna validi insieme (il Lidl
    generale e il suo «Frutta e Verdura», il Bennet normale e «Un mondo di
    bellezza»). Se non c'e niente da distinguere torna vuoto, e la casella
    resta pulita."""
    for taglio in (', dal ', ", dall'", ', dall’'):
        if taglio in periodo:
            return periodo.split(taglio)[0].strip().strip('"\u201c\u201d«»')
    return ''


def quando_corto(periodo):
    """«"Un mondo di bellezza", dal 17 al 30 settembre» -> «dal 17 al 30 settembre».

    Nel riquadro dei volantini aggiornati il nome sta gia nel titolo della
    riga: ripeterlo sotto, fra virgolette, faceva leggere due volte la stessa
    cosa."""
    for taglio in (', dal ', ", dall'", ', dall\u2019'):
        if taglio in periodo:
            return taglio.strip(', ') + ' ' + periodo.split(taglio, 1)[1]
    return periodo


def pagine_di(v, quante):
    """Gli indirizzi delle pagine di un volantino, dalla prima all'ultima.
    Come `indirizzo()` di pagina.py: dove c'è l'elenco (Mercatò, Ekom, che
    firmano ogni immagine) vince lui; se no si riempie lo schema col numero.
    Senza né l'uno né l'altro il volantino non si sfoglia e la riga resta
    scritta e basta."""
    if v.pagine:
        return list(v.pagine)
    if not v.indirizzo or not quante:
        return []
    return [v.indirizzo.format(n=n) for n in range(1, quante + 1)]

def aggiornamenti(d, periodi):
    """Cosa e cambiato NEI VOLANTINI in un giorno: arrivati, riletti, finiti.

    Chiesto da Manlio il 2026-09-19: «nella pagina novita sarebbe bene che
    apparissero prima di tutto i volantini aggiornati, cosi uno sa l'ultimo
    giorno e l'ultima settimana cosa e stato aggiornato».

    «Aggiornato» non vuol dire solo «volantino nuovo»: il 19 settembre il
    Bennet «Un mondo di bellezza» era gia nell'elenco da un giorno e quel
    giorno ci sono entrati 102 prezzi suoi. Per chi guarda, quello e
    l'aggiornamento. Quindi si contano anche le offerte nuove, raggruppate per
    volantino."""
    fuori = []
    quante = {}
    for o in d.get('offerte_nuove', []):
        if o.get('chiave'):
            quante[o['chiave']] = quante.get(o['chiave'], 0) + 1

    visti = set()
    for v in d.get('volantini_arrivati', []):
        visti.add(v['chiave'])
        fuori.append(dict(stato='nuovo', ins=v['ins'], nome=nome_corto(v['periodo']),
                          periodo=quando_corto(v['periodo']), nuove=quante.get(v['chiave'], 0)))
    for chiave, n in sorted(quante.items(), key=lambda x: -x[1]):
        if chiave in visti:
            continue
        per = periodi.get(chiave, {})
        fuori.append(dict(stato='letto', ins=per.get('ins', '?'),
                          nome=nome_corto(per.get('periodo', '')),
                          periodo=quando_corto(per.get('periodo', '')), nuove=n))
    for v in d.get('volantini_finiti', []):
        fuori.append(dict(stato='finito', ins=v['ins'], nome=nome_corto(v['periodo']),
                          periodo=quando_corto(v['periodo']), nuove=0))
    return fuori


def costruisci():
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from catalogo import UNITA
    from dati import VOLANTINI, VOLANTINI_ATTESI
    unita = {k: v[0] for k, v in UNITA.items()}
    oggi = datetime.date.today()
    # Quante pagine ha ogni volantino: le sa l'indice delle parole, che ne ha
    # una voce per pagina (anche per quelle scartate, che si sfogliano lo stesso).
    npagine = {}
    for r in json.load(open(os.path.join(QUI, 'indice.json'), encoding='utf-8')):
        npagine[r['chiave']] = max(npagine.get(r['chiave'], 0), r['pagina'])
    periodi = {v.chiave: dict(ins=v.insegna, periodo=v.periodo) for v in VOLANTINI}

    giorni = []
    finiti = []
    for f in sorted(glob.glob(os.path.join(STORIA, '2*.json')), reverse=True):
        d = json.load(open(f, encoding='utf-8'))
        data = datetime.date.fromisoformat(d['giorno'])
        quanti = (oggi - data).days
        if quanti > 7:
            continue
        giorni.append(dict(titolo=in_italiano(d['giorno'], oggi),
                           data=f'{data.day} {MESI[data.month - 1]} {data.year}',
                           quanti=quanti,
                           agg=aggiornamenti(d, periodi),
                           roba=giorno_html(d, unita, oggi)))
        # I volantini finiti spariscono da dati.py: la tabella se li ricorda da
        # qui, se no uno non capisce piu perche un negozio non c'e piu.
        for v in d.get('volantini_finiti', []):
            finiti.append(dict(ins=v['ins'], nome=nome_corto(v['periodo']),
                               periodo=v['periodo'], inizio=v.get('inizio'),
                               fino=v.get('fino'), letto=True, dove=''))
    if not giorni or giorni[0]['titolo'] != 'Oggi':
        giorni.insert(0, dict(titolo='Oggi', quanti=0, agg=[],
                              data=f'{oggi.day} {MESI[oggi.month - 1]} {oggi.year}', roba=''))

    # LA TABELLA DI TUTTI I VOLANTINI, chiesta da Manlio il 2026-09-19. Dentro
    # ci vanno quelli letti (che hanno i prezzi) E quelli che so in arrivo ma
    # non ho ancora letto: sapere che il buco fra un volantino e l'altro e gia
    # coperto vale quanto sapere i prezzi.
    #
    # Dal 2026-09-24 ogni volantino letto si SFOGLIA toccandolo (Manlio: «nella
    # pagina novità c'è ancora l'elenco di tutti i volantini: potresti renderlo
    # interattivo, facendo aprire i volantini a un clic»). Per questo la riga
    # si porta dietro gli indirizzi delle sue pagine: sono quelli sul sito di
    # chi pubblica il volantino, gli stessi della pagina dei prezzi (vincolo
    # 2: le immagini non stanno sul nostro sito).
    tabella = [dict(ins=v.insegna, nome=nome_corto(v.periodo), periodo=v.periodo,
                    inizio=v.inizio, fino=v.fino, letto=True, dove='',
                    pagine=pagine_di(v, npagine.get(v.chiave, 0)),
                    quadro=bool(v.indirizzo) and not E_IMMAGINE.search(v.indirizzo or '')
                           and not E_PDF.search(v.indirizzo or ''),
                    solopdf=bool(E_PDF.search(v.indirizzo or '')))
               for v in VOLANTINI]
    tabella += [dict(ins=a.insegna, nome=nome_corto(a.periodo), periodo=a.periodo,
                     inizio=a.inizio, fino=a.fino, letto=False, dove=a.dove)
                for a in VOLANTINI_ATTESI]

    pie = ('Le novità si contano da un giorno all\'altro: quello che vedi qui è la '
           'differenza rispetto all\'ultima volta che ho letto i volantini.')
    html_out = (PAGINA.replace('__GIORNI__', json.dumps(giorni, ensure_ascii=False))
                      .replace('__TABELLA__', json.dumps(tabella, ensure_ascii=False))
                      .replace('__FINITI__', json.dumps(finiti, ensure_ascii=False))
                      .replace('__PIE__', json.dumps(pie, ensure_ascii=False)))
    os.makedirs('out', exist_ok=True)
    open('out/novita.html', 'w', encoding='utf-8').write(html_out)
    pieni = len([g for g in giorni if g['roba']])
    print(f'out/novita.html — {len(giorni)} giorni, di cui {pieni} con qualcosa dentro')

if __name__ == '__main__':
    costruisci()
