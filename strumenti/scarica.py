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
for chiave, insegna, _, _, _, modello in VOLANTINI:
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
    # -f fa fallire curl sui 404, così le pagine oltre la fine del volantino
    # non restano sul disco come file vuoti che poi l'OCR conta come pagine.
    subprocess.run(['xargs', '-a', 'urls.txt', '-P', '12', '-n', '2', 'sh', '-c',
                    f'curl -sSf -o "$0" --max-time 35 -A "{UA}" "$1" >/dev/null 2>&1 || rm -f "$0"'])

for chiave, insegna, *_ in VOLANTINI:
    d = f'pg/{chiave}'
    if os.path.isdir(d):
        print(f'{chiave:16s} {len(os.listdir(d)):3d} pagine')
