# -*- coding: utf-8 -*-
"""I «look» della pagina: 100 combinazioni di colori, una per palette.

Chieste da Manlio il 2026-09-22, dal PDF «100 combinazioni di colori per il tuo
prossimo design» di Figma. Le palette stanno qui sotto in PALETTE, lette dal
PDF striscia per striscia: dove la sigla scritta sotto la striscia era
leggibile (239 colori su 400) vale quella, se no vale il colore campionato dal
pixel in mezzo alla striscia, che il PDF sposta di un paio di punti.

## Le quattro regole che questo file fa rispettare

1. **I colori della pagina hanno un significato, non sono decorazione.** Il
   rosso vuol dire «prodotto acceso» e «premi qui»; il verde è il bollino «il
   meno caro»; l'ambra è un avviso. Un look cambia lo SFONDO, il TESTO, le
   RIGHE e il colore di ACCENTO. Verde e ambra restano riconoscibili: cambia
   solo la loro tinta di fondo, per stare su una pagina chiara o scura.

2. **Si legge, sempre.** Ogni look passa le stesse misure di contrasto
   (WCAG): testo 7:1 sullo sfondo, testo tenue e accento 4.5:1, la scritta
   dentro il bottone rosso 4.5:1 sul rosso. Dove la palette non ci arriva, il
   colore viene scurito o schiarito finché non ci arriva: meglio un look un po'
   diverso dalla palette che un prezzo che non si legge. `verifica()` qui sotto
   lo ricontrolla e si ferma se qualcosa non torna.

3. **Niente look che si accende da solo.** La pagina parte com'è sempre stata:
   il look si sceglie a mano e resta scelto. È diverso da
   `prefers-color-scheme: dark`, che è vietato da CLAUDE.md perché il telefono
   di Manlio è in modalità notte e la pagina gli si apriva nera senza che lui
   avesse chiesto niente.

4. **Una palette scura fa un look scuro.** Se nessuno dei suoi colori è
   chiaro, invece di sbiancarla a forza si fa una pagina scura con il testo
   chiaro: è quello che la palette vuole dire, e Manlio l'ha scelta lui.
"""
import json, os

QUI = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- i conti sui colori

def _rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _hex(t):
    return '#%02X%02X%02X' % tuple(max(0, min(255, int(round(x)))) for x in t)

def _canale(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def luce(colore):
    """La luminosità di un colore, come la misura la regola sul contrasto."""
    r, g, b = _rgb(colore)
    return 0.2126 * _canale(r) + 0.7152 * _canale(g) + 0.0722 * _canale(b)

def contrasto(a, b):
    """Quanto due colori si staccano: 21 è nero su bianco, 1 è invisibile."""
    la, lb = luce(a), luce(b)
    alto, basso = max(la, lb), min(la, lb)
    return (alto + 0.05) / (basso + 0.05)

def mescola(a, b, quanto):
    """`quanto` di b dentro a: 0 = solo a, 1 = solo b."""
    ra, rb = _rgb(a), _rgb(b)
    return _hex([ra[i] + (rb[i] - ra[i]) * quanto for i in range(3)])

def _saturazione(colore):
    r, g, b = [x / 255 for x in _rgb(colore)]
    return max(r, g, b) - min(r, g, b)

def _porta_a(colore, fondo, quanto, verso):
    """Scurisce (verso='nero') o schiarisce un colore finché non stacca
    abbastanza dal fondo. Torna il colore com'era se ci arriva subito."""
    meta = '#000000' if verso == 'nero' else '#FFFFFF'
    for passo in range(0, 101, 4):
        prova = mescola(colore, meta, passo / 100)
        if contrasto(prova, fondo) >= quanto:
            return prova
    return meta

# ---------------------------------------------------------------- da palette a look

def _look(palette):
    """Le quattro (o più) tinte di una palette diventano i colori della pagina."""
    colori = list(palette['colori'])
    per_luce = sorted(colori, key=luce)
    scuro, chiaro = per_luce[0], per_luce[-1]
    notte = luce(chiaro) < 0.45           # nessun colore chiaro: pagina scura

    if notte:
        carta = mescola(scuro, '#000000', 0.35)
        pannello = mescola(scuro, '#FFFFFF', 0.08)
        inchiostro = _porta_a(chiaro, carta, 8.0, 'bianco')
    else:
        carta = mescola(chiaro, '#FFFFFF', 0.86)
        pannello = mescola(chiaro, '#FFFFFF', 0.62)
        inchiostro = _porta_a(scuro, carta, 8.0, 'nero')

    # L'ACCENTO: il colore più vivo che non sia lo sfondo né il testo. È quello
    # che nella pagina vuol dire «acceso» e «premi qui», quindi è il colore che
    # si riconosce di più della palette.
    candidati = [c for c in colori if c not in (chiaro, scuro)] or colori
    accento = max(candidati, key=lambda c: (_saturazione(c), -abs(luce(c) - 0.35)))
    accento = _porta_a(accento, carta, 4.5, 'bianco' if notte else 'nero')

    su_accento = '#FFFFFF' if contrasto('#FFFFFF', accento) >= contrasto('#111111', accento) else '#111111'

    # Il pannello è la superficie di dentro (cassetto, finestre, riquadri): se
    # resta troppo vicino al testo si legge peggio dello sfondo. Lo si porta
    # verso lo sfondo finché il testo ci si stacca.
    for passo in range(0, 101, 5):
        if contrasto(inchiostro, pannello) >= 6.0:
            break
        pannello = mescola(pannello, carta, 0.12)

    tenue = _porta_a(mescola(inchiostro, carta, 0.42), carta, 4.5, 'bianco' if notte else 'nero')
    linea = mescola(carta, inchiostro, 0.14 if not notte else 0.22)
    linea_forte = mescola(carta, inchiostro, 0.30 if not notte else 0.40)

    # Verde e ambra restano verde e ambra: cambia solo quanto sono chiari, per
    # stare su una pagina scura senza sparire.
    verde = _porta_a('#1E7A4B' if not notte else '#4ADE80', carta, 4.5, 'bianco' if notte else 'nero')
    ambra = _porta_a('#8A5A08' if not notte else '#F0B429', carta, 4.5, 'bianco' if notte else 'nero')
    blu = _porta_a('#2B4A7A' if not notte else '#9DBBEA', carta, 4.5, 'bianco' if notte else 'nero')

    return {
        'carta': carta, 'pannello': pannello, 'inchiostro': inchiostro, 'tenue': tenue,
        'linea': linea, 'linea-forte': linea_forte,
        'rosso': accento, 'su-rosso': su_accento,
        'rosso-tenue': mescola(carta, accento, 0.14),
        'verde': verde, 'verde-tenue': mescola(carta, verde, 0.16),
        'ambra': ambra, 'ambra-tenue': mescola(carta, ambra, 0.16),
        'blu': blu, 'blu-tenue': mescola(carta, blu, 0.16),
        'notte': notte,
    }

# ---------------------------------------------------------------- i dati

PALETTE = json.load(open(os.path.join(QUI, 'palette.json'), encoding='utf-8'))

FAMIGLIE = ['monocromatici', 'neutri', 'tranquilli', 'romantici',
            'giocose', 'vivaci', 'stagionali']

def costruisci():
    fuori = []
    for p in PALETTE:
        v = _look(p)
        fuori.append(dict(id='c%03d' % p['n'], nome=p['nome'], fam=p['famiglia'],
                          base=p['colori'], notte=v.pop('notte'), v=v))
    fuori.sort(key=lambda x: (FAMIGLIE.index(x['fam']) if x['fam'] in FAMIGLIE else 9, x['id']))
    return fuori

LOOK = costruisci()

# ---------------------------------------------------------------- il controllo

MISURE = [
    ('il testo sullo sfondo', 'inchiostro', 'carta', 7.0),
    ('il testo tenue sullo sfondo', 'tenue', 'carta', 4.5),
    ('l\'accento sullo sfondo', 'rosso', 'carta', 4.5),
    ('la scritta dentro il bottone acceso', 'su-rosso', 'rosso', 4.5),
    ('il verde del «meno caro»', 'verde', 'carta', 4.5),
    ('l\'ambra degli avvisi', 'ambra', 'carta', 4.5),
    ('il testo sul pannello', 'inchiostro', 'pannello', 6.0),
]

def verifica(look=None):
    """Ogni look deve reggere tutte le misure. Se una non regge il programma si
    ferma: un look che non si legge non si pubblica, come una prova che non
    passa."""
    guai = []
    for l in (look or LOOK):
        for nome, a, b, minimo in MISURE:
            c = contrasto(l['v'][a], l['v'][b])
            if c < minimo - 0.01:
                guai.append('%s (%s): %s è %.1f:1, ne serve %.1f' %
                            (l['nome'], l['id'], nome, c, minimo))
    if guai:
        raise SystemExit('LOOK CHE NON SI LEGGONO:\n  ' + '\n  '.join(guai))
    return True

if __name__ == '__main__':
    verifica()
    scuri = [l for l in LOOK if l['notte']]
    print('look costruiti:', len(LOOK), '— di cui scuri:', len(scuri))
    for f in FAMIGLIE:
        print('  %-16s %d' % (f, sum(1 for l in LOOK if l['fam'] == f)))
    print('tutti leggibili: sì')
