# -*- coding: utf-8 -*-
"""Il catalogo su un foglio da stampare e correggere a penna.

Chiesto da Manlio il 2026-09-05: «fammi un elenco delle categorie merceologiche
e dei sinonimi formattato in un bel PDF che possa stampare e correggere io, sai
gli umani servono ancora a qualcosa». Ha ragione: le parole che il computer
cerca nei volantini le puo giudicare solo chi in quei negozi ci va. Se manca
«bovino» la carne di bue in offerta non si trova, e nessuna prova automatica se
ne accorge — non e un guasto, e una parola che non c'e.

    python3 -m stampa            out/catalogo.pdf e out/catalogo.html

La prima volta era uno script buttato via dopo l'uso, e infatti alla richiesta
dopo non c'era piu. Adesso sta qui: **si rilancia a ogni modifica del catalogo**,
se no il foglio stampato racconta un catalogo che non esiste piu.

Il PDF lo fa Chromium senza finestra. Il conto delle offerte viene da dati.py:
uno zero non e un errore, vuol dire che questa settimana quella voce non e in
offerta da nessuna parte, ed e proprio l'informazione che serve per capire se
una voce e sbagliata o solo sfortunata.
"""
import datetime as _dt, html, os, subprocess, sys
from catalogo import REPARTI, METRI
from dati import OFFERTE

CHROME = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'
MESI = ('gennaio febbraio marzo aprile maggio giugno luglio agosto settembre '
        'ottobre novembre dicembre').split()

def _oggi():
    o = _dt.date.today()
    return f'{o.day} {MESI[o.month - 1]} {o.year}'

def _quante():
    """Quante offerte ha oggi ogni voce. Le scadute non si contano: il foglio
    serve a giudicare il catalogo adesso, non il mese scorso."""
    oggi = _dt.date.today().isoformat()
    n = {}
    for o in OFFERTE:
        if o.fino and o.fino < oggi:
            continue
        n[o.cat] = n.get(o.cat, 0) + 1
    return n

STILE = """
@page { size: A4; margin: 14mm 12mm 16mm; }
* { box-sizing: border-box; }
body { font: 9.5pt/1.35 "DejaVu Sans", Arial, sans-serif; color: #1B1B1A; margin: 0; }
h1 { font-size: 19pt; margin: 0; letter-spacing: -.01em; }
.testa { border-bottom: 2.5pt solid #1B1B1A; padding-bottom: 7pt; margin-bottom: 11pt;
  display: flex; align-items: flex-end; justify-content: space-between; gap: 14pt; }
.testa .occhio { font-size: 7.5pt; letter-spacing: .16em; text-transform: uppercase;
  color: #D40D2B; font-weight: bold; margin: 0 0 3pt; }
.testa .data { font-size: 8pt; color: #6E6C66; text-align: right; white-space: nowrap; }
.istruzioni { background: #F6F5F2; border-left: 3pt solid #D40D2B; padding: 7pt 9pt;
  font-size: 8.5pt; margin-bottom: 11pt; }
.istruzioni p { margin: 0 0 4pt; }
.istruzioni p:last-child { margin-bottom: 0; }
table { width: 100%; border-collapse: collapse; }
th, td { text-align: left; vertical-align: top; padding: 3.2pt 4pt; }
tr.rep th { font-size: 8pt; letter-spacing: .12em; text-transform: uppercase;
  color: #6E6C66; border-bottom: .8pt solid #1B1B1A; padding-top: 11pt; }
tbody tr:not(.rep) { border-bottom: .4pt solid #E5E3DD; page-break-inside: avoid; }
td.segno { width: 13pt; }
td.segno::before { content: ""; display: block; width: 9pt; height: 9pt;
  border: .8pt solid #9A968C; border-radius: 1.5pt; margin-top: 1.5pt; }
td.nome { width: 30%; font-weight: bold; }
td.nome .unita { display: block; font-weight: normal; font-size: 7.5pt; color: #6E6C66; }
td.parole { color: #4A4842; font-size: 8.5pt; }
td.quanti { width: 7%; text-align: right; font-variant-numeric: tabular-nums;
  color: #6E6C66; font-size: 8.5pt; white-space: nowrap; }
.coda { margin-top: 14pt; border-top: .8pt solid #E5E3DD; padding-top: 7pt;
  font-size: 8pt; color: #6E6C66; }
"""

def costruisci():
    n = _quante()
    voci = sum(len(v) for _, v in REPARTI)
    r = ['<!doctype html><html lang="it"><head><meta charset="utf-8">',
         '<title>Catalogo della Spesa</title>', '<style>', STILE, '</style></head><body>',
         '<div class="testa">',
         '  <div><p class="occhio">Spesa &middot; Torino, corso Siracusa</p>'
         '<h1>Catalogo della spesa</h1></div>',
         f'  <div class="data">{voci} voci in {len(REPARTI)} reparti<br>'
         f'stampato il {_oggi()}</div>',
         '</div>',
         '<div class="istruzioni">',
         '  <p><b>A cosa serve questo foglio.</b> Le <b>parole</b> sono quelle che il computer '
         'cerca nelle pagine dei volantini. Se una parola manca, quel prodotto in offerta non lo '
         'trova: il volantino scrive &laquo;bovino&raquo; dove tu diresti carne di bue, '
         '&laquo;lavatrice&raquo; dove diresti detersivo.</p>',
         '  <p><b>Cosa correggere.</b> Aggiungi le parole che mancano, cancella quelle sbagliate, '
         'e segna con la casella a sinistra le voci da togliere o da spaccare in due. Scrivi a '
         'margine i prodotti che non ci sono per niente.</p>',
         '  <p><b>L&rsquo;ultima colonna</b> dice quante offerte ha oggi quella voce. Uno zero non '
         '&egrave; un errore: vuol dire che questa settimana non &egrave; in offerta da nessuna '
         'parte.</p>',
         '</div>', '<table><tbody>']
    for reparto, elenco in REPARTI:
        r.append(f'<tr class="rep"><th colspan="4">{html.escape(reparto)}</th></tr>')
        for nome, parole, unita in elenco:
            q = n.get(nome, 0)
            r.append('<tr><td class="segno"></td>'
                     f'<td class="nome">{html.escape(nome)}'
                     f'<span class="unita">{METRI[unita][0]}</span></td>'
                     f'<td class="parole">{html.escape(" &middot; ".join(parole.split()))}</td>'
                     f'<td class="quanti">{q if q else "&mdash;"}</td></tr>')
    r.append('</tbody></table>')
    r.append('<p class="coda">Le parole vanno minuscole e senza accenti: il confronto le abbassa '
             'da solo. Riconsegna il foglio corretto e le riporto nel catalogo.</p>')
    r.append('</body></html>')
    # &middot; e &mdash; passati da html.escape diventano testo: si rimettono
    return '\n'.join(r).replace('&amp;middot;', '&middot;').replace('&amp;mdash;', '&mdash;')

if __name__ == '__main__':
    os.makedirs('out', exist_ok=True)
    open('out/catalogo.html', 'w', encoding='utf-8').write(costruisci())
    if not os.path.exists(CHROME):
        sys.exit(f'manca Chromium in {CHROME}: il PDF non si fa, l HTML si')
    subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu',
                    '--no-pdf-header-footer', '--print-to-pdf=out/catalogo.pdf',
                    'file://' + os.path.abspath('out/catalogo.html')],
                   check=True, capture_output=True)
    voci = sum(len(v) for _, v in REPARTI)
    print(f'out/catalogo.pdf — {voci} voci, {os.path.getsize("out/catalogo.pdf") // 1024} KB')
