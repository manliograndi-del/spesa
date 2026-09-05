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

Volantino = _nt('Volantino', 'chiave insegna periodo pdf fino indirizzo inizio')
Volantino.__new__.__defaults__ = (None,)   # inizio: se manca, e gia in corso

def _v(*campi):
    return Volantino(*campi)

VOLANTINI = [
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
 ("Salmone","Carrefour Iper","carriper04","Pescheria","Saku di salmone – Gimar","140 g",0.140,7.90,11,V,"−20%, prima 9,90. Per sushi e sashimi. Il volantino stampa 56,43 al kg."),
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
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","Fagiolini e patate – Bonduelle","450 g",0.450,1.45,18,V,"−25%, prima 1,94. Solo con la tessera SpesAmica Payback."),
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","Piselli finissimi – La Valle degli Orti","850 g",0.850,2.99,18,V,"−28%, prima 4,16. Solo con la tessera SpesAmica Payback."),
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","Carciofi a spicchi – Orogel","300 g",0.300,2.39,18,V,"−36%, prima 3,74. Solo con la tessera SpesAmica Payback."),
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","Tortini spinaci o ortolano – Frosta","240 g",0.240,1.99,18,V,"−25%, prima 2,66. Solo con la tessera SpesAmica Payback."),
 ("Verdure surgelate","Carrefour Iper","carriper04","Surgelati","Funghi porcini a cubetti","300 g",0.300,3.99,18,V,"−20%, prima 4,99. Solo con la tessera SpesAmica Payback."),
 # ------------------------------- PIZZA SURGELATA (kg) -------------------------------
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
