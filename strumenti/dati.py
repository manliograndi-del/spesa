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
from pagine_mercato import PAGINE_MERCATO

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

VOLANTINI = [
 _v('mercato',        'Mercatò',        'dal 3 al 16 settembre',                        'Mercatò — 3-16 settembre.pdf',                     '2026-09-16', None, None, PAGINE_MERCATO),
 _v('lidl',           'Lidl',           'dal 3 al 9 settembre (sottocosto fino al 12)', 'Lidl — 3-9 settembre.pdf',                          '2026-09-12', _AV + '/2026/08/volantino-lidl-2026-09-03-p-{n:02d}.jpg'),
 _v('eurospin',       'Eurospin',       'dal 24 agosto al 6 settembre',                 'Eurospin — 24 agosto-6 settembre.pdf',              '2026-09-06', _AV + '/2026/08/volantino-eurospin-2026-08-24-p-{n:02d}.jpg'),
 _v('md',             'MD',             'dal 25 agosto al 6 settembre',                 'MD — 25 agosto-6 settembre.pdf',                    '2026-09-06', _AV + '/2026/08/volantino-md-2026-08-25-p-{n:02d}.jpg'),
 _v('bennet',         'Bennet',         'dal 27 agosto al 9 settembre',                 'Bennet — 27 agosto-9 settembre.pdf',                '2026-09-09', _AV + '/2026/08/volantino-bennet-2026-08-27-p-{n:05d}.jpg'),
 _v('ipercoop',       'Ipercoop',       'Sottocosto, dal 31 agosto al 9 settembre',     'Ipercoop Sottocosto — 31 agosto-9 settembre.pdf',   '2026-09-09', _VP + '/2/8/4/8/0/pagine/{n}.jpg'),
 _v('ipercoop_extra', 'Ipercoop',       'Extra offerte, dal 27 agosto al 9 settembre',  'Ipercoop Extra offerte — 27 agosto-9 settembre.pdf','2026-09-09', _VP + '/2/8/4/5/1/pagine/{n}.jpg'),
 _v('carriper04',     'Carrefour Iper', 'dal 4 settembre (fine stimata)',               'Carrefour Iper — dal 4 settembre.pdf',              '2026-09-17', _AV + '/2026/09/volantino-carrefour-iper-2026-09-04-p-{n:05d}.jpg'),

 # In arrivo: letti in anticipo, con la data d'inizio. Fino a quel giorno la
 # pagina li segna «dal ...» invece di farli passare per offerte di oggi.
 _v('eurospin10',     'Eurospin',       'dal 10 al 20 settembre',                       'Eurospin — 10-20 settembre.pdf',                    '2026-09-20', _AV + '/2026/09/volantino-eurospin-2026-09-10-p-{n:02d}.jpg', '2026-09-10'),
 _v('md08',           'MD',             "dall'8 al 20 settembre",                       'MD — 8-20 settembre.pdf',                          '2026-09-20', _AV + '/2026/09/volantino-md-2026-09-08-p-{n:02d}.jpg',       '2026-09-08'),
]

PRODOTTI = [
 # ------------------------------- CARNE DI BUE (kg) -------------------------------
 ("Carne di bue","MD","md08","Macelleria","Hamburger di Angus – Mister Meat","180 g",0.180,3.79,35,V,"Vale solo dal 18 al 21 settembre («Weekend più uno»), non per tutto il volantino. Carne 100% irlandese. Il volantino stampa 21,06 al kg.","2026-09-18","2026-09-21"),
 ("Carne di bue","Carrefour Iper","carriper04","Surgelati","4 hamburger classici – 1934","400 g",0.400,4.59,18,V,"Surgelati. −23%, prima 5,97. Solo con la tessera SpesAmica Payback."),
 ("Carne di bue","MD","md08","Macelleria","Hamburger di suino e bovino","al kg",1,10.90,9,V,"È misto suino e bovino, non solo bue."),
 ("Carne di bue","Eurospin","eurospin10","Macelleria","Spalla e reale a fette di bovino adulto","al kg",1,13.99,13,V,""),
 ("Carne di bue","MD","md08","Macelleria","Polpa scelta per roastbeef di bovino adulto","al kg",1,15.90,9,V,""),
 ("Bresaola","Eurospin","eurospin10","Salumi","Bresaola punta d'anca","80 g",0.080,2.19,5,V,"Prima 2,99. È bresaola, salume di bovino: il prezzo al chilo non si confronta con la carne fresca."),
 ("Carne di bue","Carrefour Iper","carriper04","Macelleria","Fettine di bovino adulto","al kg, almeno 1 kg",1,12.99,10,V,"«Prendi Spendi»: 12,99 al kg da 1 kg in su. Sotto il chilo 14,99. Prima 19,99."),
 ("Carne di bue","MD","md","Surgelati","10 hamburger di bovino – Le Specialità di Beppe","750 g",0.750,4.99,3,V,"Surgelato. Il volantino stampa 6,65 al kg."),
 ("Carne di bue","Eurospin","eurospin","Macelleria","Macinato per ragù di bovino adulto","Confezione Famiglia, al kg",1,8.99,11,V,"È la confezione grande, il prezzo è già al chilo."),
 ("Carne di bue","Lidl","lidl","Macelleria","Macinato di bovino adulto Scottona","400 g",0.400,4.49,16,V,"Prima 5,99. Il volantino stampa 11,23 al kg."),
 ("Carne di bue","Bennet","bennet","Surgelati","4 hamburger di carne bovina con bacon – Montana","400 g",0.400,4.79,10,V,"Surgelato, −20%, prima 5,99."),
 ("Carne di bue","Ipercoop","ipercoop_extra","Macelleria","Macinato di bovino – Fattorie Natura","800 g",0.800,9.90,14,V,"PREZZO SOCI (−20%). Senza tessera 12,38, cioè 15,48 al kg."),
 ("Carne di bue","Eurospin","eurospin","Macelleria","Maxi hamburger di scottona","200 g",0.200,2.49,11,V,"Il volantino stampa 12,45 al kg."),
 ("Carne di bue","Lidl","lidl","Macelleria","Rollata di bovino allo speck","600 g",0.600,7.99,16,V,"Attenzione: 7,99 è il prezzo della confezione, non al chilo."),
 ("Carne di bue","Bennet","bennet","Macelleria","Fettine di bovino adulto","al kg",1,13.99,None,D,"Sottocosto Freschi."),
 ("Carne di bue","Ipercoop","ipercoop_extra","Macelleria","Fettine di reale di bovino adulto – Fattorie Natura","al kg",1,16.38,14,V,"Etichetta «Conviene»."),
 ("Carne di bue","Eurospin","eurospin","Macelleria","Fettine sottili di bovino adulto","al kg",1,17.99,11,V,""),
 # ------------------------------- TONNO (kg) -------------------------------
 ("Tonno","MD","md08","Dispensa","Tonno al naturale – Poseidon","240 g (3 × 80 g)",0.240,1.69,12,V,"Solo con la MD Buona Spesa Card. Senza tessera 1,99, cioè 8,29 al kg. È al naturale, non all'olio."),
 ("Tonno","Eurospin","eurospin10","Dispensa","Tonno all'olio di oliva pinna gialla – Ondina","960 g (12 × 80 g)",0.960,7.49,1,V,"Prima 10,99. Quantità limitata. Confezione grande."),
 ("Tonno","MD","md08","Freschi","Tonno o pesce spada affumicato – Fish Fine","100 g",0.100,3.49,4,V,"Prima 3,99. È affumicato al banco, e la confezione può essere pesce spada."),
 ("Tonno","Carrefour Iper","carriper04","Dispensa","Tonno in olio di oliva Filo d'olio – Mare Aperto","360 g (6 × 60 g)",0.360,3.99,25,V,"Sottocosto −50%, prima 7,99. Solo con la tessera SpesAmica Payback."),
 ("Tonno","Carrefour Iper","carriper04","Dispensa","Tonno pinne gialle in olio di girasole – Maruzzella","480 g (6 × 80 g)",0.480,4.99,25,V,"−44%, prima 8,92. Solo con la tessera SpesAmica Payback. Confezione grande."),
 ("Tonno","Carrefour Iper","carriper04","Dispensa","Filetti di tonno all'olio di oliva – Nostromo","180 g",0.180,2.99,25,V,"−38%, prima 4,83. Solo con la tessera SpesAmica Payback."),
 ("Tonno","Carrefour Iper","carriper04","Pescheria","Trancio di tonno pinne gialle","al kg",1,17.90,11,V,"−30%, prima 25,90. È tonno fresco decongelato al banco, non in scatola."),
 ("Tonno","Bennet","bennet","Dispensa","Tonno all'olio di oliva – Flotta Azzurra","840 g (12 × 70 g)",0.840,7.48,12,V,"−30%, prima 10,69. Confezione grande."),
 ("Tonno","MD","md","Dispensa","Tonno all'olio d'oliva – Poseidon","840 g (12 × 70 g)",0.840,7.79,1,V,"Prima 9,49. Confezione grande."),
 ("Tonno","Carrefour Iper","carriper04","Dispensa","Tonno all'olio di oliva – Rio Mare","960 g (12 × 80 g)",0.960,10.45,4,V,"Sottocosto −47%, prima 19,73. Confezione grande."),
 ("Tonno","Eurospin","eurospin","Dispensa","Filetti di tonno all'olio di oliva pinna gialla – Ondina","260 g",0.260,2.99,6,V,"Prima 4,29. Barattolo di vetro."),
 ("Tonno","Lidl","lidl","Sottocosto","Tonno in olio di oliva – Rio Mare","780 g (12 × 65 g)",0.780,9.99,1,V,"Sgocciolato fa 16,01 al kg. Sottocosto fino al 12 settembre."),
 ("Tonno","Ipercoop","ipercoop","Dispensa","Tonno Yellowfin in olio di oliva – Rio Mare","780 g (12 × 65 g)",0.780,10.89,3,V,"Sottocosto −30%, prima 15,57. Stesso pacco del Lidl, ma più caro."),
 ("Tonno","Bennet","bennet","Dispensa","Filetti di tonno – Rio Mare","250 g",0.250,4.99,12,V,"−40%, prima 8,32."),
 ("Tonno","Bennet","bennet","Dispensa","Tonno in olio – Consorcio","175 g",0.175,3.99,12,V,"−50%, ma solo con la tessera Bennet Club."),
 # ------------------------------- SALMONE (kg) -------------------------------
 ("Salmone","Eurospin","eurospin10","Dispensa","Filetti di salmone al naturale – Ondina","150 g, sgocciolati 100 g",0.100,2.39,6,V,"Prima 3,19. È in scatola. Il volantino conta i 100 g sgocciolati: 23,90 al kg."),
 ("Salmone","Carrefour Iper","carriper04","Pescheria","Salmone affumicato Essential – Mowi","50 g",0.050,1.99,11,V,"Sottocosto −50%, prima 3,98. Il volantino stampa 39,80 al kg."),
 ("Salmone","Bennet","bennet","Pescheria","Filetto di salmone","al kg",1,17.69,None,D,"Sottocosto in copertina. Non valido nel Bennet di Alessandria."),
 ("Salmone","Lidl","lidl","Pesce","Filetto di salmone con pelle – Gastronomia di Mare","500 g",0.500,8.99,17,V,"Solo con carta Lidl Plus. Senza carta 10,49, cioè 20,98 al kg."),
 ("Salmone","Ipercoop","ipercoop","Freschi","Salmone scozzese affumicato – Icelander","100 g",0.100,1.99,4,V,"Sottocosto −50%, prima 3,98. Max 6 confezioni."),
 ("Salmone","MD","md","Freschi","Salmone affumicato","200 g",0.200,3.99,1,V,"Prima 5,49. Il volantino stampa 19,95 al kg."),
 ("Salmone","Ipercoop","ipercoop_extra","Freschi","Sashimi di salmone affumicato – Gimar","140 g",0.140,6.67,14,V,"PREZZO SOCI (−25%). Senza tessera 8,90, cioè 63,58 al kg."),
 # ------------------------------- CAFFÈ (kg) -------------------------------
 ("Caffè","Ipercoop","ipercoop","Dispensa","Caffè macinato Crema e Gusto – Lavazza","1 kg (4 × 250 g)",1,9.90,2,V,"Sottocosto −50%, prima 19,90. Max 3 confezioni."),
 ("Caffè","Ipercoop","ipercoop_extra","Dispensa","Caffè macinato per moka classico – Illy","250 g",0.250,5.69,6,V,"Etichetta «Conviene»."),
 ("Caffè","Eurospin","eurospin","Colazione","Capsule caffè espresso/cortado – Don Jerez","100 g, compatibili Dolce Gusto",0.100,2.59,3,V,"Prima 3,59. Sono capsule: al chilo costano molto più del macinato."),
 ("Caffè","Ipercoop","ipercoop_extra","Dispensa","Capsule compatibili Nespresso – Starbucks","57 g",0.057,2.99,6,V,"Capsule."),
 ("Caffè","Ipercoop","ipercoop_extra","Dispensa","Caffè solubile Gold – Nescafé","100 g",0.100,5.49,6,V,"PREZZO SOCI. È solubile, non macinato."),
 # ------------------------------- LATTE (litri) -------------------------------
 ("Latte","MD","md","Dispensa","Valigetta latte parzialmente scremato – Malga Paradiso","6 litri (6 × 1 l)",6,4.19,1,V,"Prima 5,10. Il volantino stampa 0,70 al litro."),
 ("Latte","Lidl","lidl","Sottocosto","Latte UHT Bontà e Leggerezza 1,2% – Parmalat","1 litro",1,0.79,1,V,"Sottocosto fino al 12 settembre."),
 ("Latte","Ipercoop","ipercoop","Dispensa","Latte UHT parzialmente scremato – Granarolo","4 litri (4 × 1 l)",4,3.99,4,V,"Sottocosto −49%, prima 7,96. Max 6 confezioni."),
 # ------------------------------- PASTA (kg) -------------------------------
 ("Pasta","Lidl","lidl","Sottocosto","Tortellini al prosciutto crudo – Fini","250 g",0.250,0.99,4,V,"Sottocosto fino al 12 settembre. Pasta fresca."),
 ("Pasta","Carrefour Iper","carriper04","Dispensa","Pasta di semola Al Bronzo – Barilla","500 g",0.500,0.79,23,V,"−38%, prima 1,29. Solo con la tessera SpesAmica Payback."),
 ("Pasta","Ipercoop","ipercoop","Dispensa","Pasta di semola formati classici – Barilla","500 g",0.500,0.48,3,V,"Sottocosto −50%, prima 0,97. Max 20 confezioni."),
 ("Pasta","MD","md","Freschi","Pasta fresca orecchiette o trofie – Ca' Bianca","1 kg",1,1.29,3,V,"Prima 1,99."),
 ("Pasta","MD","md","Freschi","Pasta sfoglia rettangolare","550 g (2 × 275 g)",0.550,1.69,3,V,"Prima 2,69."),
 ("Pasta","Bennet","bennet","Freschi","Gnocchetti freschi – Patamore","500 g",0.500,1.78,8,V,"−40%, prima 2,98."),
 ("Pasta","Bennet","bennet","Freschi","Pasta fresca all'uovo – Bennet","250 g",0.250,0.96,8,V,"−35% con la tessera Bennet Club."),
 ("Pasta","Ipercoop","ipercoop","Freschi","Pasta fresca ripiena Antica Bottega – Fini","250 g",0.250,1.79,4,V,"Sottocosto −51%, prima 3,69."),
 ("Pasta","Bennet","bennet","Freschi","Pasta fresca ripiena Sfogliagrezza – Giovanni Rana","250 g",0.250,2.59,8,V,"−35%, prima 3,99."),
 # ------------------------------- OLIO D'OLIVA (litri) -------------------------------
 ("Olio d'oliva","Eurospin","eurospin10","Dispensa","Olio extra vergine di oliva Fruttato o Fruttato Leggero – Frantoio La Rocca","1 litro",1,4.49,6,V,"Prima 5,99."),
 ("Olio d'oliva","Carrefour Iper","carriper04","Dispensa","Olio extravergine di oliva Terre Antiche – Dante","1 litro",1,3.89,4,V,"Sottocosto −57%, prima 9,05."),
 ("Olio d'oliva","Ipercoop","ipercoop","Dispensa","Olio extravergine di oliva Classico – Monini","1 litro",1,4.59,3,V,"Sottocosto −51%, prima 9,49. Max 4 confezioni."),
 ("Olio d'oliva","Bennet","bennet","Dispensa","Olio extravergine di oliva grezzo Il Casolare – Farchioni","1 litro",1,7.99,12,V,"−33%, prima 11,93."),
 # ------------------------------- POLLO (kg) -------------------------------
 ("Pollo","Bennet","bennet","Surgelati","Ortaiola con spinaci – Amadori","300 g",0.300,2.47,10,V,"Surgelata. −33%, prima 3,69."),
 ("Pollo","MD","md08","Freschi","Würstel di pollo e tacchino – La Fattoria","1 kg",1,2.29,35,V,"Vale solo dal 18 al 21 settembre («Weekend più uno»), non per tutto il volantino. Prima 2,59. Senza glutine.","2026-09-18","2026-09-21"),
 ("Pollo","Eurospin","eurospin10","Macelleria","Fusi e sovracosce di pollo","Confezione Famiglia, al kg",1,3.29,13,V,""),
 ("Pollo","MD","md08","Macelleria","Sovracosce di pollo","al kg",1,4.49,9,V,""),
 ("Pollo","MD","md08","Macelleria","Fuselli di pollo","al kg",1,4.49,9,V,""),
 ("Pollo","Eurospin","eurospin10","Gastronomia","Ali di pollo cotte piccanti","500 g",0.500,2.99,13,V,"Già cotte. Il volantino stampa 5,98 al kg."),
 ("Tacchino","Eurospin","eurospin10","Macelleria","Hamburger di tacchino","204 g",0.204,1.29,13,V,"È tacchino. Il volantino stampa 6,32 al kg."),
 ("Pollo","MD","md08","Surgelati","Spinacine classiche – AIA","500 g",0.500,4.99,9,V,"Il volantino stampa 9,98 al kg."),
 ("Pollo","MD","md08","Surgelati","Cordon bleu classico – AIA","490 g",0.490,4.99,9,V,"Il volantino stampa 10,18 al kg."),
 ("Pollo","Carrefour Iper","carriper04","Macelleria","Quarto posteriore di pollo – Aia","al kg",1,4.73,10,V,"−25%, prima 6,31."),
 ("Pollo","Carrefour Iper","carriper04","Macelleria","Filettini di pollo","al kg, almeno 3 kg",1,7.99,10,V,"«Prendi Spendi»: 7,99 al kg da 3 kg in su. Sotto i 3 kg 9,99. Prima 16,49."),
 ("Pollo","Carrefour Iper","carriper04","Macelleria","Linea Bon Roll – Aia","680 g",0.680,6.89,10,V,"−40%, prima 11,59. Il volantino stampa 10,14 al kg."),
 ("Pollo","Carrefour Iper","carriper04","Macelleria","Kebab di pollo – Aia","300 g",0.300,4.99,10,V,"−21%, prima 6,39. Il volantino stampa 16,64 al kg."),
 ("Pollo","Eurospin","eurospin","Macelleria","Cordon bleu di pollo e tacchino","490 g",0.490,1.99,11,V,"Il volantino stampa 4,06 al kg."),
 ("Pollo","Ipercoop","ipercoop_extra","Macelleria","Alette arrosto di pollo – Origine Coop","450 g",0.450,2.19,14,V,"Da polli allevati senza antibiotici."),
 ("Pollo","Lidl","lidl","Macelleria","Pollo allevato all'aperto Campese – Amadori","al kg",1,5.99,16,V,"Senza uso di antibiotici."),
 ("Pollo","MD","md","Surgelati","Nuggets di pollo – Tyson","1 kg",1,6.49,3,V,"Surgelato. Prima 7,99."),
 ("Pollo","Lidl","lidl","Macelleria","Petto di pollo intero","al kg",1,6.79,16,V,"−18%, prima 8,29."),
 ("Pollo","Eurospin","eurospin","Macelleria","Petto di pollo a fette","Confezione Famiglia, al kg",1,7.99,11,V,""),
 ("Pollo","Ipercoop","ipercoop_extra","Macelleria","Tagliata di petto di pollo SQ","400 g",0.400,3.73,14,V,"PREZZO SOCI (−25%). Senza tessera 4,98, cioè 12,45 al kg."),
 ("Pollo","Ipercoop","ipercoop_extra","Macelleria","Sottilissime di petto di pollo – AIA","al kg",1,12.54,14,V,"−30%, prima 17,92."),
 ("Pollo","Ipercoop","ipercoop_extra","Surgelati","La Viennese cotoletta di pollo – AIA","300 g",0.300,3.99,14,V,"Etichetta «Conviene»."),
 # ------------------------------- FORMAGGIO (kg) -------------------------------
 ("Mozzarella","MD","md08","Freschi","Formaggio a pasta filata (mozzarella)","1 kg",1,4.99,1,V,"Prima 6,89."),
 ("Mozzarella","Eurospin","eurospin10","Freschi","Ciliegine di mozzarella","150 g",0.150,0.99,5,V,"Prima 1,39. Latte 100% italiano."),
 ("Ricotta","MD","md08","Freschi","Ricotta bianca salata stagionata","al kg",1,6.99,4,V,"Prima 7,90. Speciale Sicilia."),
 ("Ricotta","MD","md08","Freschi","Ricotta al forno dura","al kg",1,7.39,4,V,"Prima 8,90. Speciale Sicilia."),
 ("Formaggio","MD","md08","Freschi","Formaggio canestrato tuma","al kg",1,8.99,4,V,"Prima 9,90. Speciale Sicilia."),
 ("Formaggio","MD","md08","Freschi","Formaggio pecoricco","al kg",1,8.99,4,V,"Prima 9,99. Speciale Sicilia."),
 ("Grana e parmigiano","Eurospin","eurospin10","Freschi","Grana Padano DOP","al kg",1,9.99,5,V,"Prima 13,29. Lo sconto del 25% si vede alla cassa."),
 ("Formaggio","MD","md08","Freschi","Formaggetta mista","al kg",1,9.99,4,V,"Prima 12,90. Speciale Sicilia."),
 ("Mozzarella","MD","md","Freschi","Mozzarelle in busta – Reggia","1 kg (8 × 125 g)",1,4.49,1,V,"Prima 5,49."),
 ("Formaggio","Ipercoop","ipercoop","Freschi","Sottilette Classiche","400 g",0.400,1.89,4,V,"Sottocosto −43%, prima 3,34."),
 ("Mozzarella","Ipercoop","ipercoop","Freschi","Mozzarella Santa Lucia – Galbani","375 g (3 × 125 g)",0.375,2.09,4,V,"Sottocosto −52%, prima 4,40."),
 ("Mozzarella","Lidl","lidl","Sottocosto","Mozzarella 100% latte italiano – Granarolo","375 g (3 × 125 g)",0.375,2.29,1,V,"Sottocosto fino al 12 settembre."),
 ("Formaggi spalmabili","Ipercoop","ipercoop","Freschi","Philadelphia formaggio fresco","350 g",0.350,2.19,4,V,"Sottocosto −39%, prima 3,64."),
 ("Ricotta","Bennet","bennet","Freschi","Mascarpone – Granarolo","500 g",0.500,3.58,8,V,"−40%, prima 5,97."),
 ("Grana e parmigiano","Ipercoop","ipercoop","Freschi","Grana Padano DOP 16 mesi – GranTerre","700 g",0.700,7.99,4,V,"Sottocosto −42%, prima 13,90. Max 3 confezioni."),
 ("Grana e parmigiano","Bennet","bennet","Freschi","Parmigiano Reggiano – Bennet","500 g",0.500,12.87,8,V,"−19% con la tessera Bennet Club."),
 # ------------------------------- UOVA (uova) -------------------------------
 ("Uova","Bennet","bennet","Freschi","10 uova fresche medie da allevamento a terra – Ovonovo","10 uova",10,2.99,8,V,"−25%, prima 3,99. È l'unica offerta sulle uova che ho trovato."),
 # ------------------------------- CARTA IGIENICA (rotoli) -------------------------------
 ("Carta igienica","Carrefour Iper","carriper04","Cura casa","Carta igienica Sensation Extra – Regina","4 rotoli",4,1.99,30,V,"−42%, prima 3,49."),
 ("Carta igienica","MD","md","Cura casa","4 rotoloni carta igienica – Regina","4 rotoloni, dichiarati pari a 12 rotoli",12,2.89,18,V,"Prima 3,29. Il conto al rotolo usa i 12 dichiarati sul pacco: sui 4 rotoloni veri fa 0,72 l'uno."),
 ("Carta igienica","Ipercoop","ipercoop","Cura casa","Carta igienica Scottonelle – Scottex","18 rotoli",18,4.99,5,V,"Sottocosto −50%, prima 9,98. Max 3 confezioni."),
 # ------------------------------- DETERSIVO (lavaggi) -------------------------------
 ("Ammorbidente","Ipercoop","ipercoop","Cura casa","Ammorbidente concentrato – Coccolino","87 lavaggi (1,827 l)",87,3.19,5,V,"Sottocosto −54%, prima 6,99. È ammorbidente, non detersivo: si usa in aggiunta."),
 ("Detersivo lavatrice","Ipercoop","ipercoop","Cura casa","Detersivo per lavatrice in polvere Power – Dash+","105 misurini (5,25 kg)",105,14.90,5,V,"Sottocosto −50%, prima 29,80. Max 2 confezioni."),
 ("Detersivo lavatrice","Ipercoop","ipercoop","Cura casa","Detersivo liquido per lavatrice Base – Dash","75 lavaggi (3 × 25)",75,10.90,5,V,"Sottocosto −50%, prima 21,80."),
 ("Detersivo lavastoviglie","Ipercoop","ipercoop","Cura casa","Detersivo per lavastoviglie Platinum Plus – Fairy","71 capsule",71,10.90,5,V,"Sottocosto −50%, prima 21,80. È per la lavastoviglie."),
 ("Detersivo lavatrice","MD","md","Cura casa","24 Fresh Caps 3 in 1 per lavatrice – Actiff","24 capsule",24,4.29,18,V,"Prima 4,89."),
 ("Detersivo lavatrice","MD","md","Cura casa","24 capsule per lavatrice bouquet floreale – DAT5","24 capsule",24,4.29,18,V,"Prima 4,99."),
 # ------------------------------- SUINO (kg) -------------------------------
 ("Suino","MD","md08","Macelleria","Cotolette o nodini di suino","al kg",1,6.90,9,V,""),
 ("Suino","Eurospin","eurospin10","Macelleria","Lonza o arista di suino a tranci","al kg",1,6.99,13,V,""),
 ("Salame","Eurospin","eurospin10","Salumi","Salame ungherese o Milano","150 g",0.150,1.15,5,V,"Prima 1,55. Solo con la tessera Eurospin Family."),
 ("Suino","Eurospin","eurospin10","Macelleria","Spiedini di suino","Confezione Famiglia, 1 kg",1,8.49,13,V,""),
 ("Pancetta e bacon","Eurospin","eurospin10","Salumi","Pancetta arrotolata","100 g",0.100,0.99,15,V,"Prima 1,29."),
 ("Pancetta e bacon","MD","md08","Salumi","Bacon a fette leggermente affumicato – La Fattoria","150 g",0.150,1.49,13,V,"Prima 1,69."),
 ("Suino","MD","md08","Macelleria","Involtini di suino","al kg",1,10.90,9,V,""),
 ("Prosciutto cotto","Eurospin","eurospin10","Salumi","Prosciutto cotto alta qualità 2% di grassi","150 g",0.150,1.69,1,V,"Quantità limitata."),
 ("Mortadella","Eurospin","eurospin10","Salumi","Mortadella Bologna IGP con pistacchio","120 g",0.120,1.59,5,V,"Prima 1,99."),
 ("Prosciutto cotto","Eurospin","eurospin10","Salumi","Prosciutto cotto alta qualità Praga","120 g",0.120,1.69,5,V,"Prima 1,99."),
 ("Prosciutto crudo","Eurospin","eurospin10","Salumi","Lonzino stagionato","120 g",0.120,1.99,5,V,"Prima 2,49."),
 ("Prosciutto cotto","MD","md08","Salumi","Prosciutto cotto nazionale selezione – La Fattoria","100 g",0.100,1.69,1,V,"Prima 2,59."),
 ("Salame","MD","md08","Salumi","Salame siciliano con pistacchio","80 g",0.080,1.79,4,V,"Prima 2,19."),
 ("Mortadella","MD","md08","Salumi","Mortadella di suino nero dei Nebrodi","80 g",0.080,2.39,4,V,"Prima 2,99."),
 ("Prosciutto crudo","Eurospin","eurospin10","Salumi","Prosciutto crudo stagionato 24 mesi","100 g",0.100,3.19,5,V,"Prima 3,99. Carne italiana."),
 ("Suino","Carrefour Iper","carriper04","Macelleria","Fettine di coscia di suino","al kg",1,5.99,10,V,"−40%, prima 9,99."),
 ("Suino","Carrefour Iper","carriper04","Macelleria","Spezzato di suino","al kg",1,5.99,10,V,"−33%, prima 8,99."),
 ("Salsiccia","Carrefour Iper","carriper04","Macelleria","Salamella di suino – confezione famiglia","al kg",1,7.99,10,V,"−20%, prima 9,99."),
 # Ci stanno sia i tagli freschi sia i salumi: sono tutti maiale, e il formato
 # di ogni riga dice cos'e. Se un domani vuole separarli, basta una categoria in piu.
 ("Salsiccia","Lidl","lidl","Macelleria","Bocconcini di salsiccia","250 g",0.250,1.69,16,V,"−21%, prima 2,15. Il volantino stampa 6,76 al kg."),
 ("Suino","Eurospin","eurospin","Macelleria","Braciole di coppa di suino","al kg",1,6.99,11,V,""),
 ("Suino","Lidl","lidl","Macelleria","Trancio di coppa di suino","al kg",1,6.99,16,V,"Novità."),
 ("Suino","Lidl","lidl","Macelleria","Sottilissime di lonza di suino","250 g",0.250,1.99,16,V,"−21% con la carta Lidl Plus, prima 2,55. Il volantino stampa 7,96 al kg."),
 ("Suino","Ipercoop","ipercoop_extra","Gastronomia","Polpettone Buona Domenica – Amadori","700 g",0.700,7.43,14,V,"PREZZO SOCI (−40%). Senza tessera 9,91, cioè 14,16 al kg."),
 ("Pancetta e bacon","Bennet","bennet","Salumi","Pancetta dolce o affumicata a cubetti – Fratelli Beretta","300 g (4 × 75 g)",0.300,3.98,8,V,"−30%, prima 5,69."),
 ("Prosciutto cotto","Ipercoop","ipercoop","Salumi","Prosciutto cotto Alta Qualità – Beretta","240 g (2 × 120 g)",0.240,3.29,4,V,"Sottocosto −52%, prima 6,98."),
 ("Salame","Ipercoop","ipercoop","Salumi","Salame Negronetto – Negroni","220 g",0.220,3.48,4,V,"Sottocosto −38%, prima 5,69."),
 ("Prosciutto crudo","Bennet","bennet","Salumi","Prosciutto crudo o cotto di alta qualità – Citterio","240 g (3 × 80 g)",0.240,4.99,8,V,"−50% con la tessera Bennet Club, prima 9,99."),
 ("Carne di bue","Ipercoop","ipercoop_extra","Gastronomia","Carne salada del Trentino per carpaccio","100 g",0.100,3.36,14,V,"PREZZO SOCI (−25%). Senza tessera 4,49, cioè 44,90 al kg."),
 # ------------------------------- BISCOTTI (kg) -------------------------------
 ("Biscotti","MD","md08","Colazione","Biscotti Oswego – Le Bon","500 g",0.500,1.39,35,V,"Vale solo dal 18 al 21 settembre («Weekend più uno»), non per tutto il volantino. Prima 1,69.","2026-09-18","2026-09-21"),
 ("Biscotti","Carrefour Iper","carriper04","Colazione","Grisbì gusti assortiti","135 g",0.135,0.99,23,V,"Sottocosto −55%, prima 2,20. Solo con la tessera SpesAmica Payback."),
 ("Biscotti","Carrefour Iper","carriper04","Colazione","Biscotto – Plasmon","720 g",0.720,4.99,23,V,"−33%, prima 7,46. Solo con la tessera SpesAmica Payback."),
 ("Biscotti","Eurospin","eurospin10","Colazione","Frollini con cacao e nocciole – Dolciando","700 g",0.700,1.69,6,V,"Prima 2,19. Senza olio di palma."),
 ("Biscotti","Eurospin","eurospin10","Colazione","Frollini con granelli di zucchero di canna","700 g",0.700,1.79,15,V,"Prima 2,19. Senza olio di palma."),
 ("Biscotti","Eurospin","eurospin10","Colazione","Frollini con gocce di cioccolato – Dolciando","1 kg",1,2.69,3,V,"Quantità limitata. Senza olio di palma."),
 ("Biscotti","MD","md08","Colazione","Frollini senza zuccheri aggiunti – Vivo Meglio","200 g",0.200,0.89,3,V,"Prima 1,49, sconto 40%."),
 ("Biscotti","Carrefour Iper","carriper04","Colazione","Biscotti Atene – Doria","500 g",0.500,0.99,21,V,"−40% con la tessera SpesAmica Payback, prima 1,65."),
 ("Biscotti","Eurospin","eurospin","Colazione","Frollini con panna","700 g",0.700,1.39,3,V,"Prima 1,89. Senza olio di palma."),
 ("Biscotti","Eurospin","eurospin","Colazione","Frollini all'uovo","700 g",0.700,1.49,3,V,"Prima 1,99."),
 ("Biscotti","Eurospin","eurospin","Colazione","Biscotti Digestive con avena e cioccolato","425 g",0.425,1.19,3,V,"Prima 1,59."),
 ("Biscotti","Ipercoop","ipercoop","Dispensa","Gocciole Chocolate – Pavesi","500 g",0.500,1.59,2,V,"Sottocosto −46%, prima 2,99. Max 6 confezioni."),
 ("Biscotti","Carrefour Iper","carriper04","Colazione","Plumcake Classico – Mulino Bianco","330 g",0.330,1.39,21,V,"−30%, prima 1,99."),
 ("Biscotti","Carrefour Iper","carriper04","Colazione","Frollini gusti assortiti – Colussi","273 g",0.273,1.19,21,V,"−40% con la tessera SpesAmica Payback, prima 1,99."),
 ("Biscotti","Ipercoop","ipercoop","Dispensa","Pan Gocciogli – Mulino Bianco","336 g (8 pezzi)",0.336,1.59,2,V,"Sottocosto −44%, prima 2,89."),
 ("Biscotti","Lidl","lidl","Colazione","Pangoccioli – Mulino Bianco","336 g (8 pezzi)",0.336,2.15,24,V,"−25%, prima 2,89. Stesso prodotto che l'Ipercoop fa a 1,59."),
 ("Biscotti","Ipercoop","ipercoop_extra","Dispensa","Biscotti Oro Ciok – Saiwa","250 g",0.250,1.79,6,V,"−40%, prima 2,99."),
 ("Biscotti","Ipercoop","ipercoop_extra","Dispensa","Millefoglie d'Italia – Vicenzi","125 g",0.125,0.93,6,V,"−25%, prima 1,25."),
 ("Biscotti","Ipercoop","ipercoop_extra","Dispensa","Pavesini – Pavesi","200 g",0.200,1.54,6,V,"−40%, prima 2,57."),
 ("Biscotti","Carrefour Iper","carriper04","Colazione","Nutella Biscuits","304 g",0.304,2.69,21,V,"−22% con la tessera SpesAmica Payback, prima 3,46."),
 # ------------------------------- YOGURT (kg) -------------------------------
 ("Yogurt","Lidl","lidl","Sottocosto","Yogurt intero alla frutta – Granarolo","1 kg (8 × 125 g)",1,1.99,4,V,"Sottocosto fino al 12 settembre."),
 ("Yogurt","MD","md08","Freschi","Yogurt intero bianco – Buona Spesa!","1 kg",1,1.99,13,V,"Prima 2,39. Secchiello da un chilo."),
 ("Yogurt","Eurospin","eurospin10","Freschi","Fermenti attivi da bere alla fragola o multifrutti","600 g (6 × 100 g)",0.600,1.49,5,V,"Prima 1,99. Sono da bere, non vasetti."),
 ("Yogurt","Eurospin","eurospin10","Freschi","Yogurt fragola o banana con confetti al cioccolato","110 g",0.110,0.49,5,V,"Prima 0,69. Solo con la tessera Eurospin Family."),
 ("Yogurt","MD","md08","Freschi","Yogurt proteico magro bianco – Milk Pro","180 g",0.180,1.00,18,V,"Prima 1,45. 20 g di proteine."),
 ("Yogurt","Ipercoop","ipercoop","Freschi","Yogurt intero gusti vari – Müller","1 kg (8 × 125 g)",1,1.99,4,V,"Sottocosto −55%, prima 4,49. Max 6 confezioni."),
 ("Yogurt","Carrefour Iper","carriper04","Freschi","Yogurt Fieno Fiordilatte","1 kg",1,2.19,21,V,"−35%, prima 3,39."),
 ("Yogurt","Carrefour Iper","carriper04","Freschi","Kefir bianco naturale – Sveltesse","500 g",0.500,1.29,16,V,"−31%, prima 1,89."),
 ("Yogurt","Carrefour Iper","carriper04","Freschi","Yogurt intero alle fragole – Yomo","250 g (2 × 125 g)",0.250,0.79,16,V,"−43%, prima 1,39."),
 ("Yogurt","Carrefour Iper","carriper04","Freschi","Yogurt 0% grassi – Activia","500 g (4 × 125 g)",0.500,1.99,16,V,"−28% con la tessera SpesAmica Payback, prima 2,77."),
 ("Yogurt","Carrefour Iper","carriper04","Freschi","Muu Muu al cioccolato – Cameo","460 g (4 pezzi)",0.460,1.99,16,V,"−39%, prima 3,29."),
 ("Yogurt","Carrefour Iper","carriper04","Freschi","Müller Mix gusti assortiti","140 g",0.140,0.69,16,V,"−44%, prima 1,25."),
 ("Yogurt","Bennet","bennet","Freschi","Kefir – Milk","150 g",0.150,0.83,8,V,"−30%, prima 1,19."),
 ("Yogurt","Carrefour Iper","carriper04","Freschi","Kefir gusti assortiti – Milk","160 g",0.160,0.99,16,V,"−31%, prima 1,45."),
 ("Yogurt","Carrefour Iper","carriper04","Freschi","Kefir bianco senza lattosio – Polenghi","500 ml",0.500,0.79,16,V,"−20%, prima 0,99. È da bere: mezzo litro pesa circa mezzo chilo, il confronto regge."),
 # ------------------------------- MARMELLATA (kg) -------------------------------
 ("Marmellata","Carrefour Iper","carriper04","Colazione","Confettura ai frutti di bosco senza zuccheri aggiunti","220 g",0.220,1.49,23,V,"−21%, prima 1,89. Solo con la tessera SpesAmica Payback."),
 ("Marmellata","MD","md08","Colazione","Confettura light ciliegia, albicocca, fragola o prugna – Vivo Meglio","310 g",0.310,1.59,3,V,"Prima 1,99. Con stevia."),
 ("Marmellata","Eurospin","eurospin10","Colazione","Confettura extra di lamponi – Alpenspitz","340 g",0.340,2.39,10,V,"Quantità limitata."),
 ("Marmellata","Eurospin","eurospin","Colazione","Confettura extra albicocca o ciliegia","370 g",0.370,1.29,3,V,"Prima 1,69."),
 ("Marmellata","Carrefour Iper","carriper04","Colazione","Confetture gusti assortiti – Terre d'Italia","340 g",0.340,2.69,21,V,"−21% con la tessera SpesAmica Payback, prima 3,41."),
 ("Marmellata","Ipercoop","ipercoop_extra","Colazione","Confetture Fiordifrutta – Rigoni di Asiago","330 g",0.330,3.45,6,V,"PREZZO SOCI. Bio, 100% da frutta."),
 ("Marmellata","Carrefour Iper","carriper04","Colazione","Confettura Zero Residui – Zuegg","230 g",0.230,2.49,21,V,"−22% con la tessera SpesAmica Payback, prima 3,20."),
 # ------------------------------- CIOCCOLATO (kg) -------------------------------
 ("Cioccolato","Carrefour Iper","carriper04","Dispensa","Tavolette gusti assortiti – Milka","250 g",0.250,3.95,23,V,""),
 ("Cioccolato","Carrefour Iper","carriper04","Dispensa","Tavolette Excellence 85% cacao – Lindt","100 g",0.100,2.89,23,V,"−20%, prima 3,62. Solo con la tessera SpesAmica Payback."),
 ("Cioccolato","Eurospin","eurospin","Colazione","Crema alla nocciola","750 g",0.750,2.79,3,V,"Prima 3,59. È una crema da spalmare, non una tavoletta."),
 ("Cioccolato","Ipercoop","ipercoop","Dispensa","Nutella – Ferrero","750 g",0.750,4.99,2,V,"Sottocosto −25%, prima 6,68. Crema da spalmare."),
 ("Cioccolato","Carrefour Iper","carriper04","Colazione","Nutella – Ferrero","950 g",0.950,6.89,21,V,"Crema da spalmare. Il barattolo grande."),
 ("Cioccolato","Lidl","lidl","Colazione","Gallette di riso al cioccolato – Sondey","100 g",0.100,1.29,24,V,"−23% con la carta Lidl Plus, prima 1,69."),
 ("Cioccolato","Lidl","lidl","Colazione","Bastoncini ricoperti di cioccolato – Sondey","90 g",0.090,1.29,24,V,"−23% con la carta Lidl Plus, prima 1,69. Fondente o al latte."),
 ("Cioccolato","Bennet","bennet","Dispensa","KitKat – Nestlé","124 g (conf. da 3)",0.124,2.29,12,V,"−30%, prima 3,28."),
 ("Cioccolato","Ipercoop","ipercoop_extra","Dispensa","Mini Tower Movie Night – Ritter Sport","150 g",0.150,2.89,6,V,"PREZZO SOCI."),
 ("Cioccolato","Bennet","bennet","Dispensa","Tavoletta cioccolato nero fondente extra – Perugina","85 g",0.085,1.98,12,V,"−25%, prima 2,65. Tavoletta vera, non crema."),
 # ------------------------------- MERLUZZO E BACCALÀ (kg) -------------------------------
 ("Merluzzo e baccalà","Carrefour Iper","carriper04","Surgelati","Polpette di pesce merluzzo dalla Norvegia – Frosta","240 g",0.240,3.99,18,V,"Surgelate. −20%, prima 4,99. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- RISO (kg) -------------------------------
 ("Riso","Eurospin","eurospin10","Dispensa","Riso Arborio","5 kg (5 × 1 kg)",5,6.96,3,V,"Quantità limitata. Riso italiano."),
 # ------------------------------- PANE (kg) -------------------------------
 ("Pane","Carrefour Iper","carriper04","Colazione","Pan Bauletto Bianco – Mulino Bianco","400 g",0.400,0.85,23,V,"−22%, prima 1,09. Solo con la tessera SpesAmica Payback."),
 ("Pane","Eurospin","eurospin10","Dispensa","Taralli multipack","500 g (10 × 50 g)",0.500,1.49,3,V,"Quantità limitata. Senza olio di palma."),
 ("Pane","Carrefour Iper","carriper04","Colazione","Piadelle Toast – Mulino Bianco","240 g",0.240,1.49,23,V,"−32%, prima 2,20. Solo con la tessera SpesAmica Payback."),
 ("Pane","Carrefour Iper","carriper04","Colazione","Gallette Bio mais o riso – Carrefour Bio","120 g",0.120,0.79,23,V,"−20%, prima 0,99. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- POMODORO E PASSATA (kg) -------------------------------
 ("Pomodoro e passata","Lidl","lidl","Sottocosto","Passata di pomodoro – Mutti","700 g",0.700,0.89,4,V,"Sottocosto fino al 12 settembre. 100% pomodoro italiano."),
 ("Pomodoro e passata","Eurospin","eurospin10","Dispensa","Polpa di pomodoro a pezzetti","2,4 kg (6 × 400 g)",2.4,2.49,3,V,"Quantità limitata. 100% pomodori italiani."),
 # ------------------------------- OLIO DI SEMI (litri) -------------------------------
 ("Olio di semi","MD","md08","Dispensa","Olio di semi vari – Semì","1 litro",1,1.55,35,V,"Vale solo dal 18 al 21 settembre («Weekend più uno»), non per tutto il volantino. Prima 1,79.","2026-09-18","2026-09-21"),
 ("Olio di semi","Eurospin","eurospin10","Dispensa","Olio di semi di girasole","5 litri",5,6.59,3,V,"Prima 7,75."),
 # ------------------------------- LEGUMI IN SCATOLA (kg) -------------------------------
 ("Legumi in scatola","Eurospin","eurospin10","Dispensa","Fagioli borlotti","6 × 400 g, sgocciolati 1,44 kg",1.44,1.99,3,V,"Quantità limitata. Il conto usa il peso sgocciolato."),
 # ------------------------------- SUGHI PRONTI (kg) -------------------------------
 ("Sughi pronti","Carrefour Iper","carriper04","Surgelati","Sugo pronto per spaghettata di mare – Esca","400 g",0.400,3.49,18,V,"Surgelato. −34%, prima 5,29. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- VERDURE IN SCATOLA (kg) -------------------------------
 ("Verdure in scatola","MD","md08","Dispensa","Mais, piselli e peperoni cotti a vapore – Buona Spesa!","420 g (3 × 140 g)",0.420,1.39,35,V,"Vale solo dal 18 al 21 settembre («Weekend più uno»), non per tutto il volantino. Prima 2,29.","2026-09-18","2026-09-21"),
 ("Verdure in scatola","Carrefour Iper","carriper04","Dispensa","Mais – Bonduelle","420 g (3 × 140 g)",0.420,1.99,23,V,"−45%, prima 3,62. Solo con la tessera SpesAmica Payback."),
 ("Verdure in scatola","Eurospin","eurospin10","Dispensa","Carciofini alla contadina sott'olio","535 g",0.535,1.99,3,V,"Quantità limitata."),
 ("Verdure in scatola","Carrefour Iper","carriper04","Dispensa","Funghetti interi – Polli","190 g",0.190,1.95,23,V,"−35%, prima 3,16. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- MERENDINE (kg) -------------------------------
 ("Merendine","Carrefour Iper","carriper04","Colazione","Panini con gocce di cioccolato","252 g",0.252,0.99,23,V,"−37%, prima 1,58. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- MIELE (kg) -------------------------------
 ("Miele","Carrefour Iper","carriper04","Dispensa","Miele millefiori","500 g",0.500,4.39,23,V,"−20%, prima 5,49. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- VERDURE SURGELATE (kg) -------------------------------
 ("Verdure surgelate","Bennet","bennet","Surgelati","Minestrone Leggerezza – Orogel","750 g",0.750,1.99,10,V,"−33%, prima 2,98."),
 ("Verdure surgelate","Bennet","bennet","Surgelati","Contorno colorato – Bennet","400 g",0.400,1.99,10,V,"−26%, prima 2,69. Solo con la tessera Bennet Club."),
 ("Verdure surgelate","Ipercoop","ipercoop_extra","Surgelati","Contorni ricette varie – La Valle degli Orti Frosta","400 g",0.400,1.99,19,V,"PREZZO SOCI Coop."),
 ("Verdure surgelate","Bennet","bennet","Surgelati","Zucchine grigliate – Bennet","450 g",0.450,2.39,10,V,"−20%, prima 2,99."),
 ("Verdure surgelate","Bennet","bennet","Surgelati","8 tortini di verdure – Frosta","240 g",0.240,1.79,10,V,"−28%, prima 2,49."),
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","Fagiolini e patate – Bonduelle","450 g",0.450,1.45,18,V,"−25%, prima 1,94. Solo con la tessera SpesAmica Payback."),
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","Piselli finissimi – La Valle degli Orti","850 g",0.850,2.99,18,V,"−28%, prima 4,16. Solo con la tessera SpesAmica Payback."),
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","Carciofi a spicchi – Orogel","300 g",0.300,2.39,18,V,"−36%, prima 3,74. Solo con la tessera SpesAmica Payback."),
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","Tortini spinaci o ortolano – Frosta","240 g",0.240,1.99,18,V,"−25%, prima 2,66. Solo con la tessera SpesAmica Payback."),
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","Funghi porcini a cubetti","300 g",0.300,3.99,18,V,"−20%, prima 4,99. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- PIZZA SURGELATA (kg) -------------------------------
 ("Pizza surgelata","Ipercoop","ipercoop_extra","Surgelati","Pizza margherita – gli Spesotti","885 g (3 pizze)",0.885,3.55,10,V,"Prezzo di tutti i giorni, non un'offerta a tempo. Il volantino stampa 4,01 al kg."),
 ("Pizza surgelata","MD","md08","Surgelati","Pizza ai funghi","375 g",0.375,1.79,12,V,"Solo con la MD Buona Spesa Card. Senza tessera 2,69, cioè 7,17 al kg."),
 ("Pizza surgelata","Eurospin","eurospin10","Surgelati","Pizza alle verdure","415 g",0.415,1.99,15,V,"Prima 2,49. Il volantino stampa 4,80 al kg."),
 ("Pizza surgelata","MD","md08","Surgelati","Pizza ai 4 formaggi","350 g",0.350,1.79,12,V,"Solo con la MD Buona Spesa Card. Senza tessera 2,89, cioè 8,26 al kg."),
 ("Pizza surgelata","Lidl","lidl","Sottocosto","Pizza Big Americans Supreme – Cameo","455 g",0.455,2.49,4,V,"Sottocosto fino al 12 settembre. Il volantino stampa 5,47 al kg."),
 ("Pizza surgelata","Bennet","bennet","Surgelati","Pizza tipi vari – Bennet","370 g",0.370,2.79,10,V,"−20%, prima 3,49. Solo con la tessera Bennet Club."),
 ("Pizza surgelata","Bennet","bennet","Surgelati","Mini pizzette margherita – Italpizza","360 g (4 × 90 g)",0.360,3.19,10,V,"−20%, prima 3,99."),
 ("Pizza surgelata","Carrefour Iper","carriper04","Surgelati","Pizza Bella Napoli farcite gusti assortiti – Buitoni","375 g",0.375,2.49,18,V,"−28%, prima 3,47. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- FRUTTA (kg) -------------------------------
 ("Frutta","MD","md08","Ortofrutta","Uva bianca in bauletto","2 kg",2,2.78,35,V,"Vale solo dal 18 al 21 settembre («Weekend più uno»), non per tutto il volantino. Il volantino stampa 1,39 al kg.","2026-09-18","2026-09-21"),
 ("Frutta","Carrefour Iper","carriper04","Ortofrutta","Banane sfuse – Chiquita","al kg",1,1.49,12,V,"−25%, prima 1,99."),
 ("Frutta","Carrefour Iper","carriper04","Ortofrutta","Uva bianca senza semi, sfusa","al kg",1,2.99,12,V,"−20%, prima 3,74. Prodotta in Italia."),
 # ------------------------------- VERDURA (kg) -------------------------------
 ("Verdura","Carrefour Iper","carriper04","Ortofrutta","Pomodoro datterino","250 g",0.250,0.99,12,V,"Prodotto in Italia. Il volantino stampa 3,96 al kg."),
 ("Verdura","Carrefour Iper","carriper04","Ortofrutta","Funghi champignon affettati","300 g",0.300,1.59,12,V,"−30%, prima 2,28. Prodotti in Italia."),
 # ------------------------------- INSALATA IN BUSTA (kg) -------------------------------
 ("Insalata in busta","Carrefour Iper","carriper04","Ortofrutta","Insalata Baby Iceberg – Vertical Farms","80 g, almeno 2 buste",0.080,1.29,12,V,"«Prendi Spendi»: 1,29 comprandone due o più, se no 1,59. Prima 1,99."),
 # ------------------------------- PATATE (kg) -------------------------------
 ("Patate","Ipercoop","ipercoop_extra","Surgelati","Patatine Golden Long – McCain","750 g",0.750,1.79,19,V,"Surgelate. Etichetta «Conviene»."),
 ("Patate","Carrefour Iper","carriper04","Ortofrutta","Patate","2 kg",2,1.78,12,V,"−30%. Il volantino stampa 0,89 al kg. Prodotte in Italia."),
 ("Patate","Carrefour Iper","carriper04","Surgelati","Patate Forno Country – McCain","650 g",0.650,1.99,18,V,"Surgelate. −35%, prima 3,07. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- ACQUA (litri) -------------------------------
 ("Acqua","MD","md08","Bevande","Acqua naturale – Sant'Anna","2 litri",2,0.45,35,V,"Vale solo dal 18 al 21 settembre («Weekend più uno»), non per tutto il volantino. Prima 0,65.","2026-09-18","2026-09-21"),
 ("Acqua","Carrefour Iper","carriper04","Bevande","Acqua naturale o frizzante – Vera","9 litri (6 × 1,5 l)",9,1.79,26,V,"−40%, prima 3,10. Solo con la tessera SpesAmica Payback."),
 ("Acqua","Carrefour Iper","carriper04","Bevande","Acqua effervescente naturale – Uliveto","9 litri (6 × 1,5 l)",9,2.49,26,V,"−33%, prima 3,78. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- VINO (litri) -------------------------------
 ("Vino","Carrefour Iper","carriper04","Bevande","Bonarda o Barbera Oltrepò Pavese DOC – Le Cascine","750 ml",0.750,1.99,26,V,"−56%, prima 4,54. Solo con la tessera SpesAmica Payback."),
 ("Vino","Carrefour Iper","carriper04","Bevande","Gutturnio DOC Colli Piacentini – Cantina Valtidone","750 ml",0.750,2.69,26,V,"−46%, prima 4,99. Solo con la tessera SpesAmica Payback."),
 ("Vino","Carrefour Iper","carriper04","Bevande","Linea vini – La Calenzana","750 ml",0.750,2.79,26,V,"−54%, prima 6,08. Solo con la tessera SpesAmica Payback. Abruzzo."),
 ("Vino","Carrefour Iper","carriper04","Bevande","Collezione Oro – Piccini","750 ml",0.750,3.99,26,V,"−50%, prima 7,99. Solo con la tessera SpesAmica Payback. Toscana."),
 ("Vino","Carrefour Iper","carriper04","Bevande","Valpolicella Superiore DOC Radole – Sartori","750 ml",0.750,5.99,26,V,"−24%, prima 7,89. Solo con la tessera SpesAmica Payback. Veneto."),
 ("Vino","Carrefour Iper","carriper04","Bevande","Franciacorta DOCG Millesimato Brut – Terre d'Italia","750 ml",0.750,14.50,26,V,"−22%, prima 18,59. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- BIRRA (litri) -------------------------------
 ("Birra","Lidl","lidl","Sottocosto","Birra Pils in lattina – Beck's","440 ml",0.440,0.75,4,V,"Sottocosto fino al 12 settembre."),
 ("Birra","Carrefour Iper","carriper04","Bevande","Birra – Peroni","1,98 litri (6 × 330 ml)",1.98,3.99,26,V,"−31%, prima 5,79. Solo con la tessera SpesAmica Payback."),
 ("Birra","Carrefour Iper","carriper04","Bevande","Birra Metodo Lento – Ichnusa","500 ml",0.500,1.09,26,V,"−31%, prima 1,59. Solo con la tessera SpesAmica Payback."),
 ("Birra","Carrefour Iper","carriper04","Bevande","Birra Cristalli di Sale – Messina","990 ml (3 × 330 ml)",0.990,2.99,26,V,"−25%, prima 3,99. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- SUCCHI E BIBITE (litri) -------------------------------
 ("Succhi e bibite","Carrefour Iper","carriper04","Bevande","Thè Linea Standard o Zero – Sant'Anna","1,5 litri",1.5,0.69,26,V,"−45%, prima 1,29. Solo con la tessera SpesAmica Payback."),
 ("Succhi e bibite","Carrefour Iper","carriper04","Bevande","Bibite gusti assortiti – Tomarchio","1,25 litri",1.25,0.79,26,V,"−25%, prima 1,09. Solo con la tessera SpesAmica Payback."),
 ("Succhi e bibite","Carrefour Iper","carriper04","Bevande","Coca Cola Regular o Zero Zuccheri","6 litri (4 × 1,5 l)",6,4.65,26,V,"−40%, prima 8,02. Solo con la tessera SpesAmica Payback."),
 ("Succhi e bibite","Carrefour Iper","carriper04","Bevande","Succhi di frutta senza zuccheri aggiunti – Skipper","1 litro",1,1.49,26,V,"−20%, prima 1,89. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- SAPONE E BAGNOSCHIUMA (litri) -------------------------------
 ("Sapone e bagnoschiuma","Carrefour Iper","carriper04","Cura persona","Bagnodoccia Dermazero – Neutro Roberts","900 ml (2 × 450 ml)",0.900,2.85,30,V,"−64%, prima 7,94. Solo con la tessera SpesAmica Payback."),
 ("Sapone e bagnoschiuma","Carrefour Iper","carriper04","Cura persona","Detergente intimo – Lactacyd","200 ml",0.200,2.39,30,V,"−26%, prima 3,24. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- DENTIFRICIO (litri) -------------------------------
 ("Dentifricio","Carrefour Iper","carriper04","Cura persona","Collutorio Denti e Gengive – Listerine","1 litro (2 × 500 ml)",1,4.99,30,V,"−58%, prima 11,89. È collutorio, non dentifricio. Solo con la tessera SpesAmica Payback."),
 ("Dentifricio","Carrefour Iper","carriper04","Cura persona","Dentifricio Microgranuli – Mentadent","225 ml (3 × 75 ml)",0.225,4.49,30,V,"−39%, prima 7,37. Solo con la tessera SpesAmica Payback."),
 ("Prosciutto crudo","Ipercoop","ipercoop_extra","Salumi","Prosciutto crudo stagionato – gli Spesotti","100 g",0.100,1.70,10,V,"Prezzo di tutti i giorni, non un'offerta a tempo."),
 # ------------------------------- BURRO (kg) -------------------------------
 ("Burro","Ipercoop","ipercoop_extra","Freschi","Burro – gli Spesotti","250 g",0.250,1.85,10,V,"Prezzo di tutti i giorni, non un'offerta a tempo. Il volantino stampa 7,40 al kg."),
 # ------------------------------- CALAMARI E SEPPIE (kg) -------------------------------
 ("Calamari e seppie","Ipercoop","ipercoop_extra","Surgelati","Anelli di totano – Pescanova","400 g",0.400,5.49,19,V,"Surgelati. PREZZO SOCI Coop."),
 # ------------------------------- BASTONCINI DI PESCE (kg) -------------------------------
 ("Bastoncini di pesce","Bennet","bennet","Surgelati","I Gratinati tipi vari – Capitan Findus","380 g",0.380,3.59,10,V,"−40%, prima 5,99. Solo con la tessera Bennet Club."),
 # ------------------------------- GELATO (kg) -------------------------------
 ("Gelato","Ipercoop","ipercoop_extra","Surgelati","Gelato Soft vaniglia e cacao o caramello – Algida","440 g",0.440,1.99,19,V,"Vaschetta. PREZZO SOCI Coop."),
 ("Gelato","Bennet","bennet","Surgelati","Gelato Soft vaniglia e cacao o caramello – Algida","440 g",0.440,1.99,10,V,"Vaschetta. −33%, prima 2,98."),
 ("Gelato","Ipercoop","ipercoop_extra","Surgelati","Gelato allo yogurt greco – Kri Kri","320 g",0.320,1.99,19,V,"Etichetta «Conviene»."),
 ("Gelato","Bennet","bennet","Surgelati","Cornetto Classico – Algida","480 g (8 pezzi)",0.480,2.99,10,V,"−58%, prima 7,14. Solo con la tessera Bennet Club."),
 ("Gelato","Ipercoop","ipercoop_extra","Surgelati","Coppa del Nonno","390 g (6 pezzi)",0.390,3.69,19,V,"Etichetta «Conviene»."),
 ("Gelato","Ipercoop","ipercoop_extra","Surgelati","Cucciolone – Algida","480 g (6 pezzi)",0.480,4.39,19,V,"PREZZO SOCI Coop."),
 ("Gelato","Bennet","bennet","Surgelati","Solero tipi vari – Algida","204 g (3 pezzi)",0.204,2.15,10,V,"−46%, prima 3,99."),
 ("Gelato","Ipercoop","ipercoop_extra","Surgelati","Nuii caramello salato e noci di Macadamia","272 g (4 pezzi)",0.272,3.79,19,V,"Etichetta «Conviene»."),
 ("Gelato","Ipercoop","ipercoop_extra","Surgelati","Mini Gruvi assortiti – Sammontana","225 g (6 pezzi)",0.225,3.29,19,V,"Sconto 40%, prima 5,49."),
 ("Gelato","Bennet","bennet","Surgelati","Mini Gruvi tipi vari – Sammontana","225 g (6 pezzi)",0.225,3.39,10,V,"−40%, prima 5,66. Solo con la tessera Bennet Club."),
 # ============================ MERCATÒ, 3-16 settembre ============================
 # Letto pagina per pagina il 2026-09-05, dal volantino «La convenienza migliore
 # dell'anno». La pagina scritta qui è quella STAMPATA in basso sul foglio.
 # «Solo con Fidelity Card» è nelle note dove il volantino lo dice: senza la
 # tessera quel prezzo non si paga, ed è un'informazione che serve in cassa.
 # I prezzi del banco sono stampati all'etto: qui stanno al chilo, come tutti
 # gli altri, così si confrontano davvero.
 ("Carne di bue","Mercatò","mercato","Macelleria","Arrosto di bovino adulto piemontese","al kg",1,20.39,22,V,""),
 ("Carne di bue","Mercatò","mercato","Macelleria","Carne tritata scelta di bovino adulto piemontese","al kg",1,17.99,22,V,"Per polpette e ragù."),
 ("Carne di bue","Mercatò","mercato","Macelleria","Burger di scottona – You&Meat","200 g",0.200,3.89,22,V,"Il volantino stampa 19,45 al kg."),
 ("Pollo","Mercatò","mercato","Macelleria","Coscette di pollo piemontese","al kg",1,6.99,22,V,""),
 ("Pollo","Mercatò","mercato","Macelleria","Petto di pollo","al kg",1,11.99,22,V,"Origine Italia."),
 ("Pollo","Mercatò","mercato","Macelleria","Involtino di pollo con speck e provola","al kg",1,15.79,22,V,""),
 ("Suino","Mercatò","mercato","Macelleria","Lonza di suino piemontese","al kg",1,9.89,22,V,""),
 ("Salsiccia","Mercatò","mercato","Macelleria","Salsiccia rustica piemontese","al kg",1,9.79,22,V,""),
 ("Prosciutto cotto","Mercatò","mercato","Gastronomia","Prosciutto cotto alta qualità – Dimarello","al kg (al banco)",1,10.90,21,V,"Al banco, 1,09 all'etto."),
 ("Prosciutto cotto","Mercatò","mercato","Salumi","Prosciutto cotto – Dimarello","120 g",0.120,1.69,25,V,"Il volantino stampa 14,08 al kg."),
 ("Prosciutto cotto","Mercatò","mercato","Gastronomia","Prosciutto cotto 100% italiano Stella – Negroni","al kg (al banco)",1,17.90,21,V,"Al banco, 1,79 all'etto."),
 ("Prosciutto cotto","Mercatò","mercato","Salumi","Prosciutto cotto Teneroni – Casa Modena","150 g",0.150,1.99,26,V,"Il volantino stampa 13,27 al kg."),
 ("Prosciutto cotto","Mercatò","mercato","Salumi","Prosciutto cotto Gran Biscotto – Rovagnati","100 g",0.100,1.99,25,V,"Sconto 50%. Il volantino stampa 19,90 al kg."),
 ("Prosciutto crudo","Mercatò","mercato","Gastronomia","Prosciutto di Parma DOP 22 mesi – Saper di Sapori","al kg (al banco)",1,26.90,21,V,"Al banco, 2,69 all'etto."),
 ("Prosciutto crudo","Mercatò","mercato","Gastronomia","Speck IGP Gran Resa – Senfter","al kg (al banco)",1,13.90,21,V,"Al banco, 1,39 all'etto."),
 ("Prosciutto crudo","Mercatò","mercato","Salumi","Prosciutto crudo – Citterio","120 g",0.120,2.79,25,V,"Il volantino stampa 23,25 al kg."),
 ("Salame","Mercatò","mercato","Gastronomia","Salame crudo filzetta – Gabba","al kg (al banco)",1,14.90,21,V,"Al banco, 1,49 all'etto."),
 ("Salame","Mercatò","mercato","Gastronomia","Salame bocconcino Cavour","al kg (al banco)",1,16.90,21,V,"Al banco, 1,69 all'etto."),
 ("Salame","Mercatò","mercato","Salumi","Salame Felino IGP – Cavalier Umberto Boschi","350 g",0.350,7.90,25,V,"Il volantino stampa 22,57 al kg."),
 ("Salame","Mercatò","mercato","Salumi","Salame Piemonte IGP – Raspini","100 g",0.100,2.39,25,V,"Il volantino stampa 23,90 al kg."),
 ("Salame","Mercatò","mercato","Salumi","Salame Golfetta – Golfera","100 g",0.100,2.59,26,V,"Il volantino stampa 25,90 al kg."),
 ("Mortadella","Mercatò","mercato","Gastronomia","Mortadella vari tipi – Saper di Sapori","al kg (al banco)",1,8.90,21,V,"Al banco, 0,89 all'etto."),
 ("Bresaola","Mercatò","mercato","Gastronomia","Bresaola punta d'anca IGP – Rigamonti","al kg (al banco)",1,29.90,21,V,"Al banco, 2,99 all'etto."),
 ("Pancetta e bacon","Mercatò","mercato","Gastronomia","Pancetta magra coppata – Cavalier Umberto Boschi","al kg (al banco)",1,16.90,21,V,"Al banco, 1,69 all'etto."),
 ("Tacchino","Mercatò","mercato","Gastronomia","Fesa di tacchino arrosto – Lenti","al kg (al banco)",1,14.90,21,V,"Al banco, 1,49 all'etto. È già cotta, non è carne cruda."),
 ("Tonno","Mercatò","mercato","Dispensa","Tonno all'olio di oliva – Nostromo","210 g (70 g × 3)",0.210,1.79,10,V,"Sconto 50%."),
 ("Tonno","Mercatò","mercato","Dispensa","Tonno all'olio di oliva – Palmera","480 g (160 g × 2 + 1 omaggio)",0.480,4.99,10,V,"Solo con Fidelity Card."),
 ("Tonno","Mercatò","mercato","Dispensa","Tonno all'olio di oliva Pescato a Canna – Rio Mare","720 g (120 g × 6)",0.720,7.99,10,V,"Sconto 50%."),
 ("Tonno","Mercatò","mercato","Dispensa","Tonno leggero – Mareblu","180 g (60 g × 3)",0.180,2.25,10,V,""),
 ("Tonno","Mercatò","mercato","Dispensa","Tonno all'olio di oliva meno olio – Asdomar","180 g (60 g × 3)",0.180,2.49,10,V,""),
 ("Tonno","Mercatò","mercato","Dispensa","Tonno al naturale – Asdomar","240 g (168 g sgocciolati)",0.168,1.99,10,V,"Solo con Fidelity Card. Il tonno al naturale è per metà acqua: il conto è sul peso sgocciolato, come lo fa il volantino, se no sembrerebbe il più conveniente di tutti senza esserlo."),
 ("Salmone","Mercatò","mercato","Dispensa","Filetti di salmone – Zarotti","150 g",0.150,2.99,10,V,"Il volantino stampa 19,93 al kg."),
 ("Salmone","Mercatò","mercato","Freschi","Salmone affumicato norvegese Essential – Mowi","100 g",0.100,3.99,26,V,"Il volantino stampa 39,90 al kg."),
 ("Bastoncini di pesce","Mercatò","mercato","Freschi","Bastoncini di mare – Coraya","180 g",0.180,1.49,26,V,"SONO SURIMI, non bastoncini di pesce impanati: polpa di pesce macinata e ricomposta, si mangiano freddi. Li tengo qui perche a Mercato e l'unica cosa del genere, ma non si confrontano con i bastoncini da friggere. Il volantino stampa 8,28 al kg."),
 ("Merluzzo e baccalà","Mercatò","mercato","Surgelati","Filetto di merluzzo nordico Skin MSC – Delfin","400 g",0.400,5.96,27,V,"Il volantino stampa 14,90 al kg."),
 ("Latte","Mercatò","mercato","Freschi","Latte UHT parzialmente scremato 100% italiano – Granarolo","1 litro",1,0.89,13,V,""),
 ("Latte","Mercatò","mercato","Freschi","Latte UHT senza lattosio Zymil – Parmalat","1 litro",1,1.49,13,V,""),
 ("Yogurt","Mercatò","mercato","Freschi","Yogurt assortito caffè, fragola, agrumi, banana – Yomo","1 kg (125 g × 8)",1.0,2.19,23,V,"Sconto 50%."),
 ("Yogurt","Mercatò","mercato","Freschi","Yogurt fragola e vaniglia Maxiduo Fruttolo – Nestlé","400 g (100 g × 4)",0.400,1.39,23,V,""),
 ("Yogurt","Mercatò","mercato","Freschi","Kefir cremoso – Milk","150 g",0.150,0.59,23,V,"Sconto 50%."),
 ("Yogurt","Mercatò","mercato","Freschi","Actimel – Danone","600 g (100 g × 6)",0.600,2.59,23,V,""),
 ("Burro","Mercatò","mercato","Freschi","Burro italiano – Beppino Occelli","125 g",0.125,2.19,24,V,"Solo con Fidelity Card. Il volantino stampa 17,52 al kg."),
 ("Mozzarella","Mercatò","mercato","Freschi","Mozzarelle – La Fattoria delle Cose Buone","300 g (100 g × 3)",0.300,1.89,24,V,"Il volantino stampa 6,30 al kg."),
 ("Mozzarella","Mercatò","mercato","Freschi","Mozzarella Julienne senza lattosio – Bayernland","200 g",0.200,1.49,24,V,"Sconto 50%. È già a filetti, per la pizza."),
 ("Mozzarella","Mercatò","mercato","Freschi","Mozzarella di bufala campana DOP – Ponte Reale","375 g (125 g × 3)",0.375,3.69,24,V,"Il volantino stampa 9,84 al kg."),
 ("Mozzarella","Mercatò","mercato","Gastronomia","Stracciatella di burrata – Sabelli","al kg (al banco)",1,11.90,20,V,"Al banco, 1,19 all'etto. È il ripieno della burrata, non mozzarella tonda."),
 ("Formaggio","Mercatò","mercato","Gastronomia","Bra tenero DOP","al kg (al banco)",1,8.90,20,V,"Al banco, 0,89 all'etto."),
 ("Formaggio","Mercatò","mercato","Gastronomia","Tuma d'Visu – Valform","al kg (al banco)",1,9.50,20,V,"Al banco, 0,95 all'etto."),
 ("Formaggio","Mercatò","mercato","Gastronomia","Gorgonzola DOP – Palzola","al kg (al banco)",1,9.90,20,V,"Al banco, 0,99 all'etto."),
 ("Formaggio","Mercatò","mercato","Gastronomia","Asiago DOP","al kg (al banco)",1,9.90,20,V,"Al banco, 0,99 all'etto."),
 ("Formaggio","Mercatò","mercato","Gastronomia","Primosale – Osella","al kg (al banco)",1,9.90,20,V,"Al banco, 0,99 all'etto."),
 ("Formaggio","Mercatò","mercato","Gastronomia","Leerdammer","al kg (al banco)",1,9.90,20,V,"Al banco, 0,99 all'etto."),
 ("Formaggio","Mercatò","mercato","Gastronomia","Taleggio DOP a latte crudo – Carozzi","al kg (al banco)",1,10.50,20,V,"Al banco, 1,05 all'etto."),
 ("Formaggio","Mercatò","mercato","Gastronomia","Brie – Président","al kg (al banco)",1,10.90,20,V,"Al banco, 1,09 all'etto."),
 ("Formaggio","Mercatò","mercato","Gastronomia","Fontal nazionale","al kg (al banco)",1,10.90,20,V,"Al banco, 1,09 all'etto."),
 ("Formaggio","Mercatò","mercato","Gastronomia","Stracchino Stella bianca","al kg (al banco)",1,10.90,20,V,"Al banco, 1,09 all'etto."),
 ("Formaggio","Mercatò","mercato","Gastronomia","Tomini del boscaiolo – Longo","al kg (al banco)",1,10.90,20,V,"Al banco, 1,09 all'etto."),
 ("Formaggio","Mercatò","mercato","Gastronomia","Pizzicotti affumicati – Caseificio Pugliese","al kg (al banco)",1,12.90,20,V,"Al banco, 1,29 all'etto."),
 ("Formaggio","Mercatò","mercato","Gastronomia","Pecorino Giglio – Argiolas","al kg (al banco)",1,18.90,20,V,"Al banco, 1,89 all'etto."),
 ("Formaggio","Mercatò","mercato","Freschi","Sottilette classiche × 7","200 g",0.200,1.59,24,V,"Il volantino stampa 7,95 al kg."),
 ("Formaggio","Mercatò","mercato","Freschi","Stracchino – Nonno Nanni","200 g",0.200,1.99,24,V,"Il volantino stampa 9,95 al kg."),
 ("Formaggio","Mercatò","mercato","Freschi","Tomino del boscaiolo con speck – Caseificio Longo","195 g",0.195,1.99,24,V,"Sconto 50%. Il volantino stampa 10,21 al kg."),
 ("Formaggio","Mercatò","mercato","Freschi","Primosale Linea – Osella","190 g",0.190,2.19,24,V,"Il volantino stampa 11,53 al kg."),
 ("Formaggio","Mercatò","mercato","Freschi","Fette morbidissime – Camoscio d'Oro","150 g",0.150,2.19,24,V,"Il volantino stampa 14,60 al kg."),
 ("Formaggio","Mercatò","mercato","Freschi","Biraghini – Biraghi","400 g",0.400,5.49,23,V,"Solo con Fidelity Card. Il volantino stampa 13,73 al kg."),
 ("Grana e parmigiano","Mercatò","mercato","Gastronomia","Parmigiano Reggiano DOP 24 mesi","al kg (al banco)",1,22.90,20,V,"Al banco, 2,29 all'etto."),
 ("Grana e parmigiano","Mercatò","mercato","Freschi","Parmigiano Reggiano grattugiato – Parmareggio","60 g",0.060,1.19,23,V,"Il volantino stampa 19,83 al kg."),
 ("Formaggi spalmabili","Mercatò","mercato","Freschi","Exquisa Fresco Cremoso classico","175 g",0.175,0.89,24,V,"Sconto 50%."),
 ("Formaggi spalmabili","Mercatò","mercato","Gastronomia","Robiola d'Alba bianca","al kg (al banco)",1,10.90,20,V,"Al banco, 1,09 all'etto."),
 ("Formaggi spalmabili","Mercatò","mercato","Freschi","Robiola – Osella","200 g (100 g × 2)",0.200,2.39,24,V,"Il volantino stampa 11,95 al kg."),
 ("Ricotta","Mercatò","mercato","Freschi","Ricotta Santa Lucia – Galbani","250 g",0.250,0.99,23,V,"Il volantino stampa 3,96 al kg."),
 ("Ricotta","Mercatò","mercato","Freschi","Ricotta del boscaiolo – Longo","400 g",0.400,1.59,23,V,"Il volantino stampa 3,98 al kg."),
 ("Ricotta","Mercatò","mercato","Gastronomia","Ricotta fuscelle – Caseificio Pugliese","al kg (al banco)",1,6.90,20,V,"Al banco, 0,69 all'etto."),
 ("Pasta","Mercatò","mercato","Dispensa","Pasta vari tipi – Agnesi","500 g",0.500,0.77,11,V,"Solo con Fidelity Card. Il volantino stampa 1,54 al kg."),
 ("Pasta","Mercatò","mercato","Dispensa","Pasta vari tipi – Rummo","500 g",0.500,0.79,11,V,"Sconto 50%. Il volantino stampa 1,58 al kg."),
 ("Pasta","Mercatò","mercato","Freschi","Pasta fresca vari tipi – Maffei","250 g",0.250,0.55,25,V,"Sconto 50%. Il volantino stampa 2,20 al kg."),
 ("Pasta","Mercatò","mercato","Dispensa","Pasta Khorasan bio – Sgambaro","500 g",0.500,1.99,11,V,"Il volantino stampa 3,98 al kg."),
 ("Pasta","Mercatò","mercato","Dispensa","Pasta senza glutine – Le Veneziane","250 g",0.250,1.17,11,V,"Il volantino stampa 4,68 al kg."),
 ("Pasta","Mercatò","mercato","Gastronomia","Ravioles della Val Varaita","al kg (al banco)",1,4.90,20,V,"Al banco, 0,49 all'etto."),
 ("Pasta","Mercatò","mercato","Freschi","Tajarin all'uovo – La Fattoria delle Cose Buone","250 g",0.250,1.39,26,V,"Il volantino stampa 5,56 al kg."),
 ("Pasta","Mercatò","mercato","Freschi","Pasta fresca vari tipi – Stemarpast","250 g",0.250,1.49,25,V,"Sconto 50%. Il volantino stampa 5,96 al kg."),
 ("Pasta","Mercatò","mercato","Freschi","Lasagne alla bolognese – Rana","350 g",0.350,2.99,25,V,"Il volantino stampa 8,54 al kg."),
 ("Pasta","Mercatò","mercato","Freschi","Pasta fresca ripiena Sfogliavelo – Rana","250 g",0.250,2.39,26,V,"Il volantino stampa 9,56 al kg."),
 ("Pasta","Mercatò","mercato","Freschi","Agnolotti – La Fattoria delle Cose Buone","250 g",0.250,2.99,26,V,"Il volantino stampa 11,96 al kg."),
 ("Riso","Mercatò","mercato","Dispensa","Riso Roma – Grandi Riso","1 kg",1,0.98,11,V,"Sconto 50%."),
 ("Riso","Mercatò","mercato","Dispensa","Riso Blond integrale – Gallo","1 kg",1,1.71,12,V,"Sconto 50%."),
 ("Riso","Mercatò","mercato","Dispensa","Riso Blond per risotti – Gallo","1 kg",1,1.84,12,V,"Sconto 50%."),
 ("Riso","Mercatò","mercato","Dispensa","Riso Carnaroli – Curtiriso","1 kg",1,1.99,11,V,"Sconto 50%."),
 ("Riso","Mercatò","mercato","Dispensa","Riso Arborio Selezione Speciale – Riso Scotti","1 kg",1,2.37,11,V,"Solo con Fidelity Card."),
 ("Riso","Mercatò","mercato","Dispensa","Riso Basmati – Molino di Borgo San Dalmazzo","500 g",0.500,1.49,12,V,"Solo con Fidelity Card. Il volantino stampa 2,98 al kg."),
 ("Riso","Mercatò","mercato","Dispensa","Riso Roma – Il Buon Riso","1 kg",1,2.59,11,V,"Solo con Fidelity Card."),
 ("Farina","Mercatò","mercato","Dispensa","Farina «00» per pizza grano italiano – Molino Spadoni","1 kg",1,0.99,9,V,"Solo con Fidelity Card."),
 ("Farina","Mercatò","mercato","Dispensa","Farina «00» Gran Mugnaio antigrumi – Molino Spadoni","1 kg",1,1.14,9,V,"Solo con Fidelity Card."),
 ("Farina","Mercatò","mercato","Dispensa","Farina tipo «1» di grano tenero macinata a pietra – Molino Spadoni","1 kg",1,1.39,9,V,"Solo con Fidelity Card."),
 ("Farina","Mercatò","mercato","Dispensa","Preparato per pane nero – Molino Spadoni","1 kg",1,1.79,9,V,"Solo con Fidelity Card."),
 ("Farina","Mercatò","mercato","Dispensa","Farina di avena – Molino Rossetto","900 g",0.900,1.77,11,V,"Sconto 50%. Il volantino stampa 1,97 al kg."),
 ("Pane","Mercatò","mercato","Dispensa","Pan carrè – Mulino Bianco Barilla","285 g",0.285,0.60,12,V,"Il volantino stampa 2,11 al kg."),
 ("Pane","Mercatò","mercato","Macelleria","Baguette rustica","al kg",1,2.98,22,V,"Solo nei punti vendita col forno."),
 ("Pane","Mercatò","mercato","Dispensa","Il Cracker – Gran Pavesi","560 g",0.560,1.67,12,V,"Solo con Fidelity Card. Il volantino stampa 2,98 al kg."),
 ("Pane","Mercatò","mercato","Dispensa","Spuntinelle – Morato","350 g (175 g × 2)",0.350,1.09,12,V,"Sconto 50%. Il volantino stampa 3,11 al kg."),
 ("Pane","Mercatò","mercato","Dispensa","Pane vari tipi – Daily Bread","500 g",0.500,1.69,13,V,"Il volantino stampa 3,38 al kg."),
 ("Pane","Mercatò","mercato","Dispensa","Grissini nostrani – Panealba","200 g",0.200,0.74,13,V,"Sconto 50%. Il volantino stampa 3,70 al kg."),
 ("Pane","Mercatò","mercato","Freschi","Piadina romagnola IGP alla riminese – Riccione Piadina","360 g (120 g × 3)",0.360,1.69,24,V,"Sconto 50%. Il volantino stampa 4,69 al kg."),
 ("Pane","Mercatò","mercato","Dispensa","Cuor di Pane – Mulino Bianco Barilla","325 g",0.325,1.48,12,V,"Il volantino stampa 4,55 al kg."),
 ("Pane","Mercatò","mercato","Dispensa","Grissino iposodico è senza – Monviso","120 g",0.120,0.74,12,V,"Sconto 50%. Il volantino stampa 6,17 al kg."),
 ("Pane","Mercatò","mercato","Dispensa","Cracker Bellebuone – Galbusera","200 g",0.200,1.69,12,V,"Solo con Fidelity Card. Il volantino stampa 8,45 al kg."),
 ("Pane","Mercatò","mercato","Macelleria","Pinsa classica – Pinsami","460 g (2 basi)",0.460,3.99,22,V,"Il volantino stampa 8,67 al kg."),
 ("Pane","Mercatò","mercato","Freschi","Tramezzino pane ai cereali, pollo, bacon e pomodoro – Riva","170 g",0.170,2.49,24,V,"Il volantino stampa 14,65 al kg."),
 ("Pomodoro e passata","Mercatò","mercato","Dispensa","Passata vellutata al vapore – Valfrutta","700 g",0.700,0.74,10,V,"Sconto 50%. Il volantino stampa 1,06 al kg."),
 ("Pomodoro e passata","Mercatò","mercato","Dispensa","Polpa di pomodoro – Mutti","400 g",0.400,0.64,9,V,"Sconto 50%. Il volantino stampa 1,60 al kg."),
 ("Pomodoro e passata","Mercatò","mercato","Dispensa","Pomodori pelati – Cirio","400 g",0.400,0.89,10,V,"Solo con Fidelity Card. Il volantino stampa 2,23 al kg."),
 ("Olio d'oliva","Mercatò","mercato","Dispensa","Olio extra vergine di oliva classico – Filippo Berio","0,75 litri",0.75,4.24,8,V,"Sconto 50%. Il volantino stampa 5,65 al litro."),
 ("Olio d'oliva","Mercatò","mercato","Dispensa","Olio extra vergine di oliva 100% italiano – Terre Nostre","0,75 litri",0.75,5.89,8,V,"Solo con Fidelity Card. Il volantino stampa 7,85 al litro."),
 ("Olio d'oliva","Mercatò","mercato","Dispensa","Olio d'oliva – Colavita","1 litro",1,3.96,8,V,"Solo con Fidelity Card. È olio d'oliva, non extra vergine."),
 ("Olio d'oliva","Mercatò","mercato","Dispensa","Olio extra vergine di oliva classico – Monini","1 litro",1,5.96,8,V,""),
 ("Olio di semi","Mercatò","mercato","Dispensa","Olio di semi di soia – Valsoia","1 litro",1,2.98,8,V,""),
 ("Legumi in scatola","Mercatò","mercato","Dispensa","Legumi vari tipi – Valfrutta","240 g",0.240,0.79,11,V,"Il volantino stampa 3,29 al kg."),
 ("Legumi in scatola","Mercatò","mercato","Dispensa","Piselli medi italiani – Valfrutta","400 g (270 g sgocciolati)",0.270,0.85,10,V,"Il volantino stampa 3,15 al kg, sul peso sgocciolato."),
 ("Sughi pronti","Mercatò","mercato","Dispensa","Salsa – Agromonte","330 g",0.330,1.14,9,V,"Solo con Fidelity Card. Il volantino stampa 3,45 al kg."),
 ("Sughi pronti","Mercatò","mercato","Dispensa","Sugo vari tipi – Mutti","280 g",0.280,0.99,9,V,"Solo con Fidelity Card. Il volantino stampa 3,54 al kg."),
 ("Sughi pronti","Mercatò","mercato","Dispensa","Sugo vari tipi – Barilla","300 g",0.300,1.59,9,V,"Solo con Fidelity Card. Il volantino stampa 5,30 al kg."),
 ("Sughi pronti","Mercatò","mercato","Dispensa","Sugo vari tipi – Althea","120 g",0.120,0.66,9,V,"Sconto 50%. Il volantino stampa 5,50 al kg."),
 ("Sughi pronti","Mercatò","mercato","Dispensa","Pesto Tigullio","185 g",0.185,1.69,9,V,"Il volantino stampa 9,14 al kg."),
 ("Sughi pronti","Mercatò","mercato","Dispensa","Ragù vegetale senza aglio – Biffi","190 g",0.190,1.89,9,V,"Il volantino stampa 9,95 al kg."),
 ("Sughi pronti","Mercatò","mercato","Freschi","Pesto vari tipi – Rana","140 g",0.140,1.45,25,V,"Sconto 50%. Il volantino stampa 10,36 al kg."),
 ("Verdure in scatola","Mercatò","mercato","Dispensa","Mais al vapore – Bonduelle","560 g (150 g × 3 + 1 gratis)",0.560,2.99,11,V,"Il volantino stampa 5,34 al kg."),
 ("Verdure in scatola","Mercatò","mercato","Dispensa","Antipasto di verdure – Granda Gourmet","290 g",0.290,1.98,11,V,"Sconto 50%. Il volantino stampa 6,83 al kg."),
 ("Verdure in scatola","Mercatò","mercato","Dispensa","Carciofini tagliati e funghetti sottolio – Saclà","285 g",0.285,1.99,11,V,"Il volantino stampa 6,98 al kg."),
 ("Verdure in scatola","Mercatò","mercato","Gastronomia","Olive Snocciomix","al kg (al banco)",1,6.80,21,V,"Al banco, 0,68 all'etto."),
 ("Caffè","Mercatò","mercato","Colazione","Caffè Aroma Italiano – Kimbo","500 g (250 g × 2)",0.500,6.49,13,V,"Solo con Fidelity Card. Il volantino stampa 12,98 al kg."),
 ("Caffè","Mercatò","mercato","Colazione","Caffè Granaroma – Vergnano","500 g (250 g × 2)",0.500,6.79,13,V,"Solo con Fidelity Card. Il volantino stampa 13,58 al kg."),
 ("Caffè","Mercatò","mercato","Colazione","Caffè classico decaffeinato – Hag","250 g",0.250,3.59,13,V,"Solo con Fidelity Card. Il volantino stampa 14,36 al kg."),
 ("Caffè","Mercatò","mercato","Colazione","Caffè in cialde Espresso Napoletano Formula Bar × 15 – Kimbo","110 g",0.110,2.44,14,V,"Solo con Fidelity Card. Il volantino stampa 22,18 al kg."),
 ("Caffè","Mercatò","mercato","Colazione","Caffè in capsule Dolce Gusto × 30 – Nescafé","186 g",0.186,6.79,14,V,"Solo con Fidelity Card. Il volantino stampa 36,51 al kg."),
 ("Caffè","Mercatò","mercato","Colazione","Caffè in capsule × 50 – Vergnano","250 g",0.250,9.49,14,V,"Solo con Fidelity Card. Il volantino stampa 37,96 al kg."),
 ("Caffè","Mercatò","mercato","Colazione","Caffè solubile classico – Nescafé","100 g",0.100,4.44,14,V,"Solo con Fidelity Card. Il volantino stampa 44,40 al kg."),
 ("Tè e tisane","Mercatò","mercato","Colazione","Camomilla solubile 20 bustine – Bonomelli","25 g",0.025,1.34,14,V,"Il volantino stampa 53,60 al kg. Al chilo fa impressione, ma è una scatola da 20 bustine."),
 ("Tè e tisane","Mercatò","mercato","Colazione","Thè deteinato 18 filtri – Infré","27 g",0.027,2.39,14,V,"Il volantino stampa 88,52 al kg. Al chilo fa impressione, ma è una scatola da 18 filtri."),
 ("Biscotti","Mercatò","mercato","Colazione","Novellino classico – Campiello","700 g",0.700,1.49,17,V,"Sconto 50%. Il volantino stampa 2,13 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Biscotti Zuppalatte – Colussi","250 g",0.250,0.62,17,V,"Sconto 50%. Il volantino stampa 2,48 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Biscotti Gocciolotti vari tipi – Balocco","700 g",0.700,1.99,16,V,"Il volantino stampa 2,84 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Biscotti Buonicosì vari tipi – Galbusera","400 g",0.400,1.54,17,V,"Sconto 50%. Il volantino stampa 3,85 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Biscotto Salute vari tipi – Monviso","300 g",0.300,1.29,16,V,"Solo con Fidelity Card. Il volantino stampa 4,30 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Frollini integrali Fibrextra – Misura","330 g",0.330,1.49,17,V,"Il volantino stampa 4,52 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Canestrellini – La Sassellese","250 g",0.250,1.48,14,V,"Il volantino stampa 5,92 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Biscotti Ringo × 6 vari tipi – Pavesi","330 g",0.330,2.09,14,V,"Solo con Fidelity Card. Il volantino stampa 6,33 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Biscotti del Lagaccio classici – Panarello","250 g",0.250,1.59,16,V,"Il volantino stampa 6,36 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Biscotti vari tipi – La Fattoria delle Cose Buone","300 g",0.300,1.95,14,V,"Il volantino stampa 6,50 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Paste di meliga – Nonna Lucia","280 g",0.280,1.98,14,V,"Il volantino stampa 7,07 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Torcettini – Gilber","200 g",0.200,1.49,14,V,"Il volantino stampa 7,45 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Frolle ripiene Grisbì vari tipi – Vicenzi","135 g",0.135,1.14,14,V,"Sconto 50%. Il volantino stampa 8,44 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Pavesini – Pavesi","200 g",0.200,1.79,17,V,"Il volantino stampa 8,95 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Baci di dama – Nonna Lucia","150 g",0.150,2.42,14,V,"Il volantino stampa 16,13 al kg."),
 ("Cereali","Mercatò","mercato","Colazione","Fiocchi di riso e frumento integrale con cioccolato fondente Vivi Bene – Selex","300 g",0.300,1.89,16,V,"Solo con Fidelity Card. Il volantino stampa 6,30 al kg."),
 ("Marmellata","Mercatò","mercato","Colazione","Confettura 100% da frutta vari tipi – Zuegg","230 g",0.230,1.99,18,V,"Solo con Fidelity Card. Il volantino stampa 8,65 al kg."),
 ("Miele","Mercatò","mercato","Colazione","Miele – Ambrosoli","250 g",0.250,2.49,18,V,"Solo con Fidelity Card. Il volantino stampa 9,96 al kg."),
 ("Miele","Mercatò","mercato","Colazione","Miele millefiori – Piemonte Miele","500 g",0.500,5.29,18,V,"Solo con Fidelity Card. Il volantino stampa 10,58 al kg."),
 ("Creme spalmabili","Mercatò","mercato","Colazione","Crema Pan di Stelle – Mulino Bianco Barilla","380 g",0.380,1.99,18,V,"Solo con Fidelity Card. Il volantino stampa 5,24 al kg."),
 ("Creme spalmabili","Mercatò","mercato","Colazione","Nutella – Ferrero","750 g",0.750,5.79,18,V,"Solo con Fidelity Card. Il volantino stampa 7,72 al kg."),
 ("Cioccolato","Mercatò","mercato","Colazione","Gran Blocco di cioccolato fondente 70% – Perugina","150 g",0.150,1.79,17,V,"Il volantino stampa 11,93 al kg."),
 ("Cioccolato","Mercatò","mercato","Colazione","Cioccolato fondente Emilia – Zaini","200 g",0.200,2.48,16,V,"Il volantino stampa 12,40 al kg."),
 ("Cioccolato","Mercatò","mercato","Colazione","Tavoletta di cioccolato vari tipi – Kit Kat","99 g",0.099,1.98,17,V,"Il volantino stampa 20,00 al kg."),
 ("Cioccolato","Mercatò","mercato","Colazione","Cacao amaro in polvere Emilia – Zaini","120 g",0.120,2.49,17,V,"Solo con Fidelity Card. È cacao in polvere, non cioccolato da mangiare. Il volantino stampa 20,75 al kg."),
 ("Cioccolato","Mercatò","mercato","Colazione","Tavoletta di cioccolato vari tipi – Lindt","100 g",0.100,2.48,17,V,"Il volantino stampa 24,80 al kg."),
 ("Verdure surgelate","Mercatò","mercato","Surgelati","Spinaci Cubello Foglia Più – Orogel","900 g",0.900,1.98,27,V,"Sconto 50%. Il volantino stampa 2,20 al kg."),
 ("Verdure surgelate","Mercatò","mercato","Surgelati","Fagiolini extra fini – Bonduelle","450 g",0.450,1.29,27,V,"Sconto 50%. Il volantino stampa 2,87 al kg."),
 ("Verdure surgelate","Mercatò","mercato","Surgelati","Verdurì Leggerezza – Orogel","600 g",0.600,1.99,27,V,"Il volantino stampa 3,32 al kg."),
 ("Verdure surgelate","Mercatò","mercato","Surgelati","Misto funghi con porcini – Funghi&Sapori","450 g",0.450,2.89,27,V,"Il volantino stampa 6,42 al kg."),
 ("Verdure surgelate","Mercatò","mercato","Surgelati","Cuori di carciofi in spicchi – Orogel","300 g",0.300,2.29,27,V,"Il volantino stampa 7,63 al kg."),
 ("Verdure surgelate","Mercatò","mercato","Surgelati","Funghi porcini a cubetti – Funghi&Sapori","300 g",0.300,4.96,27,V,"Solo con Fidelity Card. Il volantino stampa 16,53 al kg."),
 ("Pizza surgelata","Mercatò","mercato","Surgelati","Pizza margherita Bella Napoli × 2 – Buitoni","650 g",0.650,2.74,27,V,"Sconto 50%. Il volantino stampa 4,22 al kg."),
 ("Patate","Mercatò","mercato","Surgelati","Patatine prefritte Patasnella – Pizzoli","1 kg",1,2.29,27,V,""),
 ("Frutta","Mercatò","mercato","Ortofrutta","Mele Gala Piemonte Cuneo IGP","al kg",1,1.49,19,V,"","2026-09-03","2026-09-09"),
 ("Frutta","Mercatò","mercato","Ortofrutta","Banane bioequosolidali Natura Chiama – Selex","al kg",1,1.99,19,V,"","2026-09-10","2026-09-16"),
 ("Frutta","Mercatò","mercato","Ortofrutta","Uva bianca Italia","al kg",1,2.99,19,V,"","2026-09-03","2026-09-09"),
 ("Frutta","Mercatò","mercato","Ortofrutta","Pere Williams bianche Opera","al kg",1,2.99,19,V,"Origine Italia.","2026-09-10","2026-09-16"),
 ("Verdura","Mercatò","mercato","Ortofrutta","Carote sfuse","al kg",1,0.99,19,V,"","2026-09-03","2026-09-09"),
 ("Verdura","Mercatò","mercato","Ortofrutta","Zucchine chiare","al kg",1,1.99,19,V,"","2026-09-10","2026-09-16"),
 ("Verdura","Mercatò","mercato","Ortofrutta","Pomodoro costoluto – Gandini","al kg",1,2.99,19,V,"Origine Italia.","2026-09-03","2026-09-09"),
 ("Patate","Mercatò","mercato","Ortofrutta","Patate Iodì – Pizzoli","1,25 kg",1.25,2.49,19,V,"Il volantino stampa 1,99 al kg.","2026-09-10","2026-09-16"),
 ("Insalata in busta","Mercatò","mercato","Ortofrutta","Armonia – Bonduelle","170 g",0.170,1.49,19,V,"Il volantino stampa 8,76 al kg.","2026-09-10","2026-09-16"),
 ("Insalata in busta","Mercatò","mercato","Ortofrutta","Lattughino bio Natura Chiama – Selex","100 g",0.100,0.99,19,V,"Solo con Fidelity Card. Il volantino stampa 9,90 al kg.","2026-09-03","2026-09-09"),
 ("Insalata in busta","Mercatò","mercato","Ortofrutta","Insalata ricca Natura Chiama – Selex","140 g",0.140,1.99,19,V,"Solo con Fidelity Card. Il volantino stampa 14,21 al kg.","2026-09-10","2026-09-16"),
 ("Acqua","Mercatò","mercato","Bevande","Acqua Uliveto","1,5 litri",1.5,0.44,4,V,"Il volantino stampa 0,29 al litro."),
 ("Acqua","Mercatò","mercato","Bevande","Acqua San Benedetto Ecogreen vari tipi","3 litri (0,5 l × 6)",3.0,0.99,4,V,"Sconto 50%. Il volantino stampa 0,33 al litro."),
 ("Succhi e bibite","Mercatò","mercato","Bevande","Thè vari tipi – San Benedetto","1,5 litri",1.5,0.79,4,V,"Il volantino stampa 0,53 al litro."),
 ("Succhi e bibite","Mercatò","mercato","Bevande","Nettare vari tipi – Valfrutta","1,2 litri (200 ml × 6)",1.2,1.49,4,V,"Sconto 50%. Il volantino stampa 1,24 al litro."),
 ("Succhi e bibite","Mercatò","mercato","Bevande","Bevanda vari tipi – Bravo","1 litro",1,1.25,4,V,""),
 ("Succhi e bibite","Mercatò","mercato","Bevande","Bevanda vari tipi – Skipper","1 litro",1,1.29,4,V,""),
 ("Succhi e bibite","Mercatò","mercato","Bevande","Coca Cola vari tipi","2,64 litri (66 cl × 4)",2.64,3.99,4,V,"Solo con Fidelity Card. Il volantino stampa 1,51 al litro."),
 ("Succhi e bibite","Mercatò","mercato","Bevande","Estathé – Ferrero","600 ml (200 ml × 3)",0.600,1.59,4,V,"Il volantino stampa 2,65 al litro."),
 ("Succhi e bibite","Mercatò","mercato","Bevande","Succo d'arancia – Innocent","900 ml",0.900,2.49,19,V,"Il volantino stampa 2,77 al litro.","2026-09-03","2026-09-09"),
 ("Succhi e bibite","Mercatò","mercato","Bevande","Bibita vari tipi – Lurisia","1,1 litri (275 ml × 4)",1.1,3.89,4,V,"Il volantino stampa 3,54 al litro."),
 ("Succhi e bibite","Mercatò","mercato","Bevande","Nettare vari tipi – Zuegg","750 ml (125 ml × 6)",0.750,4.49,4,V,"Il volantino stampa 5,99 al litro."),
 ("Detersivo lavatrice","Mercatò","mercato","Cura casa","Detersivo liquido universale 49 lavaggi – General","1,98 litri",49,3.29,34,V,"Il volantino stampa 1,66 al litro; qui il conto è a lavaggio, che è quello che serve."),
 ("Detersivo lavatrice","Mercatò","mercato","Cura casa","Detersivo liquido Marsiglia 36 lavaggi – Spuma di Sciampagna","1,62 litri",36,2.99,34,V,""),
 ("Detersivo lavatrice","Mercatò","mercato","Cura casa","Detersivo liquido classico igienizzante 38 lavaggi – Ace","1,9 litri",38,3.49,34,V,"Sconto 50%."),
 ("Detersivo lavatrice","Mercatò","mercato","Cura casa","Detersivo liquido 28 lavaggi vari tipi – Chanteclair","1,26 litri",28,2.89,34,V,""),
 ("Detersivo lavatrice","Mercatò","mercato","Cura casa","Detersivo in polvere Power 71 lavaggi – Dash","3,55 kg",71,14.95,34,V,"Sconto 50%."),
 ("Ammorbidente","Mercatò","mercato","Cura casa","Ammorbidente classico 40 lavaggi – Felce Azzurra","2 litri",40,2.09,34,V,""),
 ("Carta igienica","Mercatò","mercato","Cura casa","Carta igienica Seta 2 veli 12 rotoli – Foxy","12 rotoli",12,4.59,28,V,"Sconto 50%."),
 ("Carta igienica","Mercatò","mercato","Cura casa","Carta igienica Ultra Comfort × 6 – Tenderly","6 rotoli",6,2.49,28,V,""),
 ("Carta igienica","Mercatò","mercato","Cura casa","Carta igienica Comfort 4 maxi rotoli – Tempo","4 maxi rotoli",4,1.98,28,V,"Solo con Fidelity Card. Sono maxi rotoli: al rotolo costa più di altri, ma dura di più."),
 ("Carta igienica","Mercatò","mercato","Cura casa","Carta igienica 4 rotoloni – Regina","4 rotoloni",4,2.99,28,V,"Sono rotoloni, lunghi più del doppio dei normali: al rotolo non si confrontano coi rotoli piccoli."),
 ("Carta cucina e tovaglioli","Mercatò","mercato","Cura casa","Bobina milleusi Comprami Sempre 600 strappi","1 bobina (600 strappi)",1,3.69,35,V,"È una bobina sola da 600 strappi, non un pacco di rotoli: al rotolo sembra cara, ma sono sei o sette rotoli normali."),
 ("Shampoo","Mercatò","mercato","Cura persona","Shampoo linea capelli vari tipi – Sunsilk","250 ml",0.250,1.99,31,V,"Solo con Fidelity Card. Il volantino stampa 7,96 al litro."),
 ("Shampoo","Mercatò","mercato","Cura persona","Shampoo linea capelli Elvive vari tipi – L'Oréal","300 ml",0.300,2.49,31,V,"Il volantino stampa 8,30 al litro."),
 ("Shampoo","Mercatò","mercato","Cura persona","Shampoo linea capelli vari tipi – Pantene","250 ml",0.250,2.59,31,V,"Solo con Fidelity Card. Il volantino stampa 10,36 al litro."),
 ("Shampoo","Mercatò","mercato","Cura persona","Shampoo linea capelli vari tipi – Biopoint","400 ml",0.400,4.99,31,V,"Solo con Fidelity Card. Il volantino stampa 12,48 al litro."),
 ("Shampoo","Mercatò","mercato","Cura persona","Shampoo a secco classico – Batist","200 ml",0.200,3.99,31,V,"Il volantino stampa 19,95 al litro."),
 ("Shampoo","Mercatò","mercato","Cura persona","Olio shampoo vari tipi – Restivoil","150 ml",0.150,6.69,31,V,"Il volantino stampa 44,60 al litro."),
 ("Dentifricio","Mercatò","mercato","Cura persona","Dentifricio protezione carie – Colgate","150 ml (75 ml × 2)",0.150,1.93,31,V,"Sconto 50%. Il volantino stampa 12,87 al litro."),
 # ===================== PESCE E DINTORNI, letti il 2026-09-05 =====================
 # Manlio: «continuo a notare una poca quantita di offerte di merluzzo e di
 # gamberi». Aveva ragione, ed era di nuovo un buco mio: gamberi zero e merluzzo
 # due, con sette volantini in casa. La pescheria del Bennet (pagina 3) e la
 # pagina «Pesce» del Carrefour non le avevo mai aperte.
 ("Gamberi","Bennet","bennet","Pescheria","Mazzancolle tropicali precotte 30/50","1 kg",1,11.90,3,V,"Sottocosto Freschi. L'offerta pescheria non vale in tutti i punti vendita."),
 ("Gamberi","Bennet","bennet","Pescheria","Gambero argentino decongelato 10/20 pezzi al kg","al kg",1,14.90,3,V,"Sottocosto Freschi."),
 ("Gamberi","Carrefour Iper","carriper04","Pescheria","Gamberi argentini decongelati","al kg",1,16.90,11,V,"−26%, prima 22,90. Con «Prendi Spendi», da 2 kg in su vanno a 14,90 al kg."),
 ("Gamberi","Eurospin","eurospin10","Surgelati","Gamberi argentini – Ondina","800 g",0.800,9.89,8,V,"Prima 11,99. Il volantino stampa 12,37 al kg."),
 ("Gamberi","Eurospin","eurospin10","Surgelati","Code di mazzancolla tropicale sgusciate precotte","240 g",0.240,3.79,8,V,"Prima 4,79. Il volantino stampa 15,80 al kg."),
 ("Merluzzo e baccalà","Lidl","lidl","Surgelati","Nuggets di merluzzo – Strada del Gusto","240 g",0.240,1.69,34,V,"Sono bocconcini impanati, non filetto: al chilo costano poco anche per questo. Il volantino stampa 7,04 al kg."),
 ("Merluzzo e baccalà","Ipercoop","ipercoop_extra","Surgelati","Gratinati di merluzzo gusti vari – Capitan Findus","380 g",0.380,2.99,49,V,"Sono gratinati impanati, non filetto. Il volantino stampa 7,87 al kg."),
 ("Merluzzo e baccalà","Bennet","bennet","Surgelati","14 bocconcini di merluzzo d'Alaska – Frosta","280 g",0.280,3.75,9,V,"−20%, prima 4,69. Impanati. Il volantino stampa 13,39 al kg."),
 ("Merluzzo e baccalà","Carrefour Iper","carriper04","Surgelati","Cuori di filetti di nasello del Pacifico – Frosta","300 g",0.300,4.49,16,V,"−34%, prima 6,81. Solo con la tessera SpesAmica Payback. Il volantino stampa 14,97 al kg."),
 ("Merluzzo e baccalà","Bennet","bennet","Surgelati","Fior di merluzzo d'Alaska – Findus","500 g",0.500,7.99,9,V,"−50% con la tessera Bennet Club, prima 15,98. È filetto, non impanato."),
 ("Merluzzo e baccalà","Ipercoop","ipercoop_extra","Surgelati","Filetti di merluzzo – Capitan Findus","360 g",0.360,5.99,49,V,"Etichetta «Conviene». È filetto. Il volantino stampa 16,64 al kg."),
 ("Merluzzo e baccalà","Bennet","bennet","Pescheria","Cuore filetto di merluzzo nordico decongelato","al kg",1,27.90,3,V,"Sottocosto Freschi, banco pescheria. È il filetto fresco: costa il doppio dei surgelati, ma è un'altra cosa."),
 ("Bastoncini di pesce","Carrefour Iper","carriper04","Surgelati","Bastoncini di merluzzo 30 pezzi – Ocean Catch","900 g",0.900,2.99,16,V,"−33%, prima 4,47. Solo con la tessera SpesAmica Payback. Il volantino stampa 3,33 al kg."),
 ("Bastoncini di pesce","Eurospin","eurospin10","Surgelati","Bastoncini di filetti di merluzzo, 15 pezzi","450 g",0.450,2.89,14,V,"Prima 3,49. Il volantino stampa 6,43 al kg."),
 ("Calamari e seppie","Carrefour Iper","carriper04","Pescheria","Anelli di totano decongelati","al kg",1,8.90,11,V,"−31%, prima 12,90."),
 ("Calamari e seppie","Bennet","bennet","Pescheria","Anelli di totano gigante del Pacifico decongelati","al kg",1,10.90,3,V,"Sottocosto Freschi."),
 ("Calamari e seppie","Bennet","bennet","Pescheria","Seppia pulita","al kg",1,19.90,3,V,"Sottocosto Freschi."),
 ("Tonno","Carrefour Iper","carriper04","Pescheria","Trancio di tonno pinne gialle decongelato","al kg",1,17.90,11,V,"−30%, prima 25,90. È il trancio fresco del banco, non la scatoletta."),
 ("Salmone","Bennet","bennet","Surgelati","Cuori di filetti di salmone selvaggio – Buon Vento","250 g",0.250,4.99,26,V,"Il volantino stampa 19,96 al kg."),
 ("Salmone","Carrefour Iper","carriper04","Pescheria","Saku di salmone – Gimar","140 g",0.140,7.90,11,V,"−20%, prima 9,90. Per sushi e sashimi. Il volantino stampa 56,43 al kg."),

 # Trovati sulle stesse pagine mentre cercavo il pesce: non buttarli via.
 ("Verdure surgelate","Eurospin","eurospin10","Surgelati","Minestrone 14 verdure","1,5 kg",1.5,1.79,8,V,"Prima 2,19. Il volantino stampa 1,20 al kg."),
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","Spinaci Millefoglie – Bonduelle","750 g",0.750,1.65,16,V,"−50%, prima 3,31. Solo con la tessera SpesAmica Payback. Il volantino stampa 2,20 al kg."),
 ("Verdure surgelate","Eurospin","eurospin10","Surgelati","Vellutata di verdure","600 g",0.600,1.59,8,V,"Prima 1,99. Il volantino stampa 2,65 al kg."),
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","Minestrone Leggerezza – Orogel","750 g",0.750,1.99,16,V,"−37%, prima 3,17. Solo con la tessera SpesAmica Payback. Il volantino stampa 2,66 al kg."),
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","Contorno Benessere o Leggerezza – Orogel","450 g",0.450,1.99,16,V,"−33%, prima 2,98. Solo con la tessera SpesAmica Payback. Il volantino stampa 4,43 al kg."),
 ("Verdure surgelate","Bennet","bennet","Surgelati","Pisellini Primavera – Findus","700 g",0.700,3.99,9,V,"−20%, prima 4,99. Il volantino stampa 5,70 al kg."),
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","Carciofi spicchi – Orogel","300 g",0.300,2.39,18,V,"−36%, prima 3,74. Solo con la tessera SpesAmica Payback. Il volantino stampa 7,97 al kg."),
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","8 tortini ortolano o spinaci – Frosta","240 g",0.240,1.99,18,V,"−25%, prima 2,66. Solo con la tessera SpesAmica Payback. Il volantino stampa 8,30 al kg."),
 ("Patate","Eurospin","eurospin10","Surgelati","Patatine da forno","750 g",0.750,1.39,8,V,"Prima 1,79. Il volantino stampa 1,86 al kg."),
 ("Patate","Bennet","bennet","Surgelati","Patatine We Love croccanti – Pizzoli","750 g",0.750,1.59,9,V,"−36%, prima 2,49. Il volantino stampa 2,12 al kg."),
 ("Patate","Carrefour Iper","carriper04","Surgelati","Patasnella Stick – Pizzoli","1 kg",1,2.29,16,V,"−30%, prima 3,28. Solo con la tessera SpesAmica Payback."),
 ("Gelato","Bennet","bennet","Surgelati","Ghiaccioli assortiti, 10 pezzi – Bennet","700 g",0.700,1.99,9,V,"−23%, prima 2,59. Il volantino stampa 2,84 al kg."),
 ("Gelato","Eurospin","eurospin10","Surgelati","Vaschette gelato gusti assortiti","500 g",0.500,2.19,8,V,"Prima 2,89. Il volantino stampa 4,38 al kg."),
 ("Gelato","Bennet","bennet","Surgelati","Gelato gusti vari – Bennet","500 g",0.500,2.39,9,V,"−20%, prima 2,99. Il volantino stampa 4,78 al kg."),
 ("Gelato","Eurospin","eurospin10","Surgelati","Coni gelato gusti assortiti, 6 pezzi","450 g",0.450,2.19,8,V,"Prima 2,89. Il volantino stampa 4,87 al kg."),
 ("Gelato","Bennet","bennet","Surgelati","Stecchi croccanti, 4 pezzi – Bennet","260 g",0.260,3.19,9,V,"−20%, prima 3,99. Il volantino stampa 12,27 al kg."),
 ("Gelato","Bennet","bennet","Surgelati","Stecco Mini Magnum, 6 pezzi","254 g",0.254,3.49,9,V,"−30%, prima 4,99. Il volantino stampa 13,74 al kg."),
 ("Gelato","Bennet","bennet","Surgelati","Gelato Kinder Bueno o Nutella – Ferrero","230 g",0.230,3.49,9,V,"−30%, prima 4,99. Il volantino stampa 15,17 al kg."),
 ("Pizza surgelata","Eurospin","eurospin10","Surgelati","Pizza margherita, 3 pezzi","960 g",0.960,3.49,8,V,"Prima 4,35. Il volantino stampa 3,64 al kg."),
 ("Yogurt","Eurospin","eurospin10","Freschi","Yogurt magro da bere 0,1% di grassi","500 g",0.500,0.79,14,V,"Prima 0,99. Il volantino stampa 1,58 al kg."),
 ("Yogurt","Carrefour Iper","carriper04","Freschi","Yogurt intero fragola – Yomo","250 g (125 g × 2)",0.250,0.79,16,V,"−43%, prima 1,39. Il volantino stampa 3,16 al kg."),
 ("Yogurt","Bennet","bennet","Freschi","Yogurt intero bianco – Sterzing Vipiteno","1 kg (125 g × 8)",1.0,3.59,26,V,""),
 ("Yogurt","Carrefour Iper","carriper04","Freschi","Yogurt 0% grassi – Activia","500 g (125 g × 4)",0.500,1.99,16,V,"−28%, prima 2,77. Solo con la tessera SpesAmica Payback."),
 ("Yogurt","Carrefour Iper","carriper04","Freschi","Müller mix gusti assortiti","140 g",0.140,0.69,16,V,"−44%, prima 1,25. Il volantino stampa 4,93 al kg."),
 ("Yogurt","Bennet","bennet","Freschi","Yogurt Super Mario tipi vari – Danone","220 g",0.220,1.79,26,V,"Il volantino stampa 8,14 al kg."),
 ("Pomodoro e passata","Eurospin","eurospin10","Dispensa","Passata rustica di pomodoro","680 g",0.680,0.75,14,V,"Prima 0,99. Pomodoro 100% italiano. Il volantino stampa 1,11 al kg."),
 ("Riso","Eurospin","eurospin10","Dispensa","Riso Basmati","1 kg",1,1.89,14,V,"Prima 2,49."),
 ("Olio d'oliva","Eurospin","eurospin10","Dispensa","Olio extra vergine di oliva bio","750 ml",0.750,6.49,14,V,"Prima 8,49. Il volantino stampa 8,66 al litro."),
 ("Succhi e bibite","Eurospin","eurospin10","Bevande","Cola Zero","1,5 litri",1.5,0.49,14,V,"Prima 0,69. Il volantino stampa 0,33 al litro."),
 ("Biscotti","Eurospin","eurospin10","Colazione","Fourré con farcitura al cacao","500 g",0.500,1.69,14,V,"Prima 1,99. Il volantino stampa 3,38 al kg."),
 ("Biscotti","Eurospin","eurospin10","Colazione","Biscottini alla vaniglia, 12 pezzi","570 g",0.570,2.75,8,V,"Prima 3,69. Il volantino stampa 4,83 al kg."),
 ("Pasta","Bennet","bennet","Surgelati","Lasagne alla bolognese o cannelloni ricotta e spinaci – Bennet","500 g",0.500,2.99,9,V,"Surgelate. −25%, prima 3,99. Il volantino stampa 5,98 al kg."),
 ("Pasta","Carrefour Iper","carriper04","Freschi","Pasta fresca ripiena Antiche Storie – Pastificio Orobico","250 g",0.250,2.79,16,V,"Il volantino stampa 11,16 al kg."),
 ("Pollo","Eurospin","eurospin10","Surgelati","Cotolette di pollo, agli spinaci o cordon bleu","240 g",0.240,1.59,8,V,"Prima 2,19. Carne italiana. Il volantino stampa 6,63 al kg."),
 ("Pollo","Ipercoop","ipercoop_extra","Surgelati","Bastoncini di pollo Carletto – Findus","200 g",0.200,1.99,49,V,"SOLO PER I SOCI. Il volantino stampa 9,95 al kg."),
 ("Tacchino","Eurospin","eurospin10","Salumi","Cotto di tacchino con olive","90 g",0.090,0.89,14,V,"Prima 1,15. Il volantino stampa 9,89 al kg."),
 ("Sughi pronti","Bennet","bennet","Surgelati","Sugo allo scoglio classico – Bennet","450 g",0.450,3.99,9,V,"Surgelato. −20%, prima 4,99. Il volantino stampa 8,87 al kg."),
 ("Formaggi spalmabili","Eurospin","eurospin10","Freschi","Robiola","200 g (100 g × 2)",0.200,1.49,14,V,"Prima 1,79. Latte 100% italiano. Il volantino stampa 7,45 al kg."),
 ("Mozzarella","Bennet","bennet","Freschi","Mozzarella a julienne – Bayernland","200 g",0.200,2.98,26,V,"Senza lattosio, già a filetti. Il volantino stampa 14,90 al kg."),
 ("Mozzarella","Bennet","bennet","Freschi","Bocconcini di mozzarella di bufala campana DOP – Mandara","200 g",0.200,3.49,26,V,"Il volantino stampa 17,45 al kg."),
 ("Grana e parmigiano","Bennet","bennet","Freschi","Cuor di Forma Grana Padano DOP oltre 16 mesi – Ferrari","150 g",0.150,2.99,26,V,"Il volantino stampa 19,93 al kg."),
 ("Pane","Bennet","bennet","Colazione","Focaccelle all'olio extravergine d'oliva, 6 pezzi – Mulino Bianco","198 g",0.198,1.99,26,V,"Il volantino stampa 10,05 al kg."),
 # ----- Mercatò, le pagine che il primo giro aveva saltato (lette il 2026-09-05) -----
 # Birra, vino, merendine, sapone: quattro categorie che per Mercatò erano vuote
 # e che stavano tutte dietro pagine mai aperte.
 ("Birra","Mercatò","mercato","Bevande","Birra Premium – Bavaria","0,5 litri",0.5,0.79,5,V,"Solo con Fidelity Card. Il volantino stampa 1,58 al litro."),
 ("Birra","Mercatò","mercato","Bevande","Birra – Tuborg","0,66 litri",0.66,1.08,5,V,"Solo con Fidelity Card. Il volantino stampa 1,64 al litro."),
 ("Birra","Mercatò","mercato","Bevande","Birra – Peroni","0,66 litri (33 cl × 2)",0.66,1.28,5,V,"Solo con Fidelity Card. Il volantino stampa 1,94 al litro."),
 ("Birra","Mercatò","mercato","Bevande","Birra Beck's","0,99 litri (33 cl × 3)",0.99,1.99,5,V,"Solo con Fidelity Card. Il volantino stampa 2,01 al litro."),
 ("Birra","Mercatò","mercato","Bevande","Birra Ichnusa","1,98 litri (33 cl × 6)",1.98,3.99,5,V,"Sconto 50%. Il volantino stampa 2,02 al litro."),
 ("Birra","Mercatò","mercato","Bevande","Birra Cristalli di Sale – Messina","0,5 litri",0.5,1.39,5,V,"Solo con Fidelity Card. Il volantino stampa 2,78 al litro."),
 ("Birra","Mercatò","mercato","Bevande","Birra Strong Ale 7,7 – Ceres","0,5 litri",0.5,1.58,5,V,"Il volantino stampa 3,16 al litro."),
 ("Birra","Mercatò","mercato","Bevande","Birra Blonde – La Chouffe","0,75 litri",0.75,3.99,5,V,"Solo con Fidelity Card. Il volantino stampa 5,32 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Sangiovese Rubicone IGT – Botte Buona","0,75 litri",0.75,1.59,7,V,"Il volantino stampa 2,12 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Lambrusco di Modena DOC secco o amabile – Cavicchioli","1,5 litri",1.5,3.49,7,V,"Solo con Fidelity Card. Il volantino stampa 2,33 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Bonarda dell'Oltrepò Pavese DOC – Le Cascine","0,75 litri",0.75,1.95,6,V,"Sconto 50%. Il volantino stampa 2,60 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Rosato o bianco Trevenezie IGT – Turà","0,75 litri",0.75,2.29,7,V,"Il volantino stampa 3,05 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Grignolino Piemonte DOC – Araldica","0,75 litri",0.75,2.48,6,V,"Sconto 50%. Il volantino stampa 3,31 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Dogliani DOCG Grappoli Cantina Dolcetto di Dogliani","1,5 litri",1.5,4.98,6,V,"Solo con Fidelity Card. Il volantino stampa 3,32 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Pignoletto DOC frizzante secco – Righi","0,75 litri",0.75,2.98,7,V,"Solo con Fidelity Card. Il volantino stampa 3,97 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Arneis Langhe DOC – Produttori di Govone","0,75 litri",0.75,2.98,7,V,"Sconto 50%. Il volantino stampa 3,97 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Bonarda dell'Oltrepò Pavese DOC – Manfredi","0,75 litri",0.75,2.99,6,V,"Solo con Fidelity Card. Il volantino stampa 3,99 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Orvieto Classico secco DOC – Bigi","0,75 litri",0.75,2.99,7,V,"Il volantino stampa 3,99 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Cortese dell'Alto Monferrato DOC – Duchessa Lia","0,75 litri",0.75,2.99,5,V,"Solo con Fidelity Card. Il volantino stampa 3,99 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Favorita Langhe DOC – Terredavino","0,75 litri",0.75,3.69,6,V,"Solo con Fidelity Card. Il volantino stampa 4,92 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Bianco o rosso Terre Siciliane IGT – Corvo","0,75 litri",0.75,3.78,7,V,"Solo con Fidelity Card. Il volantino stampa 5,04 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Chianti DOCG – Leonardo da Vinci","0,75 litri",0.75,3.78,7,V,"Il volantino stampa 5,04 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Prosecco frizzante DOC Spago – Tenuta Sant'Anna","0,75 litri",0.75,3.98,7,V,"Il volantino stampa 5,31 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Spumante Brut Pinot di Pinot – Gancia","0,75 litri",0.75,3.99,6,V,"Solo con Fidelity Card. Il volantino stampa 5,32 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Chardonnay Langhe DOC – Terre del Barolo","0,75 litri",0.75,4.48,7,V,"Solo con Fidelity Card. Il volantino stampa 5,97 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Pinot Grigio Friuli DOC – Ca' Vescovo","0,75 litri",0.75,4.48,6,V,"Il volantino stampa 5,97 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Prosecco Millesimato Rosé DOC – Sant'Orsola","0,75 litri",0.75,4.48,6,V,"Solo con Fidelity Card. Il volantino stampa 5,97 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Dolcetto d'Alba DOC – Fontanafredda","0,75 litri",0.75,4.98,7,V,"Solo con Fidelity Card. Il volantino stampa 6,64 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Prosecco Valdobbiadene DOCG Spago – La Gioiosa","0,75 litri",0.75,5.48,7,V,"Solo con Fidelity Card. Il volantino stampa 7,31 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Valpolicella DOC Classico Superiore Ripasso – Cantina di Negrar","0,75 litri",0.75,6.49,6,V,"Solo con Fidelity Card. Il volantino stampa 8,65 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Prosecco Valdobbiadene DOCG – Mionetto","0,75 litri",0.75,6.98,6,V,"Il volantino stampa 9,31 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Gewürztraminer Trentino DOC – Santa Margherita","0,75 litri",0.75,7.49,7,V,"Solo con Fidelity Card. Il volantino stampa 9,99 al litro."),
 ("Vino","Mercatò","mercato","Bevande","Barbaresco DOCG – Mainerdo","0,75 litri",0.75,9.98,6,V,"Il volantino stampa 13,31 al litro."),
 ("Succhi e bibite","Mercatò","mercato","Bevande","Lemonsoda o Mojito vari tipi","1,32 litri (33 cl × 4)",1.32,1.89,5,V,"Il volantino stampa 1,43 al litro."),
 ("Succhi e bibite","Mercatò","mercato","Bevande","Sanbittèr Rosso – Sanpellegrino","0,6 litri (10 cl × 6)",0.6,3.19,5,V,"Il volantino stampa 5,32 al litro."),
 ("Merendine","Mercatò","mercato","Colazione","Plumcake Offerta Convenienza – Mulino Bianco Barilla","660 g (330 g × 2)",0.660,1.99,15,V,"Sconto 50%. Il volantino stampa 3,02 al kg."),
 ("Merendine","Mercatò","mercato","Colazione","Croissant all'albicocca × 6 – Bauli","300 g",0.300,1.59,15,V,"Il volantino stampa 5,30 al kg."),
 ("Merendine","Mercatò","mercato","Colazione","Pains au chocolat × 6 – Pasquier","270 g",0.270,1.48,15,V,"Il volantino stampa 5,48 al kg."),
 ("Merendine","Mercatò","mercato","Colazione","Merendine senza lattosio × 6 – Mister Day","300 g",0.300,1.98,15,V,"Il volantino stampa 6,60 al kg."),
 ("Merendine","Mercatò","mercato","Colazione","Cereabel alla frutta – Campiello","220 g",0.220,1.39,15,V,"Solo con Fidelity Card. Il volantino stampa 6,32 al kg."),
 ("Merendine","Mercatò","mercato","Colazione","Pancake × 8 – Mulino Bianco Barilla","280 g",0.280,1.98,15,V,"Solo con Fidelity Card. Il volantino stampa 7,07 al kg."),
 ("Merendine","Mercatò","mercato","Colazione","Buondì classico × 6 – Bauli","198 g",0.198,1.48,15,V,"Il volantino stampa 7,47 al kg."),
 ("Merendine","Mercatò","mercato","Colazione","Cornetto Dolcesenza extra farcitura – Misura","298 g",0.298,2.48,15,V,"Senza zuccheri aggiunti. Il volantino stampa 8,32 al kg."),
 ("Merendine","Mercatò","mercato","Colazione","Croissant classico – Orso Bianco","350 g",0.350,2.98,15,V,"Il volantino stampa 8,51 al kg."),
 ("Merendine","Mercatò","mercato","Colazione","Pan e Cioc – Kinder","290 g",0.290,2.48,15,V,"Il volantino stampa 8,55 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Biscotti Macine vari tipi – Mulino Bianco Barilla","350 g",0.350,0.99,15,V,"Sconto 50%. Il volantino stampa 2,83 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Biscotti Bucaneve classici – Doria","200 g",0.200,0.65,15,V,"Il volantino stampa 3,25 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Amaretti – Matilde Vicenzi","250 g",0.250,1.69,15,V,"Il volantino stampa 6,76 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Pick Up × 4 vari tipi – Bahlsen","112 g",0.112,1.48,15,V,"Il volantino stampa 13,21 al kg."),
 ("Biscotti","Mercatò","mercato","Colazione","Wafer classic vari tipi – Loacker","180 g (45 g × 4)",0.180,2.49,15,V,"Il volantino stampa 13,83 al kg."),
 ("Sapone e bagnoschiuma","Mercatò","mercato","Cura persona","Sapone crema ecoricarica vari tipi – Spuma di Sciampagna","1,3 litri",1.3,2.39,29,V,"È la ricarica, non il flacone. Il volantino stampa 1,84 al litro."),
 ("Sapone e bagnoschiuma","Mercatò","mercato","Cura persona","Bagnocrema vari tipi – Spuma di Sciampagna","650 ml",0.650,1.39,29,V,"Sconto 50%. Il volantino stampa 2,14 al litro."),
 ("Sapone e bagnoschiuma","Mercatò","mercato","Cura persona","Bagnoschiuma – Pino Silvestre","750 ml",0.750,1.79,29,V,"Il volantino stampa 2,39 al litro."),
 ("Sapone e bagnoschiuma","Mercatò","mercato","Cura persona","Bagnodoccia vari tipi – Vidal","600 ml",0.600,1.49,29,V,"Il volantino stampa 2,48 al litro."),
 ("Sapone e bagnoschiuma","Mercatò","mercato","Cura persona","Bagnoschiuma vari tipi – Felce Azzurra","650 ml",0.650,1.98,29,V,"Solo con Fidelity Card. Il volantino stampa 3,05 al litro."),
 ("Sapone e bagnoschiuma","Mercatò","mercato","Cura persona","Docciaschiuma vari tipi – Dove","225 ml",0.225,1.24,29,V,"Sconto 50%. Il volantino stampa 5,51 al litro."),
 ("Sapone e bagnoschiuma","Mercatò","mercato","Cura persona","Detergente intimo – Neutromed","200 ml",0.200,1.69,29,V,"Il volantino stampa 8,45 al litro."),
 ("Sapone e bagnoschiuma","Mercatò","mercato","Cura persona","Detergente intimo vari tipi – Infasil","200 ml",0.200,1.99,29,V,"Il volantino stampa 9,95 al litro."),
 ("Dentifricio","Mercatò","mercato","Cura persona","Collutorio vari tipi – Pasta del Capitano","400 ml",0.400,1.49,30,V,"È collutorio, non dentifricio: il conto al litro non si confronta con un tubetto. Il volantino stampa 3,73 al litro."),
 ("Dentifricio","Mercatò","mercato","Cura persona","Collutorio per denti e gengive – Listerine","600 ml",0.600,2.95,30,V,"Sconto 50%. È collutorio, non dentifricio. Il volantino stampa 5,90 al litro."),
 ("Dentifricio","Mercatò","mercato","Cura persona","Dentifricio vari tipi – Antica Erboristeria","75 ml",0.075,1.19,30,V,"Il volantino stampa 15,87 al litro."),
 ("Dentifricio","Mercatò","mercato","Cura persona","Dentifricio vari tipi – Biorepair","75 ml",0.075,2.49,30,V,"Il volantino stampa 33,20 al litro."),
 # ------------------------------- PESCE FRESCO (kg) -------------------------------
 # Voce nuova del 2026-09-05: prima queste offerte le vedevo e le lasciavo fuori
 # perche non avevano dove stare. Sono al banco o surgelate, e il prezzo al kg
 # del banco viene dai cartellini all'etto, moltiplicati per dieci.
 ("Pesce fresco","Carrefour Iper","carriper04","Pescheria","Alaccia pescata in Italia","al kg",1,2.90,11,V,"−40%, prima 4,90. È pesce azzurro, piccolo e da friggere."),
 ("Pesce fresco","Carrefour Iper","carriper04","Pescheria","Cefalo pescato in Italia","al kg",1,3.90,11,V,"−20%, prima 4,90."),
 ("Pesce fresco","Eurospin","eurospin10","Surgelati","Preparato per risotto di mare","300 g",0.300,1.79,8,V,"Prima 2,15. È un misto di frutti di mare, non pesce intero. Il volantino stampa 5,97 al kg."),
 ("Pesce fresco","Bennet","bennet","Pescheria","Vongola o lupino","al kg",1,7.90,3,V,"Sottocosto Freschi. L'offerta pescheria non vale in tutti i punti vendita."),
 ("Pesce fresco","Carrefour Iper","carriper04","Pescheria","Trota iridea salmonata allevata nelle Marche e in Umbria","al kg",1,7.90,11,V,"−20%, prima 9,90."),
 ("Pesce fresco","Carrefour Iper","carriper04","Pescheria","Orata","al kg",1,8.90,11,V,"−35%, prima 13,90."),
 ("Pesce fresco","Mercatò","mercato","Surgelati","Tranci di verdesca – Maremundi","450 g",0.450,3.99,27,V,"Il volantino stampa 8,87 al kg. La verdesca è uno squalo: polpa soda, senza spine."),
 ("Pesce fresco","Bennet","bennet","Surgelati","Fritto misto di pesce – Specamare","450 g",0.450,4.79,9,V,"−20%, prima 5,99. Il volantino stampa 10,64 al kg."),
 ("Pesce fresco","Ipercoop","ipercoop_extra","Surgelati","Polpo intero – Pescanova","1 kg",1,11.90,19,V,"SOLO PER I SOCI."),
 ("Pesce fresco","Eurospin","eurospin10","Surgelati","Scampi interi – Ondina","450 g",0.450,5.99,14,V,"Prima 7,19. Il volantino stampa 13,32 al kg."),
 ("Pesce fresco","Bennet","bennet","Pescheria","Branzino Filiera Valore Bennet","al kg",1,13.90,3,V,"Sottocosto Freschi."),
 ("Pesce fresco","Bennet","bennet","Surgelati","Tranci di pesce spada – Noriberica","450 g",0.450,6.99,26,V,"Il volantino stampa 15,53 al kg."),
 ("Pesce fresco","Carrefour Iper","carriper04","Surgelati","Pesce spada in trance – Pescanova","500 g",0.500,7.99,18,V,"−31%, prima 11,58. Solo con la tessera SpesAmica Payback. Il volantino stampa 15,98 al kg."),
 ("Pesce fresco","Eurospin","eurospin10","Surgelati","Filetti di branzino spigola – Ondina","380 g",0.380,6.29,8,V,"Prima 7,99. Il volantino stampa 16,56 al kg."),
 ("Pesce fresco","Mercatò","mercato","Gastronomia","Filetti di sgombro marinati","al kg (al banco)",1,17.90,21,V,"Al banco, 1,79 all'etto."),
 ("Pesce fresco","Bennet","bennet","Pescheria","Filetto di pesce spada decongelato marinato","al kg",1,19.90,3,V,"Sottocosto Freschi."),
 ("Pesce fresco","Bennet","bennet","Pescheria","Polpo arricciato","al kg",1,22.90,3,V,"Sottocosto Freschi."),
 ("Pesce fresco","Mercatò","mercato","Gastronomia","Insalata di mare","al kg (al banco)",1,27.90,21,V,"Al banco, 2,79 all'etto. È già condita, si mangia fredda."),
 ("Pesce fresco","Carrefour Iper","carriper04","Pescheria","Sgombro grigliato","120 g",0.120,3.99,11,V,"−20%, prima 4,99. È già cotto. Il volantino stampa 33,25 al kg."),
 ("Pesce fresco","Ipercoop","ipercoop_extra","Surgelati","Fiori Special branzino, orata, salmone o tonno – Capitan Findus","200 g (2 pezzi)",0.200,6.99,49,V,"Etichetta «Conviene». Il volantino stampa 34,95 al kg."),
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
