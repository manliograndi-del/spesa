# -*- coding: utf-8 -*-
"""Quali pagine dei volantini ho letto davvero, e quali no.

Nato il 2026-09-05 da una domanda di Manlio: «cosa sta succedendo, alcune cose
non le guardi perché». La risposta era un numero che non avevo mai calcolato:
79 pagine lette su 332.

IL MOTIVO, che e anche il difetto del metodo. Fino a oggi aprivo una pagina
solo se una PAROLA me la faceva trovare: cercavo «pizza» nell'indice OCR e
leggevo quelle pagine. Cosi si trova solo cio che si e gia pensato di cercare.
Le pizze, Mercato e il pesce sono lo stesso errore tre volte: nessuno dei tre
era difficile, erano tutti dietro una pagina che non avevo aperto.

    python3 -m lette              quante pagine per volantino
    python3 -m lette bennet       quali pagine del Bennet mancano

Una pagina si conta «letta» se almeno un prezzo la nomina. E una misura per
difetto — una pagina di detersivi guardata e scartata risulta non letta — ma
sbaglia dalla parte giusta: meglio riaprirla per niente che non aprirla mai.

Non e una prova che fallisce: e un promemoria. Il 100% non e l'obiettivo, un
volantino ha pagine di pentole e di quaderni. Serve a non credere di aver
guardato tutto quando si e guardato un quarto.
"""
import json, os, sys, collections
from dati import OFFERTE, VOLANTINI

def coperture():
    dove = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'indice.json')
    sorgente = 'indice.json' if os.path.exists('indice.json') else dove
    idx = json.load(open(sorgente, encoding='utf-8'))
    tutte = collections.defaultdict(set)
    for r in idx:
        tutte[r['chiave']].add(r['pagina'])
    lette = collections.defaultdict(set)
    for o in OFFERTE:
        if o.pag:
            lette[o.chiave].add(o.pag)
    return tutte, lette

if __name__ == '__main__':
    tutte, lette = coperture()
    soltanto = sys.argv[1] if len(sys.argv) > 1 else None
    T = L = 0
    for v in VOLANTINI:
        t, l = tutte.get(v.chiave, set()), lette.get(v.chiave, set())
        T += len(t); L += len(l)
        if soltanto and v.chiave != soltanto:
            continue
        quota = 100 * len(l) / len(t) if t else 0
        print('%-16s %-15s %3d pagine, %3d lette  %3d%%' % (v.chiave, v.insegna, len(t), len(l), quota))
        if soltanto:
            mancano = sorted(t - l)
            print('   da leggere: ' + (', '.join(map(str, mancano)) if mancano else 'nessuna'))
    if not soltanto:
        print('%-32s %3d pagine, %3d lette  %3d%%' % ('TUTTI', T, L, 100 * L / T if T else 0))
        print('\nPer sapere quali mancano:  python3 -m lette <chiave>')
