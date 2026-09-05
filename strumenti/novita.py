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
import datetime, glob, html, json, os

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

    for v in d.get('volantini_arrivati', []):
        parti.append(f'<p class="vol arriva"><b>Volantino nuovo</b> — {e(v["ins"])}, {e(v["periodo"])}</p>')
    for v in d.get('volantini_finiti', []):
        parti.append(f'<p class="vol finito"><b>Volantino finito</b> — {e(v["ins"])}, {e(v["periodo"])}</p>')

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
.torna{display:inline-block;margin-top:14px;color:var(--rosso);font-weight:600;font-size:15px;
  text-decoration:underline;text-underline-offset:3px;padding:6px 0;min-height:34px}
.scelta{display:flex;gap:8px;margin:18px 0 0;border-bottom:2px solid var(--inchiostro);
  padding-bottom:12px}
.scelta button{flex:1;background:var(--carta);border:1.5px solid var(--linea-forte);
  border-radius:99px;padding:11px 14px;font-size:15px;font-weight:600;cursor:pointer;
  min-height:46px}
.scelta button[aria-pressed="true"]{background:var(--rosso);border-color:var(--rosso);
  color:var(--su-rosso)}
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
  <h1><span>Spesa · Torino, corso Siracusa</span>Novità</h1>
  <a class="torna" href="./index.html">← Torna ai prezzi</a>
</header>

<div class="scelta" role="group" aria-label="Quanto indietro guardare">
  <button type="button" id="b-oggi" aria-pressed="true">Oggi</button>
  <button type="button" id="b-sette" aria-pressed="false">Ultimi 7 giorni</button>
</div>

<div id="dentro"></div>

<footer id="pie"></footer>
</div>

<script>
const GIORNI = __GIORNI__;
let sette = false;

function disegna() {
  const dentro = document.getElementById('dentro');
  document.getElementById('b-oggi').setAttribute('aria-pressed', String(!sette));
  document.getElementById('b-sette').setAttribute('aria-pressed', String(sette));
  const quali = sette ? GIORNI : GIORNI.slice(0, 1);
  const pieni = quali.filter(g => g.roba);
  if (!pieni.length) {
    dentro.innerHTML = '<p class="niente">' + (sette
      ? '<b>Negli ultimi sette giorni non è cambiato niente.</b> Vuol dire che i volantini sono gli stessi e i prezzi non si sono mossi.'
      : '<b>Oggi non è cambiato niente.</b> Prova con «Ultimi 7 giorni».') + '</p>';
    return;
  }
  dentro.innerHTML = pieni.map(g =>
    '<section class="giorno"><h2>' + g.titolo + '</h2>' +
    '<p class="quando">' + g.data + '</p>' + g.roba + '</section>').join('');
}
document.getElementById('b-oggi').onclick = () => { sette = false; disegna(); };
document.getElementById('b-sette').onclick = () => { sette = true; disegna(); };
document.getElementById('pie').textContent = __PIE__;
disegna();
</script>
</body>
</html>
'''

def costruisci():
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from catalogo import UNITA
    unita = {k: v[0] for k, v in UNITA.items()}
    oggi = datetime.date.today()

    giorni = []
    for f in sorted(glob.glob(os.path.join(STORIA, '2*.json')), reverse=True):
        d = json.load(open(f, encoding='utf-8'))
        data = datetime.date.fromisoformat(d['giorno'])
        if (oggi - data).days > 7:
            continue
        giorni.append(dict(titolo=in_italiano(d['giorno'], oggi),
                           data=f'{data.day} {MESI[data.month - 1]} {data.year}',
                           roba=giorno_html(d, unita, oggi)))
    if not giorni or giorni[0]['titolo'] != 'Oggi':
        giorni.insert(0, dict(titolo='Oggi',
                              data=f'{oggi.day} {MESI[oggi.month - 1]} {oggi.year}', roba=''))

    pie = ('Le novità si contano da un giorno all\'altro: quello che vedi qui è la '
           'differenza rispetto all\'ultima volta che ho letto i volantini.')
    html_out = (PAGINA.replace('__GIORNI__', json.dumps(giorni, ensure_ascii=False))
                      .replace('__PIE__', json.dumps(pie, ensure_ascii=False)))
    os.makedirs('out', exist_ok=True)
    open('out/novita.html', 'w', encoding='utf-8').write(html_out)
    pieni = len([g for g in giorni if g['roba']])
    print(f'out/novita.html — {len(giorni)} giorni, di cui {pieni} con qualcosa dentro')

if __name__ == '__main__':
    costruisci()
