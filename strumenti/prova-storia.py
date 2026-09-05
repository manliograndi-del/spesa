# -*- coding: utf-8 -*-
"""Controlla che il diario racconti il vero.

Si finge un domani: un volantino che finisce, un'offerta che sparisce, una che
arriva, un prezzo che scende, e il più conveniente di una categoria che cambia
padrone. Poi si pretende che la differenza dica esattamente quelle cinque cose.

    python3 -m prova_storia        (con PYTHONPATH sugli strumenti)
"""
import copy
from storia import fotografia, differenza

oggi = fotografia()
domani = copy.deepcopy(oggi)
domani['giorno'] = '2999-01-01'

guai = []

# 1. un volantino finisce
finito = sorted(domani['volantini'])[0]
del domani['volantini'][finito]

# 2. un'offerta sparisce, 3. una arriva
chiavi = sorted(domani['offerte'])
sparita = chiavi[0]
del domani['offerte'][sparita]
domani['offerte']['Tonno\tPippo\tTonno finto\t100 g'] = dict(
    cat='Tonno', ins='Pippo', pro='Tonno finto', fmt='100 g',
    prezzo=0.10, unitario=1.0, chiave='finto')

# 4. un prezzo scende  5. e con quello cambia il più conveniente del tonno
#
# Il tonno da far calare va SCELTO, non preso a caso: la prima volta la prova
# aveva pescato quello che era già il più conveniente, e abbassarlo non
# cambiava padrone. La prova diceva «non se ne accorge» e il diario invece
# aveva ragione.
tonni = [k for k in domani['offerte'] if domani['offerte'][k]['cat'] == 'Tonno'
         and domani['offerte'][k]['ins'] != 'Pippo']
gia_meno_caro = min(tonni, key=lambda k: domani['offerte'][k]['unitario'])
calato = next(k for k in tonni if k != gia_meno_caro)
domani['offerte'][calato] = dict(domani['offerte'][calato], unitario=0.5, prezzo=0.5)

d = differenza(oggi, domani)

def pretendi(quanti, quali, nome):
    if len(quali) != quanti:
        guai.append(f'{nome}: attesi {quanti}, trovati {len(quali)}')

pretendi(1, d['volantini_finiti'], 'volantini finiti')
pretendi(0, d['volantini_arrivati'], 'volantini arrivati')
pretendi(1, d['offerte_nuove'], 'offerte nuove')
pretendi(1, d['offerte_sparite'], 'offerte sparite')
pretendi(1, d['prezzi_cambiati'], 'prezzi cambiati')

cam = d['prezzi_cambiati']
if cam and cam[0]['unitario'] >= cam[0]['prima']:
    guai.append('il prezzo calato non risulta calato')

capo = [c for c in d['meno_caro_cambiato'] if c['cat'] == 'Tonno']
if not capo:
    guai.append('il tonno più conveniente è cambiato e il diario non se ne accorge')
elif capo[0]['unitario'] >= capo[0]['unitario_prima']:
    guai.append('dice che il nuovo più conveniente costa di più di quello di prima')

print(f"  volantino finito:  {d['volantini_finiti'][0]['ins'] if d['volantini_finiti'] else '—'}")
print(f"  offerta sparita:   {d['offerte_sparite'][0]['pro'][:44] if d['offerte_sparite'] else '—'}")
print(f"  offerta nuova:     {d['offerte_nuove'][0]['pro'] if d['offerte_nuove'] else '—'}")
if cam:
    print(f"  prezzo calato:     {cam[0]['pro'][:34]} da {cam[0]['prima']:.2f} a {cam[0]['unitario']:.2f}")
if capo:
    print(f"  più conveniente:   {capo[0]['cat']} passa a {capo[0]['pro'][:34]} ({capo[0]['ins']})")

if guai:
    print('\nNON VA:')
    for g in guai:
        print('  ✗ ' + g)
    raise SystemExit(1)
print('  il diario racconta il vero')
