# -*- coding: utf-8 -*-
"""Le pagine guardate e scartate: viste, e non c'era niente da prendere.

Regola di Manlio, 2026-09-05: «una volta che hai visto una pagina piena di
quaderni o di pubblicita o di offerte che danno solo punti premio, lasciala
perdere».

Serve a distinguere due cose che prima si confondevano. `lette.py` contava
«letta» una pagina che avesse almeno un prezzo, quindi una pagina di pentole
guardata e scartata restava per sempre nell'elenco delle cose da fare, e la
volta dopo la riaprivo. Qui invece si scrive che e stata vista: sparisce dalle
cose da fare e non si riapre.

**Si scrive solo dopo averla guardata davvero**, mai per sentito dire dal
titolo o dall'OCR: e proprio saltando pagine senza aprirle che mi sono perso
la pescheria del Bennet. E il motivo va scritto per esteso, perche fra un mese
serve a capire se lo scarto era giusto: «pentole» si, «niente» no.

Se un volantino cambia, le sue pagine qui vanno buttate: i numeri di pagina
valgono per QUEL volantino. La pulizia la fa lette.py da solo, ignorando le
chiavi che non stanno piu in dati.py.
"""

# chiave del volantino -> {numero di pagina: perche l'ho scartata}
SCARTATE = {
 # Guardate una per una il 2026-09-18, leggendo il volantino per intero (37 pagine).
 'md22': {
   5: 'pagina "tutto a 1€" di bevande e dolci senza categoria del catalogo (avena drink, frutta da bere, cannucce, maionese, taralli, merende, barrette)',
   11: 'pagina ricetta pubblicitaria con GialloZafferano (cous cous alle melanzane): nessun prezzo',
   23: 'speciale Cura Persona: salviette, detergenti, shampoo, creme, nessuna categoria del catalogo',
   27: 'speciale Accessori Cucina: pentole e utensili, nessun prezzo di spesa alimentare',
   28: 'speciale Accessori Cucina: pentole professionali e piastre, nessun prezzo di spesa alimentare',
   29: 'speciale Accessori Cucina: batterie di pentole e bistecchiere, nessun prezzo di spesa alimentare',
   30: 'speciale Casalingo: elettrodomestici (forno, asciugatrice, ferro da stiro), nessun prezzo di spesa alimentare',
   31: 'speciale Casalingo: stendini, tappeti, ferro da stiro, nessun prezzo di spesa alimentare',
   32: 'speciale Casalingo: arredo e decorazioni, nessun prezzo di spesa alimentare',
   33: 'speciale Tessile: biancheria e abbigliamento, nessun prezzo di spesa alimentare',
   34: 'speciale Urban E-Mobility: bici e monopattini elettrici, nessun prezzo di spesa alimentare',
   35: 'MD Viaggi: pacchetti vacanza, nessun prezzo di spesa alimentare',
   36: 'MD Viaggi: pacchetti vacanza (pagina 2), nessun prezzo di spesa alimentare',
 },
 # Guardate una per una il 2026-09-17, leggendo il volantino per intero (7 pagine).
 'lidlfv17': {
   6: 'pagina pubblicitaria sul premio "Sicurezza Alimentare Frutta e Verdura": nessun prezzo',
 },
 # Guardate una per una il 2026-09-16, leggendo il volantino per intero (20 pagine).
 'mercato17': {
   20: 'speciale casa calda (biancheria, tappeti, calze, felpe) ed elenco dei punti vendita: nessun prezzo di spesa',
 },
 'mercato': {
   1:  'copertina: cartoleria e zaini per la scuola, nessun prezzo di spesa',
   2:  'raccolta punti FILA: bollini e codici sport, niente da comprare',
   3:  'elenco delle associazioni sportive dei codici, nessun prezzo',
   32: 'detersivi per lavastoviglie con un prezzo solo per tre formati diversi: '
       'non si sa a quale dei tre si riferisca, meglio niente che un numero inventato',
   33: 'detersivi per pavimenti e spugne: nessuna categoria del catalogo li copre',
   36: 'pentole, pile, lampadine, calze e risma di carta',
 },
 # Guardate una per una il 2026-09-09, leggendo il volantino per intero.
 'bennet0903': {
   1:  'copertina: solo il titolo e le date, nessun prezzo',
   20: 'regolamento del buono sconto del 50%: come si prende e come si spende',
   30: 'caffettiere, padelle, tortiere, thermos, borracce, tazze',
   31: 'tovaglie, strofinacci, presine, tappeti da cucina, cuscini',
   32: 'pubblicita: il volantino Bennet su WhatsApp',
   33: "pubblicita: l'app Bennet",
   34: 'pubblicita: bennetdrive, ordina online e ritira in negozio',
   35: 'pubblicita: catalogo Bennet Club 2026',
   36: 'quarta di copertina: di nuovo il buono del 50% e i recapiti',
 },
 # Guardate una per una il 2026-09-10, leggendo il volantino per intero. La
 # maggior parte e sconto percentuale su intere linee di marca, senza prezzo
 # di base: non si puo calcolare un prezzo vero (vedi anche l'Ipercoop dello
 # stesso giorno, stesso formato).
 # Guardate una per una il 2026-09-10, leggendo le pagine mai aperte prima.
 'eurospin10': {
   9:  'pubblicità: accettazione buoni pasto, nessun prezzo di spesa',
   16: 'mobili e arredo per la casa (appendiabiti, scaffali, stiro, TV, soundbar)',
   17: 'accessori per la pulizia della casa (panni, mop, aspirapolvere, scope elettriche)',
   18: 'abbigliamento e calzature uomo/donna, elettrodomestici da stiro',
   19: 'attrezzi e arredo da giardino',
   20: 'pubblicità: EuroSpin Viaggi, hotel in Italia',
   21: 'pubblicità: EuroSpin Viaggi, viaggi all\'estero',
 },
 'md08': {
   7:  'pubblicità: ricetta GialloZafferano coi peperoni, nessun prezzo',
   15: 'piccoli elettrodomestici da colazione (tazzine, cappuccinatore, spremiagrumi, vassoio da letto)',
   20: 'integratori alimentari Equilibra (gummies, bustine, flaconi): nessuna categoria del catalogo',
   22: 'concorso a premi Calvé, ketchup e maionese: nessuna categoria del catalogo li copre',
   16: 'elettrodomestici da cucina a marchio MXD (tritatutto, spremiagrumi, sbattitore, macchina da caffè)',
   17: 'elettrodomestici Tognana e Zephir (sbattitore, montalatte, tostapane, frullatore, bollitore, tostiera)',
   26: 'detergenti per la casa, cibo e accessori per animali: nessuna categoria del catalogo',
   27: 'elettrodomestici da cucina (frullatore, sminuzzatore) e casalinghi (tortiere, taglieri, lavatrice, pattumiera)',
   28: 'casalinghi: ceste, contenitori, pouf, cassettiera, rasoio, pulisci pori',
   29: 'igiene orale e giochi per bambini',
   30: 'abbigliamento e scarpe sport e tempo libero',
   31: 'calze e calzini sportivi e da lavoro',
   32: 'elettrodomestici grandi (microonde, forno, lavatrice, lavastoviglie, asciugatrice)',
   33: 'pubblicità: MD Viaggi, pacchetti mare estero',
   34: 'pubblicità: MD Viaggi, capitali europee e extraeuropee',
 },
 'bennet10': {
   1:  'copertina: solo il titolo e le date, nessun prezzo',
   2:  'sconto 50% su intere linee di marca (Müller, Divella, Fini, Rana, Wudy), senza prezzo di base',
   3:  'sconto 50% su intere linee di marca (Buitoni, Magnum, 4 Salti in Padella, Curtiriso, Pomì/De Rica), senza prezzo di base',
   4:  'sconto 50% su intere linee di marca (Garofalo, Morato, San Bernardo, San Benedetto, Tenuta Ca\' Vescovo), senza prezzo di base',
   5:  'sconto 50% su intere linee di marca (Colgate, Neutro Roberts, Dash, Foxy, Duracell, Implux), senza prezzo di base',
   6:  'sconto 40% su intere linee di marca (Gocciole, Lemon Soda, Settesoli, Sammontana, Amadori, Findus), senza prezzo di base',
   7:  'sconto 40% su intere linee di marca (Pizzoli, Findus, Viva la Mamma, Galbani, KV Nordic, Yomo, Fruttolo), senza prezzo di base',
   8:  'sconto 40% su intere linee di marca (Spuma di Sciampagna, Omino Bianco, Mareblu, Clemente, Mio, La Vangadizza), senza prezzo di base',
   9:  'sconto 40% su intere linee di marca (Lines, pentole Moneta, Tempo, Fresh&Clean, cibo per animali Adoc, Frigoverre, Loctite, Selenia), senza prezzo di base',
   10: 'sconto 30% su intere linee di marca (Orogel, Magnum, Frosta, Parmalat/Zymil/Chef, Parmareggio, Philadelphia), senza prezzo di base',
   11: 'sconto 30% su intere linee di marca (Ferrari, Beretta, Bonduelle, Lavazza, Novi), senza prezzo di base',
   12: 'sconto 30% su intere linee di marca (Coca Cola, Ichnusa, Raffo, Angelo Poretti, Capetta, Monster, Yoga, Loacker), senza prezzo di base',
   13: 'sconto 30% su intere linee di marca (Garnier, Lines Specialist, Swiffer, Vileda, Diavolina, Ariasana), senza prezzo di base',
   26: 'piante da vaso, fiori, cibo e lettiere per cani e gatti: nessuna categoria del catalogo',
   27: 'abbigliamento, accappatoi, calze, ciabatte, scarpe',
   28: 'scatole, candele, bicchieri, caraffe, contenitori, stendibiancheria, zerbini',
   29: 'articoli di cartoleria e giochi per bambini',
   32: 'pubblicita: l\'app Bennet',
   33: 'pubblicita: bennetdrive, ordina online e ritira in negozio',
   34: 'pubblicita: catalogo Bennet Club 2026',
   35: 'quarta di copertina: elenco dei negozi dove vale la promozione, nessun prezzo',
 },
 # Guardate una per una il 2026-09-10, leggendo il volantino per intero (58 pagine).
 'lidl10': {
   20: 'Sottocosto (Beck\'s, pizza Cameo, tortellini Fini, yogurt Granarolo, passata Mutti): stessa offerta già scritta sotto la chiave "lidl", non si ripete',
   13: 'pubblicità: voto "Insegna dell\'anno", concorso a premi, nessun prezzo di spesa',
   16: 'pubblicità: voto "Insegna dell\'anno", seconda pagina',
   26: 'specialità Alpenfest (leberkäse, canederli, crauti, cavolo rosso): nessuna categoria del catalogo le copre',
   27: 'pubblicità Alpenfest e prodotti da forno del festival (stinco, grissini decorativi): niente che rientri nel catalogo',
   28: 'specialità Alpenfest (wurstel con formaggio, aglio orsino, spezie): nessuna categoria del catalogo',
   29: 'utensili Parkside da giardino, piccoli prezzi',
   30: 'utensili Parkside: occhiali, spatole, chiavi, set meccanica',
   31: 'utensili Parkside: guanti, colla, punte per trapano',
   32: 'abbigliamento Esmara uomo',
   33: 'abbigliamento Esmara donna',
   34: 'abbigliamento Esmara donna, seconda pagina',
   35: 'pubblicità: accettazione buoni pasto, nessun prezzo di spesa',
   36: 'pubblicità: Gardaland partner Lidl Plus',
   37: 'utensili Parkside «da lunedì 14/09»',
   38: 'utensili Parkside, batterie e aspirapolvere',
   39: 'utensili Parkside: sega, elettroutensile multiuso, trapano',
   40: 'utensili Parkside: luce LED, torcia, ombrello',
   41: 'utensili Parkside: smerigliatrice, abbigliamento da lavoro',
   42: 'arredo Livarno: biancheria da letto, pouf, cuscini',
   43: 'arredo Livarno: coperte, pouf, cuscino laterale, tappeto',
   44: 'arredo Livarno: mobile TV, mobiletto, tavolino, lampade',
   45: 'arredo Livarno: illuminazione, tappeti decorativi',
   46: 'fiori e piante: mix di fiori, succulente, crisantemo, bulbi — non in catalogo',
   47: 'fiori e piante: piante verdi, orchidee, rose — non in catalogo',
   49: 'cosmetica Nivea',
   50: 'cosmetica L\'Oréal',
   56: 'pubblicità: Lidl Viaggi, Parma',
   57: 'pubblicità: Lidl Viaggi, montagna e Spagna',
 },
 # Guardate una per una il 2026-09-14, leggendo il volantino per intero (50/50 pagine).
 'carriper15': {
   1:  'copertina «Grandi Marche»: sconto 50% su pasta Rummo, pizze Italpizza, birre Nastro Azzurro/Peroni, senza prezzo di base',
   2:  'sconto 50% su intere linee di marca (Consorcio, Cirio, Maxibon, Pavonero), senza prezzo di base',
   3:  'sconto 50% su intere linee di marca (Rummo, Aia impanati, Bonduelle, Fabuloso, Implux), senza prezzo di base',
   4:  'sconto 30-40% su intere linee di marca (Orogel, OraSì, Balocco), senza prezzo di base',
   5:  'sconto 30-40% su intere linee di marca (Italpizza, Fruttolo, San Benedetto, Kellogg\'s), senza prezzo di base',
   6:  'sconto 40% su intere linee di marca (Amadori, Kraft, pasta fresca Maffei, tramezzini Alba), senza prezzo di base',
   7:  'sconto 40% su intere linee di marca (Sabelli, Sant\'Anna, Arcasa, Caleffi), senza prezzo di base',
   8:  'sconto 30% su intere linee di marca (Peroni, Teneroni, Lamb Weston, Granarolo Accadì, Pattex), senza prezzo di base',
   9:  'sconto 30% su intere linee di marca (Lavazza, Plasmon, Milka, Loacker, Calvé), senza prezzo di base',
   10: 'sconto 30% su intere linee di marca (San Pellegrino, Mowi salmone affumicato, Winni\'s, WC Net, Tena), senza prezzo di base',
   11: 'sconto 30% su intere linee di marca non alimentari (Gillette, Cuki, Sloggi, Solo Soprani, Golden Lady)',
   27: 'aperitivi e snack (formaggio, olive, patatine, crodino, gin, prosecco): niente che rientri stabilmente nel catalogo',
   28: 'speciale Oktoberfest: birre tedesche a tema, wurstel, stinco, bretzel — offerte simili già prese altrove nel volantino',
   30: 'shampoo, tinture, balsami e prodotti per capelli',
   31: 'dentifrici, spazzolini, rasoi e schiuma da barba',
   32: 'creme viso, sieri, detergenti e trucco',
   33: 'deodoranti, bagnoschiuma, saponi e detergenti intimi',
   34: 'detersivi e prodotti per la pulizia della casa: prezzi non migliori di quelli già in dati.py per le stesse categorie',
   35: 'pannolini, carta igienica, assorbenti e cibo per animali: nessun prezzo migliore di quelli già presenti',
   36: 'piatti, bicchieri, padelle e accessori da cucina',
   37: 'scatole, stendibiancheria, cesti e organizzatori per la casa',
   38: 'padelle, taglieri, moka e stoviglie monouso',
   39: 'lubrificanti auto, batteria auto, aspirapolvere e pile',
   40: 'peluche e giocattoli',
   41: 'carta, panni, padelle, bottiglie termiche e biancheria da letto',
   42: 'giubbotti, scarpe e abbigliamento sportivo uomo/donna',
   43: 'abbigliamento uomo',
   44: 'intimo uomo e donna, pantofole',
   45: 'piccoli elettrodomestici e bicchieri',
   46: 'smartphone e televisori',
   47: 'grandi elettrodomestici (lavatrice, frigorifero, microonde, friggitrice ad aria)',
   48: 'pubblicità: raccolta bollini bicchieri RCR Diamonds, nessun prezzo di spesa',
   49: 'raccolta bollini bicchieri RCR Diamonds: quanti bollini servono, nessun prezzo di spesa',
 },
 # Guardate una per una il 2026-09-15, leggendo il volantino per intero.
 'lidl17': {
   16: 'barrette e integratori proteici, porridge, budino e bevande sportive: nessuna categoria del catalogo li copre',
   18: 'abbigliamento e scarpe sportive Crivit uomo/donna',
   19: 't-shirt e leggings sportivi Crivit, bilancia pesapersone, fascia elastica',
   20: 'aspirapolvere, copri piano cottura e contenitori salvafreschezza SilverCrest',
   21: 'contenitori, portaoggetti e box W5',
   22: 'organizer, stendibiancheria, ferro da stiro e bacinelle per la casa',
   23: 'spazzole, tagliacapelli e asciugacapelli Cien Beauty',
   24: 'idropulsore, bilancia, accessori manicure, orologi da bagno e tappeti',
   25: 'accessori bagno Livarno: asse WC, set doccia, rubinetteria',
   26: 'abbigliamento uomo Esmara: gilet e pantaloni cargo',
   27: 'abbigliamento uomo Esmara: camicie, maglioni, jeans, clogs',
   28: 'abbigliamento Jeep: felpe, t-shirt, calze, boxer',
   29: 'utensili da giardino Parkside: tagliarami, soffiatore, tagliasiepi',
   30: 'utensili da giardino Parkside: motosega, potatore, batterie',
   31: 'cavalletto, scaffale, faro LED e forbici da giardinaggio Parkside',
   32: 'specialità orientali Vitasia (mochi, gyoza, cotolette di pollo panko, zuppa di miso): nessuna categoria del catalogo le copre',
   33: 'specialità orientali Vitasia (tofu, panko, olio di sesamo, zenzero, miso, ramen) e carta da cucina decorata',
   34: 'sushi box, edamame, involtini, snack di alga nori, tè e gin: nessuna categoria del catalogo li copre',
   35: 'fiori e piante da appartamento e da esterno',
 },
}
