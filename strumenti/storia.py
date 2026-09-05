# -*- coding: utf-8 -*-
"""Tiene il diario di cosa cambia da un giorno all'altro.

Manlio ha chiesto una pagina con le novità del giorno e, a scelta, quelle
degli ultimi sette giorni. La pagina si farà dopo, ma il diario va cominciato
SUBITO: le novità di lunedì si possono raccontare solo se domenica qualcuno ha
segnato com'era. Aspettare la pagina vorrebbe dire una prima settimana vuota.

Come funziona: `storia/stato.json` è la fotografia di adesso. A ogni giro si
confronta la fotografia vecchia con quella nuova e si scrive la differenza in
`storia/AAAA-MM-GG.json`. Le fotografie non si accumulano — ne resta una sola,
l'ultima — mentre le differenze sì, e sono piccole: è da quelle che la pagina
metterà insieme la settimana.

    python3 -m storia            scrive la differenza e aggiorna la fotografia
    python3 -m storia --guarda   dice soltanto cosa cambierebbe

Un'offerta è la stessa offerta se sono uguali insegna, prodotto e formato. La
categoria NON entra nel riconoscimento: il 2026-09-05, dividendo «Formaggio» in
mozzarella, grana, spalmabili e ricotta, il diario ha annunciato 38 offerte
sparite e altrettante nuove — erano le stesse, spostate di scaffale. Un
cambio di reparto si racconta a parte, e il prezzo invece deve poter cambiare:
quella è proprio la cosa che vogliamo vedere.
"""
import datetime, json, os, sys
from dati import PRODOTTI, VOLANTINI, UNITA

QUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOVE = os.path.join(QUI, 'storia')
FOTO = os.path.join(DOVE, 'stato.json')

def fotografia():
    offerte = {}
    for cat, ins, chiave, rep, pro, fmt, qta, pre, pag, fon, note in PRODOTTI:
        offerte['\t'.join((ins, pro, fmt))] = dict(
            cat=cat, ins=ins, pro=pro, fmt=fmt, prezzo=pre,
            unitario=round(pre / qta, 3), chiave=chiave)
    return dict(
        giorno=datetime.date.today().isoformat(),
        volantini={v.chiave: dict(ins=v.insegna, periodo=v.periodo,
                                  inizio=v.inizio, fino=v.fino)
                   for v in VOLANTINI},
        offerte=offerte)

def meno_caro(offerte):
    """Per ogni categoria l'offerta che costa meno per unità.

    È la novità che conta davvero: sapere che è comparso un tonno non serve,
    sapere che il tonno più conveniente adesso è un altro sì."""
    fuori = {}
    for o in offerte.values():
        c = o['cat']
        if c not in fuori or o['unitario'] < fuori[c]['unitario']:
            fuori[c] = o
    return fuori

def differenza(prima, adesso):
    vp, va = prima.get('volantini', {}), adesso['volantini']
    op, oa = prima.get('offerte', {}), adesso['offerte']
    mp, ma = meno_caro(op), meno_caro(oa)

    cambiati, traslocati = [], []
    for k in set(op) & set(oa):
        if abs(op[k]['unitario'] - oa[k]['unitario']) > 0.005:
            cambiati.append(dict(oa[k], prima=op[k]['unitario']))
        if op[k]['cat'] != oa[k]['cat']:
            traslocati.append(dict(oa[k], cat_prima=op[k]['cat']))
    capovolti = []
    for cat, nuovo in ma.items():
        vecchio = mp.get(cat)
        if vecchio and (vecchio['ins'], vecchio['pro']) != (nuovo['ins'], nuovo['pro']):
            capovolti.append(dict(cat=cat, ins=nuovo['ins'], pro=nuovo['pro'],
                                  unitario=nuovo['unitario'],
                                  ins_prima=vecchio['ins'], pro_prima=vecchio['pro'],
                                  unitario_prima=vecchio['unitario'],
                                  unita=UNITA.get(cat, ('al kg',))[0]))
    return dict(
        giorno=adesso['giorno'],
        volantini_arrivati=[dict(chiave=k, **va[k]) for k in va if k not in vp],
        volantini_finiti=[dict(chiave=k, **vp[k]) for k in vp if k not in va],
        offerte_nuove=[oa[k] for k in oa if k not in op],
        offerte_sparite=[op[k] for k in op if k not in oa],
        prezzi_cambiati=sorted(cambiati, key=lambda o: o['unitario'] - o['prima']),
        cambiati_reparto=sorted(traslocati, key=lambda o: o['cat']),
        meno_caro_cambiato=sorted(capovolti, key=lambda x: x['cat']),
    )

def quanto(d):
    return (len(d['volantini_arrivati']) + len(d['volantini_finiti'])
            + len(d['offerte_nuove']) + len(d['offerte_sparite'])
            + len(d['prezzi_cambiati']))

if __name__ == '__main__':
    solo_guardare = '--guarda' in sys.argv
    os.makedirs(DOVE, exist_ok=True)
    adesso = fotografia()
    prima = json.load(open(FOTO, encoding='utf-8')) if os.path.exists(FOTO) else {}

    if not prima:
        print('prima fotografia: da domani ci sarà qualcosa da confrontare.')
        if not solo_guardare:
            json.dump(adesso, open(FOTO, 'w', encoding='utf-8'), ensure_ascii=False)
            print(f"segnate {len(adesso['offerte'])} offerte e "
                  f"{len(adesso['volantini'])} volantini in storia/stato.json")
        raise SystemExit

    d = differenza(prima, adesso)
    print(f"da {prima.get('giorno', '?')} a {d['giorno']}:")
    print(f"  volantini arrivati  {len(d['volantini_arrivati'])}")
    print(f"  volantini finiti    {len(d['volantini_finiti'])}")
    print(f"  offerte nuove       {len(d['offerte_nuove'])}")
    print(f"  offerte sparite     {len(d['offerte_sparite'])}")
    print(f"  prezzi cambiati     {len(d['prezzi_cambiati'])}")
    if d['cambiati_reparto']:
        print(f"  cambiati di reparto {len(d['cambiati_reparto'])}")
    for c in d['meno_caro_cambiato']:
        print(f"  → il {c['cat'].lower()} più conveniente adesso è "
              f"{c['pro']} ({c['ins']}), {c['unitario']:.2f} {c['unita']}")
    if solo_guardare:
        raise SystemExit

    if quanto(d):
        fuori = os.path.join(DOVE, f"{d['giorno']}.json")
        json.dump(d, open(fuori, 'w', encoding='utf-8'), ensure_ascii=False)
        print(f"scritto storia/{d['giorno']}.json")
    else:
        print('niente di nuovo: nessun file scritto.')
    json.dump(adesso, open(FOTO, 'w', encoding='utf-8'), ensure_ascii=False)
