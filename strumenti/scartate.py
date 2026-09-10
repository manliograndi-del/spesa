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
 'mercato': {
   1:  'copertina: cartoleria e zaini per la scuola, nessun prezzo di spesa',
   2:  'raccolta punti FILA: bollini e codici sport, niente da comprare',
   3:  'elenco delle associazioni sportive dei codici, nessun prezzo',
   32: 'detersivi per lavastoviglie con un prezzo solo per tre formati diversi: '
       'non si sa a quale dei tre si riferisca, meglio niente che un numero inventato',
   33: 'detersivi per pavimenti e spugne: nessuna categoria del catalogo li copre',
   36: 'pentole, pile, lampadine, calze e risma di carta',
 },
 # Guardate una per una il 2026-09-07, leggendo il volantino per intero.
 # Il Carrefour Iper riempie meta volantino di roba che non e spesa.
 'carriper04': {
   6:  'televisori e smartphone',
   7:  'lavatrice, asciugatrice, frigorifero, friggitrice ad aria',
   8:  'piatti, padelle, microonde, scopa elettrica, mocio',
   9:  'AdBlue, olio per motore, lenzuola, zaino, scarpe da ginnastica',
   28: 'raccolta bollini bicchieri RCR: si prendono coi bollini, non si comprano',
   29: 'seconda pagina della stessa raccolta bollini',
   35: 'zaini, trolley e astucci per la scuola',
   36: 'zaini e astucci per la scuola, seconda pagina',
   37: 'zaini e trolley per la scuola, terza pagina',
   38: 'quaderni, raccoglitori, risme di carta',
   39: 'quaderni, pennarelli, matite, pastelli',
   40: 'penne, colla, correttori',
   41: 'evidenziatori, post-it, nastro adesivo, pennarelli',
   42: 'carte Pokemon, scrivanie, stampanti, notebook, cuffie',
   43: 'elettrodomestici: lavatrice, frigo, robot, phon, rasoio',
   44: 'bicchieri, piatti, pentole, contenitori, tagliere, pattumiera',
   45: 'lenzuola, asciugamani, guanciali, materassi',
   46: 'abbigliamento bambini: tute, felpe, leggings',
   47: 'abbigliamento neonati e bambini, pantofole, grembiuli',
   48: 'pigiami, calze, slip, scarpe',
   49: 'abbigliamento uomo: felpe, t-shirt, jeans, scarpe',
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
}
