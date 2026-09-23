# -*- coding: utf-8 -*-
"""Genera la pagina web da pubblicare.

Prodotti e prezzi da dati.py, lista di partenza da lista.py.

Due scelte volute, chieste da Manlio il 2026-09-02 dopo aver provato la
prima versione:

1. TEMA CHIARO FISSO. Niente blocco `prefers-color-scheme: dark`: il suo
   telefono è in modalità notte e la pagina gli si apriva nera («così non
   si può vedere»). Sfondo bianco dichiarato esplicitamente, così tiene
   anche se chi ospita la pagina è scuro.
2. BOTTONI IN CIMA. I prodotti sono bottoni in testa alla pagina; toccarne
   uno riempie la lista qui sotto, già ordinata dal meno caro. Prima erano
   schede da aprire e chiudere una per una, e per arrivare al tonno
   toccava scorrere.

La lista vive in localStorage, non sul server: vedi NOTE.md.
"""
import json, os, re
from dati import OFFERTE, VOLANTINI, UNITA, D
from catalogo import CATALOGO, REPARTI, RINOMINATE
from lista import PARTENZA
from look import LOOK, verifica as verifica_look
from loghi import LOGHI, chiave as chiave_logo

# I look non si pubblicano senza essere stati misurati: `verifica` si ferma con
# un errore se in uno di essi il testo non stacca abbastanza dallo sfondo.
verifica_look()

PDF     = {v.chiave: v.pdf for v in VOLANTINI}
MODELLO = {v.chiave: v.indirizzo for v in VOLANTINI}
ELENCO  = {v.chiave: v.pagine for v in VOLANTINI if v.pagine}

def indirizzo(chiave, n):
    """L'indirizzo pubblico di una pagina del volantino, per renderla cliccabile.
    Senza numero di pagina non c'e niente da aprire: torna None e la riga resta
    scritta e basta.

    Due forme, non una: quasi tutti i volantini hanno un indirizzo a schema col
    numero dentro; Mercato ha invece l'elenco delle pagine, una per una, perche
    la sua fonte le firma e il numero da solo non basta (vedi pagine_mercato)."""
    if not n:
        return None
    if chiave in ELENCO:
        elenco = ELENCO[chiave]
        return elenco[n - 1] if 1 <= n <= len(elenco) else None
    if chiave not in MODELLO or not MODELLO[chiave]:
        return None
    return MODELLO[chiave].format(n=n)
PERIODO = {v.chiave: v.periodo for v in VOLANTINI}

import datetime as _dt
_oggi = _dt.date.today()

# SCADUTO E «NON ANCORA COMINCIATO» LI DECIDE LA PAGINA, NON QUESTO PROGRAMMA.
# Qui si scrivono solo le due date; il confronto con oggi lo fa il browser di
# chi apre. Se lo facessimo qui, il giudizio resterebbe congelato al giorno in
# cui la pagina e stata generata: il 7 settembre avrebbe continuato a dare per
# buone offerte scadute il 6, finche qualcuno non rigenerava. E chi rigenera,
# per ora, non e affidabile — vedi il controllo giornaliero.

INIZIO = {v.chiave: v.inizio for v in VOLANTINI}
FINO   = {v.chiave: v.fino for v in VOLANTINI}

# LO SCONTO IN PERCENTUALE (Manlio, 2026-09-23: «in molti prodotti c'è
# scritto che sconto hanno: questa cifra in percentuale andrebbe messa fra il
# cerchietto dei giorni e l'icona del volantino»). Si legge dalla nota, che
# riporta quello che stampa il volantino:
#   1. se il volantino stampa la percentuale («−30%, prima 3,29», «Sconto del
#      30%: …», «Sconto soci del 40%»), vale quella, così com'è;
#   2. se stampa solo il prezzo di prima («Prima 2,99»), la si calcola, ma solo
#      quando il conto è sicuro: il «prima» dev'essere il prezzo della STESSA
#      confezione, non quello al kg o all'etto («… al kg, prima 1,50»), e non
#      su una riga «1+1», dove il prezzo scritto e il «prima» possono
#      riferirsi a quantità diverse;
#   3. altrimenti niente: meglio nessun bollino che uno sbagliato.
# «Senza tessera 4,99» NON è uno sconto stampato: non si trasforma in uno.
_PCT = [re.compile(r'^\s*[−–-]\s?(\d{1,2})\s?%'),
        re.compile(r'[Ss]conto(?: soci)?(?: del)? (\d{1,2})\s?%'),
        re.compile(r'(?<![\d,])[−–]\s?(\d{1,2})\s?%')]
_PRIMA = re.compile(r'\b[Pp]rima (\d+,\d{2})(?!\s*(?:€\s*)?(?:al|all|a |per|l\'))')
_UNITA_PRIMA = re.compile(r'(?:al|all[\'’]|a)\s*(?:kg|chilo|litro|l|etto|pezzo|lavaggio|rotolo)\s*,?\s*$')

def sconto(prezzo, fmt, note):
    n = note or ''
    for rx in _PCT:
        m = rx.search(n)
        if m:
            v = int(m.group(1))
            return v if 5 <= v <= 90 else None
    m = _PRIMA.search(n)
    if not m or _UNITA_PRIMA.search(n[:m.start()]):
        return None
    if re.search(r'\d\s*\+\s*\d', fmt or ''):
        return None
    prima = float(m.group(1).replace(',', '.'))
    if prima <= prezzo:
        return None
    v = round((1 - prezzo / prima) * 100)
    return v if 5 <= v <= 80 else None

def prima(note):
    m = _PRIMA.search(note or '')
    return m.group(1) if m else ''

# LE NOTE DIVENTANO BOLLINI BREVI (Manlio, 2026-09-23, punto 2 della critica
# esterna: «le note gialle diventano bollini brevi, e tolgo i numeri
# ripetuti»). Prima ogni scheda aveva sotto un riquadro ambra lungo due o tre
# righe. Adesso le CONDIZIONI (tessera, app, al banco, surgelato, 1+1, non in
# tutti i negozi) sono bollini di una o due parole, sotto il nome, e il resto
# della nota NON SI MOSTRA (Manlio, lo stesso giorno: «toglierei del tutto la
# scritta dettagli e ciò che fa apparire: molto spesso sono di troppo e sono
# davvero dei dettagli»). La nota intera resta nei dati: «Cerca» cerca anche
# lì dentro, ed è da lì che nascono i bollini e lo sconto.
_TESSERA = re.compile(r"Lidl Plus|Buona Spesa Card|Carta Insieme|[Ss]olo titolari|"
                      r"EKOM UP|SpesAmica|\bsoci\b|CARTA BENNET|Fidelity Card|"
                      r"Perte Plus|\bcon APP\b|\bl'app\b|[Tt]essera")
_BOLLO_TESSERA = {'Pam': 'Solo con app', 'Lidl': 'Con Lidl Plus', 'Ipercoop': 'Solo soci'}

def condizioni(ins, cat, fmt, note):
    n = note or ''
    bolli = []
    if _TESSERA.search(n):
        bolli.append(_BOLLO_TESSERA.get(ins, 'Con tessera'))
    if re.search(r'\b[Aa]l banco\b|banco servito|banco taglio', n + ' ' + (fmt or '')):
        bolli.append('Al banco')
    if (re.search(r'\b[Ss]urgelat', n) and not re.search(r'non surgelat', n)
            and 'surgel' not in cat.lower()):
        bolli.append('Surgelato')
    m = re.search(r'(\d)\s*\+\s*(\d)', fmt or '') or re.search(r'\b(\d)\s*\+\s*(\d)\b', n)
    if m:
        bolli.append(f'{m.group(1)}+{m.group(2)}')
    elif re.search(r'[Cc]omprando|[Pp]iù compri|[Dd]al (?:secondo|terzo|quarto) pezzo', n):
        bolli.append('Più ne prendi')
    if re.search(r'Solo nei punti vendita|Vale solo nei negozi', n):
        bolli.append('Non in tutti i negozi')
    return bolli

# LE COSE DAVVERO IMPORTANTI DEI VECCHI «DETTAGLI», IN UNA PILLOLA BEIGE IN
# PIÙ (Manlio, 2026-09-23: «se quello che c'è scritto in questi dettagli è
# davvero importante e soprattutto breve, lo si può fare apparire in
# un'altra pillola beige accanto a quella che già c'è»). Solo tre tipi di
# cose, e solo se stanno in poche parole (NON il prezzo all'etto dei banchi:
# è il prezzo al kg diviso per dieci, un numero ripetuto):
#   - quanto costa SENZA la tessera («Senza tessera 3,49 €»);
#   - COS'È DAVVERO il prodotto, quando la nota lo dice («È burrata, non
#     mozzarella» → «Burrata»; «Sono capsule: …» → «Capsule»), purché non sia
#     già scritto nel nome;
#   - il PESO: sgocciolato, o no («Peso non sgocciolato» sul tonno col conto
#     sul peso della scatola), e il prezzo di una confezione sola nei 1+1.
# Tutto il resto dei dettagli resta fuori, come ha chiesto.
_MAX_BREVE = 26
_COSE = re.compile(r"^(?:È|Sono) (?:(?:un|una|uno|il|la|lo|l'|i|le|gli) )?(.+?)(?=[,:;(]|\.$| non |$)")

def _gia_nel_nome(cosa, pro):
    # «Fresche» su «Pasta fresca», «Birra al 10%» su «Birra Faxe 10%»: ogni
    # parola che conta (i primi cinque caratteri) è già nel nome.
    nome = (pro or '').lower()
    parole = [w[:5] for w in re.findall(r"[\wà-ù%]+", cosa.lower()) if len(w) >= 3 and w not in ('con', 'per', 'non')]
    return all(w in nome for w in parole)

def brevi(pro, note):
    n = note or ''
    out = []
    # L'unità si porta dietro: «senza tessera 25,90 al kg» scritto «25,90 €»
    # si leggerebbe come il prezzo della confezione.
    m = re.search(r"[Ss]enza tessera (\d+(?:,\d+)?)( (?:al kg|al litro|all'etto|al pezzo))?", n)
    if m:
        out.append(f'Senza tessera {m.group(1)} €' + (m.group(2) or ''))
    for f in re.split(r'(?<=\.)\s+(?=[A-ZÈÉ«−–\d])', n.strip()):
        m = _COSE.match(f)
        if m and not re.match(r'\d\s*\+\s*\d', m.group(1)):
            cosa = m.group(1).strip()
            cosa = cosa[:1].upper() + cosa[1:]
            if len(cosa) <= _MAX_BREVE and not _gia_nel_nome(cosa, pro) and not cosa.lower().startswith('banco'):
                out.append(cosa)
            break
        m = re.match(r'^(Già cott[eoia]|Precott[eoia]|Panat[oaie]|Impanat[oaie])\b', f)
        if m:
            out.append(m.group(1))
            break
    if re.search(r'sgocciolato non è stampato|sgocciolato il tonno è meno', n):
        out.append('Peso non sgocciolato')
    elif re.search(r'sgocciolat', n):
        out.append('Peso sgocciolato')
    m = re.search(r'Una confezione sola costa (\d+(?:,\d+)?)', n)
    if m:
        out.append(f'Una sola {m.group(1)} €')
    if re.search(r'[Qq]uantità limitata|Offerta limitata', n):
        out.append('Quantità limitata')
    return out

# Le date di un'offerta sono quelle del suo volantino, a meno che l'offerta ne
# abbia di sue e più strette: allora comandano quelle, e la riga viene marcata
# «ristretta» — la pagina la mostra soltanto nei giorni in cui vale davvero.
offerte = [dict(cat=o.cat, ins=o.ins, rep=o.rep, pro=o.pro, fmt=o.fmt, prezzo=o.prezzo,
                unitario=round(o.prezzo / o.qta, 3), pag=o.pag, pdf=PDF[o.chiave],
                url=indirizzo(o.chiave, o.pag),
                periodo=PERIODO[o.chiave], dubbio=(o.fonte == D), note=o.note,
                sconto=sconto(o.prezzo, o.fmt, o.note), prima=prima(o.note),
                bolli=condizioni(o.ins, o.cat, o.fmt, o.note) + brevi(o.pro, o.note),
                inizio=o.inizio or INIZIO[o.chiave],
                fino=o.fino or FINO[o.chiave],
                ristretta=bool(o.inizio or o.fino))
           for o in OFFERTE]

# indice.json sta nel progetto, non nella cartella di lavoro: le immagini dei
# volantini non si tengono (non sono nostre) e prima l'elenco delle pagine
# veniva filtrato guardando i file jpg sul disco. Risultato: chi rigenerava la
# pagina senza aver riscaricato tutto si ritrovava zero pagine. L'indice
# contiene già solo pagine esistite davvero: basta lui.
QUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ind = 'indice.json' if os.path.exists('indice.json') else os.path.join(QUI, 'indice.json')
idx = json.load(open(_ind, encoding='utf-8'))
idx = [r for r in idx if r['chiave'] in PDF]      # via i volantini tolti da dati.py
if not idx:
    raise SystemExit('indice.json vuoto o senza volantini noti: fermati.')
pagine = sorted((dict(ins=r['insegna'], periodo=r['validita'], pdf=PDF.get(r['chiave'], ''),
                      pag=r['pagina'], parole=r['parole'],
                      url=indirizzo(r['chiave'], r['pagina']))
                 for r in idx),
                key=lambda r: (r['ins'], r['periodo'], r['pag']))

MESI = ('gennaio febbraio marzo aprile maggio giugno luglio agosto '
        'settembre ottobre novembre dicembre').split()
# La data in fondo alla pagina si calcola: scritta a mano era rimasta indietro
# di due giorni e Manlio l'ha fotografata mentre si contraddiceva da sola.
OGGI = f'{_oggi.day} {MESI[_oggi.month - 1]} {_oggi.year}'
# Il primo indirizzo utile di ogni volantino: e quello che apre il tasto «Il
# volantino» in fondo alla pagina. Si prende dall'indice, cioe da pagine che
# esistono davvero, e non dal modello con dentro il numero: cosi il tasto non
# porta mai su un indirizzo inventato.
PRIMA = {}
for _r in pagine:
    if _r['url'] and _r['pdf'] not in PRIMA:
        PRIMA[_r['pdf']] = _r['url']

volantini = [x for x in (dict(ins=v.insegna, periodo=v.periodo, pdf=v.pdf,
                              pagine=len([y for y in pagine if y['pdf'] == v.pdf]),
                              apri=PRIMA.get(v.pdf),
                              inizio=v.inizio, fino=v.fino)
                         for v in VOLANTINI) if x['pagine']]

partenza = [dict(nome=n, parole=p, cat=c) for n, p, c in PARTENZA]

# LA LISTA CHE COMANDA E QUELLA CHE HANNO LORO.
# Manlio e la moglie aggiungono e tolgono prodotti dalla pagina pubblicata. Se
# l'aggiornamento settimanale dei volantini ripartisse da PARTENZA, gliela
# cancellerebbe tutta a ogni giro. Quindi: prima di rigenerare, si legge la
# lista dalla pagina viva (lista_attuale.py la tira fuori e la scrive qui) e si
# riparte da quella. PARTENZA serve solo se il file non c'e, cioe la prima volta.
lista_viva = 'lista-attuale.json'
if os.path.exists(lista_viva):
    salvata = json.load(open(lista_viva, encoding='utf-8'))
    if isinstance(salvata, list) and salvata:
        partenza = salvata
        print(f'lista ripresa dalla pagina viva: {len(partenza)} prodotti')

# Il catalogo va nella pagina perché è quello che si vede nel cassetto: nome,
# reparto e parole con cui il volantino chiama la stessa cosa. Sono ~66 voci,
# meno di 6 KB: non è quello che pesa.
catalogo = [dict(nome=v['nome'], rep=v['reparto'], parole=v['parole']) for v in CATALOGO]

# LE NOVITÀ DELLA PAGINA — non dei prezzi.
# Chiesto da Manlio il 2026-09-18: «la prima volta che uno apre la pagina
# sarebbe carino che ci fosse una finestra novità, a partire dalla casella di
# ricerca; le novità sono nell'interfaccia e nelle possibilità, non nei
# prodotti». Le novità dei PREZZI hanno gia il loro posto: il tasto «Novità»
# in alto a destra, che porta al diario. Qui dentro non ci vanno prezzi, ne
# offerte, ne nomi di prodotto: solo cosa si puo fare adesso che prima non si
# poteva.
#
# In ordine di tempo, dalla piu vecchia: si legge come una storia di cosa e
# arrivato. Aggiungendone una nuova si mette IN FONDO, con la sua data: chi ha
# gia visto le altre si vede comparire solo quella (il confronto e sull'id
# dell'ultima vista, tenuto nel browser di chi guarda).
NOVITA_PAGINA = [
    dict(id='2026-09-15-cerca', quando='15 settembre',
         titolo='«Cerca fra i prezzi»',
         testo='Il tasto rosso sotto i prodotti apre una casella che cerca fra '
               'TUTTE le offerte lette, non nel catalogo: scrivi una marca, un '
               'formato o il nome di un negozio e trovi quella singola offerta. '
               'È un\'altra cosa dalla casella dentro «+ altri prodotti», che '
               'invece accende i prodotti della lista.'),
    dict(id='2026-09-18-ekom', quando='18 settembre',
         titolo='Un supermercato in più: l\'Ekom',
         testo='I volantini letti adesso sono otto insegne invece di sette. '
               'Non devi fare niente: le offerte dell\'Ekom entrano da sole nel '
               'confronto di ogni prodotto che hai acceso.'),
    dict(id='2026-09-18-tasti', quando='18 settembre',
         titolo='Due tasti su ogni volantino',
         testo='In fondo alla pagina, nell\'elenco dei volantini, ogni riga ha '
               'due tasti: «Le offerte» ti mostra i prezzi letti da quel '
               'volantino, reparto per reparto, e «Il volantino» apre le sue '
               'pagine sul sito di chi lo pubblica. Tutti e due si aprono in '
               'una pagina nuova, così non perdi quello che stavi guardando.'),
    dict(id='2026-09-21-aiuto', quando='21 settembre',
         titolo='Il tasto «Aiuto»',
         testo='In cima, accanto a «Novità», c\'è un tasto «Aiuto»: apre una '
               'finestra che spiega in poche righe come funziona la pagina. '
               'Non si apre mai da sola, e la puoi riaprire tutte le volte che '
               'vuoi.'),
    dict(id='2026-09-22-look', quando='22 settembre',
         titolo='Il tasto «Look»: cento vestiti per la pagina',
         testo='In cima c\'è un tasto «Look»: apre un elenco di cento '
               'combinazioni di colori, divise per famiglia (neutri, '
               'tranquilli, vivaci, stagionali...). Ne tocchi una e la pagina '
               'si ricolora subito, comprese quelle scure per la sera. La '
               'scelta se la ricorda il telefono, e con «Originale» torni '
               'com\'era. Cambiano solo i colori: le offerte e la tua lista '
               'restano quelle.'),
    dict(id='2026-09-22-meno-caro', quando='22 settembre',
         titolo='Il meno caro si vede da lontano',
         testo='Nell\'elenco dei prezzi, l\'offerta meno cara che puoi '
               'comprare oggi adesso sta dentro una pastiglia con il bordo '
               'verde, staccata dalle altre. E le offerte che devono ancora '
               'cominciare sono sbiadite: si leggono, ma si vede subito che '
               'oggi non valgono.'),
    dict(id='2026-09-23-impaginazione', quando='22 settembre',
         titolo='La pagina è rifatta: tutto in schede e pillole',
         testo='In cima il titolo «Spesa» e il tasto rosso per cercare fra '
               'tutte le offerte. Ogni offerta '
               'adesso è una scheda tutta sua, con in alto il marchio del '
               'negozio, il prodotto, il formato, le condizioni in un '
               'riquadro giallo e a destra i due prezzi: quello della '
               'confezione e quello per unità. Quella meno cara che puoi '
               'comprare oggi ha il bordo verde. In fondo a ogni scheda, '
               '«Vedi tutte le offerte del volantino».'),
    dict(id='2026-09-22-giorni', quando='22 settembre',
         titolo='Quanti giorni restano, su ogni offerta',
         testo='Accanto a ogni offerta c\'è un cerchietto con dentro un '
               'numero: sono i giorni che restano per comprarla, oggi '
               'compreso. L\'anello si consuma man mano che il volantino '
               'scade, e negli ultimi tre giorni diventa arancione. «1 oggi» '
               'vuol dire che oggi è l\'ultimo giorno. La scritta lunga «apri '
               'la pagina del volantino» è diventata un bottoncino col '
               'foglietto e il numero della pagina, così ogni offerta occupa '
               'meno schermo. Le offerte che devono ancora cominciare, invece '
               'del cerchietto, hanno un tondino col giorno in cui partono e '
               'il mese sotto, e il prezzo scritto in grigio: si vede subito '
               'che oggi non valgono. E in cima ho tolto «Torino · corso '
               'Siracusa» e il bollino accanto: erano le uniche cose lassù '
               'che non servivano a fare niente.'),
    # L'id e «2026-09-23-...» e non «-22-»: le novita si segnano per id PIU
    # GRANDE, e «2026-09-23-impaginazione» c'e gia. Con «-22-» questa non
    # comparirebbe mai a chi ha gia visto quella.
    dict(id='2026-09-23-pallini', quando='22 settembre',
         titolo='Due pallini in alto, le grandi marche, il Pam',
         testo='In alto a destra, accanto al titolo, ci sono due pallini: '
               'l\'ingranaggio apre la configurazione (colori, supermercati, '
               'aiuto), quello con la N apre le novità dei volantini. Accanto '
               'al tasto rosso c\'è «GRANDI MARCHE»: tocchi un marchio e la '
               'pagina scende da sola alle sue offerte. E fra i negozi adesso '
               'ci sono anche il Pam e il Conad.'),
    dict(id='2026-09-23-supermercati', quando='22 settembre',
         titolo='Scegli i tuoi supermercati',
         testo='Tocca l\'ingranaggio in alto a destra: c\'è l\'elenco di tutti '
               'i supermercati. Toccandone uno lo togli o lo rimetti, e quelli '
               'tolti spariscono dai prezzi, dalla ricerca e dalle grandi '
               'marche. La scelta resta sul tuo telefono. Lì dentro ci sono '
               'anche i colori della pagina e l\'aiuto.'),
    dict(id='2026-09-23-tretasti', quando='23 settembre',
         titolo='Tre tasti, tre parti della pagina',
         testo='In alto ci sono «Prodotti», «Cerca» e «Grandi marche», e restano '
               'lì anche quando scorri. Quello rosso è la parte in cui sei. Per '
               'tornare ai tuoi prodotti da qualunque punto basta toccare '
               '«Prodotti».'),
    # «u» dopo «tretasti»: le novità si segnano per id più grande.
    dict(id='2026-09-23-u-personale', quando='23 settembre',
         titolo='La tua sezione: «Personale»',
         testo='Il quarto tasto in alto. Scrivi un prodotto o una marca e tocca '
               '«Aggiungi»: diventa una pillola, e sotto trovi la sua offerta più '
               'conveniente, con un tasto per vederle tutte. Con «Personalizza '
               'supermercati» scegli dove cercare, solo per questa sezione. Le '
               'parole restano sul tuo telefono: ognuno ha le sue.'),
    # «v» dopo «u-personale»: le novità si segnano per id più grande.
    dict(id='2026-09-23-v-categorie', quando='23 settembre',
         titolo='Categorie più pulite',
         testo='Würstel, hamburger, polpette, cotolette e nuggets non stanno più '
               'insieme alla carne fresca: hanno le categorie «Würstel» e '
               '«Preparati». Così il meno caro di Suino, Manzo e Pollo è davvero '
               'carne. Nuove anche «Affettati», «Salmone affumicato», '
               '«Collutorio» e «Panati» (i bastoncini e il pesce impanato). Se ti '
               'servono, le accendi da «+ altri prodotti».'),
    dict(id='2026-09-23-w-bollini', quando='23 settembre',
         titolo='Schede più corte',
         testo='Le note gialle lunghe sono diventate bollini brevi sotto il nome: '
               '«Con tessera», «Solo con app», «Al banco», «Surgelato», «1+1». '
               'Tolti anche i numeri '
               'scritti due volte: il prezzo della confezione sta solo a destra. '
               'Così in una schermata ci stanno più offerte.'),
    dict(id='2026-09-23-x-formato', quando='23 settembre',
         titolo='Via la riga «Formato… fino al…»',
         testo='Sotto il nome non c\'è più «Formato: … · fino al …»: quando scade '
               'lo dice il cerchietto dei giorni, «al kg» lo dice il prezzo grande. '
               'Il peso della confezione adesso sta accanto al suo prezzo, dove '
               'prima c\'era scritto «al pezzo».'),
    dict(id='2026-09-23-y-volantino', quando='23 settembre',
         titolo='Tocca un\'offerta e vedi il volantino',
         testo='Tocca un punto qualunque di una scheda: la pagina del volantino dove '
               'sta quell\'offerta si apre sopra l\'elenco. Per tornare ai prezzi '
               'c\'è il tasto grande «Chiudi» in basso (va bene anche il tasto '
               '«indietro» del telefono). In alto, «Apri sul sito» la apre sul '
               'sito del negozio. Tolto anche «Dettagli»: quello che contava davvero '
               'è diventato una pillola beige in più (il prezzo senza tessera, il '
               'peso sgocciolato, cos\'è davvero il prodotto).'),
    dict(id='2026-09-23-z-sintesi', quando='23 settembre',
         titolo='In cima: dove conviene',
         testo='Quando serve, in cima alle offerte di un prodotto c\'è una riga in '
               'più: in verde il meno caro che si compra oggi, quando sopra ci sono '
               'tre o più offerte che partono nei prossimi giorni; in blu l\'offerta '
               'che costerà meno fra qualche giorno, e da quando. Toccala e la '
               'pagina scende a quella scheda. Quando il meno caro di oggi è fra le '
               'prime tre schede, la riga non c\'è.'),
    dict(id='2026-09-23-zz-colori', quando='23 settembre',
         titolo='Calendarietto, N ed «Elimina»',
         testo='Le offerte che devono ancora cominciare hanno un calendarietto col '
               'giorno in cui partono, invece del tondino: così non si confonde col '
               'cerchietto dei giorni che mancano. La N in alto a destra non è più '
               'rossa. «Elimina prodotto» non sta più accanto al nome: lo trovi '
               'toccando la «i», vicino a «Cambia nome».'),
    dict(id='2026-09-23-zzz-menu', quando='23 settembre',
         titolo='Il menù in basso',
         testo='I quattro tasti Prodotti, Cerca, Grandi marche e Personale adesso '
               'stanno in fondo allo schermo, sempre a portata di pollice, ognuno con '
               'la sua icona. Quello rosso è la parte in cui sei. In cima resta più '
               'spazio per i tuoi prodotti.'),
    dict(id='2026-09-23-zzzz-prezzi', quando='23 settembre',
         titolo='I prezzi a destra',
         testo='Sulle schede il prezzo sta a destra, su due righe: sopra quello al '
               'chilo (o al litro), sotto quanto costa la confezione e quanto pesa. '
               'A sinistra restano il nome e i bollini. Tolti il foglietto rosso del '
               'volantino (basta toccare la scheda), il simbolo dell\'euro e la '
               'scritta «prezzo al kg» accanto al nome del prodotto.'),
]

# LE QUARANTA GRANDI MARCHE (erano venti; «pensandoci bene sono almeno 40»). Chiesto da Manlio il 2026-09-22: «un tasto GRANDI
# MARCHE tutto maiuscolo che porta a una scelta fra 20 pillole delle grandi
# marche italiane più famose; toccandone una si fa una ricerca per nome che dà
# solo i prodotti di quella marca». Scelte fra le marche italiane che nei
# volantini letti compaiono davvero (almeno due offerte ciascuna quando sono
# state scelte): una pillola che non trova niente sarebbe una presa in giro.
# LE MARCHE SENZA OFFERTE NON SI TOLGONO: SI SPENGONO (Manlio, 2026-09-22:
# «metti anche Ferrero e quelle che non appaiono, facendo i pulsanti
# disattivati e di un colore molto piu tenue»). La pillola spenta la decide
# il TELEFONO di chi guarda, ogni volta che apre il pannello, con la sua data:
# un volantino che scade la spegne da sola, uno nuovo che la contiene la
# riaccende da solo al primo aggiornamento. Niente da ricordarsi a mano.
# «Fini» e «Moretti» provate e scartate: «Fini» trovava i «piselli fini», e
# «Moretti» era un tonno, non la birra. Una pillola deve dare quello che dice.
# Si cercano a PAROLA INTERA: «AIA» cercata come pezzo di parola trovava anche
# il «maiale».
GRANDI_MARCHE = [
    # pasta, dolci e colazione
    'Ferrero', 'Mulino Bianco', 'Barilla', 'De Cecco', 'Voiello', 'Rummo', 'Garofalo', 'La Molisana',
    'Rana', 'Saiwa', 'Pavesi', 'Balocco', 'Loacker', 'Colussi', 'Bauli', 'Melegatti', 'Kinder',
    'Novi', 'Zuegg', 'Lavazza', 'Kimbo', 'Vergnano',
    # latte, formaggi, carne e salumi
    'Granarolo', 'Parmalat', 'Arborea', 'Galbani', 'Vallelata', 'AIA',
    'Amadori', 'Beretta', 'Citterio', 'Parmacotto',
    # dispensa e surgelati
    'Rio Mare', 'Orogel', 'Sammontana', 'Star', 'Cirio', 'Mutti',
    # bevande
    "Sant'Anna", 'San Benedetto', 'Levissima', 'Peroni', 'Ichnusa', 'Menabrea',
    # casa e igiene
    'Felce Azzurra', 'Omino Bianco']

# I MARCHI DELLE GRANDI MARCHE, uno per file in strumenti/marchi/ (chiesti il
# 2026-09-22: «trova anche i marchi delle grandi marche e usali al posto dei
# bottoni»). Come per i supermercati: per aggiungerne uno basta mettere il
# file li, col nome della marca in minuscolo e i trattini al posto di spazi e
# apostrofi; se manca, la pillola resta col nome scritto. Diventano immagini
# scritte dentro la pagina, cosi la pagina resta un file solo.
def _chiave_marca(m):
    import unicodedata
    s = ''.join(c for c in unicodedata.normalize('NFD', m.lower())
                if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def _marchi_marche():
    import base64
    dove = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'marchi')
    tipi = {'webp': 'image/webp', 'png': 'image/png', 'svg': 'image/svg+xml'}
    fuori = {}
    for m in GRANDI_MARCHE:
        for est, tipo in tipi.items():
            f = os.path.join(dove, _chiave_marca(m) + '.' + est)
            if os.path.exists(f):
                fuori[m] = 'data:%s;base64,%s' % (tipo, base64.b64encode(open(f, 'rb').read()).decode())
                break
    return fuori

DATI = json.dumps(dict(offerte=offerte, pagine=pagine, volantini=volantini,
                       catalogo=catalogo,
                       # I nomi vecchi delle categorie, per chi ha una lista
                       # salvata da prima che li accorciassimo: vedi catalogo.py.
                       rinominate=RINOMINATE,
                       marche=GRANDI_MARCHE,
                       marchiMarche=_marchi_marche(),
                       reparti=[r for r, _ in REPARTI],
                       unita={k: v[0] for k, v in UNITA.items()},
                       novita=NOVITA_PAGINA,
                       # I marchi delle insegne, quelli veri, uno per chiave.
                       # Chi non ce l'ha resta con la pillola scritta.
                       loghi={i: LOGHI[chiave_logo(i)] for i in sorted({o['ins'] for o in offerte})
                              if chiave_logo(i) in LOGHI},
                       look=[dict(id=l['id'], nome=l['nome'], fam=l['fam'],
                                  base=l['base'], notte=l['notte'], v=l['v'])
                             for l in LOOK],
                       letto=OGGI),
                  ensure_ascii=False, separators=(',', ':'))
LISTA0 = json.dumps(partenza, ensure_ascii=False, separators=(',', ':'))

HTML = r'''<title>Spesa</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Asap:wght@400;500;600;700&family=Oswald:wght@500;600;700&display=swap">
<style>
/* Tema chiaro unico e dichiarato: nessun blocco scuro, perché la pagina
   si apriva nera sul telefono di Manlio in modalità notte. */
:root{
  --carta:#FFFFFF;
  --pannello:#F6F5F2;
  --inchiostro:#1B1B1A;
  --tenue:#6E6C66;
  --linea:#E5E3DD;
  --linea-forte:#CFCCC4;
  --rosso:#D40D2B;
  --su-rosso:#FFFFFF;
  --verde:#1E7A4B;
  --verde-tenue:#E6F3EC;
  --ambra:#8A5A08;
  --ambra-tenue:#FCF2DE;
  /* Servono al tasto «Look»: erano scritti a mano dentro le regole e un look
     nuovo non poteva cambiarli. Qui i valori sono quelli di sempre. */
  --rosso-tenue:#FBEEF0;
  --blu:#2B4A7A;
  --blu-tenue:#E9EEF6;
  --f-testo:'Asap',ui-sans-serif,system-ui,'Segoe UI',sans-serif;
  --f-prezzo:'Oswald','Arial Narrow',ui-sans-serif,sans-serif;
  /* La lente del tasto rosso, disegnata qui dentro: nessun carattere
     speciale, che sui telefoni diventa un quadratino. */
  --ingranaggio:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='3'/%3E%3Cpath d='M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z'/%3E%3C/svg%3E");
  --lente:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.4' stroke-linecap='round'%3E%3Ccircle cx='11' cy='11' r='7'/%3E%3Cpath d='M16.5 16.5 21 21'/%3E%3C/svg%3E");
  color-scheme:light;
}
*{box-sizing:border-box}
html{background:var(--carta)}
body{background:var(--carta);color:var(--inchiostro);font-family:var(--f-testo);
  font-size:16px;line-height:1.45;-webkit-text-size-adjust:100%}
button{font-family:var(--f-testo);color:inherit}
:focus-visible{outline:3px solid var(--rosso);outline-offset:2px}
.guscio{max-width:800px;margin:0 auto;padding:0 15px 60px}

/* ---- testa ---- */
/* L'IMPAGINAZIONE NUOVA, chiesta da Manlio il 2026-09-22 con una schermata
   alla mano: «l'impaginazione è più bella così, con tutto messo in pillole e
   ordinato». In cima il marchio della pagina, il titolo, il sottotitolo e i
   tasti. */
header{padding:18px 0 2px}
.riga-alta{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;
  flex-wrap:wrap;margin-bottom:12px}
.marca{display:flex;align-items:center;gap:11px;min-width:0;color:inherit;text-decoration:none}
.segno{flex:none;width:44px;height:44px;border-radius:13px;background:var(--rosso);
  color:var(--su-rosso);display:grid;place-items:center;font-family:var(--f-prezzo);
  font-size:25px;font-weight:700;line-height:1}
.nomi{min-width:0}
h1{font-family:var(--f-prezzo);font-weight:700;font-size:27px;letter-spacing:.01em;
  line-height:1.05;margin:0}
.sotto-marca{display:block;color:var(--tenue);font-size:13px;margin-top:2px}
/* LA RIGA «Data di riferimento: …» NON C'E PIU, tolta il 2026-09-22 su
   richiesta di Manlio, come «Torino · corso Siracusa» prima di lei: una riga
   in cima che occupa spazio e non si tocca per fare niente. La data del
   telefono continua a comandare quello che conta — cosa e scaduto, quanti
   giorni mancano, quale offerta si puo comprare oggi — solo non e piu scritta
   li in mezzo. */
/* Il tasto «Novità», in alto a destra. Punta all'INDIRIZZO COMPLETO e non a
   «./novita.html»: la copia di Claude non ha una cartella accanto a se, e un
   collegamento relativo di la porterebbe nel vuoto. Si apre in una finestra
   nuova cosi non si perde il posto nell'elenco dei prezzi. */
.novita{flex:none;display:inline-flex;align-items:center;gap:6px;
  background:var(--rosso);color:var(--su-rosso);text-decoration:none;
  border-radius:99px;padding:9px 15px;font-size:14px;font-weight:700;
  letter-spacing:.02em;min-height:40px;line-height:1;white-space:nowrap}
.novita::after{content:'\2197';font-weight:600}
/* «Aiuto», chiesto da Manlio il 2026-09-21: un pulsantino accanto a «Novità».
   Vuoto invece che rosso pieno: il rosso pieno, in questa pagina, vuol dire
   «premi qui adesso» (il tasto Novità e «Cerca fra i prezzi»), e l'aiuto non
   e una cosa da premere adesso — e li per quando serve. */
/* LA SCELTA DEL LOOK, chiesta da Manlio il 2026-09-22: cento combinazioni di
   colori, una riga per ognuna, con le sue tinte in vista. Si sceglie a occhio,
   non per nome: la striscia dei colori conta più della scritta. */
.look-riga{display:flex;align-items:center;gap:11px;width:100%;text-align:left;
  background:var(--carta);border:1.5px solid var(--linea);border-radius:14px;
  padding:9px 11px;margin-top:7px;cursor:pointer;font-family:inherit;
  color:var(--inchiostro);min-height:52px}
.look-riga[aria-pressed="true"]{border-color:var(--rosso);border-width:2px}
.look-riga .strisce{flex:none;display:flex;border-radius:8px;overflow:hidden;
  border:1px solid var(--linea-forte)}
.look-riga .strisce i{display:block;width:17px;height:30px}
.look-riga .come{flex:1;min-width:0}
.look-riga .come b{display:block;font-size:14.5px;font-weight:600;line-height:1.2}
.look-riga .come span{display:block;color:var(--tenue);font-size:12px;margin-top:2px}
.look-riga .scelto{flex:none;color:var(--rosso);font-weight:700;font-size:13px}
.gruppo-look{font-family:var(--f-prezzo);text-transform:uppercase;letter-spacing:.06em;
  font-size:12px;font-weight:600;color:var(--tenue);margin:18px 0 2px}

/* ---- barra dei prodotti ---- */
.riga-cerca{margin:8px 0 0}
.capo-prodotti{display:flex;align-items:baseline;justify-content:space-between;gap:10px;
  flex-wrap:wrap;margin:0 0 7px;font-family:var(--f-prezzo);text-transform:uppercase;
  letter-spacing:.07em;font-size:12px;font-weight:600;color:var(--tenue)}
.capo-prodotti .suggerimento{font-family:var(--f-testo);text-transform:none;
  letter-spacing:0;font-size:13px;font-weight:400}
.barra{position:sticky;top:0;z-index:20;background:var(--carta);
  padding:11px 0 9px;border-bottom:1.5px solid var(--linea);margin-top:13px}
/* LE PASTIGLIE DEI PRODOTTI SONO BASSE E STRETTE. Manlio, 2026-09-22: «i
   bottoni delle categorie tengono troppo posto, bisogna assolutamente
   rimpicciolirli». Erano alte 44 px con 15 px di scritta: due file di bottoni
   si mangiavano mezzo schermo del telefono prima ancora dei prezzi. Adesso
   34 px, che con un dito si prende lo stesso, e i nomi sono di una parola
   sola (vedi catalogo.py), quindi in una riga ce ne stanno il doppio. */
.tasti{display:flex;flex-wrap:wrap;gap:6px}
.tasto{background:var(--carta);border:1.5px solid var(--linea-forte);border-radius:99px;
  padding:6px 12px;font-size:14px;font-weight:600;cursor:pointer;line-height:1.1;
  min-height:34px;white-space:nowrap}
.tasto[aria-pressed="true"]{background:var(--rosso);border-color:var(--rosso);color:var(--su-rosso)}
.tasto.agg{border-style:dashed;color:var(--tenue);font-weight:500}
/* «Cerca fra i prezzi». Era un bottone tratteggiato come «+ altri prodotti» e
   Manlio non lo vedeva: «poco visibile, dovrebbe essere rosso». Rosso pieno
   come chiede lui, ma su UNA RIGA TUTTA SUA (flex-basis 100%) e non in mezzo
   alle pastiglie dei prodotti: li dentro il rosso pieno vuol dire «prodotto
   acceso», e un rosso pieno in fila con quelli si leggerebbe come una voce
   della lista accesa per sbaglio. Da solo, largo quanto lo schermo, il rosso
   torna a voler dire quello che deve: «premi qui». */
.tasto.trova{display:flex;align-items:center;justify-content:center;gap:8px;
  width:100%;background:var(--rosso);border-color:var(--rosso);color:var(--su-rosso);
  border-style:solid;border-radius:99px;font-weight:700;font-size:15px;min-height:42px}
.tasto.trova::before{content:'';flex:none;width:17px;height:17px;
  background:currentColor;-webkit-mask:var(--lente) center/contain no-repeat;
  mask:var(--lente) center/contain no-repeat}

/* ---- aggiunta ---- */
.cassetto[hidden]{display:none}
.cassetto{margin-top:14px;background:var(--pannello);border:1.5px solid var(--linea);
  border-radius:20px;padding:14px}
.cerca{width:100%;border:1.5px solid var(--linea-forte);border-radius:16px;
  padding:12px 13px;font-size:16px;background:var(--carta);color:var(--inchiostro);
  font-family:var(--f-testo)}
.cerca:focus{outline:none;border-color:var(--rosso)}
.reparto{font-family:var(--f-prezzo);text-transform:uppercase;letter-spacing:.08em;
  font-size:11.5px;font-weight:600;color:var(--tenue);margin:16px 0 8px}
.reparto:first-child{margin-top:14px}
.chiudi{width:100%;margin-top:16px;background:var(--inchiostro);color:var(--carta);border:0;
  border-radius:99px;padding:13px;font-size:15px;font-weight:600;cursor:pointer;min-height:48px}
.fuori-catalogo{margin:8px 0 0;font-size:13.5px;color:var(--tenue)}
.form-agg{display:flex;gap:8px;margin-top:16px}
.form-agg input{flex:1;min-width:0;background:var(--carta);color:var(--inchiostro);
  border:1.5px solid var(--rosso);border-radius:16px;padding:12px 13px;
  font-family:var(--f-testo);font-size:16px}
.form-agg input:focus{outline:none}
.form-agg button{background:var(--rosso);color:var(--su-rosso);border:0;border-radius:99px;
  padding:0 18px;font-size:15px;font-weight:600;cursor:pointer;min-height:46px}

/* ---- la casella che cerca fra TUTTI i prezzi ---- */
/* Sta fuori dalla barra appiccicata, come il cassetto e per la stessa ragione:
   dentro, la barra diventerebbe piu alta dello schermo e il telefono dovrebbe
   rifarne i conti a ogni tocco. */
.ricerca[hidden]{display:none}
/* IL TASTO «GRANDI MARCHE» e le sue venti pillole (2026-09-22). Il tasto sta
   accanto a quello rosso, vuoto col bordo rosso: e' un'altra strada per la
   stessa ricerca, non una cosa da premere per prima. */
.riga-cerca{display:flex;gap:6px;align-items:stretch}
.riga-cerca .tasto.trova{flex:1 1 auto;width:auto;min-width:0;white-space:normal;
  line-height:1.15;font-size:14px;padding:5px 12px;text-align:center}
/* Sul telefono, accanto a GRANDI MARCHE, la scritta del tasto rosso non ci
   stava su una riga e veniva tagliata ai due lati («erca un prodotto o una
   ma»): adesso va a capo dentro la pastiglia invece di sparire. */
.tasto.marchi{flex:none;border:1.5px solid var(--rosso);color:var(--rosso);
  background:var(--carta);border-radius:99px;font-weight:700;font-size:12.5px;
  letter-spacing:.02em;min-height:42px;padding:6px 10px}
.tasto.marchi[aria-pressed="true"]{background:var(--rosso);color:var(--su-rosso)}
/* I DUE TASTI SONO GRANDI UGUALI (Manlio, 2026-09-23: «i tasti Grandi Marche
   e Cerca devono essere delle stesse dimensioni, Grandi Marche messo a
   destra»). Metà riga ciascuno, stessa altezza. */
.riga-cerca .tasto.trova,.riga-cerca .tasto.marchi,.riga-cerca .tasto.sez{flex:1 1 0;
  width:auto;min-width:0;margin:0;letter-spacing:0}
.ricerca .q[hidden]{display:none}
/* LA STRISCIA DEI TRE TASTI RESTA SEMPRE IN ALTO (Manlio, 2026-09-23: «quando
   si fa scroll i tre tasti devono rimanere sempre visibili in alto»). Prima
   restavano attaccate le pillole dei prodotti: due o tre righe che, insieme ai
   tasti, si sarebbero mangiate mezzo schermo. Adesso le pillole scorrono via
   e per tornarci si tocca «Prodotti». I tasti sono alti 44 px, più delle
   pillole (34): sono i tasti principali della pagina, da prendere al volo. */
.riga-cerca{position:sticky;top:0;z-index:25;background:var(--carta);
  margin:0 -15px;padding:8px 15px;border-bottom:1.5px solid var(--linea)}
.barra{position:static}
.barra.fissa{position:sticky;z-index:20;margin-top:0;padding-top:10px}
/* Con l'id: la regola dei quattro tasti, più sotto, rimette gap:7px. */
#riga-cerca .tasto.marchi{flex-direction:column;gap:0}
.riga-gm{display:block;line-height:1.05}
/* Sui telefoni più stretti, un filo più piccola: «Personale» toccava i bordi. */
@media (max-width:380px){ #riga-cerca .tasto{font-size:13px} }
/* ---- la sezione personale ---- */
.personale[hidden],.negozi-pers-box[hidden]{display:none}
.personale{margin-top:14px}
.form-pers{display:flex;gap:8px}
.form-pers input{flex:1;min-width:0;border:1.5px solid var(--rosso);border-radius:99px;
  padding:11px 18px;font-size:16px;background:var(--carta);color:var(--inchiostro);
  font-family:var(--f-testo)}
.form-pers input:focus{outline:none}
.form-pers button{flex:none;background:var(--rosso);color:var(--su-rosso);border:0;
  border-radius:99px;padding:0 18px;font-size:15px;font-weight:700;cursor:pointer;min-height:46px}
.pillole-pers{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.pillola-pers{display:inline-flex;align-items:stretch;border:1.5px solid var(--linea-forte);
  border-radius:99px;background:var(--carta);overflow:hidden}
.pillola-pers .nome-pers{background:none;border:0;padding:6px 4px 6px 13px;font-size:14px;
  font-weight:600;cursor:pointer;min-height:34px;font-family:inherit;color:var(--inchiostro)}
.pillola-pers .via-pers{background:none;border:0;padding:0 11px 0 7px;font-size:17px;
  line-height:1;cursor:pointer;color:var(--tenue);font-family:inherit}
.pillola-pers.aperta{border-color:var(--rosso);background:var(--rosso)}
.pillola-pers.aperta .nome-pers,.pillola-pers.aperta .via-pers{color:var(--su-rosso)}
.tasto-negozi-pers{margin-top:12px;background:var(--carta);border:1.5px solid var(--linea-forte);
  border-radius:99px;padding:8px 15px;font-size:14px;font-weight:600;cursor:pointer;
  min-height:38px;font-family:inherit;color:var(--inchiostro)}
.tasto-negozi-pers[aria-expanded="true"]{border-color:var(--rosso);color:var(--rosso)}
.negozi-pers-box{margin-top:10px;background:var(--pannello);border-radius:18px;padding:12px}
.negozi-pers-box .sotto-titolo{margin:0 0 10px;color:var(--tenue);font-size:13.5px}
.blocco-pers{margin-top:18px;scroll-margin-top:70px}
.blocco-pers h2{font-family:var(--f-prezzo);text-transform:uppercase;letter-spacing:.02em;
  font-size:21px;font-weight:600;margin:0}
.blocco-pers .nulla{color:var(--tenue);font-size:14px;margin:6px 0 0}
.vuoto-pers{color:var(--tenue);font-size:14.5px;margin:16px 0 0;background:var(--pannello);
  border-radius:20px;padding:16px}
/* Sui telefoni più stretti «Grandi marche» non sta su una riga: va a capo
   dentro il tasto, che resta alto uguale, invece di uscire dai bordi. */
@media (max-width:420px){
  #riga-cerca .tasto{white-space:normal;text-align:center}
}
/* I DUE TASTI ALTI COME LE PASTIGLIE DEI PRODOTTI, BIANCHI ALL'INIZIO
   (Manlio, 2026-09-23). Quello della pagina aperta diventa rosso pieno:
   «Cerca» rosso nella ricerca, «GRANDI MARCHE» rosso nelle marche. */
.riga-cerca .tasto.trova,.riga-cerca .tasto.marchi,.riga-cerca .tasto.sez{min-height:44px;
  padding:6px 4px;font-size:14px;display:flex;align-items:center;justify-content:center;gap:7px;line-height:1.1;background:var(--carta);color:var(--rosso);
  border:1.5px solid var(--rosso);font-weight:700;white-space:nowrap}
.riga-cerca .tasto.trova[aria-pressed="true"],.riga-cerca .tasto.marchi[aria-pressed="true"],
.riga-cerca .tasto.sez[aria-pressed="true"]{
  background:var(--rosso);color:var(--su-rosso)}
.spiega[hidden],.chiudi[hidden]{display:none}
/* La pagina della ricerca è solo una pillola dove scrivere: niente riquadro
   intorno. */
#ricerca{background:none;border:0;padding:0}
.ricerca .q{border-radius:99px;padding:11px 18px}
.marche[hidden],.barra[hidden]{display:none}
/* «hidden» da solo NON basta su un elemento a cui il CSS da display:flex: il
   2026-09-22 i quattro tasti in cima e la riga «I tuoi prodotti» erano stati
   nascosti cosi, le prove (che guardano l'attributo) dicevano di si, e sul
   telefono si vedevano ancora. Scoperto guardando una schermata vera. */
.capo-prodotti[hidden]{display:none}
/* I DUE PALLINI accanto al titolo, a destra (2026-09-22). Piccoli, 32 px: il
   primo è l'ingranaggio della configurazione (colori, supermercati, aiuto),
   il secondo ha una N e apre le novità. */
.riga-alta{align-items:center;flex-wrap:nowrap}
.pallini{flex:none;display:flex;align-items:center;gap:8px}
.pallino{flex:none;width:32px;height:32px;min-height:0;border-radius:50%;padding:0;
  display:grid;place-items:center;cursor:pointer;text-decoration:none;line-height:1}
.pallino.config{background:var(--carta);border:1.5px solid var(--linea-forte);color:var(--inchiostro)}
.pallino.config::before{content:'';width:19px;height:19px;background:currentColor;
  -webkit-mask:var(--ingranaggio) center/contain no-repeat;mask:var(--ingranaggio) center/contain no-repeat}
/* LA FINESTRA DELLA CONFIGURAZIONE: i supermercati da tenere, e le altre
   finestre (colori, aiuto, novità della pagina). */
.sez-config{font-family:var(--f-prezzo);text-transform:uppercase;letter-spacing:.06em;
  font-size:13px;font-weight:600;color:var(--tenue);margin:16px 0 6px}
.negozi{display:flex;flex-wrap:wrap;gap:8px}
.negozi button{display:inline-flex;align-items:center;gap:6px;background:#FFFFFF;
  border:2px solid var(--verde);border-radius:99px;padding:3px 10px 3px 4px;cursor:pointer;
  min-height:42px;font-family:inherit}
.negozi button::after{content:'\2713';color:var(--verde);font-weight:700;font-size:15px}
.negozi button .marchio{border:0;min-height:0;padding:2px 4px}
.negozi button[aria-pressed="false"]{border:1.5px dashed var(--linea-forte);opacity:.45}
.negozi button[aria-pressed="false"] img,.negozi button[aria-pressed="false"] svg{filter:grayscale(1)}
.negozi button[aria-pressed="false"]::after{content:'';}
.avviso-negozi{margin:8px 0 0;font-size:13px;color:var(--ambra);font-weight:600}
.voci-config{display:grid;gap:8px}
.voci-config button{width:100%;text-align:left;background:var(--carta);
  border:1.5px solid var(--linea-forte);border-radius:14px;padding:11px 14px;
  font-size:15px;font-weight:600;cursor:pointer;min-height:46px;font-family:inherit;
  color:var(--inchiostro)}
/* LA N NON È PIÙ ROSSA (Manlio, 2026-09-23, punto 4: «toglie il rosso solo
   dal pulsante in alto a destra rotondo con N in mezzo»): bianca col bordo,
   come l'ingranaggio accanto. */
.pallino.novita{background:var(--carta);color:var(--inchiostro);border:1.5px solid var(--linea-forte);
  font-family:var(--f-prezzo);font-size:16px;font-weight:700;letter-spacing:0;gap:0}
.pallino.novita::after{content:none}
.marche{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px}
.marche button{background:var(--carta);border:1.5px solid var(--linea-forte);
  border-radius:99px;padding:5px 11px;font-size:13.5px;font-weight:600;
  min-height:32px;cursor:pointer;font-family:inherit;color:var(--inchiostro)}
.marche button:disabled{opacity:.4;border-style:dashed;cursor:default;
  font-weight:500}
/* Le pillole col marchio vero: fondo BIANCO fisso come quelle dei
   supermercati, se no con un look scuro i loghi sparirebbero. Quella scelta
   non diventa rossa piena (coprirebbe il logo): prende un bordo rosso spesso.
   Quelle spente diventano grigie, oltre che sbiadite. */
.marche button.col-logo{background:#FFFFFF;padding:3px 10px;min-height:36px;
  display:inline-flex;align-items:center}
.marche button.col-logo img{height:24px;width:auto;max-width:110px;display:block;object-fit:contain}
.marche button.col-logo:disabled img{filter:grayscale(1)}
.marche button.col-logo[aria-pressed="true"]{background:#FFFFFF;
  border-color:var(--rosso);box-shadow:0 0 0 2px var(--rosso)}
.marche button[aria-pressed="true"]{background:var(--rosso);border-color:var(--rosso);
  color:var(--su-rosso)}
.ricerca{margin-top:14px;background:var(--pannello);border:1.5px solid var(--linea);
  border-radius:20px;padding:14px}
.ricerca .q{width:100%;border:1.5px solid var(--rosso);border-radius:16px;
  padding:13px 13px;font-size:16px;background:var(--carta);color:var(--inchiostro);
  font-family:var(--f-testo)}
.ricerca .q:focus{outline:none}
.quanti-trovati{margin:10px 0 0;font-size:13.5px;color:var(--tenue);scroll-margin-top:14px}
.quanti-trovati b{color:var(--inchiostro)}
#trovati{margin-top:4px}
#trovati .fascia:first-child{margin-top:14px}

/* ---- intestazione del risultato ---- */
.capo{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:20px 0 2px}
.capo .info{flex:none}
/* Dice cosa fa, invece di una crocetta da interpretare. */
.elimina{flex:none;background:var(--carta);border:1.5px solid var(--rosso);color:var(--rosso);
  border-radius:99px;padding:8px 15px;font-size:14px;font-weight:600;cursor:pointer;
  min-height:38px;line-height:1.1;white-space:nowrap}
.conferma[hidden]{display:none}
.conferma{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-top:10px;
  background:var(--rosso-tenue);border:1.5px solid var(--rosso);border-radius:18px;padding:11px 13px}
.conferma span{font-size:14.5px;font-weight:600;flex:1;min-width:9em}
.conferma button{border-radius:99px;padding:9px 15px;font-size:14.5px;font-weight:600;
  cursor:pointer;min-height:42px;border:1.5px solid var(--rosso);background:var(--carta);
  color:var(--rosso)}
.conferma .si{background:var(--rosso);color:var(--su-rosso)}
.capo h2{font-family:var(--f-prezzo);text-transform:uppercase;letter-spacing:.02em;
  font-size:23px;font-weight:600;margin:0}
.capo .unita{flex:none;background:var(--pannello);border:1px solid var(--linea);
  border-radius:99px;padding:4px 11px;font-size:12.5px;color:var(--tenue);
  font-weight:600;white-space:nowrap}
#risultato .quanti{color:var(--tenue);font-size:13px;font-variant-numeric:tabular-nums;
  margin:0 0 8px}
.sinonimi{margin:6px 0 0;font-size:13.5px;color:var(--tenue);display:flex;
  flex-wrap:wrap;gap:6px;align-items:baseline}
.sinonimi em{font-style:normal;background:var(--pannello);border:1px solid var(--linea);
  border-radius:99px;padding:2px 9px;font-size:13px;color:var(--inchiostro)}
.gestisci{display:flex;gap:9px;margin:12px 0 0;flex-wrap:wrap}
.gestisci button{background:var(--carta);border:1.5px solid var(--linea-forte);border-radius:99px;
  padding:10px 16px;font-size:14.5px;font-weight:600;cursor:pointer;min-height:44px}
.form-rin{display:none;gap:8px;margin-top:10px}
.form-rin.on{display:flex}
.form-rin input{flex:1;min-width:0;border:1.5px solid var(--rosso);border-radius:10px;
  padding:12px 13px;font-family:var(--f-testo);font-size:16px;background:var(--carta);
  color:var(--inchiostro)}
.form-rin input:focus{outline:none}
.form-rin button{background:var(--rosso);color:var(--su-rosso);border:0;border-radius:99px;
  padding:0 18px;font-size:15px;font-weight:600;cursor:pointer;min-height:46px}

/* ---- il cerchietto dei giorni che mancano ---- */
/* Chiesto da Manlio il 2026-09-22, con in mano le schermate dei riquadri
   Material: «quella dove c'è scritto 6.80, potresti utilizzarla, messa in
   ogni offerta, magari piccola, per indicare quanti giorni mancano».
   L'anello si consuma come si consuma il volantino: quasi pieno il primo
   giorno, un filo l'ultimo. Il numero dentro conta ANCHE OGGI, quindi non
   arriva mai a zero: «1» vuol dire «oggi è l'ultimo giorno».

   Blu finché c'è tempo, ambra negli ultimi tre giorni: l'ambra, in questa
   pagina, è il colore di «attenzione alla data», e resta ambra in tutti i
   look. Il rosso no: lì vuol dire «premi qui». */
.giorni{display:flex;flex-direction:column;align-items:center;gap:2px;margin-top:8px}
.giorni .anello{position:relative;width:38px;height:38px}
.giorni svg{width:38px;height:38px;display:block;transform:rotate(-90deg)}
.giorni .fondo{fill:none;stroke:var(--blu-tenue);stroke-width:4}
.giorni .arco{fill:none;stroke:var(--blu);stroke-width:4;stroke-linecap:round}
.giorni .num{position:absolute;inset:0;display:grid;place-items:center;
  font-family:var(--f-prezzo);font-size:15px;font-weight:700;color:var(--blu);
  font-variant-numeric:tabular-nums;line-height:1}
.giorni .gg{font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;
  font-weight:700;color:var(--blu);font-family:var(--f-testo)}
.giorni.poco .fondo{stroke:var(--ambra-tenue)}
.giorni.poco .arco{stroke:var(--ambra)}
.giorni.poco .num,.giorni.poco .gg{color:var(--ambra)}
/* Nelle righe dell'elenco sta sotto il prezzo, appoggiato a destra come lui. */
.prezzo-riga .giorni{align-items:flex-end}

/* IL TONDINO DI QUANDO COMINCIA. Chiesto da Manlio il 2026-09-22: «"vale dal",
   che adesso è in una pillola, potrebbe anche lui diventare un'icona rotonda
   come quella dei giorni di validità, con al centro il numero del giorno e
   sotto il nome del mese». Sta nello stesso posto del cerchietto dei giorni,
   nella colonna del prezzo: le due cose non capitano mai insieme, o
   un'offerta è cominciata o deve cominciare. */
.parte{display:flex;flex-direction:column;align-items:flex-end;gap:2px;margin-top:8px}
.parte .num{position:absolute;inset:0;display:grid;place-items:center;
  font-family:var(--f-prezzo);font-size:15px;font-weight:700;color:var(--blu);
  font-variant-numeric:tabular-nums;line-height:1}
.parte .mese{font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;
  font-weight:700;color:var(--blu);font-family:var(--f-testo)}

/* IL PREZZO DI UN'OFFERTA CHE NON È ANCORA COMINCIATA È GRIGIO. Manlio,
   2026-09-22: «si nota poco che non sono ancora attivi; secondo me dovrebbero
   avere il prezzo in grigio». Il numero rosso grande era la cosa che si
   vedeva di più della riga, e continuava a gridare «sono qui» anche quando
   in cassa non lo facevano. */
.prezzo-riga.dopo .val .n{color:var(--tenue)}
/* ---- le schede delle offerte ---- */
/* Ogni offerta è una scheda con gli angoli tondi, e dentro tutto in pillole:
   il marchio del negozio, il nome, il formato, la nota, e a destra i due
   prezzi (quello della confezione e quello per unità). Chiesto da Manlio il
   2026-09-22 con una schermata alla mano. */
.fascia{font-size:13.5px;color:var(--tenue);margin:14px 0 0}
/* Piu compatte dal 2026-09-22, sempre su sua richiesta: stessa roba, meno
   aria intorno, cosi in uno schermo ci stanno piu offerte. */
.prezzo-riga{display:grid;grid-template-columns:1fr auto;gap:2px 14px;
  background:var(--carta);border:1.5px solid var(--linea);border-radius:16px;
  padding:10px 13px 9px;margin-top:8px}
.prezzo-riga .dati{grid-column:1;grid-row:2;min-width:0}
/* Il nome è MENO NERO del resto (Manlio, 2026-09-23: «praticamente tutte le
   scritte sono in grassetto, in particolare quella della descrizione»): se è
   tutto in grassetto, niente risalta. Un gradino sotto, non sottile: è il
   titolo dell'offerta e si deve leggere bene. */
.prezzo-riga .nome{margin:5px 0 0;font-size:16px;font-weight:500;line-height:1.25}
.prezzo-riga .sotto{margin:4px 0 0;color:var(--tenue);font-size:13.5px}
.prezzo-riga .sotto b{color:var(--inchiostro);font-weight:600}
.prezzo-riga .val{grid-column:2;grid-row:2;align-self:start;text-align:right;line-height:1;white-space:nowrap}
.prezzo-riga .val .p1,.prezzo-riga .val .p2{display:block}
.prezzo-riga .val .p2{margin-top:5px}
.prezzo-riga .val .n{display:inline-block;font-family:var(--f-prezzo);font-size:26px;
  font-weight:700;color:var(--rosso);font-variant-numeric:tabular-nums}
.prezzo-riga .val .pz{display:inline-block;font-family:var(--f-prezzo);font-size:19px;
  font-weight:600;font-variant-numeric:tabular-nums}
.prezzo-riga .val .u,.prezzo-riga .val .et{display:inline-block;font-size:10.5px;
  letter-spacing:.07em;text-transform:uppercase;font-weight:700;color:var(--tenue);
  margin-left:7px}
/* Il peso della confezione accanto al suo prezzo: minuscolo, come si scrive. */
.prezzo-riga .val .et.fmt{text-transform:none;letter-spacing:0;font-size:13px;font-weight:600}
/* Sul telefono i due prezzi finiscono sulla stessa riga: senza questo,
   «al pezzo» resta appiccicato all'euro di prima. */
.prezzo-riga .val .p2{margin-left:2px}
.prezzo-riga .coda{grid-column:1/-1;grid-row:1;margin:0;display:flex;flex-wrap:wrap;
  gap:6px;align-items:center}
/* IL MARCHIO DEL NEGOZIO, chiesto da Manlio il 2026-09-22: «al posto del nome
   del negozio e dell'intero indirizzo, che non mi interessa niente, mettici
   il marchio dei supermercati». I marchi veri non si possono prendere e
   pubblicare, quindi sono disegnati qui: il nome dell'insegna scritto nei
   suoi colori. I colori stanno tutti e due dentro la pillola, quindi si
   leggono uguale con qualunque look. */
.marchio{display:inline-flex;align-items:center;border-radius:99px;
  padding:5px 13px;font-size:13px;font-weight:700;letter-spacing:.02em;
  line-height:1.1;white-space:nowrap}
/* Il marchio vero: dentro una pastiglia bianca, alto 26 px. Il bianco non
   cambia con il look — i loghi hanno i loro colori e su un fondo scuro
   sparirebbero. */
.marchio.col-logo{background:#FFFFFF;border:1px solid var(--linea-forte);
  padding:4px 9px;min-height:34px}
.marchio.col-logo svg,.marchio.col-logo img{height:26px;width:auto;max-width:104px;
  display:block;object-fit:contain}
/* Il nome scritto c'e sempre, ma si vede solo con un lettore di schermo: un
   logo, per chi non lo vede, e un buco. */
.solo-voce{position:absolute;width:1px;height:1px;margin:-1px;padding:0;
  overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
/* LA SCHEDA DEL MENO CARO. Bordo verde e fondo verde chiaro, con la sua
   pillola in cima: il verde, in questa pagina, vuol dire «il meno caro» e
   resta verde in tutti i cento look. */
.prezzo-riga.vince{background:var(--verde-tenue);border:2px solid var(--verde);
  padding:9px 12px 8px}
/* LE OFFERTE CHE DEVONO ANCORA COMINCIARE SONO SBIADITE, col prezzo grigio:
   sbiadite, non nascoste — un prezzo che parte lunedì serve saperlo. */
.prezzo-riga.dopo{opacity:.82}
.prezzo-riga.dopo .val .n{color:var(--tenue)}
.bollo{font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;font-weight:700;
  border-radius:99px;padding:4px 11px}
.bollo.meno{background:var(--verde);color:var(--carta)}
.bollo.dubbio{background:var(--ambra-tenue);color:var(--ambra)}
.bollo.stretta{background:var(--rosso);color:var(--su-rosso)}
.prezzo-riga .sotto .quando{white-space:nowrap}
.prezzo-riga .sotto .quando.stretta{color:var(--rosso);font-weight:700}
/* Le condizioni, in bollini brevi sotto il nome: tessera, app, al banco,
   surgelato, 1+1. Ambra, che qui vuol dire «attenzione a questo». */
.prezzo-riga .cond{display:flex;flex-wrap:wrap;align-items:center;gap:5px;margin:6px 0 0}
.bollo.cond{background:var(--ambra-tenue);color:var(--ambra);font-size:11px;
  padding:3px 9px;letter-spacing:.03em;font-weight:600}
.prezzo-riga.apribile{cursor:pointer}
.prezzo-riga.apribile:active{border-color:var(--rosso)}
.prezzo-riga .dove{margin:8px 0 0;font-size:12.5px;color:var(--tenue)}
a.dove.apri{display:inline-flex;align-items:center;justify-content:center;margin:0;
  padding:5px;border:0;background:none;color:var(--rosso);
  text-decoration:none;min-height:34px;min-width:34px;line-height:1}
a.dove.apri svg{width:24px;height:24px;flex:none;fill:none;stroke:currentColor;
  stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
a.dove.apri::after{content:none}
/* Il tondino dei giorni e il foglietto del volantino, in cima accanto al
   marchio e alti come lui. */
.angolo{display:flex;align-items:center;gap:4px;margin:0}
.angolo .giorni,.angolo .parte{margin:0;gap:0}
.angolo .giorni .gg{display:none}
.angolo .anello,.angolo svg{width:30px;height:30px}
.angolo .num{font-size:12.5px}
.angolo a.dove.apri{min-height:30px;min-width:30px;padding:2px}
/* Lo sconto: una pastiglia scura alta come il tondino. Non rossa (il rosso
   qui vuol dire «premi qui»), non verde («il meno caro»), non ambra
   («attenzione»): è un'informazione, e si legge con qualunque look. */
.angolo .sconto{display:inline-flex;align-items:center;height:30px;padding:0 9px;
  border-radius:99px;background:var(--inchiostro);color:var(--carta);
  font-family:var(--f-prezzo);font-size:14px;font-weight:700;letter-spacing:.02em;
  font-variant-numeric:tabular-nums;white-space:nowrap}
.angolo a.dove.apri svg{width:23px;height:23px}
/* TUTTA LA RIGA IN CIMA ALLA SCHEDA È ALTA 30 PX (Manlio, 2026-09-23: «porta
   le pillole dei marchi alla dimensione del cerchio dei giorni e del
   volantino che hanno di fianco, in altezza»). Il marchio era alto 34-36 px e
   sporgeva sopra e sotto il cerchietto. */
.prezzo-riga .coda .marchio{height:30px;min-height:0;padding-top:0;padding-bottom:0;
  box-sizing:border-box}
.prezzo-riga .coda .marchio.col-logo{padding:0 8px}
.prezzo-riga .coda .marchio.col-logo svg,.prezzo-riga .coda .marchio.col-logo img{height:21px;max-width:96px}
/* IL CALENDARIETTO DI QUANDO PARTE UN'OFFERTA (punto 4, 2026-09-23): mese
   nella striscia in alto e giorno sotto, tutti e due DENTRO, così è alto 30 px
   come il marchio e il cerchietto (Manlio, 2026-09-23: «in modo che abbia
   sempre la stessa altezza»). */
.parte .cal{display:flex;flex-direction:column;width:30px;height:30px;border-radius:6px;
  border:1.5px solid var(--blu);background:var(--carta);overflow:hidden;box-sizing:border-box}
.parte .cal .mese{display:block;background:var(--blu);color:var(--carta);font-size:7.5px;
  line-height:9px;height:9px;text-align:center;letter-spacing:.04em;margin:0;font-weight:700}
.parte .cal .num{position:static;display:grid;place-items:center;flex:1;font-size:12.5px;
  color:var(--blu);line-height:1}

/* SUL TELEFONO LA SCHEDA VA IN COLONNA. A 390 px le due colonne si
   strozzano: il nome del prodotto andava a capo ogni due parole e i prezzi
   finivano schiacciati a sinistra. Sotto i 560 px i prezzi scendono su una
   riga loro, sotto il nome. */
@media (max-width:560px){
  .tasto.trova{font-size:14.5px}
}
/* I PREZZI TORNANO A DESTRA, ANCHE SUL TELEFONO (Manlio, 2026-09-23: «non è
   tutto un po' troppo sbilanciato sulla sinistra… a destra ci potrebbe
   stare il prezzo, eventualmente su due linee»). Il 22 settembre la scheda
   era andata in colonna perché i due prezzi affiancati, con le loro scritte,
   rubavano metà riga al nome. Adesso stanno uno SOPRA l'altro e senza «€»:
   la colonna è stretta. Sopra il prezzo per unità, sotto quello della
   confezione col suo peso.
   I PREZZI STANNO A METÀ DELLA SCHEDA, non attaccati alla prima riga del
   nome (Manlio, 2026-09-23: «rispetto alla pillola finiscono una volta in
   basso, una volta a metà, una volta in alto»). A sinistra le righe vanno da
   una a cinque (sui suoi 13 prodotti: 108 schede da una, 154 da due, 76 da
   tre in su), a destra sono sempre due: attaccati in alto, ballavano. Adesso
   occupano tutta l'altezza della scheda, riga del marchio compresa, e ci
   stanno in mezzo; per questo la riga del marchio sta solo a sinistra. */
.prezzo-riga{grid-template-columns:minmax(0,1fr) auto}
.prezzo-riga .coda{grid-column:1}
.prezzo-riga .val{grid-column:2;grid-row:1 / 3;align-self:center;text-align:right;
  display:flex;flex-direction:column;align-items:flex-end;gap:4px;margin:0;
  white-space:nowrap}
.prezzo-riga .val .p1,.prezzo-riga .val .p2{display:block;margin:0;white-space:nowrap}
.bollo.cond{white-space:nowrap}
.prezzo-riga .val .u{text-transform:none;letter-spacing:0;font-size:13px;margin-left:1px;
  font-weight:600}
.prezzo-riga .val .pz{font-size:15px;color:var(--inchiostro)}
.prezzo-riga .val .et{margin-left:4px;font-size:12px}
.prezzo-riga .val .et.fmt{font-size:12px}

/* ---- elenco pagine ---- */
.pag-riga{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
  padding:11px 0;border-top:1px solid var(--linea);font-size:14.5px}
.pag-riga:first-of-type{border-top:1.5px solid var(--inchiostro)}
.pag-riga .ins{font-weight:600}
.pag-riga .per{display:block;color:var(--tenue);font-size:12.5px;font-weight:400}
.pag-riga .np{font-family:var(--f-prezzo);font-size:19px;font-weight:600;
  font-variant-numeric:tabular-nums;white-space:nowrap}
a.pag-riga{text-decoration:none;color:inherit}
a.pag-riga.apribile{padding:13px 0;min-height:48px}
a.pag-riga.apribile .ins{color:var(--rosso);text-decoration:underline;text-underline-offset:3px}
a.pag-riga.apribile .np{color:var(--rosso)}
a.pag-riga.apribile .np::after{content:' \2197';font-family:var(--f-testo);font-size:13px}
.altre{width:100%;margin-top:12px;background:var(--pannello);border:1.5px solid var(--linea);
  border-radius:99px;padding:12px;font-size:14.5px;font-weight:600;cursor:pointer;min-height:46px}
.vuoto{color:var(--tenue);font-size:14.5px;margin:14px 0 0;background:var(--pannello);
  border-radius:20px;padding:16px}

/* ---- coda ---- */
.spiega{margin-top:34px;background:var(--pannello);border-radius:22px;padding:18px 18px 6px}
.spiega h2{font-family:var(--f-prezzo);text-transform:uppercase;font-size:15px;
  letter-spacing:.04em;margin:0;display:flex;align-items:center;gap:9px}
/* Il bollino «i». Manlio: «la pagina è molto lunga, le spiegazioni meglio che
   appaiano solo quando si fa clic su un bollino di informazioni». Tondo, con
   la i minuscola, grande abbastanza da prendersi col dito. */
.info{flex:none;width:24px;height:24px;border-radius:50%;border:1.5px solid var(--linea-forte);
  background:var(--carta);color:var(--tenue);font-family:var(--f-testo);font-size:14px;
  font-weight:700;line-height:1;cursor:pointer;padding:0;display:grid;place-items:center}
.info:hover{border-color:var(--rosso);color:var(--rosso)}
.info[aria-expanded="true"]{background:var(--rosso);border-color:var(--rosso);color:var(--su-rosso)}
.dettaglio[hidden]{display:none}
.dettaglio{margin-top:10px}
.spiega .dettaglio > p:last-child{margin-bottom:12px}
.spiega > h2 + .dettaglio{margin-bottom:0}
.spiega > h2:not(:first-child){margin-top:18px}
.spiega p{font-size:14px;margin:0 0 12px}
.spiega .ev{color:var(--ambra);font-weight:700}
/* ---- la finestra delle novità della pagina ---- */
/* Sta SOPRA tutto (la barra appiccicata ha z-index 20) e si chiude in tre
   modi: il tasto, il buio intorno, il tasto Esc. Si apre una volta sola:
   quello che uno ha gia visto se lo ricorda il suo browser. */
.buio[hidden]{display:none}
.buio{position:fixed;inset:0;z-index:60;background:rgba(20,19,18,.5);
  display:flex;align-items:center;justify-content:center;padding:16px}
.finestra{background:var(--carta);border-radius:24px;max-width:460px;width:100%;
  max-height:84vh;overflow:auto;padding:18px 18px 0;
  box-shadow:0 18px 50px rgba(0,0,0,.28)}
/* Il tasto per chiudere resta SEMPRE in fondo allo schermo, attaccato: con le
   novità lunghe finiva sotto il bordo e per chiuderla bisognava indovinare
   che si poteva scorrere dentro la finestra. Una finestra che non si capisce
   come si chiude e una trappola. */
.pie-finestra{position:sticky;bottom:0;background:var(--carta);padding:4px 0 14px}
.finestra h2{font-family:var(--f-prezzo);text-transform:uppercase;font-size:17px;
  letter-spacing:.03em;margin:0 0 4px}
.finestra .sotto-titolo{margin:0 0 14px;color:var(--tenue);font-size:13.5px}
.finestra .voce{border-top:1px solid var(--linea);padding:13px 0}
.finestra .voce:first-of-type{border-top:1.5px solid var(--inchiostro)}
.finestra .quando{display:block;color:var(--tenue);font-size:11.5px;
  letter-spacing:.06em;text-transform:uppercase;font-weight:700;margin-bottom:3px}
.finestra .voce h3{margin:0 0 4px;font-size:16px}
.finestra .voce p{margin:0;font-size:14px;color:var(--inchiostro)}
.vol{list-style:none;padding:0;margin:10px 0 0;display:grid;gap:1px;background:var(--linea);
  border:1px solid var(--linea);border-radius:20px;overflow:hidden}
.vol li{background:var(--carta);padding:11px 13px;font-size:14px}
.vol .capo-vol{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
/* I DUE TASTI DI OGNI VOLANTINO, chiesti da Manlio il 2026-09-18: uno apre i
   prezzi letti da quel volantino, l'altro il volantino stesso sul sito di chi
   lo pubblica. Larghi uguali, uno accanto all'altro, alti abbastanza da
   prendersi col dito sul telefono. */
.vol-tasti{display:flex;gap:8px;margin-top:9px}
.vol-t{flex:1 1 0;min-height:40px;display:flex;align-items:center;justify-content:center;
  gap:3px;text-align:center;padding:8px 10px;border:1.5px solid var(--linea-forte);
  border-radius:99px;background:var(--pannello);color:var(--rosso);font-weight:600;
  font-size:13.5px;font-family:inherit;text-decoration:none;cursor:pointer}
.vol-t.fuori::after{content:'\2197'}
.vol-t.spento{color:var(--tenue);border-style:dashed;cursor:default;font-weight:400}
.vol .i{font-weight:600}
.vol .p{color:var(--tenue);font-size:13px}
.vol .n{color:var(--tenue);font-size:12.5px;font-variant-numeric:tabular-nums;white-space:nowrap}
footer{margin-top:28px;padding-top:14px;border-top:1px solid var(--linea);
  color:var(--tenue);font-size:13px}
/* ---- LA PAGINA DEL VOLANTINO, SOPRA L'ELENCO (Manlio, 2026-09-23: «fare
   aprire il volantino quando si fa clic in qualunque di queste schede… e
   mettere in sovrimpressione un bel tastone chiudi in basso»). L'immagine
   NON è nostra e non sta sul sito: la pagina la chiede al sito di chi
   pubblica il volantino, come faceva il collegamento. Il tasto «Chiudi» è
   largo quanto lo schermo e resta attaccato in basso. ---- */
.vol-sopra[hidden]{display:none}
.vol-sopra{position:fixed;inset:0;z-index:70;background:rgba(20,19,18,.92);
  display:flex;flex-direction:column}
.vol-sopra .testa-vol{flex:none;display:flex;align-items:center;justify-content:space-between;
  gap:10px;padding:10px 14px;color:#FFFFFF;font-size:14px}
.vol-sopra .testa-vol b{font-weight:700}
.vol-sopra .testa-vol a{color:#FFFFFF;font-weight:600;text-decoration:underline;
  text-underline-offset:3px;white-space:nowrap}
.vol-sopra .foglio{flex:1;min-height:0;overflow:auto;-webkit-overflow-scrolling:touch;
  padding:0 8px 96px}
.vol-sopra .foglio img{display:block;width:100%;height:auto;margin:0 auto;max-width:900px;
  background:#FFFFFF;border-radius:6px}
.vol-sopra .foglio iframe{display:block;width:100%;height:100%;border:0;background:#FFFFFF;
  border-radius:6px}
.vol-sopra .avviso-vol{color:#FFFFFF;text-align:center;margin:40px 16px;font-size:15px}
.vol-sopra .avviso-vol a{color:#FFFFFF;font-weight:700}
.vol-sopra .chiudi-vol{position:absolute;left:14px;right:14px;
  bottom:calc(14px + env(safe-area-inset-bottom,0px));min-height:58px;border:0;
  border-radius:99px;background:var(--rosso);color:var(--su-rosso);font-family:inherit;
  font-size:19px;font-weight:700;letter-spacing:.02em;cursor:pointer;
  box-shadow:0 6px 24px rgba(0,0,0,.45)}
/* LA RIGA IN CIMA A OGNI PRODOTTO (punto 3): verde per «oggi», come la
   scheda del meno caro; blu per «da domani», come il tondino di quando
   parte un'offerta. */
.sintesi{display:grid;gap:6px;margin:12px 0 0}
.sint{display:flex;align-items:center;gap:6px;flex-wrap:wrap;width:100%;text-align:left;
  border:0;border-radius:14px;padding:9px 13px;font:inherit;font-size:14.5px;cursor:pointer;
  line-height:1.25}
.sint b{font-weight:700}
.sint .freccia{margin-left:auto;font-weight:700}
.sint.oggi{background:var(--verde-tenue);color:var(--verde)}
.sint.dopo{background:var(--blu-tenue);color:var(--blu)}
/* IL MENÙ IN BASSO (Manlio, 2026-09-23, punto 5, dopo le schermate di
   prova: «lo sai che mi piace davvero, bravo, possiamo farla»). I quattro
   tasti delle sezioni stanno in fondo allo schermo, sempre visibili, come
   nelle app: si toccano col pollice. Icona sopra, scritta sotto; quello
   della sezione in cui si è è rosso su un fondino rosa, gli altri grigi.
   Tutte le regole hanno l'id: devono vincere su quelle della striscia in
   alto, più sopra, che restano per la storia. */
#riga-cerca{position:fixed;top:auto;bottom:0;left:0;right:0;margin:0;z-index:30;
  background:var(--carta);border-bottom:0;border-top:1.5px solid var(--linea);
  padding:6px 8px calc(6px + env(safe-area-inset-bottom,0px));gap:4px;
  box-shadow:0 -4px 16px rgba(0,0,0,.06)}
#riga-cerca .tasto,#riga-cerca .tasto.trova,#riga-cerca .tasto.marchi,#riga-cerca .tasto.sez{
  flex-direction:column;justify-content:flex-start;border:0;background:none;color:var(--tenue);
  min-height:56px;font-size:11.5px;gap:4px;border-radius:14px;padding:6px 2px 4px;
  font-weight:700;white-space:normal;text-align:center;line-height:1.1}
#riga-cerca .tasto::before{content:'';display:block;flex:none;width:23px;height:23px;
  background:currentColor;-webkit-mask:var(--ic) center/contain no-repeat;
  mask:var(--ic) center/contain no-repeat}
#riga-cerca .tasto[aria-pressed="true"]{color:var(--rosso);background:var(--rosso-tenue)}
#vai-prodotti{--ic:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='M4 7h16M4 12h16M4 17h10'/%3E%3C/svg%3E")}
#riga-cerca .tasto.trova{--ic:var(--lente)}
#riga-cerca .tasto.marchi{--ic:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 12V4h8l10 10-8 8z'/%3E%3Ccircle cx='7.5' cy='8.5' r='1.5'/%3E%3C/svg%3E")}
#vai-personale{--ic:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round'%3E%3Ccircle cx='12' cy='8' r='4'/%3E%3Cpath d='M4 21c0-4 4-6 8-6s8 2 8 6'/%3E%3C/svg%3E")}
/* «Grandi marche» resta su due righe, ma strette (Manlio: «lo lascerei così,
   con meno interlinea»). */
#riga-cerca .riga-gm{display:block;line-height:.95}
.guscio{padding-bottom:100px}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>

<div class="guscio">
<header>
  <!-- IN CIMA NON C'E PIU «Torino · corso Siracusa» NE IL BOLLINO «i».
       Manlio, 2026-09-22: «togli Torino corso Siracusa e informazioni, che e
       inutile, cioe la lettera i che c'e accanto al corso Siracusa». Dove
       sono i negozi lo sa gia lui, ed era l'unica cosa in cima che non si
       poteva toccare per fare qualcosa. Quello che stava dietro il bollino
       (com'e fatta questa copia) e finito in fondo alla finestra «Aiuto»,
       che e il posto delle spiegazioni. -->
  <div class="riga-alta">
    <!-- IL TITOLO RIPORTA ALL'INIZIO (Manlio, 2026-09-23: «cliccando sopra
         Spesa, Offerte grande distribuzione, si tornerà alla pagina
         iniziale»). Chiude ricerca, grandi marche, cassetto e il volantino
         aperto, e torna in cima. -->
    <a class="marca" id="vai-inizio" href="https://manliograndi-del.github.io/spesa/">
      <span class="segno" aria-hidden="true">S</span>
      <span class="nomi">
        <h1>Spesa</h1>
        <span class="sotto-marca">Offerte grande distribuzione</span>
      </span>
    </a>
    <!-- I DUE PALLINI IN CIMA A DESTRA (Manlio, 2026-09-22: prima «un tasto
         novità e uno rotondo con tanti colori», poi, la stessa notte, «un
         pallino unico di configurazione che porta a una pagina con i colori,
         i supermercati e le altre opzioni... ci vanno due pallini, uno di
         configurazione e l'altro novità»). L'ingranaggio apre la finestra
         «Configurazione»; la N apre il diario delle novità dei prezzi. -->
    <span class="pallini">
      <button type="button" class="pallino config" id="apri-config"
              aria-label="Configurazione" title="Configurazione"></button>
      <a class="pallino novita" href="https://manliograndi-del.github.io/spesa/novita.html"
         target="_blank" rel="noopener noreferrer" aria-label="Novità" title="Novità">N</a>
    </span>
  </div>
</header>

<div class="riga-cerca" id="riga-cerca"></div>

<div class="barra">
  <!-- «I tuoi prodotti (N) · Tocca per confrontare i prezzi» nascosto il
       2026-09-22 su richiesta sua, per guadagnare spazio. -->
  <p class="capo-prodotti" hidden><span id="quanti-prodotti"></span>
    <span class="suggerimento">Tocca per confrontare i prezzi</span></p>
  <div class="tasti" id="tasti" role="group" aria-label="Scegli il prodotto"></div>
  <p class="stato" id="stato-lista" role="status"></p>
</div>

<!-- IL CASSETTO STA FUORI DALLA BARRA, E NON È UN DETTAGLIO.
     Stava dentro, e la barra è appiccicata in alto: aprendolo, quella barra
     diventava più alta dello schermo e il telefono doveva ricalcolarla a ogni
     tocco e a ogni scorrimento. Manlio: «escono solo le prime categorie, poi
     la pagina resta bloccata per un tempo abbastanza lungo». Qui fuori la
     barra resta piccola e il cassetto è roba normale che scorre. -->
<div class="cassetto" id="cassetto" hidden>
  <input class="cerca" id="cerca" type="text" placeholder="Cerca un prodotto…"
         autocomplete="off" aria-label="Cerca un prodotto nel catalogo">
  <div id="scaffali"></div>
  <form class="form-agg" id="form-agg">
    <input id="nuovo" type="text" placeholder="Un altro nome, o più separati da virgola"
           autocomplete="off" aria-label="Nomi del prodotto da aggiungere, separati da virgola">
    <button type="submit">Aggiungi</button>
  </form>
  <p class="fuori-catalogo" id="fuori-catalogo"></p>
  <button type="button" class="chiudi" id="chiudi-cassetto">Fatto</button>
</div>

<!-- LA RICERCA STA FUORI DALLA BARRA, come il cassetto. -->
<div class="ricerca" id="ricerca" hidden>
  <div class="marche" id="marche" hidden role="group" aria-label="Grandi marche"></div>
  <input class="q" id="q" type="search" placeholder="Scrivi un prodotto, una marca, un negozio…"
         autocomplete="off" aria-label="Cerca fra tutti i prezzi dei volantini">
  <p class="quanti-trovati" id="quanti-trovati" role="status"></p>
  <div id="trovati"></div>
  <!-- «Fatto» non serve più (Manlio, 2026-09-23): si esce toccando il titolo
       o l'altro tasto. Resta nascosto perché le prove lo usano per chiudere. -->
  <button type="button" class="chiudi" id="chiudi-ricerca" hidden>Fatto</button>
</div>

<!-- LA SEZIONE PERSONALE (Manlio, 2026-09-23): parole sue, fatte pillole,
     con sotto il riepilogo delle offerte di ognuna e una scelta dei
     supermercati che vale solo qui. Sta fuori dalla barra come la ricerca.
     Tutto resta sul telefono di chi la usa. -->
<div class="personale" id="personale" hidden>
  <form class="form-pers" id="form-pers">
    <input id="parola-pers" type="text" placeholder="Prodotto o marca…"
           autocomplete="off" aria-label="Parola da aggiungere alla sezione personale">
    <button type="submit">Aggiungi</button>
  </form>
  <div class="pillole-pers" id="pillole-pers" role="group" aria-label="Le tue parole"></div>
  <button type="button" class="tasto-negozi-pers" id="apri-negozi-pers"
          aria-expanded="false" aria-controls="negozi-pers-box">Personalizza supermercati</button>
  <div class="negozi-pers-box" id="negozi-pers-box" hidden>
    <p class="sotto-titolo">Tocca un supermercato per toglierlo o rimetterlo. Vale solo
    per questa sezione, e resta su questo telefono.</p>
    <div class="negozi" id="negozi-pers" role="group" aria-label="Supermercati della sezione personale"></div>
    <p class="avviso-negozi" id="avviso-negozi-pers" role="status"></p>
  </div>
  <div id="riepilogo-pers"></div>
</div>

<div id="risultato"></div>


<section class="spiega">
  <h2>Come leggerla <button type="button" class="info" aria-expanded="false" aria-label="Mostra la spiegazione">i</button></h2>
  <div class="dettaglio" hidden>
  <p>In cima ci sono <b>i prodotti che hai scelto tu</b>. Per cambiarli tocca
  <b>«+ altri prodotti»</b>: si apre un cassetto con tutto il catalogo, diviso per reparto come
  il negozio. Tocca un prodotto per accenderlo, toccalo di nuovo per spegnerlo, poi «Fatto».
  <b>Nessuno deve chiedere niente a nessuno</b>: ognuno accende i suoi, sul suo telefono.</p>
  <p>Nel cassetto c'è anche <b>una casella per cercare</b>, e cerca anche fra i nomi che usa il
  volantino: scrivendo «bovino» trovi la carne di bue, scrivendo «lavatrice» trovi il
  detersivo.</p>
  <p>I prezzi sono <b>letti a mano</b>, uno per uno, dalle pagine dei volantini. Il confronto è
  per unità e cambia col prodotto: la carne al chilo, il latte al litro, le uova all'uovo, la
  carta igienica al rotolo, il detersivo a lavaggio. Al chilo il detersivo darebbe un numero
  vero e inutile.</p>
  <p><b>Non tutte le voci del catalogo hanno già i prezzi.</b> Quelle che non ce l'hanno ancora
  ti dicono in quali pagine dei volantini compare la parola, e il prezzo lo leggi tu aprendo la
  pagina. Le sto leggendo a mano, un reparto per volta: compariranno senza che tu debba fare
  niente.</p>
  <p>Se ti serve <b>qualcosa che nel catalogo non c'è</b>, scrivilo nella casella in fondo al
  cassetto: puoi mettere anche più nomi separati da virgola — per esempio
  <i>tovaglioli, salviette</i> — e la pagina cerca le pagine dove compare almeno uno di quelli.</p>
  <p>Le righe segnate <span class="ev">da controllare</span> vengono da riassunti trovati
  online e possono essere sbagliate: di errori così ne ho già trovati tre.</p>
  <p>Certi prezzi valgono <b>solo con la tessera</b> — soci Coop, Lidl Plus, Bennet Club — e
  qualche riga confronta cose diverse fra loro: il caffè in capsule al chilo costa sempre molto
  più del macinato, e l'ammorbidente non è detersivo. Sta scritto nella riga.</p>
  <p>Le parole le ha lette il computer dalle immagini: sulle scritte grandi spesso sbaglia. Se
  un prodotto dà zero pagine può esserci lo stesso, prova a chiamarlo in un altro modo.</p>

  </div>

  <h2>Quando arrivano le offerte nuove <button type="button" class="info" aria-expanded="false" aria-label="Mostra la spiegazione">i</button></h2>
  <div class="dettaglio" hidden>
  <p>I prezzi qui sopra sono dei volantini <b id="letto"></b>. Quando escono quelli nuovi
  <b>la pagina si aggiorna da sola</b>: chi l'ha aperta col link ricarica e vede i prezzi nuovi,
  senza premere niente e senza che nessuno debba rimandare niente. Vale per chiunque abbia il
  link, da qualsiasi telefono.</p>
  <p>L'unica copia che <b>non</b> si aggiorna è il file salvato sul telefono: quello resta fermo
  al giorno in cui è stato fatto. Se ti interessa avere sempre i prezzi giusti, usa il link.</p>
  <p id="p-lista"></p>
  <p>Un prodotto acceso adesso mostra <b>subito le pagine</b> dove compare, ma i
  <b>prezzi arrivano dopo</b>: quelli vanno letti dalle pagine dei volantini a occhio, non c'è
  modo di ricavarli da soli. Quando li ho letti compaiono anche quelli, senza che dobbiate
  rifare niente.</p>

  </div>

  <h2>I volantini</h2>
  <ul class="vol" id="vol"></ul>
  <p style="margin-top:12px">Su ogni riga ci sono due tasti, e tutti e due aprono
  <b>una pagina nuova</b>, così non perdi quello che stavi guardando:
  <b>«Le offerte»</b> ti mostra i prezzi letti da quel volantino, reparto per reparto;
  <b>«Il volantino»</b> apre le sue pagine sul sito di chi lo pubblica.</p>
  <p style="margin-top:12px">I <b>marchi dei supermercati</b> restano di chi li ha:
  stanno qui solo per far riconoscere a colpo d'occhio di quale negozio è un'offerta.
  Dove un marchio non c'è, al suo posto trovi il nome scritto.</p>
  <p style="margin-top:12px">Di Mercatò si legge il volantino del punto vendita di
  <b>via Filadelfia 232</b>. Mercatò Local, Big ed Extra sono insegne diverse con volantini
  diversi: quello di via Demargherita, per dire, è un Local e queste offerte non sono le sue.</p>
  <p style="margin-top:12px">Di Pam si legge il volantino dei <b>supermercati Pam</b>, quello
  del Pam di <b>corso Orbassano 212</b>, il più vicino. I Pam Panorama hanno un volantino loro,
  con prezzi diversi.</p>
  <p style="margin-top:12px">Di Conad si legge il volantino del <b>Conad di via Cesana 78</b>,
  preso direttamente dal sito di Conad. I Conad City e i Superstore hanno volantini loro.</p>
</section>

<footer id="pie"></footer>
</div>

<!-- LA FINESTRA DEI LOOK. Chiesta da Manlio il 2026-09-22: «crea una palette
     di colori per il sito da ciascuna di queste e aggiungi un tasto look che
     permette di scegliere fra queste palette». Le righe si costruiscono quando
     si apre, non prima: sono cento, e farle all'avvio rallenterebbe la pagina
     per una finestra che quasi sempre non si apre. -->
<div class="buio" id="buio-look" hidden>
  <div class="finestra" role="dialog" aria-modal="true" aria-labelledby="titolo-look">
    <h2 id="titolo-look">Scegli il look</h2>
    <p class="sotto-titolo">Cambia i colori della pagina. Il verde del «meno caro»
    e l'ambra degli avvisi restano riconoscibili in tutti i look: quelli vogliono
    dire qualcosa. La scelta resta anche domani.</p>
    <div id="voci-look"></div>
    <div class="pie-finestra">
      <button type="button" class="chiudi" id="chiudi-look">Fatto</button>
    </div>
  </div>
</div>

<!-- LA FINESTRA DELL'AIUTO. Chiesta da Manlio il 2026-09-21: «un pulsantino
     con scritto sopra aiuto, di fianco a quello di novità». Il testo l'ha letto
     e approvato prima che la facessi — l'unico pezzo che ha tolto era un
     «due cose da sapere» sui prezzi letti a mano.

     Sta fuori dal guscio e fuori dalla barra, come quella delle novità, e usa
     lo stesso vestito: una finestra sopra la pagina, non un pezzo che le
     cresce dentro. Questa pero NON si apre da sola e si puo riaprire quante
     volte si vuole: e li per quando serve. -->
<!-- LA FINESTRA DELLA CONFIGURAZIONE (Manlio, 2026-09-22 notte): «un pallino
     unico di configurazione che porta a una pagina con i colori, i
     supermercati e le altre opzioni che volevo mettere in alto». Si apre
     dall'ingranaggio in cima; come le altre sta fuori dalla barra e non resta
     aperta insieme a un'altra finestra. -->
<!-- LA PAGINA DEL VOLANTINO, SOPRA L'ELENCO: si apre toccando una scheda. -->
<div class="vol-sopra" id="vol-sopra" hidden role="dialog" aria-modal="true" aria-labelledby="titolo-vol">
  <div class="testa-vol"><span id="titolo-vol"></span>
    <a id="fuori-vol" target="_blank" rel="noopener noreferrer">Apri sul sito</a></div>
  <div class="foglio" id="foglio-vol"></div>
  <button type="button" class="chiudi-vol" id="chiudi-vol">Chiudi</button>
</div>

<div class="buio" id="buio-config" hidden>
  <div class="finestra" role="dialog" aria-modal="true" aria-labelledby="titolo-config">
    <h2 id="titolo-config">Configurazione</h2>
    <h3 class="sez-config">Supermercati</h3>
    <p class="sotto-titolo">Tocca un supermercato per toglierlo o rimetterlo. Quelli
    tolti spariscono dai prezzi, dalla ricerca, dalle grandi marche e dall'elenco dei
    volantini. La scelta resta su questo telefono.</p>
    <div class="negozi" id="negozi" role="group" aria-label="Supermercati da tenere"></div>
    <p class="avviso-negozi" id="avviso-negozi" role="status"></p>
    <h3 class="sez-config">Altro</h3>
    <div class="voci-config">
      <button type="button" id="apri-look">Colori della pagina</button>
      <button type="button" id="apri-aiuto">Aiuto: come si usa</button>
      <button type="button" id="apri-novita-app">Cosa c'è di nuovo nella pagina</button>
    </div>
    <div class="pie-finestra">
      <button type="button" class="chiudi" id="chiudi-config">Fatto</button>
    </div>
  </div>
</div>

<div class="buio" id="buio-aiuto" hidden>
  <div class="finestra" role="dialog" aria-modal="true" aria-labelledby="titolo-aiuto">
    <h2 id="titolo-aiuto">Come si usa</h2>
    <div class="voce">
      <h3>A cosa serve</h3>
      <p>Cerca i prodotti della tua lista nei volantini dei supermercati vicino a casa
      e ti dice dove costano meno. Il confronto è <b>per unità</b> — al chilo, al litro,
      all'uovo, al rotolo — non a confezione: è l'unico modo per capire chi costa
      davvero meno.</p>
    </div>
    <div class="voce">
      <h3>I bottoni in cima sono i tuoi prodotti</h3>
      <p>Toccane uno: sotto escono tutte le offerte, <b>dalla meno cara in giù</b>.
      La scheda col bordo verde e la scritta <b>«il meno caro valido oggi»</b> è
      quella che puoi comprare <b>oggi</b>: se la prima costa meno ma comincia
      fra qualche giorno, il verde va a quella dopo. Le offerte non ancora
      cominciate sono sbiadite, col prezzo in grigio.</p>
    </div>
    <div class="voce">
      <h3>Per cambiare i prodotti: «+ altri prodotti»</h3>
      <p>Si apre un cassetto col catalogo diviso per reparto, come il negozio. Tocca
      per accendere, tocca di nuovo per spegnere, poi «Fatto». In fondo al cassetto
      puoi anche scrivere un nome che nel catalogo non c'è.</p>
    </div>
    <div class="voce">
      <h3>Il menù in basso: «Prodotti», «Cerca», «Grandi marche», «Personale»</h3>
      <p>Sono le parti della pagina, e restano sempre in fondo allo schermo anche
      quando scorri. Quello rosso è la parte in cui sei. <b>«Prodotti»</b> è la pagina
      con i tuoi prodotti. <b>«Cerca»</b> trova <b>una singola offerta</b> fra
      <b>tutte</b> quelle lette: scrivi un prodotto, una marca, un formato o il
      nome di un negozio, e le offerte escono mentre scrivi. <b>«Grandi
      marche»</b>: tocchi una marca ed escono le sue offerte. <b>«Personale»</b>
      è tua: scrivi un prodotto o una marca, tocchi «Aggiungi» e diventa una
      pillola; sotto trovi la sua offerta più conveniente, e col tasto tutte le
      altre. Lì dentro puoi anche scegliere in quali supermercati cercare. Le
      tue parole restano su questo telefono. È un'altra cosa dalla casella dentro
      il cassetto, che invece accende i prodotti della lista.</p>
    </div>
    <div class="voce">
      <h3>La riga in cima</h3>
      <p>A volte, sopra le offerte di un prodotto, c'è una riga in più. <b>In
      verde</b>: il meno caro che puoi comprare <b>oggi</b>, quando non è fra
      le prime tre schede (sopra ci sono offerte che partono nei prossimi giorni).
      <b>In blu</b>: un'offerta che costerà <b>meno</b> e parte fra poco, con il
      giorno. Toccala e la pagina scende a quella scheda.</p>
    </div>
    <div class="voce">
      <h3>Cosa dice ogni riga</h3>
      <p>Ogni offerta è una scheda. In cima il <b>marchio del negozio</b>, poi il
      <b>cerchietto dei giorni che mancano</b> (o, se l'offerta deve ancora
      cominciare, un <b>calendarietto</b> col giorno in cui parte), poi il prodotto. Il numero grande
      rosso è il prezzo <b>per unità</b>, quello con cui si confrontano i negozi;
      accanto, quanto costa la confezione e quanto pesa. Sotto il nome, quando servono, dei
      <b>bollini gialli con le condizioni</b>: con tessera, solo con app, al banco,
      surgelato, 1+1; e, quando conta, quanto costa senza tessera, se il peso è
      sgocciolato o cos'è davvero il prodotto («Burrata», «Già cotte»).
      <b>Le offerte scadute
      spariscono da sole</b>, secondo la data del telefono.</p>
    </div>
    <div class="voce">
      <h3>Il volantino di ogni offerta</h3>
      <p><b>Tocca un'offerta</b>, in un punto qualunque della scheda: sopra
      l'elenco si apre la pagina del volantino vero dove sta quell'offerta. Per
      tornare ai prezzi tocca il tasto grande <b>«Chiudi»</b> in basso, o il
      tasto «indietro» del telefono. In alto c'è <b>«Apri sul sito»</b>, se la
      vuoi sul sito del negozio.</p>
    </div>
    <div class="voce">
      <h3>In fondo: l'elenco dei volantini</h3>
      <p>Ogni riga ha due tasti: <b>«Le offerte»</b> mostra i prezzi letti da quel
      volantino, <b>«Il volantino»</b> apre le sue pagine. Si aprono in una pagina
      nuova, così non perdi il posto.</p>
    </div>
    <div class="voce">
      <h3>L'ingranaggio in alto: la configurazione</h3>
      <p>Il pallino con l'ingranaggio, accanto al titolo, apre la configurazione: lì
      scegli <b>i supermercati</b> da tenere (quelli tolti spariscono dai prezzi e
      dalla ricerca), i <b>colori</b> della pagina, questo aiuto e le novità della
      pagina.</p>
    </div>
    <div class="voce">
      <h3>Il tasto «Novità»</h3>
      <p>Dice cosa è cambiato: quali volantini sono stati aggiornati, quali stanno per
      arrivare e quali prezzi si sono mossi.</p>
    </div>
    <div class="voce">
      <h3>Questa copia</h3>
      <p id="dove-vive"></p>
    </div>
    <div class="pie-finestra">
      <button type="button" class="chiudi" id="chiudi-aiuto">Ho capito</button>
    </div>
  </div>
</div>

<!-- LA FINESTRA DELLE NOVITÀ. Chiesta da Manlio il 2026-09-18: si apre da sola
     la prima volta che uno apre la pagina, e dice cosa si puo fare adesso che
     prima non si poteva. Sta FUORI dal guscio e fuori dalla barra: e una
     finestra sopra la pagina, non un pezzo che le cresce dentro. -->
<div class="buio" id="buio" hidden>
  <div class="finestra" role="dialog" aria-modal="true" aria-labelledby="titolo-novita">
    <h2 id="titolo-novita">Cosa c'è di nuovo</h2>
    <p class="sotto-titolo">Non i prezzi — quelli stanno nel tasto «Novità» in alto.
    Qui c'è cosa si può fare adesso che prima non si poteva.</p>
    <div id="voci-novita"></div>
    <div class="pie-finestra">
      <button type="button" class="chiudi" id="chiudi-novita">Ho capito</button>
    </div>
  </div>
</div>

<script>
const DATI = __DATI__;

/* La lista non e piu solo mia: vive DENTRO questa pagina pubblicata, cosi la
   vedono e la cambiano tutti quelli che hanno il link. Quando qualcuno la
   tocca, la pagina si ripubblica con la lista nuova dentro e ogni schermo
   aperto si ricarica su quella. Vedi NOTE.md per il perche di questa strada
   invece della memoria sul server. */
const LISTA_PUBBLICATA = __LISTA__;
const TEMPLATE = __TEMPLATE__;

/* Vero solo nella copia pubblicata su Claude, dove la lista e davvero
   condivisa e comanda quella dentro la pagina. Sul sito e falso: li dentro non
   c'e niente che possa aggiornare la lista incorporata, quindi comanda quella
   che l'utente si e fatto nel suo browser, altrimenti le sue modifiche
   sparirebbero a ogni ricaricamento. */
const CONDIVISA = __CONDIVISA__;
const CHIAVE = 'spesa.lista.v1';
const CHIAVE_VISTI = 'spesa.visti.v1';

/* Rimette insieme il documento intero con dentro una lista nuova. L'ordine
   conta: prima la lista, poi il template. Al contrario, il template appena
   infilato porterebbe dentro un altro __LISTA__ e verrebbe riempito quello
   sbagliato. Le barre si spezzano in <\/ perche il tag di chiusura dello
   script, scritto per esteso dentro una stringa, chiuderebbe lo script per
   davvero: il browser lo cerca nel testo, non gli importa che sia in una
   stringa o in un commento. */
function documento(nuova) {
  const l = JSON.stringify(nuova).split('</').join('<\\/');
  const t = JSON.stringify(TEMPLATE).split('</').join('<\\/');
  /* Il modello va SEMPRE per ultimo: appena infilato porta dentro una copia di
     tutti gli altri segnaposto, e da quel momento replace() troverebbe quelli
     invece dei veri. Chi si ripubblica e sempre la copia condivisa. */
  return TEMPLATE
    .replace('__LISTA__', () => l)
    .replace('__CONDIVISA__', () => 'true')
    .replace('__TEMPLATE__', () => t);
}

const norm = s => (s || '').toLowerCase()
  .normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/['\u2019]/g, ' ');
/* i detersivi stanno sotto i 20 centesimi a lavaggio: con due decimali
   diventerebbero tutti «0,14 €» e non si distinguerebbero piu */
const eur = n => (n < 1 ? n.toFixed(3) : n.toFixed(2)).replace('.', ',');

/* Iniziale maiuscola sul nome che si legge, chiesto da Manlio: scriveva
   «biscotti» e se lo ritrovava minuscolo in mezzo agli altri. Si tocca solo la
   prima lettera, non ogni parola: «Olio d'oliva» deve restare cosi, e
   text-transform:capitalize del CSS lo storpierebbe in «Olio D'oliva».
   Le parole con cui si cerca restano minuscole: tanto il confronto le
   abbassa comunque. */
const maiuscola = t => (t || '').charAt(0).toUpperCase() + (t || '').slice(1);

/* Dove la lista e condivisa comanda quella dentro la pagina: e quella che
   vedono tutti, e viene aggiornata ripubblicando. Dove non lo e (il sito, il
   file) comanda quella che l'utente si e fatto: nessuno aggiornera mai quella
   incorporata, che li vale solo come punto di partenza. */
function leggiLista() {
  const dentro = Array.isArray(LISTA_PUBBLICATA) && LISTA_PUBBLICATA.length
    ? LISTA_PUBBLICATA.map(riaggancia) : null;
  if (CONDIVISA && dentro) return dentro;
  try {
    const g = localStorage.getItem(CHIAVE);
    if (g) { const v = JSON.parse(g); if (Array.isArray(v) && v.length) return aggiungiNuovi(v.map(riaggancia), dentro); }
  } catch (e) { /* memoria non disponibile: si riparte da quella incorporata */ }
  /* «dentro» è la lista incorporata quando la pagina è stata generata, e non è
     mai vuota. Il ramo di scorta lascia la lista vuota invece di ripescare una
     seconda copia: fino al 2026-09-05 la lista di partenza viaggiava DUE volte
     nella pagina, una come LISTA_PUBBLICATA e una dentro DATI. Con il catalogo,
     una lista vuota non è più un vicolo cieco: si apre «+ altri prodotti». */
  return dentro || [];
}

/* I PRODOTTI NUOVI ARRIVANO ANCHE SUL TELEFONO DI CHI HA GIA UNA SUA LISTA.
   Sul sito la lista vive nel browser di chi apre, e appena uno la tocca quella
   salvata comanda per sempre. Risultato visto il 2026-09-05: Manlio aveva
   aggiunto «Dentifricio» giorni prima, e i quattro prodotti chiesti da lui il
   4 settembre — biscotti, yogurt, marmellata, cioccolato — sul suo telefono
   non sono mai comparsi. Ha aperto la pagina, ha cercato lo yogurt di cui gli
   avevo appena parlato, e non c'era.

   Quindi: un prodotto della lista pubblicata che questo telefono non ha MAI
   visto viene aggiunto. Uno che ha visto e poi tolto NON torna: i nomi visti
   si segnano a parte e restano segnati anche dopo che il prodotto e stato
   tolto. Senza quella memoria, ogni cancellazione sarebbe stata annullata al
   ricaricamento dopo — che e il baco opposto, e peggiore. */
function visti() {
  try {
    const g = localStorage.getItem(CHIAVE_VISTI);
    const v = g ? JSON.parse(g) : null;
    return Array.isArray(v) ? v : null;
  } catch (e) { return null; }
}
function segnaVisti(nomi) {
  try {
    const dentro = visti() || [];
    nomi.forEach(n => { if (!dentro.some(x => norm(x) === norm(n))) dentro.push(n); });
    localStorage.setItem(CHIAVE_VISTI, JSON.stringify(dentro));
  } catch (e) { /* pazienza: al massimo un prodotto tolto ricompare una volta */ }
}
function aggiungiNuovi(mia, pubblicata) {
  if (!pubblicata) return mia;
  const gia = visti();
  /* La prima volta la memoria dei visti non c'e ancora: allora contano per
     visti i prodotti che questo telefono ha in lista adesso, e i mancanti
     sono davvero prodotti nuovi mai arrivati fin qui. */
  const noti = gia || mia.map(v => v.nome);
  const nuovi = pubblicata.filter(x => !noti.some(n => norm(n) === norm(x.nome))
                                    && !mia.some(v => norm(v.nome) === norm(x.nome)));
  segnaVisti(pubblicata.map(x => x.nome).concat(mia.map(v => v.nome)));
  if (!nuovi.length) return mia;
  arrivati = nuovi.map(x => maiuscola(x.nome));
  const unita = mia.concat(nuovi.map(x => ({ ...x })));
  /* Salvare subito, non aspettare che tocchi qualcosa: al caricamento dopo i
     nuovi risultano gia visti e non verrebbero riaggiunti, cioe sparirebbero
     un'altra volta. */
  try { localStorage.setItem(CHIAVE, JSON.stringify(unita)); } catch (e) {}
  return unita;
}

/* Una lista salvata da una versione vecchia della pagina puo avere prodotti
   senza categoria — quando i prezzi letti a mano coprivano solo carne, tonno e
   salmone. Qui si riattaccano ai prezzi che nel frattempo sono arrivati, senza
   toccare i nomi che l'utente si e scelto. Chi ha aggiunto un prodotto suo che
   non corrisponde a niente resta com'e. */
function riaggancia(v) {
  if (!v || !v.nome) return v;
  v = { ...v, nome: maiuscola(v.nome) };
  /* Una categoria salvata prima puo non esistere piu. Il 2026-09-05 «Detersivo»
     si e diviso in lavatrice, lavastoviglie e ammorbidente: chi aveva quel
     bottone si sarebbe ritrovato un prodotto che non trova piu nessun prezzo,
     senza capire perche. Quindi una categoria che il catalogo non conosce si
     butta e si riprova ad agganciare dal nome. */
  /* I NOMI ACCORCIATI DEL 2026-09-22. Chi ha una lista salvata ce l'ha ancora
     coi nomi lunghi: «Prosciutto crudo», «Succhi e bibite», «Carne di bue».
     Qui il bottone prende il nome nuovo e si riattacca alla categoria nuova,
     senza perdere niente. Si tocca SOLO chi ha ancora esattamente il nome che
     aveva il catalogo: se uno si e rinominato il prodotto a modo suo, quel
     nome resta suo. Senza questo pezzo «Pesce fresco» non si riaggancerebbe
     affatto: il ripescaggio qui sotto va per nome e per parole del volantino,
     e fra le parole del pesce la parola «pesce» non c'e apposta. */
  const nuovoNome = (DATI.rinominate || {})[v.nome];
  if (nuovoNome) v = { ...v, nome: nuovoNome, cat: nuovoNome };
  else if (v.cat && (DATI.rinominate || {})[v.cat]) v = { ...v, cat: DATI.rinominate[v.cat] };

  if (v.cat && !DATI.catalogo.some(x => x.nome === v.cat)) v = { ...v, cat: null };
  if (v.cat) return v;
  const nomi = [v.nome].concat(v.parole || []).map(norm);
  const seme = DATI.catalogo.find(x =>
    nomi.includes(norm(x.nome)) || (x.parole || []).some(w => nomi.includes(norm(w))));
  if (!seme) return v;
  const parole = (v.parole || []).slice();
  seme.parole.forEach(p => { if (!parole.some(x => norm(x) === norm(p))) parole.push(p); });
  return { nome: maiuscola(v.nome), parole, cat: seme.nome };
}
function salvaLocale() {
  segnaVisti(lista.map(v => v.nome));   // cosi un prodotto tolto non ricompare
  try { localStorage.setItem(CHIAVE, JSON.stringify(lista)); }
  catch (e) { /* la pagina funziona lo stesso, solo non ricorda */ }
}

let arrivati = [];       // prodotti nuovi comparsi in questo caricamento
let ART = null;          // la capacita di ripubblicare, se questa vista ce l'ha
let soloMio = true;      // finche non sappiamo il contrario, la lista e solo qui
let attesa = null;       // per non ripubblicare a ogni singolo tocco

function stato(testo, brutto) {
  const e = document.getElementById('stato-lista');
  if (!e) return;
  e.textContent = testo;
  e.className = 'stato' + (brutto ? ' brutto' : '');
}

/* Si ripubblica dopo un attimo, non a ogni tocco: chi ne toglie tre di fila
   fa una pubblicazione sola invece di tre, e gli altri schermi si ricaricano
   una volta sola. */
function salva() {
  salvaLocale();
  if (!ART || soloMio || !TEMPLATE) return;
  stato('Sto salvando per tutti…');
  clearTimeout(attesa);
  attesa = setTimeout(async () => {
    try {
      await ART.publish(documento(lista));
      stato('Salvata. La vedono tutti quelli che hanno il link.');
    } catch (err) {
      const c = err && err.code;
      if (c === 'conflict') {
        /* qualcun altro ha salvato nel frattempo: ogni schermo si ricarica
           sulla sua versione, quindi qui non si insiste */
        stato('Nel frattempo l\'ha cambiata qualcun altro: fra un attimo vedi la sua.');
      } else if (c === 'not_writer' || c === 'not_granted') {
        soloMio = true;
        stato('Puoi solo guardare la lista di chi te l\'ha mandata: le tue modifiche restano su questo telefono.', true);
      } else {
        stato('Non sono riuscito a salvarla per tutti. Resta su questo telefono.', true);
      }
    }
  }, 1200);
}


let lista = leggiLista();
let scelto = 0;
let tutteLePagine = false;

/* Le offerte gia in corso prima, quelle che devono ancora cominciare dopo.
   I volantini nuovi si leggono in anticipo — quello dell'Eurospin letto il
   5 settembre partiva il 10 — e senza questo si sarebbero piazzate in cima
   con tanto di bollo «il meno caro» pur non valendo ancora niente in cassa. */
/* «2026-09-10» -> «dal 10 settembre»: la data grezza in mezzo a un bollo non
   si legge, e l'anno non serve a chi guarda le offerte di questa settimana.
   L'8 e l'11 vogliono «dall'», non «dal»: il bollo diceva «vale dal 8
   settembre» e si leggeva come una svista. */
const MESI = ('gennaio febbraio marzo aprile maggio giugno luglio agosto '
  + 'settembre ottobre novembre dicembre').split(' ');
function soloGiorno(iso) {
  if (!iso) return '';
  const p = iso.split('-');
  return Number(p[2]) + ' ' + MESI[Number(p[1]) - 1];
}
function giorno(iso) {
  if (!iso) return '';
  const n = Number(iso.split('-')[2]);
  return (n === 8 || n === 11 ? "dall'" : 'dal ') + soloGiorno(iso);
}

/* Scaduto e «non ancora cominciato» si decidono QUI, a ogni apertura, contro
   la data del telefono di chi guarda — non a tavolino quando la pagina viene
   fatta. Cosi una pagina lasciata li una settimana non spaccia per buone le
   offerte finite nel frattempo: al massimo non ne ha di nuove. */
const OGGI_ISO = new Date().toLocaleDateString('sv');   // «2026-09-05»
const futuro  = x => !!x.inizio && x.inizio > OGGI_ISO;
const scaduto = x => !!x.fino   && x.fino   < OGGI_ISO;

/* «2026-09-09» -> «9 settembre». Le date su ogni riga servono perche i
   volantini durano periodi diversi: senza, guardando un prezzo non si sa se
   vale ancora domani o per altre due settimane. Chiesto da Manlio. */
function durata(o) {
  if (futuro(o))  return 'vale ' + giorno(o.inizio) + (o.fino ? ' al ' + soloGiorno(o.fino) : '');
  if (o.fino)     return 'fino al ' + soloGiorno(o.fino);
  return '';
}

/* UN'OFFERTA CHE DURA MENO DEL SUO VOLANTINO SI VEDE SOLO NEI GIORNI IN CUI
   VALE. Nel volantino MD dell'8-20 settembre c'e una pagina valida solo dal 18
   al 21: mostrarla prima vorrebbe dire mandare Manlio in negozio a chiedere un
   prezzo che non gli fanno. Un VOLANTINO INTERO non ancora cominciato invece
   resta visibile con «vale dal»: quello e voluto, serve a sapere cosa arriva.
   La differenza e che li e tutto il volantino, e si vede. */
/* I SUPERMERCATI TOLTI (Manlio, 2026-09-22 notte: «ci dovrebbe essere anche
   un tasto per scegliere i supermercati: appare l'elenco completo e tu
   scegli quello che vuoi»). Si ricordano quelli TOLTI, non quelli tenuti:
   un'insegna nuova, messa dopo, compare da sola a tutti. La scelta sta nel
   telefono di chi guarda: Manlio e sua moglie possono tenere negozi diversi.
   Un'offerta di un negozio tolto e nascosta come una scaduta, quindi sparisce
   dappertutto (prezzi, «il meno caro», ricerca, grandi marche) senza altro. */
const NEGOZI_TOLTI = 'spesa.negozi.v1';
let tolti = [];
try { tolti = JSON.parse(localStorage.getItem(NEGOZI_TOLTI) || '[]') || []; } catch (e) { tolti = []; }
if (!Array.isArray(tolti)) tolti = [];
const tolta = ins => tolti.indexOf(ins) >= 0;
const nascosta = o => tolta(o.ins) || scaduto(o) || (o.ristretta && futuro(o));

/* IN ORDINE DI PREZZO E BASTA, dal 2026-09-05.
   Prima le offerte dei volantini non ancora cominciati venivano spinte in
   fondo, qualunque prezzo avessero. Manlio se n'e accorto: «quando si
   aggiungono nuove cose vanno in fondo anche se hanno un prezzo piu basso,
   dovrebbero proprio essere in ordine di prezzo». Ha ragione: un elenco
   ordinato per prezzo che poi non lo e in fondo non e un elenco ordinato, e
   il prezzo piu basso finiva dove nessuno lo guarda.
   Il «da quando vale» non si perde: resta il bollo rosso sulla riga. Quello
   che si sposta e solo dove sta scritta. */
const offerteDi = v => v.cat
  ? DATI.offerte.filter(o => o.cat === v.cat && !nascosta(o))
  : [];

/* «Il meno caro» e il meno caro CHE SI PUO COMPRARE OGGI, non la prima riga.
   Con l'ordine per prezzo la prima riga puo essere di un volantino che parte
   fra una settimana: dargli il bollo verde vorrebbe dire mandare Manlio in
   negozio a chiedere un prezzo che non gli fanno ancora — e lasciare senza
   bollo l'offerta che invece stasera gli farebbero. */
const menoCaroOggi = off => off.find(o => !futuro(o));

/* LA RIGA IN CIMA A OGNI PRODOTTO, SOLO QUANDO SERVE (Manlio, 2026-09-23,
   punto 3 dell'analisi esterna: «va bene la prima», cioè la riga che compare
   solo quando dice qualcosa che dall'elenco non si capisce al primo sguardo).
   Compare solo quando il meno caro di OGGI è dalla quarta scheda in giù
   (sopra ci sono offerte che partono nei prossimi giorni), e dice:
   - «Oggi il meno caro: MD, 16,90 € al kg»;
   - se un'offerta PIÙ conveniente parte nei prossimi giorni, anche «Da
     domani conviene di più: Conad, 9,90 € al kg».
   Se il meno caro di oggi è fra le prime tre schede, la riga NON c'è: il 2026-09-22 un riquadro che ripeteva la scheda
   verde era stato tolto dopo mezz'ora. Toccando una riga la pagina scende
   alla sua scheda. Il confronto è sui numeri come si leggono (eur). */
const SETTIMANA = 'domenica lunedì martedì mercoledì giovedì venerdì sabato'.split(' ');
function quandoParte(iso) {
  const d0 = new Date(OGGI_ISO + 'T12:00:00'), d1 = new Date(iso + 'T12:00:00');
  const n = Math.round((d1 - d0) / 86400000);
  if (n === 1) return 'domani';
  if (n === 2) return 'dopodomani';
  return SETTIMANA[d1.getDay()] + ' ' + d1.getDate();
}
function sintesi(off, meno, schede) {
  const prima = off.find(o => futuro(o));
  const piuBasso = (a, b) => parseFloat(eur(a.unitario).replace(',', '.')) < parseFloat(eur(b.unitario).replace(',', '.'));
  /* SOLO SE LA SCHEDA VERDE NON È FRA LE PRIME TRE (Manlio, 2026-09-23:
     «metterei quella barra solo quando il prezzo più conveniente non è fra i
     primi tre»): se è la prima, la seconda o la terza si vede già senza
     scorrere. E senza un meno caro di oggi niente barra: la prima scheda è
     già l'offerta che arriva. */
  const pos = meno ? off.indexOf(meno) : -1;
  if (pos < 3) return null;
  const righe = [['oggi', meno, 'Oggi il meno caro']];
  if (prima && piuBasso(prima, meno)) {
    const q = quandoParte(prima.inizio);
    righe.push(['dopo', prima, 'Da ' + q + (meno ? ' conviene di più' : '')]);
  }
  if (!righe.length) return null;
  const box = document.createElement('div');
  box.className = 'sintesi';
  for (const [tipo, o, testo] of righe) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'sint ' + tipo;
    b.innerHTML = '<span class="cosa"></span> <b></b><span class="freccia" aria-hidden="true">\u2193</span>';
    b.querySelector('.cosa').textContent = testo + ':';
    b.querySelector('b').textContent = o.ins + ', ' + eur(o.unitario) + ' € ' + (DATI.unita[o.cat] || 'al kg');
    b.onclick = () => {
      const el = schede.get(o);
      if (!el) return;
      const meta = Math.max(0, el.getBoundingClientRect().top + (window.scrollY || 0) - altaFissa() - 10);
      try { window.scrollTo({ top: meta, behavior: 'smooth' }); } catch (e) { window.scrollTo(0, meta); }
    };
    box.appendChild(b);
  }
  return box;
}

/* Le pagine dei volantini dove compare almeno uno dei nomi del prodotto.
   Se non ha nomi alternativi si cerca il nome stesso. */
/* PAROLE INTERE, NON PEZZI DI PAROLA.
   Prima si guardava se il termine comparisse dentro il testo della pagina, in
   qualunque posizione: «oro» (di Oro Saiwa) lo trovava dentro «loro», «cola»
   dentro «piccola», «anca» dentro «bianca». Manlio se n'è accorto da fuori:
   «per pizza surgelata appaiono pagine nelle quali la pizza non c'entra
   niente». Quarantacinque pagine su sessantanove erano rumore, per i biscotti.

   E si tiene conto di QUANTE parole ha preso ogni pagina: una che ne ha tre
   parla davvero di quel prodotto, una che ne ha una può essere una ricetta che
   nomina la pizza di sfuggita. Le migliori vanno in cima, e ogni riga dice
   quali parole ha trovato, così si giudica invece di indovinare. */
const pagineDi = v => {
  const termini = (v.parole && v.parole.length ? v.parole : [v.nome]).map(norm);
  return DATI.pagine
    .map(p => {
      const dentro = new Set(norm(p.parole).split(' '));
      const prese = termini.filter(t => dentro.has(t));
      return prese.length ? { ...p, prese } : null;
    })
    .filter(Boolean)
    .sort((a, b) => b.prese.length - a.prese.length);
};

/* tutti i nomi di un prodotto: quello sul bottone piu gli altri con cui cercarlo */
function nomiDi(v) {
  const out = [v.nome];
  (v.parole || []).forEach(p => { if (norm(p) !== norm(v.nome)) out.push(p); });
  return out;
}

/* Un prodotto si puo chiamare in piu modi, e il volantino ne usa uno solo:
   «detersivo» o «lavatrice», «carne di bue» o «bovino». Qui si scrivono tutti,
   separati da virgola, e la pagina cerca le pagine dove compare ALMENO UNO.
   Il primo nome e quello che si legge sul bottone, gli altri lavorano sotto.
   Se uno dei nomi e gia noto (uno dei dodici di partenza, o una delle sue
   parole), si porta dietro anche i prezzi letti a mano e le sue parole. */
function costruisci(testo) {
  const termini = testo.split(/[,;]+/).map(x => x.trim()).filter(Boolean);
  if (!termini.length) return null;
  let seme = null;
  for (const t of termini) {
    const n = norm(t);
    seme = DATI.catalogo.find(x => norm(x.nome) === n || (x.parole || []).some(w => norm(w) === n));
    if (seme) break;
  }
  const parole = [];
  for (const p of termini.concat(seme ? seme.parole : [])) {
    if (!parole.some(x => norm(x) === norm(p))) parole.push(p);
  }
  return { nome: maiuscola(termini[0]), parole, cat: seme ? seme.nome : null };
}

/* ---------- barra dei prodotti ---------- */
function disegnaTasti() {
  const box = document.getElementById('tasti');
  box.textContent = '';
  lista.forEach((v, i) => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'tasto'; b.textContent = v.nome;
    b.setAttribute('aria-pressed', String(i === scelto));
    b.onclick = () => {
      const cambiato = scelto !== i;
      scelto = i; tutteLePagine = false;
      if (cassettoAperto) apriCassetto(false);
      disegna();
      if (cambiato) inCima();
    };
    box.appendChild(b);
  });
  const piu = document.createElement('button');
  piu.type = 'button'; piu.className = 'tasto agg';
  piu.textContent = cassettoAperto ? 'Chiudi' : '+ altri prodotti';
  piu.setAttribute('aria-expanded', String(cassettoAperto));
  piu.setAttribute('aria-controls', 'cassetto');
  piu.onclick = () => { apriCassetto(!cassettoAperto); };
  box.appendChild(piu);

  /* «Cerca fra i prezzi» e un'altra cosa dal cassetto, e vanno tenute
     separate. Il cassetto sceglie QUALI PRODOTTI stanno nella lista, e cerca
     fra le 67 voci del catalogo. Questa cerca fra le OFFERTE vere, tutte,
     anche di prodotti che in lista non ci sono e magari non ci vanno: uno
     vuole sapere quanto costa quella marca li, una volta sola, senza
     accendersi un bottone per sempre. Chiesto da Manlio il 2026-09-15,
     quando i prezzi erano diventati milleduecento. */
  const cer = document.createElement('button');
  /* Tiene anche «agg»: e la classe con cui tutte le prove riconoscono i
     bottoni che NON sono prodotti della lista. Toglierla lo farebbe contare
     come un prodotto in mezzo agli altri. Il rosso arriva da «.tasto.trova»,
     scritto dopo «.tasto.agg» nel foglio di stile, e vince lui. */
  cer.type = 'button'; cer.className = 'tasto agg trova';
  /* LA SCRITTA DEL TASTO ROSSO, scelta da Manlio il 2026-09-22 fra tre:
     «Cerca un prodotto o una marca». Prima diceva «Cerca fra i prezzi di
     tutte le offerte», che spiegava meglio la differenza col cassetto ma era
     lunga il doppio e costringeva la pastiglia a due righe sul telefono.
     Quello che si perde — che cerca fra TUTTE le offerte lette, non fra i
     prodotti della lista — resta scritto nell'Aiuto e nella casella che si
     apre («Scrivi un prodotto, una marca, un negozio…»). */
  /* Le due pagine sono separate (Manlio, 2026-09-23): il tasto rosso apre
     SOLO la ricerca, GRANDI MARCHE SOLO le marche. Col pannello delle marche
     aperto, il rosso passa alla ricerca invece di chiudere. */
  const cercaAperta = ricercaAperta && !vistaMarche;
  /* Solo «Cerca», con la lente (Manlio, 2026-09-23). Aperta resta «Cerca»,
     rossa piena: non «Chiudi la ricerca». */
  cer.textContent = 'Cerca';
  cer.setAttribute('aria-expanded', String(cercaAperta));
  cer.setAttribute('aria-pressed', String(cercaAperta));
  cer.setAttribute('aria-controls', 'ricerca');
  /* Toccato quando si è già nella ricerca, resta lì e torna in cima: è una
     sezione, non un interruttore (Manlio, 2026-09-23, i tre tasti). */
  cer.onclick = () => {
    if (cercaAperta) { suInCima(); return; }
    if (personaleAperto) apriPersonale(false);
    vistaMarche = false; marcaScelta = null;
    document.getElementById('q').value = '';
    apriRicerca(true);
    suInCima();
  };
  /* Sta SOPRA i prodotti e FUORI dalla barra appiccicata, come nella
     schermata che ha mandato Manlio il 2026-09-22: è la prima cosa che si
     vede, e la barra resta bassa. */
  /* I TRE TASTI DELLE SEZIONI (Manlio, 2026-09-23: «i tasti diventano tre e
     ognuno porta alla sua sezione, e quando si è nella sua sezione diventa
     colorato»). «Prodotti» è la pagina principale, con le pillole: è acceso
     finché non si è nella ricerca o nelle marche. Tiene «agg» come gli altri
     due, così le prove non lo contano fra i prodotti. */
  const suo = document.getElementById('riga-cerca');
  suo.textContent = '';
  const pro = document.createElement('button');
  pro.type = 'button';
  pro.className = 'tasto agg sez';
  pro.id = 'vai-prodotti';
  pro.textContent = 'Prodotti';
  pro.setAttribute('aria-pressed', String(!ricercaAperta && !personaleAperto));
  pro.onclick = vaiInizio;
  suo.appendChild(pro);
  suo.appendChild(cer);
  const gm = document.createElement('button');
  gm.type = 'button';
  gm.className = 'tasto agg marchi';
  /* Con le minuscole dal 2026-09-23: in un terzo di schermo, tutto
     maiuscolo non ci stava. */
  /* SEMPRE SU DUE RIGHE, «Grandi» sopra e «marche» sotto (Manlio,
     2026-09-23: «mi sembra davvero schiacciata, meglio su due righe»). Prima
     andava a capo solo sotto i 420 px; sui telefoni più larghi stava su una
     riga, stretta fra i bordi tondi. Lo spazio fra le due parti resta, così
     chi legge il testo (e le prove) trova ancora «Grandi marche». */
  gm.innerHTML = '<span class="riga-gm">Grandi</span> <span class="riga-gm">marche</span>';
  gm.setAttribute('aria-pressed', String(ricercaAperta && vistaMarche));
  gm.onclick = () => {
    if (ricercaAperta && vistaMarche) { suInCima(); return; }
    if (personaleAperto) apriPersonale(false);
    vistaMarche = true;
    marcaScelta = null;
    filtroVol = null;
    document.getElementById('q').value = '';
    apriRicerca(true, true);
    suInCima();
  };
  suo.appendChild(gm);
  /* «Personale», il quarto (Manlio, 2026-09-23): le sue parole e le loro
     offerte. Anche lui è una sezione: ritoccato non chiude. */
  const per = document.createElement('button');
  per.type = 'button';
  per.className = 'tasto agg sez';
  per.id = 'vai-personale';
  per.textContent = 'Personale';
  per.setAttribute('aria-pressed', String(personaleAperto));
  per.onclick = () => { if (!personaleAperto) apriPersonale(true); suInCima(); };
  suo.appendChild(per);

  const cont = document.getElementById('quanti-prodotti');
  if (cont) cont.textContent = 'I tuoi prodotti (' + lista.length + ')';
  sistemaBarra();
}

/* LE PILLOLE DEI PRODOTTI RESTANO FERME IN ALTO, SE SONO POCHE (Manlio,
   2026-09-23: «dato che la parte superiore è molto diminuita è inutile far
   salire in alto l'elenco dei prodotti, perché già si vedono; al limite la
   parte superiore, se non ci sono troppi prodotti, potrebbe rimanere
   fissa»). Sotto la striscia dei quattro tasti, finché non occupano più di
   un terzo dello schermo: con tanti prodotti le pillole si mangerebbero le
   offerte, e allora scorrono via come prima. */
function sistemaBarra() {
  const barra = document.querySelector('.barra');
  const striscia = document.getElementById('riga-cerca');
  if (!barra || !striscia) return;
  barra.classList.remove('fissa');
  barra.style.top = '';
  if (barra.hidden) return;
  const alta = barra.getBoundingClientRect().height;
  const schermo = window.innerHeight || 0;
  if (alta > 0 && schermo > 0 && alta <= schermo / 3) {
    /* Dal 2026-09-23 i tasti delle sezioni stanno IN BASSO: le pillole
       ferme stanno proprio in cima, a zero. */
    barra.classList.add('fissa');
    barra.style.top = '0px';
  }
}
window.addEventListener('resize', () => { try { sistemaBarra(); } catch (e) {} });

/* IL CASSETTO. Chiesto da Manlio il 2026-09-05: scrivere il nome di un
   prodotto per aggiungerlo era scomodo, e chi non ero io non poteva farlo.
   Adesso c'e un catalogo gia pronto, diviso per reparto come il negozio, e
   ognuno accende i suoi. La fila dei bottoni in cima resta identica: chi non
   tocca «+ altri prodotti» non si accorge nemmeno che il catalogo esiste. */
let cassettoAperto = false;

function apriCassetto(si) {
  cassettoAperto = si;
  if (si && personaleAperto) apriPersonale(false);
  if (si && ricercaAperta) apriRicerca(false);   // uno alla volta
  const c = document.getElementById('cassetto');
  c.hidden = !si;
  /* Col cassetto aperto l'elenco dei prezzi di prima non c'entra più niente e
     stava lì sotto a confondere: Manlio l'ha visto subito. Torna quando si
     chiude, sul prodotto che nel frattempo si è acceso. */
  document.getElementById('risultato').hidden = si;
  disegnaTasti();
  /* Niente focus sulla casella: aprendo il cassetto faceva saltare su la
     tastiera del telefono, che copre mezzo schermo proprio mentre uno vuole
     guardarsi i reparti. Chi vuole cercare la tocca. */
  if (si) disegnaScaffali();
  else document.getElementById('cerca').value = '';
}

/* ---------- la sezione personale ---------- */
/* Chiesta da Manlio il 2026-09-23: «una sezione personale: si scrivono delle
   parole e col tasto Aggiungi diventano pillole che restano lì; in basso le
   offerte per questi prodotti, con davanti il nome; all'inizio solo il più
   conveniente per ciascuno, premendo il tasto tutte le offerte; e un tasto
   Personalizza supermercati che vale solo per questa sezione». E: «una
   versione personale per ogni telefonino». Per questo le parole e i
   supermercati tolti stanno in localStorage, sul telefono di chi li sceglie,
   come la scelta dei negozi generale: nessuno vede quelle degli altri. */
const PAROLE_PERS = 'spesa.personale.v1';
const NEGOZI_PERS = 'spesa.personale.negozi.v1';
let personaleAperto = false;
let parolePers = [];
let toltiPers = [];
let aperte = [];          // le parole di cui si vedono tutte le offerte
try { parolePers = JSON.parse(localStorage.getItem(PAROLE_PERS) || '[]') || []; } catch (e) { parolePers = []; }
try { toltiPers = JSON.parse(localStorage.getItem(NEGOZI_PERS) || '[]') || []; } catch (e) { toltiPers = []; }
if (!Array.isArray(parolePers)) parolePers = [];
if (!Array.isArray(toltiPers)) toltiPers = [];

function salvaPers() {
  try { localStorage.setItem(PAROLE_PERS, JSON.stringify(parolePers)); } catch (e) {}
  try { localStorage.setItem(NEGOZI_PERS, JSON.stringify(toltiPers)); } catch (e) {}
}

/* Le offerte di una parola: la stessa ricerca del tasto «Cerca» (tutte le
   parole scritte devono esserci), meno i supermercati tolti qui. */
function offertePers(parola) {
  const parole = norm(parola).split(/\s+/).filter(x => x.length > 1);
  if (!parole.length) return [];
  return DATI.offerte
    .filter(o => !nascosta(o) && toltiPers.indexOf(o.ins) < 0)
    .filter(o => {
      const pagliaio = norm([o.pro, o.ins, o.cat, o.fmt, o.note].join(' '));
      return parole.every(w => pagliaio.indexOf(w) >= 0);
    })
    .sort((a, b) => a.unitario - b.unitario);
}

/* IL PIÙ CONVENIENTE DI UNA PAROLA. I prezzi per unità si confrontano solo
   dentro lo stesso reparto: «tonno» trova il tonno al kg ma anche la pizza
   al tonno al pezzo, e 3 euro al pezzo non è «meno caro» di 9 al kg. Quindi
   si prende il reparto con più offerte per quella parola, e lì la meno cara
   che si può comprare OGGI (una che parte lunedì non manda nessuno in
   negozio stasera). Se oggi non ce n'è, la meno cara in assoluto. */
function piuConveniente(off) {
  if (!off.length) return null;
  const conta = {};
  off.forEach(o => { conta[o.cat] = (conta[o.cat] || 0) + 1; });
  const cat = Object.keys(conta).sort((a, b) => conta[b] - conta[a])[0];
  const dentro = off.filter(o => o.cat === cat);
  return dentro.find(o => !futuro(o)) || dentro[0];
}

function apriPersonale(si) {
  if (si) {
    if (ricercaAperta) apriRicerca(false);
    if (cassettoAperto) apriCassetto(false);
  }
  personaleAperto = si;
  document.getElementById('personale').hidden = !si;
  document.getElementById('risultato').hidden = si || ricercaAperta || cassettoAperto;
  if (!si) {
    document.getElementById('negozi-pers-box').hidden = true;
    document.getElementById('apri-negozi-pers').setAttribute('aria-expanded', 'false');
  }
  disegnaTasti();
  disegnaMarche();
  if (si) disegnaPersonale();
}

function disegnaPersonale() {
  const box = document.getElementById('pillole-pers');
  box.textContent = '';
  parolePers.forEach(w => {
    const p = document.createElement('span');
    p.className = 'pillola-pers' + (aperte.indexOf(w) >= 0 ? ' aperta' : '');
    const n = document.createElement('button');
    n.type = 'button'; n.className = 'nome-pers'; n.textContent = w;
    n.title = 'Tutte le offerte di «' + w + '»';
    /* Toccando la pillola si aprono tutte le sue offerte, e la pagina ci va. */
    /* UNA APERTA ALLA VOLTA (Manlio, 2026-09-23: «i tasti sono rimasti tutti
       rossi»): ogni pillola toccata restava rossa, e dopo qualche tocco lo
       erano tutte. Adesso toccarne una chiude le altre, e rossa è solo lei. */
    n.onclick = () => {
      aperte = [w];
      disegnaPersonale();
      const b = [...document.querySelectorAll('.blocco-pers')].find(x => x.dataset.parola === w);
      if (b && b.scrollIntoView) b.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };
    const x = document.createElement('button');
    x.type = 'button'; x.className = 'via-pers'; x.textContent = '\u00d7';
    x.setAttribute('aria-label', 'Togli «' + w + '»');
    x.onclick = () => {
      parolePers = parolePers.filter(y => y !== w);
      aperte = aperte.filter(y => y !== w);
      salvaPers(); disegnaPersonale();
    };
    p.appendChild(n); p.appendChild(x);
    box.appendChild(p);
  });

  const out = document.getElementById('riepilogo-pers');
  out.textContent = '';
  if (!parolePers.length) {
    out.innerHTML = '<p class="vuoto-pers">Scrivi qui sopra un prodotto o una marca '
      + '(per esempio <i>tonno</i>, <i>mozzarella</i>, <i>Barilla</i>) e tocca '
      + '«Aggiungi»: diventa una pillola, e qui sotto trovi la sua offerta più '
      + 'conveniente. Le parole restano su questo telefono.</p>';
    return;
  }
  parolePers.forEach(w => {
    const off = offertePers(w);
    const b = document.createElement('section');
    b.className = 'blocco-pers';
    b.dataset.parola = w;
    const h = document.createElement('h2');
    h.textContent = w;
    b.appendChild(h);
    if (!off.length) {
      const n = document.createElement('p');
      n.className = 'nulla';
      n.textContent = 'Nessuna offerta adesso, nei supermercati scelti.';
      b.appendChild(n);
      out.appendChild(b);
      return;
    }
    const tutte = aperte.indexOf(w) >= 0;
    /* Niente bollino verde nemmeno qui: vorrebbe dire «il meno caro della
       categoria», e questo è il meno caro di una parola scritta a mano. */
    (tutte ? off : [piuConveniente(off)]).forEach(o => b.appendChild(rigaPrezzo(o, false)));
    if (off.length > 1) {
      const t = document.createElement('button');
      t.type = 'button'; t.className = 'altre';
      t.textContent = tutte ? 'Mostra solo la più conveniente'
                            : 'Mostra tutte le ' + off.length + ' offerte';
      t.onclick = () => {
        aperte = tutte ? [] : [w];
        disegnaPersonale();
      };
      b.appendChild(t);
    }
    out.appendChild(b);
  });
}

function disegnaNegoziPers() {
  const box = document.getElementById('negozi-pers');
  box.textContent = '';
  document.getElementById('avviso-negozi-pers').textContent = '';
  /* Solo i supermercati tenuti nella configurazione generale: uno tolto là
     non ha niente da mostrare nemmeno qui. */
  const insegne = [];
  DATI.volantini.forEach(v => { if (insegne.indexOf(v.ins) < 0 && !tolta(v.ins)) insegne.push(v.ins); });
  const via = ins => toltiPers.indexOf(ins) >= 0;
  insegne.forEach(ins => {
    const b = document.createElement('button');
    b.type = 'button';
    b.appendChild(marchio(ins));
    b.setAttribute('aria-pressed', String(!via(ins)));
    b.title = ins;
    b.onclick = () => {
      if (!via(ins) && insegne.filter(x => !via(x)).length <= 1) {
        document.getElementById('avviso-negozi-pers').textContent =
          'Almeno un supermercato deve restare.';
        return;
      }
      toltiPers = via(ins) ? toltiPers.filter(x => x !== ins) : toltiPers.concat([ins]);
      salvaPers(); disegnaNegoziPers(); disegnaPersonale();
    };
    box.appendChild(b);
  });
}

document.getElementById('form-pers').onsubmit = ev => {
  ev.preventDefault();
  const i = document.getElementById('parola-pers');
  const w = i.value.trim().replace(/\s+/g, ' ');
  if (w.length < 2) return;
  if (!parolePers.some(y => norm(y) === norm(w))) parolePers.push(w);
  i.value = '';
  salvaPers(); disegnaPersonale();
};
document.getElementById('apri-negozi-pers').onclick = () => {
  const box = document.getElementById('negozi-pers-box');
  const apri = box.hidden;
  box.hidden = !apri;
  document.getElementById('apri-negozi-pers').setAttribute('aria-expanded', String(apri));
  if (apri) disegnaNegoziPers();
};

/* ---------- cercare fra tutti i prezzi ---------- */
let ricercaAperta = false;
let quantiMostrati = 40;

/* Con un volantino scelto dai tasti in fondo, lo stesso pannello mostra le
   offerte di QUEL volantino invece dei risultati di una parola. E lo stesso
   pannello apposta: e gia fuori dalla barra (se cresce dentro la barra il
   telefono si pianta a ogni scorrimento) e le sue righe non portano il
   bollino verde, che qui vorrebbe dire «il meno caro di questo negozio» e si
   leggerebbe «il meno caro di tutti». */
let filtroVol = null;
const SCRITTA_Q = document.getElementById('q').placeholder;

function apriRicerca(si, senzaFuoco) {
  if (si && personaleAperto) apriPersonale(false);
  ricercaAperta = si;
  if (!si) { vistaMarche = false; marcaScelta = null; }
  if (si && cassettoAperto) apriCassetto(false);
  document.getElementById('ricerca').hidden = !si;
  /* Col pannello aperto l'elenco di prima non c'entra piu niente e sta li a
     confondere, come per il cassetto. */
  document.getElementById('risultato').hidden = si;
  disegnaTasti();
  disegnaMarche();
  if (si) {
    quantiMostrati = 40;
    disegnaTrovati();
    /* QUI il fuoco sulla casella CI VA, al contrario del cassetto. La regola
       del 2026-09-05 («niente focus, la tastiera copre mezzo schermo») valeva
       per chi apre il cassetto per GUARDARSI i reparti. Qui uno ha appena
       toccato «Cerca»: vuole scrivere, e fargli fare un secondo tocco sulla
       casella e solo una seccatura.
       ECCEZIONE: quando il pannello si apre da solo per mostrare un volantino
       intero non c'e niente da scrivere, e la tastiera coprirebbe le offerte
       appena arrivate. */
    if (!senzaFuoco) { try { document.getElementById('q').focus(); } catch (e) {} }
  } else {
    document.getElementById('q').value = '';
    document.getElementById('q').placeholder = SCRITTA_Q;
    filtroVol = null;
    vistaMarche = false;
    marcaScelta = null;
    /* Via la coda «#volantino=...» dall'indirizzo: se no chi ricarica questa
       scheda dopo aver chiuso il pannello se lo ritrova aperto. */
    if (location.hash) {
      try { history.replaceState(null, '', location.pathname + location.search); } catch (e) {}
    }
  }
}

/* Apre il pannello sulle offerte di un volantino solo. Lo chiamano i tasti in
   fondo (di solito in una scheda nuova) e l'indirizzo con «#volantino=». */
function apriVolantino(pdf) {
  filtroVol = pdf;
  const q = document.getElementById('q');
  q.value = '';
  q.placeholder = 'Cerca dentro questo volantino…';
  apriRicerca(true, true);
}

/* Tutte le parole scritte devono comparire da qualche parte nella riga: cosi
   «tonno rio» trova i Rio Mare e «mozzarella bennet» solo quelle del Bennet.
   Qui si cerca dentro le parole, non a parola intera come nell'indice delle
   pagine: li il testo veniva dall'OCR ed era pieno di rumore, qui sono nomi di
   prodotto scritti a mano, e chi scrive «mozzar» si aspetta di trovarli. */
let vistaMarche = false;   // il pannello e' aperto dal tasto GRANDI MARCHE
let marcaScelta = null;   // la pillola accesa: si cerca a parola intera

function disegnaMarche() {
  const box = document.getElementById('marche');
  box.hidden = !vistaMarche;
  /* NELLA PAGINA DELLE MARCHE NON C'È LA CASELLA (Manlio, 2026-09-23: «deve
     portare a una pagina dove ci sono solo i tasti delle grandi marche e non
     un tasto di ricerca; l'altro ha una pagina dove c'è solo la ricerca»). La
     casella resta nascosta e ci si scrive dentro il nome della marca toccata:
     è così che si cercano le sue offerte. */
  document.getElementById('q').hidden = vistaMarche && ricercaAperta;
  /* CON LE GRANDI MARCHE APERTE LE CATEGORIE NON SI VEDONO (Manlio,
     2026-09-22: «quando c'è grandi marche ci sono anche le categorie, non ha
     senso, non devono apparire»). Si cerca per marca, non per prodotto: le
     pastiglie dei prodotti li in mezzo erano solo rumore. Tornano appena si
     chiude il pannello. */
  /* Col pannello aperto (ricerca, grandi marche o un volantino) non si
     vedono né le categorie né, in fondo, le spiegazioni e l'elenco dei
     volantini (Manlio, 2026-09-23: prima solo con le grandi marche). */
  document.querySelector('.barra').hidden = ricercaAperta || personaleAperto;
  document.querySelector('.spiega').hidden = ricercaAperta || personaleAperto;
  sistemaBarra();   // le pillole ricompaiono: vanno rimesse ferme se sono poche
  box.textContent = '';
  if (!vistaMarche) return;
  (DATI.marche || []).forEach(m => {
    const b = document.createElement('button');
    b.type = 'button';
    const logo = (DATI.marchiMarche || {})[m];
    if (logo) {
      /* Il marchio al posto del nome, e il nome dentro, nascosto alla vista:
         un logo, per chi non lo vede, e un buco. */
      b.className = 'col-logo';
      b.innerHTML = '<img alt=""><span class="solo-voce"></span>';
      b.querySelector('img').src = logo;
      b.querySelector('.solo-voce').textContent = m;
      b.title = m;
    } else {
      b.textContent = m;
    }
    b.setAttribute('aria-pressed', String(marcaScelta === m));
    if (!cercaMarca(m).length) {
      b.disabled = true;
      b.title = 'Nei volantini di adesso non c\'è nessuna offerta ' + m;
    }
    b.onclick = () => {
      marcaScelta = marcaScelta === m ? null : m;
      document.getElementById('q').value = marcaScelta || '';
      quantiMostrati = 40;
      disegnaMarche();
      disegnaTrovati();
      /* LA PAGINA SCORRE AI RISULTATI (Manlio, 2026-09-22: «quando si fa clic
         su un grande marchio, la pagina scrolli per far vedere in alto i
         risultati»). Le 46 pillole occupano uno schermo intero: senza questo,
         toccata una marca, le offerte restavano sotto, fuori vista. */
      const capo = document.getElementById('quanti-trovati');
      if (marcaScelta && capo.scrollIntoView)
        capo.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };
    box.appendChild(b);
  });
}

function cercaMarca(m) {
  /* I nomi delle marche sono solo lettere, spazi e apostrofi: niente da
     proteggere dentro l'espressione. */
  const re = new RegExp('(^|[^a-z0-9])' + norm(m) + '($|[^a-z0-9])');
  return DATI.offerte
    .filter(o => !nascosta(o))
    .filter(o => re.test(norm([o.pro, o.fmt, o.note].join(' '))))
    .sort((a, b) => a.unitario - b.unitario);
}

function cercaOfferte(testo) {
  if (marcaScelta && testo === marcaScelta) return cercaMarca(marcaScelta);
  const parole = norm(testo).split(/\s+/).filter(x => x.length > 1);
  if (!parole.length && !filtroVol) return [];
  return DATI.offerte
    .filter(o => !nascosta(o))
    .filter(o => !filtroVol || o.pdf === filtroVol)
    .filter(o => {
      const pagliaio = norm([o.pro, o.ins, o.cat, o.fmt, o.note].join(' '));
      return parole.every(w => pagliaio.indexOf(w) >= 0);
    })
    .sort((a, b) => a.unitario - b.unitario);
}

function disegnaTrovati() {
  const testo = document.getElementById('q').value;
  const box = document.getElementById('trovati');
  const capo = document.getElementById('quanti-trovati');
  box.textContent = '';
  const parole = norm(testo).split(/\s+/).filter(x => x.length > 1);
  if (!parole.length && !filtroVol && vistaMarche) {
    capo.innerHTML = 'Tocca una marca: escono tutte le sue offerte, dalla meno cara in giù.';
    return;
  }
  /* Con la casella vuota (o una lettera sola) sotto non si scrive niente
     (Manlio, 2026-09-23: «la scritta sotto la finestra non è necessaria»). */
  if (!parole.length && !filtroVol) {
    capo.textContent = '';
    return;
  }
  const trovate = cercaOfferte(testo);
  if (!trovate.length) {
    /* Senza parola scritta e senza offerte il volantino e finito: dirlo com'e,
       invece di far credere che sia colpa di come uno ha cercato. */
    capo.innerHTML = filtroVol
      ? (parole.length
         ? '<b>Niente.</b> In questo volantino non c\u2019e nessuna offerta con questa '
           + 'parola. Cancellala e tornano tutte.'
         : '<b>Questo volantino e finito.</b> Le sue offerte non valgono piu: '
           + 'guarda quelle dei volantini in corso.')
      : '<b>Niente.</b> Prova con una parola sola, o piu corta: '
        + 'i nomi sono quelli stampati sul volantino, non sempre quelli che diresti tu.';
    return;
  }
  /* Niente bollino verde qui dentro. «Il meno caro» vuol dire il meno caro
     della sua categoria, e in un elenco di risultati direbbe una cosa falsa:
     cercando «tonno rio mare» il primo sarebbe il Rio Mare meno caro, non il
     tonno meno caro. Una novita falsa manda uno in negozio. Per il confronto
     vero c'e il bottone del prodotto. */
  capo.innerHTML = '';
  if (filtroVol) {
    /* Col volantino scelto il titolo deve dire QUALE, se no uno non sa cosa
       sta guardando: di Lidl ce ne sono due validi insieme, e di Bennet pure. */
    const v = DATI.volantini.find(x => x.pdf === filtroVol);
    const b = document.createElement('b');
    b.textContent = v ? v.ins + ' — ' + v.periodo : 'questo volantino';
    capo.appendChild(b);
    capo.appendChild(document.createTextNode(': ' + trovate.length
      + (trovate.length === 1 ? ' offerta' : ' offerte')
      + (parole.length ? ' con questa parola' : '')
      + ', divise per reparto e dalla meno cara in giù dentro ognuno. Sono solo quelle '
      + 'di questo volantino: per sapere qual è il meno caro fra tutti i negozi tocca '
      + 'il bottone del prodotto.'));
  } else {
    /* Nessuna scritta sotto la casella: le offerte parlano da sole (Manlio,
       2026-09-23: «la scritta sotto la finestra non è necessaria e si
       toglie»). Resta solo quella del volantino, che dice QUALE volantino. */
    capo.textContent = '';
  }

  /* Raggruppate per categoria, e le categorie in ordine di prezzo migliore:
     cercando «barilla» esce prima la pasta e poi i sughi, non alla rinfusa. */
  const gruppi = [];
  trovate.slice(0, quantiMostrati).forEach(o => {
    const c = o.cat || '—';
    let g = gruppi.find(x => x.cat === c);
    if (!g) { g = { cat: c, righe: [] }; gruppi.push(g); }
    g.righe.push(o);
  });
  gruppi.forEach(g => {
    const f = document.createElement('p');
    f.className = 'fascia';
    f.textContent = g.cat;
    box.appendChild(f);
    g.righe.forEach(o => box.appendChild(rigaPrezzo(o, false)));
  });
  if (trovate.length > quantiMostrati) {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'altre';
    b.textContent = 'Mostra le altre ' + (trovate.length - quantiMostrati) + ' offerte';
    b.onclick = () => { quantiMostrati = trovate.length; disegnaTrovati(); };
    box.appendChild(b);
  }
}

function inLista(nome) {
  return lista.some(v => norm(v.nome) === norm(nome) || norm(v.cat || '') === norm(nome));
}

function accendi(nome) {
  const voce = DATI.catalogo.find(x => x.nome === nome);
  if (!voce) return;
  if (inLista(nome)) {
    /* Spegnendo si toglie sia il prodotto col suo nome sia quello che punta a
       quella categoria con un nome diverso: se no il bottone resta li. */
    lista = lista.filter(v => norm(v.nome) !== norm(nome) && norm(v.cat || '') !== norm(nome));
    if (scelto >= lista.length) scelto = Math.max(0, lista.length - 1);
  } else {
    lista.push({ nome: voce.nome, parole: voce.parole.slice(), cat: voce.nome });
    scelto = lista.length - 1;
    tutteLePagine = false;
  }
  salva(); disegnaScaffali(); disegna();
}

function disegnaScaffali() {
  const box = document.getElementById('scaffali');
  const cerca = document.getElementById('cerca');
  const filtro = norm(cerca ? cerca.value.trim() : '');
  box.textContent = '';
  /* Tutto in un mucchietto a parte, e dentro la pagina in un colpo solo: prima
     si infilavano i nove reparti uno per uno, e il telefono rifaceva i conti
     nove volte con la roba che cresceva sotto. Si vedeva: comparivano le prime
     categorie, poi si piantava. */
  const mucchio = document.createDocumentFragment();
  let quanti = 0;
  DATI.reparti.forEach(rep => {
    const voci = DATI.catalogo.filter(v => v.rep === rep && (!filtro
      || norm(v.nome).includes(filtro) || v.parole.some(w => norm(w).includes(filtro))));
    if (!voci.length) return;
    quanti += voci.length;
    const h = document.createElement('p');
    h.className = 'reparto'; h.textContent = rep;
    mucchio.appendChild(h);
    const fila = document.createElement('div');
    fila.className = 'tasti';
    voci.forEach(v => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'tasto'; b.textContent = v.nome;
      b.setAttribute('aria-pressed', String(inLista(v.nome)));
      b.onclick = () => accendi(v.nome);
      fila.appendChild(b);
    });
    mucchio.appendChild(fila);
  });
  box.appendChild(mucchio);
  const f = document.getElementById('fuori-catalogo');
  f.textContent = quanti
    ? 'Non c\u2019\u00e8 quello che cerchi? Scrivilo qui sopra: cerco la parola nelle pagine dei volantini.'
    : 'Nel catalogo non c\u2019\u00e8 niente con questo nome. Scrivilo lo stesso qui sopra: cerco la parola nelle pagine dei volantini.';
}

/* In cima alla pagina. La usano i tre tasti delle sezioni: la striscia coi
   tasti resta attaccata in alto, quindi si possono toccare anche in fondo a
   un elenco, e la sezione nuova deve cominciare dall'inizio. */
function suInCima() {
  try { window.scrollTo(0, 0); } catch (x) {}
}

/* «Prodotti», e il titolo «Spesa»: la pagina principale, dall'inizio. */
function vaiInizio() {
  if (personaleAperto) apriPersonale(false);
  if (ricercaAperta) apriRicerca(false);
  if (cassettoAperto) apriCassetto(false);
  suInCima();
}

/* Quanto è alta la striscia che resta attaccata in alto. Dal 2026-09-23 è
   quella dei tre tasti, non più le pillole dei prodotti. */
function altaFissa() {
  /* Quanto è occupato in cima: solo le pillole, se sono ferme. I tasti delle
     sezioni dal 2026-09-23 stanno in basso (menù in fondo, Manlio: «lo sai
     che mi piace davvero»), e non coprono più niente in alto. */
  const b = document.querySelector('.barra');
  return b && !b.hidden && b.classList.contains('fissa') ? b.getBoundingClientRect().height : 0;
}

/* Cambiando prodotto si torna all'inizio del suo elenco.
   Manlio: scorreva i prezzi del tonno, toccava «Suino», e si ritrovava in
   mezzo alla lista del suino invece che in cima — perche la pagina cambiava
   sotto ma la finestra restava dov'era. Non si torna in cima alla pagina: si
   va al primo prezzo, appena sotto la barra dei bottoni, che resta attaccata
   in alto. Cosi si vede subito quale bottone e acceso e da dove parte
   l'elenco. Se si e gia lassu non si muove niente. */
function inCima() {
  const r = document.getElementById('risultato');
  if (!r) return;
  const alto = altaFissa();
  /* Il taglio a zero va fatto PRIMA del confronto, non dopo: con una meta
     negativa «sono gia sopra?» risponde sempre no, e la pagina chiederebbe di
     scorrere anche stando gia in cima. */
  const meta = Math.max(0, r.getBoundingClientRect().top + (window.scrollY || 0) - alto - 8);
  if ((window.scrollY || 0) <= meta) return;      // gia sopra: fermo dov'e
  try { window.scrollTo({ top: meta, behavior: 'smooth' }); }
  catch (e) { window.scrollTo(0, meta); }
}

/* ---------- il cerchietto dei giorni ---------- */
/* Quanti giorni restano per comprarla, OGGI COMPRESO: se l'offerta finisce
   oggi ne resta uno, non zero. Un «0» su una riga ancora valida si
   leggerebbe «è finita» e farebbe saltare un'offerta buona. */
const UN_GIORNO = 86400000;
const dataDi = iso => Date.parse(iso + 'T00:00:00Z');
function giorniRimasti(o) {
  if (!o.fino) return null;
  const g = Math.round((dataDi(o.fino) - dataDi(OGGI_ISO)) / UN_GIORNO);
  return g < 0 ? null : g + 1;
}
function cerchioGiorni(o) {
  if (futuro(o)) return null;        // non ancora cominciata: la riga lo dice già
  const resta = giorniRimasti(o);
  if (resta === null) return null;
  const inizio = o.inizio && o.inizio <= o.fino ? o.inizio : null;
  const tutti = inizio
    ? Math.round((dataDi(o.fino) - dataDi(inizio)) / UN_GIORNO) + 1
    : Math.max(resta, 14);
  const quota = Math.max(0.06, Math.min(1, resta / tutti));
  const giro = 2 * Math.PI * 16;
  const d = document.createElement('div');
  d.className = 'giorni' + (resta <= 3 ? ' poco' : '');
  d.innerHTML = '<span class="anello">'
    + '<svg viewBox="0 0 38 38" aria-hidden="true" focusable="false">'
    + '<circle class="fondo" cx="19" cy="19" r="16"></circle>'
    + '<circle class="arco" cx="19" cy="19" r="16"'
    + ' stroke-dasharray="' + (giro * quota).toFixed(1) + ' ' + giro.toFixed(1) + '"></circle>'
    + '</svg><span class="num"></span></span><span class="gg"></span>';
  d.querySelector('.num').textContent = String(resta);
  d.querySelector('.gg').textContent = resta === 1 ? 'oggi' : 'giorni';
  d.title = resta === 1
    ? 'Ultimo giorno: scade oggi, ' + soloGiorno(o.fino)
    : 'Restano ' + resta + ' giorni, fino al ' + soloGiorno(o.fino);
  return d;
}

/* Il tondino di quando comincia: il giorno grande dentro, il mese sotto. */
const MESI_CORTI = ('gen feb mar apr mag giu lug ago set ott nov dic').split(' ');
function cerchioInizio(o) {
  if (!o.inizio) return null;
  const p = o.inizio.split('-');
  const d = document.createElement('div');
  d.className = 'parte';
  /* UN CALENDARIETTO, NON UN TONDINO (Manlio, 2026-09-23, punto 4: «va bene
     la tua soluzione del calendarietto»). Il tondino dei giorni che mancano e
     quello del giorno in cui parte avevano la stessa forma e si
     confondevano: adesso questo è un foglietto quadrato con la striscia del
     mese in alto, come i calendari da tavolo. Alto 30 px come il resto. */
  d.innerHTML = '<span class="cal"><span class="mese"></span><span class="num"></span></span>';
  d.querySelector('.num').textContent = String(Number(p[2]));
  d.querySelector('.mese').textContent = MESI_CORTI[Number(p[1]) - 1] || '';
  d.title = 'Non è ancora cominciata: vale ' + giorno(o.inizio);
  return d;
}

/* ---------- righe ---------- */
/* «meno» non vuol dire «prima riga»: e il meno caro fra quelli che valgono
   oggi. Le righe sono in ordine di prezzo, e la prima puo essere di un
   volantino che deve ancora cominciare. */
/* I MARCHI DELLE INSEGNE, disegnati qui: il nome scritto nei colori suoi.
   I marchi veri sono di chi li ha, e questa pagina non li pubblica (come non
   pubblica le pagine dei volantini). Fondo e scritta sono fissati tutti e due,
   quindi la pillola si legge uguale con qualunque look addosso. */
const MARCHI = {
  'Lidl':           ['#0050AA', '#FFFFFF'],
  'Eurospin':       ['#1B4F9C', '#FFFFFF'],
  'MD':             ['#D4001F', '#FFFFFF'],
  'Bennet':         ['#C8102E', '#FFFFFF'],
  'Mercatò':        ['#8A1538', '#FFFFFF'],
  'Ekom':           ['#F47A20', '#FFFFFF'],
  'Ipercoop':       ['#A3123A', '#FFFFFF'],
  'Carrefour Iper': ['#004E9F', '#FFFFFF'],
  'Pam':            ['#00843D', '#FFFFFF'],
  'Conad':          ['#E30613', '#FFFFFF'],
};
function marchio(ins) {
  const e = document.createElement('b');
  const logo = (DATI.loghi || {})[ins];
  if (logo) {
    /* IL MARCHIO VERO. Il fondo resta bianco anche nei look scuri: i loghi
       hanno i loro colori, e messi su un fondo nero sparirebbero o
       diventerebbero un'altra cosa. La scritta col nome resta dentro, solo
       per chi usa un lettore di schermo: senza, un logo e un'immagine muta. */
    e.className = 'marchio col-logo';
    e.innerHTML = logo + '<span class="solo-voce"></span>';
    e.querySelector('.solo-voce').textContent = ins;
    e.title = ins;
    return e;
  }
  const c = MARCHI[ins] || ['#3F3F3F', '#FFFFFF'];
  e.className = 'marchio';
  e.style.background = c[0];
  e.style.color = c[1];
  e.textContent = ins;
  return e;
}

/* I formati che non dicono niente più del prezzo per unità: «al kg», «1 kg»,
   «1 litro», «al kg (al banco)». Per questi, accanto al prezzo della
   confezione resta «al pezzo» (o niente, se è lo stesso numero). */
const FORMATO_BANALE = /^(?:al (?:kg|litro|pezzo)|1 ?(?:kg|l|litro|rotolo)|kg 1|1000 g)(?: confezione)?(?: \(al banco\))?$/;

/* «al kg» -> «/kg», «al litro» -> «/l», «all'uovo» -> «/uovo». */
function unitaCorta(u) {
  const v = u.replace(/^(?:al|allo|alla|a)\s+|^all['’]/, '');
  return '/' + (v === 'litro' ? 'l' : v === 'pezzo' ? 'pz' : v);
}

function rigaPrezzo(o, meno) {
  const d = document.createElement('article');
  d.className = 'prezzo-riga' + (meno ? ' vince' : '') + (futuro(o) ? ' dopo' : '');
  d.innerHTML = `<div class="coda"></div>
    <div class="dati"><p class="nome"></p><p class="sotto"></p></div>
    <p class="val"><span class="p1"><span class="n"></span><span class="u"></span></span>
      <span class="p2"><span class="pz"></span><span class="et">al pezzo</span></span></p>`;

  /* In cima alla scheda: il marchio del negozio e i bollini che contano. */
  const coda = d.querySelector('.coda');
  coda.appendChild(marchio(o.ins));
  if (meno) coda.insertAdjacentHTML('beforeend',
    '<span class="bollo meno">il meno caro valido oggi</span>');
  if (o.ristretta) coda.insertAdjacentHTML('beforeend',
    '<span class="bollo stretta">solo ' + giorno(o.inizio) + ' al ' + soloGiorno(o.fino) + '</span>');
  if (o.dubbio) coda.insertAdjacentHTML('beforeend', '<span class="bollo dubbio">da controllare</span>');

  d.querySelector('.nome').textContent = o.pro;

  /* QUANDO I DUE PREZZI SONO LO STESSO NUMERO, SI SCRIVE UNA VOLTA SOLA.
     Chiesto da Manlio il 2026-09-22: «ci sono dei prodotti col prezzo al kg
     che corrisponde al prezzo al pezzo, soprattutto nei salumi ma anche negli
     altri prodotti da banco, che chiaramente non sono confezionati; puoi
     toglierli nel caso in cui coincidano». Sono le offerte vendute sfuse —
     al kg, al banco: lì «la confezione» non esiste, e lo stesso numero
     scritto due volte fa solo rumore. Si confrontano i numeri COME VENGONO
     SCRITTI (eur), non i decimali interi: 12,67 e 12,670001 sulla pagina
     sono la stessa cosa. */
  const doppio = eur(o.prezzo) === eur(o.unitario);

  /* LA RIGA «Formato: … · fino al …» NON SI VEDE PIÙ (Manlio, 2026-09-23:
     «le righe formato al kg e vale dal eccetera secondo me vanno tutte tolte,
     perché la data in cui scade c'è scritta e sotto c'è scritto il prezzo al
     kg»). La scadenza la dice il cerchietto dei giorni (o il tondino di
     quando parte, o il bollino rosso delle date strette), «al kg» lo dice il
     prezzo grande. La riga resta dentro la scheda SOLO PER CHI NON VEDE
     (.solo-voce): per un lettore di schermo il cerchietto è un numero muto. */
  const s = d.querySelector('.sotto');
  s.classList.add('solo-voce');
  s.innerHTML = 'Formato: <b></b>';
  s.querySelector('b').textContent = o.fmt;
  const q = durata(o);
  if (q) {
    const d2 = document.createElement('span');
    d2.className = 'quando' + (o.ristretta ? ' stretta' : '');
    d2.textContent = q;
    s.appendChild(document.createTextNode(' · '));
    s.appendChild(d2);
  }

  /* IL PESO DELLA CONFEZIONE VA ACCANTO AL SUO PREZZO: «1,39 € 160 g» al
     posto di «1,39 € al pezzo». Era l'unica cosa della riga tolta che non
     stava già altrove. Sulle offerte sfuse («al kg», «1 kg», «1 litro») il
     formato non dice niente di più del prezzo grande e non si scrive; se
     dice qualcosa (una confezione «2 × 500 g (1+1)» che costa come un
     chilo) si scrive da solo accanto al prezzo per unità. */
  const banale = FORMATO_BANALE.test(o.fmt);
  const p2 = d.querySelector('.val .p2'), et = p2.querySelector('.et');
  if (doppio && banale) p2.remove();
  else {
    if (doppio) p2.querySelector('.pz').remove();
    else p2.querySelector('.pz').textContent = eur(o.prezzo);
    /* Del formato si scrive solo la prima parte: «4x160 g, sgocciolati
       425 g» diventa «4x160 g», «360 g (2 × 180 g)» diventa «360 g». Il
       resto allargava la colonna dei prezzi e schiacciava il nome; lo
       sgocciolato ha già la sua pillola. */
    const corto = o.fmt.split(/,\s|\s\(/)[0].trim() || o.fmt;   // «1,5 l» resta intero
    if (!banale) { et.textContent = (doppio ? '' : '· ') + corto; et.classList.add('fmt'); }
  }
  /* SENZA «€» E CON L'UNITÀ CORTA ATTACCATA AL NUMERO (Manlio, 2026-09-23:
     «in più c'è sempre scritto euro… la scritta prezzo al chilo appare sia
     di fianco al nome del prodotto in alto che accanto al prezzo»): in una
     scheda ogni numero è un prezzo, e «8,69/kg» si legge da solo. L'unità
     resta su ogni prezzo perché in Cerca, Grandi marche e Personale le
     offerte mescolano chili, litri e rotoli. Nelle frasi (la riga in cima)
     il «€» resta. */
  d.querySelector('.val .n').textContent = eur(o.unitario);
  d.querySelector('.val .u').textContent = unitaCorta(DATI.unita[o.cat] || 'al kg');

  /* IL TONDINO E IL FOGLIETTO STANNO IN CIMA, accanto al marchio, chiesto da
     Manlio il 2026-09-22: prima il tondino dei giorni, poi il foglietto del
     volantino. Il tondino è piccolo come il marchio e non ha più la scritta
     «giorni» sotto: in quella riga ci sono già le parole che servono. */
  const cer = cerchioGiorni(o) || cerchioInizio(o);
  const link = dove(o);
  /* IL FOGLIETTO ROSSO DEL VOLANTINO NON C'È PIÙ (Manlio, 2026-09-23: «è
     diventato completamente inutile, ed essendo rosso fallo sparire»): tutta
     la scheda apre il volantino, e dentro c'è «Apri sul sito». Resta la riga
     scritta solo dove l'indirizzo della pagina non c'è. */
  if (cer || o.sconto) {
    const ang = document.createElement('div');
    ang.className = 'angolo';
    if (cer) ang.appendChild(cer);
    /* LO SCONTO, fra il tondino e il foglietto (Manlio, 2026-09-23). Solo
       dove il volantino lo dice: il conto sta in pagina.py, «sconto()». */
    if (o.sconto) {
      const s = document.createElement('span');
      s.className = 'sconto';
      s.textContent = '\u2212' + o.sconto + '%';
      s.title = 'Sconto del ' + o.sconto + '%' + (o.prima ? ': prima ' + o.prima + ' €' : ' sul prezzo di prima');
      ang.appendChild(s);
    }
    coda.insertBefore(ang, coda.children[1] || null);
  }

  const dati = d.querySelector('.dati');
  /* LE CONDIZIONI SONO BOLLINI BREVI (Manlio, 2026-09-23). Il resto della
     nota non si mostra: «Dettagli» c'era e l'ha fatto togliere lo stesso
     giorno, «sono davvero dei dettagli». Quali bollini lo decide pagina.py,
     «condizioni()». */
  if (o.bolli && o.bolli.length) {
    const c = document.createElement('p');
    c.className = 'cond';
    for (const b of o.bolli) {
      const e = document.createElement('span');
      e.className = 'bollo cond';
      e.textContent = b;
      c.appendChild(e);
    }
    dati.appendChild(c);
  }
  /* TUTTA LA SCHEDA APRE LA PAGINA DEL VOLANTINO (Manlio, 2026-09-23:
     «fare aprire il volantino quando si fa clic in qualunque di queste
     schede: così probabilmente la gente ne aprirebbe di più»). Si apre sopra
     l'elenco, con un tastone «Chiudi» in basso: vedi apriPaginaVol(). Anche
     il foglietto in cima fa lo stesso; tenuto premuto resta un collegamento
     normale, che si apre in un'altra scheda. */
  if (o.url) {
    d.classList.add('apribile');
    d.addEventListener('click', ev => {
      ev.preventDefault();
      apriPaginaVol(o);
    });
  }
  /* Senza indirizzo resta la riga scritta: non c'e niente da toccare, e
     un'icona che non apre niente sarebbe una presa in giro. */
  if (link.tagName !== 'A') dati.appendChild(link);

  /* NIENTE «Vedi tutte le offerte del volantino» in fondo a ogni scheda:
     tolto il 2026-09-22 su richiesta di Manlio, «e inutile». Le offerte di un
     volantino si aprono lo stesso, dal suo tasto in fondo alla pagina. */
  return d;
}

/* La riga che dice dov'e l'offerta. Se so l'indirizzo della pagina diventa un
   collegamento che apre il volantino a quella pagina: prima c'era scritto
   «pagina 16» e Manlio doveva arrangiarsi. Si apre in una scheda nuova, cosi
   non perde la lista. */
function dove(o) {
  if (!o.url) {
    const p = document.createElement('p');
    p.className = 'dove';
    p.textContent = o.pag ? `${o.pdf} — pagina ${o.pag}` : `${o.pdf} — pagina non individuata`;
    return p;
  }
  const a = document.createElement('a');
  a.className = 'dove apri';
  a.href = o.url;
  a.target = '_blank';
  a.rel = 'noopener noreferrer';
  /* Il foglietto del volantino con l'orecchia piegata, disegnato a mano:
     nessun carattere speciale, che sui telefoni diventa un quadratino. */
  a.innerHTML = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    + '<path d="M3.2 1.8h5.6l3.4 3.4v9H3.2z"></path>'
    + '<path d="M8.8 1.8v3.4h3.4"></path>'
    + '<path d="M5.6 8.2h4.8M5.6 10.8h3.2"></path></svg>';
  const frase = `Apri la pagina ${o.pag} del volantino`;
  a.title = frase;
  a.setAttribute('aria-label', frase);
  return a;
}

function rigaPagina(p) {
  const d = document.createElement(p.url ? 'a' : 'div');
  d.className = 'pag-riga' + (p.url ? ' apribile' : '');
  if (p.url) { d.href = p.url; d.target = '_blank'; d.rel = 'noopener noreferrer'; }
  d.innerHTML = `<span><span class="ins"></span><span class="per"></span></span><span class="np"></span>`;
  d.querySelector('.ins').textContent = p.ins;
  d.querySelector('.per').textContent = (p.prese && p.prese.length)
    ? 'ci ho trovato: ' + p.prese.join(', ')
    : p.periodo;
  d.querySelector('.np').textContent = 'pag. ' + p.pag;
  return d;
}

/* ---------- pagina ---------- */
function disegna() {
  disegnaTasti();
  const out = document.getElementById('risultato');
  out.textContent = '';
  if (!lista.length) {
    out.innerHTML = '<p class="vuoto">La lista è vuota. Tocca «+ aggiungi» per rimetterci qualcosa.</p>';
    return;
  }
  if (scelto >= lista.length) scelto = lista.length - 1;

  const v = lista[scelto];
  const off = offerteDi(v), pag = pagineDi(v);

  /* SOTTO IL NOME DEL PRODOTTO NON CI VA PIÙ NIENTE.
     Manlio, 2026-09-05, foto alla mano: «toglierei tutto quello che c'è
     scritto dopo carne di bue e lascerei solo una piccola scritta o un'icona
     per cancellarla». Quanti prezzi ci sono, con che altri nomi si cerca e il
     cambio nome sono roba da guardare una volta ogni tanto: stanno dietro il
     bollino «i», come le spiegazioni in fondo. Restano il nome e la crocetta. */
  const capo = document.createElement('div');
  capo.className = 'capo';
  /* Il bottone dice cosa fa. Prima c'era una crocetta, e Manlio: «la x per
     togliere il prodotto mi sembra poco comprensibile, metterei invece un
     bottone elimina prodotto». La «i» viene subito dopo, come ha chiesto. */
  /* «Elimina prodotto» NON sta più qui: è dentro la «i», accanto a «Cambia
     nome» (Manlio, 2026-09-23, punto 4: «anche qua la tua soluzione è
     ottima»). Era grande quanto il titolo per un'azione che si fa di rado. */
  /* Niente più «prezzo al kg» accanto al nome (Manlio, 2026-09-23): lo dice
     già ogni prezzo, «8,69/kg». */
  capo.innerHTML = '<h2></h2>'
    + '<button type="button" class="info" aria-expanded="false"'
    + ' aria-label="Mostra i dettagli del prodotto">i</button>';
  capo.querySelector('h2').textContent = v.nome;
  out.appendChild(capo);

  /* «Elimina prodotto» (dentro la «i»): un tocco per sbaglio non deve
     far sparire un prodotto. Chiede conferma lì dove si è toccato, senza
     finestrelle di sistema che sul telefono arrivano da tutt'altra parte. */
  const conferma = document.createElement('div');
  conferma.className = 'conferma';
  conferma.hidden = true;
  conferma.innerHTML = '<span></span><button type="button" class="si">Elimina</button>'
    + '<button type="button" class="no">Lascia</button>';
  conferma.querySelector('span').textContent = 'Elimino «' + v.nome + '»?';
  conferma.querySelector('.si').onclick = () => {
    lista.splice(scelto, 1);
    if (scelto > 0) scelto--;
    salva(); disegna();
  };
  conferma.querySelector('.no').onclick = () => { conferma.hidden = true; };

  const dett = document.createElement('div');
  dett.className = 'dettaglio';
  dett.hidden = true;

  const quanti = document.createElement('p');
  quanti.className = 'quanti';
  quanti.textContent = off.length
    ? `${off.length} ${off.length === 1 ? 'offerta letta' : 'offerte lette'} dal volantino · ${pag.length} pagine da guardare`
    : `${pag.length} ${pag.length === 1 ? 'pagina lo nomina' : 'pagine lo nominano'}`;
  dett.appendChild(quanti);

  const altri = nomiDi(v).slice(1);
  if (altri.length) {
    const p = document.createElement('p');
    p.className = 'sinonimi';
    p.innerHTML = '<span></span> ';
    p.querySelector('span').textContent = 'cerca anche:';
    altri.forEach(a => {
      const c = document.createElement('em');
      c.textContent = a;
      p.appendChild(c);
    });
    dett.appendChild(p);
  }

  const g = document.createElement('div');
  g.className = 'gestisci';
  const bRin = document.createElement('button');
  bRin.type = 'button'; bRin.textContent = 'Cambia nome';
  g.appendChild(bRin);
  const bVia = document.createElement('button');
  bVia.type = 'button'; bVia.className = 'elimina'; bVia.textContent = 'Elimina prodotto';
  bVia.setAttribute('aria-label', 'Elimina «' + v.nome + '» dalla lista');
  bVia.onclick = () => { conferma.hidden = !conferma.hidden; };
  g.appendChild(bVia);
  dett.appendChild(g);
  dett.appendChild(conferma);

  const fr = document.createElement('form');
  fr.className = 'form-rin';
  fr.innerHTML = '<input type="text" aria-label="Nomi del prodotto, separati da virgola"><button type="submit">Salva</button>';
  const inp = fr.querySelector('input');
  fr.onsubmit = ev => {
    ev.preventDefault();
    const t = inp.value.trim();
    if (!t) return;
    const v2 = costruisci(t);
    if (!v2) return;
    lista[scelto] = v2;
    salva(); disegna();
  };
  bRin.onclick = () => {
    fr.classList.add('on');
    inp.value = nomiDi(v).join(', ');
    inp.focus(); inp.select();
  };
  dett.appendChild(fr);
  out.appendChild(dett);

  capo.querySelector('.info').onclick = () => {
    const apri = dett.hidden;
    dett.hidden = !apri;
    capo.querySelector('.info').setAttribute('aria-expanded', String(apri));
  };

  if (off.length) {
    const meno = menoCaroOggi(off);
    const f = document.createElement('p');
    f.className = 'fascia';
    f.textContent = 'Offerte ordinate dal prezzo per unità più conveniente';
    const schede = new Map();
    off.forEach(o => schede.set(o, rigaPrezzo(o, o === meno)));
    const sint = sintesi(off, meno, schede);
    if (sint) out.appendChild(sint);
    out.appendChild(f);
    off.forEach(o => out.appendChild(schede.get(o)));
  } else if (v.cat && DATI.offerte.some(o => o.cat === v.cat)) {
    /* I prezzi c'erano e sono tutti scaduti. Dirlo, invece di far comparire il
       vuoto: senza questa riga sembrerebbe che il prodotto non sia mai stato
       in offerta da nessuna parte. */
    const p = document.createElement('p');
    p.className = 'vuoto';
    p.textContent = 'I volantini che avevano questo prodotto sono tutti scaduti, '
      + 'e quelli nuovi non li ho ancora letti. Qui sotto ci sono comunque le pagine.';
    out.appendChild(p);
  }

  const f2 = document.createElement('p');
  f2.className = 'fascia';
  f2.textContent = off.length ? 'Altre pagine che lo nominano' : 'Pagine da guardare';
  out.appendChild(f2);

  if (pag.length) {
    const quante = tutteLePagine ? pag.length : 10;
    pag.slice(0, quante).forEach(p => out.appendChild(rigaPagina(p)));
    if (pag.length > quante) {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'altre';
      b.textContent = `Mostra le altre ${pag.length - quante} pagine`;
      b.onclick = () => { tutteLePagine = true; disegna(); };
      out.appendChild(b);
    }
  } else {
    const p = document.createElement('p');
    p.className = 'vuoto';
    p.textContent = 'Il computer non ha letto questa parola in nessuna pagina. Può esserci lo stesso: prova a chiamare il prodotto in un altro modo, con una parola più comune.';
    out.appendChild(p);
  }
}

/* ---------- volantini in fondo ---------- */
const ul = document.getElementById('vol');
function disegnaVolantini() {
ul.textContent = '';
DATI.volantini.filter(v => !tolta(v.ins)).forEach(v => {
  const li = document.createElement('li');
  li.innerHTML = `<div class="capo-vol"><span><span class="i"></span> <span class="p"></span></span><span class="n"></span></div>`;
  li.querySelector('.i').textContent = v.ins;
  li.querySelector('.p').textContent = v.periodo
    + (scaduto(v) ? ' — scaduto' : futuro(v) ? ' — non ancora cominciato' : '');
  if (scaduto(v) || futuro(v)) li.querySelector('.p').style.color = 'var(--ambra)';
  li.querySelector('.n').textContent = v.pagine + ' pag.';

  /* I DUE TASTI, chiesti da Manlio il 2026-09-18: «visto che alla fine c'e
     l'elenco dei supermercati, un tasto per vedere le offerte e uno per vedere
     il volantino». Tutti e due aprono una scheda nuova, come ha chiesto: chi
     guarda non perde la lista ne il punto in cui era. */
  const tasti = document.createElement('div');
  tasti.className = 'vol-tasti';

  /* Quante ne valgono OGGI, non quante ne ho lette: di un volantino scaduto
     non c'e niente da aprire, e il tasto lo direbbe per finta. Il conto lo fa
     il browser di chi guarda, con la sua data, come tutto il resto. */
  const quante = DATI.offerte.filter(o => o.pdf === v.pdf && !nascosta(o)).length;
  if (quante) {
    const a = document.createElement('a');
    a.className = 'vol-t';
    a.href = location.href.split('#')[0] + '#volantino=' + encodeURIComponent(v.pdf);
    a.target = '_blank';
    a.rel = 'noopener';
    a.textContent = 'Le offerte (' + quante + ')';
    /* La scheda nuova si apre a mano, e non per capriccio: dentro la copia di
       Claude la pagina sta in una cornice che a volte la scheda nuova non la
       lascia aprire. Se non si apre, invece di non fare niente si apre il
       pannello qui, sulla stessa pagina: meglio un tasto che funziona in un
       modo un po' diverso di un tasto che non fa niente. */
    a.onclick = ev => {
      ev.preventDefault();
      let nuova = null;
      try { nuova = window.open(a.href, '_blank'); } catch (e) { nuova = null; }
      if (nuova) { try { nuova.opener = null; } catch (e) {} return; }
      apriVolantino(v.pdf);
      inCima();
    };
    tasti.appendChild(a);
  } else {
    const spento = document.createElement('span');
    spento.className = 'vol-t spento';
    spento.textContent = scaduto(v) ? 'offerte scadute'
      : futuro(v) ? 'prezzi in arrivo' : 'prezzi non ancora letti';
    tasti.appendChild(spento);
  }

  if (v.apri) {
    const b = document.createElement('a');
    b.className = 'vol-t fuori';
    b.href = v.apri;
    b.target = '_blank';
    b.rel = 'noopener noreferrer';
    b.textContent = 'Il volantino';
    tasti.appendChild(b);
  }
  li.appendChild(tasti);
  ul.appendChild(li);
});
}
disegnaVolantini();

/* Ogni bollino «i» apre e chiude il pannello che gli sta subito dopo il
   titolo. Un solo giro per tutti: aggiungendo una sezione basta scriverci il
   bollino e il pannello, senza toccare questo. */
document.querySelectorAll('.info').forEach(b => {
  /* h1 O h2: il primo bollino di questa pagina stava in un h2, e cercare solo
     quello bastava. Aggiungendone uno nel titolone in cima, closest('h2') ha
     dato niente e la pagina è uscita MUTA — bottoni compresi, perché l'errore
     fermava tutto il resto dello script. È lo stesso guasto del tag di
     chiusura scritto per esteso: da fuori sembra a posto e non funziona
     niente. Se un giorno un bollino finisce in un h3, va aggiunto qui. */
  const testa = b.closest('h1, h2');
  const pannello = testa && testa.nextElementSibling;
  if (!pannello || !pannello.classList.contains('dettaglio')) return;
  b.onclick = () => {
    const apri = pannello.hidden;
    pannello.hidden = !apri;
    b.setAttribute('aria-expanded', String(apri));
    b.setAttribute('aria-label', apri ? 'Nascondi la spiegazione' : 'Mostra la spiegazione');
  };
});

document.getElementById('cerca').oninput = disegnaScaffali;
document.getElementById('chiudi-cassetto').onclick = () => apriCassetto(false);
document.getElementById('chiudi-ricerca').onclick = () => apriRicerca(false);
document.getElementById('vai-inizio').onclick = e => { e.preventDefault(); vaiInizio(); };
document.getElementById('q').addEventListener('input', () => {
  if (marcaScelta) { marcaScelta = null; disegnaMarche(); }
  quantiMostrati = 40;
  disegnaTrovati();
});

document.getElementById('form-agg').onsubmit = ev => {
  ev.preventDefault();
  const c = document.getElementById('nuovo');
  const t = c.value.trim();
  if (!t) return;
  const v2 = costruisci(t);
  if (!v2) return;
  lista.push(v2);
  scelto = lista.length - 1;
  tutteLePagine = false;
  c.value = '';
  apriCassetto(false);
  salva(); disegna();
};


/* Una data sola per tutta la pagina. Prima quella in fondo era scritta a mano e
   restava indietro: la pagina diceva 4 settembre in mezzo e 2 settembre in fondo,
   e se n'e accorto Manlio. */
document.getElementById('letto').textContent = 'letti il ' + DATI.letto;
document.getElementById('pie').textContent =
  'Volantini letti il ' + DATI.letto + '. I numeri di pagina sono quelli dei volantini.';
aggiornaTestoLista();

/* Cosa dire della lista dipende dalla copia che si sta guardando: sul sito e
   una per telefono, sulla copia di Claude e una sola per tutti. Scriverne una
   sola delle due era una bugia per meta dei lettori. */
function aggiornaTestoLista() {
  const p = document.getElementById('p-lista');
  if (!p) return;
  p.innerHTML = soloMio
    ? '<b>La lista dei prodotti è tua e resta su questo telefono.</b> Puoi aggiungere e '
      + 'togliere quello che vuoi senza toccare quella di nessun altro. Chi apre da un altro '
      + 'telefono riparte dai prodotti di partenza e se la regola per conto suo.'
    : '<b>La lista dei prodotti è una sola, condivisa.</b> Chi apre il link vede la stessa, e se '
      + 'la cambia la cambia per tutti. Quando qualcuno la tocca, gli altri schermi si aggiornano '
      + 'da soli.';
}


disegna();

/* «#volantino=...» in coda all'indirizzo: e quello che i tasti in fondo mettono
   nella scheda nuova. Qui si legge e si apre subito il pannello con le offerte
   di quel volantino. Se non corrisponde a niente non succede niente: meglio la
   pagina normale che un pannello vuoto. */
(function daIndirizzo() {
  const m = /^#volantino=(.+)$/.exec(location.hash || '');
  if (!m) return;
  let pdf = '';
  try { pdf = decodeURIComponent(m[1]); } catch (e) { return; }
  if (!DATI.volantini.some(v => v.pdf === pdf)) return;
  apriVolantino(pdf);
  /* Nella scheda nuova si arriva in cima, con lo schermo pieno di bottoni, e
     le offerte appena aperte restano mezze sotto. Un piccolo scorrimento le
     porta subito sotto la barra: chi ha toccato «Le offerte» vuole vedere
     quelle, non la fila dei prodotti. */
  try {
    const pan = document.getElementById('ricerca');
    const alto = altaFissa();
    window.scrollTo(0, Math.max(0, pan.getBoundingClientRect().top + (window.scrollY || 0) - alto - 8));
  } catch (e) {}
})();

/* ---------- la finestra delle novità DELLA PAGINA ---------- */
/* Chiesta da Manlio il 2026-09-18. Si apre da sola la prima volta, e dice cosa
   si puo fare adesso che prima non si poteva: l'interfaccia, non i prezzi. I
   prezzi nuovi hanno gia il tasto «Novità» in alto a destra.

   Chi ha gia visto tutto non la rivede piu: nel browser di chi guarda resta
   l'id dell'ultima novita vista, e la volta dopo compaiono SOLO quelle
   arrivate dopo. Gli id cominciano con la data apposta: e cosi che «dopo»
   diventa un confronto fra due scritte, senza tenere elenchi.

   Se il browser non lascia leggere ne scrivere (navigazione privata, memoria
   piena), la finestra si comporta come per uno nuovo: si apre. Meglio una
   volta di troppo che una pagina che non funziona. */
const NOVITA_VISTE = 'spesa.novita.v1';

function novitaDaMostrare() {
  const tutte = DATI.novita || [];
  if (!tutte.length) return [];
  let vista = '';
  try { vista = localStorage.getItem(NOVITA_VISTE) || ''; } catch (e) { vista = ''; }
  if (!vista) return tutte;
  return tutte.filter(n => n.id > vista);
}

function mostraNovita() {
  const buio = document.getElementById('buio');
  if (!buio) return;
  const da = novitaDaMostrare();
  if (!da.length) { buio.hidden = true; return; }
  const box = document.getElementById('voci-novita');
  box.textContent = '';
  da.forEach(n => {
    const d = document.createElement('div');
    d.className = 'voce';
    d.innerHTML = '<span class="quando"></span><h3></h3><p></p>';
    d.querySelector('.quando').textContent = n.quando;
    d.querySelector('h3').textContent = n.titolo;
    d.querySelector('p').textContent = n.testo;
    box.appendChild(d);
  });
  buio.hidden = false;
  /* Il fuoco sul tasto SENZA muovere la pagina: con lo scorrimento in automatico
     la finestra si apriva gia scorsa in fondo e il titolo non si vedeva. */
  try { document.getElementById('chiudi-novita').focus({ preventScroll: true }); } catch (e) {}
  try { document.querySelector('.finestra').scrollTop = 0; } catch (e) {}
}

/* Chiudendo si segna l'ULTIMA della lista, non l'ultima mostrata: se uno apre
   per la prima volta le vede tutte, e da li in poi conta solo quello che
   arriva dopo. */
function chiudiNovita() {
  const buio = document.getElementById('buio');
  if (!buio || buio.hidden) return;
  buio.hidden = true;
  /* SI SEGNA IL PIU GRANDE, NON L'ULTIMO DELL'ELENCO.
     Il confronto fra id e alfabetico, e due novita dello stesso giorno
     finiscono in elenco nell'ordine in cui le ho scritte, non in ordine di
     nome: segnando l'ultima, «2026-09-22-look» restava «mai vista» perche
     viene dopo «2026-09-22-giorni» in ordine alfabetico, e la finestra
     tornava a ogni apertura. */
  const tutte = DATI.novita || [];
  if (tutte.length) {
    const piu = tutte.reduce((a, n) => (n.id > a ? n.id : a), tutte[0].id);
    try { localStorage.setItem(NOVITA_VISTE, piu); } catch (e) {}
  }
}

/* ---------- i look: i colori della pagina ---------- */
/* Chiesti da Manlio il 2026-09-22, uno per ognuna delle cento combinazioni del
   libretto di Figma. Un look e solo un pugno di colori messi nelle variabili
   del foglio di stile: tutta la pagina li usa gia, quindi cambiarli cambia
   tutto insieme, senza ricaricare niente.

   LA PAGINA PARTE SEMPRE COM'E SEMPRE STATA. Il look si sceglie a mano e resta
   scelto nel browser di chi guarda. Non e la modalita scura automatica, che e
   vietata da anni in questo progetto: li decideva il telefono, qui decide lui. */
const LOOK_SCELTO = 'spesa.look.v1';
const TINTE = ['carta', 'pannello', 'inchiostro', 'tenue', 'linea', 'linea-forte',
               'rosso', 'su-rosso', 'rosso-tenue', 'verde', 'verde-tenue',
               'ambra', 'ambra-tenue', 'blu', 'blu-tenue'];
let lookAdesso = '';

function applicaLook(id, ricorda) {
  const radice = document.documentElement;
  const l = (DATI.look || []).find(x => x.id === id);
  TINTE.forEach(n => radice.style.removeProperty('--' + n));
  if (l) TINTE.forEach(n => { if (l.v[n]) radice.style.setProperty('--' + n, l.v[n]); });
  lookAdesso = l ? l.id : '';
  if (ricorda !== false) {
    try { localStorage.setItem(LOOK_SCELTO, lookAdesso); } catch (e) {}
  }
  /* La barra del telefono in cima prende il colore della pagina: senza, su un
     look scuro resta una striscia bianca che sembra un pezzo rotto. */
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) {
    try {
      meta.content = getComputedStyle(radice).getPropertyValue('--carta').trim() || '#FFFFFF';
    } catch (e) {}
  }
  if (!document.getElementById('buio-look').hidden) segnaLookScelto();
}

function segnaLookScelto() {
  document.querySelectorAll('#voci-look .look-riga').forEach(b => {
    const suo = b.getAttribute('data-look') === lookAdesso;
    b.setAttribute('aria-pressed', String(suo));
    b.querySelector('.scelto').textContent = suo ? 'scelto' : '';
  });
}

function rigaLook(id, nome, sotto, tinte) {
  const b = document.createElement('button');
  b.type = 'button';
  b.className = 'look-riga';
  b.setAttribute('data-look', id);
  b.innerHTML = '<span class="strisce"></span>'
    + '<span class="come"><b></b><span></span></span><span class="scelto"></span>';
  const str = b.querySelector('.strisce');
  tinte.forEach(c => {
    const i = document.createElement('i');
    i.style.background = c;
    str.appendChild(i);
  });
  b.querySelector('.come b').textContent = nome;
  b.querySelector('.come span').textContent = sotto;
  b.onclick = () => applicaLook(id, true);
  return b;
}

function disegnaLook() {
  const box = document.getElementById('voci-look');
  if (box.dataset.fatto) { segnaLookScelto(); return; }
  box.textContent = '';
  /* Primo di tutti: come torni indietro. Una pagina che cambia colore e non sa
     tornare com'era e una trappola. */
  box.appendChild(rigaLook('', 'Originale', 'com’era prima',
    ['#FFFFFF', '#D40D2B', '#1E7A4B', '#8A5A08']));
  const fam = [];
  (DATI.look || []).forEach(l => {
    if (!fam.length || fam[fam.length - 1].nome !== l.fam) fam.push({ nome: l.fam, righe: [] });
    fam[fam.length - 1].righe.push(l);
  });
  fam.forEach(g => {
    const t = document.createElement('p');
    t.className = 'gruppo-look';
    t.textContent = g.nome;
    box.appendChild(t);
    g.righe.forEach(l => box.appendChild(
      rigaLook(l.id, l.nome, l.notte ? 'scuro' : '', l.base)));
  });
  box.dataset.fatto = '1';
  segnaLookScelto();
}

function apriLook(si) {
  const buio = document.getElementById('buio-look');
  if (!buio) return;
  if (si) { chiudiNovita(); apriAiuto(false); apriConfig(false); }
  buio.hidden = !si;
  if (si) {
    disegnaLook();
    try { buio.querySelector('.finestra').scrollTop = 0; } catch (e) {}
    try { document.getElementById('chiudi-look').focus({ preventScroll: true }); } catch (e) {}
  }
}

document.getElementById('apri-look').onclick = () => apriLook(true);
document.getElementById('chiudi-look').onclick = () => apriLook(false);
document.getElementById('buio-look').onclick = ev => {
  if (ev.target.id === 'buio-look') apriLook(false);
};

/* Il look scelto l'altra volta si rimette subito, prima di disegnare i prezzi:
   se no la pagina compare com'era e cambia colore sotto gli occhi. */
(function lookDiPrima() {
  let id = '';
  try { id = localStorage.getItem(LOOK_SCELTO) || ''; } catch (e) { id = ''; }
  if (id) applicaLook(id, false);
})();

/* ---------- la finestra dell'aiuto ---------- */
/* Al contrario di quella delle novita non si apre mai da sola e non si ricorda
   niente: si apre quando uno tocca «Aiuto» e si chiude in tre modi, il tasto,
   il buio intorno, il tasto Esc. */
function apriAiuto(si) {
  const buio = document.getElementById('buio-aiuto');
  if (!buio) return;
  if (si) { chiudiNovita(); apriLook(false); apriConfig(false); }   // una finestra alla volta
  buio.hidden = !si;
  if (si) {
    try { document.getElementById('chiudi-aiuto').focus({ preventScroll: true }); } catch (e) {}
    try { buio.querySelector('.finestra').scrollTop = 0; } catch (e) {}
  }
}

document.getElementById('apri-aiuto').onclick = () => apriAiuto(true);
/* «Novità app» riapre la finestra «Cosa c'è di nuovo» anche a chi l'ha già
   vista: prima si poteva solo aspettare che si aprisse da sola. */
document.getElementById('apri-novita-app').onclick = () => {
  apriAiuto(false); apriLook(false); apriConfig(false);
  const buio = document.getElementById('buio');
  const box = document.getElementById('voci-novita');
  const tutte = DATI.novita || [];
  box.textContent = '';
  tutte.forEach(n => {
    const e = document.createElement('div');
    e.className = 'voce';
    e.innerHTML = '<span class="quando"></span><h3></h3><p></p>';
    e.querySelector('.quando').textContent = n.quando;
    e.querySelector('h3').textContent = n.titolo;
    e.querySelector('p').textContent = n.testo;
    box.appendChild(e);
  });
  buio.hidden = false;
  try { document.getElementById('chiudi-novita').focus({ preventScroll: true }); } catch (e) {}
  try { document.querySelector('#buio .finestra').scrollTop = 0; } catch (e) {}
};
document.getElementById('chiudi-aiuto').onclick = () => apriAiuto(false);
document.getElementById('buio-aiuto').onclick = ev => {
  if (ev.target.id === 'buio-aiuto') apriAiuto(false);
};

document.getElementById('chiudi-novita').onclick = chiudiNovita;
/* Il buio intorno chiude, la finestra no: toccando dentro non deve sparire. */
document.getElementById('buio').onclick = ev => { if (ev.target.id === 'buio') chiudiNovita(); };
/* ---------- la pagina del volantino, sopra l'elenco ---------- */
/* Toccando una scheda (Manlio, 2026-09-23). Le pagine di nove insegne su
   dieci sono immagini sul sito di chi le pubblica, e si mostrano così come
   sono; il Conad ha un visore suo, che si apre qui dentro. Se l'immagine non
   arriva (niente rete, o un sito che la rifiuta) resta scritto come aprirla
   fuori. Il tasto «indietro» del telefono chiude, come «Chiudi»: si mette una
   voce nella cronologia apposta. */
const E_IMMAGINE = /\.(?:jpe?g|png|webp|gif)(?:\?|$)|\/thumbor\//i;
let volAperto = false;
function apriPaginaVol(o) {
  const box = document.getElementById('vol-sopra');
  const foglio = document.getElementById('foglio-vol');
  document.getElementById('titolo-vol').innerHTML = '<b></b> · pagina <span></span>';
  document.querySelector('#titolo-vol b').textContent = o.ins;
  document.querySelector('#titolo-vol span').textContent = o.pag;
  document.getElementById('fuori-vol').href = o.url;
  foglio.textContent = '';
  const guasto = () => {
    foglio.innerHTML = '<p class="avviso-vol">La pagina qui non si vede. <a target="_blank" rel="noopener noreferrer">Aprila sul sito</a></p>';
    foglio.querySelector('a').href = o.url;
  };
  if (E_IMMAGINE.test(o.url)) {
    const img = document.createElement('img');
    img.alt = 'Pagina ' + o.pag + ' del volantino ' + o.ins;
    img.referrerPolicy = 'no-referrer';
    img.onerror = guasto;
    img.src = o.url;
    foglio.appendChild(img);
  } else {
    const f = document.createElement('iframe');
    f.title = 'Pagina ' + o.pag + ' del volantino ' + o.ins;
    f.referrerPolicy = 'no-referrer';
    f.src = o.url;
    foglio.appendChild(f);
  }
  box.hidden = false;
  document.documentElement.style.overflow = 'hidden';
  foglio.scrollTop = 0;
  if (!volAperto) {
    volAperto = true;
    try { history.pushState({ volSopra: 1 }, '', location.href); } catch (e) {}
  }
  try { document.getElementById('chiudi-vol').focus({ preventScroll: true }); } catch (e) {}
}
function chiudiPaginaVol(daIndietro) {
  const box = document.getElementById('vol-sopra');
  if (box.hidden) return;
  box.hidden = true;
  document.getElementById('foglio-vol').textContent = '';
  document.documentElement.style.overflow = '';
  if (volAperto) {
    volAperto = false;
    if (!daIndietro) { try { history.back(); } catch (e) {} }
  }
}
document.getElementById('chiudi-vol').onclick = () => chiudiPaginaVol(false);
addEventListener('popstate', () => { if (volAperto) chiudiPaginaVol(true); });
addEventListener('keydown', ev => {
  if (ev.key !== 'Escape') return;
  chiudiPaginaVol(false);
  chiudiNovita();
  apriAiuto(false);
  apriLook(false);
  apriConfig(false);
});

/* ---------- la configurazione ---------- */
function apriConfig(si) {
  const buio = document.getElementById('buio-config');
  if (!buio) return;
  if (si) { chiudiNovita(); apriAiuto(false); apriLook(false); disegnaNegozi(); }
  buio.hidden = !si;
  if (si) {
    try { buio.querySelector('.finestra').scrollTop = 0; } catch (e) {}
    try { document.getElementById('chiudi-config').focus({ preventScroll: true }); } catch (e) {}
  }
}

function disegnaNegozi() {
  const box = document.getElementById('negozi');
  box.textContent = '';
  document.getElementById('avviso-negozi').textContent = '';
  const insegne = [];
  DATI.volantini.forEach(v => { if (insegne.indexOf(v.ins) < 0) insegne.push(v.ins); });
  insegne.forEach(ins => {
    const b = document.createElement('button');
    b.type = 'button';
    b.appendChild(marchio(ins));
    b.setAttribute('aria-pressed', String(!tolta(ins)));
    b.title = ins;
    b.onclick = () => {
      if (!tolta(ins) && insegne.filter(x => !tolta(x)).length <= 1) {
        /* Tolti tutti, la pagina resterebbe senza un prezzo: meglio dirlo. */
        document.getElementById('avviso-negozi').textContent =
          'Almeno un supermercato deve restare.';
        return;
      }
      tolti = tolta(ins) ? tolti.filter(x => x !== ins) : tolti.concat([ins]);
      try { localStorage.setItem(NEGOZI_TOLTI, JSON.stringify(tolti)); } catch (e) {}
      disegnaNegozi();
      disegna();
      disegnaVolantini();
      if (!document.getElementById('ricerca').hidden) { disegnaMarche(); disegnaTrovati(); }
      if (personaleAperto) disegnaPersonale();
    };
    box.appendChild(b);
  });
}

document.getElementById('apri-config').onclick = () => apriConfig(true);
document.getElementById('chiudi-config').onclick = () => apriConfig(false);
document.getElementById('buio-config').onclick = ev => {
  if (ev.target.id === 'buio-config') apriConfig(false);
};
mostraNovita();

/* Va in fondo, DOPO che «lista» e stata creata e la pagina disegnata una prima
   volta. Messo prima, chiamava disegna() quando «lista» non esisteva ancora e
   moriva li: i bottoni comparivano lo stesso (li disegnava la chiamata in
   fondo) ma sotto non usciva niente. La capacita, dove c'e, arriva comunque
   dopo il primo giro di questo script: la pagina deve funzionare gia prima e
   accendersi quando arriva. */
(async () => {
  try {
    ART = window.claude && claude.use ? await claude.use('artifact') : null;
  } catch (e) { ART = null; }
  if (ART) {
    soloMio = false;
    lista = leggiLista();
  } else {
    /* La riga sotto i bottoni dice SOLO le novità di adesso. «Questa copia è
       solo tua» è vero per sempre e stava lì a occupare due righe di schermo:
       Manlio l'ha evidenziata fra le cose da togliere. È finita dietro il
       bollino in cima, dove si va a leggere quando si vuole. */
    stato(arrivati.length ? 'Aggiunti alla tua lista: ' + arrivati.join(', ') + '.' : '');
  }
  const dv = document.getElementById('dove-vive');
  if (dv) dv.textContent = soloMio
    ? 'Questa copia è solo tua: quello che cambi resta su questo telefono.'
    : 'Questa copia è condivisa: quello che cambi lo vede anche chi ha il link.';
  aggiornaTestoLista();
  disegna();
})();
</script>'''

# ---------------------------------------------------------------------------
# Il documento contiene una copia di se stesso, cosi puo ripubblicarsi con una
# lista nuova dentro senza perdere la capacita di rifarlo la volta dopo.
#
#   CORPO    = la pagina come la vuole il servizio (senza <html>/<head>: li
#              mette lui), con dentro i due segnaposto
#   COMPLETO = lo stesso, ma documento intero: e questo che la pagina
#              ripubblica di sua iniziativa, e quindi e questo che si porta
#              dietro come modello
#
# I segnaposto restano NON risolti dentro COMPLETO: e proprio quello che
# permette alla generazione dopo di riempirli di nuovo. Prima la lista e poi il
# modello, altrimenti il modello appena infilato porta dentro un altro
# __LISTA__ e si riempie quello sbagliato.
# ---------------------------------------------------------------------------
def racchiudi(testo):
    """JSON da mettere dentro un <script>: </script> va spezzato o chiude il tag."""
    return json.dumps(testo, ensure_ascii=False).replace('</', '<\\/')

CORPO = HTML.replace('__DATI__', DATI)

INTESTA = ('<!doctype html>\n<html lang="it">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           '<style>body{margin:0}img{max-width:100%}</style>\n')
COMPLETO = (INTESTA + CORPO + '\n</body>\n</html>\n').replace(
    '</style>\n\n<div class="guscio">', '</style>\n</head>\n<body>\n<div class="guscio">', 1)

def riempi(modello):
    """Riempie SOLO la prima occorrenza di ogni segnaposto.

    I due segnaposto compaiono due volte ciascuno: una e quella vera, in cima
    allo script, l'altra e la stringa dentro documento() che serve a
    sostituirla la volta dopo. Riempiendole tutte e due si rompe documento() e
    il file cresce di 200 KB inutili. La prima e sempre quella vera, perche le
    due costanti sono dichiarate sopra la funzione; in JavaScript replace() con
    una stringa si ferma alla prima da solo, quindi le due parti si comportano
    allo stesso modo."""
    # il modello per ultimo: vedi documento() nello script, stessa trappola
    return (modello
            .replace('__LISTA__', LISTA0, 1)
            .replace('__CONDIVISA__', 'true', 1)
            .replace('__TEMPLATE__', racchiudi(COMPLETO), 1))

open('out/pagina.html', 'w', encoding='utf-8').write(riempi(CORPO))

# Copia che si apre a doppio clic, senza account e senza rete. Non puo
# ripubblicare (non c'e nessun window.claude), quindi niente modello e niente
# lista condivisa: li la lista e di chi apre e resta nel suo browser.
open('out/spesa-da-sola.html', 'w', encoding='utf-8').write(
    COMPLETO.replace('__LISTA__', LISTA0, 1)
            .replace('__TEMPLATE__', '""', 1)
            .replace('__CONDIVISA__', 'false', 1))

# ---------------------------------------------------------------------------
# La versione per il sito vero (GitHub Pages). Li dentro non esiste
# window.claude, quindi la pagina non potra mai ripubblicarsi: il modello e
# peso morto e lo si toglie (230 KB in meno). Ha invece il manifest e il suo
# service worker, per potersi installare sul telefono e funzionare in negozio
# senza segnale.
# ---------------------------------------------------------------------------
TESTA_SITO = ('<link rel="manifest" href="./manifest.webmanifest">\n'
              '<meta name="theme-color" content="#FFFFFF">\n'
              '<meta name="apple-mobile-web-app-title" content="Spesa">\n')
CODA_SITO = '''<script>
/* Un service worker suo, in questa cartella. Serve a due cose: tenere la
   pagina disponibile senza rete (in negozio il segnale e pessimo) e togliere
   di mezzo quello della Palestra, che ha lo scope sopra e senza rete
   servirebbe l'app della palestra al posto di questa. */
if ('serviceWorker' in navigator) {
  addEventListener('load', () => navigator.serviceWorker.register('./sw.js').catch(() => {}));
}
</script>
'''
sito = (COMPLETO
        .replace('<meta name="viewport" content="width=device-width, initial-scale=1">\n',
                 '<meta name="viewport" content="width=device-width, initial-scale=1">\n' + TESTA_SITO, 1)
        .replace('\n</body>\n</html>\n', '\n' + CODA_SITO + '</body>\n</html>\n', 1)
        .replace('__LISTA__', LISTA0, 1)
        .replace('__TEMPLATE__', '""', 1)
        .replace('__CONDIVISA__', 'false', 1))
open('out/sito.html', 'w', encoding='utf-8').write(sito)
print('sito:', len(sito) // 1024, 'KB (senza la copia di se stessa)')


# ---------------------------------------------------------------------------
# CONTROLLO OBBLIGATORIO, non un lusso.
#
# Il 2026-09-03 un commento conteneva il tag di chiusura dello script scritto
# per esteso. Il browser lo cerca nel testo e non gli importa che sia dentro un
# commento: ha chiuso lo script a meta e tutte e tre le pagine sono uscite
# morte, quella gia in mano a Manlio compresa. Da fuori sembravano a posto —
# intestazione, riquadri, tutto — solo senza prodotti.
#
# Qui si spezza ogni file dove il browser lo spezzerebbe e si controlla che
# ogni pezzo sia JavaScript valido e che quello grosso contenga davvero la
# funzione che disegna la pagina. Se non torna, il file NON si consegna.
# ---------------------------------------------------------------------------
def controlla(percorso):
    import re, subprocess, tempfile
    testo = open(percorso, encoding='utf-8').read()
    pezzi = re.findall(r'<script>(.*?)</script>', testo, re.S)
    if not pezzi:
        raise SystemExit(f'{percorso}: nessuno script trovato')
    for n, pezzo in enumerate(pezzi):
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as t:
            t.write(pezzo); tmp = t.name
        esito = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        os.unlink(tmp)
        if esito.returncode != 0:
            riga = esito.stderr.strip().split(chr(10))
            raise SystemExit(f'{percorso}: il pezzo {n} non e JavaScript valido\n  '
                             + chr(10).join('  ' + r for r in riga[:4]))
    if 'function disegna' not in pezzi[0]:
        raise SystemExit(f'{percorso}: lo script principale e stato tagliato prima di '
                         'disegna(). Quasi certamente c\'e un tag di chiusura scritto '
                         'per esteso in un commento o in una stringa.')
    print(f'  {os.path.basename(percorso):24s} {len(pezzi)} script, tutti validi')

print('controllo che le pagine non siano spezzate:')
for f in ('out/pagina.html', 'out/sito.html', 'out/spesa-da-sola.html'):
    controlla(f)

print('scritta —', len(riempi(CORPO)) // 1024, 'KB;', len(partenza), 'prodotti in lista,',
      len(offerte), 'prezzi,', len(pagine), 'pagine indicizzate')
