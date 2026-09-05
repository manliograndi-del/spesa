# -*- coding: utf-8 -*-
"""Scarica le pagine dei volantini.

Gli indirizzi NON si riscrivono qui: sono già in dati.py, nell'ultimo campo di
VOLANTINI, con {n} al posto del numero di pagina — gli stessi che rendono
cliccabili le righe della pagina. Prima erano copiati anche in uno script a
parte e le due copie divergevano.

    python3 scarica.py                 tutti i volantini che mancano
    python3 scarica.py carriper04      soltanto questo

Scarica solo quello che non c'è già: rilanciarlo non riscarica niente.
"""
import os, subprocess, sys
from dati import VOLANTINI

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120'
soltanto = set(sys.argv[1:])

righe = []
for v in VOLANTINI:
    chiave, modello = v.chiave, v.indirizzo
    if soltanto and chiave not in soltanto:
        continue
    os.makedirs(f'pg/{chiave}', exist_ok=True)
    for n in range(1, 61):
        dove = f'pg/{chiave}/{n:03d}.jpg'
        if not (os.path.isfile(dove) and os.path.getsize(dove)):
            righe.append(f'{dove} {modello.format(n=n)}')

if not righe:
    print('niente da scaricare')
else:
    open('urls.txt', 'w').write('\n'.join(righe) + '\n')
    # -f fa fallire curl sui 404. Non basta: il 2026-09-05 la fonte ha risposto
    # **200 con un'immagine finta da 1,2 KB** per una pagina che non esiste, e
    # anche i 403 arrivano con un corpo di quella misura. Quindi si guarda la
    # DIMENSIONE, non il codice: sotto i 20 KB non e una pagina di volantino.
    # E si riprova tre volte, perche la fonte ogni tanto molla una pagina buona.
    subprocess.run(['xargs', '-a', 'urls.txt', '-P', '8', '-n', '2', 'sh', '-c',
                    'for t in 1 2 3; do '
                    f'curl -sS -o "$0" --max-time 40 -A "{UA}" "$1" >/dev/null 2>&1'
                    ' && [ "$(stat -c%s "$0")" -gt 20000 ] && exit 0; sleep 2; done; rm -f "$0"'])

for v in VOLANTINI:
    d = f'pg/{v.chiave}'
    if os.path.isdir(d):
        print(f'{v.chiave:16s} {len(os.listdir(d)):3d} pagine')
