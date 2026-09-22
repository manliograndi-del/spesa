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
import datetime, json, os, subprocess, sys, tempfile
from dati import OFFERTE, VOLANTINI, UNITA
from catalogo import RINOMINATE

QUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOVE = os.path.join(QUI, 'storia')
FOTO = os.path.join(DOVE, 'stato.json')

def fotografia():
    offerte = {}
    vol = {v.chiave: v for v in VOLANTINI}
    for o in OFFERTE:
        v = vol[o.chiave]
        offerte['\t'.join((o.ins, o.pro, o.fmt))] = dict(
            cat=o.cat, ins=o.ins, pro=o.pro, fmt=o.fmt, prezzo=o.prezzo,
            unitario=round(o.prezzo / o.qta, 3), chiave=o.chiave,
            inizio=o.inizio or v.inizio, fino=o.fino or v.fino)
    return dict(
        giorno=datetime.date.today().isoformat(),
        volantini={v.chiave: dict(ins=v.insegna, periodo=v.periodo,
                                  inizio=v.inizio, fino=v.fino)
                   for v in VOLANTINI},
        offerte=offerte)

def git(*argomenti):
    """Una domanda a git, dalla cartella del progetto. None se git non c'è o
    non risponde: qui dentro nessuna risposta deve far cadere il programma."""
    try:
        return subprocess.run(('git', '-C', QUI) + argomenti, check=True,
                              capture_output=True, text=True).stdout.strip()
    except Exception:
        return None


def commit_di_dati():
    """I commit che hanno toccato i prezzi, dal più recente: [(sigla, data)].

    Serve a rifare la fotografia di un giorno qualsiasi: i prezzi di quel
    giorno sono quelli dell'ultimo commit fino a quel giorno."""
    fuori = git('log', '--format=%H %cs', '--', 'strumenti/dati.py')
    if not fuori:
        return []
    return [(r.split()[0], r.split()[1]) for r in fuori.splitlines() if ' ' in r]


def fotografia_da_commit(commit, giorno):
    """La fotografia com'era a un certo commit, datata al giorno che si vuole.

    È la RISPOSTA AL BUCO: `storia/stato.json` non sta nel repository — «le
    fotografie no, le differenze sì» — e ogni sessione nuova parte da un clone
    pulito, quindi senza. Il diario diceva «prima fotografia» tutte le notti e
    non scriveva mai un giorno: dal 9 al 15 settembre 2026 la pagina Novità è
    rimasta ferma, e Manlio se n'è accorto da fuori. Ma la fotografia non serve
    tenerla: `strumenti/dati.py` è nel repository, e la fotografia è solo una
    lettura di quel file. Basta chiederla a git.

    Si tira fuori l'intera cartella `strumenti/` di quel commit e la si mette
    davanti a tutto in un processo a parte: `dati` e `catalogo` di allora
    devono stare insieme. A leggerli è QUESTO storia.py, non quello di allora:
    le due fotografie vanno confrontate, e devono avere la stessa forma."""
    if not commit:
        return None
    with tempfile.TemporaryDirectory() as tmp:
        try:
            tar = subprocess.run(('git', '-C', QUI, 'archive', commit, 'strumenti'),
                                 check=True, capture_output=True)
            subprocess.run(('tar', '-x', '-C', tmp), input=tar.stdout, check=True)
            programma = (
                'import sys, json, importlib.util\n'
                'sys.path.insert(0, sys.argv[1])\n'
                's = importlib.util.spec_from_file_location("storia_di_allora", sys.argv[2])\n'
                'm = importlib.util.module_from_spec(s); s.loader.exec_module(m)\n'
                'f = m.fotografia(); f["giorno"] = sys.argv[3]\n'
                'json.dump(f, sys.stdout, ensure_ascii=False)\n')
            fuori = subprocess.run(
                (sys.executable, '-c', programma, os.path.join(tmp, 'strumenti'),
                 os.path.abspath(__file__), giorno),
                check=True, capture_output=True, text=True).stdout
            return json.loads(fuori)
        except Exception as e:
            print(f'  non riesco a rifare la fotografia di {commit[:7]}: {e}')
            return None


def giorni_fra(da, a):
    """I giorni STRETTAMENTE in mezzo fra due date, in ordine.

    Servono perché una novità può nascere senza che nessuno tocchi i prezzi:
    a mezzanotte un volantino scade e il più conveniente di quella categoria
    diventa un altro. Saltando i giorni in mezzo, quelle novità finirebbero
    tutte ammucchiate sull'ultimo giorno, con la data sbagliata."""
    d = datetime.date.fromisoformat(da) + datetime.timedelta(days=1)
    fine = datetime.date.fromisoformat(a)
    while d < fine:
        yield d.isoformat()
        d += datetime.timedelta(days=1)


def meno_caro(offerte, giorno):
    """Per ogni categoria l'offerta che costa meno per unità, FRA QUELLE CHE
    VALGONO QUEL GIORNO.

    È la novità che conta davvero: sapere che è comparso un tonno non serve,
    sapere che il tonno più conveniente adesso è un altro sì.

    Le date non sono un dettaglio. La prima volta questo conto le ignorava, e
    appena entrate le sette offerte del «Weekend più uno» il diario ha
    annunciato che il pollo più conveniente erano dei würstel a 2,29 — veri, ma
    validi dal 18 settembre, tredici giorni dopo. Una novità falsa è peggio di
    nessuna novità: manda uno in negozio."""
    fuori = {}
    for o in offerte.values():
        if (o.get('inizio') or '') > giorno or (o.get('fino') or '9') < giorno:
            continue
        c = o['cat']
        if c not in fuori or o['unitario'] < fuori[c]['unitario']:
            fuori[c] = o
    return fuori

def differenza(prima, adesso):
    vp, va = prima.get('volantini', {}), adesso['volantini']
    op, oa = prima.get('offerte', {}), adesso['offerte']
    # UNA CATEGORIA CHE HA CAMBIATO NOME NON E UN'OFFERTA CHE HA CAMBIATO
    # REPARTO. Il 2026-09-22 i nomi delle categorie sono stati accorciati
    # (catalogo.py): senza questa riga il diario di quel giorno avrebbe
    # annunciato che 393 offerte erano traslocate — «Prosciutto crudo diventa
    # Prosciutto» ripetuto 26 volte — e una novita falsa manda uno in negozio.
    # Si traduce la fotografia VECCHIA coi nomi di adesso e si confronta.
    op = {k: (dict(o, cat=RINOMINATE[o['cat']]) if o.get('cat') in RINOMINATE else o)
          for k, o in op.items()}
    mp = meno_caro(op, prima.get('giorno', adesso['giorno']))
    ma = meno_caro(oa, adesso['giorno'])

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
    """Quante cose sono successe. Il cambio del più conveniente conta, e non è
    ovvio: può cambiare SENZA che nessuna offerta si muova, semplicemente
    perché quella di ieri è scaduta stanotte. Senza contarlo, il giorno in cui
    scade il volantino dell'Eurospin il diario direbbe «niente di nuovo»."""
    return (len(d['volantini_arrivati']) + len(d['volantini_finiti'])
            + len(d['offerte_nuove']) + len(d['offerte_sparite'])
            + len(d['prezzi_cambiati']) + len(d['meno_caro_cambiato']))

def racconta(d, prima_giorno):
    print(f"da {prima_giorno} a {d['giorno']}:")
    print(f"  volantini arrivati  {len(d['volantini_arrivati'])}")
    print(f"  volantini finiti    {len(d['volantini_finiti'])}")
    print(f"  offerte nuove       {len(d['offerte_nuove'])}")
    print(f"  offerte sparite     {len(d['offerte_sparite'])}")
    print(f"  prezzi cambiati     {len(d['prezzi_cambiati'])}")
    if d['cambiati_reparto']:
        print(f"  cambiati di reparto {len(d['cambiati_reparto'])}")
    for c in d['meno_caro_cambiato']:
        print(f"  \u2192 il {c['cat'].lower()} pi\u00f9 conveniente adesso \u00e8 "
              f"{c['pro']} ({c['ins']}), {c['unitario']:.2f} {c['unita']}")


if __name__ == '__main__':
    solo_guardare = '--guarda' in sys.argv
    os.makedirs(DOVE, exist_ok=True)
    adesso = fotografia()
    prima = json.load(open(FOTO, encoding='utf-8')) if os.path.exists(FOTO) else {}

    if not prima:
        # Nessuna fotografia: siamo in un clone pulito, com'è ogni sessione
        # nuova. Non è un motivo per buttare via il giorno: la fotografia si
        # rifà dall'ultimo commit che ha toccato i prezzi.
        commit = commit_di_dati()
        if commit:
            sigla, data = commit[0]
            print(f'nessuna fotografia: la rifaccio da git, commit {sigla[:7]} del {data}')
            prima = fotografia_da_commit(sigla, data) or {}

    if not prima:
        print('prima fotografia: da domani ci sar\u00e0 qualcosa da confrontare.')
        if not solo_guardare:
            json.dump(adesso, open(FOTO, 'w', encoding='utf-8'), ensure_ascii=False)
            print(f"segnate {len(adesso['offerte'])} offerte e "
                  f"{len(adesso['volantini'])} volantini in storia/stato.json")
        raise SystemExit

    if prima.get('giorno') == adesso['giorno']:
        # La fotografia è già di oggi: è il SECONDO giro della stessa giornata.
        # Confrontarsi con se stessi svuota il giorno. Il 2026-09-16 è successo
        # davvero: il giro delle 8 aveva lanciato `storia` una volta, poi aveva
        # aggiunto altre righe a `dati.py` e l'aveva rilanciato, e il file di
        # quel giorno era rimasto con le ultime cinque righe invece che con
        # tutta la giornata. Il paragone giusto è sempre l'ultimo giorno
        # PUBBLICATO, e quello sta in git: così rilanciarlo dieci volte di fila
        # riscrive dieci volte lo stesso giorno, intero.
        indietro = next(((s, g) for s, g in commit_di_dati()
                         if g < adesso['giorno']), None)
        if indietro:
            print(f'la fotografia è già di oggi: riprendo il paragone da '
                  f'{indietro[0][:7]} del {indietro[1]}')
            prima = fotografia_da_commit(*indietro) or prima

    # I giorni rimasti indietro, uno per uno e con la loro data. Se in mezzo
    # c'è stato un commit sui prezzi si riprende quello: è così che si
    # recuperano i giorni persi quando la fotografia non è arrivata.
    storici = commit_di_dati()
    fatte = {}
    tappe = []
    for g in giorni_fra(prima['giorno'], adesso['giorno']):
        sigla = next((s for s, data in storici if data <= g), None)
        if sigla and sigla not in fatte:
            fatte[sigla] = fotografia_da_commit(sigla, g)
        f = fatte.get(sigla)
        tappe.append(dict(f, giorno=g) if f else dict(prima, giorno=g))
    tappe.append(adesso)

    scritti = 0
    for tappa in tappe:
        d = differenza(prima, tappa)
        racconta(d, prima['giorno'])
        if not solo_guardare and quanto(d):
            json.dump(d, open(os.path.join(DOVE, f"{d['giorno']}.json"), 'w',
                              encoding='utf-8'), ensure_ascii=False)
            print(f"  scritto storia/{d['giorno']}.json")
            scritti += 1
        elif not quanto(d):
            print('  niente di nuovo: nessun file scritto.')
        prima = tappa

    if not solo_guardare:
        json.dump(adesso, open(FOTO, 'w', encoding='utf-8'), ensure_ascii=False)
        if scritti > 1:
            print(f'{scritti} giorni scritti in una volta: erano rimasti indietro.')
