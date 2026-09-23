# -*- coding: utf-8 -*-
"""I dati letti a mano dai volantini, uno per uno, guardando le pagine.

Ogni riga:
  categoria, insegna, chiave del volantino, reparto, prodotto, formato,
  quantità, prezzo, pagina del PDF, fonte, note

Il prezzo per unità NON si scrive qui: si calcola prezzo/quantità, così non
può mai essere in disaccordo col prezzo. L'unità la decide la categoria
(UNITA qui sotto): il latte si confronta al litro, le uova all'uovo, la carta
igienica al rotolo e il detersivo al lavaggio. Confrontare tutto al chilo
darebbe numeri veri ma inutili.

Fonte V = letto dal volantino. Fonte D = preso da un riassunto online e mai
verificato: nella pagina esce marcato «da controllare», perché di riassunti
sbagliati ne ho già trovati tre.
"""
V = 'letto dal volantino'
D = 'DA CONTROLLARE (riassunto online)'

# LE CATEGORIE E LE LORO UNITÀ STANNO IN catalogo.py, NON QUI.
# Erano scritte qui in una lista a parte, e a ogni categoria nuova bisognava
# ricordarsi di aggiungerla in due posti; la seconda volta che ce ne si
# dimentica, il programma si ferma con un errore che non dice niente.
# Adesso l'unico posto è il catalogo, che è anche quello che Manlio e la
# moglie vedono nel cassetto.
from catalogo import UNITA, NOMI
from pagine_mercato import PAGINE_MERCATO, PAGINE_MERCATO_17
from pagine_ekom import PAGINE_EKOM_08, PAGINE_EKOM_22

# I volantini sono namedtuple e non tuple nude di proposito: il 2026-09-05 e
# servito aggiungere un campo (l'inizio) e gli otto punti che le spacchettavano
# per posizione sarebbero saltati tutti insieme. Con i nomi, chi non usa il
# campo nuovo non se ne accorge.
#
# chiave, insegna, periodo leggibile, nome del PDF, ultimo giorno, INDIRIZZO DELLA PAGINA,
# primo giorno (facoltativo: se manca, il volantino e gia in corso)
#
# L'ultimo campo e l'indirizzo pubblico di una singola pagina del volantino, con
# {n} al posto del numero: serve a rendere cliccabili le righe della pagina, cosi
# Manlio apre il volantino al punto giusto invece di leggere «pagina 16» e
# arrangiarsi. Le due fonti numerano diversamente: anteprimavolantino riempie di
# zeri (a volte due cifre, a volte cinque, dipende dal volantino), volantinopiu
# no. Vanno ricontrollati a ogni volantino nuovo insieme alle date.
# L'ultimo giorno serve a due cose: sapere quando andare a prendere il volantino
# nuovo (il giorno prima), e buttare via il vecchio due giorni dopo, come ha
# chiesto Manlio per non ritrovarsi una collezione. Se non e stampato sul
# volantino si mette la stima e si scrive «stimato» nel periodo.
_AV = 'https://www.anteprimavolantino.it/public/uploads'
_VP = 'https://resources.volantinopiu.it/flyer'

from collections import namedtuple as _nt

Volantino = _nt('Volantino', 'chiave insegna periodo pdf fino indirizzo inizio pagine')
Volantino.__new__.__defaults__ = (None, None)   # inizio: se manca, e gia in corso

# «pagine» serve a un volantino solo, Mercato: la sua fonte firma ogni immagine
# con un codice calcolato sull'indirizzo, quindi lo schema con {n} non esiste e
# gli indirizzi vanno elencati uno per uno (pagine_mercato.py). Dove c'e questa
# lista vince lei; dove manca si usa l'indirizzo a schema, come sempre.

def _v(*campi):
    return Volantino(*campi)

# I volantini che si scaricano da un PDF invece che pagina per pagina (Conad):
# scarica.py prende il PDF e ne fa le immagini. L'indirizzo in VOLANTINI resta
# quello da aprire sul telefono, pagina per pagina.
PDF = {
 'conad24': 'https://www.conad.it/assets/common/volantini/cno/v20262/20262620PCONADPIEMONTE.pdf',
}

VOLANTINI = [
 _v('bennet10',       'Bennet',         'dal 10 al 23 settembre',                       'Bennet — 10-23 settembre.pdf',                      '2026-09-23', _AV + '/2026/09/volantino-bennet-2026-09-10-p-{n:05d}.jpg'),

 # In arrivo: letti in anticipo, con la data d'inizio. Fino a quel giorno la
 # pagina li segna «dal ...» invece di farli passare per offerte di oggi.
 # eurospin10 (10-20 settembre) scaduto e tolto il 2026-09-23: copertura senza
 # buchi passata a eurospin24 dal giorno stesso in cui e scaduto.
 _v('eurospin24',     'Eurospin',       'dal 24 settembre al 4 ottobre',                'Eurospin — 24 settembre-4 ottobre.pdf',            '2026-10-04', _AV + '/2026/09/volantino-eurospin-2026-09-24-p-{n:05d}.jpg', '2026-09-24'),
 # md08 (8-20 settembre) scaduto e tolto il 2026-09-23: copertura passata a md22.
 _v('carriper15',     'Carrefour Iper', 'dal 15 al 28 settembre',                       'Carrefour Iper — 15-28 settembre.pdf',              '2026-09-28', _AV + '/2026/09/volantino-carrefour-iper-2026-09-15-p-{n:05d}.jpg', '2026-09-15'),
 _v('lidl17',         'Lidl',           'dal 17 al 23 settembre',                       'Lidl — 17-23 settembre.pdf',                        '2026-09-23', _AV + '/2026/09/volantino-lidl-2026-09-17-p-{n:05d}.jpg',       '2026-09-17'),
 _v('lidlfv17',       'Lidl',           'speciale Frutta e Verdura, dal 17 al 23 settembre', 'Lidl Frutta e Verdura — 17-23 settembre.pdf',      '2026-09-23', _AV + '/2026/09/volantino-lidl-frutta-e-verdura-2026-09-17-p-{n:05d}.jpg', '2026-09-17'),
 _v('mercato17',      'Mercatò',        'dal 17 al 30 settembre',                       'Mercatò — 17-30 settembre.pdf',                    '2026-09-30', None, '2026-09-17', PAGINE_MERCATO_17),
 _v('ekom08',         'Ekom',           '1+1, dall\'8 al 21 settembre',                 'Ekom 1+1 — 8-21 settembre.pdf',                     '2026-09-21', None, None, PAGINE_EKOM_08),
 _v('md22',           'MD',             "dal 22 settembre al 4 ottobre",                'MD — 22 settembre-4 ottobre.pdf',                  '2026-10-04', _AV + '/2026/09/volantino-md-2026-09-22-p-{n:02d}.jpg',       '2026-09-22'),
 # Trovato il 2026-09-18, letto per intero il 2026-09-19: un Bennet nuovo,
 # "Un mondo di bellezza", uscito mentre bennet10 (10-23) era ancora valido —
 # la stessa sovrapposizione che ha già fatto perdere sei giorni col "Dolce
 # Buongiorno" di settembre. Non è solo bellezza: da pagina 18 in poi ha
 # alimentari, surgelati e casa: 27 pagine lette, 14 scartate (in scartate.py).
 _v('bennet1709',     'Bennet',         '"Un mondo di bellezza", dal 17 al 30 settembre', 'Bennet — 17-30 settembre.pdf',                    '2026-09-30', _AV + '/2026/09/volantino-bennet-2026-09-17-p-{n:05d}.jpg',   '2026-09-17'),
 # Annunciato il 21/9 (VOLANTINI_ATTESI), pagine pubblicate il 22/9: letto in
 # anticipo, comincia il 24 (lidl17 scade il 23, nessun buco).
 _v('lidl24',         'Lidl',           'dal 24 al 30 settembre',                       'Lidl — 24-30 settembre.pdf',                        '2026-09-30', _AV + '/2026/09/volantino-lidl-2026-09-24-p-{n:05d}.jpg',       '2026-09-24'),
 # «I più ekonomici», visto da Manlio di carta il 19/9, online dal 22/9 su
 # ekomdiscount.it (non più kimbino: vedi pagine_ekom.py). ekom08 e' scaduto
 # il 21, quindi un giorno di buco (il 21) gia passato quando si legge questo.
 # IPERCOOP «Extra offerte», dal 24 settembre al 7 ottobre. Trovato il 22/9
 # sul canale Nova Coop di volantinopiu: era gia caricato ma non ancora
 # mostrato nell'elenco pubblico del negozio, e si e trovato interrogando gli
 # id uno per uno su ipercoop.volantinopiu.com/volantino<id>00pv24.html.
 # ATTENZIONE: Nova Coop stampa QUATTORDICI edizioni diverse dello stesso
 # volantino, una per zona, e i prezzi di qualche riga cambiano fra l'una e
 # l'altra (il latte Arborea va da 1,39 a 1,45). La zona e scritta sul
 # frontespizio. La nostra e la PRIMA, id 28831, «TORINO - COLLEGNO».
 # Le altre: 28832 Novara, 28833 Borgomanero, 28834 Casale, 28835 Borgosesia,
 # 28836 Chieri, 28837 Cirie, 28838 Cuorgne, 28839 Cuneo, 28840 Crevoladossola,
 # 28841 Pinerolo, 28842 Biella, 28843 Gravellona Toce, 28844 Beinasco.
 _v('ipercoop24',    'Ipercoop',       '«Extra offerte», dal 24 settembre al 7 ottobre', 'Ipercoop «Extra offerte» — 24 settembre-7 ottobre.pdf', '2026-10-07', _VP + '/2/8/8/3/1/pagine/{n}.jpg', '2026-09-24'),
 _v('ekom22',         'Ekom',           '«I più ekonomici», dal 22 settembre al 5 ottobre', 'Ekom «I più ekonomici» — 22 settembre-5 ottobre.pdf', '2026-10-05', None, '2026-09-22', PAGINE_EKOM_22),
 # PAM, la nona insegna, chiesta da Manlio il 2026-09-22 («a Torino ce ne sono
 # tantissimi»). Il più vicino a corso Siracusa è il Pam di CORSO ORBASSANO 212
 # (a 400 metri), un Pam «normale», non Panorama né Local.
 # Pam mette i volantini su volantinopiu come Nova Coop, e la sua app li
 # chiede a coeus.ppapi.it per NEGOZIO: per corso Orbassano (store 71, codice
 # pv 2311) il 10-23 settembre dava 28606 «PAM Supermercati - Sotto Prezzo» e
 # 28609 «PAM Supermercati - Occasioni Extra». I Panorama hanno id loro
 # (28603-28605, 28607-28608), con prezzi loro: non vanno confusi.
 # Quelli dal 24 non erano ancora nell'elenco del negozio il 22: trovati
 # chiedendo gli id uno per uno su pam.volantinopiu.com/volantino<id>00pv2311.html,
 # come per l'Ipercoop. I «PAM Supermercati» sono 28807 e 28849; 28804-28806,
 # 28808-28810 e 28848 sono Panorama.
 _v('pam24',          'Pam',            '«Tante offerte a 1, 2, 3 euro», dal 24 settembre al 7 ottobre', 'Pam — 24 settembre-7 ottobre.pdf', '2026-10-07', _VP + '/2/8/8/0/7/pagine/{n}.jpg', '2026-09-24'),
 _v('pamextra24',     'Pam',            '«Occasioni Extra», dal 24 settembre al 7 ottobre', 'Pam «Occasioni Extra» — 24 settembre-7 ottobre.pdf', '2026-10-07', _VP + '/2/8/8/4/9/pagine/{n}.jpg', '2026-09-24'),
 # CONAD, la decima insegna, chiesta da Manlio il 2026-09-22 («a Torino c'è
 # anche Conad»). Il più vicino a corso Siracusa è il CONAD di VIA CESANA 78
 # (2,7 km; codice negozio «anacanId» 009843), un Conad «normale»: i Conad
 # City (via Bardonecchia, 3,3 km) e i Superstore hanno volantini loro.
 # FONTE UFFICIALE: la scheda del negozio su conad.it elenca i volantini, che
 # stanno sul sito Conad stesso in PDF:
 #   https://www.conad.it/ricerca-negozi/conad-via-cesana-78-10139-torino--009843
 # Il collegamento di ogni riga porta al PDF sul sito Conad alla sua pagina
 # (#page=n). scarica.py sa leggere questi PDF: lo scarica una volta e ne fa
 # le immagini delle pagine.
 # IL COLLEGAMENTO NON È IL PDF (Manlio, 2026-09-23: «il volantino Conad non fa
 # vedere la pagina ma il volantino completo»). Sul telefono il PDF con
 # «#page=n» si apre dall'inizio, o si scarica: il numero di pagina si perde.
 # Il sito Conad ha il suo visore (Yumpu, su volantini.conad.it) e lì ogni
 # pagina ha un indirizzo suo: .../<id>/<n>. L'id e il nome si leggono nella
 # pagina del volantino su conad.it («Guarda il volantino», i tasti di
 # condivisione). Il PDF serve solo a scaricare le pagine: sta in PDF qui sotto.
 _v('conad24',        'Conad',          '«Freschi di convenienza», dal 24 settembre al 7 ottobre', 'Conad — 24 settembre-7 ottobre.pdf', '2026-10-07', 'https://volantini.conad.it/volantino-freschi-di-convenienza-conad-piemonte/71286440/{n}', '2026-09-24'),
 # Il foglio «Perché conviene» (conad.it/.../vperch/PERCHECONVIENEPPN20PI.pdf)
 # ripete tre offerte di conad24 agli stessi prezzi (detersivo ACE, crudo
 # Assisi, olio Conad): non è un volantino a parte, guardato e lasciato fuori.
]

# VOLANTINI CHE SO ESSERE IN ARRIVO, ma che non ho ancora letto.
# Non hanno prezzi e non entrano in nessun confronto: servono solo alla
# tabella in fondo alla pagina delle Novità, chiesta da Manlio il 2026-09-19
# («una tabellina con tutti i supermercati e l'intervallo di validità dei loro
# volantini presenti e di quelli che sai anche futuri»). Senza questi, un buco
# di quattro giorni fra un volantino e il successivo sembrerebbe un buco vero
# anche quando so gia che verra coperto.
#
# Si tolgono di qui appena il volantino viene letto ed entra in VOLANTINI:
# `dati.py` si ferma se un attesa ha la stessa insegna e le stesse date di un
# volantino vero, cosi non puo restare il doppione.
Atteso = _nt('Atteso', 'insegna periodo inizio fino dove')

VOLANTINI_ATTESI = [
    # Vuota: l'Ipercoop che stava qui e' stato letto il 2026-09-22 ed e'
    # passato in VOLANTINI come `ipercoop24`. Si rimette qui dentro un
    # volantino solo quando SO che sta per uscire e non l'ho ancora letto.
]

for _a in VOLANTINI_ATTESI:
    for _v2 in VOLANTINI:
        if _a.insegna == _v2.insegna and (_a.inizio, _a.fino) == (_v2.inizio, _v2.fino):
            raise SystemExit('volantino atteso gia letto, toglilo da VOLANTINI_ATTESI: '
                             + _a.insegna + ' ' + _a.periodo)

PRODOTTI = [
 # ------------------------------- CARNE DI BUE (kg) -------------------------------
 # ------------------------------- TONNO (kg) -------------------------------
 # ------------------------------- SALMONE (kg) -------------------------------
 # ------------------------------- CAFFÈ (kg) -------------------------------
 # ------------------------------- LATTE (litri) -------------------------------
 # ------------------------------- PASTA (kg) -------------------------------
 # ------------------------------- OLIO D'OLIVA (litri) -------------------------------
 # ------------------------------- POLLO (kg) -------------------------------
 # ------------------------------- FORMAGGIO (kg) -------------------------------
 # ------------------------------- UOVA (uova) -------------------------------
 # ------------------------------- CARTA IGIENICA (rotoli) -------------------------------
 # ------------------------------- DETERSIVO (lavaggi) -------------------------------
 # ------------------------------- SUINO (kg) -------------------------------
 # Ci stanno sia i tagli freschi sia i salumi: sono tutti maiale, e il formato
 # di ogni riga dice cos'e. Se un domani vuole separarli, basta una categoria in piu.
 # ------------------------------- BISCOTTI (kg) -------------------------------
 # ------------------------------- YOGURT (kg) -------------------------------
 # ------------------------------- MARMELLATA (kg) -------------------------------
 # ------------------------------- CIOCCOLATO (kg) -------------------------------
 # ------------------------------- MERLUZZO E BACCALÀ (kg) -------------------------------
 # ------------------------------- RISO (kg) -------------------------------
 # ------------------------------- PANE (kg) -------------------------------
 # ------------------------------- POMODORO E PASSATA (kg) -------------------------------
 # ------------------------------- OLIO DI SEMI (litri) -------------------------------
 # ------------------------------- LEGUMI IN SCATOLA (kg) -------------------------------
 # ------------------------------- SUGHI PRONTI (kg) -------------------------------
 # ------------------------------- VERDURE IN SCATOLA (kg) -------------------------------
 # ------------------------------- MERENDINE (kg) -------------------------------
 # ------------------------------- MIELE (kg) -------------------------------
 # ------------------------------- VERDURE SURGELATE (kg) -------------------------------
 # ------------------------------- PIZZA SURGELATA (kg) -------------------------------
 # ------------------------------- FRUTTA (kg) -------------------------------
 # ------------------------------- VERDURA (kg) -------------------------------
 # ------------------------------- INSALATA IN BUSTA (kg) -------------------------------
 # ------------------------------- PATATE (kg) -------------------------------
 # ------------------------------- ACQUA (litri) -------------------------------
 # ------------------------------- VINO (litri) -------------------------------
 # ------------------------------- BIRRA (litri) -------------------------------
 # ------------------------------- SUCCHI E BIBITE (litri) -------------------------------
 # ------------------------------- SAPONE E BAGNOSCHIUMA (litri) -------------------------------
 # ------------------------------- DENTIFRICIO (litri) -------------------------------
 # ------------------------------- BURRO (kg) -------------------------------
 # ------------------------------- CALAMARI E SEPPIE (kg) -------------------------------
 # ------------------------------- BASTONCINI DI PESCE (kg) -------------------------------
 # ------------------------------- GELATO (kg) -------------------------------
 # ============================ MERCATÒ, 3-16 settembre ============================
 # Letto pagina per pagina il 2026-09-05, dal volantino «La convenienza migliore
 # dell'anno». La pagina scritta qui è quella STAMPATA in basso sul foglio.
 # «Solo con Fidelity Card» è nelle note dove il volantino lo dice: senza la
 # tessera quel prezzo non si paga, ed è un'informazione che serve in cassa.
 # I prezzi del banco sono stampati all'etto: qui stanno al chilo, come tutti
 # gli altri, così si confrontano davvero.
 # ===================== PESCE E DINTORNI, letti il 2026-09-05 =====================
 # Manlio: «continuo a notare una poca quantita di offerte di merluzzo e di
 # gamberi». Aveva ragione, ed era di nuovo un buco mio: gamberi zero e merluzzo
 # due, con sette volantini in casa. La pescheria del Bennet (pagina 3) e la
 # pagina «Pesce» del Carrefour non le avevo mai aperte.

 # Trovati sulle stesse pagine mentre cercavo il pesce: non buttarli via.
 # ----- Mercatò, le pagine che il primo giro aveva saltato (lette il 2026-09-05) -----
 # Birra, vino, merendine, sapone: quattro categorie che per Mercatò erano vuote
 # e che stavano tutte dietro pagine mai aperte.
 # ------------------------------- PESCE FRESCO (kg) -------------------------------
 # Voce nuova del 2026-09-05: prima queste offerte le vedevo e le lasciavo fuori
 # perche non avevano dove stare. Sono al banco o surgelate, e il prezzo al kg
 # del banco viene dai cartellini all'etto, moltiplicati per dieci.
 # ----- Carrefour Iper, le 39 pagine mai aperte (lette il 2026-09-07) -----
 # Il volantino era a 11 pagine lette su 50. Qui ci sono tutte le altre.
 # La copertina dice «DAL 4 AL 13 SETTEMBRE»: la fine non e piu una stima.
 # ----- Bennet «Dolce Buongiorno», 3-16 settembre (letto per intero il 2026-09-07) -----
 # Volantino a tema colazione che non c'era in dati.py: e uscito il 3 settembre,
 # mentre il Bennet vecchio era ancora valido, e nessuno se n'era accorto perche
 # il controllo giornaliero guarda solo le scadenze, non gli arrivi.
 # BC = solo con la carta Bennet Club.
 # Molti prodotti a marchio Bennet non sono scontati: e il prezzo di listino, e
 # in cambio danno un buono del 50% da spendere dal 17 al 30 settembre. Il conto
 # usa il prezzo che si paga in cassa, non il buono.
 # I prodotti a marchio Bennet non sono scontati: e il prezzo di listino, e in
 # cambio danno un buono del 50% da spendere dal 17 al 30 settembre. Il conto usa
 # il prezzo che si paga in cassa: il buono e uno sconto sulla spesa DOPO.
 # ------------------------------- BENNET10 (10-23 settembre 2026) -------------------------------
 # Il volantino generale e per lo piu sconti percentuali su intere linee di marca,
 # senza prezzo di base: pagine scartate (vedi scartate.py). I prezzi veri stanno
 # nelle pagine del banco fresco, pescheria, frutta e verdura, panetteria, e nella
 # sezione «prodotto acceleratore». La pagina Oktoberfest (20-21) vale fino al 4
 # ottobre, non fino al 23: date sue.
 ("Formaggio","Bennet","bennet10","Salumi","Taleggio DOP – Mauri","al kg",1,11.90,14,V,"Al banco."),
 ("Prosciutto","Bennet","bennet10","Salumi","Prosciutto crudo","al kg",1,15.90,14,V,"Al banco."),
 ("Formaggio","Bennet","bennet10","Salumi","Formaggio duro Grangusto","al kg",1,11.90,14,V,"Al banco."),
 ("Prosciutto","Bennet","bennet10","Salumi","Prosciutto cotto alta qualità Riccafetta – Raspini","al kg",1,15.90,14,V,"Al banco."),
 ("Formaggio","Bennet","bennet10","Salumi","Formaggio Scimudin","al kg",1,11.90,14,V,"Al banco."),
 ("Formaggio","Bennet","bennet10","Salumi","Mu' di Bruna","al kg",1,13.90,14,V,"Al banco."),
 ("Mortadella","Bennet","bennet10","Salumi","Mortadella al pistacchio con cotenna – Felsineo","al kg",1,13.90,14,V,"Al banco."),
 ("Pancetta","Bennet","bennet10","Salumi","Guanciale","al kg",1,14.90,14,V,"Al banco."),
 ("Salame","Bennet","bennet10","Salumi","Salame di Milano – Citterio","al kg",1,19.90,14,V,"Al banco."),
 ("Bresaola","Bennet","bennet10","Salumi","Bresaola Angus – Gardani","al kg",1,39.90,14,V,"Al banco."),
 ("Manzo","Bennet","bennet10","Macelleria","Roastbeef a fette di bovino adulto – Filiera Valore Bennet","al kg",1,20.89,15,V,""),
 ("Tacchino","Bennet","bennet10","Macelleria","Fesa di tacchino a fette","al kg",1,10.59,15,V,""),
 ("Suino","Bennet","bennet10","Macelleria","Cotolette e nodini di suino italiano – Filiera Valore Bennet","al kg",1,6.99,15,V,""),
 ("Vitello","Bennet","bennet10","Macelleria","Coscia a pezzi di vitello","al kg",1,17.99,15,V,""),
 ("Suino","Bennet","bennet10","Macelleria","Bistecche di suino","al kg",1,6.99,15,V,""),
 ("Vitello","Bennet","bennet10","Macelleria","Reale con osso di vitello","al kg",1,9.49,15,V,""),
 ("Manzo","Bennet","bennet10","Macelleria","Polpa per tonnato di bovino adulto","al kg",1,18.99,15,V,""),
 ("Manzo","Bennet","bennet10","Macelleria","Hamburger piemontese – Casa Vercelli","200 g",0.200,4.49,15,V,""),
 ("Pollo","Bennet","bennet10","Macelleria","Pollo busto – AIA","al kg",1,5.19,15,V,""),
 ("Pollo","Bennet","bennet10","Macelleria","Buona Domenica – Amadori","700 g",0.700,6.20,15,V,"Ripieno di verdure e formaggio."),
 ("Patate","Bennet","bennet10","Ortofrutta","Patate del Fucino IGP","kg 1,5",1.5,2.19,16,V,""),
 ("Verdura","Bennet","bennet10","Ortofrutta","Carote – Filiera Valore Bennet","kg 1",1,1.15,16,V,""),
 ("Frutta","Bennet","bennet10","Ortofrutta","Kiwi polpa gialla Sungold – Zespri","500 g",0.500,3.18,16,V,""),
 ("Frutta","Bennet","bennet10","Ortofrutta","Mele Sweetango – Melinda","kg 3",3,3.45,16,V,""),
 ("Verdura","Bennet","bennet10","Ortofrutta","Funghi champignon bianchi","500 g",0.500,1.95,16,V,""),
 ("Insalata","Bennet","bennet10","Ortofrutta","Insalata coleslaw – Ortoromi","200 g",0.200,0.95,16,V,""),
 ("Verdura","Bennet","bennet10","Ortofrutta","Radicchio rosso – Ortoromi","175 g",0.175,1.35,16,V,""),
 ("Pane","Bennet","bennet10","Panetteria","Focaccia mini alle olive","al kg",1,11.50,17,V,""),
 ("Pane","Bennet","bennet10","Panetteria","Focaccia mini classica","al kg",1,11.50,17,V,""),
 ("Pane","Bennet","bennet10","Panetteria","Pagnotta con lievito madre","al kg",1,4.70,17,V,""),
 ("Pesce","Bennet","bennet10","Pescheria","Orata","al kg",1,8.90,18,V,""),
 ("Pesce","Bennet","bennet10","Pescheria","Filetto di persico africano","al kg",1,15.90,18,V,""),
 ("Salmone","Bennet","bennet10","Pescheria","Scaloppa di salmone tagli pregiati – Selezione del pescatore","al kg",1,23.90,18,V,""),
 ("Tonno","Bennet","bennet10","Pescheria","Trancio di tonno a pinne gialle marinato decongelato","140 g",0.140,7.90,18,V,""),
 ("Gamberi","Bennet","bennet10","Pescheria","Code di gambero argentino congelate","kg 2",2,36.90,18,V,""),
 ("Pesce","Bennet","bennet10","Pescheria","Filetto di pesce spada decongelato marinato","al kg",1,20.90,18,V,""),
 ("Pesce","Bennet","bennet10","Pescheria","Polpo decongelato","al kg",1,19.90,18,V,""),
 ("Gamberi","Bennet","bennet10","Pescheria","Mazzancolle tropicali precotte 80/100","kg 1",1,9.90,18,V,""),
 ("Pesce","Bennet","bennet10","Pescheria","Branzino agli aromi","al kg",1,21.50,18,V,""),
 ("Pesce","Bennet","bennet10","Pescheria","Vongole veraci cotte al naturale","500 g",0.500,19.90,18,V,"Già cotte, non crude."),
 ("Pesce","Bennet","bennet10","Pescheria","Cozze cotte al naturale","800 g",0.800,6.90,18,V,"Già cotte, non crude."),
 ("Pesce","Bennet","bennet10","Pescheria","Vongole lupini cotte al naturale","500 g",0.500,6.90,18,V,"Già cotte, non crude."),
 ("Frutta","Bennet","bennet10","Ortofrutta","Uva bianca o rossa senza semi – Filiera Valore Bennet","750 g",0.750,2.65,19,V,""),
 ("Frutta","Bennet","bennet10","Ortofrutta","Uva da tavola nera Palieri","al kg",1,1.95,19,V,""),
 ("Frutta","Bennet","bennet10","Ortofrutta","Uva di Mazzarrone IGP","al kg",1,2.55,19,V,""),
 ("Frutta","Bennet","bennet10","Ortofrutta","Uva da tavola Pizzutella bianca","al kg",1,2.55,19,V,""),
 ("Frutta","Bennet","bennet10","Ortofrutta","Uva da tavola Red Globe","al kg",1,1.95,19,V,""),
 ("Suino","Bennet","bennet10","Macelleria","Carré di suino affumicato","250 g",0.250,3.59,20,V,"Affumicato. Offerta Oktoberfest, valida fino al 4 ottobre, non fino al 23 come il resto del volantino.",None,"2026-10-04"),
 ("Suino","Bennet","bennet10","Macelleria","Costine di suino affumicate","al kg",1,11.59,20,V,"Affumicate. Offerta Oktoberfest, valida fino al 4 ottobre.",None,"2026-10-04"),
 ("Birra","Bennet","bennet10","Bevande","Birra Weissbier – Kapuziner","500 ml",0.500,1.99,20,V,"Offerta Oktoberfest, valida fino al 4 ottobre.",None,"2026-10-04"),
 ("Birra","Bennet","bennet10","Bevande","Birra Weisoktoberfest 5,7° – Edinger","500 ml",0.500,1.29,20,V,"Offerta Oktoberfest, valida fino al 4 ottobre.",None,"2026-10-04"),
 ("Birra","Bennet","bennet10","Bevande","Birra Oktoberfest HB, con bicchiere","1,5 litri (3 × 500 ml)",1.5,5.89,20,V,"Offerta Oktoberfest, valida fino al 4 ottobre.",None,"2026-10-04"),
 ("Birra","Bennet","bennet10","Bevande","Birra Hofbräu München","500 ml",0.500,1.19,20,V,"Tipi vari. Offerta Oktoberfest, valida fino al 4 ottobre.",None,"2026-10-04"),
 ("Birra","Bennet","bennet10","Bevande","Birra Hell – Benediktiner","500 ml",0.500,1.19,21,V,"Offerta Oktoberfest, valida fino al 4 ottobre.",None,"2026-10-04"),
 ("Birra","Bennet","bennet10","Bevande","Birra Oktoberfest – Paulaner","500 ml",0.500,1.39,21,V,"Offerta Oktoberfest, valida fino al 4 ottobre. Sul volantino compare anche una seconda confezione a 1,49.",None,"2026-10-04"),
 ("Birra","Bennet","bennet10","Bevande","Weissbier Augustiner Bräu München, con bicchiere","1,5 litri (3 × 500 ml)",1.5,9.89,21,V,"Offerta Oktoberfest, valida fino al 4 ottobre.",None,"2026-10-04"),
 ("Ricotta","Bennet","bennet10","Freschi","Ricotta fresca – Caseificio Pini","330 g",0.330,1.49,22,V,""),
 ("Mozzarella","Bennet","bennet10","Freschi","Mozzarella «Oggi Puoi» Benessere – Granarolo","300 g (3 × 100 g)",0.300,2.99,22,V,""),
 ("Formaggio","Bennet","bennet10","Freschi","Stracchino – Nonno Nanni","200 g",0.200,2.79,22,V,""),
 ("Uova","Bennet","bennet10","Freschi","Uova fresche da allevamento a terra medie – Le Naturelle","10 uova",10,2.93,22,V,""),
 ("Yogurt","Bennet","bennet10","Freschi","Muu Muu – Cameo","460 g (4 × 115 g)",0.460,2.68,22,V,""),
 ("Pasta","Bennet","bennet10","Freschi","Pasta per lasagne fresche all'uovo – Giovanni Rana","250 g",0.250,1.99,22,V,""),
 ("Verdure surgelate","Bennet","bennet10","Surgelati","Coccole surgelate – Bonduelle","300 g",0.300,2.47,22,V,"Tortini di verdure."),
 ("Patate","Bennet","bennet10","Surgelati","Patatine surgelate Kid Smile – McCain","650 g",0.650,2.95,22,V,"Surgelate."),
 ("Verdure surgelate","Bennet","bennet10","Surgelati","Minestrone tradizione con pasta – Findus","450 g",0.450,2.80,22,V,""),
 ("Gamberi","Bennet","bennet10","Surgelati","Mazzancolle tropicali in tempura surgelate – Oggi Pesce","200 g",0.200,3.99,22,V,"Impanate in tempura."),
 ("Sughi","Bennet","bennet10","Surgelati","Sugo surgelato spaghettata di mare – Esca","400 g",0.400,3.99,22,V,""),
 ("Tonno","Bennet","bennet10","Dispensa","Filetto di tonno rosa – Rizzoli","400 g",0.400,5.99,23,V,""),
 ("Pasta","Bennet","bennet10","Dispensa","Riccioli all'ortolana o maccheroncini tricolore – Di Bari","500 g",0.500,1.39,23,V,""),
 ("Biscotti","Bennet","bennet10","Colazione","Biscotti Mini Animals – Milka","99,5 g",0.0995,1.19,23,V,""),
 ("Biscotti","Bennet","bennet10","Colazione","Biscotti artigianali – Artebianca","250 g",0.250,1.74,23,V,""),
 ("Biscotti","Bennet","bennet10","Colazione","Biscotti rustici integrali – Cabrioni","650 g",0.650,1.98,23,V,""),
 ("Bibite","Bennet","bennet10","Bevande","Coca Cola Original o Zero","3,3 litri (10 × 330 ml)",3.3,4.89,23,V,""),
 ("Vino","Bennet","bennet10","Bevande","Cannonau di Sardegna, Alghero Rosato o Vermentino DOC – Sella & Mosca","750 ml",0.750,3.98,23,V,""),
 ("Vino","Bennet","bennet10","Bevande","Spumante Brut Diamante – Bosio","750 ml",0.750,2.99,23,V,""),
 ("Birra","Bennet","bennet10","Bevande","Birra Corona classica o analcolica","330 ml",0.330,1.19,23,V,""),
 ("Birra","Bennet","bennet10","Bevande","Birra Corona","500 ml",0.500,1.49,23,V,""),
 ("Dentifricio","Bennet","bennet10","Igiene","Dentifricio – Parodontax","75 ml",0.075,2.99,24,V,"Tipi vari."),
 ("Dentifricio","Bennet","bennet10","Igiene","Dentifricio – Oral B","225 ml (3 × 75 ml)",0.225,4.89,24,V,""),
 ("Shampoo","Bennet","bennet10","Igiene","Shampoo – I Provenzali","250 ml",0.250,2.69,24,V,"Tipi vari."),
 ("Shampoo","Bennet","bennet10","Igiene","Balsamo – Elvive","250 ml",0.250,2.99,24,V,"Tipi vari."),
 ("Shampoo","Bennet","bennet10","Igiene","Shampoo o balsamo – Pantene Pro-V","500 ml",0.500,4.79,24,V,"Tipi vari."),
 ("Bagnoschiuma","Bennet","bennet10","Igiene","Bagnodoccia – Dermomed","650 ml",0.650,1.49,24,V,"Tipi vari."),
 ("Bagnoschiuma","Bennet","bennet10","Igiene","Docciaschiuma Advanced Care – Dove","225 ml",0.225,1.95,24,V,""),
 ("Bagnoschiuma","Bennet","bennet10","Igiene","Sapone liquido mani – Palmolive","600 ml (2 × 300 ml)",0.600,2.99,24,V,""),
 ("Lavatrice","Bennet","bennet10","Casa","Detersivo liquido per lavatrice – Ace","2 × 27 lavaggi",54,6.99,25,V,""),
 ("Lavatrice","Bennet","bennet10","Casa","Detersivo in polvere per lavatrice – Bio Presto","62 lavaggi",62,9.88,25,V,""),
 ("Ammorbidente","Bennet","bennet10","Casa","Ammorbidente concentrato – Coccolino","87 lavaggi",87,3.98,25,V,""),
 ("Lavastoviglie","Bennet","bennet10","Casa","Detersivo in caps per lavastoviglie – Finish","65 lavaggi",65,12.90,25,V,"Confezioni da 65, 70 o 77 lavaggi allo stesso prezzo: preso il numero più basso."),
 ("Burro","Bennet","bennet10","Freschi","Burro italiano – Beppino Occelli","125 g",0.125,3.59,30,V,""),
 ("Burro","Bennet","bennet10","Freschi","Metà metà burro e vegetale – Prealpi","250 g",0.250,2.98,30,V,""),
 ("Ricotta","Bennet","bennet10","Freschi","Ricottine «Oggi Puoi» – Granarolo","200 g (2 × 100 g)",0.200,1.69,30,V,""),
 ("Mozzarella","Bennet","bennet10","Freschi","Mozzarella in sfoglia – Bayernland","130 g",0.130,1.99,30,V,""),
 ("Formaggio","Bennet","bennet10","Freschi","Formaggio fuso pastorizzato – Tigre","140 g (6 spicchi)",0.140,2.99,30,V,""),
 ("Sughi","Bennet","bennet10","Dispensa","Pesto alla genovese «Che sugo!» – Biffi","140 g",0.140,2.98,30,V,""),
 ("Verdure surgelate","Bennet","bennet10","Surgelati","Carciofi trifolati surgelati – Pagnan","300 g",0.300,2.99,30,V,""),
 ("Gelato","Bennet","bennet10","Surgelati","Magnum bomboniera classic o almond – Algida","104 g",0.104,4.19,30,V,""),
 ("Gelato","Bennet","bennet10","Surgelati","Maxibon classic – Nestlé","384 g (conf. da 4)",0.384,5.49,30,V,""),
 ("Acqua","Bennet","bennet10","Bevande","Acqua minerale naturale – Lauretana","3 litri (6 × 500 ml)",3,2.45,30,V,""),
 ("Vino","Bennet","bennet10","Bevande","Valdobbiadene Prosecco Superiore DOCG – Casa Sant'Orsola","750 ml",0.750,9.49,30,V,""),
 ("Olio d'oliva","Bennet","bennet10","Dispensa","Olio extravergine di oliva DOP – Col di Fiore","750 ml",0.750,9.90,31,V,""),
 ("Riso","Bennet","bennet10","Dispensa","Riso Bomba Oro di Spagna – Vignola","500 g",0.500,5.99,31,V,""),
 ("Birra","Bennet","bennet10","Bevande","Birra Strong Ale o Extreme Ten – Ceres","500 ml",0.500,1.99,31,V,""),
 ("Bagnoschiuma","Bennet","bennet10","Igiene","Bagnoschiuma – Dove","700 ml",0.700,4.99,31,V,"Tipi vari."),
 ("Merendine","Bennet","bennet10","Colazione","Buondì – Bauli","276 g (conf. da 6)",0.276,2.19,31,V,"Farcito albicocca o ricoperto al cioccolato."),
 # ------------------------------- LIDL10 (10-16 settembre 2026) -------------------------------
 # Volantino intero di prezzi veri (non sconti percentuali). Alcune pagine hanno
 # date proprie diverse dal resto: «da giovedì a domenica» (10-13), il
 # Sottocosto (fino al 12), e un blocco Italiamo/«il meglio del lunedì» che
 # comincia il 14. I prodotti del Sottocosto già letti nel vecchio volantino
 # 'lidl' (Tonno Rio Mare, Latte Parmalat, Tortellini Fini, Yogurt Granarolo,
 # Passata Mutti, Pizza Cameo, Birra Beck's, Mozzarella Granarolo) non si
 # ripetono qui: sono la stessa offerta, non una nuova.
 # ------------------------------- MD08, pagine lette il 2026-09-10 -------------------------------
 # ------------------------------- EUROSPIN10, pagine lette il 2026-09-10 -------------------------------
 # Pagina «Doppio Weekend di follia»: due finestre corte con date proprie
 # (11-13 e 18-20 settembre), diverse dal resto del volantino (10-20).

 # ---- Carrefour Iper, 15-28 settembre: letto per intero, 50/50 pagine ----
 # È in gran parte «Grandi Marche», sconti percentuali su intere linee senza
 # prezzo di base (pagine 1-11): scartate, vedi scartate.py. I prezzi veri
 # stanno nelle pagine di carne, pesce, salumi, formaggi, ortofrutta e in
 # alcune pagine di alimentari confezionati e bevande.
 ("Manzo","Carrefour Iper","carriper15","Macelleria","Carpaccio di bovino adulto","al kg",1,19.99,12,V,"−29%, prima 28,49."),
 ("Manzo","Carrefour Iper","carriper15","Macelleria","Hamburger di bovino adulto","al kg",1,12.99,12,V,"−20%, prima 16,29."),
 ("Vitello","Carrefour Iper","carriper15","Macelleria","Macinata di vitello","al kg",1,13.99,12,V,""),
 ("Vitello","Carrefour Iper","carriper15","Macelleria","Spezzatino di vitello, confezione risparmio","al kg",1,15.99,12,V,"−20%, prima 19,99."),
 ("Suino","Carrefour Iper","carriper15","Macelleria","Lonza di suino a fette, confezione risparmio","al kg",1,6.49,12,V,"−48%, prima 12,49. Comprando il taglio intero costa 5,49 al kg."),
 ("Suino","Carrefour Iper","carriper15","Macelleria","Hamburger misti di suino, conf. 6 pezzi","600 g",0.600,5.99,12,V,"−25%, prima 7,99."),
 ("Pollo","Carrefour Iper","carriper15","Macelleria","Petto di pollo a fette – Aia","al kg",1,9.89,12,V,"−32%, prima 14,76."),
 ("Pollo","Carrefour Iper","carriper15","Macelleria","Fusi e sovracosce di pollo, conf. 6 pezzi","al kg",1,4.99,12,V,"−28%, prima 6,99. Comprando 2 kg o più costa 3,99 al kg."),
 ("Salmone","Carrefour Iper","carriper15","Pescheria","Trancio di salmone allevato in Norvegia","al kg",1,16.90,13,V,"−22%, prima 21,90. Senza uso di antibiotici."),
 ("Pesce","Carrefour Iper","carriper15","Pescheria","Branzino","al kg",1,8.49,13,V,"−43%, prima 14,90. Comprando 3 kg o più costa 7,99 al kg."),
 ("Gamberi","Carrefour Iper","carriper15","Pescheria","Mazzancolle tropicali cotte","al kg",1,10.90,13,V,"−26%, prima 14,90. Già cotte. Comprando 2 kg o più costa 8,90 al kg."),
 ("Calamari","Carrefour Iper","carriper15","Pescheria","Tentacolo di totano gigante, decongelato","al kg",1,8.90,13,V,"−25%, prima 11,90."),
 ("Merluzzo","Carrefour Iper","carriper15","Surgelati","5 filetti di merluzzo d'Alaska – Frosta","340 g",0.340,3.99,19,V,"−43%, prima 7,00. Surgelato."),
 ("Pancetta","Carrefour Iper","carriper15","Salumi","Pancetta Piacentina DOP","al kg",1,17.90,15,V,"−20%, prima 2,25 all'etto."),
 ("Mortadella","Carrefour Iper","carriper15","Salumi","Mortadella Bologna IGP – Bonomia","al kg",1,11.90,15,V,"−25%, prima 15,90 al kg. Comprando 3 etti o più costa 10,90 al kg."),
 ("Prosciutto","Carrefour Iper","carriper15","Salumi","Prosciutto Cotto Alta Qualità 1956 – Ferrarini","al kg",1,19.90,15,V,"−20%, prima 2,49 all'etto."),
 ("Prosciutto","Carrefour Iper","carriper15","Salumi","Prosciutto Crudo – Fattorie del Gennargentu","al kg",1,21.99,16,V,"−30%, prima 3,19 all'etto."),
 ("Salame","Carrefour Iper","carriper15","Salumi","Salame Nostrano Bortolotti","al kg",1,17.50,15,V,"−20%, prima 2,19 all'etto."),
 ("Salsiccia","Carrefour Iper","carriper15","Salumi","Salsiccia di Fonni – Fattorie del Gennargentu","al kg",1,13.93,16,V,"−30%, prima 1,99 all'etto. Solo con la tessera SpesAmica Payback."),
 ("Bresaola","Carrefour Iper","carriper15","Salumi","Bresaola della Valtellina IGP – Beretta","70 g",0.070,2.99,17,V,"−33%, prima 4,47. Solo con la tessera SpesAmica Payback."),
 ("Grana","Carrefour Iper","carriper15","Freschi","Grana Padano DOP grattugiato – Latteria Soresina","100 g",0.100,1.29,17,V,"−43%, prima 2,27. Solo con la tessera SpesAmica Payback."),
 ("Grana","Carrefour Iper","carriper15","Salumi","Parmigiano Reggiano DOP stagionato 22 mesi, confezione famiglia","al kg",1,18.90,15,V,"Comprando 2 kg o più costa 17,90 al kg."),
 ("Formaggio","Carrefour Iper","carriper15","Salumi","Gorgonzola DOP – Terre d'Italia","al kg",1,12.70,15,V,"−20%, prima 1,59 all'etto."),
 ("Formaggio","Carrefour Iper","carriper15","Salumi","Leerdammer","al kg",1,13.50,15,V,"−20%, prima 1,69 all'etto."),
 ("Mozzarella","Carrefour Iper","carriper15","Freschi","Mozzarella Valfiorita – Bayernland, conf. 3 pezzi","300 g (3 × 100 g)",0.300,1.79,17,V,"−28%, prima 2,49."),
 ("Uova","Carrefour Iper","carriper15","Freschi","Uova da allevamento a terra – Le Naturelle, conf. 10 pezzi","10 uova",10,2.49,18,V,"−37%, prima 3,99."),
 ("Olio d'oliva","Carrefour Iper","carriper15","Dispensa","Olio extravergine di oliva – Ulisse Clemente","1 litro",1,4.59,23,V,"−45%, prima 8,35. Solo con la tessera SpesAmica Payback."),
 ("Tonno","Carrefour Iper","carriper15","Dispensa","Tonno all'olio di oliva – As do Mar, conf. 8 pezzi","560 g (8 × 70 g)",0.560,6.99,23,V,"−43%, prima 12,27."),
 ("Tonno","Carrefour Iper","carriper15","Dispensa","Tonno naturale zero olio – Nostromo, conf. 6 pezzi","336 g (6 × 65 g)",0.336,3.99,23,V,"−50%, prima 7,99. È al naturale, non all'olio. Solo con la tessera SpesAmica Payback."),
 ("Biscotti","Carrefour Iper","carriper15","Colazione","Biscotti Oro Saiwa","1 kg",1,2.29,22,V,"Comprando 3 pezzi o più costa 1,99 al pezzo."),
 ("Marmellata","Carrefour Iper","carriper15","Dispensa","Confetture Bio – Rigoni di Asiago","330 g",0.330,3.39,22,V,"−26%, prima 4,59. Solo con la tessera SpesAmica Payback."),
 ("Miele","Carrefour Iper","carriper15","Dispensa","Miele dosatore – Millefiori","400 g",0.400,2.69,22,V,"−21%, prima 3,41."),
 ("Cioccolato","Carrefour Iper","carriper15","Colazione","Tavoletta fondente −30% di zuccheri – Novi","100 g",0.100,2.29,21,V,"−22%, prima 2,94."),
 ("Cioccolato","Carrefour Iper","carriper15","Colazione","Tavolette nocciolato – Milka","95 g",0.095,1.29,50,V,"«96 ore scontate», valido solo dal 24 al 27 settembre, non per tutto il volantino. −40%, prima 2,15.","2026-09-24","2026-09-27"),
 ("Yogurt","Carrefour Iper","carriper15","Freschi","Yogurt bianco magro – Müller, conf. 8 pezzi","1 kg (8 × 125 g)",1,2.29,18,V,"−28%, prima 3,19."),
 ("Latte","Carrefour Iper","carriper15","Freschi","Latte UHT parzialmente scremato – Polenghi","1 litro",1,0.69,18,V,"−45%, prima 1,26."),
 ("Caffè","Carrefour Iper","carriper15","Colazione","Macinato Granaroma – Vergnano, conf. 4 pezzi","1 kg (4 × 250 g)",1,13.59,21,V,"−32%, prima 19,99. Solo con la tessera SpesAmica Payback."),
 ("Gelato","Carrefour Iper","carriper15","Surgelati","Carte D'Or Classic – Algida","500 g",0.500,2.99,20,V,"−40%, prima 4,99. Solo con la tessera SpesAmica Payback."),
 ("Frutta","Carrefour Iper","carriper15","Ortofrutta","Mele Golden sfuse","al kg",1,0.89,14,V,"−50%, prima 1,79. Comprando 3 kg o più costa 0,79 al kg."),
 ("Verdura","Carrefour Iper","carriper15","Ortofrutta","Pomodoro Datterino","500 g",0.500,1.99,14,V,"−25%, prima 2,66."),
 ("Patate","Carrefour Iper","carriper15","Ortofrutta","Patate al selenio, rete 1,5 kg","al kg",1,1.79,14,V,"−20%, prima 2,24 al kg."),
 ("Pomodoro","Carrefour Iper","carriper15","Dispensa","Passata Vellutata – Delverde","690 g",0.690,0.89,24,V,"−40%, prima 1,49."),
 ("Riso","Carrefour Iper","carriper15","Dispensa","Riso Carnaroli – El Ris de Milan","2 kg",2,4.90,24,V,""),
 ("Acqua","Carrefour Iper","carriper15","Bevande","Acqua minerale naturale o frizzante – Boario, conf. 6 pezzi","9 litri (6 × 1,5 l)",9,1.79,25,V,"−35%, prima 2,76. Solo con la tessera SpesAmica Payback."),
 ("Birra","Carrefour Iper","carriper15","Bevande","Birra in lattina – Tuborg","500 ml",0.500,0.99,29,V,""),
 ("Vino","Carrefour Iper","carriper15","Bevande","Rosso o Bianco Terre Siciliane IGT – Corvo","750 ml",0.750,3.99,26,V,"−30%, prima 5,70. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- LIDL 17-23 SETTEMBRE -------------------------------
 ("Manzo","Lidl","lidl17","Macelleria","Hamburger di bovino","400 g",0.400,4.29,1,V,"Prima 5,79. Allevato in Italia. Il volantino stampa 10,73 al kg."),
 ("Latte","Lidl","lidl17","Latteria","Latte parzialmente scremato UHT XXL","6 x 1 litro",6,4.69,1,V,"Formato convenienza XXL: il formato base costa 1,19 al litro, questo 0,78."),
 ("Uova","Lidl","lidl17","Latteria","Uova fresche medie – Maia","24 uova",24,4.99,1,V,"Da allevamento a terra. 1 uovo = 0,21€."),
 ("Pollo","Lidl","lidl17","Macelleria","Filetto di petto di pollo a fette","400 g",0.400,3.19,2,V,"Con Lidl Plus, prima 4,59. Valido solo dal 17 al 20 settembre, non per tutto il volantino.","2026-09-17","2026-09-20"),
 ("Prosciutto","Lidl","lidl17","Salumi","Prosciutto crudo stagionato – Dal Salumiere","150 g",0.150,1.99,2,V,"Minimo 11 mesi di stagionatura. Prima 2,99. Valido solo dal 17 al 20 settembre, non per tutto il volantino.","2026-09-17","2026-09-20"),
 ("Mozzarella","Lidl","lidl17","Latteria","Burrata – Italiamo","2x200 g",0.400,2.39,2,V,"1+1: un pezzo da solo costa 2,39, prima 4,78 la confezione doppia. Valido solo dal 17 al 20 settembre. È burrata, non mozzarella tonda.","2026-09-17","2026-09-20"),
 ("Bibite","Lidl","lidl17","Bevande","Coca-Cola","4x1,75 l",7,5.89,3,V,"Valido solo dal 17 al 20 settembre, non per tutto il volantino.","2026-09-17","2026-09-20"),
 ("Frutta","Lidl","lidl17","Ortofrutta","Uva bianca da tavola di Mazzarrone IGP","1 kg confezione",1,1.99,4,V,"Prima 2,79."),
 ("Verdura","Lidl","lidl17","Ortofrutta","Carote del Fucino IGP","800 g confezione",0.800,1.19,4,V,"Prima 1,59."),
 ("Frutta","Lidl","lidl17","Ortofrutta","Pesche","al kg",1,1.89,5,V,"Con Lidl Plus, prima 2,49. Valido solo dal 17 al 20 settembre, non per tutto il volantino.","2026-09-17","2026-09-20"),
 ("Salsiccia","Lidl","lidl17","Macelleria","Salsiccia di tacchino con suino e pollo","450 g",0.450,2.29,6,V,"Prima 2,99."),
 ("Tacchino","Lidl","lidl17","Macelleria","Macinato di tacchino","400 g",0.400,2.99,6,V,"Prima 3,99."),
 ("Tacchino","Lidl","lidl17","Macelleria","Bocconcini di fesa di tacchino","400 g",0.400,3.59,6,V,"Prima 4,59."),
 ("Pollo","Lidl","lidl17","Macelleria","Kebab di pollo","350 g",0.350,2.99,6,V,"Con Lidl Plus, prima 3,99."),
 ("Pollo","Lidl","lidl17","Macelleria","Cotoletta di pollo con scamorza affumicata","200 g",0.200,2.19,7,V,""),
 ("Pollo","Lidl","lidl17","Macelleria","Panzerotti di pollo con provola e speck","220 g",0.220,2.29,7,V,""),
 ("Suino","Lidl","lidl17","Macelleria","Lonza di maiale, trancio intero","al kg",1,4.99,7,V,""),
 ("Pesce","Lidl","lidl17","Gastronomia","Tentacoli di polpo scottati – Gastronomia di Mare","250 g",0.250,7.99,7,V,"Già scottati, pronti. Prima 9,99."),
 ("Gamberi","Lidl","lidl17","Pesce","Mazzancolle XXL – Ocean Sea","300 g",0.300,4.79,8,V,"Sgusciate e scottate, surgelate. Formato XXL, 60 g in più rispetto al formato base."),
 ("Suino","Lidl","lidl17","Macelleria","Fettine di coppa di suino senza osso XXL","1 kg confezione",1,7.49,8,V,"Formato convenienza XXL."),
 ("Salmone","Lidl","lidl17","Pesce","Filetti di salmone con pelle XXL","8x125 g",1,17.49,8,V,"Formato convenienza XXL, nel banco pesce."),
 ("Pancetta","Lidl","lidl17","Salumi","Pancetta a cubetti XXL – Salumeo","2x120 g",0.240,2.19,8,V,"Formato XXL, 40 g in più rispetto al formato base."),
 ("Merluzzo","Lidl","lidl17","Surgelati","Merluzzo d'Alaska panato XXL","500 g",0.500,4.49,8,V,"Panato, surgelato. Formato convenienza XXL."),
 ("Pane","Lidl","lidl17","Panetteria","Piadina Romagnola IGP alla Riminese XXL – Italiamo","720 g",0.720,1.69,9,V,"Formato XXL, 120 g in più rispetto al formato base."),
 ("Pasta","Lidl","lidl17","Dispensa","Pasta fresca all'uovo ripiena XXL – Nonna Mia","300 g",0.300,1.19,9,V,"Cappelletti al prosciutto crudo o tortelloni ricotta e spinaci. Formato XXL, 50 g in più."),
 ("Pasta","Lidl","lidl17","Dispensa","Gnocchi di patate XXL – Nonna Mia","600 g",0.600,1.39,9,V,"Formato XXL, 100 g in più."),
 ("Conserve","Lidl","lidl17","Dispensa","Cetriolini XXL – Freshona","360 g (sgocc.)",0.360,1.69,10,V,"All'aceto di vino. Formato XXL, sgocciolato."),
 ("Sughi","Lidl","lidl17","Dispensa","Pesto alla Genovese XXL – Baresa","290 g",0.290,1.49,10,V,"Formato convenienza XXL."),
 ("Olio di semi","Lidl","lidl17","Dispensa","Olio di semi vari XXL – Vita d'Or","5 litri",5,7.99,10,V,"Formato convenienza XXL."),
 ("Tonno","Lidl","lidl17","Dispensa","Tonno all'olio di semi di girasole XXL – Nixe","6x52 g (sgocc.)",0.312,3.69,10,V,"Formato convenienza XXL, sgocciolato."),
 ("Merendine","Lidl","lidl17","Colazione","Mini croissant XXL – Realforno","250 g",0.250,1.29,11,V,"Formato XXL, 50 g in più."),
 ("Creme","Lidl","lidl17","Colazione","Crema spalmabile alla nocciola XXL – Choco Nussa","1 kg",1,3.99,11,V,"Formato convenienza XXL."),
 ("Cioccolato","Lidl","lidl17","Colazione","Kinder Bueno","258 g",0.258,3.99,11,V,"Formato convenienza, con pezzi extra in omaggio."),
 ("Vino","Lidl","lidl17","Bevande","Pinot Grigio delle Venezie DOC – Giulio Pasotti","0,75 litri",0.750,2.39,12,V,"Vino bianco secco. Prima 2,99."),
 ("Vino","Lidl","lidl17","Bevande","Mures Nero di Troia Rosé Puglia IGP – Cantina di Ruvo di Puglia","0,75 litri",0.750,2.29,12,V,"Vino rosato. Prima 2,99."),
 ("Vino","Lidl","lidl17","Bevande","Prosecco DOC – Allini","0,75 litri",0.750,3.19,12,V,"Con Lidl Plus. Vino spumante extra dry. Prima 3,99."),
 ("Formaggio","Lidl","lidl17","Latteria","Emmental francese – Milbona","250 g",0.250,1.79,12,V,"Con Lidl Plus. Formaggio a pasta dura. Prima 2,35."),
 ("Prosciutto","Lidl","lidl17","Salumi","Prosciutto cotto alta qualità – Dal Salumiere","125 g",0.125,1.19,12,V,"Con Lidl Plus. Prima 1,55."),
 ("Bresaola","Lidl","lidl17","Salumi","Bresaola della Valtellina IGP, Punta d'Anca – Dal Salumiere","100 g",0.100,2.79,13,V,"Con Lidl Plus. Prima 3,49."),
 ("Pollo","Lidl","lidl17","Salumi","Petto di pollo cotto al forno – Dal Salumiere","120 g",0.120,1.89,13,V,"Solo carne italiana. È petto di pollo cotto (un salume), non carne fresca. Prima 2,49."),
 ("Pancetta","Lidl","lidl17","Salumi","Pancetta coppata – Dal Salumiere","90 g",0.090,1.69,13,V,"Con Lidl Plus. Prima 2,15."),
 ("Salame","Lidl","lidl17","Salumi","Ventricina piccante a fette – Dal Salumiere","100 g",0.100,1.11,13,V,"Prima 1,49."),
 ("Merluzzo","Lidl","lidl17","Surgelati","Burger di merluzzo d'Alaska – Ocean Sea","210 g",0.210,1.79,13,V,"Con Lidl Plus. Prima 2,29."),
 ("Verdure surgelate","Lidl","lidl17","Surgelati","Pisellini Primavera – Findus","660 g",0.660,3.19,13,V,"Con Lidl Plus. Prima 4,19."),
 ("Mozzarella","Lidl","lidl17","Latteria","Mozzarella High Protein – Latteria","3x100 g",0.300,2.49,17,V,"Multipack."),
 ("Yogurt","Lidl","lidl17","Latteria","Kefir Shot – Milbona","600 g",0.600,1.99,17,V,"Bevanda a base di kefir con succo di frutta ai frutti misti o alla fragola."),
 ("Birra","Lidl","lidl17","Bevande","Birra analcolica – Finkbräu","4x0,5 l",2,1.47,14,V,"Con Lidl Plus. 3+1: un pezzo da solo costa 0,49. Prima 1,96 la confezione. Senza alcol."),
 ("Sughi","Lidl","lidl17","Dispensa","Gran Pesto alla Genovese – Star Tigullio","190 g",0.190,1.69,15,V,"Classico o senza aglio. Prima 2,19."),
 ("Birra","Lidl","lidl17","Bevande","Strong lager, birra doppio malto – Tennent's Super","0,355 litri",0.355,1.39,15,V,"9% Vol. Prima 1,79."),
 ("Gelato","Lidl","lidl17","Surgelati","Gelato variegato al triplo cioccolato – Bon Gelati","522 g",0.522,2.19,15,V,"Prima 2,89."),
 ("Gelato","Lidl","lidl17","Surgelati","Gelato variegato al tiramisù – Bon Gelati","515 g",0.515,2.19,15,V,"Prima 2,89."),
 ("Marmellata","Lidl","lidl17","Colazione","Confettura extra pesca – Maribel","425 g",0.425,1.19,15,V,"Con Lidl Plus. 50% di frutta. Prima 1,55."),
 ("Dentifricio","Lidl","lidl17","Igiene","Dentifricio Tripla protezione menta fresca – Aquafresh","125 ml",0.125,1.49,15,V,"Prima 1,99."),
 ("Frutta","Lidl","lidl17","Ortofrutta","Pere Williams","1 kg confezione",1,1.79,36,V,"Prima 2,49. Valido solo dal 21 al 23 settembre, non per tutto il volantino.","2026-09-21","2026-09-23"),
 ("Patate","Lidl","lidl17","Ortofrutta","Patate Selenella","1,5 kg rete",1.5,2.29,36,V,"Prima 2,99. Valido solo dal 21 al 23 settembre, non per tutto il volantino.","2026-09-21","2026-09-23"),
 ("Verdura","Lidl","lidl17","Ortofrutta","Zucca Butternut","al kg",1,1.19,36,V,"Con Lidl Plus, prima 1,69. Valido solo dal 21 al 23 settembre, non per tutto il volantino.","2026-09-21","2026-09-23"),

 # Lidl, speciale Frutta e Verdura dal 17 al 23 settembre (7 pagine, letto per
 # intero). Tre prodotti della sua pagina «Il meglio del lunedì» (Pere Williams,
 # Patate Selenella, Zucca Butternut) e altri tre (Uva bianca di Mazzarrone,
 # Carote del Fucino, Pesche) ripetono identici, stesso prezzo, quelli già
 # letti nel volantino Lidl generale 17-23: non riscritti qui, sennò dati.py
 # si ferma per riga doppia. Cetrioli lunghi, Mango e Fichi freschi sono al
 # pezzo, senza un peso: nessun prezzo per unità onesto da scrivere.
 ("Frutta","Lidl","lidlfv17","Ortofrutta","Mele Golden Alto Adige IGP, formato XXL","2,5 kg confezione",2.5,2.99,1,V,"500 g in più, formato base 2 kg a 2,99. Il volantino stampa 1,20 al kg, prima 1,50."),
 ("Verdura","Lidl","lidlfv17","Ortofrutta","Cavolo rosso","al kg",1,0.98,1,V,""),
 ("Frutta","Lidl","lidlfv17","Ortofrutta","Susine, formato XXL","1,25 kg confezione",1.25,1.79,1,V,"250 g in più, formato base 1 kg a 1,79. Il volantino stampa 1,43 al kg."),
 ("Frutta","Lidl","lidlfv17","Ortofrutta","Pere Carmen","1 kg confezione",1,1.99,2,V,"Con Lidl Plus, prima 2,49. Valido dal 17 al 20 settembre, non per tutto il volantino.","2026-09-17","2026-09-20"),
 ("Verdura","Lidl","lidlfv17","Ortofrutta","Aglio","200 g confezione",0.200,0.98,3,V,"Il volantino stampa 4,90 al kg."),
 ("Verdura","Lidl","lidlfv17","Ortofrutta","Cavolo cappuccio","al kg",1,0.98,3,V,""),
 ("Verdura","Lidl","lidlfv17","Ortofrutta","Rape rosse precotte","500 g confezione",0.500,0.98,3,V,"Precotte, non crude. Il volantino stampa 1,96 al kg."),
 ("Frutta","Lidl","lidlfv17","Ortofrutta","Mele Golden","al kg",1,0.98,3,V,""),
 ("Verdura","Lidl","lidlfv17","Ortofrutta","Cetrioli snack","250 g confezione",0.250,1.15,5,V,"Con Lidl Plus, prima 1,49. Il volantino stampa 4,60 al kg."),
 ("Frutta","Lidl","lidlfv17","Ortofrutta","Uva scura senza semi","500 g confezione",0.500,1.39,5,V,"Con Lidl Plus, prima 1,79. Il volantino stampa 2,78 al kg."),
 ("Frutta","Lidl","lidlfv17","Ortofrutta","Mele Sweet Tango","900 g confezione",0.900,1.49,5,V,"Con Lidl Plus, prima 1,99. Il volantino stampa 1,66 al kg."),
 ("Frutta","Lidl","lidlfv17","Ortofrutta","Limoni","1 kg rete",1,1.89,5,V,"Con Lidl Plus, prima 2,49."),

 # Mercatò, dal 17 al 30 settembre. Letto per intero, 20 pagine.
 ("Salmone","Mercatò","mercato17","Gastronomia","Salmone affumicato scozzese – Hendricks","100 g",0.100,3.89,1,V,"Il volantino stampa 38,90 al kg."),
 ("Vino","Mercatò","mercato17","Bevande","Prosecco Superiore Valdobbiadene DOCG Millesimato Extra Dry – Maschio","750 ml",0.750,4.98,1,V,"Il volantino stampa 6,64 al litro."),
 ("Carta igienica","Mercatò","mercato17","Cura casa","Carta igienica kilometrica Maxi Convenienza 12 rotoli – Tenderly","12 rotoli",12,5.79,1,V,""),
 ("Formaggio","Mercatò","mercato17","Gastronomia","Gorgonzola DOP – Dolce Tosi","al kg (al banco)",1,10.90,2,V,"Al banco, 1,09 all'etto."),
 ("Ricotta","Mercatò","mercato17","Gastronomia","Ricotta del Boscaiolo – Longo","al kg (al banco)",1,3.90,2,V,"Al banco, 0,39 all'etto."),
 ("Formaggio","Mercatò","mercato17","Gastronomia","Fiandino Selezione","al kg (al banco)",1,12.90,2,V,"Al banco, 1,29 all'etto."),
 ("Formaggio","Mercatò","mercato17","Gastronomia","Provola bianca – San Vincenzo","al kg (al banco)",1,9.80,2,V,"Al banco, 0,98 all'etto."),
 ("Formaggio","Mercatò","mercato17","Gastronomia","Tronchetto di capra stagionato – Cabrifin Laita","al kg (al banco)",1,14.50,2,V,"Al banco, 1,45 all'etto."),
 ("Formaggio","Mercatò","mercato17","Gastronomia","Emmental francese – President","al kg (al banco)",1,9.90,2,V,"Al banco, 0,99 all'etto."),
 ("Formaggio","Mercatò","mercato17","Gastronomia","Pecorino DOP – Galluradoro","al kg (al banco)",1,18.90,2,V,"Al banco, 1,89 all'etto."),
 ("Formaggio","Mercatò","mercato17","Gastronomia","Dimarella da tavola morbida","al kg (al banco)",1,9.50,2,V,"Al banco, 0,95 all'etto."),
 ("Formaggio","Mercatò","mercato17","Gastronomia","Raschera DOP","al kg (al banco)",1,9.90,2,V,"Al banco, 0,99 all'etto."),
 ("Formaggio","Mercatò","mercato17","Gastronomia","Stracchino Stella Bianca","al kg (al banco)",1,8.90,2,V,"Al banco, 0,89 all'etto."),
 ("Formaggio","Mercatò","mercato17","Gastronomia","La Tuma d'Martiniana – Val Form","al kg (al banco)",1,9.90,2,V,"Al banco, 0,99 all'etto."),
 ("Formaggio","Mercatò","mercato17","Gastronomia","Toma – La Bergera Osella","al kg (al banco)",1,10.90,2,V,"Al banco, 1,09 all'etto."),
 ("Formaggio","Mercatò","mercato17","Gastronomia","Primo sale – Valform","al kg (al banco)",1,7.90,2,V,"Al banco, 0,79 all'etto."),
 ("Formaggio","Mercatò","mercato17","Gastronomia","Tomini vari tipi","al kg (al banco)",1,14.90,2,V,"Al banco, 1,49 all'etto."),
 ("Formaggio","Mercatò","mercato17","Freschi","Burrata Deliziosa in foglia","250 g",0.250,3.59,2,V,"Il volantino stampa 14,36 al kg."),
 ("Prosciutto","Mercatò","mercato17","Gastronomia","Prosciutto cotto magro e morbido – Lenti","al kg (al banco)",1,10.50,3,V,"Al banco, 1,05 all'etto."),
 ("Prosciutto","Mercatò","mercato17","Gastronomia","Speck IGP Alto Adige","al kg (al banco)",1,13.90,3,V,"Al banco, 1,39 all'etto."),
 ("Pancetta","Mercatò","mercato17","Gastronomia","Pancetta magra coppata – Cavalier Umberto Boschi","al kg (al banco)",1,14.90,3,V,"Al banco, 1,49 all'etto."),
 ("Salame","Mercatò","mercato17","Gastronomia","Salame Milano – Citterio","al kg (al banco)",1,15.90,3,V,"Al banco, 1,59 all'etto."),
 ("Tacchino","Mercatò","mercato17","Gastronomia","Tacchino arrosto Monte San Savino, senza antibiotici","al kg (al banco)",1,14.90,3,V,"Al banco, 1,49 all'etto."),
 ("Mortadella","Mercatò","mercato17","Gastronomia","Mortadella IGP – Negroni","al kg (al banco)",1,8.90,3,V,"Al banco, 0,89 all'etto."),
 ("Pane","Mercatò","mercato17","Gastronomia","Patapane","al kg",1,3.38,3,V,""),
 ("Manzo","Mercatò","mercato17","Macelleria","Rolatine di bovino adulto","al kg",1,22.39,4,V,""),
 ("Manzo","Mercatò","mercato17","Macelleria","Scamone di bovino adulto","al kg",1,22.99,4,V,""),
 ("Suino","Mercatò","mercato17","Macelleria","Costina di suino piemontese","al kg",1,8.98,4,V,""),
 ("Suino","Mercatò","mercato17","Macelleria","Capocollo senz'osso di suino a fette, confezione convenienza","al kg",1,9.29,4,V,"Origine Italia."),
 ("Pollo","Mercatò","mercato17","Macelleria","Controfiletto di pollo – La Fattoria delle Cose Buone","300 g",0.300,3.39,4,V,"Il volantino stampa 11,30 al kg."),
 ("Pollo","Mercatò","mercato17","Macelleria","Cotolette o cordon bleu di pollo – Gusto Ricco","400 g",0.400,1.99,4,V,"Vari tipi. Il volantino stampa 4,98 al kg."),
 ("Pollo","Mercatò","mercato17","Macelleria","Coscette di pollo dalle Langhe allevato senza l'uso di antibiotici","al kg",1,7.99,4,V,""),
 ("Calamari","Mercatò","mercato17","Pescheria","Tentacoli di totano decongelato","al kg",1,10.90,4,V,""),
 ("Merluzzo","Mercatò","mercato17","Pescheria","Filetto di baccalà bagnato – Aquolina","400 g",0.400,13.90,4,V,"Il volantino stampa 34,75 al kg."),
 ("Pesce","Mercatò","mercato17","Pescheria","Cozza / mitilo – La Spezia","al kg",1,4.90,4,V,""),
 ("Pesce","Mercatò","mercato17","Pescheria","Branzino 4/6, allevato Italia","al kg",1,13.90,4,V,""),
 ("Vino","Mercatò","mercato17","Bevande","Gavi DOCG – Duchessa Lia","750 ml",0.750,5.69,4,V,"Il volantino stampa 7,59 al litro."),
 ("Verdura","Mercatò","mercato17","Ortofrutta","Broccoletti","al kg",1,1.99,5,V,"Origine Italia. Valido dal 17 al 23 settembre, non per tutto il volantino.","2026-09-17","2026-09-23"),
 ("Frutta","Mercatò","mercato17","Ortofrutta","Banane – Dole","al kg",1,1.49,5,V,"Valido dal 17 al 23 settembre, non per tutto il volantino.","2026-09-17","2026-09-23"),
 ("Insalata","Mercatò","mercato17","Ortofrutta","Rucola – Natura Chiama Selex","150 g",0.150,0.99,5,V,"Valido dal 17 al 23 settembre, non per tutto il volantino. Il volantino stampa 6,60 al kg.","2026-09-17","2026-09-23"),
 ("Verdura","Mercatò","mercato17","Ortofrutta","Finocchi","800 g",0.800,1.69,5,V,"Origine Italia. Valido dal 17 al 23 settembre, non per tutto il volantino.","2026-09-17","2026-09-23"),
 ("Frutta","Mercatò","mercato17","Ortofrutta","Uva bianca senza semi – Saper di Sapori","500 g",0.500,1.99,5,V,"Origine Italia. Valido dal 17 al 23 settembre, non per tutto il volantino.","2026-09-17","2026-09-23"),
 ("Verdura","Mercatò","mercato17","Ortofrutta","Pomodori cuore di bue","al kg",1,2.49,5,V,"Origine Italia. Valido dal 24 al 30 settembre, non per tutto il volantino.","2026-09-24","2026-09-30"),
 ("Frutta","Mercatò","mercato17","Ortofrutta","Fichi d'India dell'Etna DOP – Saper di Sapori","800 g",0.800,1.99,5,V,"Origine Italia. Valido dal 24 al 30 settembre, non per tutto il volantino.","2026-09-24","2026-09-30"),
 ("Frutta","Mercatò","mercato17","Ortofrutta","Kiwi Hayward – Zespri Green","al kg",1,4.99,5,V,"Valido dal 24 al 30 settembre, non per tutto il volantino.","2026-09-24","2026-09-30"),
 ("Patate","Mercatò","mercato17","Ortofrutta","Patate per tutti gli usi – Natura Chiama Selex","1,5 kg",1.5,1.75,5,V,"Valido dal 24 al 30 settembre, non per tutto il volantino.","2026-09-24","2026-09-30"),
 ("Frutta","Mercatò","mercato17","Ortofrutta","Mele Golden Delicious – Melinda","al kg",1,1.69,5,V,"Origine Italia. Valido dal 24 al 30 settembre, non per tutto il volantino.","2026-09-24","2026-09-30"),
 ("Vino","Mercatò","mercato17","Bevande","Frappato Terre Siciliane IGT – Cardilla","750 ml",0.750,3.98,6,V,"Il volantino stampa 5,31 al litro."),
 ("Tonno","Mercatò","mercato17","Dispensa","Tonno all'olio di oliva – Selex","420 g (70 g × 6)",0.420,5.79,7,V,"Il volantino stampa 13,79 al kg."),
 ("Verdure surgelate","Mercatò","mercato17","Surgelati","Tortini di verdure con spinaci, piselli e mozzarella – Selex","200 g",0.200,1.69,7,V,"Il volantino stampa 8,45 al kg."),
 ("Pomodoro","Mercatò","mercato17","Dispensa","Passata pomodoro – Selex","600 g (200 g × 3)",0.600,0.95,7,V,"Il volantino stampa 1,58 al kg."),
 ("Pane","Mercatò","mercato17","Dispensa","Piadina con farina integrale – Selex","225 g (3 pezzi)",0.225,1.14,7,V,"Il volantino stampa 5,07 al kg."),
 ("Tè","Mercatò","mercato17","Dispensa","Camomilla solubile con melatonina – Selex","64 g (16 buste)",0.064,1.69,7,V,"Il volantino stampa 26,41 al kg."),
 ("Biscotti","Mercatò","mercato17","Colazione","Savoiardi – Selex","300 g",0.300,1.34,7,V,"Il volantino stampa 4,47 al kg."),
 ("Bastoncini","Mercatò","mercato17","Surgelati","Bastoncini di merluzzo surgelati, formato convenienza 24+6 gratis – Findus","750 g",0.750,6.59,10,V,"Il volantino stampa 8,79 al kg."),
 ("Gelato","Mercatò","mercato17","Surgelati","Gelato Barattolino Delizioso – Sammontana","500 g",0.500,2.99,10,V,"Vari tipi. Il volantino stampa 5,98 al kg."),
 ("Acqua","Mercatò","mercato17","Bevande","Acqua naturale – Sant'Anna","1 litro",1,0.31,11,V,""),
 ("Bibite","Mercatò","mercato17","Bevande","Coca-Cola, bottiglia 1,5 litri","1,5 litri",1.5,1.85,11,V,"Vari tipi (Original, Zero, Lemon)."),
 ("Grana","Mercatò","mercato17","Freschi","Grana Padano DOP grattugiato Riserva – Saper di Sapori","80 g",0.080,1.39,8,V,"Il volantino stampa 17,38 al kg."),
 ("Formaggio","Mercatò","mercato17","Freschi","Stracciatella di burrata – Sabelli","250 g",0.250,2.69,8,V,"Il volantino stampa 10,76 al kg."),
 ("Mozzarella","Mercatò","mercato17","Freschi","Mozzarella di bufala senza lattosio – Vivi Bene Selex","125 g",0.125,1.39,8,V,"Solo con Fidelity Card. Il volantino stampa 11,12 al kg."),
 ("Formaggio","Mercatò","mercato17","Freschi","Fette Original – Leerdammer Maxi Formato","260 g",0.260,2.99,8,V,"Il volantino stampa 11,50 al kg."),
 ("Spalmabili","Mercatò","mercato17","Freschi","Robiola d'Alba naturale","200 g",0.200,2.29,8,V,"Il volantino stampa 11,45 al kg."),
 ("Spalmabili","Mercatò","mercato17","Freschi","Robiola – Nonno Nanni","200 g (100 g × 2)",0.200,1.59,8,V,"Solo con Fidelity Card. Il volantino stampa 7,95 al kg."),
 ("Spalmabili","Mercatò","mercato17","Freschi","Philadelphia Original","160 g (80 g × 2)",0.160,1.74,8,V,"Solo con Fidelity Card. Il volantino stampa 10,88 al kg."),
 ("Mozzarella","Mercatò","mercato17","Freschi","Mozzarella Gran Luna – Caseificio Pugliese","300 g",0.300,2.99,8,V,"Il volantino stampa 9,97 al kg."),
 ("Yogurt","Mercatò","mercato17","Freschi","Yogurt Activia – Danone","1 kg (125 g × 8)",1.0,2.99,8,V,"Solo con Fidelity Card. Vari tipi."),
 ("Yogurt","Mercatò","mercato17","Freschi","Yogurt senza lattosio – Bella Vita","250 g (125 g × 2)",0.250,0.79,8,V,"Vari tipi. Il volantino stampa 3,16 al kg."),
 ("Mozzarella","Mercatò","mercato17","Freschi","Mozzarella fior di latte – Vallelata","375 g (125 g × 3)",0.375,2.89,9,V,"Il volantino stampa 7,71 al kg."),
 ("Olio d'oliva","Mercatò","mercato17","Dispensa","Olio d'oliva – Meriggio","750 ml",0.750,4.89,12,V,"Solo con Fidelity Card. Il volantino stampa 6,52 al litro."),
 ("Olio d'oliva","Mercatò","mercato17","Dispensa","Olio di oliva – Farchioni","1 litro",1,4.96,12,V,"Il volantino stampa 4,96 al litro."),
 ("Olio d'oliva","Mercatò","mercato17","Dispensa","Olio extra vergine di oliva 100% italiano – Bartolini","750 ml",0.750,7.69,12,V,"Il volantino stampa 10,25 al litro."),
 ("Olio di semi","Mercatò","mercato17","Dispensa","Olio di semi di mais – Dante","1 litro",1,1.99,12,V,""),
 ("Pomodoro","Mercatò","mercato17","Dispensa","Passata di pomodoro – Santa Rosa","700 g",0.700,0.79,12,V,"Il volantino stampa 1,13 al kg."),
 ("Pomodoro","Mercatò","mercato17","Dispensa","Polpa di pomodoro in pezzi biologica – Natura Chiama Selex","400 g",0.400,0.49,12,V,"Il volantino stampa 1,23 al kg."),
 ("Sughi","Mercatò","mercato17","Dispensa","Sugo alle olive – Barilla","400 g",0.400,1.69,12,V,"Il volantino stampa 4,23 al kg."),
 ("Tonno","Mercatò","mercato17","Dispensa","Tonno all'olio di oliva – Auriga","420 g (70 g × 6)",0.420,4.49,13,V,"Il volantino stampa 10,69 al kg."),
 ("Tonno","Mercatò","mercato17","Dispensa","Filetti di tonno all'olio extravergine di oliva – Mareblu","250 g",0.250,3.85,13,V,"Solo con Fidelity Card. Il volantino stampa 15,40 al kg."),
 ("Farina","Mercatò","mercato17","Dispensa","Farina di grano tenero tipo 00 – Barilla","1 kg",1,0.79,13,V,""),
 ("Pasta","Mercatò","mercato17","Dispensa","Pasta – La Molisana","500 g",0.500,0.69,13,V,"Vari tipi. Il volantino stampa 1,38 al kg."),
 ("Riso","Mercatò","mercato17","Dispensa","Riso Carnaroli chicchi grandi – Principe","1 kg",1,2.33,13,V,""),
 ("Conserve","Mercatò","mercato17","Dispensa","Olive nere snocciolate – Saclà","150 g",0.150,1.39,13,V,"Il volantino stampa 9,27 al kg."),
 ("Pane","Mercatò","mercato17","Dispensa","Pan bauletto al grano duro – Mulino Bianco Barilla","400 g",0.400,0.86,14,V,"Il volantino stampa 2,15 al kg."),
 ("Caffè","Mercatò","mercato17","Dispensa","Caffè macinato Aromadicasa – Vergnano","500 g (250 g × 2)",0.500,4.89,14,V,"Il volantino stampa 9,78 al kg."),
 ("Biscotti","Mercatò","mercato17","Colazione","Frollino Ancora Uno – Tre Marie","315 g",0.315,1.49,15,V,"Vari tipi. Il volantino stampa 4,73 al kg."),
 ("Biscotti","Mercatò","mercato17","Colazione","Biscotti Zalet – Galbusera","510 g",0.510,1.69,15,V,"Il volantino stampa 3,31 al kg."),
 ("Marmellata","Mercatò","mercato17","Colazione","Confettura bio Fiordifrutta – Rigoni di Asiago","250 g",0.250,2.59,15,V,"Vari tipi. Il volantino stampa 10,36 al kg."),
 ("Biscotti","Mercatò","mercato17","Colazione","Biscotti Ringo – Pavesi","165 g",0.165,0.89,16,V,"Vari tipi. Il volantino stampa 5,39 al kg."),
 ("Biscotti","Mercatò","mercato17","Colazione","Krumiri classici – Bistefani","290 g",0.290,1.65,16,V,"Il volantino stampa 5,69 al kg."),
 ("Cioccolato","Mercatò","mercato17","Colazione","Praline – Witors","200 g",0.200,2.98,16,V,"Vari tipi. Il volantino stampa 14,90 al kg."),
 ("Bagnoschiuma","Mercatò","mercato17","Cura persona","Sapone liquido Marsiglia Spuma di Sciampagna","430 ml",0.430,1.48,17,V,"Il volantino stampa 3,44 al litro."),
 ("Dentifricio","Mercatò","mercato17","Cura persona","Dentifricio Mentadent Protect+ Care","75 ml",0.075,1.99,17,V,"Il volantino stampa 26,53 al litro."),
 ("Asciugatutto","Mercatò","mercato17","Cura casa","Asciugoni 2 rotoli – Regina","2 rotoli",2,1.98,18,V,""),
 ("Lavatrice","Mercatò","mercato17","Cura casa","Detersivo per lavatrice in polvere Bianco Splendente, 61 lavaggi – Sole","3,05 kg",61,7.69,19,V,""),
 ("Ammorbidente","Mercatò","mercato17","Cura casa","Ammorbidente concentrato Blue Oxygen, 78 lavaggi – Vernel","1,716 litri",78,3.29,19,V,""),

 # MD nuovo, dal 22 settembre al 4 ottobre. Trovato il 2026-09-18 mentre
 # bennet10 aveva gia un volantino nuovo sovrapposto (vedi sotto): le insegne
 # pubblicano volantini che si accavallano, e md08 scadeva il 20. Letto per
 # intero, 37 pagine. Scartate 5, 11, 23, 27-36 (accessori casa, cura persona,
 # pagina ricetta, tessile, e-mobility, viaggi: nessun prezzo di spesa).
 ("Salame","MD","md22","Salumi","Salame Ungherese/Napoli/Milano/Campagnolo – La Fattoria","100 g",0.100,1.00,1,V,""),
 ("Spalmabili","MD","md22","Freschi","Formaggio fresco spalmabile – Buona Spesa!","200 g",0.200,1.00,1,V,"Prima 1,39."),
 ("Asciugatutto","MD","md22","Cura casa","Carta casa asciugatutto 4 rotoli 2 veli – Scala","4 rotoli",4,1.00,1,V,"Prima 1,29."),
 ("Yogurt","MD","md22","Freschi","Yogurt bianco magro zero grassi – Bontà Viva","500 g (125 g × 4)",0.500,1.00,2,V,"Prima 1,19."),
 ("Yogurt","MD","md22","Freschi","Latte di Kefir arancia e zenzero/frutti misti – Vivo Meglio","480 g",0.480,1.00,2,V,"Prima 1,09. È da bere, non un vasetto."),
 ("Burro","MD","md22","Freschi","Burro senza lattosio – Vivo Meglio","125 g",0.125,1.00,2,V,"Prima 1,15."),
 ("Spalmabili","MD","md22","Freschi","Robiola senza lattosio – Vivo Meglio","100 g",0.100,1.00,2,V,"Prima 1,15."),
 ("Formaggio","MD","md22","Freschi","Edamer/Gouda a fette","150 g",0.150,1.00,2,V,"Prima 1,35."),
 ("Mortadella","MD","md22","Salumi","Gran Mortadella Nazionale selezione – La Fattoria","90 g",0.090,1.00,2,V,"Prima 1,99."),
 ("Prosciutto","MD","md22","Salumi","Spalla cotta – La Fattoria","100 g",0.100,1.00,2,V,"Prima 1,09. È spalla cotta, non prosciutto cotto vero e proprio, ma un affettato cotto comparabile."),
 ("Pancetta","MD","md22","Salumi","Pancetta a cubetti dolce/affumicata – La Fattoria","160 g (80 g × 2)",0.160,1.00,2,V,"Prima 1,29."),
 ("Suino","MD","md22","Salumi","Würstel di puro suino – La Fattoria","200 g (2 pezzi da 100 g)",0.200,1.00,3,V,""),
 ("Pasta","MD","md22","Dispensa","Chicche di patata – Ca' Bianca","500 g (250 g × 2)",0.500,1.00,3,V,"Prima 1,59. Sono gnocchi di patata."),
 ("Pasta","MD","md22","Dispensa","Sfoglia di semola per lasagne – Ca' Bianca","500 g",0.500,1.00,3,V,"Prima 1,39."),
 ("Sughi","MD","md22","Dispensa","Pesto alla siciliana/Sugo funghi porcini-noci-formaggi – La Fattoria del Cavaliere","130 g",0.130,1.00,3,V,"Prima 1,39."),
 ("Merendine","MD","md22","Colazione","2 Krapfen crema/albicocca/cioccolato – Arca","160 g",0.160,1.00,4,V,"Prima 1,29."),
 ("Pasta","MD","md22","Dispensa","Pasta trafilata al bronzo assortita – Pasta Reale","500 g",0.500,1.00,4,V,"Prima 1,29."),
 ("Pasta","MD","md22","Dispensa","Lasagne di semola – Pasta Reale","500 g",0.500,1.00,4,V,"Prima 1,29."),
 ("Legumi","MD","md22","Dispensa","Piselli e carote – Gustato","400 g, peso sgocciolato 265 g",0.265,1.00,4,V,"Prima 1,19. Prezzo calcolato sul peso sgocciolato."),
 ("Sughi","MD","md22","Dispensa","Sugo pronto all'ortolana/alla puttanesca – Gustato","350 g",0.350,1.00,4,V,"Prima 1,29."),
 ("Riso","MD","md22","Dispensa","Risotto ai funghi porcini/alla milanese – Arnaboldi","175 g",0.175,1.00,4,V,"Prima 1,39."),
 ("Biscotti","MD","md22","Colazione","Biscotti ripieni crema al limone/crema al cacao – Playtime","150 g",0.150,1.00,6,V,"Prima 1,39."),
 ("Biscotti","MD","md22","Colazione","Biscotti Digestive – Gullón","400 g",0.400,1.00,6,V,"Prima 1,29."),
 ("Biscotti","MD","md22","Colazione","Canestrellini della Lanterna","250 g",0.250,1.00,6,V,"Prima 1,29."),
 ("Biscotti","MD","md22","Colazione","6 Crostatine albicocca/cacao – La Dolce","240 g",0.240,1.00,6,V,"Prima 1,39."),
 ("Bagnoschiuma","MD","md22","Cura persona","Sapone liquido antibatterico/neutro – Cliosan","500 ml",0.500,1.00,6,V,"Prima 1,25."),
 ("Dentifricio","MD","md22","Cura persona","Dentifricio Total Care – Neoveda","75 ml",0.075,1.00,6,V,"Prima 1,49."),
 ("Carta igienica","MD","md22","Cura casa","Carta igienica profumata 4 rotoli 2 veli – Mega Soft","4 rotoli",4,1.00,7,V,"Prima 1,29."),
 ("Asciugatutto","MD","md22","Cura casa","Carta casa 1 rotolo 160 strappi – Flou","1 rotolo",1,1.00,7,V,"Prima 1,39."),
 ("Formaggio","MD","md22","Gastronomia","Provola sarda dolce","100 g",0.100,1.89,8,V,"Prima 2,09. Speciale Sardegna."),
 ("Formaggio","MD","md22","Gastronomia","Pecorino sardo DOP dolce – Graziola","250 g",0.250,3.89,8,V,"Prima 4,09. Speciale Sardegna."),
 ("Pasta","MD","md22","Gastronomia","Culurgiones classico","250 g",0.250,1.89,8,V,"Prima 1,99. Speciale Sardegna, pasta fresca ripiena."),
 ("Formaggio","MD","md22","Gastronomia","Pecorino sardo di montagna – Gennargentu","300 g",0.300,4.89,8,V,"Prima 4,99. Speciale Sardegna."),
 ("Pasta","MD","md22","Gastronomia","Ravioli ricotta e zafferano – Cossu","400 g",0.400,1.99,8,V,"Prima 2,59. Speciale Sardegna."),
 ("Pasta","MD","md22","Gastronomia","Ravioli di ricotta – Cossu","400 g",0.400,1.99,8,V,"Prima 2,29. Speciale Sardegna."),
 ("Pancetta","MD","md22","Gastronomia","Guanciale affettato di Barbagia","100 g",0.100,1.79,9,V,"Prima 2,29. Speciale Sardegna."),
 ("Prosciutto","MD","md22","Gastronomia","Prosciutto crudo di Barbagia","100 g",0.100,2.69,9,V,"Prima 3,49. Speciale Sardegna."),
 ("Salame","MD","md22","Gastronomia","Salame affettato di Barbagia, grana grossa","100 g",0.100,1.75,9,V,"Prima 2,29. Speciale Sardegna."),
 ("Salame","MD","md22","Gastronomia","Salamino di Barbagia","280 g",0.280,2.99,9,V,"Prima 3,59. Speciale Sardegna."),
 ("Pasta","MD","md22","Gastronomia","Fregola sarda media – Le Tradizionali","500 g",0.500,1.89,9,V,"Prima 2,39. Speciale Sardegna."),
 ("Vino","MD","md22","Bevande","Carignano del Sulcis DOC","750 ml",0.750,3.99,10,V,"Prima 4,89. Speciale Sardegna."),
 ("Vino","MD","md22","Bevande","Vermentino di Sardegna DOC","750 ml",0.750,2.69,10,V,"Prima 3,49. Speciale Sardegna."),
 ("Birra","MD","md22","Bevande","Birra Ichnusa","990 ml (330 ml × 3)",0.990,2.29,10,V,"Prima 2,79. Speciale Sardegna."),
 ("Pane","MD","md22","Panetteria","Pane Carasau in sfoglie","200 g",0.200,2.49,10,V,"Prima 2,99. Speciale Sardegna."),
 ("Pane","MD","md22","Panetteria","Pane Guttiau","500 g",0.500,2.99,10,V,"Prima 3,59. Speciale Sardegna."),
 ("Pane","MD","md22","Panetteria","Pane Guttiau in sfoglie","200 g",0.200,2.49,10,V,"Prima 2,99. Speciale Sardegna."),
 ("Pane","MD","md22","Panetteria","Pane Carasau","500 g",0.500,2.49,10,V,"Prima 2,99. Speciale Sardegna."),
 ("Biscotti","MD","md22","Colazione","Biscotti di Fonni","350 g",0.350,1.85,10,V,"Prima 1,99. Speciale Sardegna."),
 ("Frutta","MD","md22","Ortofrutta","Mele Red Delicious","al kg",1,1.39,12,V,""),
 ("Frutta","MD","md22","Ortofrutta","Uva bianca Italia","al kg",1,1.99,12,V,""),
 ("Frutta","MD","md22","Ortofrutta","Arance Valencia","al kg",1,1.49,12,V,""),
 ("Frutta","MD","md22","Ortofrutta","Pere Williams","al kg",1,1.99,12,V,""),
 ("Frutta","MD","md22","Ortofrutta","Susine Angeleno","al kg",1,1.39,12,V,""),
 ("Verdura","MD","md22","Ortofrutta","Pomodoro Grappolo","al kg",1,1.99,12,V,""),
 ("Patate","MD","md22","Ortofrutta","Patate","4 kg",4,2.60,12,V,""),
 ("Pollo","MD","md22","Macelleria","Petto di pollo a fette","al kg",1,8.90,13,V,""),
 ("Pollo","MD","md22","Macelleria","Cosciotto di pollo","al kg",1,3.40,13,V,""),
 ("Vitello","MD","md22","Macelleria","Arrosto scelto di reale di vitello","al kg",1,15.90,13,V,""),
 ("Vitello","MD","md22","Macelleria","Spezzatino di vitello","al kg",1,16.90,13,V,""),
 ("Manzo","MD","md22","Macelleria","Hamburger di suino/bovino","al kg",1,12.90,13,V,"È misto suino e bovino, non solo bue."),
 ("Manzo","MD","md22","Macelleria","Reale a fette di bovino adulto","al kg",1,16.90,13,V,""),
 ("Prosciutto","MD","md22","Gastronomia","Prosciutto cotto alta qualità – Parmacotto","al kg",1,14.90,14,V,""),
 ("Mortadella","MD","md22","Gastronomia","Mortadella Bologna IGP con pistacchio","al kg",1,7.90,14,V,""),
 ("Prosciutto","MD","md22","Gastronomia","Speck","al kg",1,11.90,14,V,""),
 ("Formaggio","MD","md22","Gastronomia","Pecorino Grottino stagionato in grotta","al kg",1,19.90,14,V,""),
 ("Formaggio","MD","md22","Gastronomia","Gran Cornuto, 100% latte di capra – Capritalia","al kg",1,23.90,14,V,""),
 ("Formaggio","MD","md22","Gastronomia","Brie – Entremont","al kg",1,9.90,14,V,""),
 ("Formaggio","MD","md22","Gastronomia","Pamigo liscio e rigato – Bayernland","al kg",1,12.90,14,V,""),
 ("Conserve","MD","md22","Gastronomia","Olive verdi denocciolate con peperoni – Le Olive Miccio","al kg",1,7.90,14,V,""),
 ("Conserve","MD","md22","Gastronomia","Carciofi arrostiti – Le Delizie","al kg",1,18.90,14,V,""),
 ("Insalata","MD","md22","Freschi","Insalata mista – Buona Spesa!","200 g",0.200,0.79,15,V,"Solo con la MD Buona Spesa Card."),
 ("Formaggio","MD","md22","Freschi","Primosale senza lattosio – Vivo Meglio","180 g",0.180,1.49,15,V,"Solo con la MD Buona Spesa Card."),
 ("Latte","MD","md22","Freschi","Latte microfiltrato parzialmente scremato senza lattosio – Vivo Meglio","1 litro",1,1.09,15,V,"Solo con la MD Buona Spesa Card."),
 ("Tonno","MD","md22","Dispensa","Tonno all'olio d'oliva – Poseidon","210 g (70 g × 3)",0.210,2.15,16,V,"Solo con la MD Buona Spesa Card. Senza tessera 2,59."),
 ("Merluzzo","MD","md22","Surgelati","Croccantelle di filetto di merluzzo pomodoro/spinaci – Le Specialità di Beppe","400 g (4 pezzi)",0.400,2.99,16,V,"Solo con la MD Buona Spesa Card. Senza tessera 4,49. Sono impanate, non filetto puro."),
 ("Merendine","MD","md22","Colazione","10 Plum cake cioccolato – La Dolce","420 g",0.420,1.59,16,V,"Solo con la MD Buona Spesa Card. Senza tessera 2,29."),
 ("Bibite","MD","md22","Bevande","Coca-Cola regular/zero","1,75 litri",1.75,1.79,16,V,"Solo con la MD Buona Spesa Card. Senza tessera 2,49."),
 ("Dentifricio","MD","md22","Cura persona","Dentifricio Mentadent P","100 ml",0.100,1.59,16,V,"Solo con la MD Buona Spesa Card. Senza tessera 1,99."),
 ("Carta igienica","MD","md22","Cura casa","Carta igienica 6 rotoli 3 veli – Flou","6 rotoli",6,3.49,16,V,""),
 ("Prosciutto","MD","md22","Gastronomia","Speck IGP Alto Adige – Lettere dall'Italia","100 g",0.100,1.69,16,V,"Solo con la MD Buona Spesa Card. Senza tessera 1,85."),
 ("Yogurt","MD","md22","Freschi","Yogurt Bifidus bianco naturale – Bontà Viva","1 kg (125 g × 8)",1.0,1.99,17,V,"Prima 2,79."),
 ("Ricotta","MD","md22","Freschi","Ricotta in fuscella – Buona Spesa!","330 g",0.330,1.49,17,V,"Prima 1,79."),
 ("Formaggio","MD","md22","Freschi","Formaggio fuso a fette – Malga Paradiso","400 g",0.400,1.99,17,V,"Prima 2,25."),
 ("Spalmabili","MD","md22","Freschi","Robiola","200 g (100 g × 2)",0.200,1.49,17,V,"Prima 2,29."),
 ("Mozzarella","MD","md22","Freschi","Fior di latte senza lattosio – Sabelli","300 g (100 g × 3)",0.300,2.29,17,V,"Prima 2,59."),
 ("Formaggio","MD","md22","Freschi","Formaggio italiano grattugiato – Malga Paradiso","100 g",0.100,1.09,17,V,"Prima 1,39. È un formaggio grattugiato generico, non vero grana."),
 ("Formaggio","MD","md22","Freschi","Blu di Capra dolce – Igor","150 g",0.150,3.39,17,V,"Prima 3,99."),
 ("Salmone","MD","md22","Freschi","Salmone Norvegese affumicato – Fish&Fine","80 g",0.080,2.99,17,V,"Prima 3,99."),
 ("Prosciutto","MD","md22","Freschi","Prosciutto cotto alta qualità – Buona Spesa!","100 g",0.100,1.19,18,V,"Prima 1,45."),
 ("Suino","MD","md22","Freschi","Capocollo affettato stagionato – Buona Spesa!","100 g",0.100,2.00,18,V,"Prima 2,59. È capocollo, cioè coppa."),
 ("Tacchino","MD","md22","Freschi","Petto di tacchino arrosto nazionale selezione – La Fattoria","100 g",0.100,1.99,18,V,"Prima 2,49."),
 ("Bresaola","MD","md22","Freschi","Bresaola punta d'anca, bassa salatura – La Delicata","80 g",0.080,2.59,18,V,"Prima 3,29."),
 ("Prosciutto","MD","md22","Freschi","Prosciutto cotto a cubetti – La Fattoria","160 g",0.160,1.39,18,V,"Prima 1,69."),
 ("Pasta","MD","md22","Freschi","Gran Tortello porcini/Tortelloni salmone/Ravioli tartufo – Ca' Bianca","250 g",0.250,1.49,18,V,"Prima 1,99."),
 ("Pizza","MD","md22","Surgelati","Pizza Margherita XXL – Il Forno di Visso","460 g",0.460,2.99,19,V,"Prima 3,89."),
 ("Pane","MD","md22","Surgelati","Focaccia farcita prosciutto cotto/provola","390 g",0.390,2.49,19,V,"Prima 3,29."),
 ("Verdure surgelate","MD","md22","Surgelati","Cavolfiore a rosette – Le Specialità di Beppe","600 g",0.600,1.19,19,V,"Prima 1,69."),
 ("Gamberi","MD","md22","Surgelati","Code di mazzancolle tropicali sgusciate","200 g",0.200,2.99,19,V,"Prima 4,15."),
 ("Pesce","MD","md22","Surgelati","Filetto di pangasio senza pelle – Le Specialità di Beppe","480 g",0.480,2.49,19,V,"Prima 3,59. È pangasio, pesce d'allevamento economico: non paragonabile a pesce pregiato."),
 ("Gelato","MD","md22","Surgelati","8 Mini stecchi assortiti – Le Specialità di Beppe","250 g",0.250,2.49,19,V,"Prima 2,89."),
 ("Gelato","MD","md22","Surgelati","6 Coni classico/amarena/vaniglia e cacao – Le Specialità di Beppe","450 g",0.450,2.19,19,V,"Prima 2,89."),
 ("Gelato","MD","md22","Surgelati","Affogato caffè/amarena/cacao/frutti di bosco – Buona Spesa!","500 g",0.500,1.99,19,V,"Prima 2,89."),
 ("Vino","MD","md22","Bevande","Spumante Gran Cuvée brut","750 ml",0.750,1.79,20,V,"Prima 2,29."),
 ("Vino","MD","md22","Bevande","Cerasuolo d'Abruzzo DOC – Derio","750 ml",0.750,1.59,20,V,"Prima 1,99."),
 ("Vino","MD","md22","Bevande","Syrah Terre Siciliane IGP – Tenute Varvari","750 ml",0.750,1.59,20,V,"Prima 1,69."),
 ("Vino","MD","md22","Bevande","Vino Soave DOC – Le Cortigiane","750 ml",0.750,1.59,20,V,"Prima 1,99."),
 ("Birra","MD","md22","Bevande","Birra Contessa blanche/ipa","500 ml",0.500,1.59,20,V,"Prima 1,99."),
 ("Pomodoro","MD","md22","Dispensa","Pomodori pelati – Gustato","400 g, peso sgocciolato 240 g",0.240,0.45,21,V,"Prima 0,69. Prezzo calcolato sul peso sgocciolato."),
 ("Pomodoro","MD","md22","Dispensa","Passata di pomodoro con basilico – Gustato","690 g",0.690,0.89,21,V,"Prima 1,09."),
 ("Conserve","MD","md22","Dispensa","Funghi champignon trifolati – Jolie","180 g",0.180,0.99,21,V,"Prima 1,09."),
 ("Merendine","MD","md22","Colazione","10 Merendine ricoperte al cacao – Midi CiaoCiò","350 g",0.350,1.49,21,V,"Prima 1,69."),
 ("Merendine","MD","md22","Colazione","Croissant ripieni crema al cioccolato","252 g",0.252,1.49,21,V,"Prima 1,99."),
 ("Biscotti","MD","md22","Colazione","Frollini con zucchero di canna – Le Bon","700 g",0.700,1.69,22,V,"Prima 2,19."),
 ("Cereali","MD","md22","Colazione","Honey Snackies – Manusol","375 g",0.375,1.49,22,V,"Prima 1,79."),
 ("Merendine","MD","md22","Colazione","Sfogliaciok – Pasticceria del Centro","200 g",0.200,1.15,22,V,"Prima 1,49."),
 ("Biscotti","MD","md22","Colazione","Twin Go vaniglia – Gullón","290 g",0.290,1.15,22,V,"Prima 1,69."),
 ("Cioccolato","MD","md22","Colazione","Snack Cioko Più assortiti – Witor's","126 g",0.126,1.69,22,V,"Prima 1,99."),
 ("Miele","MD","md22","Dispensa","Miele di Acacia squeeze – Apisol","350 g",0.350,2.89,22,V,"Prima 3,19."),
 ("Lavatrice","MD","md22","Cura casa","Detersivo lavatrice muschio bianco, 56 lavaggi – Omino Bianco","2,24 litri",56,4.69,24,V,"Prima 5,59."),
 ("Lavatrice","MD","md22","Cura casa","Detersivo lavatrice color+, 56 lavaggi – Omino Bianco","2,24 litri",56,4.69,24,V,"Prima 5,59."),
 ("Lavatrice","MD","md22","Cura casa","Dash Pods 15 capsule regolare","15 capsule",15,3.99,24,V,"Prima 5,49."),
 ("Latte","MD","md22","Freschi","Latte parzialmente scremato UHT – Parmalat","1 litro",1,1.29,25,V,"Prima 1,65."),
 ("Sughi","MD","md22","Dispensa","Gran Ragù assortito – Star","360 g (180 g × 2)",0.360,2.19,26,V,"Prima 2,79."),
 ("Bibite","MD","md22","Bevande","Pepsi regular/zero","500 ml",0.500,0.65,26,V,"Prima 0,85."),
 ("Biscotti","MD","md22","Colazione","Mikado cioccolato bianco/fondente/al latte – Lu","70 g",0.070,1.39,26,V,"Prima 1,89. Il prezzo è calcolato sulla confezione più piccola, 70 g: quella da 75 g costa meno al kg."),
 ("Merendine","MD","md22","Colazione","Colazione Più, 10 merendine – Kinder","290 g",0.290,2.49,26,V,"Prima 2,89."),
 ("Bagnoschiuma","MD","md22","Cura persona","Bagnodoccia – Borotalco/Neutro Roberts","900 ml (450 ml × 2)",0.900,3.89,26,V,"Prima 4,69."),
 ("Manzo","MD","md22","Macelleria","Tartare di bovino di razza Chianina – Lettere dall'Italia","160 g",0.160,3.99,37,V,"Weekend più Uno: vale solo dal 2 al 5 ottobre, non per tutto il volantino.","2026-10-02","2026-10-05"),
 ("Sughi","MD","md22","Dispensa","Pesto verde biologico senza aglio","85 g",0.085,1.39,37,V,"Prima 1,59. Weekend più Uno: vale solo dal 2 al 5 ottobre, non per tutto il volantino.","2026-10-02","2026-10-05"),
 ("Olio di semi","MD","md22","Dispensa","Olio di semi di mais – Semì","1 litro",1,1.69,37,V,"Prima 1,89. Weekend più Uno: vale solo dal 2 al 5 ottobre, non per tutto il volantino.","2026-10-02","2026-10-05"),
 ("Biscotti","MD","md22","Colazione","Biscotti ai cereali – Le Bon","500 g (250 g × 2)",0.500,1.29,37,V,"Prima 1,59. Weekend più Uno: vale solo dal 2 al 5 ottobre, non per tutto il volantino.","2026-10-02","2026-10-05"),

 # EKOM, «1+1», dall'8 al 21 settembre. Insegna nuova, chiesta da Manlio il
 # 2026-09-18: a Torino ci sono piu Ekom e il volantino e lo stesso per tutti
 # (l'unico diverso e quello della Toscana), quindi qui non c'e la trappola del
 # Mercato, dove ogni insegna ha il suo. I piu vicini a corso Siracusa sono
 # via Castelgomberto 127 e via Tripoli 79.
 #
 # LE PAGINE 2 E 3 SONO «1+1»: prendendone due, il secondo e gratis. Il prezzo
 # scritto e lo stesso per un pezzo e per due, e il volantino stesso conta il
 # prezzo al chilo su DUE confezioni. Qui le righe dicono nel formato che sono
 # due («2 x 300 g (1+1)»), cosi il prezzo per unita e vero per quello che si
 # compra davvero, e la nota dice sempre quanto costa una confezione sola. Chi
 # ne vuole una paga il doppio al chilo, e sta scritto.
 # Letto per intero il 2026-09-18, 16 pagine. Scartata solo la 12 (concorso
 # a premi della carta fedelta, nessun prezzo).

 # --- pagina 2: 1+1 ---
 ("Merluzzo","Ekom","ekom08","Surgelati","Cuori di filetto di nasello – NÓS","2 × 300 g (1+1)",0.600,3.99,2,V,"Offerta 1+1: due confezioni al prezzo di una. Una confezione sola costa 3,99, cioè 13,30 al kg. È nasello, non merluzzo. Surgelato."),
 ("Verdure surgelate","Ekom","ekom08","Surgelati","Carote a fette – Orogel","2 × 450 g (1+1)",0.900,1.99,2,V,"Offerta 1+1: due confezioni al prezzo di una. Una confezione sola costa 1,99, cioè 4,42 al kg."),
 ("Verdure surgelate","Ekom","ekom08","Surgelati","Cavolfiori a rosette","2 × 450 g (1+1)",0.900,1.49,2,V,"Offerta 1+1: due confezioni al prezzo di una. Una confezione sola costa 1,49, cioè 3,31 al kg."),
 ("Formaggio","Ekom","ekom08","Freschi","Fettine di Emmentaler svizzero – Tigre","2 × 140 g (1+1)",0.280,1.99,2,V,"Offerta 1+1: due confezioni al prezzo di una. Una confezione sola costa 1,99, cioè 14,21 al kg."),
 ("Grana","Ekom","ekom08","Freschi","Grana Padano Riserva DOP grattugiato fresco – Ferrari","2 × 60 g (1+1)",0.120,1.79,2,V,"Offerta 1+1: due confezioni al prezzo di una. Una confezione sola costa 1,79, cioè 29,83 al kg."),
 ("Yogurt","Ekom","ekom08","Freschi","Yogurt da bere alla frutta, zero grassi o intero – Alplí","2 × 500 g (1+1)",1.000,1.19,2,V,"Offerta 1+1: due bottiglie al prezzo di una. Una bottiglia sola costa 1,19, cioè 2,38 al kg."),
 ("Biscotti","Ekom","ekom08","Colazione","Zuppalatte o Oswego – Colussi","2 × 250 g (1+1)",0.500,1.49,2,V,"Offerta 1+1: due confezioni al prezzo di una. Una confezione sola costa 1,49, cioè 5,96 al kg."),
 ("Pasta","Ekom","ekom08","Dispensa","Pasta di semola, diversi formati – Barilla","2 × 500 g (1+1)",1.000,0.99,2,V,"Offerta 1+1: due confezioni al prezzo di una. Una confezione sola costa 0,99, cioè 1,98 al kg."),
 ("Riso","Ekom","ekom08","Dispensa","Riso Apri Scalda basmati, integrale o chicco lungo – Scotti","2 × 200 g (1+1)",0.400,1.99,2,V,"Offerta 1+1: due confezioni al prezzo di una. Una confezione sola costa 1,99, cioè 9,95 al kg. È riso già cotto da scaldare, non riso crudo."),

 # --- pagina 3: 1+1 ---
 ("Olio d'oliva","Ekom","ekom08","Dispensa","Olio extra vergine di oliva classico – Coppini","2 × 1 litro (1+1)",2.000,9.99,3,V,"Offerta 1+1: due latte al prezzo di una. Una latta sola costa 9,99, cioè 9,99 al litro."),
 ("Acqua","Ekom","ekom08","Bevande","Acqua naturale – Sant'Anna","2 × 1,5 litri (1+1)",3.000,0.54,3,V,"Offerta 1+1: due bottiglie al prezzo di una. Una bottiglia sola costa 0,54, cioè 0,36 al litro."),
 ("Vino","Ekom","ekom08","Bevande","Arneis Langhe DOC","2 × 750 ml (1+1)",1.500,6.79,3,V,"Offerta 1+1: due bottiglie al prezzo di una. Una bottiglia sola costa 6,79, cioè 9,05 al litro."),
 ("Dentifricio","Ekom","ekom08","Cura persona","Dentifricio Maximum Cavity Protection – Colgate","2 × 100 ml (1+1)",0.200,2.99,3,V,"Offerta 1+1: due confezioni al prezzo di una. Una sola costa 2,99, cioè 29,90 al litro."),
 ("Bagnoschiuma","Ekom","ekom08","Cura persona","Bagnodoccia crema nutriente o idratante – Spuma di Sciampagna","2 × 650 ml (1+1)",1.300,2.99,3,V,"Offerta 1+1: due flaconi al prezzo di uno. Un flacone solo costa 2,99, cioè 4,60 al litro."),
 ("Carta igienica","Ekom","ekom08","Cura casa","Carta igienica Ultra Comfort 3 veli, 4 rotoli – Tenderly","2 × 4 rotoli (1+1)",8,2.79,3,V,"Offerta 1+1: due confezioni al prezzo di una. Una confezione sola costa 2,79, cioè 0,70 al rotolo."),
 ("Lavatrice","Ekom","ekom08","Cura casa","Detersivo universale 5 in 1 Active, 60 lavaggi – General","2 × 2,4 litri (1+1)",120,8.99,3,V,"Offerta 1+1: due flaconi al prezzo di uno. Un flacone solo costa 8,99, cioè 0,15 a lavaggio."),
 ("Lavatrice","Ekom","ekom08","Cura casa","Power Caps Total 4+1 classico o igiene, 27 lavaggi – Bio Presto","2 × 1,62 kg (1+1)",54,8.99,3,V,"Offerta 1+1: due confezioni al prezzo di una. Una confezione sola costa 8,99, cioè 0,33 a lavaggio."),

 # --- pagina 4: dispensa ---
 ("Biscotti","Ekom","ekom08","Colazione","Waferini al cacao o alla nocciola","400 g",0.400,1.39,4,V,"−20%, prima 1,85. Sono wafer."),
 ("Biscotti","Ekom","ekom08","Colazione","Baiocchi – Mulino Bianco","260 g",0.260,2.19,4,V,"−25%, prima 2,99."),
 ("Cioccolato","Ekom","ekom08","Colazione","Cioccolato al latte o fondente – Novi","100 g",0.100,1.49,4,V,"−20%, prima 1,89."),
 ("Creme","Ekom","ekom08","Colazione","Nutella – Ferrero","950 g",0.950,6.49,4,V,""),
 ("Pane","Ekom","ekom08","Panetteria","Pan Bauletto bianco – Mulino Bianco","400 g",0.400,0.89,4,V,"−20%, prima 1,12."),
 ("Pane","Ekom","ekom08","Panetteria","Pane carasau","250 g",0.250,1.99,4,V,""),
 ("Pane","Ekom","ekom08","Panetteria","Pane pita","450 g",0.450,1.59,4,V,""),
 ("Sughi","Ekom","ekom08","Dispensa","Ragù alla bolognese – Barilla","300 g",0.300,1.59,4,V,"−40%, prima 2,75."),
 ("Tonno","Ekom","ekom08","Dispensa","Tonno all'olio di oliva – Mareblu","420 g (70 g × 6)",0.420,4.99,4,V,"−25%, prima 6,99. Formato speciale da 6 lattine."),

 # --- pagina 5: bevande ---
 ("Bibite","Ekom","ekom08","Bevande","Coca Cola, Fanta o Sprite","500 ml",0.500,0.89,5,V,""),
 ("Bibite","Ekom","ekom08","Bevande","Estathé, diversi tipi","1,5 litri",1.500,1.59,5,V,"−20%, prima 1,99."),
 ("Bibite","Ekom","ekom08","Bevande","Energy drink – Red Bull","355 ml",0.355,1.59,5,V,"−25%, prima 2,19. È un energy drink, non un succo."),
 ("Birra","Ekom","ekom08","Bevande","Birra DAB","660 ml",0.660,1.39,5,V,""),
 ("Birra","Ekom","ekom08","Bevande","Birra Tennent's Super","355 ml",0.355,1.59,5,V,""),
 ("Birra","Ekom","ekom08","Bevande","Birra Raffo originale","660 ml",0.660,1.29,5,V,"−20%, prima 1,69. La «lavorazione grezza» da 450 ml costa lo stesso prezzo, cioè 2,87 al litro."),
 ("Birra","Ekom","ekom08","Bevande","Birra 8.6 Original – Bavaria","500 ml",0.500,1.39,5,V,""),
 ("Birra","Ekom","ekom08","Bevande","Birra Faxe 10%","500 ml",0.500,1.29,5,V,"È una birra al 10%: forte, non da tavola."),
 ("Birra","Ekom","ekom08","Bevande","Birra Weizen – Edelmeister","500 ml",0.500,0.79,5,V,"−20%, prima 0,99."),
 ("Birra","Ekom","ekom08","Bevande","Birra Red – Faxe","500 ml",0.500,1.19,5,V,""),
 ("Birra","Ekom","ekom08","Bevande","Birra Bud","500 ml",0.500,0.99,5,V,"−25%, prima 1,39."),
 ("Vino","Ekom","ekom08","Bevande","Bardolino DOC – Laronchi Vini","750 ml",0.750,2.99,5,V,""),
 ("Vino","Ekom","ekom08","Bevande","Cortese Piemonte DOC","750 ml",0.750,2.89,5,V,"−25%, prima 3,89."),
 ("Vino","Ekom","ekom08","Bevande","Müller Thurgau","750 ml",0.750,1.99,5,V,"−33%, prima 2,99."),

 # --- pagina 6: speciale colazione ---
 ("Merendine","Ekom","ekom08","Colazione","Ciambella zuccherata","180 g (60 g × 3)",0.180,1.19,6,V,"−20%, prima 1,49."),
 ("Latte","Ekom","ekom08","Freschi","Latte UHT Piacere Leggero – Granarolo","1 litro",1,1.29,6,V,"−20%, prima 1,69."),
 ("Burro","Ekom","ekom08","Freschi","Burro in monoporzioni – Parmareggio","124,8 g (10,4 g × 12)",0.1248,1.29,6,V,"−25%, prima 1,79. Sono monoporzioni da colazione."),
 ("Pancetta","Ekom","ekom08","Salumi","Bacon pancetta tesa – ibis","100 g",0.100,1.99,6,V,"−20%, prima 2,49."),
 ("Uova","Ekom","ekom08","Freschi","6 uova fresche da galline allevate all'aperto","6 uova",6,1.99,6,V,""),
 ("Yogurt","Ekom","ekom08","Freschi","Yogurt cremoso intero bianco, banana o frutti di bosco – Latteria Brunico","500 g",0.500,0.99,6,V,""),
 ("Caffè","Ekom","ekom08","Colazione","Caffè macinato Crema e Gusto classico – Lavazza","500 g (250 g × 2)",0.500,7.99,6,V,"−20%, prima 9,99."),
 ("Caffè","Ekom","ekom08","Colazione","Caffè macinato Decaf – Lavazza","250 g",0.250,3.99,6,V,"−33%, prima 5,99. È decaffeinato."),
 ("Caffè","Ekom","ekom08","Colazione","50 capsule classico o intenso compatibili Nespresso – Segafredo","255 g",0.255,9.90,6,V,"−20%, prima 12,99. Sono capsule: al chilo costano sempre molto più del macinato."),
 ("Caffè","Ekom","ekom08","Colazione","36 capsule A Modo Mio passionale, qualità rossa o crema e gusto – Lavazza","270 g",0.270,9.89,6,V,"−35%, prima 15,39. Sono capsule: al chilo costano sempre molto più del macinato."),
 ("Tè","Ekom","ekom08","Colazione","Tè English Breakfast, Pure Green o Earl Grey, 40 filtri – Twinings","80 g",0.080,2.99,6,V,"−25%, prima 3,99."),
 ("Cereali","Ekom","ekom08","Colazione","Bran-Sticks","375 g",0.375,1.39,6,V,"−30%, prima 1,99."),
 ("Cereali","Ekom","ekom08","Colazione","Cornflakes","375 g",0.375,0.99,6,V,"−35%, prima 1,59."),

 # --- pagina 7: speciale colazione ---
 ("Biscotti","Ekom","ekom08","Colazione","Gocciolotti e altri tipi – Balocco","350 g",0.350,1.49,7,V,"−20%, prima 1,95."),
 ("Farina","Ekom","ekom08","Dispensa","Farina di avena – Vital Love","500 g",0.500,0.89,7,V,"−30%, prima 1,29. È farina di avena, non di grano."),
 ("Creme","Ekom","ekom08","Colazione","Crema al pistacchio o burro di arachidi, monoporzioni","80 g (20 g × 4)",0.080,1.19,7,V,"−20%, prima 1,49. Sono monoporzioni."),
 ("Marmellata","Ekom","ekom08","Colazione","Confettura di frutta, gusti assortiti – Santa Rosa","600 g",0.600,1.99,7,V,"−20%, prima 2,49."),
 ("Biscotti","Ekom","ekom08","Colazione","Kinderini – Kinder","250 g",0.250,2.99,7,V,""),
 ("Bibite","Ekom","ekom08","Bevande","Bevanda Refresh+Vita multivitamin o mango maracuja – Pfanner","2 litri",2.000,1.99,7,V,"−20%, prima 2,49."),
 ("Bibite","Ekom","ekom08","Bevande","Bevanda di frutta zero zuccheri aggiunti, frutti rossi o ACE – Pfanner","1 litro",1,0.99,7,V,"−20%, prima 1,29."),

 # --- pagina 8: frutta e verdura ---
 ("Verdura","Ekom","ekom08","Ortofrutta","Melanzane nere","al kg",1,1.59,8,V,""),
 ("Verdura","Ekom","ekom08","Ortofrutta","Pomodori Piccadilly","500 g",0.500,1.59,8,V,""),
 ("Verdura","Ekom","ekom08","Ortofrutta","Spinaci Pronto Cuoci – Kome Te","400 g",0.400,1.89,8,V,""),
 ("Frutta","Ekom","ekom08","Ortofrutta","Prugne Santa Clara","al kg",1,1.89,8,V,""),
 ("Frutta","Ekom","ekom08","Ortofrutta","Banane","al kg",1,1.19,8,V,""),
 ("Frutta","Ekom","ekom08","Ortofrutta","Uva bianca senza semi","500 g",0.500,1.85,8,V,""),
 ("Frutta","Ekom","ekom08","Ortofrutta","Uva Red Globe","750 g",0.750,1.99,8,V,""),
 ("Frutta","Ekom","ekom08","Ortofrutta","Mele Gala","al kg",1,1.49,8,V,""),

 # --- pagina 9: banco salumi, formaggi e macelleria ---
 # Il volantino avverte: valide SOLO nei punti vendita col banco servito.
 ("Prosciutto","Ekom","ekom08","Gastronomia","Prosciutto di Parma DOP, al banco","al kg",1,26.90,9,V,"Il volantino stampa 2,69 all'etto. Vale solo nei negozi col banco servito."),
 ("Bresaola","Ekom","ekom08","Gastronomia","Carpaccio di bresaola punta d'anca, al banco","al kg",1,26.90,9,V,"Il volantino stampa 2,69 all'etto. Vale solo nei negozi col banco servito."),
 ("Salame","Ekom","ekom08","Gastronomia","Salame Piacentino DOP, al banco","al kg",1,21.90,9,V,"Il volantino stampa 2,19 all'etto. Vale solo nei negozi col banco servito."),
 ("Prosciutto","Ekom","ekom08","Gastronomia","Prosciutto cotto alta qualità nazionale – Lenti, al banco","al kg",1,19.90,9,V,"Il volantino stampa 1,99 all'etto. Vale solo nei negozi col banco servito."),
 ("Formaggio","Ekom","ekom08","Gastronomia","Primo sale siciliano pepato, al banco","al kg",1,12.90,9,V,"Il volantino stampa 1,29 all'etto. Vale solo nei negozi col banco servito."),
 ("Formaggio","Ekom","ekom08","Gastronomia","Gorgonzola DOP dolce Gim – Invernizzi, al banco","al kg",1,13.90,9,V,"Il volantino stampa 1,39 all'etto. Vale solo nei negozi col banco servito."),
 ("Formaggio","Ekom","ekom08","Gastronomia","Caciotta, al banco","al kg",1,11.90,9,V,"Il volantino stampa 1,19 all'etto. Vale solo nei negozi col banco servito."),
 ("Formaggio","Ekom","ekom08","Gastronomia","Maasdammer, al banco","al kg",1,8.90,9,V,"Il volantino stampa 0,89 all'etto. Vale solo nei negozi col banco servito."),
 ("Manzo","Ekom","ekom08","Macelleria","Spezzatino di bovino adulto","al kg",1,15.90,9,V,"Vale solo nei negozi col banco servito."),
 ("Manzo","Ekom","ekom08","Macelleria","Sottofiletto di bovino adulto","al kg",1,22.90,9,V,"Vale solo nei negozi col banco servito."),
 ("Suino","Ekom","ekom08","Macelleria","Coppa di suino con osso","al kg",1,6.90,9,V,"Vale solo nei negozi col banco servito."),
 ("Tacchino","Ekom","ekom08","Macelleria","Fesa di tacchino a fette","al kg",1,13.90,9,V,"Vale solo nei negozi col banco servito."),
 ("Pollo","Ekom","ekom08","Macelleria","Cosce di pollo, confezione risparmio","al kg",1,4.90,9,V,"Confezione risparmio da 600/800 g. Vale solo nei negozi col banco servito."),

 # --- pagina 10: freschi confezionati ---
 ("Burro","Ekom","ekom08","Freschi","Burro – Latteria Soresina","125 g",0.125,1.19,10,V,"−25%, prima 1,69."),
 ("Mozzarella","Ekom","ekom08","Freschi","Mozzarella fior di latte – Vallelata","300 g (100 g × 3)",0.300,2.49,10,V,""),
 ("Mozzarella","Ekom","ekom08","Freschi","Bocconcini ripieni con crema di latte – Vallelata","180 g",0.180,2.49,10,V,"Sono ripieni di crema di latte, non mozzarella semplice."),
 ("Mozzarella","Ekom","ekom08","Freschi","Mozzarella di bufala campana DOP","300 g (100 g × 3)",0.300,2.99,10,V,""),
 ("Formaggio","Ekom","ekom08","Freschi","Stracchino","320 g",0.320,1.99,10,V,""),
 ("Ricotta","Ekom","ekom08","Freschi","Ricotta fresca","450 g",0.450,1.19,10,V,""),
 ("Ricotta","Ekom","ekom08","Freschi","Ricottina light Santa Lucia – Galbani","180 g (90 g × 2)",0.180,1.19,10,V,"−20%, prima 1,49."),
 ("Formaggio","Ekom","ekom08","Freschi","Scamorza affumicata o bianca – Kome Te","90 g",0.090,1.69,10,V,"−30%, prima 2,49."),
 ("Formaggio","Ekom","ekom08","Freschi","Tomini classici – Pezzana","160 g (80 g × 2)",0.160,1.99,10,V,"−20%, prima 2,49."),
 ("Formaggio","Ekom","ekom08","Freschi","Brie","500 g",0.500,3.99,10,V,""),
 ("Formaggio","Ekom","ekom08","Freschi","Gorgonzola DOP","200 g",0.200,1.99,10,V,"−20%, prima 2,49."),
 ("Grana","Ekom","ekom08","Freschi","Parmigiano Reggiano DOP 16 mesi – Ferrari","150 g",0.150,3.99,10,V,"−20%, prima 4,99."),

 # --- pagina 11: freschi confezionati ---
 ("Formaggio","Ekom","ekom08","Freschi","Raspadura – Bella Lodi","100 g",0.100,1.99,11,V,"−20%, prima 2,49."),
 ("Grana","Ekom","ekom08","Freschi","Granbiraghi spicchio – Biraghi","500 g",0.500,6.99,11,V,"È Granbiraghi, non Grana Padano DOP."),
 ("Prosciutto","Ekom","ekom08","Salumi","Prosciutto di Parma DOP in vaschetta","80 g",0.080,2.69,11,V,"−20%, prima 3,49."),
 ("Prosciutto","Ekom","ekom08","Salumi","Prosciutto cotto di alta qualità – Rovagnati","180 g",0.180,2.39,11,V,"−20%, prima 2,99."),
 ("Suino","Ekom","ekom08","Salumi","Würstel di puro suino","250 g",0.250,0.99,11,V,"Sono würstel, non carne fresca."),
 ("Salame","Ekom","ekom08","Salumi","Salame Felino IGP – Kome Te","80 g",0.080,2.79,11,V,"−20%, prima 3,49."),
 ("Salmone","Ekom","ekom08","Freschi","Salmone scozzese affumicato","80 g",0.080,3.99,11,V,"−20%, prima 4,99. È affumicato, non fresco."),
 ("Pane","Ekom","ekom08","Panetteria","Piadina romagnola IGP, 5 pezzi","600 g",0.600,1.49,11,V,""),
 ("Sughi","Ekom","ekom08","Freschi","Pesto di Prà – I Gran Pesti","130 g",0.130,2.49,11,V,"È pesto fresco da banco frigo."),
 ("Pasta","Ekom","ekom08","Freschi","Gnocchi tricolore","400 g",0.400,1.59,11,V,"−20%, prima 1,99. Sono gnocchi freschi, non pasta secca."),

 # --- pagina 13: solo con la carta EKOM UP ---
 ("Pollo","Ekom","ekom08","Surgelati","Cotolette di pollo – AIA","280 g",0.280,1.99,13,V,"Solo con la carta EKOM UP. Senza tessera 2,99. Sono cotolette panate surgelate."),
 ("Patate","Ekom","ekom08","Surgelati","Patate grigliate al rosmarino","450 g",0.450,1.49,13,V,"Solo con la carta EKOM UP. Senza tessera 1,99. Sono surgelate e già grigliate, non patate crude."),
 ("Pane","Ekom","ekom08","Panetteria","Focaccia croccante genovese","250 g",0.250,1.99,13,V,"Solo con la carta EKOM UP. Senza tessera 2,99."),
 ("Tonno","Ekom","ekom08","Dispensa","Filetti di tonno all'olio extra vergine di oliva – Maruzzella","130 g, sgocciolati 91 g",0.091,2.39,13,V,"Solo con la carta EKOM UP. Senza tessera 2,99. Il conto è sui 91 g sgocciolati, come stampa il volantino."),
 ("Bibite","Ekom","ekom08","Bevande","Fanta Original o Sprite classica","1,5 litri",1.500,1.32,13,V,"Solo con la carta EKOM UP. Senza tessera 1,89."),
 ("Birra","Ekom","ekom08","Bevande","Birra Ichnusa non filtrata","500 ml",0.500,1.29,13,V,"Solo con la carta EKOM UP. Senza tessera 1,65."),
 ("Lavastoviglie","Ekom","ekom08","Cura casa","Gel Tutto in 1 limone e lime, 52 lavaggi – Pril","936 ml",52,5.49,13,V,"Solo con la carta EKOM UP. Senza tessera 7,99."),
 ("Asciugatutto","Ekom","ekom08","Cura casa","Asciugatutto 2 veli, 2 maxi rotoli – Bravo","2 maxi rotoli",2,4.99,13,V,"Solo con la carta EKOM UP. Senza tessera 6,99. Sono maxi rotoli: al rotolo costano più dei normali, ma durano di più."),

 # --- pagina 14: profumeria e detergenza ---
 ("Bagnoschiuma","Ekom","ekom08","Cura persona","Sapone mani e viso marsiglia o mandorle e karité – Spuma di Sciampagna","430 ml",0.430,1.79,14,V,"−25%, prima 2,49."),
 ("Shampoo","Ekom","ekom08","Cura persona","Shampoo Fructis – Garnier","700 ml",0.700,4.99,14,V,"−25%, prima 6,99."),
 ("Lavatrice","Ekom","ekom08","Cura casa","Detersivo in polvere classico, 48 misurini – Dixan","2,64 kg",48,8.99,14,V,"−30%, prima 12,90."),
 ("Ammorbidente","Ekom","ekom08","Cura casa","Ammorbidente concentrato fresca rugiada o petali di marsiglia, 65 lavaggi – Spuma di Sciampagna","1,3 litri",65,2.19,14,V,"−40%, prima 3,69."),
 ("Asciugatutto","Ekom","ekom08","Cura casa","Asciugatutto Tuttofare, 4 rotoli – Scottex","4 rotoli",4,4.59,14,V,"−30%, prima 6,79."),

 # --- pagina 15: surgelati ---
 ("Bastoncini","Ekom","ekom08","Surgelati","10 bastoncini di pesce – Ocean Blu","300 g",0.300,1.59,15,V,"−20%, prima 1,99."),
 ("Calamari","Ekom","ekom08","Surgelati","Tubi di totano","700 g",0.700,3.99,15,V,"−40%, prima 6,99. È totano, non calamaro."),
 ("Verdure surgelate","Ekom","ekom08","Surgelati","Funghi porcini di bosco cubettati – Asiago Food","300 g",0.300,3.49,15,V,"−20%, prima 4,49."),
 ("Verdure surgelate","Ekom","ekom08","Surgelati","Cicoria foglia a foglia – Agrifood","750 g",0.750,1.59,15,V,"−20%, prima 1,99."),
 ("Verdure surgelate","Ekom","ekom08","Surgelati","Minestrone Tradizione – Findus","700 g",0.700,2.39,15,V,"−20%, prima 2,99."),
 ("Verdure surgelate","Ekom","ekom08","Surgelati","Spinaci con mozzarella e formaggio","450 g",0.450,1.99,15,V,"−20%, prima 2,49. Non sono spinaci puri: dentro ci sono mozzarella e formaggio."),
 ("Gelato","Ekom","ekom08","Surgelati","Vaschetta gelato, gusti assortiti","1 kg",1,2.99,15,V,""),
 ("Gelato","Ekom","ekom08","Surgelati","Maxibon Classic – Nestlé","384 g",0.384,2.99,15,V,"−40%, prima 4,99."),
 ("Gelato","Ekom","ekom08","Surgelati","Gelato ricoperto","400 g",0.400,1.99,15,V,"−20%, prima 2,49."),
 ("Pizza","Ekom","ekom08","Surgelati","Pizza margherita La Numero Uno – Italpizza","410 g",0.410,2.39,15,V,"−20%, prima 2,99."),

 # --- pagina 16: piccoli formati ---
 ("Gelato","Ekom","ekom08","Surgelati","Vaschetta gelato, gusti assortiti – Kome Te","200 g",0.200,0.99,16,V,"−33%, prima 1,49."),
 ("Grana","Ekom","ekom08","Freschi","Gran Biraghi grattugiato – Biraghi","60 g",0.060,0.99,16,V,"−25%, prima 1,39. È Gran Biraghi, non Grana Padano DOP."),
 ("Formaggio","Ekom","ekom08","Freschi","Snack Biraghini – Biraghi","66,68 g (16,67 g × 4)",0.06668,1.39,16,V,"−20%, prima 1,79. Sono snack monoporzione."),
 ("Bresaola","Ekom","ekom08","Salumi","Sfilacci di bresaola","60 g",0.060,1.39,16,V,"−30%, prima 1,99."),
 ("Yogurt","Ekom","ekom08","Freschi","Yogurt alla fragola Super Mario – Danone","110 g",0.110,0.59,16,V,"−33%, prima 0,89."),
 ("Biscotti","Ekom","ekom08","Colazione","Canestrelli","125 g",0.125,0.79,16,V,"−20%, prima 0,99."),
 ("Biscotti","Ekom","ekom08","Colazione","Frollini Le Spighe, diversi tipi","300 g",0.300,0.89,16,V,""),
 ("Miele","Ekom","ekom08","Colazione","Miele millefiori monodose","80 g (20 g × 4)",0.080,0.99,16,V,"Sono monodose."),
 ("Riso","Ekom","ekom08","Dispensa","Riso Ribe – Scotti","500 g",0.500,0.99,16,V,"−35%, prima 1,59."),
 ("Olio d'oliva","Ekom","ekom08","Dispensa","Olio extra vergine di oliva monodose – Biffi","50 ml (10 ml × 5)",0.050,1.19,16,V,"−20%, prima 1,49. Sono monodose da 10 ml: al litro costano moltissimo, servono per il pranzo fuori casa."),
 ("Sughi","Ekom","ekom08","Dispensa","Pesto tartufo, calabrese o pomodori secchi e pistacchio – Saclà","90 g (45 g × 2)",0.090,1.49,16,V,"−25%, prima 1,99."),
 ("Pomodoro","Ekom","ekom08","Dispensa","Passata di pomodoro – Mutti","235 g",0.235,0.79,16,V,"−20%, prima 0,99."),

 # ----- Bennet «Un mondo di bellezza», 17-30 settembre (bennet1709), letto per intero il 2026-09-19 -----
 # Volantino a tema bellezza (uscito il 17/9 mentre bennet10 era ancora valido,
 # stessa sovrapposizione del "Dolce Buongiorno" di settembre) ma da pagina 18
 # in poi ci sono alimentari, surgelati e casa. BC = solo con la carta Bennet Club.
 # Molte offerte "shampoo O balsamo" hanno lo stesso prezzo per due formati
 # diversi: qui il conto è sempre sul formato più piccolo, per non sembrare
 # più conveniente di quanto sia.
 ("Shampoo","Bennet","bennet1709","Cura persona","Shampoo cocco – Splend'Or","300 ml",0.300,1.10,2,V,"−40%, prima 1,84."),
 ("Shampoo","Bennet","bennet1709","Cura persona","Shampoo 250 ml o balsamo 200 ml, vari tipi – Sunsilk","200 ml (balsamo)",0.200,1.99,2,V,"−30%, prima 2,85. Stesso prezzo per lo shampoo da 250 ml: qui il conto è sul balsamo, il formato più piccolo."),
 ("Shampoo","Bennet","bennet1709","Cura persona","Shampoo 250 ml o balsamo 220 ml, vari tipi – Head & Shoulders","220 ml (balsamo)",0.220,2.79,2,V,"−30%, prima 3,99. Stesso prezzo per lo shampoo da 250 ml: qui il conto è sul balsamo, il formato più piccolo."),
 ("Shampoo","Bennet","bennet1709","Cura persona","Shampoo 250 ml o balsamo 200 ml Active Nutri-Plex – Pantene Pro-V","200 ml (balsamo)",0.200,2.99,2,V,"−25%, prima 3,99. Stesso prezzo per lo shampoo da 250 ml: qui il conto è sul balsamo, il formato più piccolo."),
 ("Shampoo","Bennet","bennet1709","Cura persona","Shampoo Imperial Argan – Vitalcare","500 ml",0.500,2.99,2,V,"−25%, prima 3,99."),
 ("Shampoo","Bennet","bennet1709","Cura persona","Shampoo 400 ml o balsamo 200 ml Professional – Biopoint","200 ml (balsamo)",0.200,5.99,2,V,"−25%, prima 7,99. Stesso prezzo per lo shampoo da 400 ml: qui il conto è sul balsamo, il formato più piccolo."),
 ("Shampoo","Bennet","bennet1709","Cura persona","Baby shampoo – Johnson's","500 ml",0.500,3.40,16,V,"−20%, prima 4,26."),
 ("Shampoo","Bennet","bennet1709","Cura persona","Balsamo capelli o acqua profumata – Chicco","150 ml",0.150,3.99,16,V,"−20%, prima 4,99. Stesso prezzo per il balsamo o per l'acqua profumata: qui il conto è sul balsamo."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Docciaschiuma vari tipi – Vidal","250 ml",0.250,0.99,4,V,"−50%, prima 1,99."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Doccia shampoo Dermoprotect Uomo 4in1 – Neutromed","250 ml",0.250,1.49,4,V,"−25%, prima 1,99."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Bagnoschiuma Argan vari tipi – Naturaverde","750 ml",0.750,1.79,4,V,"−40%, prima 2,99."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Shower gel Energy Drive vari tipi – Adidas Vibes","250 ml",0.250,1.95,4,V,"−30%, prima 2,79."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Bagnoschiuma vari tipi – Pino Silvestre","750 ml",0.750,1.99,4,V,"−30%, prima 2,85."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Bagnodoccia classico – Felce Azzurra","650 ml",0.650,2.30,4,V,"−30%, prima 3,29."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Doccia shampoo squadre di calcio, vari tipi","250 ml",0.250,2.60,4,V,"−25%, prima 3,47."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Bagnodoccia vitamina C – White Castle","400 ml",0.400,2.99,4,V,"−30%, prima 4,28."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Sapone liquido delicato Argan – Bennet","500 ml",0.500,1.19,5,V,"−20% SOLO CON LA CARTA BENNET CLUB, prima 1,49."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Sapone liquido vari tipi – Felce Azzurra","300 ml",0.300,1.39,5,V,"−30%, prima 1,99."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Sapone liquido Argan vari tipi – Naturaverde","500 ml",0.500,1.24,5,V,"−50%, prima 2,49."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Sapone liquido mani vari tipi – Lady Venezia","500 ml",0.500,1.49,5,V,"−25% SOLO CON LA CARTA BENNET CLUB, prima 1,99."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Sapone liquido biologico argan – I Provenzali","250 ml",0.250,2.45,5,V,"−25%, prima 3,27."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Sapone liquido Marsiglia – White Castle","500 ml",0.500,3.99,5,V,"−20%, prima 4,99."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Ricarica sapone liquido aloe vera – Milmil","2 litri",2,2.39,5,V,"−40%, prima 3,99."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Ecoricarica sapone liquido idratante – Nidra","1 litro",1,2.49,5,V,"−30%, prima 3,57."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Bagnoschiuma 500 ml (+100 ml omaggio) o ricarica sapone 900 ml, vari tipi – Palmolive","600 ml (bagnoschiuma con omaggio)",0.600,1.99,5,V,"−33%, prima 2,98. Stesso prezzo per la ricarica da 900 ml: qui il conto è sul formato più piccolo, per non sembrare più conveniente."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Detergente intimo delicato – Lactacyd","200 ml",0.200,1.99,14,V,"−50%, prima 3,99."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Detergente intimo delicato – Neutroderma","400 ml",0.400,1.49,14,V,"−50%, prima 2,99."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Detergente intimo classico – Felce Azzurra","250 ml",0.250,1.85,14,V,"−30%, prima 2,65."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Detergente intimo freschezza – Neutromed","300 ml",0.300,2.29,14,V,"−30%, prima 3,28."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Detergente intimo fresco – Sauber","350 ml",0.350,1.94,14,V,"−35%, prima 2,99."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Detergente intimo lenitivo – Intima+","500 ml",0.500,3.49,14,V,"−30%, prima 4,99."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Gel detergente intimo – Chilly","300 ml",0.300,3.49,14,V,"−30%, prima 4,99."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Detergente intimo senza risciacquo, vari tipi – Chilly","100 ml",0.100,3.49,14,V,"−30%, prima 4,92."),
 ("Bagnoschiuma","Bennet","bennet1709","Cura persona","Bagnodoccia neutro – Jkare","1 litro",1,1.39,18,V,""),
 ("Dentifricio","Bennet","bennet1709","Cura persona","Dentifricio vari tipi – Sensodyne","75 ml",0.075,2.79,12,V,"−30%, prima 3,99."),
 ("Dentifricio","Bennet","bennet1709","Cura persona","Dentifricio Gengive+ – Parodontax","75 ml",0.075,3.99,12,V,"−20%, prima 4,99."),
 ("Dentifricio","Bennet","bennet1709","Cura persona","Dentifricio 3D White Bianco Perla – Oral-B","75 ml",0.075,1.19,13,V,"−40%, prima 1,99."),
 ("Dentifricio","Bennet","bennet1709","Cura persona","Dentifricio Placca e Carie – Pasta del Capitano","75 ml",0.075,0.99,13,V,"−40%, prima 1,65."),
 ("Dentifricio","Bennet","bennet1709","Cura persona","Dentifricio Microgranuli – Mentadent","75 ml",0.075,1.74,13,V,"−30%, prima 2,49."),
 ("Dentifricio","Bennet","bennet1709","Cura persona","Dentifricio White Now – Mentadent","75 ml",0.075,2.79,13,V,"−30%, prima 3,99."),
 ("Dentifricio","Bennet","bennet1709","Cura persona","Dentifricio Black carboni attivi – Blanx","75 ml",0.075,2.79,13,V,"−30%, prima 3,99."),
 ("Dentifricio","Bennet","bennet1709","Cura persona","Collutorio Total Care denti e gengive – Listerine","600 ml",0.600,4.19,13,V,"−30%, prima 5,99. È collutorio, non dentifricio: il conto al litro non si confronta con un tubetto."),
 ("Dentifricio","Bennet","bennet1709","Cura persona","Dentifricio vari tipi – Biorepair","75 ml",0.075,3.79,13,V,"−30%, prima 5,42."),
 ("Dentifricio","Bennet","bennet1709","Cura persona","Dentifricio Advanced Pro-Expert – Oral-B","75 ml",0.075,2.99,12,V,"−40%, prima 4,99."),
 ("Carta igienica","Bennet","bennet1709","Cura casa","Carta igienica Maxi – Valenty","4 rotoli",4,1.99,18,V,""),
 ("Carta igienica","Bennet","bennet1709","Cura casa","Carta igienica La Maxi – Nicky","12 rotoli",12,5.89,23,V,"−50%, prima 11,78."),
 ("Asciugatutto","Bennet","bennet1709","Cura casa","Carta cucina – Valenty","2 rotoli",2,1.49,18,V,""),
 ("Asciugatutto","Bennet","bennet1709","Cura casa","Carta casa profumo limone – Nicky","6 rotoli",6,5.99,23,V,"−40%, prima 9,99."),
 ("Ammorbidente","Bennet","bennet1709","Cura casa","Ammorbidente concentrato Blu Oxygen, 48 lavaggi – Vernel","1,056 litri",48,2.99,23,V,"−25%, prima 3,99."),
 ("Lavastoviglie","Bennet","bennet1709","Cura casa","Detersivo in caps 4in1 Excellence, 30 lavaggi – Pril","30 capsule",30,5.94,23,V,"−30%, prima 8,49."),
 ("Lavatrice","Bennet","bennet1709","Cura casa","Detersivo in caps 4in1 classico, 40 o 44 lavaggi – Dixan","40 lavaggi",40,9.79,23,V,"−30%, prima 13,99. La confezione è 40 o 44 lavaggi a seconda del formato, stesso prezzo: qui il conto è sul più piccolo, per non sembrare più conveniente."),
 ("Lavatrice","Bennet","bennet1709","Cura casa","Detersivo liquido Power Extra Smacchiante, 3×23 lavaggi (69) – Dash","3,105 litri",69,12.99,23,V,"−48% SOLO CON LA CARTA BENNET CLUB, prima 24,99."),
 ("Pasta","Bennet","bennet1709","Dispensa","Pasta di semola di grano duro, formati vari – Corticella","500 g",0.500,0.55,18,V,""),
 ("Pasta","Bennet","bennet1709","Dispensa","Pasta di semola, formati vari – Rummo","500 g",0.500,0.84,20,V,"−47% SOLO CON LA CARTA BENNET CLUB, prima 1,59."),
 ("Pasta","Bennet","bennet1709","Freschi","Gnocchi freschi classici – Patamore","500 g",0.500,1.49,22,V,"−50%, prima 2,99. Sono gnocchi freschi, non pasta secca."),
 ("Pasta","Bennet","bennet1709","Freschi","Pasta fresca ripiena, tipi vari – Le ricette di mamma Gaia","400 g",0.400,1.79,19,V,"È pasta fresca ripiena, non secca."),
 ("Pasta","Bennet","bennet1709","Surgelati","Lasagne alla bolognese surgelate – Frosta","600 g",0.600,4.69,22,V,"−20%, prima 5,87. È un piatto pronto surgelato, non pasta secca da cuocere."),
 ("Farina","Bennet","bennet1709","Dispensa","Farina di grano tenero tipo 00","1 kg",1,0.65,18,V,""),
 ("Riso","Bennet","bennet1709","Dispensa","Riso Roma – Gallo","1 kg",1,1.99,20,V,"−46%, prima 3,69."),
 ("Pomodoro","Bennet","bennet1709","Dispensa","Passata di pomodoro al vapore – Valfrutta","700 g",0.700,0.90,20,V,"−43%, prima 1,58."),
 ("Olio d'oliva","Bennet","bennet1709","Dispensa","Olio di oliva classico – Dante","750 ml",0.750,3.99,20,V,"−40%, prima 6,65. È olio di oliva classico, non specificato extravergine."),
 ("Conserve","Bennet","bennet1709","Dispensa","Cipolline sott'aceto – Magie del Gusto","340 g",0.340,1.59,18,V,""),
 ("Biscotti","Bennet","bennet1709","Colazione","Biscotti frollini Griglie Doré","1 kg",1,1.99,18,V,""),
 ("Biscotti","Bennet","bennet1709","Colazione","Biscotti Ciocofroll – Cabrioni","650 g",0.650,1.98,21,V,"−25%, prima 2,65."),
 ("Biscotti","Bennet","bennet1709","Colazione","Snack Baiocchi classici, 6 porzioni – Mulino Bianco","336 g",0.336,2.89,21,V,"−21%, prima 3,67."),
 ("Merendine","Bennet","bennet1709","Colazione","Cornetti classici, 10 pezzi – Casalini","400 g",0.400,1.99,18,V,""),
 ("Merendine","Bennet","bennet1709","Colazione","Croissant farciti albicocca, tipi vari – Bauli","300 g",0.300,1.50,21,V,"−30%, prima 2,15."),
 ("Caffè","Bennet","bennet1709","Colazione","Caffè macinato per moka Premium – Covim","250 g",0.250,2.79,18,V,""),
 ("Caffè","Bennet","bennet1709","Colazione","Capsule caffè macinato compatibili Nespresso, 30 capsule – Kimbo","165 g",0.165,6.99,20,V,"−30%, prima 9,99."),
 ("Birra","Bennet","bennet1709","Bevande","Birra Pilsener – Viktor","500 ml",0.500,0.69,18,V,""),
 ("Birra","Bennet","bennet1709","Bevande","Birra Original – Menabrea","660 ml",0.660,1.18,21,V,"−30%, prima 1,69."),
 ("Acqua","Bennet","bennet1709","Bevande","Acqua frizzante, 6×1,5 litri – Sant'Anna","9 litri",9,2.08,21,V,"−40% SOLO CON LA CARTA BENNET CLUB, prima 3,48."),
 ("Bibite","Bennet","bennet1709","Bevande","Ice tea limone, tipi vari – Lipton","1 litro",1,0.99,21,V,"−33%, prima 1,49."),
 ("Bibite","Bennet","bennet1709","Bevande","Coca-Cola Original Taste","2 litri",2,1.99,21,V,"−32%, prima 2,93."),
 ("Vino","Bennet","bennet1709","Bevande","Primitivo Puglia o Passerina Terre d'Abruzzo IGT – La Fogliata","750 ml",0.750,2.39,21,V,"−40%, prima 3,99."),
 ("Vino","Bennet","bennet1709","Bevande","Syrah, Inzolia, Nero d'Avola o Grillo, vari tipi – Barone Lopresti","750 ml",0.750,2.59,21,V,"−35%, prima 3,99."),
 ("Vino","Bennet","bennet1709","Bevande","Barbera d'Alba DOC – Terre del Barolo","750 ml",0.750,4.89,21,V,"−30%, prima 6,99."),
 ("Yogurt","Bennet","bennet1709","Freschi","Yogurt bifidus frutta e cereali, 8×125 g – Bontà Viva","1 kg",1,3.79,19,V,""),
 ("Burro","Bennet","bennet1709","Freschi","Burro","250 g",0.250,2.49,19,V,""),
 ("Mozzarella","Bennet","bennet1709","Freschi","Mozzarella fior di latte – Arborea","125 g",0.125,0.99,19,V,""),
 ("Mozzarella","Bennet","bennet1709","Freschi","Mozzarella di bufala, 3×100 g – Mandara","300 g",0.300,3.49,22,V,"−30%, prima 4,99."),
 ("Formaggio","Bennet","bennet1709","Freschi","Tilsiter a fette","80 g",0.080,0.99,19,V,""),
 ("Formaggio","Bennet","bennet1709","Freschi","Mix formaggio grattugiato","500 g",0.500,3.99,19,V,""),
 ("Grana","Bennet","bennet1709","Freschi","Grana Padano DOP","700 g",0.700,11.90,19,V,""),
 ("Grana","Bennet","bennet1709","Freschi","Grana Padano DOP – Trentingrana","250 g",0.250,4.79,22,V,"−20%, prima 5,99."),
 ("Grana","Bennet","bennet1709","Freschi","Formaggio grattugiato italiano – Granarolo","90 g",0.090,1.19,22,V,"−40%, prima 1,99. È grattugiato generico, non specificato Grana o Parmigiano DOP."),
 ("Latte","Bennet","bennet1709","Freschi","Latte UHT parzialmente scremato – Granarolo","1 litro",1,0.99,22,V,"−40%, prima 1,65."),
 ("Pollo","Bennet","bennet1709","Macelleria","Fusi di pollo","al kg",1,4.99,19,V,""),
 ("Pollo","Bennet","bennet1709","Dispensa","Carne in scatola leggera di pollo, 2×140 g – Montana","280 g",0.280,1.99,20,V,"−40%, prima 3,32. È carne in scatola, non fresca."),
 ("Salmone","Bennet","bennet1709","Freschi","Salmone norvegese affumicato – Vici","200 g",0.200,5.99,19,V,"È affumicato, non fresco."),
 ("Tonno","Bennet","bennet1709","Dispensa","Tonno all'olio d'oliva in scatola, 12×70 g – Asdomar","840 g",0.840,9.74,20,V,"−35%, prima 14,99."),
 ("Tonno","Bennet","bennet1709","Dispensa","Insalatissime di tonno, tipi vari – Rio Mare","160 g",0.160,2.59,20,V,"−40%, prima 4,32. È insalata di tonno con legumi e mais, non tonno puro."),
 ("Sughi","Bennet","bennet1709","Freschi","Pesto genovese con o senza aglio – Gusto e Convenienza","100 g",0.100,0.99,19,V,""),
 ("Uova","Bennet","bennet1709","Freschi","Uova fresche allevate a terra, 15 pezzi – Podere","15 uova",15,3.99,19,V,""),
 ("Patate","Bennet","bennet1709","Surgelati","Patate stick surgelate – Le Patatose","2,5 kg",2.5,4.90,19,V,"Sono patatine fritte surgelate, non patate fresche."),
 ("Cereali","Bennet","bennet1709","Colazione","Cereali Krave Choco Nut o Milk Choco – Kellogg's","410 g",0.410,2.49,21,V,"−25%, prima 3,32."),
 ("Prosciutto","Bennet","bennet1709","Freschi","Prosciutto cotto Alta Qualità – Parmacotto","100 g",0.100,1.99,22,V,"−50% SOLO CON LA CARTA BENNET CLUB, prima 3,99."),
 ("Prosciutto","Bennet","bennet1709","Freschi","Speck Alto Adige IGP, 2×90 g – Moser","180 g",0.180,3.89,22,V,"−40%, prima 6,49. È speck, non prosciutto crudo classico."),
 ("Verdure surgelate","Bennet","bennet1709","Surgelati","Carciofi a spicchi surgelati – Orogel","300 g",0.300,2.49,22,V,"−37%, prima 3,96."),
 ("Bastoncini","Bennet","bennet1709","Surgelati","Bastoncini di merluzzo, 12 pezzi – Findus","300 g",0.300,2.99,22,V,"−28%, prima 4,19."),
 ("Pizza","Bennet","bennet1709","Surgelati","Pizza Regina Gran Gusto Margherita surgelata – Cameo","350 g",0.350,2.76,22,V,"−30%, prima 3,95."),
 ("Pane","Bennet","bennet1709","Panetteria","Pinsa – Mulino Bianco","230 g",0.230,1.99,22,V,"−33%, prima 2,98. È una base tipo focaccia, non pane a fette."),

 # ----- Eurospin, dal 24 settembre al 4 ottobre (eurospin24), letto per intero il 2026-09-20 -----
 # Trovato online lo stesso giorno in cui scadeva eurospin10: colma il buco di
 # 4 giorni gia segnato in VOLANTINI_ATTESI il 17/9. Molte pagine sono un
 # concorso a tema Bluey (giocattoli, abbigliamento, elettronica, viaggi):
 # scartate in scartate.py, tranne i pochi alimentari Bluey che restano qui.
 # Pagina 12 (Frutta e verdura/Pescheria) ha un elenco di punti vendita
 # aderenti: Torino ne ha diversi, alcuni senza reparto pescheria — segnato
 # nella nota di chi viene dal banco pesce.
 ("Prosciutto","Eurospin","eurospin24","Salumi","Prosciutto Cotto Scelto","150 g",0.150,1.19,1,V,"Prima 1,79."),
 ("Frutta","Eurospin","eurospin24","Ortofrutta","Banane","al kg",1,0.85,1,V,""),
 ("Olio d'oliva","Eurospin","eurospin24","Dispensa","Olio Extra Vergine di Oliva – La Badia","1 l",1,4.29,1,V,"Prima 4,99."),
 ("Frutta","Eurospin","eurospin24","Ortofrutta","Mirtilli Bluey","250 g",0.250,3.49,2,V,"Confezione a tema Bluey, quantità limitata."),
 ("Frutta","Eurospin","eurospin24","Ortofrutta","Uva mix senza semi Bluey","500 g",0.500,2.49,2,V,"Confezione a tema Bluey, quantità limitata."),
 ("Frutta","Eurospin","eurospin24","Ortofrutta","Banane Bluey","al kg",1,1.89,2,V,"Confezione a tema Bluey, quantità limitata. Più care delle banane normali di pagina 1 (0,85 al kg)."),
 ("Frutta","Eurospin","eurospin24","Ortofrutta","Mele Gala Bluey","620 g",0.620,1.29,2,V,"Confezione a tema Bluey, quantità limitata."),
 ("Frutta","Eurospin","eurospin24","Ortofrutta","Susine Angeleno Bluey","500 g",0.500,1.99,2,V,"Confezione a tema Bluey, quantità limitata."),
 ("Frutta","Eurospin","eurospin24","Ortofrutta","Kiwi verdi Bluey","500 g",0.500,1.99,2,V,"Confezione a tema Bluey, quantità limitata."),
 ("Latte","Eurospin","eurospin24","Dispensa","Latte UHT parzialmente scremato vitaminizzato Bluey","1 l",1,1.19,3,V,"Confezione a tema Bluey."),
 ("Bibite","Eurospin","eurospin24","Bevande","100% Succo Arancia Bluey","1 l",1,1.69,3,V,"Confezione a tema Bluey."),
 ("Pasta","Eurospin","eurospin24","Dispensa","Pasta Tricolore Bluey","500 g",0.500,1.59,3,V,"100% grano italiano. Confezione a tema Bluey."),
 ("Asciugatutto","Eurospin","eurospin24","Casa","Asciugatutto decorato Bluey, 2 rotoli, 2 veli, 100 strappi","2 rotoli",2,1.99,3,V,"Confezione a tema Bluey."),
 ("Prosciutto","Eurospin","eurospin24","Salumi","Prosciutto Crudo","100 g",0.100,1.79,4,V,"Prima 2,49."),
 ("Prosciutto","Eurospin","eurospin24","Salumi","Speck Alto Adige IGP","100 g",0.100,1.45,4,V,"Prima 1,85."),
 ("Pollo","Eurospin","eurospin24","Salumi","Petto di pollo al forno – Fresche Fette","140 g",0.140,1.29,4,V,"Prima 1,89. È petto di pollo cotto (un salume), non carne fresca. Solo 2% di grassi."),
 ("Pollo","Eurospin","eurospin24","Salumi","Würstel con pollo e tacchino","1 kg",1,1.99,4,V,"Prima 2,59."),
 ("Grana","Eurospin","eurospin24","Freschi","Parmigiano Reggiano DOP","300 g",0.300,4.99,4,V,"Prima 5,79."),
 ("Formaggio","Eurospin","eurospin24","Freschi","Pecorino Romano DOP grattugiato","100 g",0.100,1.49,4,V,"Prima 1,85."),
 ("Formaggio","Eurospin","eurospin24","Freschi","Provolone Piccante","300 g",0.300,2.49,4,V,"Prima 3,29."),
 ("Formaggio","Eurospin","eurospin24","Freschi","Emmental Francese","250 g",0.250,1.85,4,V,"Prima 2,35."),
 ("Formaggio","Eurospin","eurospin24","Freschi","Feta Greca DOP","200 g",0.200,1.79,4,V,"Prima 2,39."),
 ("Formaggio","Eurospin","eurospin24","Freschi","Burrata","150 g",0.150,1.49,4,V,"Prima 1,89. È burrata, non mozzarella."),
 ("Mozzarella","Eurospin","eurospin24","Freschi","Mozzarella – Land","125 g",0.125,0.59,4,V,"Prima 0,85."),
 ("Burro","Eurospin","eurospin24","Freschi","Burro","250 g",0.250,1.29,5,V,"Prima 1,89."),
 ("Pasta","Eurospin","eurospin24","Freschi","Lasagne al ragù","1 kg",1,3.99,5,V,"Prima 4,99. Piatto pronto al banco frigo, già condito col ragù: non è pasta secca."),
 ("Pasta","Eurospin","eurospin24","Freschi","Tortellini superfini al prosciutto crudo","500 g",0.500,1.99,5,V,"Prima 2,49. Pasta fresca ripiena."),
 ("Salmone","Eurospin","eurospin24","Freschi","Salmone Norvegese Affumicato","150 g",0.150,2.99,5,V,"Prima 3,99."),
 ("Pane","Eurospin","eurospin24","Freschi","Piadina Romagnola IGP alla Riminese","600 g",0.600,1.29,5,V,"Prima 1,69."),
 ("Yogurt","Eurospin","eurospin24","Freschi","Yogurt Cremoso Extra alla vaniglia/bianco","150 g",0.150,0.55,5,V,"Prima 0,75."),
 ("Yogurt","Eurospin","eurospin24","Freschi","Bifidus fibre alla frutta e cereali, 8x125 g","1 kg",1,2.09,5,V,"Prima 2,95."),
 ("Latte","Eurospin","eurospin24","Freschi","Latte Intero UHT","1 l",1,0.75,5,V,"Prima 0,95."),
 ("Pasta","Eurospin","eurospin24","Dispensa","Pasta assortita (penne, spaghetti, fusilli)","1 kg",1,0.75,5,V,"Prima 0,89."),
 ("Riso","Eurospin","eurospin24","Dispensa","Riso Arborio","1 kg",1,1.99,5,V,"Prima 2,79."),
 ("Pomodoro","Eurospin","eurospin24","Dispensa","Polpa di pomodoro a pezzetti","400 g",0.400,0.39,5,V,"Prima 0,59."),
 ("Sughi","Eurospin","eurospin24","Dispensa","Sugo alla salsiccia/Ragù con funghi e salsiccia","400 g",0.400,1.19,5,V,"Prima 1,59."),
 ("Conserve","Eurospin","eurospin24","Dispensa","Funghi trifolati","180 g",0.180,0.79,6,V,"Prima 1,09."),
 ("Tonno","Eurospin","eurospin24","Dispensa","Tonno all'olio d'oliva","160 g",0.160,1.19,6,V,"Prima 1,69."),
 ("Legumi","Eurospin","eurospin24","Dispensa","Fagioli Borlotti, 400 g/sgocc. 240 g","240 g",0.240,0.35,6,V,"Prima 0,49. Il conto usa il peso sgocciolato."),
 ("Pane","Eurospin","eurospin24","Dispensa","Pan Bauletto Integrale","400 g",0.400,0.79,6,V,"Prima 0,99."),
 ("Pane","Eurospin","eurospin24","Dispensa","Cracker salati/integrali","500 g",0.500,0.99,6,V,"Prima 1,25."),
 ("Biscotti","Eurospin","eurospin24","Dispensa","Frollini con grano saraceno","700 g",0.700,1.69,6,V,"Prima 2,19."),
 ("Caffè","Eurospin","eurospin24","Dispensa","Caffè Arabica 100% Qualità Oro","250 g",0.250,2.79,6,V,"Prima 3,69."),
 ("Caffè","Eurospin","eurospin24","Dispensa","Capsule caffè assortite, 20 pz","110 g",0.110,2.89,6,V,"Compatibili Nespresso."),
 ("Miele","Eurospin","eurospin24","Dispensa","Miele Millefiori","500 g",0.500,2.39,6,V,"Prima 3,49."),
 ("Cereali","Eurospin","eurospin24","Dispensa","Muesli croccante al cioccolato al latte","400 g",0.400,1.99,6,V,"Prima 2,69."),
 ("Merendine","Eurospin","eurospin24","Dispensa","Crostatine albicocca/nocciole e cacao","240 g",0.240,0.99,6,V,"Prima 1,39."),
 ("Bibite","Eurospin","eurospin24","Bevande","Bevande assortite ACE, 6x200 ml","1200 ml",1.2,1.29,7,V,"Prima 1,75."),
 ("Bibite","Eurospin","eurospin24","Bevande","Thè alla pesca/al limone zero zucchero","1,5 l",1.5,0.59,7,V,"Prima 0,79."),
 ("Bibite","Eurospin","eurospin24","Bevande","Ginger","1,5 l",1.5,0.59,7,V,"Prima 0,85."),
 ("Bibite","Eurospin","eurospin24","Bevande","Cola/Cola zero, 4x330 ml","1320 ml",1.32,0.99,7,V,"Prima 1,39."),
 ("Birra","Eurospin","eurospin24","Bevande","Birra","330 ml",0.330,0.39,7,V,"Prima 0,49."),
 ("Vino","Eurospin","eurospin24","Bevande","Prosecco DOC Frizzante","750 ml",0.750,2.79,7,V,"Prima 3,89."),
 ("Vino","Eurospin","eurospin24","Bevande","Vino Rosato/Bianco","1 l",1,0.89,7,V,"Prima 1,09."),
 ("Birra","Eurospin","eurospin24","Bevande","Birra Premium Strong Doppio Malto – Best Bräu","500 ml",0.500,0.65,7,V,"Prima 0,89. 8,3% vol."),
 ("Vino","Eurospin","eurospin24","Bevande","Primitivo Salento IGP","750 ml",0.750,1.89,7,V,"Prima 2,55."),
 ("Vino","Eurospin","eurospin24","Bevande","Pecorino/Passerina IGT","750 ml",0.750,1.99,7,V,"Prima 2,99."),
 ("Vino","Eurospin","eurospin24","Bevande","Vermentino di Gallura DOCG","750 ml",0.750,2.99,7,V,"Prima 3,85."),
 ("Carta igienica","Eurospin","eurospin24","Casa","Carta Igienica \"La Fiorita\", 6 rotoli, 4 veli, 150 strappi","6 rotoli",6,1.69,8,V,"Prima 2,49."),
 ("Asciugatutto","Eurospin","eurospin24","Casa","Asciugatutto Extra, 2 rotoli, 3 veli, 100 strappi","2 rotoli",2,1.79,8,V,"Prima 2,49."),
 ("Asciugatutto","Eurospin","eurospin24","Casa","Rotolo Tuttofare Casa, 2 veli, 400 strappi","1 rotolo",1,1.69,8,V,"Prima 2,29."),
 ("Lavatrice","Eurospin","eurospin24","Casa","Lavatrice Classico Superbianco, 42 lavaggi","42 lavaggi",42,3.29,8,V,"Prima 4,29."),
 ("Verdure surgelate","Eurospin","eurospin24","Surgelati","Spinaci a cubetti","600 g",0.600,0.95,9,V,"Prima 1,19. Surgelato."),
 ("Merluzzo","Eurospin","eurospin24","Surgelati","Filetti di Merluzzo Atlantico – Ondina","1 kg",1,5.99,9,V,"Prima 7,49. Surgelato."),
 ("Verdure surgelate","Eurospin","eurospin24","Surgelati","Funghi porcini a cubetti","300 g",0.300,2.69,9,V,"Prima 3,29. Surgelato."),
 ("Pesce","Eurospin","eurospin24","Surgelati","Tranci di pesce spada","450 g",0.450,4.99,9,V,"Prima 6,29. Surgelato."),
 ("Gamberi","Eurospin","eurospin24","Surgelati","Code di mazzancolla tropicale","350 g",0.350,5.49,9,V,"Prima 6,99. Surgelato."),
 ("Sughi","Eurospin","eurospin24","Surgelati","Sugo alle vongole","350 g",0.350,2.19,9,V,"Prima 2,79. Surgelato."),
 ("Salmone","Eurospin","eurospin24","Surgelati","Filetti di salmone Norvegese, 2 pz","250 g",0.250,4.85,9,V,"Prima 6,49. Surgelato."),
 ("Pizza","Eurospin","eurospin24","Surgelati","Pizza würstel e patatine/integrale","225 g",0.225,1.89,9,V,"Surgelata."),
 ("Gelato","Eurospin","eurospin24","Surgelati","Vaschette gelato assortite","500 g",0.500,1.99,9,V,"Prima 2,69."),
 ("Gelato","Eurospin","eurospin24","Surgelati","Coni al croccante/stracciatella, 6 pz","450 g",0.450,2.39,9,V,""),
 ("Gelato","Eurospin","eurospin24","Surgelati","Big Boss al cioccolato, 3 pz","240 g",0.240,1.59,9,V,"Prima 1,99."),
 ("Verdura","Eurospin","eurospin24","Ortofrutta","Pomodoro ciliegino","500 g",0.500,1.29,10,V,""),
 ("Insalata","Eurospin","eurospin24","Ortofrutta","Cuori di iceberg","200 g",0.200,0.69,10,V,""),
 ("Verdura","Eurospin","eurospin24","Ortofrutta","Cipolle bianche","1 kg",1,0.99,10,V,""),
 ("Manzo","Eurospin","eurospin24","Macelleria","Hamburger di Chianina","200 g",0.200,3.49,10,V,"100% carne italiana."),
 ("Suino","Eurospin","eurospin24","Macelleria","Hamburger di suino, 4x100 g","400 g",0.400,2.49,10,V,""),
 ("Pollo","Eurospin","eurospin24","Macelleria","Hamburger di pollo","200 g",0.200,1.29,10,V,""),
 ("Merluzzo","Eurospin","eurospin24","Surgelati","Fishburger di filetto di merluzzo, 2 pz","210 g",0.210,1.79,10,V,"Prima 2,29. Surgelato."),
 ("Patate","Eurospin","eurospin24","Surgelati","Patate rustiche","1,5 kg",1.5,2.49,10,V,"Prima 3,19. Surgelate."),
 ("Pancetta","Eurospin","eurospin24","Salumi","Bacon a fette","150 g",0.150,1.29,11,V,"Prima 1,69."),
 ("Formaggio","Eurospin","eurospin24","Freschi","Edamer a fette","200 g",0.200,1.29,11,V,"Prima 1,79."),
 ("Formaggio","Eurospin","eurospin24","Freschi","Fettine al cheddar","200 g",0.200,0.99,11,V,"Prima 1,49."),
 ("Birra","Eurospin","eurospin24","Bevande","Birra Lager","1 l",1,0.99,11,V,"Prima 1,15."),
 ("Pane","Eurospin","eurospin24","Dispensa","Pane per hamburger senza semi, 6 pz","300 g",0.300,0.79,11,V,"Prima 1,05."),
 ("Pane","Eurospin","eurospin24","Dispensa","Maxi burger con semi di sesamo, 4 pz","300 g",0.300,0.75,11,V,"Prima 0,95."),
 ("Frutta","Eurospin","eurospin24","Ortofrutta","Limoni","1 kg",1,1.69,12,V,""),
 ("Verdura","Eurospin","eurospin24","Ortofrutta","Funghi champignon","500 g",0.500,1.49,12,V,""),
 ("Verdura","Eurospin","eurospin24","Ortofrutta","Melanzane","al kg",1,1.29,12,V,""),
 ("Frutta","Eurospin","eurospin24","Ortofrutta","Arance Valencia","1,5 kg",1.5,2.49,12,V,""),
 ("Verdura","Eurospin","eurospin24","Ortofrutta","Zucchine","al kg",1,1.29,12,V,""),
 ("Insalata","Eurospin","eurospin24","Ortofrutta","Insalata mista","200 g",0.200,0.79,12,V,""),
 ("Pesce","Eurospin","eurospin24","Pescheria","Trancio di pesce spada","170 g",0.170,4.49,12,V,"Solo nei punti vendita con reparto pescheria."),
 ("Merluzzo","Eurospin","eurospin24","Pescheria","Filetto di baccalà dissalato","400 g",0.400,7.75,12,V,"Solo nei punti vendita con reparto pescheria."),
 ("Calamari","Eurospin","eurospin24","Pescheria","Fritto misto","250 g",0.250,3.99,12,V,"Solo nei punti vendita con reparto pescheria. Misto di anelli e simili già pronto."),
 ("Vitello","Eurospin","eurospin24","Macelleria","Fettine scelte di vitello","al kg",1,18.99,13,V,""),
 ("Manzo","Eurospin","eurospin24","Macelleria","Fettine scelte di coscia di bovino adulto, confezione famiglia","al kg",1,16.49,13,V,""),
 ("Suino","Eurospin","eurospin24","Macelleria","Braciole di lombo di suino, confezione famiglia","al kg",1,5.49,13,V,""),
 ("Salsiccia","Eurospin","eurospin24","Macelleria","Luganega di suino","al kg",1,6.99,13,V,""),
 ("Pollo","Eurospin","eurospin24","Macelleria","Cosciotto di pollo, confezione famiglia","al kg",1,2.69,13,V,""),
 ("Prosciutto","Eurospin","eurospin24","Gastronomia","Prosciutto cotto alta qualità","al kg",1,12.99,13,V,"Al banco."),
 ("Salame","Eurospin","eurospin24","Gastronomia","Salame Milano","al kg",1,12.99,13,V,"Al banco. Carne italiana."),
 ("Mortadella","Eurospin","eurospin24","Gastronomia","Mortadella Bologna IGP con/senza pistacchi","al kg",1,8.99,13,V,"Al banco."),
 ("Formaggio","Eurospin","eurospin24","Gastronomia","Toma Piemontese DOP","al kg",1,12.49,13,V,"Al banco."),
 ("Formaggio","Eurospin","eurospin24","Gastronomia","Maasdammer","al kg",1,7.99,13,V,"Al banco."),
 ("Formaggio","Eurospin","eurospin24","Gastronomia","Burrata","250 g",0.250,2.69,13,V,"È burrata, non mozzarella."),
 ("Gelato","Eurospin","eurospin24","Surgelati","Gelatini mix, 9 pz","300 g",0.300,3.19,14,V,"Prima 3,99."),
 ("Pancetta","Eurospin","eurospin24","Salumi","Pancetta coppata","100 g",0.100,2.19,14,V,"Prima 2,69."),
 ("Salame","Eurospin","eurospin24","Salumi","Salame Nostrano","100 g",0.100,2.19,14,V,"Prima 2,59. Carne italiana."),
 ("Pomodoro","Eurospin","eurospin24","Dispensa","Pomodori pelati, 800 g/sgocc. 500 g","500 g",0.500,0.75,14,V,"Prima 1,09. Il conto usa il peso sgocciolato."),
 ("Olio di semi","Eurospin","eurospin24","Dispensa","Prodotto per friggere","1 l",1,1.49,14,V,"Prima 1,99."),
 ("Legumi","Eurospin","eurospin24","Dispensa","Fagioli Red Kidney, 410 g/sgocc. 242 g","242 g",0.242,0.49,14,V,"Prima 0,69. Il conto usa il peso sgocciolato."),
 ("Pane","Eurospin","eurospin24","Dispensa","Panetti croccanti con sesamo","300 g",0.300,2.29,14,V,"Prima 2,69."),
 ("Salsiccia","Eurospin","eurospin24","Salumi","Salsiccia Napoli piccante","320 g",0.320,2.29,15,V,"Prima 2,79."),
 ("Salame","Eurospin","eurospin24","Salumi","Spianata piccante calabrese","100 g",0.100,1.99,15,V,"Prima 2,49. Carne italiana."),
 ("Formaggio","Eurospin","eurospin24","Freschi","Dolcetto mascarpone e gorgonzola","200 g",0.200,1.89,15,V,"Prima 2,49."),
 ("Pasta","Eurospin","eurospin24","Dispensa","Pasta integrale trafilata al bronzo assortita","500 g",0.500,0.65,15,V,"Prima 0,79."),
 ("Riso","Eurospin","eurospin24","Dispensa","Riso Ribe Parboiled per insalate","1 kg",1,1.49,15,V,"Prima 1,85."),
 ("Pomodoro","Eurospin","eurospin24","Dispensa","Polpa di datterino, 2x230 g","460 g",0.460,1.19,15,V,"Prima 1,39."),
 ("Olio d'oliva","Eurospin","eurospin24","Dispensa","Olio Extravergine non filtrato","1 l",1,4.99,15,V,"Prima 6,49."),
 ("Conserve","Eurospin","eurospin24","Dispensa","Olive nere/verdi di Spagna denocciolate","150 g",0.150,0.99,15,V,"Prima 1,25."),
 ("Legumi","Eurospin","eurospin24","Dispensa","Piselli fini, 400 g/sgocc. 270 g","270 g",0.270,0.69,15,V,"Prima 0,79. Il conto usa il peso sgocciolato."),
 ("Pane","Eurospin","eurospin24","Dispensa","Crostini dorati","275 g",0.275,1.59,15,V,"Prima 1,99."),
 ("Pane","Eurospin","eurospin24","Dispensa","Grissini all'olio di oliva","200 g",0.200,0.79,15,V,"Prima 0,99."),
 ("Bibite","Eurospin","eurospin24","Bevande","Sete di frutta zero con arancia, carota e limone","1 l",1,0.99,15,V,"Prima 1,19."),
 ("Bibite","Eurospin","eurospin24","Bevande","Aranciata con arance siciliane, 4x330 ml","1320 ml",1.32,1.49,15,V,"Prima 1,79."),
 ("Carta igienica","Eurospin","eurospin24","Casa","Carta igienica, 4 rotoli, 2 veli, 300 strappi","4 rotoli",4,1.39,15,V,"Prima 1,79."),
 ("Lavatrice","Eurospin","eurospin24","Casa","Liquido lavatrice con agenti smacchianti/salva colore, 40 lavaggi","40 lavaggi",40,2.89,15,V,"Prima 3,69."),
 ("Frutta","Eurospin","eurospin24","Ortofrutta","Avocado","200 g",0.200,0.99,22,V,"«Doppio weekend di follia», valido solo da venerdì 25 a domenica 27 settembre.","2026-09-25","2026-09-27"),
 ("Ricotta","Eurospin","eurospin24","Freschi","Mascarpone Cremoso","250 g",0.250,1.09,22,V,"Prima 1,69. «Doppio weekend di follia», valido solo da venerdì 25 a domenica 27 settembre.","2026-09-25","2026-09-27"),
 ("Mozzarella","Eurospin","eurospin24","Freschi","Mozzarella di Bufala Campana DOP, 3x100 g","300 g",0.300,2.49,22,V,"Prima 3,59. «Doppio weekend di follia», valido solo da venerdì 25 a domenica 27 settembre.","2026-09-25","2026-09-27"),
 ("Manzo","Eurospin","eurospin24","Macelleria","Macinato sceltissimo di bovino adulto","al kg",1,12.99,22,V,"«Doppio weekend di follia», valido solo da venerdì 25 a domenica 27 settembre.","2026-09-25","2026-09-27"),
 ("Pomodoro","Eurospin","eurospin24","Dispensa","Passata densa di pomodoro","700 g",0.700,0.79,22,V,"Prima 1,19. «Doppio weekend di follia», valido solo da venerdì 25 a domenica 27 settembre.","2026-09-25","2026-09-27"),
 ("Tonno","Eurospin","eurospin24","Dispensa","Tonno all'olio vegetale, 4x80 g","320 g",0.320,2.19,22,V,"Prima 3,39. «Doppio weekend di follia», valido solo da venerdì 25 a domenica 27 settembre.","2026-09-25","2026-09-27"),
 ("Frutta","Eurospin","eurospin24","Ortofrutta","Uva bianca senza semi","500 g",0.500,1.49,22,V,"«Doppio weekend di follia», valido solo da venerdì 2 a domenica 4 ottobre.","2026-10-02","2026-10-04"),
 ("Suino","Eurospin","eurospin24","Macelleria","Macinato di suino","al kg",1,5.99,22,V,"«Doppio weekend di follia», valido solo da venerdì 2 a domenica 4 ottobre.","2026-10-02","2026-10-04"),
 ("Olio di semi","Eurospin","eurospin24","Dispensa","Olio di semi di arachide","1 l",1,1.99,22,V,"Prima 2,89. «Doppio weekend di follia», valido solo da venerdì 2 a domenica 4 ottobre.","2026-10-02","2026-10-04"),
 ("Gamberi","Eurospin","eurospin24","Surgelati","Gamberi Indopacifici sgusciati","350 g",0.350,2.49,22,V,"Prima 3,99. Surgelati. «Doppio weekend di follia», valido solo da venerdì 2 a domenica 4 ottobre.","2026-10-02","2026-10-04"),
 ("Latte","Eurospin","eurospin24","Freschi","Latte parzialmente scremato UHT, 6x500 ml","3 l",3,2.60,22,V,"Prezzo valido solo comprando 6 confezioni insieme (vendita abbinata): il volantino non dà il prezzo di una confezione sola. «Doppio weekend di follia», valido solo da venerdì 2 a domenica 4 ottobre.","2026-10-02","2026-10-04"),

# LIDL, dal 24 al 30 settembre. Letto per intero il 2026-09-22 (52 pagine).
# Molte pagine sono "Approfittane ora" senza data propria: valgono tutto il
# periodo del volantino, quindi niente inizio/fino sulla riga. Le pagine con
# una data stampata più corta ("Da giovedì 24/09 al 27/09" o "Da lunedì
# 28/09") hanno inizio/fino scritti riga per riga, perché sono davvero un
# sottoperiodo diverso da quello del volantino intero.
 ("Manzo","Lidl","lidl24","Macelleria","Macinato di bovino adulto","500 g",0.500,4.99,1,V,"Con Lidl Plus. Senza tessera 5,99, cioè 11,98 al kg. Allevato in Italia."),
 ("Manzo","Lidl","lidl24","Macelleria","Hamburger di bovino di razza Piemontese","200 g",0.200,2.99,8,V,"Prima 3,49."),
 ("Manzo","Lidl","lidl24","Macelleria","Tartare di bovino adulto scottona","200 g",0.200,3.59,8,V,"Prima 4,59."),
 ("Suino","Lidl","lidl24","Macelleria","Braciole di suino","700 g",0.700,3.69,8,V,"Prima 4,69."),
 ("Suino","Lidl","lidl24","Macelleria","Spiedini piccanti di pollo e suino","500 g",0.500,4.79,8,V,"È misto pollo e suino, non solo suino."),
 ("Salsiccia","Lidl","lidl24","Macelleria","Tris di salsicce di suino","650 g",0.650,4.99,8,V,""),
 ("Pollo","Lidl","lidl24","Macelleria","Sovracosce di pollo","1000 g",1,3.39,8,V,"Con Lidl Plus. Senza tessera 4,49."),
 ("Pollo","Lidl","lidl24","Macelleria","Fusi di pollo","800 g",0.800,2.99,9,V,"Con Lidl Plus. Senza tessera 3,89."),
 ("Pollo","Lidl","lidl24","Macelleria","Gran burger di pollo XXL con panatura croccante","560 g",0.560,4.49,9,V,"Panato, non petto puro."),
 ("Pollo","Lidl","lidl24","Macelleria","Cotoletta croccante di pollo","220 g",0.220,1.99,9,V,"Panata, non petto puro."),
 ("Tacchino","Lidl","lidl24","Macelleria","Polpettine di tacchino con suino","360 g",0.360,2.79,9,V,"Contengono anche suino, non solo tacchino."),
 ("Tacchino","Lidl","lidl24","Salumi","Affettato di petto di tacchino o di pollo – Idee Gustose","140 g",0.140,1.79,15,V,"Senza glutine. Stesso prezzo anche nella versione pollo."),
 ("Pesce","Lidl","lidl24","Pesce","Trancio di pesce spada – Mare Gioioso","170 g",0.170,3.49,9,V,"Con Lidl Plus. Senza tessera 4,49."),
 ("Pesce","Lidl","lidl24","Pesce","Filetto di branzino – Gastronomia di Mare","230 g",0.230,4.19,9,V,"Prima 5,39."),
 ("Calamari","Lidl","lidl24","Pesce","Anelli di totano gigante del Pacifico, al naturale","250 g",0.250,3.49,9,V,""),
 ("Calamari","Lidl","lidl24","Surgelati","Anelli di totano in pastella con aglio e prezzemolo – Sol&Mar","500 g",0.500,2.79,46,V,"In pastella, surgelati."),
 ("Prosciutto","Lidl","lidl24","Salumi","Prosciutto crudo nazionale – Deluxe","90 g",0.090,2.39,14,V,"Con Lidl Plus. Senza tessera 3,09. Stagionatura minima 24 mesi."),
 ("Prosciutto","Lidl","lidl24","Salumi","Jamón Serrano STG – Sol&Mar","240 g",0.240,4.49,52,V,"Stagionato minimo 11 mesi.","2026-09-28","2026-09-30"),
 ("Salame","Lidl","lidl24","Salumi","Salametto Cacciatore DOP – Italiamo","160 g",0.160,2.69,18,V,""),
 ("Salame","Lidl","lidl24","Salumi","Snack di salame spagnolo essiccato Fuet o Chorizo – Sol&Mar","80 g",0.080,1.39,44,V,"È salame secco spagnolo, fuet o chorizo."),
 ("Salsiccia","Lidl","lidl24","Salumi","Chorizo affettato – Sol&Mar","100 g",0.100,1.49,44,V,"È chorizo, salsiccia spagnola piccante di carne suina."),
 ("Grana","Lidl","lidl24","Latteria","Grana Padano DOP Riserva grattugiato – Deluxe","90 g",0.090,1.29,14,V,"Con Lidl Plus. Senza tessera 1,65. Stagionato oltre 20 mesi."),
 ("Formaggio","Lidl","lidl24","Latteria","Provolone Valpadana DOP dolce – Italiamo","300 g",0.300,2.19,3,V,"Prima 3,19.","2026-09-24","2026-09-27"),
 ("Formaggio","Lidl","lidl24","Latteria","Mascarpone e Gorgonzola – Italiamo","200 g",0.200,1.89,14,V,"Con Lidl Plus. Senza tessera 2,49. È un mix di mascarpone e gorgonzola, non un formaggio unico."),
 ("Formaggio","Lidl","lidl24","Latteria","Scamorza dolce senza lattosio – Latteria","100 g",0.100,1.19,15,V,""),
 ("Formaggio","Lidl","lidl24","Latteria","Formaggino Mio – Nestlé","125 g",0.125,1.39,48,V,"","2026-09-28","2026-09-30"),
 ("Spalmabili","Lidl","lidl24","Latteria","Philadelphia","2x62 g",0.124,1.19,15,V,"Prima 1,49."),
 ("Yogurt","Lidl","lidl24","Latteria","Yogurt fior di latte o alla vaniglia senza lattosio – Latteria","150 g",0.150,0.79,21,V,""),
 ("Yogurt","Lidl","lidl24","Latteria","Ayo Kefir senza lattosio – Arborea","140 g",0.140,0.79,48,V,"","2026-09-28","2026-09-30"),
 ("Latte","Lidl","lidl24","Latteria","Latte parzialmente scremato senza lattosio – Latteria Free From","6x1 litro",6,5.59,21,V,"Formato convenienza: il formato base costa 1,09 al litro, questo 0,93."),
 ("Burro","Lidl","lidl24","Latteria","Burro XXL – Milbona","1000 g",1,5.49,21,V,"Formato convenienza: il formato base (500 g) costa 7,38 al kg, questo 5,49."),
 ("Tonno","Lidl","lidl24","Dispensa","Tonno all'olio di oliva – Nostromo","4x104 g, sgocciolati 416 g",0.416,5.99,10,V,""),
 ("Tonno","Lidl","lidl24","Dispensa","Tonno all'olio di oliva 3+1 – Puerto Dorado","4x160 g, sgocciolati 425 g",0.4254,4.05,15,V,"Con Lidl Plus. Senza tessera 5,40. Offerta 3+1: un pezzo da solo costa 6,33. Il volantino conta il prezzo sul peso sgocciolato."),
 ("Verdure surgelate","Lidl","lidl24","Surgelati","Piselli finissimi – Freshona","450 g",0.450,0.75,3,V,"Prima 0,99.","2026-09-24","2026-09-27"),
 ("Verdure surgelate","Lidl","lidl24","Surgelati","Minestrone leggero – Freshona","700 g",0.700,1.05,15,V,"Prima 1,29."),
 ("Pizza","Lidl","lidl24","Surgelati","Pizza Margherita – Italiamo","390 g",0.390,1.99,14,V,"Con Lidl Plus. Senza tessera 2,49."),
 ("Pasta","Lidl","lidl24","Dispensa","Tortellini al prosciutto crudo – Fini","450 g",0.450,1.99,10,V,""),
 ("Pasta","Lidl","lidl24","Dispensa","Pasta trafilata al bronzo IGP, linguine/spaghetti/rigatoni/fusilli/penne – Italiamo","500 g",0.500,0.99,18,V,""),
 ("Pane","Lidl","lidl24","Panetteria","Pan bauletto integrale XXL – Certossa","600 g",0.600,1.19,21,V,"Formato convenienza: il formato base (400 g) costa 0,89, cioè 2,23 al kg; questo 1,98 al kg."),
 ("Pane","Lidl","lidl24","Panetteria","Grissini con semi di girasole – Sol&Mar","166 g",0.166,1.19,47,V,"","2026-09-28","2026-09-30"),
 ("Pane","Lidl","lidl24","Panetteria","Mini grissini al gusto di olive e rosmarino – Sol&Mar","110 g",0.110,1.29,47,V,"","2026-09-28","2026-09-30"),
 ("Biscotti","Lidl","lidl24","Colazione","Occhi di bue di pasta frolla XXL – Sondey","400 g",0.400,2.39,21,V,"Formato XXL, 100 g in più: il formato base (300 g) costa 7,97 al kg, questo 5,98."),
 ("Biscotti","Lidl","lidl24","Colazione","Gran Merenda, biscotto frollino senza latte e senza uova – Crich","500 g",0.500,1.99,20,V,""),
 ("Biscotti","Lidl","lidl24","Colazione","Biscotti I Puffi al latte, miele e cereali – Delser","350 g",0.350,2.19,20,V,""),
 ("Biscotti","Lidl","lidl24","Colazione","Nascondini – Mulino Bianco","600 g",0.600,2.99,21,V,"","2026-09-28","2026-09-30"),
 ("Biscotti","Lidl","lidl24","Colazione","Baiocchi al pistacchio – Mulino Bianco","168 g",0.168,1.99,21,V,"","2026-09-28","2026-09-30"),
 ("Cereali","Lidl","lidl24","Colazione","Farro soffiato bio al cioccolato – Crownfield","150 g",0.150,1.39,21,V,"Prima 1,79. Farro 100% italiano."),
 ("Cereali","Lidl","lidl24","Colazione","Farro soffiato bio al miele – Crownfield","150 g",0.150,1.49,21,V,"Prima 1,89. Farro 100% italiano."),
 ("Creme","Lidl","lidl24","Colazione","Crema spalmabile al pistacchio XXL – Deluxe","350 g",0.350,4.49,20,V,"Formato convenienza: il formato base (190 g) costa 2,99, cioè 15,74 al kg; questo 12,83 al kg."),
 ("Creme","Lidl","lidl24","Colazione","Crema spalmabile Choco&Jam, diversi gusti – Mister Choc","200 g",0.200,1.99,20,V,""),
 ("Marmellata","Lidl","lidl24","Colazione","Confetture Extra, gelsi neri e fichi bianchi – Agrisicilia","340 g",0.340,2.49,20,V,"C'è anche il gusto fragola, 360 g, stesso prezzo, cioè 6,92 al kg."),
 ("Cioccolato","Lidl","lidl24","Colazione","Cioccolato al latte con nocciole tritate – Fin Carré","100 g",0.100,0.79,16,V,"Prima 0,99."),
 ("Merendine","Lidl","lidl24","Colazione","Magdalenas – Sol&Mar","615 g",0.615,2.89,47,V,"","2026-09-28","2026-09-30"),
 ("Caffè","Lidl","lidl24","Colazione","Caffè macinato Crema e Gusto – Lavazza","4x250 g",1,10.99,1,V,""),
 ("Caffè","Lidl","lidl24","Colazione","Capsule A Modo Mio Crema&Gusto o Qualità Rossa – Lavazza","540 g, 72 capsule",0.540,18.99,49,V,"","2026-09-28","2026-09-30"),
 ("Acqua","Lidl","lidl24","Bevande","Acqua minerale naturale – Sant'Anna","24x0,5 litri",12,3.99,10,V,""),
 ("Acqua","Lidl","lidl24","Bevande","Acqua minerale naturale – Levissima","6x1,5 litri",9,1.99,2,V,"Vendita alla confezione: un pezzo da solo non in promo costa 0,49.","2026-09-24","2026-09-27"),
 ("Vino","Lidl","lidl24","Bevande","Salice Salentino DOC","0,75 litri",0.750,1.99,17,V,"Prima 2,49."),
 ("Vino","Lidl","lidl24","Bevande","Custoza DOC","0,75 litri",0.750,1.69,17,V,"Con Lidl Plus. Senza tessera 1,99."),
 ("Vino","Lidl","lidl24","Bevande","Corte Aurelio Nero d'Avola Sicilia DOC","0,75 litri",0.750,1.79,17,V,"Prima 2,29."),
 ("Vino","Lidl","lidl24","Bevande","Chiaravita Cerasuolo d'Abruzzo DOC","0,75 litri",0.750,1.59,17,V,"Con Lidl Plus. Senza tessera 1,99."),
 ("Vino","Lidl","lidl24","Bevande","Libertario Tempranillo tinto La Mancha DO","0,75 litri",0.750,1.99,47,V,"","2026-09-28","2026-09-30"),
 ("Birra","Lidl","lidl24","Bevande","Peroni Birra 4,7% Vol.","0,5 litri",0.500,0.79,1,V,""),
 ("Bibite","Lidl","lidl24","Bevande","Bevanda alla frutta tropicale o multivitaminico – Pfanner","1,5 litri",1.5,1.39,11,V,""),
 ("Bibite","Lidl","lidl24","Bevande","SanThè alla pesca o al limone – Sant'Anna","4x200 ml",0.800,1.19,11,V,""),
 ("Bibite","Lidl","lidl24","Bevande","Coca-Cola Zero, senza zuccheri caffeina e calorie","0,5 litri",0.500,0.75,11,V,""),
 ("Bibite","Lidl","lidl24","Bevande","Coca-Cola Regular","4x0,5 litri",2,2.99,49,V,"","2026-09-28","2026-09-30"),
 ("Lavatrice","Lidl","lidl24","Casa","Detersivo lavatrice in polvere – Omino Bianco","3,85 kg, 70 lavaggi",70,7.99,13,V,""),
 ("Lavatrice","Lidl","lidl24","Casa","Power Caps, 70 lavaggi – Dixan","70 lavaggi",70,11.49,13,V,""),
 ("Lavatrice","Lidl","lidl24","Casa","Detersivo liquido nero, 54+4 lavaggi – Perlana","2,9 litri, 58 lavaggi",58,6.99,12,V,""),
 ("Lavatrice","Lidl","lidl24","Casa","Detersivo liquido igienizzante, 44 lavaggi – Omino Bianco","3x1,76 litri, 44 lavaggi",44,9.79,12,V,""),
 ("Lavastoviglie","Lidl","lidl24","Casa","Gel Ultimate, 2x50 lavaggi – Finish","2x900 ml, 100 lavaggi",100,9.89,13,V,""),
 ("Ammorbidente","Lidl","lidl24","Casa","Ammorbidente diluito classico, 50 lavaggi – Felce Azzurra","2 litri",2,2.69,13,V,""),
 ("Ammorbidente","Lidl","lidl24","Casa","Ammorbidente concentrato Fresco mattino o Vaniglia, 86 lavaggi – Fabuloso","1,9 litri",1.9,2.99,13,V,""),
 ("Dentifricio","Lidl","lidl24","Igiene","Dentifricio Sensation White, Max White o Max Fresh – Colgate","75 ml",0.075,2.19,17,V,"Prima 2,99."),
 ("Dentifricio","Lidl","lidl24","Igiene","Dentifricio White Now o Protect Plus – Mentadent","2x75 ml",0.150,3.85,49,V,"","2026-09-28","2026-09-30"),
 ("Shampoo","Lidl","lidl24","Igiene","Shampoo o Balsamo Ultra Dolce – Garnier","400 ml, formato balsamo",0.400,3.59,13,V,"Lo shampoo, formato 600 ml, costa lo stesso 3,59 (5,98 al litro); qui è il formato balsamo, 400 ml, più caro al litro (8,98)."),
 ("Conserve","Lidl","lidl24","Dispensa","Olive verdi Manzanilla farcite con peperoni rossi o acciughe – Sol&Mar","170 g, sgocciolati",0.170,1.49,45,V,"","2026-09-28","2026-09-30"),
 ("Conserve","Lidl","lidl24","Dispensa","Olive verdi spagnole denocciolate e marinate – Sol&Mar","150 g",0.150,2.29,45,V,"","2026-09-28","2026-09-30"),
 ("Conserve","Lidl","lidl24","Dispensa","Peperoncini verdi sottaceto – Sol&Mar","130 g, sgocciolati",0.130,2.49,46,V,""),
 ("Legumi","Lidl","lidl24","Dispensa","Ceci cotti – Sol&Mar","400 g, sgocciolati",0.400,0.99,52,V,"","2026-09-28","2026-09-30"),
 ("Insalata","Lidl","lidl24","Ortofrutta","Insalate Regionali alla lombarda o alla trentina – Bonduelle","130 g",0.130,2.29,48,V,"Con noci e mele o con miele e noci, non solo insalata in foglia.","2026-09-28","2026-09-30"),
 ("Frutta","Lidl","lidl24","Ortofrutta","Mele Gala IGP Trentino/Alto Adige","2 kg",2,2.19,1,V,"Prima 2,99."),
 ("Frutta","Lidl","lidl24","Ortofrutta","Prugne","1 kg",1,1.49,5,V,"Con Lidl Plus. Senza tessera 1,99.","2026-09-24","2026-09-27"),
 ("Frutta","Lidl","lidl24","Ortofrutta","Uva bianca, cassetta 2 kg","2 kg",2,2.99,5,V,""),
 ("Frutta","Lidl","lidl24","Ortofrutta","Uva Red Globe","al kg",1,1.99,52,V,"Prima 2,99.","2026-09-28","2026-09-30"),
 ("Frutta","Lidl","lidl24","Ortofrutta","Pere Var. Carmen","1 kg",1,1.79,52,V,"Con Lidl Plus. Senza tessera 2,49.","2026-09-28","2026-09-30"),
 ("Verdura","Lidl","lidl24","Ortofrutta","Zucchine sfuse","al kg",1,1.79,5,V,"Con Lidl Plus. Senza tessera 2,49."),
 ("Verdura","Lidl","lidl24","Ortofrutta","Pomodori Grappolo sfusi","al kg",1,2.49,5,V,"Con Lidl Plus. Senza tessera 3,49."),
 ("Verdura","Lidl","lidl24","Ortofrutta","Pomodori ciliegino Pachino IGP","300 g",0.300,1.49,4,V,""),
 ("Verdura","Lidl","lidl24","Ortofrutta","Zucca Hokkaido","al kg",1,1.49,5,V,"Con Lidl Plus. Senza tessera 1,99.","2026-09-24","2026-09-27"),
 ("Verdura","Lidl","lidl24","Ortofrutta","Carote","al kg",1,1.09,52,V,"Con Lidl Plus. Senza tessera 1,49.","2026-09-28","2026-09-30"),
 ("Patate","Lidl","lidl24","Ortofrutta","Patate Iodi – Pizzoli","1,5 kg rete",1.5,2.19,52,V,"Prima 3,19.","2026-09-28","2026-09-30"),

# EKOM, «I più ekonomici», dal 22 settembre al 5 ottobre. Letto per intero il
# 2026-09-22 dal sito ufficiale (ekomdiscount.it), non più kimbino: vedi
# pagine_ekom.py. Manlio l'aveva già visto di carta il 19/9 e segnalato di
# nuovo il 22/9 col link diretto (kimbino non lo aveva ancora, il sito
# ufficiale sì). Tutto il volantino vale dal 22 settembre al 5 ottobre,
# nessuna pagina ha un periodo più corto.
 ("Caffè","Ekom","ekom22","Colazione","Caffè macinato Aroma Oro","250 g",0.250,2.99,2,V,""),
 ("Caffè","Ekom","ekom22","Colazione","Espresso Bar, 100 capsule","550 g",0.550,12.69,2,V,"Prima 16,99."),
 ("Merendine","Ekom","ekom22","Colazione","Croissant cioccolato, albicocca o crema","400 g",0.400,1.89,2,V,""),
 ("Biscotti","Ekom","ekom22","Colazione","Biscotti Cabrioni, diversi tipi","650 g",0.650,1.79,2,V,""),
 ("Biscotti","Ekom","ekom22","Colazione","Biscotti Buongrano – Mulino Bianco","350 g",0.350,1.59,2,V,"Prima 1,99."),
 ("Creme","Ekom","ekom22","Colazione","Fior di Nocciola, crema cacao e nocciola bicolore","400 g",0.400,1.59,2,V,"Prima 1,99."),
 ("Cioccolato","Ekom","ekom22","Colazione","Barrette di cioccolato al latte, 16 pezzi","200 g",0.200,1.99,2,V,"Prima 2,49."),
 ("Pane","Ekom","ekom22","Panetteria","Cracker Fiori d'Acqua – Mulino Bianco","250 g",0.250,1.25,2,V,"Prima 1,79."),
 ("Riso","Ekom","ekom22","Dispensa","Riso Arborio","1 kg",1,1.99,2,V,"Prima 2,79."),
 ("Pane","Ekom","ekom22","Panetteria","Baguette precotta, 2 pezzi","300 g",0.300,0.79,2,V,"Prima 0,99."),
 ("Pomodoro","Ekom","ekom22","Dispensa","Passata di pomodoro – Pomì","750 g",0.750,0.99,2,V,"Prima 1,49."),
 ("Salmone","Ekom","ekom22","Dispensa","Filetti di salmone all'olio vegetale","150 g",0.150,2.49,3,V,"È in scatola, non fresco."),
 ("Tonno","Ekom","ekom22","Dispensa","Filetti di tonno all'olio di semi di girasole","180 g",0.180,2.39,3,V,"Prima 2,99."),
 ("Tonno","Ekom","ekom22","Dispensa","Trancetti di tonno in olio di girasole, formato scorta 12x80 g – Moretti","960 g",0.960,5.99,3,V,"Prima 8,99."),
 ("Acqua","Ekom","ekom22","Bevande","Acqua Alpi Cozie, frizzante o naturale, 12x500 ml","6 litri",6,1.89,3,V,""),
 ("Bibite","Ekom","ekom22","Bevande","Bevanda alla frutta A+C+E, gusti assortiti","1,5 litri",1.5,1.39,3,V,""),
 ("Birra","Ekom","ekom22","Bevande","Birra Classic","500 ml",0.500,0.53,3,V,"Prima 0,69."),
 ("Birra","Ekom","ekom22","Bevande","Birra Extra Stout","500 ml",0.500,0.99,3,V,"Prima 1,39."),
 ("Vino","Ekom","ekom22","Bevande","Nebbiolo delle Langhe DOC","750 ml",0.750,4.25,3,V,"Prima 5,69."),
 ("Vino","Ekom","ekom22","Bevande","Bonarda dell'Oltrepò Pavese DOC – Fratelli Maggi","750 ml",0.750,1.99,3,V,""),
 ("Vino","Ekom","ekom22","Bevande","Pinot Nero IGT","750 ml",0.750,2.39,3,V,"Prima 3,29."),
 ("Vino","Ekom","ekom22","Bevande","Müller Thurgau delle Venezie IGT","750 ml",0.750,2.89,3,V,"Prima 3,89."),
 ("Vino","Ekom","ekom22","Bevande","Cabernet Sauvignon","750 ml",0.750,1.99,3,V,"Prima 2,69."),
 ("Lavastoviglie","Ekom","ekom22","Cura casa","Gel Lavastoviglie Tutto in 1, 57 lavaggi – Scala","750 ml, 57 lavaggi",57,0.99,4,V,"Prima 1,29."),
 ("Ammorbidente","Ekom","ekom22","Cura casa","Ammorbidente profumato, 40 lavaggi – Solbat","2 litri, 40 lavaggi",2,1.29,4,V,"Prima 1,79."),
 ("Carta igienica","Ekom","ekom22","Cura casa","Carta igienica 2 veli, 4 maxi rotoli (=8) – Dayly","4 rotoli maxi",8,1.19,5,V,"Prima 1,49. 4 rotoli maxi valgono come 8 normali."),
 ("Asciugatutto","Ekom","ekom22","Cura casa","Asciugatutto monorotolo decorato 3 veli, 300 strappi – Lalynea","1 rotolo",1,2.39,5,V,"Prima 2,99."),
 ("Asciugatutto","Ekom","ekom22","Cura casa","Asciugatutto 2 veli, 6 rotoli – Bravo","6 rotoli",6,2.79,5,V,"Prima 3,99."),
 ("Burro","Ekom","ekom22","Freschi","Burro","500 g",0.500,2.99,6,V,"Prima 4,49."),
 ("Yogurt","Ekom","ekom22","Freschi","Yogurt cremoso bianco&nocciole e cioccolato","150 g",0.150,0.59,6,V,"Prima 0,79."),
 ("Formaggio","Ekom","ekom22","Freschi","Fette di formaggio – Bon Fette, 20 pezzi","400 g",0.400,1.99,6,V,""),
 ("Mozzarella","Ekom","ekom22","Freschi","Mozzarella","100 g",0.100,0.69,6,V,"Prima 0,89."),
 ("Mozzarella","Ekom","ekom22","Freschi","Mozzarelle fior di latte ciliegine, 8x25 g","200 g",0.200,1.69,6,V,"Prima 2,19."),
 ("Mozzarella","Ekom","ekom22","Freschi","Mozzarella julienne","200 g",0.200,1.59,6,V,"Prima 1,99."),
 ("Pasta","Ekom","ekom22","Freschi","Pasta fresca ripiena, diversi tipi – MammAmore","500 g",0.500,1.19,6,V,"Prima 1,69. Sono tortelloni freschi, non pasta secca."),
 ("Ricotta","Ekom","ekom22","Freschi","Mascarpone","500 g",0.500,2.79,6,V,"Prima 3,49."),
 ("Formaggio","Ekom","ekom22","Freschi","Stracchino senza lattosio","150 g",0.150,1.49,6,V,"Prima 1,89."),
 ("Formaggio","Ekom","ekom22","Freschi","Caprino di latte di capra","80 g",0.080,0.99,6,V,"Prima 1,29."),
 ("Formaggio","Ekom","ekom22","Freschi","Luna di Primosale","200 g",0.200,1.49,6,V,"Prima 1,99."),
 ("Formaggio","Ekom","ekom22","Freschi","Gorgonzola dolce DOP","400 g",0.400,3.49,7,V,""),
 ("Formaggio","Ekom","ekom22","Freschi","Formaggio grattugiato mix","100 g",0.100,0.79,7,V,"Prima 0,99."),
 ("Formaggio","Ekom","ekom22","Freschi","Formaggio Telemea de Vacca – Bayernland","800 g",0.800,5.99,7,V,""),
 ("Pasta","Ekom","ekom22","Freschi","Pasta fresca, orecchiette o trofie","1 kg",1,1.69,7,V,"Sono fresche, non pasta secca."),
 ("Uova","Ekom","ekom22","Freschi","10 uova piccole \"S\"","10 uova",10,2.19,7,V,""),
 ("Salsiccia","Ekom","ekom22","Salumi","Fette di cotechino senza glutine","150 g (3 fette)",0.150,1.49,7,V,"Prima 1,99. È cotechino, salume cotto di maiale, non salsiccia fresca."),
 ("Suino","Ekom","ekom22","Salumi","Würstel Griglia&Famiglia","1 kg",1,2.59,7,V,"Sono würstel, non carne fresca."),
 ("Prosciutto","Ekom","ekom22","Salumi","Prosciutto cotto – Salumi Belletti","100 g",0.100,1.29,7,V,""),
 ("Mortadella","Ekom","ekom22","Salumi","Mortadella intera","150 g",0.150,1.19,7,V,"Prima 1,49."),
 ("Frutta","Ekom","ekom22","Ortofrutta","Uva Italia","750 g",0.750,2.59,8,V,""),
 ("Frutta","Ekom","ekom22","Ortofrutta","Uva Pizzutella","750 g",0.750,2.99,8,V,""),
 ("Frutta","Ekom","ekom22","Ortofrutta","Uva nera","750 g",0.750,1.99,8,V,""),
 ("Frutta","Ekom","ekom22","Ortofrutta","Mele Golden","al kg",1,1.49,8,V,""),
 ("Verdura","Ekom","ekom22","Ortofrutta","Pomodori a grappolo","al kg",1,1.99,8,V,""),
 ("Patate","Ekom","ekom22","Ortofrutta","Patate Selenella","1,5 kg rete",1.5,2.49,8,V,""),
 ("Prosciutto","Ekom","ekom22","Gastronomia","Speck Alto Adige IGP, al banco","al kg",1,19.90,9,V,"Il volantino stampa 1,99 all'etto. Vale solo nei negozi col banco servito."),
 ("Bresaola","Ekom","ekom22","Gastronomia","Bresaola punta d'anca IGP – Rigamonti, al banco","al kg",1,34.90,9,V,"Il volantino stampa 3,49 all'etto. Vale solo nei negozi col banco servito."),
 ("Prosciutto","Ekom","ekom22","Gastronomia","Prosciutto cotto alta qualità – Riccafetta, al banco","al kg",1,15.90,9,V,"Il volantino stampa 1,59 all'etto, prima 1,99. Vale solo nei negozi col banco servito."),
 ("Prosciutto","Ekom","ekom22","Gastronomia","Prosciutto crudo, al banco","al kg",1,16.90,9,V,"Il volantino stampa 1,69 all'etto. Vale solo nei negozi col banco servito."),
 ("Formaggio","Ekom","ekom22","Gastronomia","Caciottina Bosco Gerolo, al banco","al kg",1,9.90,9,V,"Il volantino stampa 0,99 all'etto. Vale solo nei negozi col banco servito."),
 ("Ricotta","Ekom","ekom22","Gastronomia","Ricotta Vallelata, al banco","al kg",1,6.90,9,V,"Il volantino stampa 0,69 all'etto. Vale solo nei negozi col banco servito."),
 ("Formaggio","Ekom","ekom22","Gastronomia","Gorgonzola dolce DOP, al banco","al kg",1,11.90,9,V,"Il volantino stampa 1,19 all'etto. Vale solo nei negozi col banco servito."),
 ("Formaggio","Ekom","ekom22","Gastronomia","Certosa – Galbani, al banco","al kg",1,11.90,9,V,"Il volantino stampa 1,19 all'etto. Vale solo nei negozi col banco servito."),
 ("Manzo","Ekom","ekom22","Macelleria","Arrosto di bovino adulto","al kg",1,19.90,9,V,"Vale solo nei negozi col banco servito."),
 ("Manzo","Ekom","ekom22","Macelleria","Costata di bovino adulto","al kg",1,18.90,9,V,"Vale solo nei negozi col banco servito."),
 ("Manzo","Ekom","ekom22","Macelleria","Polpa magra di bovino adulto","al kg",1,16.90,9,V,"Vale solo nei negozi col banco servito."),
 ("Pollo","Ekom","ekom22","Macelleria","Fuselli di pollo","al kg",1,4.90,9,V,"Vale solo nei negozi col banco servito."),
 ("Pollo","Ekom","ekom22","Macelleria","Rustichelle di pollo BBQ","al kg",1,13.90,9,V,"Vale solo nei negozi col banco servito."),
 ("Suino","Ekom","ekom22","Macelleria","Lonza di suino a tranci, confezione risparmio","al kg",1,7.90,9,V,"Vale solo nei negozi col banco servito."),
 ("Cereali","Ekom","ekom22","Colazione","High Protein Müesli – Cameo","300 g",0.300,2.89,10,V,"Prima 3,69."),
 ("Bibite","Ekom","ekom22","Bevande","Best Hydration, arancia/limone/frutti di bosco – Sant'Anna","330 ml",0.330,0.69,10,V,"Prima 0,99."),
 ("Bibite","Ekom","ekom22","Bevande","Sport Drink, limone o arancio","500 ml",0.500,0.59,10,V,"Prima 0,79."),
 ("Creme","Ekom","ekom22","Colazione","Peanut Butter, 100% arachidi – Fiorentini","350 g",0.350,2.79,10,V,"Prima 3,49. È burro di arachidi, non crema al cioccolato."),
 ("Bibite","Ekom","ekom22","Bevande","Powerade, diversi tipi","500 ml",0.500,1.09,10,V,""),
 ("Shampoo","Ekom","ekom22","Cura persona","Doccia Shampoo Luxury, diversi tipi","500 ml",0.500,0.85,11,V,"Prima 1,25. È un 2 in 1 doccia e shampoo."),
 ("Lavatrice","Ekom","ekom22","Cura casa","Detersivo capi sportivi, 18 lavaggi – Chanteclair","900 ml, 18 lavaggi",18,2.19,11,V,"Prima 2,99."),
 ("Manzo","Ekom","ekom22","Macelleria","Polpettine di carne bovina – Amica Natura","500 g",0.500,3.99,14,V,"Solo con la carta EKOM UP. Senza tessera 4,99."),
 ("Spalmabili","Ekom","ekom22","Freschi","Philadelphia Classico","220 g",0.220,2.19,14,V,"Solo con la carta EKOM UP."),
 ("Olio di semi","Ekom","ekom22","Dispensa","Olio di semi di girasole – Dante","1 litro",1,2.19,14,V,"Solo con la carta EKOM UP. Senza tessera 2,79."),
 ("Tonno","Ekom","ekom22","Dispensa","Tonno all'olio di oliva, 6x120 g – Rio Mare","720 g",0.720,8.99,14,V,"Solo con la carta EKOM UP. Senza tessera 11,99."),
 ("Conserve","Ekom","ekom22","Dispensa","Olive olivolì nere toste – Saclà","100 g",0.100,0.79,14,V,"Solo con la carta EKOM UP. Senza tessera 0,99."),
 ("Bibite","Ekom","ekom22","Bevande","Coca Cola Classica, 6x330 ml","1,98 litri",1.98,3.99,14,V,"Solo con la carta EKOM UP. Senza tessera 4,99."),
 ("Birra","Ekom","ekom22","Bevande","Birra Nastro Azzurro – Peroni","500 ml",0.500,0.99,14,V,"Solo con la carta EKOM UP."),
 ("Vino","Ekom","ekom22","Bevande","Vino DOC Capetta, Monferrato Chiaretto o Cortese dell'Alto Monferrato","750 ml",0.750,2.99,14,V,"Solo con la carta EKOM UP. Senza tessera 4,69."),
 ("Lavastoviglie","Ekom","ekom22","Cura casa","Pastiglie lavastoviglie Tutto in 1 Extra, 36 lavaggi – Pril","36 lavaggi",36,5.59,14,V,"Solo con la carta EKOM UP. Senza tessera 7,99."),
 ("Carta igienica","Ekom","ekom22","Cura casa","Carta igienica That's Amore, 8 rotoli 4 veli – Lalynea","8 rotoli",8,1.99,14,V,"Solo con la carta EKOM UP. Senza tessera 2,99."),
 ("Calamari","Ekom","ekom22","Surgelati","Tentacoli di totano gigante","500 g",0.500,2.99,15,V,"Prima 3,99."),
 ("Merluzzo","Ekom","ekom22","Surgelati","Filetti di merluzzo d'Alaska","400 g",0.400,1.99,15,V,"Prima 2,99."),
 ("Merluzzo","Ekom","ekom22","Surgelati","Filetti di platessa impanati","300 g",0.300,2.99,15,V,"Prima 3,99. Sono impanate."),
 ("Verdure surgelate","Ekom","ekom22","Surgelati","Spinaci in cubi","1 kg",1,1.49,15,V,"Prima 1,99."),
 ("Verdure surgelate","Ekom","ekom22","Surgelati","Minestrone","450 g",0.450,0.79,15,V,"Prima 0,99."),
 ("Verdure surgelate","Ekom","ekom22","Surgelati","Contorno broccoli e patate","450 g",0.450,1.99,15,V,"Prima 2,49."),
 ("Patate","Ekom","ekom22","Surgelati","Patate stick prefritte","1 kg",1,1.49,15,V,"Prima 1,99."),
 ("Sughi","Ekom","ekom22","Surgelati","Sugo alle vongole – Appetais","300 g",0.300,2.39,15,V,"Prima 2,99."),
 ("Gelato","Ekom","ekom22","Surgelati","Gelato stecco Mini King","280 g",0.280,2.79,15,V,"Prima 3,49."),
 ("Gelato","Ekom","ekom22","Surgelati","Vaschetta gelato, gusti assortiti – Kome Te","400 g",0.400,1.49,15,V,"Prima 1,99."),
 ("Tè","Ekom","ekom22","Colazione","Tè verde freddo, diversi gusti, 16 filtri – Everton","40 g",0.040,1.99,16,V,"Prima 2,49."),
 ("Formaggio","Ekom","ekom22","Freschi","Camembert francese","250 g",0.250,2.49,16,V,""),
 ("Formaggio","Ekom","ekom22","Freschi","Feta greca DOP a cubetti","150 g",0.150,2.49,16,V,""),
 ("Salmone","Ekom","ekom22","Freschi","Salmone affumicato","200 g",0.200,5.49,16,V,""),
 ("Yogurt","Ekom","ekom22","Freschi","Yogurt greco, magro, magro senza lattosio o intero","150 g",0.150,0.79,16,V,"Prima 0,99."),
 ("Pizza","Ekom","ekom22","Surgelati","Pizza Kebab","420 g",0.420,2.99,16,V,"Prima 3,99."),
 ("Gelato","Ekom","ekom22","Surgelati","Gelato Mochi Maka Flavor, cocco/vaniglia/mango","180 g",0.180,3.49,16,V,""),
 # ---------------------------------------------------------------------------
 # IPERCOOP «Extra offerte», 24 settembre-7 ottobre 2026 (ipercoop24).
 # Lette a occhio tutte e 47 le pagine il 2026-09-22, edizione TORINO-COLLEGNO
 # (id 28831 su volantinopiu): le altre tredici edizioni di Nova Coop hanno
 # qualche prezzo diverso, vedi il commento in VOLANTINI.
 # I prezzi «solo per i soci» e gli sconti soci sono segnati riga per riga,
 # come si fa con la MD Buona Spesa Card e con la carta EKOM UP.
 # ---------------------------------------------------------------------------

 # --- pagina 1 (copertina) ---
 ("Frutta","Ipercoop","ipercoop24","Ortofrutta","Uva bianca senza semi – Fior Fiore","1 kg",1,3.28,1,V,"Bollino «Conviene»."),
 ("Manzo","Ipercoop","ipercoop24","Macelleria","Hamburger di chianina – Linea You&Meat","200 g",0.200,4.49,1,V,"Bollino «Conviene». Il volantino stampa 22,45 al kg. Ci sono anche altri tipi allo stesso prezzo."),
 ("Pomodoro","Ipercoop","ipercoop24","Dispensa","Passata rustica Cirio","2 × 680 g (1+1)",1.360,1.69,1,V,"È un 1+1: si pagano 1,69 e se ne portano via due. Una confezione sola costa 2,49. Il volantino stampa 1,25 al kg."),
 # --- pagina 2 (1+1 e sconti 50%) ---
 ("Biscotti","Ipercoop","ipercoop24","Colazione","Frollini Gran Dispensa Colussi, tipi vari","2 × 565 g (1+1)",1.130,3.49,2,V,"È un 1+1: si pagano 3,49 e se ne portano via due. Una confezione sola costa 3,49. Il volantino stampa 3,09 al kg."),
 ("Pane","Ipercoop","ipercoop24","Panetteria","Piadina Sfogliatissima all'olio Loriana","2 × 350 g (1+1)",0.700,2.59,2,V,"È un 1+1: si pagano 2,59 e se ne portano via due. Una confezione sola costa 2,59. Il volantino stampa 3,70 al kg."),
 ("Olio d'oliva","Ipercoop","ipercoop24","Dispensa","Olio extra vergine di oliva Classico Zucchi","2 × 1 litro (1+1)",2,9.90,2,V,"È un 1+1: si pagano 9,90 e se ne portano via due. Una bottiglia sola costa 9,90. Il volantino stampa 4,95 al litro."),
 ("Vino","Ipercoop","ipercoop24","Bevande","Gutturnio frizzante D.O.C. rosso Podere Cantagallo – Cantina Valtidone","2 × 750 ml (1+1)",1.500,5.49,2,V,"È un 1+1: si pagano 5,49 e se ne portano via due. Una bottiglia sola costa 5,49. Il volantino stampa 3,66 al litro."),
 ("Bagnoschiuma","Ipercoop","ipercoop24","Igiene","Bagnodoccia Spuma di Sciampagna, varie profumazioni","2 × 650 ml (1+1)",1.300,2.79,2,V,"È un 1+1: si pagano 2,79 e se ne portano via due. Un flacone solo costa 2,79. Il volantino stampa 2,15 al litro."),
 ("Dentifricio","Ipercoop","ipercoop24","Igiene","Dentifricio Mentadent P white system o microgranuli","4 × 75 ml (1+1 da due)",0.300,4.85,2,V,"È un 1+1: si pagano 4,85 e si portano via due confezioni da due tubetti. Una confezione sola costa 4,85. Il volantino stampa 16,17 al litro."),
 ("Ammorbidente","Ipercoop","ipercoop24","Cura casa","Ammorbidente concentrato Coccolino, tipi vari","2 × 1,827 litri, 174 lavaggi (1+1)",174,6.99,2,V,"È un 1+1: si pagano 6,99 e se ne portano via due. Un flacone solo costa 6,99 e fa 87 lavaggi. Il volantino stampa 1,92 al litro."),
 ("Ricotta","Ipercoop","ipercoop24","Freschi","Ricotta Granarolo","450 g",0.450,1.50,2,V,"Sconto del 50%: prima 3,00. Il volantino stampa 3,33 al kg."),
 ("Lavatrice","Ipercoop","ipercoop24","Cura casa","Detersivo liquido per lavatrice Dash classico","3,105 litri, 3 × 23 lavaggi",69,11.85,2,V,"Sconto del 50%: prima 23,70. Offerta limitata. Il volantino stampa 3,82 al litro."),
 # --- pagina 3 («1,2,3 più compri meno paghi») ---
 ("Manzo","Ipercoop","ipercoop24","Macelleria","Hamburgerini di scottona – Fior Fiore","240 g",0.240,6.28,3,V,"Prezzo di una confezione sola (26,17 al kg). Comprandone due 10,04 (5,02 l'una), tre 13,17 (4,39 l'una, cioè 18,29 al kg). Dal quarto pezzo in poi si paga il prezzo più basso; massimo 12 pezzi per scontrino."),
 ("Mozzarella","Ipercoop","ipercoop24","Freschi","Mozzarella Latte Fieno Brimi","3 × 100 g",0.300,4.29,3,V,"Prezzo di una confezione sola (14,30 al kg). Comprandone due 6,00 (3,00 l'una), tre 7,71 (2,57 l'una, cioè 8,57 al kg). Dal quarto pezzo in poi si paga il prezzo più basso."),
 ("Latte","Ipercoop","ipercoop24","Latteria","Latte UHT parzialmente scremato Arborea","1 litro",1,1.39,3,V,"Prezzo di una confezione sola. Comprandone due 1,94 (0,97 l'una), tre 2,49 (0,83 l'una). Dal quarto pezzo in poi si paga il prezzo più basso."),
 ("Pollo","Ipercoop","ipercoop24","Freschi","Würstel Wudy Cocktail AIA","350 g",0.350,2.99,3,V,"Sono würstel di pollo e tacchino. Prezzo di una confezione sola (8,54 al kg). Comprandone due 4,18 (2,09 l'una), tre 5,37 (1,79 l'una, cioè 5,11 al kg)."),
 ("Bagnoschiuma","Ipercoop","ipercoop24","Igiene","Sapone liquido Felce Azzurra, varie profumazioni","300 ml",0.300,1.42,3,V,"Prezzo di un flacone solo (4,73 al litro). Comprandone due 2,26 (1,13 l'uno), tre 2,97 (0,99 l'uno, cioè 3,30 al litro)."),
 # --- pagina 6 ---
 ("Latte","Ipercoop","ipercoop24","Latteria","Latte microfiltrato parzialmente scremato o intero Origine Coop","1 litro",1,1.19,6,V,"Vale solo dal 28 settembre al 4 ottobre, non per tutto il volantino. Latte 100% italiano.","2026-09-28","2026-10-04"),
 # --- pagina 7 ---
 ("Merendine","Ipercoop","ipercoop24","Colazione","Croissant classico Melegatti","240 g",0.240,0.99,7,V,"Bollino «Conviene». Il volantino stampa 4,13 al kg."),
 ("Caffè","Ipercoop","ipercoop24","Colazione","Caffè Oro Lavazza","500 g (2 × 250 g)",0.500,11.99,7,V,"Solo per i soci Coop. Il volantino stampa 23,98 al kg."),
 ("Caffè","Ipercoop","ipercoop24","Colazione","Caffè Aroma Napoli Kimbo","750 g (3 × 250 g)",0.750,11.90,7,V,"Bollino «Conviene». Il volantino stampa 15,87 al kg."),
 ("Biscotti","Ipercoop","ipercoop24","Colazione","Biscotto Salute Monviso classico o integrale","500 g",0.500,3.09,7,V,"Bollino «Conviene». Il volantino stampa 6,18 al kg."),
 ("Marmellata","Ipercoop","ipercoop24","Colazione","Composta di frutta zero zuccheri Zuegg","230 g",0.230,2.39,7,V,"Solo per i soci Coop. Il volantino stampa 10,39 al kg."),
 ("Cereali","Ipercoop","ipercoop24","Colazione","Granola Fitness Nestlé, cioccolato o avena","300 g",0.300,1.53,7,V,"Sconto soci del 40%: senza tessera 2,55, cioè 8,50 al kg. Il volantino stampa 5,10 al kg."),
 ("Merendine","Ipercoop","ipercoop24","Colazione","Choco Wafer Milka, gusti vari","180 g",0.180,1.99,7,V,"Bollino «Conviene». Il volantino stampa 11,06 al kg."),
 ("Cioccolato","Ipercoop","ipercoop24","Dispensa","KitKat, gusti vari","124,5 g",0.1245,1.99,7,V,"Bollino «Conviene». Il volantino stampa 15,98 al kg."),
 ("Creme","Ipercoop","ipercoop24","Colazione","Crema spalmabile CremaNovi, barattolo","350 g",0.350,5.99,7,V,"Bollino «Conviene». Il volantino stampa 17,11 al kg."),
 ("Merendine","Ipercoop","ipercoop24","Colazione","Pandorì Bauli classico o farcito, formati vari","150 g (classico)",0.150,1.79,7,V,"Bollino «Conviene». Il conto è sul formato classico da 150 g. Il volantino stampa 11,93 al kg."),
 ("Biscotti","Ipercoop","ipercoop24","Colazione","Biscotti Oro Saiwa 5 cereali","420 g",0.420,1.79,7,V,"Bollino «Conviene». Il volantino stampa 4,26 al kg."),
 # --- pagina 8 ---
 ("Pasta","Ipercoop","ipercoop24","Dispensa","Pasta di semola Voiello, formati vari","500 g",0.500,0.89,8,V,"Solo per i soci Coop. Il volantino stampa 1,78 al kg."),
 ("Pasta","Ipercoop","ipercoop24","Dispensa","Pasta all'uovo La Pasta di Camerino, formati vari","250 g",0.250,1.32,8,V,"Sconto soci del 30%: senza tessera 1,89, cioè 7,56 al kg. Il volantino stampa 5,28 al kg."),
 ("Riso","Ipercoop","ipercoop24","Dispensa","Riso Carnaroli Gallo","1 kg",1,2.79,8,V,"Bollino «Conviene»."),
 ("Pomodoro","Ipercoop","ipercoop24","Dispensa","Passata siciliana con Piccadilly Agromonte","660 g",0.660,0.99,8,V,"Sconto del 50%: prima 1,99. Il volantino stampa 1,50 al kg."),
 # --- pagina 9 ---
 ("Olio d'oliva","Ipercoop","ipercoop24","Dispensa","Olio extra vergine di oliva grezzo naturale Il Casolare Farchioni","1 litro",1,8.19,9,V,"Solo per i soci Coop."),
 ("Tonno","Ipercoop","ipercoop24","Dispensa","Tonno pescato a canna all'olio di oliva Rio Mare","960 g (12 × 80 g)",0.960,12.90,9,V,"Bollino «Conviene». Il conto è sul peso della scatola, come fa il volantino (13,44 al kg): sgocciolato il tonno è meno, quindi al chilo costa di più."),
 ("Tonno","Ipercoop","ipercoop24","Dispensa","Filetto di tonno in olio Il Tonnotto, vaso di vetro, gusto delicato","415 g",0.415,4.95,9,V,"Sconto del 50%: prima 9,90. Il conto è sul peso del vaso, come fa il volantino (11,93 al kg): il peso sgocciolato non è stampato, quindi al chilo di tonno costa di più."),
 # --- pagina 10 (bevande) ---
 ("Birra","Ipercoop","ipercoop24","Bevande","Birra Ichnusa anima sarda","660 ml",0.660,0.95,10,V,"Bollino «Conviene». Il volantino stampa 1,44 al litro."),
 ("Birra","Ipercoop","ipercoop24","Bevande","Birra Bud","990 ml (3 × 330 ml)",0.990,2.29,10,V,"Bollino «Conviene». Il volantino stampa 2,31 al litro."),
 ("Birra","Ipercoop","ipercoop24","Bevande","Birra Beck's, lattina","440 ml",0.440,0.89,10,V,"Sconto soci del 40%: senza tessera 1,49, cioè 3,39 al litro. Il volantino stampa 2,03 al litro."),
 ("Vino","Ipercoop","ipercoop24","Bevande","Fira I.G.T. Sartori, bianco o rosso Verona","750 ml",0.750,3.99,10,V,"Bollino «Conviene». Il volantino stampa 5,32 al litro."),
 ("Vino","Ipercoop","ipercoop24","Bevande","Soave D.O.C. Pasqua","750 ml",0.750,2.75,10,V,"Sconto del 40%: prima 4,59, cioè 6,12 al litro. Il volantino stampa 3,67 al litro."),
 ("Vino","Ipercoop","ipercoop24","Bevande","Freschello Rosso","750 ml",0.750,1.59,10,V,"Solo per i soci Coop. Il volantino stampa 2,12 al litro."),
 ("Vino","Ipercoop","ipercoop24","Bevande","Refosco D.O.C. Tenimenti Civa","750 ml",0.750,6.49,10,V,"Bollino «Conviene». Il volantino stampa 8,65 al litro."),
 ("Vino","Ipercoop","ipercoop24","Bevande","Prosecco Treviso D.O.C. Maschio","750 ml",0.750,4.13,10,V,"Sconto soci del 30%: senza tessera 5,90, cioè 7,87 al litro. Il volantino stampa 5,51 al litro."),
 ("Bibite","Ipercoop","ipercoop24","Bevande","Pepsi classica o zero","2 litri",2,1.39,10,V,"Bollino «Conviene». Il volantino stampa 0,70 al litro."),
 ("Acqua","Ipercoop","ipercoop24","Bevande","Acqua Levissima naturale","1,5 litri",1.5,0.31,10,V,"Solo per i soci Coop. Il volantino stampa 0,21 al litro."),
 # --- pagina 11 (surgelati) ---
 ("Pizza","Ipercoop","ipercoop24","Surgelati","Pizza Ristorante Cameo, gusti e formati vari","320 g (al salame)",0.320,2.39,11,V,"Bollino «Conviene». Il conto è sul formato al salame da 320 g. Il volantino stampa 7,47 al kg."),
 ("Verdure surgelate","Ipercoop","ipercoop24","Surgelati","Buon Minestrone Orogel","750 g",0.750,1.54,11,V,"Sconto del 50%: prima 3,09, cioè 4,12 al kg. Il volantino stampa 2,05 al kg."),
 ("Gelato","Ipercoop","ipercoop24","Surgelati","Gelato Cornetto Soft Algida, 4 pezzi, formati vari","324 g (cookies & chocolate)",0.324,2.79,11,V,"Solo per i soci Coop. Il conto è sul formato cookies & chocolate da 324 g. Il volantino stampa 8,61 al kg."),
 ("Gamberi","Ipercoop","ipercoop24","Surgelati","Gamberi argentini Grand Krust, surgelati","400 g",0.400,6.90,11,V,"Bollino «Conviene». Il volantino stampa 17,25 al kg."),
 ("Merluzzo","Ipercoop","ipercoop24","Surgelati","Fiori di merluzzo d'Alaska Capitan Findus, 10 pezzi","500 g",0.500,7.69,11,V,"Solo per i soci Coop. Il volantino stampa 15,38 al kg."),
 ("Patate","Ipercoop","ipercoop24","Surgelati","Le Patatine Original McCain, surgelate","1,04 kg",1.040,2.29,11,V,"Solo per i soci Coop. Sono patatine fritte surgelate, non patate fresche. Il volantino stampa 2,20 al kg."),
 ("Verdure surgelate","Ipercoop","ipercoop24","Surgelati","Friarielli Cubello Orogel","600 g",0.600,2.49,11,V,"Bollino «Conviene». Il volantino stampa 4,15 al kg."),
 ("Verdure surgelate","Ipercoop","ipercoop24","Surgelati","Spinaci Primavera Findus","800 g",0.800,2.49,11,V,"Bollino «Conviene». Il volantino stampa 3,11 al kg."),
 ("Merluzzo","Ipercoop","ipercoop24","Surgelati","Croccole di merluzzo Capitan Findus, 2 pezzi","216 g",0.216,2.79,11,V,"Solo per i soci Coop. Sono impanate, non filetto nudo. Il volantino stampa 12,92 al kg."),
 ("Verdure surgelate","Ipercoop","ipercoop24","Surgelati","Pisellini Primavera Findus","700 g",0.700,3.59,11,V,"Bollino «Conviene». Il volantino stampa 5,13 al kg."),
 # --- pagina 12 (latteria) ---
 ("Yogurt","Ipercoop","ipercoop24","Latteria","Yogurt intero Müller, gusti vari","250 g (2 × 125 g)",0.250,0.86,12,V,"Sconto del 40%: prima 1,44, cioè 5,76 al kg. Il volantino stampa 3,44 al kg."),
 ("Latte","Ipercoop","ipercoop24","Latteria","Latte UHT Alta Digeribilità Candia","1 litro",1,1.19,12,V,"Bollino «Conviene»."),
 ("Merendine","Ipercoop","ipercoop24","Colazione","Dessert Cake Pops Bontà Divina, limone o cacao","84 g (3 × 28 g)",0.084,1.99,12,V,"Bollino «Conviene». Il conto è sui 3 × 28 g scritti sulla confezione: il volantino stampa 23,27 al kg."),
 ("Formaggio","Ipercoop","ipercoop24","Freschi","Fiocchi di latte Santa Lucia Galbani, formato scorta","360 g (2 × 180 g)",0.360,2.49,12,V,"Bollino «Conviene». Il volantino stampa 6,92 al kg."),
 ("Formaggio","Ipercoop","ipercoop24","Freschi","Stracchino alta qualità Granarolo","320 g",0.320,2.98,12,V,"Bollino «Conviene». Il volantino stampa 9,31 al kg."),
 ("Spalmabili","Ipercoop","ipercoop24","Freschi","Philadelphia Light","210 g",0.210,1.99,12,V,"Solo per i soci Coop. Il volantino stampa 9,48 al kg."),
 ("Formaggio","Ipercoop","ipercoop24","Freschi","Camoscio d'Oro","200 g",0.200,2.29,12,V,"Bollino «Conviene». Il volantino stampa 11,45 al kg."),
 # --- pagina 13 (salumi e freschi) ---
 ("Bresaola","Ipercoop","ipercoop24","Salumi","Bresaola della Valtellina I.G.P. Rigamonti, bipacco","180 g (2 × 90 g)",0.180,6.57,13,V,"Sconto del 40%: prima 10,95, cioè 60,84 al kg. Il volantino stampa 36,50 al kg."),
 ("Mozzarella","Ipercoop","ipercoop24","Freschi","Mozzarella fior di latte Vallelata","375 g (3 × 125 g)",0.375,3.09,13,V,"Bollino «Conviene». Il volantino stampa 8,24 al kg."),
 ("Prosciutto","Ipercoop","ipercoop24","Salumi","Speck Coop","100 g",0.100,1.69,13,V,"È speck, cioè prosciutto crudo affumicato. Il volantino stampa 16,90 al kg."),
 ("Pancetta","Ipercoop","ipercoop24","Salumi","Pancetta a cubetti Tulip, dolce o affumicata","100 g",0.100,1.13,13,V,"Sconto del 40%: prima 1,89, cioè 18,90 al kg. Il volantino stampa 11,30 al kg."),
 ("Grana","Ipercoop","ipercoop24","Freschi","Grana Padano D.O.P. Virgilio, fresco","700 g",0.700,10.90,13,V,"Bollino «Conviene». Il volantino stampa 15,57 al kg."),
 ("Uova","Ipercoop","ipercoop24","Freschi","Uova da galline allevate a terra Naturelle","6 pezzi",6,1.95,13,V,"Sconto soci del 30%: senza tessera 2,79."),
 # --- pagina 14 (macelleria) ---
 ("Pollo","Ipercoop","ipercoop24","Macelleria","Petto di pollo a fette AIA","al kg",1,11.06,14,V,"Sconto del 30%: prima 15,81 al kg."),
 ("Manzo","Ipercoop","ipercoop24","Macelleria","Macinato di bovino adulto razza piemontese – Fior Fiore","400 g",0.400,6.38,14,V,"Sconto soci del 20%: senza tessera 7,98, cioè 19,95 al kg. Il volantino stampa 15,95 al kg."),
 ("Vitello","Ipercoop","ipercoop24","Macelleria","Fettine scelte di vitello","al kg",1,21.58,14,V,"Sconto del 20%: prima 26,98 al kg."),
 ("Suino","Ipercoop","ipercoop24","Macelleria","Linea Mini Spiedini Martini, tipi vari","300 g (di suino)",0.300,3.71,14,V,"Sconto soci del 30%: senza tessera 5,30, cioè 17,67 al kg. Il conto è sul formato di suino da 300 g. Il volantino stampa 12,37 al kg."),
 ("Pollo","Ipercoop","ipercoop24","Macelleria","Linea Fidatissimi Amadori, tipi e formati vari","600 g (cotoletta)",0.600,5.57,14,V,"Sconto soci del 40%: 7,43 con lo sconto del 20% per tutti (12,38 al kg), 9,29 senza sconti (15,49 al kg). Il conto è sulla cotoletta da 600 g. Il volantino stampa 9,28 al kg col prezzo soci."),
 ("Pollo","Ipercoop","ipercoop24","Macelleria","Bocconcini di petto di pollo SQ Coop","400 g",0.400,3.96,14,V,"Sconto soci del 25%: senza tessera 5,28, cioè 13,20 al kg. Il volantino stampa 9,90 al kg."),
 ("Pollo","Ipercoop","ipercoop24","Macelleria","Mini rollé di pollo Fileni","600 g",0.600,6.99,14,V,"Bollino «Conviene». Sono di pollo con suino e tacchino. Il volantino stampa 11,65 al kg."),
 ("Tacchino","Ipercoop","ipercoop24","Macelleria","Linea Bon Roll di tacchino AIA, vari gusti","680 g",0.680,6.99,14,V,"Bollino «Conviene». Il volantino stampa 10,28 al kg."),
 # --- pagina 15 (pesce, gastronomia, panetteria) ---
 ("Pesce","Ipercoop","ipercoop24","Pescheria","Branzino allevato Cromaris","al kg",1,12.67,15,V,"Sconto soci del 25%: senza tessera 16,90 al kg."),
 ("Salmone","Ipercoop","ipercoop24","Freschi","Trancio di salmone affumicato a caldo Mowi, gusti vari","125 g",0.125,5.19,15,V,"Sconto del 20%: prima 6,49, cioè 51,92 al kg. È affumicato, non salmone fresco. Il volantino stampa 41,52 al kg."),
 ("Pasta","Ipercoop","ipercoop24","Freschi","Spätzle Valsugana Sapori, verdi o tricolore","500 g",0.500,2.93,15,V,"Sconto soci del 30%: senza tessera 4,19, cioè 8,38 al kg. È pasta fresca. Il volantino stampa 5,86 al kg."),
 ("Pasta","Ipercoop","ipercoop24","Freschi","Tortellini Gastronomia Piccinini","250 g",0.250,3.63,15,V,"Sconto del 30%: prima 5,19, cioè 20,76 al kg. È pasta fresca ripiena. Il volantino stampa 14,52 al kg."),
 ("Pane","Ipercoop","ipercoop24","Panetteria","Filone Pan Premium, fibre mais e sesamo","300 g",0.300,1.99,15,V,"Bollino «Conviene». Il volantino stampa 6,63 al kg."),
 ("Pane","Ipercoop","ipercoop24","Panetteria","Mini pinsa Alimenta","300 g",0.300,2.39,15,V,"Bollino «Conviene». Il volantino stampa 7,97 al kg."),
 ("Merendine","Ipercoop","ipercoop24","Panetteria","Sogno al cioccolato e albicocca","90 g",0.090,0.85,15,V,"Bollino «Conviene». Il volantino stampa 9,44 al kg."),
 ("Biscotti","Ipercoop","ipercoop24","Panetteria","Pasticceria secca mista Alle Cascine","400 g",0.400,4.79,15,V,"Solo per i soci Coop. Il volantino stampa 11,98 al kg."),
 # --- pagina 16 (banco taglio, prezzi all'etto) ---
 ("Prosciutto","Ipercoop","ipercoop24","Salumi","Prosciutto di Parma D.O.P., stagionatura 16 mesi, al banco","all'etto (100 g)",0.100,2.59,16,V,"Bollino «Conviene». Il volantino stampa 25,90 al kg."),
 ("Prosciutto","Ipercoop","ipercoop24","Salumi","Prosciutto cotto alta qualità Riccafetta Raspini, al banco","all'etto (100 g)",0.100,1.39,16,V,"Bollino «Conviene». Il volantino stampa 13,90 al kg."),
 ("Salame","Ipercoop","ipercoop24","Salumi","Salame Milano, al banco","all'etto (100 g)",0.100,1.59,16,V,"Bollino «Conviene». Il volantino stampa 15,90 al kg."),
 ("Pancetta","Ipercoop","ipercoop24","Salumi","Guanciale stagionato Gardani, 2 fette","200 g",0.200,3.13,16,V,"Sconto soci del 30%: senza tessera 4,49, cioè 22,45 al kg. È guanciale, non pancetta. Il volantino stampa 15,65 al kg."),
 ("Formaggio","Ipercoop","ipercoop24","Freschi","Gorgonzola D.O.P., circa 200 g, al banco","all'etto (100 g)",0.100,1.09,16,V,"Sconto soci del 15%: senza tessera 1,29 all'etto, cioè 12,90 al kg. Il volantino stampa 10,90 al kg."),
 ("Formaggio","Ipercoop","ipercoop24","Freschi","Asiago D.O.P. Cheestà, circa 350 g, al banco","all'etto (100 g)",0.100,1.50,16,V,"Sconto del 20%: prima 1,89 all'etto, cioè 18,90 al kg. Il volantino stampa 15,00 al kg."),
 ("Formaggio","Ipercoop","ipercoop24","Freschi","Brie Paysan Breton, al banco","all'etto (100 g)",0.100,0.99,16,V,"Bollino «Conviene». Il volantino stampa 9,90 al kg."),
 ("Formaggio","Ipercoop","ipercoop24","Freschi","Camoscio d'Oro, al banco","all'etto (100 g)",0.100,1.29,16,V,"Bollino «Conviene». È il banco taglio: la confezione da 200 g è a 2,29 (11,45 al kg). Il volantino stampa 12,90 al kg."),
 ("Formaggio","Ipercoop","ipercoop24","Freschi","Formaggio La Scimuda, al banco","all'etto (100 g)",0.100,1.19,16,V,"Bollino «Conviene». Il volantino stampa 11,90 al kg."),
 # --- pagina 17 (ortofrutta) ---
 ("Verdura","Ipercoop","ipercoop24","Ortofrutta","Pomodoro rosso a grappolo","al kg",1,2.48,17,V,"Bollino «Conviene»."),
 ("Verdura","Ipercoop","ipercoop24","Ortofrutta","Zucca tonda Orto Qui","al kg",1,1.28,17,V,"Bollino «Conviene»."),
 ("Frutta","Ipercoop","ipercoop24","Ortofrutta","Mele SweeTango – Fior Fiore","850 g",0.850,1.78,17,V,"Con meno del 70% di residui di pesticidi rispetto ai limiti di legge. Il volantino stampa 2,09 al kg."),
 ("Frutta","Ipercoop","ipercoop24","Ortofrutta","Pere Santa Maria","al kg",1,2.28,17,V,"Bollino «Conviene»."),
 # --- pagina 18 («Tour tra i sapori», Toscana e Lazio) ---
 ("Formaggio","Ipercoop","ipercoop24","Freschi","Pecorino Toscano D.O.P. – Fior Fiore, al banco","all'etto (100 g)",0.100,1.90,18,V,"Sconto soci del 20%: senza tessera 2,39 all'etto, cioè 23,90 al kg. Il volantino stampa 19,00 al kg."),
 ("Vino","Ipercoop","ipercoop24","Bevande","Chianti D.O.C.G. Leonardo","750 ml",0.750,3.87,18,V,"Sconto del 40%: prima 6,45, cioè 8,60 al litro. Il volantino stampa 5,16 al litro."),
 ("Salsiccia","Ipercoop","ipercoop24","Salumi","Salsiccia lucanica dolce o piccante","90 g",0.090,2.15,18,V,"Sconto soci del 20%: senza tessera 2,69, cioè 29,89 al kg. È salsiccia stagionata da affettare, non da cuocere. Il volantino stampa 23,89 al kg."),
 ("Prosciutto","Ipercoop","ipercoop24","Salumi","Prosciutto Toscano D.O.P., stagionatura 16 mesi","100 g",0.100,3.49,18,V,"Sconto del 30%: prima 4,99, cioè 49,90 al kg. Il volantino stampa 34,90 al kg."),
 ("Biscotti","Ipercoop","ipercoop24","Colazione","Biscotti Artebianca, tipi vari","400 g",0.400,2.29,18,V,"Solo per i soci Coop. Il volantino stampa 5,73 al kg."),
 ("Vino","Ipercoop","ipercoop24","Bevande","Chianti Rosé Loggia del Sole","750 ml",0.750,2.95,18,V,"Sconto del 50%: prima 5,90, cioè 7,87 al litro. Il volantino stampa 3,93 al litro."),
 ("Vino","Ipercoop","ipercoop24","Bevande","Montepulciano D.O.C. Vecchia Cantina","750 ml",0.750,3.95,18,V,"Sconto del 40%: prima 6,59, cioè 8,79 al litro. Il volantino stampa 5,27 al litro."),
 ("Vino","Ipercoop","ipercoop24","Bevande","Vermentino I.G.T. Toscana Calaforte Frescobaldi","750 ml",0.750,5.99,18,V,"Sconto del 25%: prima 7,99, cioè 10,66 al litro. Il volantino stampa 7,99 al litro."),
 ("Pane","Ipercoop","ipercoop24","Panetteria","Pinsa romana Di Marco, multicereali","230 g",0.230,1.95,18,V,"Bollino «Conviene». Il volantino stampa 8,48 al kg."),
 ("Formaggio","Ipercoop","ipercoop24","Freschi","Caciotta di Amatrice, al banco","all'etto (100 g)",0.100,1.75,18,V,"Bollino «Conviene». Il volantino stampa 17,50 al kg."),
 ("Merluzzo","Ipercoop","ipercoop24","Pescheria","Filetto di baccalà bagnato","al kg",1,19.42,18,V,"Sconto soci del 25%: senza tessera 25,90 al kg. È già bagnato, pronto da cucinare."),
 # --- pagina 19 («Tour tra i sapori», Marche e Puglia) ---
 ("Prosciutto","Ipercoop","ipercoop24","Salumi","Prosciutto di Carpegna D.O.P. Beretta, stagionatura 20 mesi","85 g",0.085,3.59,19,V,"Sconto del 40%: prima 5,99, cioè 70,47 al kg. Il volantino stampa 42,24 al kg."),
 ("Mozzarella","Ipercoop","ipercoop24","Freschi","Mozzarella Gioiella, 100% latte italiano","500 g",0.500,3.99,19,V,"Sconto del 30%: prima 5,79, cioè 11,58 al kg. Il volantino stampa 7,98 al kg."),
 ("Suino","Ipercoop","ipercoop24","Macelleria","Linea Bombette pugliesi Zì Marì","280 g",0.280,4.49,19,V,"Bollino «Conviene». Sono involtini di suino da cuocere. Il volantino stampa 16,04 al kg."),
 ("Pasta","Ipercoop","ipercoop24","Dispensa","Pasta di semola Casa Milo, formati vari","500 g",0.500,0.98,19,V,"Sconto del 30%: prima 1,40, cioè 2,80 al kg. Il volantino stampa 1,96 al kg."),
 ("Pane","Ipercoop","ipercoop24","Panetteria","Puccia salentina","230 g",0.230,1.10,19,V,"Bollino «Conviene». Il volantino stampa 4,78 al kg."),
 ("Vino","Ipercoop","ipercoop24","Bevande","Negroamaro Rosato I.G.T. Marmorelle","750 ml",0.750,5.25,19,V,"Sconto soci del 40%: senza tessera 8,75, cioè 11,67 al litro. Il volantino stampa 7,00 al litro."),
 # --- pagina 20 («Tour tra i sapori», Campania e Molise) ---
 ("Pasta","Ipercoop","ipercoop24","Freschi","Ravioli ripieni Gusto e Benessere Casa Buratti, gusti vari","250 g",0.250,1.99,20,V,"Solo per i soci Coop. È pasta fresca ripiena. Il volantino stampa 7,96 al kg."),
 ("Pasta","Ipercoop","ipercoop24","Freschi","Ravioli ripieni Casa Buratti, gusti vari","250 g",0.250,2.27,20,V,"Sconto del 30%: prima 3,25, cioè 13,00 al kg. È pasta fresca ripiena. Il volantino stampa 9,08 al kg."),
 ("Pomodoro","Ipercoop","ipercoop24","Dispensa","Polpa di pomodoro bio Masseria Mosti, bottiglia","500 g",0.500,1.88,20,V,"Sconto del 30%: prima 2,69, cioè 5,38 al kg. Il volantino stampa 3,76 al kg."),
 ("Pomodoro","Ipercoop","ipercoop24","Dispensa","Passata di pomodoro bio Masseria Mosti, bottiglia","680 g",0.680,1.88,20,V,"Sconto del 30%: prima 2,69, cioè 3,96 al kg. Il volantino stampa 2,76 al kg."),
 ("Formaggio","Ipercoop","ipercoop24","Freschi","Scamorza bianca o affumicata, circa 340 g, al banco","all'etto (100 g)",0.100,1.29,20,V,"Bollino «Conviene». Il volantino stampa 12,90 al kg."),
 ("Formaggio","Ipercoop","ipercoop24","Freschi","Caciocavallo Silano D.O.P., al banco","all'etto (100 g)",0.100,1.69,20,V,"Bollino «Conviene». Il volantino stampa 16,90 al kg."),
 # --- pagina 21 («Tour tra i sapori», Campania, Basilicata, Calabria) ---
 ("Mozzarella","Ipercoop","ipercoop24","Freschi","Mozzarella di bufala campana D.O.P.","500 g",0.500,5.99,21,V,"Bollino «Conviene». Il volantino stampa 11,98 al kg."),
 ("Mozzarella","Ipercoop","ipercoop24","Freschi","Burrata di bufala Garofalo","125 g",0.125,1.49,21,V,"Bollino «Conviene». È burrata, non mozzarella. Il volantino stampa 11,92 al kg."),
 ("Salame","Ipercoop","ipercoop24","Salumi","Salame Napoli, al banco","all'etto (100 g)",0.100,1.29,21,V,"Bollino «Conviene». Il volantino stampa 12,90 al kg."),
 ("Mozzarella","Ipercoop","ipercoop24","Freschi","Mozzarella di bufala campana D.O.P. Sorì","300 g (3 × 100 g)",0.300,3.49,21,V,"Bollino «Conviene». Il volantino stampa 11,63 al kg."),
 ("Merendine","Ipercoop","ipercoop24","Panetteria","Sfogliatella riccia","54 g",0.054,0.45,21,V,"Bollino «Conviene». Il volantino stampa 8,33 al kg."),
 ("Frutta","Ipercoop","ipercoop24","Ortofrutta","Mele Melannurca campana I.G.P.","al kg",1,2.48,21,V,"Bollino «Conviene»."),
 ("Prosciutto","Ipercoop","ipercoop24","Salumi","Filetto lucano Lucana Salumi","80 g",0.080,2.15,21,V,"Sconto del 20%: prima 2,69, cioè 33,63 al kg. È lonza di suino stagionata. Il volantino stampa 26,88 al kg."),
 ("Prosciutto","Ipercoop","ipercoop24","Salumi","Capocollo di Calabria, al banco","all'etto (100 g)",0.100,2.19,21,V,"Bollino «Conviene». È capocollo, non prosciutto. Il volantino stampa 21,90 al kg."),
 ("Salame","Ipercoop","ipercoop24","Salumi","'Nduja calabrese piccante Madeo, in sac à poche","200 g",0.200,4.63,21,V,"Sconto del 20%: prima 5,79, cioè 28,95 al kg. È salame spalmabile piccante. Il volantino stampa 23,15 al kg."),
 # --- pagina 22 (igiene) ---
 ("Dentifricio","Ipercoop","ipercoop24","Igiene","Dentifricio Aquafresh tripla protezione","450 ml (6 × 75 ml)",0.450,4.79,22,V,"Bollino «Conviene». Il volantino stampa 10,64 al litro."),
 ("Bagnoschiuma","Ipercoop","ipercoop24","Igiene","Bagnoschiuma o sapone liquido Mil Mil, ecoricarica","2 litri",2,2.49,22,V,"Bollino «Conviene». È la ricarica, non il flacone. Il volantino stampa 1,25 al litro."),
 ("Bagnoschiuma","Ipercoop","ipercoop24","Igiene","Bagnodoccia Neutro Roberts, varie profumazioni","450 ml",0.450,1.69,22,V,"Bollino «Conviene». Il volantino stampa 3,76 al litro."),
 ("Shampoo","Ipercoop","ipercoop24","Igiene","Shampoo antiforfora Clear","225 ml",0.225,1.99,22,V,"Bollino «Conviene». Il volantino stampa 8,84 al litro."),
 ("Dentifricio","Ipercoop","ipercoop24","Igiene","Dentifricio protezione carie Coop","125 ml",0.125,0.99,22,V,"Il volantino stampa 7,92 al litro."),
 # --- pagina 23 (igiene) ---
 ("Bagnoschiuma","Ipercoop","ipercoop24","Igiene","Sapone liquido Vidal, ecoricarica, profumazioni varie","1,2 litri",1.2,1.79,23,V,"Bollino «Conviene». È la ricarica, non il flacone. Il volantino stampa 1,49 al litro."),
 # --- pagina 24 (carta) ---
 ("Carta igienica","Ipercoop","ipercoop24","Casa","Carta igienica Maxi Comfort Tempo, 2 veli","12 maxi rotoli",12,6.59,24,V,"Sconto del 40%: prima 10,99. Sono maxi rotoli, più lunghi dei normali."),
 ("Carta igienica","Ipercoop","ipercoop24","Casa","Carta igienica Cartacamomilla Regina, 3 veli, 300 strappi","6 rotoli",6,3.99,24,V,"Solo per i soci Coop."),
 ("Asciugatutto","Ipercoop","ipercoop24","Casa","Carta casa Limone Nicky, 2 veli, 100 strappi","6 rotoli",6,5.99,24,V,"Bollino «Conviene»."),
 ("Asciugatutto","Ipercoop","ipercoop24","Casa","Asciugatutto Tuttofare Scottex, double face decorato","6 rotoli",6,6.19,24,V,"Bollino «Conviene»."),
 # --- pagina 25 (cura casa) ---
 ("Lavastoviglie","Ipercoop","ipercoop24","Cura casa","Detersivo per lavastoviglie gel All in One Pril, limone","1,872 litri, 2 × 52 lavaggi",104,9.95,25,V,"Bollino «Conviene». Il volantino stampa 5,32 al litro."),
 ("Lavastoviglie","Ipercoop","ipercoop24","Cura casa","Detersivo per lavastoviglie 5 in 1 Pril, caps","1,004 kg, 54 lavaggi",54,10.90,25,V,"Solo per i soci Coop. Il volantino stampa 10,86 al kg."),
 ("Lavatrice","Ipercoop","ipercoop24","Cura casa","Detersivo per lavatrice liquido concentrato Dash Pods","1,086 kg, 60 lavaggi",60,13.65,25,V,"Sconto del 40%: prima 22,75, cioè 20,95 al kg. Offerta limitata. Il volantino stampa 12,57 al kg."),
 ("Lavatrice","Ipercoop","ipercoop24","Cura casa","Detersivo per lavatrice in polvere Dash+ Power","4,15 kg, 83 misurini",83,16.74,25,V,"Sconto del 50%: prima 33,48, cioè 8,07 al kg. Offerta limitata. Il volantino stampa 4,03 al kg."),
 ("Lavatrice","Ipercoop","ipercoop24","Cura casa","Detersivo per lavatrice Coccolino, tipi vari","2 × 1,48 litri, 74 lavaggi",74,11.90,25,V,"Bollino «Conviene». Il volantino stampa 4,02 al litro."),
 # --- pagina 28 (fai da te) ---
 ("Asciugatutto","Ipercoop","ipercoop24","Casa","Rotolone carta Birillo, 500 strappi","1 rotolone",1,3.60,28,V,"Sconto del 20%: prima 4,50. È un rotolone da 500 strappi, cioè quanto cinque rotoli normali: il prezzo al rotolo non si confronta con le confezioni da sei."),
 # --- pagina 43 (bibite) ---
 ("Bibite","Ipercoop","ipercoop24","Bevande","Coca Cola original o zero","6 litri (4 × 1,5 l)",6,4.99,43,V,"Solo per i soci Coop. Il volantino stampa 0,83 al litro."),
 ("Bibite","Ipercoop","ipercoop24","Bevande","Kinley tonic water, gusti vari","1 litro",1,0.89,43,V,"Solo per i soci Coop."),
 ("Bibite","Ipercoop","ipercoop24","Bevande","Fuze Tea, gusti vari, con o senza zucchero","1,25 litri",1.25,1.05,43,V,"Solo per i soci Coop. Il volantino stampa 0,84 al litro."),
 ("Bibite","Ipercoop","ipercoop24","Bevande","Fuze Tea mini, limone o pesca","1 litro (4 × 250 ml)",1,1.99,43,V,"Solo per i soci Coop."),
 ("Bibite","Ipercoop","ipercoop24","Bevande","Powerade, gusti vari","500 ml",0.500,0.89,43,V,"Solo per i soci Coop. Il volantino stampa 1,78 al litro."),
 # --- pagina 44 (pubblicità Bellery) ---
 ("Shampoo","Ipercoop","ipercoop24","Igiene","Shampoo secco Bellery, tipi vari","200 ml",0.200,3.79,44,V,"Sconto soci del 20%: senza tessera 4,74, cioè 23,70 al litro. È uno shampoo secco spray, si usa a spruzzi fra un lavaggio e l'altro: al litro costa molto più di uno shampoo normale. Il volantino stampa 18,95 al litro."),
 # PAM «Tante offerte a 1, 2, 3 euro», dal 24 settembre al 7 ottobre (pam24).
 # Letto per intero il 2026-09-22. «Con APP» vuol dire che il prezzo vale solo
 # con l'app Pam Perte Plus: il volantino non stampa quanto costa senza.
 ("Pomodoro","Pam","pam24","Dispensa","Passata di pomodoro Mutti","700 g",0.700,1.00,1,V,"Il volantino stampa 1,43 al kg."),
 ("Pizza","Pam","pam24","Surgelati","Pizza Ristorante Cameo, gusti e formati vari","320 g (al salame)",0.320,2.00,1,V,"Solo con l'app Pam Perte Plus. Il volantino non stampa il peso: il conto è sul formato al salame da 320 g. I gusti più leggeri al chilo costano di più."),
 ("Vino","Pam","pam24","Bevande","Prosecco DOC extra dry Le Calleselle","750 ml",0.750,3.00,1,V,"Il volantino stampa 4,00 al litro."),
 ("Yogurt","Pam","pam24","Freschi","Yogurt cremoso intero Vipiteno, gusti vari","500 g",0.500,1.00,2,V,"Il volantino stampa 2,00 al kg."),
 ("Latte","Pam","pam24","Latteria","Latte UHT parzialmente scremato Arborea","1 litro",1,1.00,2,V,""),
 ("Ricotta","Pam","pam24","Freschi","Ricotta fresca Tesori dell'Arca","250 g",0.250,1.00,2,V,"Il volantino stampa 4,00 al kg."),
 ("Formaggio","Pam","pam24","Freschi","Stracchino cremoso Tesori dell'Arca","100 g",0.100,1.00,2,V,"Il volantino stampa 10,00 al kg."),
 ("Burro","Pam","pam24","Freschi","Burro senza lattosio Latteria Soresina","125 g",0.125,1.00,2,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 8,00 al kg."),
 ("Formaggio","Pam","pam24","Freschi","Fettine classiche Kraft","175 g",0.175,1.00,2,V,"Solo con l'app Pam Perte Plus. Sono formaggio fuso a fette. Il volantino stampa 5,71 al kg."),
 ("Sughi","Pam","pam24","Freschi","Pesto fresco alla genovese «Viva la Mamma» Beretta, con o senza aglio","90 g",0.090,1.00,2,V,"Il volantino stampa 11,11 al kg."),
 ("Verdure surgelate","Pam","pam24","Surgelati","Taccole o fagiolini e patate «Natura in padella» Bonduelle","450 g",0.450,1.00,2,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 2,22 al kg."),
 ("Biscotti","Pam","pam24","Colazione","Biscotti Divella: grottoli con gocce di cioccolato, ottimini integrali, grano saraceno","350 g",0.350,1.00,3,V,"Formati da 350 o 400 g allo stesso prezzo: il conto è sul più piccolo (2,86 al kg)."),
 ("Biscotti","Pam","pam24","Colazione","Biscotti Digestive classici Gullón","400 g",0.400,1.00,3,V,"Il volantino stampa 2,50 al kg."),
 ("Biscotti","Pam","pam24","Colazione","Frollini latte e miele Pam","380 g",0.380,1.00,3,V,"Il volantino stampa 2,63 al kg."),
 ("Merendine","Pam","pam24","Colazione","Croissant classico Bauli, 5 pezzi","200 g",0.200,1.00,3,V,"Il volantino stampa 5,00 al kg."),
 ("Biscotti","Pam","pam24","Colazione","Ringo tubo Pavesi, vaniglia o cacao","165 g",0.165,1.00,3,V,"Il volantino stampa 6,06 al kg."),
 ("Biscotti","Pam","pam24","Colazione","Biscotti «Cookies» Griesson, assortiti","150 g",0.150,1.00,3,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 6,67 al kg."),
 ("Pane","Pam","pam24","Dispensa","Tuc Saiwa","150 g (2 × 75 g)",0.150,1.00,3,V,"Il volantino stampa 6,67 al kg."),
 ("Riso","Pam","pam24","Dispensa","Riso «Rapid» Pam, tipi vari","250 g",0.250,1.00,3,V,"Riso a cottura rapida (basmati, nero integrale...). Il volantino stampa 4,00 al kg."),
 ("Sughi","Pam","pam24","Dispensa","Sughi pronti Pam, assortiti (amatriciana, ragù alla bolognese...)","200 g",0.200,1.00,3,V,"Formati da 200 o 350 g allo stesso prezzo: il conto è sul più piccolo (5,00 al kg)."),
 ("Pane","Pam","pam24","Dispensa","Sfoglie Pam, alle olive o classiche","150 g",0.150,1.00,3,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 6,67 al kg."),
 ("Pane","Pam","pam24","Panetteria","Pane a fette integrale Pam","400 g",0.400,1.00,3,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 2,50 al kg."),
 ("Birra","Pam","pam24","Bevande","Birra non filtrata Ichnusa, lattina","440 ml",0.440,1.00,4,V,"Il volantino stampa 2,27 al litro."),
 ("Birra","Pam","pam24","Bevande","Birra Peroni","660 ml",0.660,1.00,4,V,"Il volantino stampa 1,51 al litro."),
 ("Bibite","Pam","pam24","Bevande","Energy drink Red Bull, gusti vari","250 ml",0.250,1.00,4,V,"Il volantino stampa 4,00 al litro."),
 ("Bibite","Pam","pam24","Bevande","«Succoso» Zero San Benedetto, gusti vari","900 ml",0.900,1.00,4,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 1,11 al litro."),
 ("Vino","Pam","pam24","Bevande","Vino in brik Pam, bianco, rosso o rosato","1 litro",1,1.00,4,V,"Solo con l'app Pam Perte Plus."),
 ("Bagnoschiuma","Pam","pam24","Igiene","Bagnoschiuma Neutroderma, assortito","500 ml",0.500,1.00,4,V,""),
 ("Bagnoschiuma","Pam","pam24","Igiene","Docciaschiuma Vidal","250 ml",0.250,1.00,4,V,""),
 ("Carta igienica","Pam","pam24","Cura casa","Carta igienica Arkalia, 2 veli","4 rotoli",4,1.00,4,V,""),
 ("Dentifricio","Pam","pam24","Igiene","Dentifricio AZ, assortito","65 ml",0.065,1.00,4,V,"Solo con l'app Pam Perte Plus."),
 ("Cereali","Pam","pam24","Colazione","Muesli Pam, gusti vari","375 g",0.375,2.00,5,V,"Il volantino stampa 5,33 al kg."),
 ("Merendine","Pam","pam24","Colazione","Pan Goccioli Mulino Bianco","336 g",0.336,2.00,5,V,"Il volantino stampa 5,95 al kg."),
 ("Marmellata","Pam","pam24","Colazione","Confettura extra Zuegg, gusti vari","320 g",0.320,2.00,5,V,"Formati da 320 o 330 g allo stesso prezzo: il conto è sul più piccolo (6,25 al kg)."),
 ("Uova","Pam","pam24","Freschi","Uova da galline allevate a terra Semplici e Buoni","6 uova",6,2.00,5,V,"Da allevamento senza uso di antibiotici."),
 ("Spalmabili","Pam","pam24","Freschi","Robiola Osella","200 g (2 × 100 g)",0.200,2.00,5,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 10,00 al kg."),
 ("Farina","Pam","pam24","Dispensa","Farina di avena integrale macinata a pietra Almaverde Bio","500 g",0.500,2.00,5,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 4,00 al kg."),
 ("Frutta","Pam","pam24","Surgelati","Frutti di bosco surgelati Tesori dell'Arca","300 g",0.300,2.00,5,V,"Surgelati, non freschi. Il volantino stampa 6,67 al kg."),
 ("Pollo","Pam","pam24","Freschi","Nuggets di pollo «Panatine» Rovagnati","144 g",0.144,2.00,5,V,"Il volantino stampa 13,89 al kg."),
 ("Verdure surgelate","Pam","pam24","Surgelati","Spinaci in foglia a cubetti Pam","1 kg",1,2.00,5,V,""),
 ("Pane","Pam","pam24","Dispensa","Gallette proteiche Fiorentini","120 g",0.120,2.00,6,V,"Il volantino stampa 16,67 al kg."),
 ("Conserve","Pam","pam24","Dispensa","Cetrioli Gurken in agrodolce Tesori dell'Arca","360 g (sgocc.)",0.360,2.00,6,V,"Solo con l'app Pam Perte Plus. Vasetto da 670 g, 360 sgocciolati: il conto è sullo sgocciolato, come fa il volantino (5,55 al kg)."),
 ("Bibite","Pam","pam24","Bevande","Succo di frutta «Optimum» Yoga, gusti vari","1,2 litri (6 × 200 ml)",1.2,2.00,6,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 1,67 al litro."),
 ("Acqua","Pam","pam24","Bevande","Acqua naturale Ecogreen San Benedetto, fardello","12 litri (6 × 2 litri)",12,2.00,6,V,"Il prezzo è a fardello: 0,33 a bottiglia. Il volantino stampa 0,16 al litro."),
 ("Asciugatutto","Pam","pam24","Cura casa","Asciugatutto Fiocco, 3 veli, 75 strappi","3 maxi rotoli",3,2.00,6,V,""),
 ("Biscotti","Pam","pam24","Colazione","Biscotti «Oro» Saiwa, confezione da un chilo","1 kg",1,3.00,7,V,""),
 ("Pane","Pam","pam24","Dispensa","Bibanesi gli originali con olio extra vergine di oliva","400 g",0.400,3.00,7,V,"Il volantino stampa 7,50 al kg."),
 ("Conserve","Pam","pam24","Dispensa","Filetti di sgombro in olio di girasole Pam, vaso di vetro","250 g",0.250,3.00,7,V,"Il conto è sul peso del vaso, come fa il volantino (12,00 al kg): il peso sgocciolato non è stampato."),
 ("Mozzarella","Pam","pam24","Freschi","Mozzarella fiordilatte Tesori dell'Arca","375 g (3 × 125 g)",0.375,3.00,7,V,"Il volantino stampa 8,00 al kg."),
 ("Merluzzo","Pam","pam24","Surgelati","2 Croccole di merluzzo Findus, le originali o agli spinaci","200 g (agli spinaci)",0.200,3.00,7,V,"Formati da 216 g (originali) o 200 g (agli spinaci) allo stesso prezzo: il conto è sul più piccolo (15,00 al kg)."),
 ("Pancetta","Pam","pam24","Salumi","Pancetta a cubetti Negroni, dolce o affumicata","300 g (4 × 75 g)",0.300,3.00,7,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 10,00 al kg."),
 ("Vino","Pam","pam24","Bevande","Vini Crifo: Nero di Troia Puglia IGP, Malvasia bianca o rosato Castel del Monte DOP","750 ml",0.750,3.00,7,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 4,00 al litro."),
 ("Frutta","Pam","pam24","Ortofrutta","Banane sfuse","al kg",1,0.99,8,V,"«Prezzi bassi sempre»."),
 ("Frutta","Pam","pam24","Ortofrutta","Mele Gala, sacco da 1,5 kg","1,5 kg",1.5,1.49,8,V,"«Prezzi bassi sempre». Il volantino stampa 0,99 al kg."),
 ("Verdura","Pam","pam24","Ortofrutta","Cetrioli lunghi","350 g",0.350,0.99,8,V,"«Prezzi bassi sempre». Il volantino stampa 2,83 al kg."),
 ("Verdura","Pam","pam24","Ortofrutta","Zucca Butternut","al kg",1,0.99,8,V,"«Prezzi bassi sempre»."),
 ("Frutta","Pam","pam24","Ortofrutta","Arance, rete da 1,5 kg","1,5 kg",1.5,1.99,8,V,"Il volantino stampa 1,33 al kg."),
 ("Formaggio","Pam","pam24","Gastronomia","Formaggio fresco primo sale","all'etto",0.1,0.99,9,V,"Al banco. «Prezzi bassi sempre»."),
 ("Formaggio","Pam","pam24","Gastronomia","Gorgonzola DOP dolce Tesori dell'Arca","all'etto",0.1,0.99,9,V,"Al banco. «Prezzi bassi sempre»."),
 ("Formaggio","Pam","pam24","Gastronomia","Emmental","all'etto",0.1,0.99,9,V,"Al banco. «Prezzi bassi sempre»."),
 ("Tacchino","Pam","pam24","Gastronomia","Fesa di tacchino arrosto","all'etto",0.1,1.49,9,V,"Al banco. Prima 1,89."),
 ("Prosciutto","Pam","pam24","Gastronomia","Prosciutto cotto «Granbiscotto» Rovagnati","all'etto",0.1,2.59,9,V,"Al banco. Prima 3,19."),
 ("Prosciutto","Pam","pam24","Gastronomia","Prosciutto di Parma DOP stagionato 18 mesi","all'etto",0.1,2.79,9,V,"Al banco. Prima 3,59."),
 ("Bresaola","Pam","pam24","Gastronomia","Bresaola della Valtellina IGP","all'etto",0.1,3.49,9,V,"Al banco."),
 ("Grana","Pam","pam24","Gastronomia","Parmigiano Reggiano DOP 24 mesi, pezzi da un chilo circa","all'etto",0.1,1.99,9,V,"Al banco."),
 ("Suino","Pam","pam24","Macelleria","Filetto di suino","all'etto",0.1,0.99,10,V,"«Prezzi bassi sempre»: 9,90 al kg."),
 ("Pollo","Pam","pam24","Macelleria","Petto di pollo a fette AIA, vaschetta da 700 g circa","all'etto",0.1,0.99,10,V,"«Prezzi bassi sempre»: 9,90 al kg."),
 ("Manzo","Pam","pam24","Macelleria","Macinato sceltissimo di bovino adulto, vaschetta da 400 g circa","all'etto",0.1,1.29,10,V,"12,90 al kg."),
 ("Suino","Pam","pam24","Macelleria","Lonza di suino, trancio da un chilo circa","all'etto",0.1,0.69,10,V,"Confezione risparmio: 6,90 al kg. Prima 0,86 all'etto."),
 ("Manzo","Pam","pam24","Macelleria","Maxi hamburger di scottona skin Tesori dell'Arca","200 g",0.200,3.90,10,V,"Il volantino stampa 19,50 al kg."),
 ("Pollo","Pam","pam24","Macelleria","Bastoncini di pollo Valserena","500 g",0.500,3.69,10,V,"Il volantino stampa 7,38 al kg."),
 ("Pollo","Pam","pam24","Macelleria","Gran Dorate alla viennese AIA","300 g",0.300,3.59,10,V,"Cotolette di pollo impanate. Il volantino stampa 11,97 al kg."),
 ("Pesce","Pam","pam24","Pescheria","Trota salmonata Tesori dell'Arca","all'etto",0.1,0.99,11,V,"Vale solo dal 24 al 30 settembre, non per tutto il volantino. 9,90 al kg. Pesce allevato in Italia.","2026-09-24","2026-09-30"),
 ("Pesce","Pam","pam24","Pescheria","Ricciola","all'etto",0.1,1.99,11,V,"Vale solo dal 24 al 30 settembre, non per tutto il volantino.","2026-09-24","2026-09-30"),
 ("Pesce","Pam","pam24","Pescheria","Lupini","all'etto",0.1,0.69,11,V,"Vale solo dal 24 al 30 settembre, non per tutto il volantino. Molluschi italiani.","2026-09-24","2026-09-30"),
 ("Gamberi","Pam","pam24","Pescheria","Code di mazzancolle Tesori dell'Arca, pronte da cuocere","250 g",0.250,8.90,11,V,"Vale solo dal 24 al 30 settembre, non per tutto il volantino. Il volantino stampa 35,60 al kg.","2026-09-24","2026-09-30"),
 ("Gamberi","Pam","pam24","Pescheria","Mazzancolle tropicali intere precotte","all'etto",0.1,0.99,11,V,"Vale solo dall'1 al 7 ottobre, non per tutto il volantino. 9,90 al kg. Sono intere, con la testa.","2026-10-01","2026-10-07"),
 ("Pesce","Pam","pam24","Pescheria","Branzino Tesori dell'Arca, allevato nel golfo di Gaeta o di Follonica","all'etto",0.1,1.39,11,V,"Vale solo dall'1 al 7 ottobre, non per tutto il volantino.","2026-10-01","2026-10-07"),
 ("Merluzzo","Pam","pam24","Pescheria","Cuore di merluzzo","all'etto",0.1,2.29,11,V,"Vale solo dall'1 al 7 ottobre, non per tutto il volantino.","2026-10-01","2026-10-07"),
 ("Salmone","Pam","pam24","Pescheria","Saku di salmone Gimar, per sushi e sashimi","140 g",0.140,7.90,11,V,"Vale solo dall'1 al 7 ottobre, non per tutto il volantino. Il volantino stampa 56,43 al kg.","2026-10-01","2026-10-07"),
 ("Caffè","Pam","pam24","Colazione","Caffè macinato «Intermezzo» Segafredo","500 g (2 × 250 g)",0.500,4.99,12,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 9,98 al kg."),
 ("Caffè","Pam","pam24","Colazione","Caffè in capsule Pam gran crema o espresso, compatibili Nescafé Dolce Gusto","40 capsule, 300 g",0.300,6.99,12,V,"0,18 a capsula. Il volantino stampa 23,30 al kg."),
 ("Biscotti","Pam","pam24","Colazione","Biscotti Fagottini o Saracene Balocco","700 g",0.700,2.69,12,V,"Il volantino stampa 3,84 al kg."),
 ("Biscotti","Pam","pam24","Colazione","Pavesini classici","200 g",0.200,1.99,12,V,"Il volantino stampa 9,95 al kg."),
 ("Pane","Pam","pam24","Panetteria","Panini per hamburger, maxi hamburger o hot dog Pam","250 g",0.250,0.89,12,V,"Formati da 250 o 300 g allo stesso prezzo: il conto è sul più piccolo (3,56 al kg)."),
 ("Riso","Pam","pam24","Dispensa","Riso «Chicchiricchi» Gran Risparmio Gallo","850 g",0.850,1.49,12,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 1,75 al kg."),
 ("Pasta","Pam","pam24","Dispensa","Pasta di semola Barilla, formati classici","500 g",0.500,0.59,12,V,"Sconto del 40%: prima 0,99. Il volantino stampa 1,18 al kg."),
 ("Tonno","Pam","pam24","Dispensa","Filetti di tonno in olio di oliva Pam, vaso di vetro","130 g",0.130,2.00,12,V,"Solo con l'app Pam Perte Plus. Il conto è sul peso del vaso, come fa il volantino (15,38 al kg): il peso sgocciolato non è stampato, quindi al chilo di tonno costa di più."),
 ("Yogurt","Pam","pam24","Freschi","Yogurt cremoso Müller, gusti vari","250 g (2 × 125 g)",0.250,0.95,13,V,"Il volantino stampa 3,80 al kg."),
 ("Pasta","Pam","pam24","Freschi","Pasta fresca ripiena «Sfogliagrezza» Giovanni Rana, gusti vari","250 g",0.250,2.49,13,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 9,96 al kg."),
 ("Spalmabili","Pam","pam24","Freschi","Crescenza «Certosa» Galbani","165 g",0.165,1.49,13,V,"Il volantino stampa 9,03 al kg."),
 ("Pasta","Pam","pam24","Freschi","Lasagne all'uovo Tesori dell'Arca","250 g",0.250,1.29,13,V,"Il volantino stampa 5,16 al kg."),
 ("Prosciutto","Pam","pam24","Salumi","Prosciutto cotto o crudo affettato «I Firmati» Rovagnati","90 g",0.090,2.39,13,V,"Sconto del 40%: prima 3,99. Vaschette da 90 o 100 g allo stesso prezzo: il conto è sulla più piccola (26,55 al kg)."),
 ("Formaggio","Pam","pam24","Freschi","Fette Original Leerdammer, maxi formato","260 g",0.260,2.99,13,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 11,50 al kg."),
 ("Verdure surgelate","Pam","pam24","Surgelati","Minestrone Tradizione Findus","1 kg",1,2.99,15,V,""),
 ("Verdure surgelate","Pam","pam24","Surgelati","Contorno «Verdure tricolore» Orogel","450 g",0.450,1.69,15,V,"Il volantino stampa 3,76 al kg."),
 ("Vino","Pam","pam24","Bevande","Valpolicella Ripasso DOC La Poesia degli Alberi","750 ml",0.750,5.74,15,V,"Sconto del 25%: prima 7,65."),
 ("Merluzzo","Pam","pam24","Surgelati","Cuori di merluzzo sudafricano Pam","300 g",0.300,3.99,15,V,"Il volantino stampa 13,30 al kg."),
 ("Vino","Pam","pam24","Bevande","Vermentino Terre Siciliane IGT Colle del Sole","750 ml",0.750,1.99,15,V,"Il volantino stampa 2,65 al litro."),
 ("Bibite","Pam","pam24","Bevande","Coca-Cola regular o zero, bi-pack","3 litri (2 × 1,5 litri)",3,2.99,15,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 1,00 al litro."),
 ("Carta igienica","Pam","pam24","Cura casa","Carta igienica «Cartacamomilla» maxi Regina","6 rotoli maxi",6,4.49,16,V,"Solo con l'app Pam Perte Plus. Sulla confezione c'è scritto che 6 maxi valgono 12 rotoli normali: il conto è sui 6 rotoli veri."),
 ("Shampoo","Pam","pam24","Igiene","Shampoo o balsamo «Ultra Dolce» Garnier, assortito","200 ml",0.200,2.00,16,V,"Solo con l'app Pam Perte Plus. Flaconi da 200 o 250 ml allo stesso prezzo: il conto è sul più piccolo."),
 ("Ammorbidente","Pam","pam24","Cura casa","Ammorbidente concentrato Tesori d'Oriente","760 ml, 38 lavaggi",38,1.79,17,V,""),
 ("Lavatrice","Pam","pam24","Cura casa","Detersivo liquido per lavatrice Spuma di Sciampagna, Marsiglia o Fresco Puro","36 lavaggi",36,2.99,17,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 0,09 a lavaggio."),
 ("Lavastoviglie","Pam","pam24","Cura casa","Detersivo per lavastoviglie Pril, tabs o gel","24 tabs",24,3.99,17,V,"Stesso prezzo per le 24 tabs «Tutto in 1» o il gel da 30 lavaggi: il conto è sulle tabs, che sono di meno."),
 ("Cereali","Pam","pam24","Colazione","Cereali Choko Crock o Anellini al miele Pam","375 g",0.375,1.99,18,V,"Il volantino stampa 5,31 al kg."),
 ("Biscotti","Pam","pam24","Colazione","Wafer Pam, assortiti","175 g",0.175,0.99,18,V,"Il volantino stampa 5,66 al kg."),
 ("Tonno","Pam","pam24","Dispensa","Tonno pinne gialle all'olio di oliva Pam","560 g (8 × 70 g)",0.560,5.99,18,V,"0,75 a lattina. Il conto è sul peso delle scatolette, come fa il volantino (10,70 al kg): sgocciolato il tonno è meno, quindi al chilo costa di più."),
 ("Conserve","Pam","pam24","Dispensa","Funghi trifolati sottolio Pam","185 g",0.185,1.00,18,V,"Il volantino stampa 5,40 al kg."),
 ("Bibite","Pam","pam24","Bevande","Nettari di frutta Pam, gusti vari","1 litro",1,1.19,18,V,""),
 ("Salmone","Pam","pam24","Freschi","Salmone affumicato norvegese Pam","150 g",0.150,4.50,18,V,"Il volantino stampa 30,00 al kg."),
 ("Pane","Pam","pam24","Panetteria","Piadina integrale Pam","300 g",0.300,1.59,18,V,"Il volantino stampa 5,30 al kg."),
 ("Pizza","Pam","pam24","Surgelati","4 mini pizze margherita Pam","320 g (4 × 80 g)",0.320,2.39,19,V,"Il volantino stampa 7,47 al kg."),
 ("Pollo","Pam","pam24","Surgelati","Nuggets di pollo Pam","300 g",0.300,2.69,19,V,"Il volantino stampa 8,97 al kg."),
 ("Verdure surgelate","Pam","pam24","Surgelati","Piselli finissimi Pam","450 g",0.450,1.29,19,V,"Il volantino stampa 2,87 al kg."),
 ("Salame","Pam","pam24","Salumi","Salame Milano o ungherese affettato Pam","110 g",0.110,1.69,19,V,"Il volantino stampa 15,36 al kg."),
 ("Grana","Pam","pam24","Freschi","Parmigiano Reggiano DOP grattugiato Pam","100 g",0.100,2.29,19,V,"Il volantino stampa 22,90 al kg."),
 ("Mozzarella","Pam","pam24","Freschi","Ciliegine di mozzarella Pam","150 g",0.150,1.49,19,V,"Il volantino stampa 9,93 al kg."),
 ("Bagnoschiuma","Pam","pam24","Igiene","Sapone liquido Arkalia, assortito","500 ml",0.500,1.29,19,V,""),
 ("Asciugatutto","Pam","pam24","Cura casa","Asciugatutto Arkalia decorato, 3 veli","2 rotoli",2,1.49,19,V,""),
 ("Yogurt","Pam","pam24","Freschi","Yogurt greco bianco 0% senza lattosio +a-","500 g",0.500,2.59,20,V,"Linea nuova di Pam. Il volantino stampa 5,18 al kg."),
 ("Yogurt","Pam","pam24","Freschi","Yogurt greco +a-, gusti vari","150 g",0.150,0.89,20,V,"Linea nuova di Pam. Il volantino stampa 5,93 al kg."),
 ("Yogurt","Pam","pam24","Freschi","Kefir multifrutti senza lattosio +a-","480 g",0.480,1.19,20,V,"È kefir, latte fermentato da bere. Il volantino stampa 2,48 al kg."),
 ("Yogurt","Pam","pam24","Freschi","Kefir bianco senza lattosio +a-","480 g",0.480,0.99,20,V,"È kefir, latte fermentato da bere. Il volantino stampa 2,06 al kg."),
 # PAM «Occasioni Extra», dal 24 settembre al 7 ottobre (pamextra24): l'altro
 # volantino dello stesso periodo, letto per intero il 2026-09-22.
 ("Pomodoro","Pam","pamextra24","Dispensa","Salsa di pomodoro ciliegino o datterino Tesori dell'Arca","330 g",0.330,1.00,1,V,"Il volantino stampa 3,03 al kg."),
 ("Caffè","Pam","pamextra24","Colazione","Caffè in capsule Starbucks, compatibili Nespresso, gusti vari","10 capsule, 55 g",0.055,3.00,2,V,"Confezioni da 55 o 57 g allo stesso prezzo: il conto è sulla più leggera (54,55 al kg)."),
 ("Caffè","Pam","pamextra24","Colazione","Caffè in grani Vivace Tradizionale Pellini, classico","1 kg",1,14.90,2,V,"Solo con l'app Pam Perte Plus."),
 ("Caffè","Pam","pamextra24","Colazione","Caffè in cialde Palombini, classico o decaffeinato","18 cialde, 126 g",0.126,3.00,2,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 23,81 al kg."),
 ("Tè","Pam","pamextra24","Colazione","Tè Ati classico, 25 filtri","38 g",0.038,1.39,2,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 36,58 al kg."),
 ("Tè","Pam","pamextra24","Colazione","Tisana Tesori dell'Arca, gusti vari, 20 filtri","36 g",0.036,1.89,2,V,"Il volantino stampa 52,50 al kg."),
 ("Biscotti","Pam","pamextra24","Colazione","Biscotti «Krumiri» Bistefani, classici o gocce di cioccolato","290 g",0.290,2.00,2,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 6,90 al kg."),
 ("Biscotti","Pam","pamextra24","Colazione","Frollini «Ancora uno» con cioccolato in pezzi Tre Marie","360 g",0.360,2.00,2,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 5,55 al kg."),
 ("Biscotti","Pam","pamextra24","Colazione","Biscotti Pan di Stelle, Abbracci o Nascondini Mulino Bianco","330 g",0.330,2.00,2,V,"Formati da 330 o 350 g allo stesso prezzo: il conto è sul più piccolo (6,06 al kg)."),
 ("Biscotti","Pam","pamextra24","Colazione","Biscotti «È il Novellino» Campiello, senza zuccheri aggiunti o senza latte e uova","350 g",0.350,1.00,2,V,"Il volantino stampa 2,86 al kg."),
 ("Cereali","Pam","pamextra24","Colazione","Cereali Nesquik Nestlé","375 g",0.375,2.49,3,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 6,64 al kg."),
 ("Biscotti","Pam","pamextra24","Colazione","Frollini Oro Saiwa, grano fondente o Cruscoro","300 g",0.300,1.99,3,V,"Solo con l'app Pam Perte Plus. Formati da 300 o 400 g allo stesso prezzo: il conto è sul più piccolo (6,63 al kg)."),
 ("Biscotti","Pam","pamextra24","Colazione","Bocconcini di sfoglia ripieni Millevoglie Matilde Vicenzi, assortiti","90 g",0.090,1.00,3,V,"Formati da 90 o 100 g allo stesso prezzo: il conto è sul più piccolo (11,11 al kg)."),
 ("Biscotti","Pam","pamextra24","Colazione","Wafer Loacker, vaniglia, napolitaner o cremkakao","175 g",0.175,1.69,3,V,"Il volantino stampa 9,66 al kg."),
 ("Merendine","Pam","pamextra24","Colazione","Croissant tradizionali o farciti Ore Liete","200 g",0.200,1.00,3,V,"Formati da 200 o 240 g allo stesso prezzo: il conto è sul più piccolo (5,00 al kg)."),
 ("Merendine","Pam","pamextra24","Colazione","Choco Brownie, Cookies o Chocowafer Milka","150 g",0.150,2.00,3,V,"Solo con l'app Pam Perte Plus. Formati da 150 a 184 g allo stesso prezzo: il conto è sul più piccolo (13,33 al kg)."),
 ("Merendine","Pam","pamextra24","Colazione","Torta Roll Midi, cacao o nocciola","250 g",0.250,1.00,3,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 4,00 al kg."),
 ("Cioccolato","Pam","pamextra24","Dispensa","Tavoletta di cioccolato Novi, al latte o fondente","100 g",0.100,1.69,3,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 16,90 al kg."),
 # Pagina 4: la confettura extra Zuegg (320/330 g a 2,00) è identica, stesso
 # prezzo, a quella di pam24 pagina 5: non riscritta, sarebbe una riga doppia.
 ("Creme","Pam","pamextra24","Colazione","Crema spalmabile CremaNovi 45% nocciole","350 g",0.350,6.79,4,V,"Il volantino stampa 19,40 al kg."),
 ("Creme","Pam","pamextra24","Colazione","Crema spalmabile bicolore Pam","400 g",0.400,2.00,4,V,"Il volantino stampa 5,00 al kg."),
 ("Miele","Pam","pamextra24","Colazione","Miele millefiori armonioso Pam, squeezer","250 g",0.250,2.00,4,V,"Il volantino stampa 8,00 al kg."),
 ("Farina","Pam","pamextra24","Dispensa","Farina d'America Manitoba tipo 0 Molino Spadoni","1 kg",1,1.49,5,V,""),
 ("Burro","Pam","pamextra24","Freschi","Burro Parmareggio","200 g",0.200,2.19,6,V,"Il volantino stampa 10,95 al kg."),
 ("Yogurt","Pam","pamextra24","Freschi","Yogurt cremoso Müller magro o intero, gusti vari, formato risparmio","1 kg (8 × 125 g)",1,3.39,6,V,""),
 ("Yogurt","Pam","pamextra24","Freschi","Yogurt vegetale Yosoi Valsoia, gusti vari","250 g (2 × 125 g)",0.250,1.29,6,V,"Solo con l'app Pam Perte Plus. È vegetale, di soia. Il volantino stampa 5,16 al kg."),
 ("Merendine","Pam","pamextra24","Colazione","Snack Nesquik Nestlé, cacao o latte","130 g (5 × 26 g)",0.130,1.25,6,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 9,62 al kg."),
 ("Latte","Pam","pamextra24","Latteria","Latte UHT alta digeribilità senza lattosio Latte Reggiano","1 litro",1,0.99,7,V,""),
 ("Pane","Pam","pamextra24","Panetteria","La Pinsa di Bugli","230 g",0.230,2.99,7,V,"È una base per pinsa, da farcire. Il volantino stampa 13,00 al kg."),
 ("Uova","Pam","pamextra24","Freschi","Uova medie Aequilibrium AIA, alla vitamina E","10 uova",10,3.99,7,V,"Da galline allevate a terra senza uso di antibiotici."),
 ("Pasta","Pam","pamextra24","Freschi","Gnocchetti o gnocchi di patate Giovanni Rana","500 g",0.500,2.29,7,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 4,58 al kg."),
 ("Salmone","Pam","pamextra24","Freschi","Salmone scozzese affumicato Tesori dell'Arca","100 g",0.100,5.90,7,V,"Il volantino stampa 59,00 al kg."),
 ("Salmone","Pam","pamextra24","Freschi","Salmone norvegese affumicato KV Nordic","50 g",0.050,2.99,7,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 59,80 al kg."),
 ("Mozzarella","Pam","pamextra24","Freschi","Mozzarella Nonno Nanni, formato convenienza","375 g (3 × 125 g)",0.375,3.19,8,V,"Il volantino stampa 8,51 al kg."),
 ("Formaggio","Pam","pamextra24","Freschi","Stracchino Nonno Nanni","100 g",0.100,1.49,8,V,"Il volantino stampa 14,90 al kg."),
 ("Prosciutto","Pam","pamextra24","Salumi","Il Cotto di Parma Parmacotto, affettato","100 g",0.100,3.49,8,V,"Sconto del 30%: prima 4,99."),
 ("Mortadella","Pam","pamextra24","Salumi","Mortadella Felsineo affettata, bipack","200 g (2 × 100 g)",0.200,3.00,8,V,"Sconto del 30%: prima 4,29. Il volantino stampa 15,00 al kg."),
 ("Pollo","Pam","pamextra24","Freschi","Würstel Wüber «Gli Originali» di pollo","100 g",0.100,0.59,8,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 5,90 al kg."),
 ("Salame","Pam","pamextra24","Salumi","Salame Strolghino Fratelli Boschi","230 g",0.230,3.84,8,V,"Sconto del 30%: prima 5,49. Il volantino stampa 16,70 al kg."),
 ("Spalmabili","Pam","pamextra24","Freschi","Formaggio fresco Philadelphia Original","250 g",0.250,2.69,8,V,"Il volantino stampa 10,76 al kg."),
 ("Ricotta","Pam","pamextra24","Freschi","Ricottine fresche Vallelata","200 g (2 × 100 g)",0.200,1.39,8,V,"Il volantino stampa 6,95 al kg."),
 ("Formaggio","Pam","pamextra24","Freschi","Provolone Valpadana DOP a fette Pam, dolce o piccante","150 g",0.150,2.29,8,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 15,27 al kg."),
 ("Formaggio","Pam","pamextra24","Freschi","Sottilette «Le Originali» classiche","200 g",0.200,1.79,8,V,"Il volantino stampa 8,95 al kg."),
 ("Grana","Pam","pamextra24","Freschi","«Biraghini» Gran Biraghi","400 g",0.400,7.49,8,V,"Il volantino stampa 18,72 al kg."),
 ("Formaggio","Pam","pamextra24","Freschi","Formaggio «Le Brie» Président","200 g",0.200,2.99,8,V,"Il volantino stampa 14,95 al kg."),
 ("Formaggio","Pam","pamextra24","Freschi","Grattugiato fresco di pecorino Biraghi","60 g",0.060,1.39,8,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 23,17 al kg."),
 ("Formaggio","Pam","pamextra24","Freschi","Mini Babybel Original","100 g (5 × 20 g)",0.100,2.19,9,V,"Solo con l'app Pam Perte Plus. Il volantino stampa «al kg 2,19», ma è un errore di stampa: 100 g a 2,19 sono 21,90 al kg."),
 ("Pasta","Pam","pamextra24","Dispensa","Pastine all'uovo «Emiliane» Barilla, formati vari","275 g",0.275,0.75,10,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 2,73 al kg."),
 ("Pasta","Pam","pamextra24","Dispensa","Pasta di semola integrale La Molisana, formati vari","500 g",0.500,1.00,10,V,"Il volantino stampa 2,00 al kg."),
 ("Riso","Pam","pamextra24","Dispensa","Riso Basmati Curtiriso","1 kg",1,2.99,10,V,""),
 ("Olio d'oliva","Pam","pamextra24","Dispensa","Olio extra vergine di oliva 100% italiano Clemente","1 litro",1,5.99,10,V,"Solo con l'app Pam Perte Plus."),
 ("Olio d'oliva","Pam","pamextra24","Dispensa","Olio extra vergine di oliva Il Frantolio Carapelli","750 ml",0.750,3.99,10,V,"Il volantino stampa 5,32 al litro."),
 ("Pomodoro","Pam","pamextra24","Dispensa","«Polpa finissima» Cirio","1,2 kg (3 × 400 g)",1.2,2.00,10,V,"Il volantino stampa 1,67 al kg."),
 ("Pomodoro","Pam","pamextra24","Dispensa","Pomodoro datterino intero in succo di pomodoro Tesori dell'Arca","360 g",0.360,1.00,10,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 2,78 al kg."),
 ("Tonno","Pam","pamextra24","Dispensa","Tonno «Filo d'olio» Rio Mare all'olio di oliva","260 g (4 × 65 g)",0.260,4.99,10,V,"Solo con l'app Pam Perte Plus. Il conto è sul peso delle scatolette, come fa il volantino (19,19 al kg)."),
 ("Tonno","Pam","pamextra24","Dispensa","Filetti di tonno all'olio di oliva Rio Mare, vaso di vetro","180 g",0.180,3.99,10,V,"Il conto è sul peso del vaso, come fa il volantino (22,17 al kg): il peso sgocciolato non è stampato, quindi al chilo di tonno costa di più."),
 ("Sughi","Pam","pamextra24","Dispensa","Pesti Rio Mare, gusti vari","130 g",0.130,2.00,10,V,"Il volantino stampa 15,38 al kg."),
 ("Formaggio","Pam","pamextra24","Gastronomia","Caciotta vaccina","all'etto",0.1,1.19,12,V,"Al banco."),
 ("Formaggio","Pam","pamextra24","Gastronomia","Tomino piemontese bianco o con speck","200 g",0.200,3.49,12,V,"Vaschette da 200 o 220 g allo stesso prezzo: il conto è sulla più piccola (17,45 al kg)."),
 ("Formaggio","Pam","pamextra24","Gastronomia","Bella Lodi classico stagionato 18 mesi","all'etto",0.1,1.29,12,V,"Al banco. È un formaggio duro da grattugiare, ma non è Grana Padano né Parmigiano."),
 ("Pancetta","Pam","pamextra24","Gastronomia","Pancetta affumicata","all'etto",0.1,1.49,12,V,"Al banco. Carne italiana."),
 ("Pancetta","Pam","pamextra24","Gastronomia","Guanciale al pepe a fette, vaschetta da 200 g circa","all'etto",0.1,1.43,12,V,"Sconto del 20%: prima 1,79 all'etto. Carne italiana."),
 ("Salame","Pam","pamextra24","Gastronomia","Spianata calabra piccante","all'etto",0.1,1.79,12,V,"Al banco."),
 ("Salame","Pam","pamextra24","Gastronomia","Salame Filzetta, da 400 g circa","all'etto",0.1,1.39,12,V,"Al banco."),
 ("Pizza","Pam","pamextra24","Panetteria","Pizza gourmet salsiccia e funghi, trancio da 150 g circa","150 g circa",0.150,2.50,13,V,"Prezzo al pezzo. È un trancio fresco del banco, non surgelato. Il peso è indicativo. Sulla pala intera sconto del 30%."),
 ("Merendine","Pam","pamextra24","Panetteria","Pain au chocolat","80 g",0.080,0.99,13,V,"Il volantino stampa 12,38 al kg."),
 ("Pane","Pam","pamextra24","Panetteria","Focaccina ai semi di zucca e grani antichi","65 g",0.065,0.89,13,V,"Il volantino stampa 13,69 al kg."),
 ("Pollo","Pam","pamextra24","Macelleria","Le Tenerelle di pollo Qualità 10+ Amadori","300 g",0.300,3.69,13,V,"Il volantino stampa 12,30 al kg."),
 ("Tacchino","Pam","pamextra24","Macelleria","Hamburger di tacchino Amadori","320 g",0.320,3.15,13,V,"Il volantino stampa 9,84 al kg."),
 ("Pollo","Pam","pamextra24","Macelleria","Cotoletta di pollo sottile Amadori","300 g",0.300,2.99,13,V,"Il volantino stampa 9,97 al kg."),
 ("Pesce","Pam","pamextra24","Surgelati","Vongole del Pacifico sgusciate cotte Lopesce","200 g",0.200,2.79,14,V,"Solo con l'app Pam Perte Plus. Surgelate. Il volantino stampa 13,95 al kg."),
 ("Gamberi","Pam","pamextra24","Surgelati","Code di gambero argentino sgusciato e devenato Tesori dell'Arca","250 g",0.250,7.49,14,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 29,96 al kg."),
 ("Calamari","Pam","pamextra24","Surgelati","Seppioline pulite 20/40 Marinai","800 g",0.800,9.69,14,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 12,11 al kg."),
 ("Merluzzo","Pam","pamextra24","Surgelati","Filetti di platessa alla mugnaia Pam","250 g",0.250,3.89,14,V,"Solo con l'app Pam Perte Plus. Surgelati e già conditi. Il volantino stampa 15,56 al kg."),
 ("Merluzzo","Pam","pamextra24","Surgelati","Cotolette di merluzzo Pam","400 g",0.400,4.39,14,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 10,97 al kg."),
 ("Pollo","Pam","pamextra24","Surgelati","Ortaiola con spinaci Amadori","300 g",0.300,2.49,14,V,"Solo con l'app Pam Perte Plus. Cotolette di pollo con spinaci. Il volantino stampa 8,30 al kg."),
 ("Merluzzo","Pam","pamextra24","Surgelati","4 Fiori di merluzzo Findus","300 g",0.300,7.49,14,V,"Il volantino stampa 24,96 al kg."),
 # Pagina 14: le 2 Croccole Findus a 3,00 e il Minestrone Findus a 2,99 sono
 # identici, stesso prezzo, a pam24 pagine 7 e 15: non riscritti.
 ("Verdure surgelate","Pam","pamextra24","Surgelati","Piselli novelli Findus, maxi formato","1 kg",1,4.69,14,V,""),
 ("Verdure surgelate","Pam","pamextra24","Surgelati","Fagiolini fini Pam","1 kg",1,2.99,15,V,"Solo con l'app Pam Perte Plus."),
 ("Verdure surgelate","Pam","pamextra24","Surgelati","Caponata di verdure «Gusto ricco» Orogel","250 g",0.250,2.19,15,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 8,76 al kg."),
 ("Pizza","Pam","pamextra24","Surgelati","Pizza würstel e patatine Pam","400 g",0.400,2.95,15,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 7,37 al kg."),
 ("Pizza","Pam","pamextra24","Surgelati","Pizza margherita Bella Napoli Buitoni, 2 pizze","650 g",0.650,4.49,15,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 6,91 al kg."),
 ("Pizza","Pam","pamextra24","Surgelati","Pizza bufala e pomodorini Tesori dell'Arca","380 g",0.380,3.89,15,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 10,24 al kg."),
 ("Pizza","Pam","pamextra24","Surgelati","Pizza tonno e cipolla rossa o salame piccante Tesori dell'Arca","340 g",0.340,3.69,15,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 10,85 al kg."),
 ("Gelato","Pam","pamextra24","Surgelati","Mini cono panna e cioccolato Pam, 8 pezzi","400 g",0.400,2.89,15,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 7,22 al kg."),
 ("Gelato","Pam","pamextra24","Surgelati","Gelato sandwich bianco e cacao 100% vegetale Valsoia, 8 pezzi","320 g",0.320,3.99,15,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 12,47 al kg."),
 ("Birra","Pam","pamextra24","Bevande","Birra Corona Extra o Cero","330 ml",0.330,1.19,16,V,"Il volantino stampa 3,61 al litro."),
 ("Birra","Pam","pamextra24","Bevande","Birra Heineken 0.0, lattina","330 ml",0.330,0.99,16,V,"Solo con l'app Pam Perte Plus. Analcolica. Il volantino stampa 3,00 al litro."),
 ("Birra","Pam","pamextra24","Bevande","Birra Heineken, lattina","500 ml",0.500,1.09,16,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 2,18 al litro."),
 ("Birra","Pam","pamextra24","Bevande","Birra Strong Ale Ceres, lattina","500 ml",0.500,1.79,16,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 3,58 al litro."),
 ("Birra","Pam","pamextra24","Bevande","Birra «Weiss» Franziskaner","500 ml",0.500,1.39,16,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 2,78 al litro."),
 ("Birra","Pam","pamextra24","Bevande","Birra Super Tennent's","825 ml (3 × 275 ml)",0.825,3.79,16,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 4,62 al litro."),
 ("Birra","Pam","pamextra24","Bevande","Birra Peroni, lattine","660 ml (2 × 330 ml)",0.660,1.39,16,V,"Il volantino stampa 2,11 al litro."),
 ("Birra","Pam","pamextra24","Bevande","Birra «Cristalli di sale» Messina","500 ml",0.500,1.39,16,V,"Il volantino stampa 2,78 al litro."),
 ("Birra","Pam","pamextra24","Bevande","Birra Tuborg","660 ml",0.660,0.99,16,V,"Il volantino stampa 1,50 al litro."),
 ("Birra","Pam","pamextra24","Bevande","Birra «Kronen» Forst","660 ml",0.660,1.29,16,V,"Il volantino stampa 1,95 al litro."),
 ("Birra","Pam","pamextra24","Bevande","Birra analcolica Tourtel","990 ml (3 × 330 ml)",0.990,2.29,16,V,"Il volantino stampa 2,31 al litro."),
 ("Birra","Pam","pamextra24","Bevande","Birra 6 Luppoli Poretti, doppio malto rossa","990 ml (3 × 330 ml)",0.990,2.69,17,V,"Il volantino stampa 2,72 al litro."),
 ("Birra","Pam","pamextra24","Bevande","Birra 9 Luppoli Poretti, IPA","990 ml (3 × 330 ml)",0.990,3.29,17,V,"Il volantino stampa 3,32 al litro."),
 ("Vino","Pam","pamextra24","Bevande","Passerina Volpe Cantina Tollo, biologico","750 ml",0.750,4.50,17,V,"Il volantino stampa 6,00 al litro."),
 ("Vino","Pam","pamextra24","Bevande","Spumante Prosecco DOC extra dry Astoria","750 ml",0.750,4.99,17,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 6,65 al litro."),
 ("Vino","Pam","pamextra24","Bevande","Primitivo di Manduria Stilio Mottura","750 ml",0.750,9.95,17,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 13,27 al litro."),
 ("Vino","Pam","pamextra24","Bevande","Morellino di Scansano DOCG Cantina Vignaioli","750 ml",0.750,5.99,17,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 7,99 al litro."),
 ("Vino","Pam","pamextra24","Bevande","Vino Tavernello bianco o rosso, brik","750 ml (3 × 250 ml)",0.750,1.69,17,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 2,25 al litro."),
 ("Acqua","Pam","pamextra24","Bevande","Acqua effervescente naturale Lete","9 litri (6 × 1,5 litri)",9,2.16,18,V,"Solo con l'app Pam Perte Plus. 0,36 a bottiglia. Il volantino stampa 0,24 al litro."),
 ("Acqua","Pam","pamextra24","Bevande","Acqua minerale Lete","3 litri (6 × 500 ml)",3,1.29,18,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 0,43 al litro."),
 ("Bibite","Pam","pamextra24","Bevande","Bibite San Benedetto, gusti vari","1,5 litri",1.5,0.79,18,V,"Solo con l'app Pam Perte Plus. Il volantino stampa 0,53 al litro."),
 ("Bibite","Pam","pamextra24","Bevande","Thè Beltè, limone o pesca","1,5 litri",1.5,0.69,18,V,"Solo con l'app Pam Perte Plus. È tè freddo. Il volantino stampa 0,46 al litro."),
 ("Bibite","Pam","pamextra24","Bevande","Succhi di frutta Pam, gusti vari","600 ml (3 × 200 ml)",0.600,0.99,18,V,"Il volantino stampa 1,65 al litro."),
 ("Bibite","Pam","pamextra24","Bevande","Gatorade, gusti vari","500 ml",0.500,0.85,18,V,"Il volantino stampa 1,70 al litro."),
 ("Lavatrice","Pam","pamextra24","Cura casa","Detersivo per capi delicati Spuma di Sciampagna, nero e delicati","30 lavaggi",30,2.99,20,V,"Solo con l'app Pam Perte Plus."),
 ("Lavatrice","Pam","pamextra24","Cura casa","Detersivo liquido per lavatrice Soft","2,25 litri, 50 lavaggi",50,2.50,20,V,"Solo con l'app Pam Perte Plus."),
 ("Lavatrice","Pam","pamextra24","Cura casa","Detersivo per lavatrice Coccolino","37 lavaggi",37,5.99,20,V,""),
 ("Ammorbidente","Pam","pamextra24","Cura casa","Ammorbidente diluito Mon Amour","3 litri, 60 lavaggi",60,3.49,20,V,""),
 ("Asciugatutto","Pam","pamextra24","Cura casa","Carta cucina «Regina di Cuori», 3 veli","3 rotoli",3,2.79,22,V,""),
 ("Asciugatutto","Pam","pamextra24","Cura casa","Asciugatutto maxi rotolo Arkalia, 2 veli, 300 strappi","1 maxi rotolo",1,2.00,22,V,"Un rotolo solo ma grande (300 strappi): contato come un rotolo, al rotolo sembra caro più di quanto sia."),
 ("Asciugatutto","Pam","pamextra24","Cura casa","Bobina «Mega» Famy, 700 strappi","1 bobina",1,3.99,22,V,"Una bobina sola ma enorme (700 strappi): contata come un rotolo, al rotolo sembra cara più di quanto sia."),
 ("Dentifricio","Pam","pamextra24","Igiene","Dentifricio Aquafresh menta fresca, doppio formato","150 ml (2 × 75 ml)",0.150,1.99,24,V,""),
 ("Dentifricio","Pam","pamextra24","Igiene","Dentifricio «3D White» AZ","50 ml",0.050,2.00,24,V,""),
 ("Dentifricio","Pam","pamextra24","Igiene","Dentifricio Total Original Colgate","75 ml",0.075,2.00,24,V,"Solo con l'app Pam Perte Plus."),
 ("Shampoo","Pam","pamextra24","Igiene","Shampoo o balsamo Sunsilk, assortiti","200 ml",0.200,2.09,24,V,"Solo con l'app Pam Perte Plus. Flaconi da 250 o 200 ml allo stesso prezzo: il conto è sul più piccolo."),
 ("Shampoo","Pam","pamextra24","Igiene","Shampoo Vidal","250 ml",0.250,1.00,24,V,"Solo con l'app Pam Perte Plus."),
 ("Carta igienica","Pam","pamextra24","Cura casa","Carta igienica Flutech Infiore, 3 veli","6 rotoli",6,2.99,25,V,"Solo con l'app Pam Perte Plus."),
 ("Bagnoschiuma","Pam","pamextra24","Igiene","Bagnoschiuma Nivea, varie profumazioni","650 ml",0.650,3.29,26,V,"Solo con l'app Pam Perte Plus."),
 # CONAD «Freschi di convenienza», dal 24 settembre al 7 ottobre (conad24),
 # edizione Piemonte, quella del Conad di via Cesana 78. Letto per intero il
 # 2026-09-22 dal PDF sul sito Conad.
 ("Frutta","Conad","conad24","Ortofrutta","Uva senza semi mix bicolore Conad Percorso Qualità","500 g",0.500,1.77,1,V,"Prodotto italiano. Il volantino stampa 3,54 al kg."),
 ("Manzo","Conad","conad24","Macelleria","Macinato di bovino adulto Conad Percorso Qualità","al kg",1,9.90,1,V,""),
 ("Formaggio","Conad","conad24","Gastronomia","Gorgonzola dolce DOP Sapori&Dintorni Conad","all'etto",0.1,0.99,1,V,"Al banco."),
 ("Formaggio","Conad","conad24","Gastronomia","Caprino pura capra Caseificio dell'Alta Langa, take away","all'etto",0.1,1.65,4,V,"Formaggio del territorio."),
 ("Prosciutto","Conad","conad24","Gastronomia","Prosciutto cotto Gran Biscotto Rovagnati Delì","all'etto",0.1,2.19,4,V,"Al banco."),
 ("Prosciutto","Conad","conad24","Gastronomia","Prosciutto crudo Assisi Salumi","all'etto",0.1,1.69,4,V,"Al banco."),
 ("Grana","Conad","conad24","Gastronomia","Formaggio Trentingrana DOP Sapori&Dintorni Conad, stagionatura minima 20 mesi","all'etto",0.1,1.69,4,V,"Al banco. È un grana del Trentino."),
 ("Bresaola","Conad","conad24","Gastronomia","Bresaola della Valtellina IGP Sapori&Dintorni Conad","all'etto",0.1,3.69,4,V,"Al banco."),
 ("Salame","Conad","conad24","Gastronomia","Salame Rosa Brizio","all'etto",0.1,1.99,4,V,"Al banco."),
 ("Mortadella","Conad","conad24","Salumi","Affettati take away Sapori&Dintorni Conad, vari tipi (per esempio mortadella)","120 g",0.120,2.69,4,V,"Il volantino dà il prezzo sull'esempio della mortadella da 120 g (22,42 al kg): gli altri affettati hanno pesi loro."),
 ("Prosciutto","Conad","conad24","Gastronomia","Speck Alto Adige IGP Sapori&Dintorni Conad","all'etto",0.1,1.69,4,V,"Al banco."),
 ("Tacchino","Conad","conad24","Gastronomia","Petto di tacchino al forno Kometa","all'etto",0.1,1.99,4,V,"Al banco."),
 ("Formaggio","Conad","conad24","Gastronomia","Bra tenero DOP Caseificio Rabbia","all'etto",0.1,1.29,5,V,"Al banco. Formaggio del territorio."),
 ("Manzo","Conad","conad24","Gastronomia","Roast beef di fesa all'inglese Conad","all'etto",0.1,3.49,5,V,"Al banco, già cotto."),
 ("Formaggio","Conad","conad24","Gastronomia","Formaggio Maasdam Conad","all'etto",0.1,0.99,5,V,"Al banco. «Bassi e fissi»."),
 ("Pollo","Conad","conad24","Gastronomia","Cotolette con filetti di pollo Gustosamente Conad","all'etto",0.1,1.49,5,V,"Al banco, già pronte."),
 ("Pane","Conad","conad24","Panetteria","Focaccia Conad con olio extra vergine di oliva, farina 100% italiana","135 g",0.135,1.90,5,V,"Il volantino dà il prezzo sull'esempio della focaccia all'olio da 135 g (14,08 al kg): ci sono altri tipi e pesi."),
 ("Formaggio","Conad","conad24","Gastronomia","Formaggio Toma piemontese DOP Caseificio Rosso","all'etto",0.1,1.29,5,V,"Al banco."),
 ("Pane","Conad","conad24","Panetteria","Base pinsa Selezione Forno","500 g",0.500,3.98,5,V,"È una base da farcire. Il volantino stampa 7,96 al kg."),
   # pagina 5: la crostata De Mori e le «verdure Gustosamente» cotte non hanno una categoria nel catalogo
 ("Pollo","Conad","conad24","Macelleria","Petto di pollo a fette Conad Percorso Qualità","al kg",1,10.19,6,V,"Sconto del 40%: prima 16,99. Carne italiana."),
 ("Suino","Conad","conad24","Macelleria","Lonza disossata di suino a tranci Conad Percorso Qualità, confezione convenienza","al kg",1,5.99,6,V,"Sconto del 40%: prima 9,99. Carne italiana."),
 ("Manzo","Conad","conad24","Macelleria","Hamburger di Chianina Sapori&Dintorni Conad","200 g (2 × 100 g)",0.200,4.79,6,V,"Il volantino stampa 23,95 al kg."),
 ("Manzo","Conad","conad24","Macelleria","Fettine di anteriore di bovino adulto Conad Percorso Qualità","al kg",1,17.59,6,V,""),
 ("Manzo","Conad","conad24","Macelleria","Spezzatino di bovino adulto Conad Percorso Qualità","al kg",1,15.99,6,V,""),
 ("Suino","Conad","conad24","Macelleria","Bombette di suino con bacon e formaggio Conad","200 g",0.200,2.19,6,V,"Sconto del 30%: prima 3,14. Il volantino stampa 10,95 al kg."),
 ("Salsiccia","Conad","conad24","Macelleria","Salsicce di pollo, tacchino e suino Amadori","650 g",0.650,4.74,6,V,"Sconto del 50%: prima 9,49. Il volantino stampa 7,30 al kg."),
 ("Manzo","Conad","conad24","Macelleria","Polpa di anteriore di bovino adulto Conad Percorso Qualità","al kg",1,16.69,6,V,""),
 ("Pollo","Conad","conad24","Macelleria","Fusi o sovracosce di pollo Conad Percorso Qualità","al kg",1,5.39,6,V,"Carne italiana."),
 ("Tacchino","Conad","conad24","Macelleria","Bon Roll AIA, classico o con speck","680 g",0.680,6.95,6,V,"Sconto del 40%: prima 11,59. È un arrosto di tacchino. Il volantino stampa 10,23 al kg."),
 ("Pesce","Conad","conad24","Pescheria","Trota iridea salmonata Conad Percorso Qualità, allevata in Italia","al kg",1,6.90,7,V,"Solo nei punti vendita con reparto pescheria. Sconto del 30%: prima 9,86."),
 ("Salmone","Conad","conad24","Pescheria","Salmone a tranci","al kg",1,13.90,7,V,"Solo nei punti vendita con reparto pescheria."),
 ("Calamari","Conad","conad24","Pescheria","Totani","al kg",1,8.90,7,V,"Solo nei punti vendita con reparto pescheria."),
 ("Gamberi","Conad","conad24","Pescheria","Code di mazzancolle tropicali sgusciate cotte","al kg",1,23.90,7,V,"Solo nei punti vendita con reparto pescheria."),
 ("Pesce","Conad","conad24","Pescheria","Vongole lupini del mar Adriatico","al kg",1,5.98,7,V,"Solo nei punti vendita con reparto pescheria."),
 ("Pesce","Conad","conad24","Pescheria","Rondelle di polpo Sapori&Idee Conad","200 g",0.200,7.90,7,V,"Solo nei punti vendita con reparto pescheria. Il volantino stampa 39,50 al kg."),
 ("Pesce","Conad","conad24","Pescheria","Ombrina Conad Percorso Qualità, allevata in Italia","al kg",1,12.90,7,V,"Solo nei punti vendita con reparto pescheria."),
 ("Frutta","Conad","conad24","Ortofrutta","Uva Palieri Conad Percorso Qualità","al kg",1,2.47,8,V,"Origine Italia, categoria I."),
 ("Frutta","Conad","conad24","Ortofrutta","Uva Red Globe Conad Percorso Qualità","al kg",1,2.47,8,V,"Origine Italia, categoria I."),
 ("Frutta","Conad","conad24","Ortofrutta","Uva Pizzutella Conad Percorso Qualità","al kg",1,2.97,8,V,"Origine Italia, categoria I."),
 ("Frutta","Conad","conad24","Ortofrutta","Uva bianca senza semi Almaverde Bio","500 g",0.500,2.18,8,V,"Biologica, origine Italia. Il volantino stampa 4,36 al kg."),
 ("Frutta","Conad","conad24","Ortofrutta","Banane Conad Percorso Qualità","al kg",1,1.27,9,V,"Categoria I."),
 ("Frutta","Conad","conad24","Ortofrutta","Susine Metis Sapori&Idee Conad","500 g",0.500,1.47,9,V,"Prodotto italiano. Il volantino stampa 2,94 al kg."),
 ("Frutta","Conad","conad24","Ortofrutta","Ficodindia dell'Etna DOP Sapori&Dintorni Conad","800 g",0.800,2.17,9,V,"Il volantino stampa 2,72 al kg."),
 ("Frutta","Conad","conad24","Ortofrutta","Mele Sweetango Melinda, calibro 73/78","al kg",1,1.25,9,V,"Sconto del 30%: prima 1,79. Origine Italia."),
 ("Verdura","Conad","conad24","Ortofrutta","Fagiolini burrini Conad Percorso Qualità","750 g",0.750,2.27,9,V,"Prodotto italiano. Il volantino stampa 3,03 al kg."),
 ("Patate","Conad","conad24","Ortofrutta","Patate gialle Naturella Ruggiero, saporite al forno e vapore","1,5 kg",1.5,2.17,9,V,"Origine Italia. Il volantino stampa 1,45 al kg."),
 ("Verdura","Conad","conad24","Ortofrutta","Cicoria Conad Percorso Qualità","400 g",0.400,1.47,9,V,"Da cuocere. Il volantino stampa 3,68 al kg."),
 # pagina 9: mousse Melinda, noci Jumbo e zuppe fresche Conad non hanno una categoria nel catalogo
 ("Pasta","Conad","conad24","Freschi","Lasagne fresche all'uovo Sfogliavelo Giovanni Rana","250 g",0.250,1.69,10,V,"Solo con la Carta Insieme Conad. Senza tessera 2,09, cioè 8,36 al kg."),
 ("Mozzarella","Conad","conad24","Freschi","Mozzarella di bufala campana DOP Garofalo","300 g (3 × 100 g)",0.300,3.00,10,V,"Il volantino stampa 10,00 al kg."),
 ("Ricotta","Conad","conad24","Freschi","Ricotta Santa Lucia Galbani","250 g",0.250,0.99,10,V,"Il volantino stampa 3,96 al kg."),
 ("Pasta","Conad","conad24","Freschi","Pasta fresca Conad di semola di grano duro italiano, trofie o orecchiette","500 g",0.500,1.39,10,V,"«Bassi e fissi». Il volantino stampa 2,78 al kg."),
 ("Pasta","Conad","conad24","Freschi","Pasta fresca ripiena Sfoglia sottile Conad, vari tipi","250 g",0.250,1.58,10,V,"Il volantino stampa 6,32 al kg."),
 ("Mozzarella","Conad","conad24","Freschi","Mozzarella Santa Lucia Galbani, Tris","375 g (3 × 125 g)",0.375,2.69,10,V,"Il volantino stampa 7,18 al kg."),
 ("Spalmabili","Conad","conad24","Freschi","Philadelphia vegetale","145 g",0.145,2.29,10,V,"È vegetale, non di latte. Il volantino stampa 15,80 al kg."),
 ("Formaggio","Conad","conad24","Freschi","Formaggio a fette Freschi & Convenienti Conad, vari tipi (per esempio maasdam, 8 fette)","200 g",0.200,2.39,10,V,"«Bassi e fissi». Il volantino dà il prezzo sull'esempio del maasdam da 200 g (11,95 al kg): gli altri tipi hanno pesi loro."),
 ("Spalmabili","Conad","conad24","Freschi","Crescenza light Conad Piacersi","200 g",0.200,1.59,10,V,"Latte italiano. Il volantino stampa 7,95 al kg."),
 ("Ricotta","Conad","conad24","Freschi","Ricottine senza lattosio Conad Piacersi","200 g (2 × 100 g)",0.200,0.99,10,V,"Latte italiano. Il volantino stampa 4,95 al kg."),
 ("Spalmabili","Conad","conad24","Freschi","Robiola senza lattosio Conad Piacersi","100 g",0.100,1.09,10,V,"Latte italiano. Il volantino stampa 10,90 al kg."),
 ("Pancetta","Conad","conad24","Salumi","Guanciale in stick Negroni","100 g",0.100,1.45,11,V,"Solo con la Carta Insieme Conad. Senza tessera 2,07, cioè 20,70 al kg."),
 ("Salmone","Conad","conad24","Freschi","Salmone norvegese affumicato Fjordisalmone Riunione","100 g",0.100,2.98,11,V,"Sconto del 40%: prima 4,98."),
 ("Formaggio","Conad","conad24","Freschi","Fiocchi di latte senza lattosio Conad Piacersi","200 g",0.200,1.09,11,V,"Il volantino stampa 5,45 al kg."),
 ("Formaggio","Conad","conad24","Freschi","Finette classiche senza lattosio Conad Alimentum, 6 fette","150 g",0.150,1.10,11,V,"Formaggio fuso a fette. Il volantino stampa 7,34 al kg."),
 ("Yogurt","Conad","conad24","Freschi","I love Kefir Nestlé, vari tipi","500 g",0.500,1.25,11,V,"È kefir da bere. Il volantino stampa 2,50 al kg."),
 ("Yogurt","Conad","conad24","Freschi","Yogurt alla greca zero grassi senza lattosio Zymil Parmalat, vari tipi","150 g",0.150,0.95,11,V,"Il volantino stampa 6,34 al kg."),
 ("Latte","Conad","conad24","Latteria","Latte UHT senza lattosio Conad Piacersi, vari tipi","1 litro",1,1.19,11,V,"Latte italiano."),
 ("Yogurt","Conad","conad24","Freschi","Yogurt senza lattosio Conad Piacersi, vari tipi","250 g (2 × 125 g)",0.250,0.68,11,V,"Latte italiano. Il volantino stampa 2,72 al kg."),
 ("Pollo","Conad","conad24","Salumi","Affettati Conad Piacersi, vari tipi (per esempio petto di pollo al forno)","100 g",0.100,1.39,11,V,"È un affettato di petto di pollo al forno, carne italiana; gli altri tipi della linea allo stesso prezzo."),
 ("Latte","Conad","conad24","Latteria","Latte UHT parzialmente scremato Bontà e Linea Parmalat","1 litro",1,0.95,11,V,""),
 # pagina 11: la bevanda vegetale Orasì non ha una categoria nel catalogo
 ("Verdure surgelate","Conad","conad24","Surgelati","Minestrone classico La Valle degli Orti","400 g",0.400,1.49,12,V,"Solo con la Carta Insieme Conad. Senza tessera 2,29, cioè 5,73 al kg."),
 ("Bastoncini","Conad","conad24","Surgelati","Bastoncini di filetti di merluzzo Frosta, 15 pezzi","450 g",0.450,4.39,12,V,"Solo con la Carta Insieme Conad. Senza tessera 6,24, cioè 13,87 al kg."),
 ("Uova","Conad","conad24","Freschi","Le uova del Piemonte Le Naturelle, da allevamento a terra","6 uova",6,1.59,12,V,"Solo con la Carta Insieme Conad. Senza tessera 1,88."),
 ("Verdure surgelate","Conad","conad24","Surgelati","Verdure biologiche Conad Verso Natura, vari tipi (per esempio spinaci in foglie)","450 g",0.450,1.59,12,V,"Solo con la Carta Insieme Conad. Senza tessera 1,89, cioè 4,20 al kg."),
 ("Grana","Conad","conad24","Freschi","Grana Padano DOP grattugiato Conad","100 g",0.100,1.79,12,V,"«Bassi e fissi»."),
 ("Prosciutto","Conad","conad24","Salumi","Prosciutto cotto Gardani","100 g",0.100,1.99,12,V,"Solo con la Carta Insieme Conad. Senza tessera 3,99."),
 ("Manzo","Conad","conad24","Freschi","Teneroni Granterre, vari tipi (per esempio classici)","150 g",0.150,2.09,12,V,"Solo con la Carta Insieme Conad. Senza tessera 2,35, cioè 15,67 al kg. Sono hamburger di carne mista: il volantino non dice di quale."),
 ("Gelato","Conad","conad24","Surgelati","Gelato Nutella","230 g",0.230,3.39,12,V,"Solo con la Carta Insieme Conad. Senza tessera 4,99, cioè 21,70 al kg."),
 # pagina 12: i piatti pronti Garden Gourmet (vegetali), il Danacol e la pasta sfoglia senza glutine non hanno una categoria nel catalogo
 ("Pesce","Conad","conad24","Surgelati","Filetti di branzino o di orata Conad","250 g",0.250,4.98,13,V,"Solo con la Carta Insieme Conad. Senza tessera 7,45, cioè 29,80 al kg. Surgelati."),
 ("Pasta","Conad","conad24","Dispensa","Pasta all'uovo Sapori&Idee Conad, vari tipi (fettuccine, tagliatelle)","500 g",0.500,2.19,13,V,"Solo con la Carta Insieme Conad. Senza tessera 2,82, cioè 5,64 al kg. Ingredienti 100% italiani."),
 ("Gelato","Conad","conad24","Surgelati","Gelato pralinato Conad alla vaniglia con amarena, 6 pezzi","360 g",0.360,2.99,13,V,"«Bassi e fissi». Il volantino stampa 8,31 al kg."),
 ("Pizza","Conad","conad24","Surgelati","Pizza La Rettangolare Conad, vari tipi (per esempio 4 formaggi)","365 g",0.365,3.49,13,V,"«Bassi e fissi». Il volantino dà il prezzo sull'esempio della 4 formaggi da 365 g (9,57 al kg)."),
 ("Pane","Conad","conad24","Panetteria","Pane per sandwich Conad","550 g",0.550,1.39,13,V,"«Bassi e fissi». Il volantino stampa 2,53 al kg."),
 ("Pasta","Conad","conad24","Dispensa","Pasta di semola La Molisana, vari tipi","500 g",0.500,0.75,13,V,"Solo con la Carta Insieme Conad. Senza tessera 1,45, cioè 2,90 al kg."),
 ("Pasta","Conad","conad24","Dispensa","Pasta di legumi biologica Conad Piacersi, vari tipi","250 g",0.250,1.45,13,V,"Solo con la Carta Insieme Conad. Senza tessera 2,05, cioè 8,20 al kg. È pasta di lenticchie o piselli, non di grano."),
 ("Sughi","Conad","conad24","Dispensa","Il mio Gran Ragù Star, vari tipi","360 g (2 × 180 g)",0.360,2.59,13,V,"Solo con la Carta Insieme Conad. Senza tessera 3,15, cioè 8,75 al kg."),
 ("Pane","Conad","conad24","Panetteria","Gran Bauletto Mulino Bianco, integrale, rustico o campagnolo (per esempio integrale)","465 g",0.465,1.95,13,V,"Solo con la Carta Insieme Conad. Senza tessera 2,89, cioè 6,22 al kg. Il volantino dà il prezzo sull'esempio dell'integrale da 465 g."),
 # pagina 13: il piatto bilanciato Piacersi e le salse Heinz non hanno una categoria nel catalogo
 ("Olio d'oliva","Conad","conad24","Dispensa","Olio extra vergine di oliva classico Conad","1 litro",1,4.39,14,V,"Solo con la Carta Insieme Conad. Senza tessera 6,49."),
 ("Conserve","Conad","conad24","Dispensa","Filetti di alici in olio di oliva Delicius","150 g",0.150,5.99,14,V,"Solo con la Carta Insieme Conad. Senza tessera 6,69, cioè 44,60 al kg. Il conto è sul peso del vasetto, come fa il volantino."),
 ("Pane","Conad","conad24","Panetteria","Pinsata Savini","230 g",0.230,1.98,14,V,"Solo con la Carta Insieme Conad. Senza tessera 2,75, cioè 11,96 al kg."),
 ("Pane","Conad","conad24","Dispensa","Linea Wasa, vari tipi (per esempio Crunchy Twist semi di lino e papavero)","245 g",0.245,1.98,14,V,"Solo con la Carta Insieme Conad. Senza tessera 3,15, cioè 12,86 al kg. Il volantino dà il prezzo sull'esempio del Crunchy Twist da 245 g."),
 ("Tonno","Conad","conad24","Dispensa","Filetti di tonno Rio Mare lavorati a mano, all'olio di oliva, vaso di vetro","180 g",0.180,4.39,14,V,"Solo con la Carta Insieme Conad. Senza tessera 5,99, cioè 33,28 al kg. Il conto è sul peso del vaso, come fa il volantino (24,39 al kg)."),
 ("Tonno","Conad","conad24","Dispensa","Tonno Mareblu all'olio d'oliva o al naturale, formato speciale","480 g (8 × 60 g)",0.480,6.64,14,V,"Solo con la Carta Insieme Conad. Senza tessera 8,15, cioè 16,98 al kg. Il conto è sul peso delle scatolette, come fa il volantino (13,84 al kg)."),
 ("Salmone","Conad","conad24","Dispensa","Filetto di salmone Conad all'olio di oliva o al naturale, in scatola","150 g",0.150,3.35,14,V,"«Bassi e fissi». In scatola. Il volantino stampa 22,34 al kg."),
 ("Olio di semi","Conad","conad24","Dispensa","Prodotto per friggere Friol","1 litro",1,2.39,14,V,"Solo con la Carta Insieme Conad. Senza tessera 2,99."),
 ("Olio d'oliva","Conad","conad24","Dispensa","Olio extra vergine di oliva Granfruttato Monini, 100% italiano","750 ml",0.750,5.99,14,V,"Solo con la Carta Insieme Conad. Senza tessera 9,99, cioè 13,32 al litro. Il volantino stampa 7,99 al litro."),
 ("Pomodoro","Conad","conad24","Dispensa","Passata di pomodoro Mutti, 100% italiano","700 g",0.700,0.99,14,V,"Solo con la Carta Insieme Conad. Senza tessera 1,75, cioè 2,50 al kg. Il volantino stampa 1,42 al kg."),
 # pagina 14: la maionese Calvé non ha una categoria nel catalogo
 ("Cioccolato","Conad","conad24","Dispensa","Cioccolato Novi -30% di zuccheri, vari tipi (per esempio al latte)","100 g",0.100,2.19,15,V,"Solo con la Carta Insieme Conad. Senza tessera 2,59."),
 ("Cioccolato","Conad","conad24","Dispensa","Cioccolato Nero Nero Novi, vari tipi (per esempio 88% cacao extra fondente)","75 g",0.075,2.09,15,V,"Solo con la Carta Insieme Conad. Senza tessera 2,39, cioè 31,87 al kg. Il volantino stampa 2,79 all'etto."),
 ("Cioccolato","Conad","conad24","Dispensa","Mini fondente Nero Nero Novi (per esempio 88% cacao)","140 g",0.140,3.90,15,V,"Solo con la Carta Insieme Conad. Senza tessera 4,49, cioè 32,08 al kg. Il volantino stampa 27,86 al kg."),
 ("Creme","Conad","conad24","Colazione","CremaNovi fondente, 45% nocciole, senza latte","200 g",0.200,4.90,15,V,"Solo con la Carta Insieme Conad. Senza tessera 5,49, cioè 27,45 al kg. Il volantino stampa 24,50 al kg."),
 ("Pomodoro","Conad","conad24","Dispensa","Pomodori pelati biologici Conad Verso Natura","400 g",0.400,0.75,15,V,"Solo con la Carta Insieme Conad. Senza tessera 0,99, cioè 2,48 al kg."),
 ("Sughi","Conad","conad24","Dispensa","Pesto Cipressa Sapori Alberti con basilico genovese DOP, classico o senza aglio","170 g",0.170,3.25,15,V,"Solo con la Carta Insieme Conad. Senza tessera 4,61, cioè 27,12 al kg."),
 ("Caffè","Conad","conad24","Colazione","Capsule caffè espresso compatibili Nespresso Conad, 10 capsule","50 g",0.050,2.39,15,V,"«Bassi e fissi». 0,24 a capsula. Il volantino stampa 4,78 all'etto."),
 ("Tè","Conad","conad24","Colazione","Infuso Conad, vari tipi, 20 filtri","50 g",0.050,1.69,15,V,"«Bassi e fissi». Il volantino stampa 3,38 all'etto."),
 ("Pomodoro","Conad","conad24","Dispensa","Polpa finissima Il Polposissimo Petti","800 g (2 × 400 g)",0.800,1.98,15,V,"Solo con la Carta Insieme Conad. Senza tessera 2,72, cioè 3,40 al kg."),
 ("Caffè","Conad","conad24","Colazione","Caffè macinato fresco Kimbo","500 g (2 × 250 g)",0.500,6.99,15,V,"Solo con la Carta Insieme Conad. Senza tessera 10,68, cioè 21,36 al kg."),
 ("Tè","Conad","conad24","Colazione","Tè Twinings, vari tipi, 20 filtri","40 g",0.040,2.19,15,V,"Solo con la Carta Insieme Conad. Senza tessera 2,79, cioè 69,75 al kg."),
 # pagina 15: i brodi Knorr non hanno una categoria nel catalogo
 ("Biscotti","Conad","conad24","Colazione","Biscotti Mulino Bianco, vari tipi (per esempio Abbracci)","330 g",0.330,1.89,16,V,"Solo con la Carta Insieme Conad. Senza tessera 2,49. Formati da 330 o 350 g allo stesso prezzo: il conto è sul più piccolo (5,73 al kg)."),
 ("Biscotti","Conad","conad24","Colazione","Baiocchi Mulino Bianco, nocciola e cacao o pistacchio","260 g",0.260,2.49,16,V,"Solo con la Carta Insieme Conad. Senza tessera 2,79, cioè 10,74 al kg."),
 ("Merendine","Conad","conad24","Colazione","Il Cornetto classico Mulino Bianco, 6 pezzi","240 g",0.240,2.19,16,V,"Solo con la Carta Insieme Conad. Senza tessera 2,49, cioè 10,38 al kg."),
 ("Biscotti","Conad","conad24","Colazione","Biscotti Cuor di Mela Mulino Bianco","300 g",0.300,1.99,16,V,"Solo con la Carta Insieme Conad. Senza tessera 2,49, cioè 8,30 al kg."),
 ("Pane","Conad","conad24","Colazione","Fette biscottate Mulino Bianco, dorate o integrali, 72 fette","630 g",0.630,1.99,16,V,"Solo con la Carta Insieme Conad. Senza tessera 2,45, cioè 3,89 al kg."),
 ("Cereali","Conad","conad24","Colazione","Cereali Krave Kellogg's, vari tipi (per esempio nocciole)","410 g",0.410,2.82,16,V,"Solo con la Carta Insieme Conad. Senza tessera 3,15, cioè 7,69 al kg."),
 ("Biscotti","Conad","conad24","Colazione","Biscotti Il Granturchese Colussi, classici","800 g",0.800,2.99,16,V,"Solo con la Carta Insieme Conad. Senza tessera 3,45, cioè 4,32 al kg."),
 ("Marmellata","Conad","conad24","Colazione","Confettura light Hero senza zuccheri aggiunti, vari tipi","280 g",0.280,1.95,16,V,"Solo con la Carta Insieme Conad. Senza tessera 2,19, cioè 7,83 al kg."),
 ("Cereali","Conad","conad24","Colazione","Muesli alla frutta biologico Conad Verso Natura","375 g",0.375,2.85,16,V,"Solo con la Carta Insieme Conad. Senza tessera 3,19, cioè 8,51 al kg."),
 ("Biscotti","Conad","conad24","Colazione","Biscotti Ringo Pavesi, vari tipi, 6 porzioni","330 g",0.330,2.49,16,V,"Solo con la Carta Insieme Conad. Senza tessera 2,89, cioè 8,76 al kg."),
 ("Merendine","Conad","conad24","Colazione","Pandorì Bauli, vari tipi (per esempio classici)","150 g",0.150,1.77,16,V,"Solo con la Carta Insieme Conad. Sconto del 20%: senza tessera 2,22, cioè 14,80 al kg."),
 # pagina 16: la linea Mellin (omogeneizzati) non ha una categoria nel catalogo
 ("Acqua","Conad","conad24","Bevande","Acqua minerale Sant'Anna, naturale o frizzante","1,5 litri",1.5,0.35,17,V,"Solo con la Carta Insieme Conad. Senza tessera 0,54, cioè 0,36 al litro."),
 ("Birra","Conad","conad24","Bevande","Birra 11 Paralleli Conad, bionda","990 ml (3 × 330 ml)",0.990,2.10,17,V,"Solo con la Carta Insieme Conad. Senza tessera 2,40, cioè 2,43 al litro."),
 ("Vino","Conad","conad24","Bevande","Vermentino di Gallura DOCG Aghera Sarda","750 ml",0.750,6.90,17,V,"Solo con la Carta Insieme Conad. Senza tessera 8,70, cioè 11,60 al litro."),
 ("Acqua","Conad","conad24","Bevande","Acqua minerale naturale Uliveto","1,5 litri",1.5,0.45,17,V,"Solo con la Carta Insieme Conad. Senza tessera 0,59, cioè 0,40 al litro."),
 ("Bibite","Conad","conad24","Bevande","Bevanda alla frutta Vit Conad, vari tipi","1,5 litri",1.5,1.54,17,V,"«Bassi e fissi». Il volantino stampa 1,03 al litro."),
 ("Vino","Conad","conad24","Bevande","Aglianico del Vulture DOP Balì","750 ml",0.750,4.30,17,V,"«Bassi e fissi». Il volantino stampa 5,74 al litro."),
 ("Bibite","Conad","conad24","Bevande","Bevanda 100% a base di frutta Yoga, vari tipi","1 litro",1,1.55,17,V,"Solo con la Carta Insieme Conad. Senza tessera 1,75."),
 ("Birra","Conad","conad24","Bevande","Birra Bavaria","660 ml",0.660,1.09,17,V,"Solo con la Carta Insieme Conad. Senza tessera 1,29, cioè 1,96 al litro."),
 ("Vino","Conad","conad24","Bevande","Barbera del Monferrato DOC, Monferrato DOC Dolcetto Capetta","1,5 litri",1.5,4.90,17,V,"Solo con la Carta Insieme Conad. Senza tessera 6,20, cioè 4,14 al litro."),
 # pagina 17: patatine San Carlo e snack Conad non hanno una categoria nel catalogo
 ("Bagnoschiuma","Conad","conad24","Igiene","Bagnodoccia Palmolive, vari tipi","500 ml",0.500,2.24,18,V,"Solo con la Carta Insieme Conad. Sconto del 30%: senza tessera 3,20, cioè 6,40 al litro."),
 ("Carta igienica","Conad","conad24","Cura casa","Carta igienica La Maxi Scottex","4 rotoli maxi",4,2.99,18,V,"Solo con la Carta Insieme Conad. Senza tessera 3,99. Sulla confezione c'è scritto che 4 maxi valgono 12 rotoli normali: il conto è sui 4 rotoli veri."),
 # pagina 18: dentifricio Oral-B solo a sconto del 40% senza prezzo stampato;
 # deodoranti, detergenti intimi, assorbenti, pannolini, shampoo Restivoil a solo sconto,
 # salvaslip, traverse e fazzoletti non hanno una categoria nel catalogo
 ("Asciugatutto","Conad","conad24","Cura casa","Carta da cucina Quanto Basta Scottex","2 maxi rotoli",2,2.19,19,V,"Solo con la Carta Insieme Conad. Sconto del 40%: senza tessera 3,66."),
 ("Carta igienica","Conad","conad24","Cura casa","Carta igienica Conad salvaspazio","10 rotoli",10,2.79,19,V,"«Bassi e fissi»."),
 # pagina 19: cibo per animali, sementi, terriccio, macchina del caffè e aspirapolveri non hanno una categoria nel catalogo
 ("Lavatrice","Conad","conad24","Cura casa","Detersivo liquido per lavatrice ACE, vari tipi","1,9 litri, 38 lavaggi",38,3.24,20,V,"Solo con la Carta Insieme Conad. Sconto del 50%: senza tessera 6,49, cioè 0,17 a lavaggio. Il volantino stampa 0,09 a lavaggio."),
 ("Lavastoviglie","Conad","conad24","Cura casa","Detersivo per lavastoviglie Tutto in 1 Pril, gel (3 × 1,89 litri) o caps","76 lavaggi",76,8.99,20,V,"Solo con la Carta Insieme Conad. Senza tessera 16,99. Stesso prezzo per il gel da 105 lavaggi (3 flaconi da 35) o le 76 caps: il conto è sulle caps, che sono di meno."),
 # pagina 20: detergenti per la casa (Winni's, Napisan, Calgon, candeggina, Pronto, Smac, Quasar...) non hanno una categoria nel catalogo
 ("Asciugatutto","Conad","conad24","Cura casa","Asciugatutto superfici lucide Conad, extra large, 100 strappi","1 rotolo",1,1.99,21,V,"«Bassi e fissi». È per vetri e superfici lucide."),
 # pagina 21: detergenti, panni, guanti, scope e deodoranti per ambienti non hanno una categoria nel catalogo
 ("Verdure surgelate","Conad","conad24","Surgelati","Minestrone Tradizione Findus","1 kg",1,2.99,24,V,"Solo con la Carta Insieme Conad. Senza tessera 3,99."),
 ("Verdure surgelate","Conad","conad24","Surgelati","Piselli novelli Findus","1 kg",1,3.89,24,V,"Solo con la Carta Insieme Conad. Senza tessera 4,79."),
 ("Pesce","Conad","conad24","Surgelati","Burger Findus, vari tipi (per esempio di salmone con limone e aneto), 2 pezzi","170 g",0.170,3.49,24,V,"Solo con la Carta Insieme Conad. Sconto del 30%: senza tessera 4,99, cioè 29,36 al kg. Il volantino stampa 20,53 al kg."),
 # pagina 24: le vellutate Cremosa Findus non hanno una categoria nel catalogo. In fondo l'elenco dei
 # negozi in cui vale: per Torino c'è anche via Cesana 78, il nostro.
]

# LE OFFERTE CON DATE LORO.
# Quasi tutte le offerte durano quanto il volantino che le contiene. Alcune no:
# nel volantino MD dell'8-20 settembre c'è una pagina «Weekend più uno» valida
# solo dal 18 al 21. Metterla con le altre vorrebbe dire dire a Manlio che quel
# prezzo vale da lunedì, e mandarlo in negozio a prenderlo. L'avevo risolta
# saltando la pagina; il 2026-09-05 lui ha chiesto di farlo per bene.
#
# Quindi una riga può avere DUE CAMPI IN PIÙ in fondo, primo e ultimo giorno.
# Le righe senza restano come sono: la namedtuple ci mette i valori vuoti da
# sola, e nessuna delle 230 righe già scritte è stata toccata.
Offerta = _nt('Offerta', 'cat ins chiave rep pro fmt qta prezzo pag fonte note inizio fino')
Offerta.__new__.__defaults__ = (None, None)

# LE DATE DI UN'OFFERTA SI SCRIVONO SOLO SE DIVERSE DA QUELLE DEL VOLANTINO.
# Il 2026-09-05 ho scritto a mano su 22 righe dell'Eurospin nuovo le stesse date
# del volantino che le contiene. Sembrava innocuo ed era il contrario: la pagina
# legge «ha date sue» come «offerta ristretta», e un'offerta ristretta non ancora
# cominciata NON SI MOSTRA — servirebbe a non mandare Manlio a chiedere un
# prezzo che vale solo tre giorni. Cosi i gamberi e i bastoncini di merluzzo
# appena aggiunti erano invisibili, senza che niente segnalasse il guasto.
# Le date qui servono SOLO al caso vero: la pagina «Weekend piu uno» dell'MD,
# valida dal 18 al 21 dentro un volantino che va dall'8 al 20.
_perdata = {v.chiave: (v.inizio, v.fino) for v in VOLANTINI}
for _p in PRODOTTI:
    if len(_p) > 11:
        _ini, _fin = _p[11], _p[12] if len(_p) > 12 else None
        if (_ini, _fin) == _perdata.get(_p[2]):
            raise SystemExit('date inutili (sono quelle del volantino): ' + _p[4])

# NIENTE RIGHE DOPPIE. Il 2026-09-05, rileggendo i volantini in cerca del pesce,
# dieci prodotti del Carrefour sono stati riscritti da capo: li avevo gia letti
# in una sessione precedente e non me n'ero accorto. I prezzi combaciavano tutti
# — la rilettura confermava la prima — ma nell'elenco la stessa offerta compariva
# due volte, e chi guarda pensa che siano due negozi.
# Si confronta insegna + prodotto + formato, non la riga intera: due righe che
# dicono la stessa cosa con una nota diversa restano un doppione.
_visti = {}
for _p in PRODOTTI:
    _k = (_p[1], _p[4], _p[5])
    if _k in _visti:
        raise SystemExit('riga doppia: ' + ' / '.join(_k))
    _visti[_k] = True

# Ogni prezzo deve stare in una categoria che esiste nel catalogo: se no la
# pagina lo carica e non lo mostra a nessuno, in silenzio.
_orfani = sorted({p[0] for p in PRODOTTI} - set(NOMI))
if _orfani:
    raise SystemExit('categorie che non stanno nel catalogo: ' + ', '.join(_orfani))

# Dentro ogni categoria, dal meno caro per unità. Fra categorie, l'ordine del
# catalogo, cioè quello dei reparti del negozio.
PRODOTTI.sort(key=lambda p: (NOMI.index(p[0]), p[7] / p[6]))

# Da qui in poi si lavora su OFFERTE, coi nomi dei campi. PRODOTTI resta come
# lista di tuple perché è così che si scrive a mano leggendo i volantini: 230
# righe con undici nomi di campo l'una sarebbero illeggibili.
OFFERTE = [Offerta(*r) for r in PRODOTTI]
