# -*- coding: utf-8 -*-
"""Segna in registro.txt a che punto è arrivato il controllo giornaliero.

Nasce da un guaio preciso: il 4 e il 5 settembre 2026 il controllo automatico
è partito, ha lavorato (diciassette minuti l'ultima volta) e non ha pubblicato
né detto niente. Dal di fuori si vede solo che non è successo nulla, e non c'è
modo di sapere DOVE si sia fermato: la sessione che parte da sola non lascia
niente da rileggere.

Questo lo risolve nel modo più stupido che funziona: ogni passo scrive una riga
e la spinge sul progetto. Se domani in registro.txt c'è «clonato» e non c'è
«pubblicato», si sa che il clone e la spinta funzionano e il guaio sta in mezzo.
Se non c'è nemmeno «clonato», il guaio è prima.

    python3 -m registro "clonato"
    python3 -m registro "niente da fare"      e poi git commit && git push
"""
import datetime, os, sys

QUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOVE = os.path.join(QUI, 'registro.txt')

def segna(testo):
    riga = f'{datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC  {testo}\n'
    with open(DOVE, 'a', encoding='utf-8') as f:
        f.write(riga)
    return riga

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('uso: python3 -m registro "cosa è appena successo"')
    print(segna(' '.join(sys.argv[1:])).rstrip())
