# -*- coding: utf-8 -*-
"""Costruisce indice.json: per ogni pagina, le parole leggibili trovate dall'OCR.

L'OCR sulle pagine dei volantini restituisce molta spazzatura (sono immagini
disegnate, non testo). Il filtro qui sotto tiene solo le parole che hanno la
forma di una parola italiana; i prezzi non passano quasi mai, perche sono
numeri grandi e stilizzati che tesseract non riconosce. Per questo l'indice
serve a trovare LA PAGINA, e il prezzo si legge poi sul PDF.
"""
import glob, os, re, json, sys
from dati import VOLANTINI

# Le insegne e i periodi NON si riscrivono qui: vengono da dati.py, che è
# l'unico posto dove stanno. Prima erano copiati anche qui dentro, e la copia
# restava indietro: il 2026-09-04 nominava ancora un volantino tolto.
META = {c: (i, p) for c, i, p, _, _, _ in VOLANTINI}

VOC = set('aeiouàèéìòù')

def plausibile(w):
    w = w.strip(" .,;:|_-–—•*()[]{}\"'”“’«»/\\!?")
    if not 4 <= len(w) <= 22:
        return None
    lw = w.lower()
    if not all(c.isalpha() or c in "'-" for c in lw):
        return None
    v = sum(1 for c in lw if c in VOC)
    if not 0.22 <= v / len(lw) <= 0.75:      # senza vocali, o tutte vocali: e rumore
        return None
    if re.search(r'(.)\1\1', lw):            # tre lettere uguali di fila: e rumore
        return None
    return lw

# INCREMENTALE. indice.json sta nel progetto ed è già buono per i volantini
# vecchi: qui si rileggono solo le pagine di cui c'è l'OCR sul disco, e il
# resto si tiene. Così il controllo giornaliero scarica e legge SOLO il
# volantino nuovo invece di rifare tutti e sette da capo — che è la ragione
# per cui prima non finiva mai in tempo.
DOVE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'indice.json')
sorgente = 'indice.json' if os.path.exists('indice.json') else DOVE
righe = json.load(open(sorgente, encoding='utf-8')) if os.path.exists(sorgente) else []
righe = [r for r in righe if r['chiave'] in META]      # via i volantini tolti da dati.py
for r in righe:                                        # periodi sempre quelli di dati.py
    r['insegna'], r['validita'] = META[r['chiave']]
avute = {(r['chiave'], r['pagina']) for r in righe}

nuove = 0
for chiave, (insegna, validita) in sorted(META.items()):
    for f in sorted(glob.glob(f'ocr/{chiave}/*.txt')):
        pagina = int(os.path.basename(f)[:-4])
        parole = []
        for w in re.split(r'\s+', open(f, encoding='utf-8', errors='ignore').read()):
            pp = plausibile(w)
            if pp and pp not in parole:
                parole.append(pp)
        riga = dict(chiave=chiave, insegna=insegna, validita=validita,
                    pagina=pagina, parole=' '.join(sorted(parole)))
        if (chiave, pagina) in avute:
            for i, r in enumerate(righe):
                if (r['chiave'], r['pagina']) == (chiave, pagina):
                    righe[i] = riga; break
        else:
            righe.append(riga); nuove += 1

righe.sort(key=lambda r: (r['chiave'], r['pagina']))
if not righe:
    sys.exit('indice vuoto: fermati, rigenerare adesso svuoterebbe la pagina.')
json.dump(righe, open(DOVE, 'w', encoding='utf-8'), ensure_ascii=False)
if os.path.abspath('indice.json') != DOVE:
    json.dump(righe, open('indice.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(f'pagine indicizzate: {len(righe)} (nuove: {nuove})')
