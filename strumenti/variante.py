# -*- coding: utf-8 -*-
"""Una VERSIONE DI PROVA della pagina, da confrontare con quella vera.

Chiesta da Manlio il 2026-09-22: «prova a farne anche una versione con i due
tasti, Cerca un prodotto o una marca e GRANDI MARCHE, messi sotto le
categorie». Non si decide qui quale tenere: la decide lui guardandole tutte e
due sul telefono.

La prova sta sul sito accanto a quella vera, `prova-tasti-sotto.html`: STESSO
indirizzo di casa, quindi legge la stessa lista di prodotti salvata nel
telefono e si confronta a parità di tutto. È la pagina di sempre (out/sito.html)
con una sola differenza: la riga dei due tasti spostata da sopra a sotto la
barra delle categorie.

    python3 -m variante        (dopo python3 -m pagina)

Se lui sceglie questa, la si fa diventare la pagina vera spostando la riga in
pagina.py, e questo file e la prova sul sito si cancellano.
"""
import os

RIGA = '<div class="riga-cerca" id="riga-cerca"></div>\n'
FINE_BARRA = '  <p class="stato" id="stato-lista" role="status"></p>\n</div>\n'
STILE = ('<style>/* versione di prova: i due tasti sotto le categorie */\n'
         '.riga-cerca{margin:12px 0 0}</style>\n')


def fai():
    t = open(os.path.join('out', 'sito.html'), encoding='utf-8').read()
    # Se la pagina cambia forma, meglio fermarsi che pubblicare una prova rotta.
    assert t.count(RIGA) == 1, 'non trovo la riga dei due tasti'
    assert t.count(FINE_BARRA) == 1, 'non trovo la fine della barra delle categorie'
    t = t.replace(RIGA, '', 1)
    t = t.replace(FINE_BARRA, FINE_BARRA + STILE + RIGA, 1)
    dove = os.path.join('out', 'prova-tasti-sotto.html')
    open(dove, 'w', encoding='utf-8').write(t)
    print('scritta', dove)


if __name__ == '__main__':
    fai()
