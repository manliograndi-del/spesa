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
 # Guardate una per una il 2026-09-22, leggendo i volantini Conad per intero
 # (edizione Piemonte, Conad di via Cesana 78).
 'conad24': {
   2: 'buono spesa da 10 euro ogni 60 di spesa dall\'1 al 7 ottobre: nessun prezzo',
   3: 'buono macelleria del 20% (dal 24 al 30 settembre, da spendere dall\'1 al 7 ottobre): nessun prezzo',
   22: 'completo letto, piante, fiori e concimi: nessun prezzo di spesa alimentare',
   23: 'viaggi HeyConad e concorso dell\'app: nessun prezzo di spesa',
 },
 # Guardate una per una il 2026-09-22, leggendo i due volantini Pam per intero
 # (edizione «PAM Supermercati», quella di corso Orbassano 212).
 'pam24': {
   14: '«Speciale sconto 20%» sui Tesori dell\'Arca (speck, cotto, mortadella, bresaola, mozzarella di bufala, parmigiano...): solo lo sconto, nessun prezzo stampato',
 },
 'pamextra24': {
   11: 'cucina orientale Suzi Wan (vermicelli di riso, cialde di gamberi, salse, latte di cocco), involtini primavera e snack salati (patatine, tortillas): nessuna categoria del catalogo',
   19: 'superalcolici (brandy, amaro, vodka, rum): solo sconti del 10% senza prezzo, nessuna categoria del catalogo',
   21: 'pulizia della casa: detergente pavimenti, panni, mocio, scope, spugne, cattura polvere, deodoranti e candele: nessuna categoria del catalogo',
   23: 'salviettine e carta igienica umidificata Fria (a pezzi, non a rotoli), dentifricio Sensodyne solo a sconto del 10% senza prezzo',
   27: 'cancelleria e casa: temperamatite, correttori, colla, assorbiumidità: nessun prezzo di spesa alimentare',
 },
 # Guardate una per una il 2026-09-22, leggendo il volantino per intero
 # (47 pagine, edizione Torino-Collegno).
 'ipercoop24': {
   4: '«Grandi Marche Selection»: solo sconti percentuali (30-40%) senza il prezzo di partenza, nessun prezzo ricavabile',
   5: '«Grandi Marche Selection», seconda pagina: solo sconti percentuali senza prezzo di partenza',
   26: 'piante e fiori: orchidee, bonsai, composizioni, nessun prezzo di spesa alimentare',
   27: 'giardinaggio: bulbi, concimi, terricci, sementi, nessun prezzo di spesa alimentare',
   29: 'fai da te: lampadine, pennelli, idropittura, accendifuoco, nessun prezzo di spesa alimentare',
   30: 'auto: oli motore, batterie, adblue, nessun prezzo di spesa alimentare',
   31: 'auto: lavavetri, tappetini, spazzole tergicristallo, nessun prezzo di spesa alimentare',
   32: '«Occasioni di felicità»: collant, calze, pentole, accessori cucina, nessun prezzo di spesa alimentare',
   33: '«Occasioni di felicità»: bilancia, zerbino, teli per piante, antifurti, nessun prezzo di spesa alimentare',
   34: 'libri, biancheria per la casa, filtri per acqua, nessun prezzo di spesa alimentare',
   35: 'Expert: smartphone, scopa elettrica, forno a microonde, nessun prezzo di spesa alimentare',
   36: 'Expert: elettrodomestici (lavatrice, asciugatrice, frigorifero), nessun prezzo di spesa alimentare',
   37: 'raccolta bollini Alessi: i prodotti sponsor hanno solo il numero di bollini, nessun prezzo',
   38: 'raccolta bollini Alessi, seconda pagina: solo bollini, nessun prezzo',
   39: 'raccolta bollini Alessi, terza pagina: solo bollini, nessun prezzo',
   40: 'cura persona a sconto percentuale senza prezzo di partenza, più elenco dei punti vendita e buoni sconto',
   41: 'pubblicità Asia Mama: ravioli e involtini surgelati pronti, nessuna categoria del catalogo',
   42: 'pubblicità Knorr: dadi, brodo e risotti pronti, nessuna categoria del catalogo',
   45: "Dr. Scholl's: solette, creme e lime per i piedi, sconto soci 15% senza prezzo di partenza",
   46: 'pubblicità Hero: cerottini per brufoli, nessuna categoria del catalogo',
   47: 'pubblicità vini Tenute del Cerro: solo sconti del 30% senza il prezzo di partenza',
 },
 # Guardate una per una il 2026-09-18, leggendo il volantino per intero (37 pagine).
 'bennetextra24': {
   6: 'pubblicità Gillette e King C. Gillette: rimborsi e concorsi, nessun prezzo',
 },
 'mercatoreal17': {
   2: 'creme viso, balsamo multiuso e trucco (Mixa, Maybelline, Revitalift): nessuna categoria del catalogo',
 },
 'carriper29': {
   7: 'offerte al 50% non alimentari: cuscino, padelle, lavavetri, panni, jeans, felpa, pantofole, Barbie',
   26: 'raccolta bollini dei bicchieri RCR: nessun prezzo di spesa',
   27: 'animali: snack e cibo per cani e gatti, nessuna categoria del catalogo',
   32: 'mocio, scope, panni, secchi: nessuna categoria del catalogo',
   33: 'sacchi, grucce, guanti, asse da stiro: nessuna categoria del catalogo',
   36: 'auto, pellet, piatti e bicchieri di plastica, Halloween: nessun prezzo di spesa',
   37: 'televisori, telefoni ed elettrodomestici',
   38: 'pentole e lasagnere',
   39: 'pentole e padelle',
   40: 'tovaglie e tessile per la casa',
   41: 'tessile per la casa',
   42: 'smartphone e televisori',
   43: 'abbigliamento',
   44: 'abbigliamento uomo',
   45: 'abbigliamento',
   46: 'piatti, ciotole, tazze: «svuota tutto» della casa',
   47: 'abbigliamento e intimo',
 },
 'carrcoca15': {
   1: 'concorso «Vinci premi iconici Coca-Cola»: nessun prezzo',
 },
 'md22': {
   # Edizione di corso Sebastopoli (nord-atm-na-gastro, 36 pagine): non ha la
   # pagina della gastronomia al banco, quindi dalla 14 in poi i numeri sono
   # uno meno di quelli dell'edizione letta il 22/9 su anteprimavolantino.
   5: 'pagina "tutto a 1€" di bevande e dolci senza categoria del catalogo (avena drink, frutta da bere, cannucce, maionese, taralli, merende, barrette)',
   11: 'pagina ricetta pubblicitaria con GialloZafferano (cous cous alle melanzane): nessun prezzo',
   22: 'speciale Cura Persona: salviette, detergenti, shampoo, creme, nessuna categoria del catalogo',
   26: 'speciale Accessori Cucina: pentole e utensili, nessun prezzo di spesa alimentare',
   27: 'speciale Accessori Cucina: pentole professionali e piastre, nessun prezzo di spesa alimentare',
   28: 'speciale Accessori Cucina: batterie di pentole e bistecchiere, nessun prezzo di spesa alimentare',
   29: 'speciale Casalingo: elettrodomestici (forno, asciugatrice, ferro da stiro), nessun prezzo di spesa alimentare',
   30: 'speciale Casalingo: stendini, tappeti, ferro da stiro, nessun prezzo di spesa alimentare',
   31: 'speciale Casalingo: arredo e decorazioni, nessun prezzo di spesa alimentare',
   32: 'speciale Tessile: biancheria e abbigliamento, nessun prezzo di spesa alimentare',
   33: 'speciale Urban E-Mobility: kart e moto elettriche per bambini, scooter subacqueo, nessun prezzo di spesa alimentare',
   34: 'MD Viaggi: pacchetti vacanza, nessun prezzo di spesa alimentare',
   35: 'MD Viaggi: pacchetti vacanza (pagina 2), nessun prezzo di spesa alimentare',
 },
 # Guardate una per una il 2026-09-16, leggendo il volantino per intero (20 pagine).
 'mercato17': {
   20: 'speciale casa calda (biancheria, tappeti, calze, felpe) ed elenco dei punti vendita: nessun prezzo di spesa',
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
 # Guardate una per una il 2026-09-19, leggendo il volantino per intero.
 'bennet1709': {
   1:  'copertina: solo il titolo «Un mondo di bellezza» e le date, nessun prezzo',
   3:  'styling e colorazione capelli (gel, lacca, tinte, olio-shampoo antiforfora): nessuna categoria del catalogo li copre',
   6:  'creme viso, sieri e trattamenti antirughe: nessuna categoria del catalogo li copre',
   7:  'maschere viso, acqua micellare, salviette struccanti, labello, patch brufoli',
   8:  'creme corpo idratanti e scrub: nessuna categoria del catalogo li copre',
   9:  'depilazione donna: creme, strisce, rasoi',
   10: 'deodoranti e profumi: nessuna categoria del catalogo li copre',
   11: 'beauty uomo: rasoi, schiuma e dopobarba, lamette',
   15: 'cura donna: assorbenti, salvaslip, incontinenza, coppetta mestruale',
   17: 'salutistica: integratori detox, drenanti, barrette proteiche: non sono generi alimentari normali',
   24: 'pubblicità: l\'app Bennet, nessun prezzo di spesa',
   25: 'pubblicità: il servizio Bennet Drive (ordina online, ritira in negozio), nessun prezzo di spesa',
   26: 'pubblicità: catalogo Bennet Club 2026, nessun prezzo di spesa',
   27: 'retro: iniziativa «Noi amiamo la scuola» e informazioni sui punti vendita, nessun prezzo di spesa',
 },
 # Guardate una per una il 2026-09-20, leggendo il volantino per intero.
 'eurospin24': {
   16: 'abbigliamento e calzature uomo/donna, pigiami Disney, ciabatte: nessuna categoria del catalogo li copre',
   17: 'elettrodomestici ed elettronica (borracce, spazzole, cuscini, misuratore di pressione, scopa a vapore, smart TV, lavasciuga)',
   18: 'mobili e accessori bagno (mobiletti, accappatoio, asciugamani, bilancia, asciugacapelli, pattumiera)',
   19: 'articoli di riponimento e casalinghi in plastica, ferro da stiro, deumidificatori: nessuna categoria del catalogo li copre',
   20: 'pubblicità viaggi Eurospin Viaggi, speciale montagna inverno: nessun prezzo di spesa',
   21: 'pubblicità viaggi Eurospin Viaggi, mare ed estero: nessun prezzo di spesa',
 },
 # Guardate una per una il 2026-09-22, leggendo il volantino per intero (52 pagine).
 'lidl24': {
   6:  'pubblicità "Freschezza in tutti i sensi" sulle zucchine di Reggio Calabria: nessun prezzo',
   7:  'pubblicità premio "Sicurezza Alimentare Frutta e Verdura": nessun prezzo',
   19: 'pubblicità: accettazione Buoni Pasto, nessun prezzo di spesa',
   22: 'abbigliamento bambini Lupilu (giacche, joggers): nessuna categoria del catalogo li copre',
   23: 'abbigliamento bambini Lupilu (pullover, felpe, leggings, jeggings)',
   24: 'abbigliamento e giochi bambini (pigiami, calze, boxer, colori acrilici, decorazioni per feste)',
   25: 'abbigliamento e stivali impermeabili per bambini Lupilu',
   26: 'Auto e Garage Ultimate Speed: powerbank, compressori, caricabatterie, tappeto garage',
   27: 'Auto e Garage Ultimate Speed: tappetini, coprisedili, protezioni parabrezza, estintore',
   28: 'prodotti per la pulizia auto W5 (panni, spray, deodoranti per auto)',
   29: 'pubblicità: vantaggi partner Lidl Plus (parchi, viaggi, assicurazioni), nessun prezzo di spesa',
   30: 'Auto e Garage Parkside: avvitatori e chiavi a bussola',
   31: 'Auto e Garage Parkside: compressore, tubi, banco da lavoro',
   32: 'Auto e Garage Parkside: chiavi dinamometriche, kit cambio pneumatici, attrezzi',
   33: 'pubblicità: sondaggio "Insegna dell\'Anno", nessun prezzo di spesa',
   34: 'elettrodomestici SilverCrest (bollitore, frullatori)',
   35: 'elettrodomestici SilverCrest (macchina caffè, spremiagrumi, tritatutto, caffettiera Bialetti)',
   36: 'casalinghi SilverCrest (tostapane, pentole in ghisa, contenitori, borraccia)',
   37: 'Fai da te e Giardino Parkside: aspiratore, sega circolare, martello demolitore',
   38: 'Fai da te e Giardino Parkside: fresatrice, pannello organizer, pantaloni da lavoro',
   39: 'Fai da te e Giardino Parkside: scalpelli, righello, guanti, colla',
   40: 'Fai da te e Giardino Parkside: localizzatore, pinza rivettatrice, pinza multiuso',
   41: 'Fai da te e Giardino Parkside: pistola sparapunti, prolunga, morsetti',
   42: 'Fiori e Piante (crisantemi, rododendro, conifere, calluna): nessuna categoria del catalogo li copre',
   43: 'Fiori e Piante da interno (orchidee, piante grasse, sansevieria, fiori recisi)',
   50: 'pubblicità Lidl Viaggi: hotel a Parma, nessun prezzo di spesa',
   51: 'pubblicità Lidl Viaggi: montagna, terme e Madrid, nessun prezzo di spesa',
 },
 # Guardate una per una il 2026-09-22, leggendo il volantino per intero (16 pagine).
 'ekom22': {
   1:  'copertina: solo il titolo «I più ekonomici» e le date, nessun prezzo',
   12: 'concorso a premi "Punta in alto: Up&Vinci" della carta fedeltà EKOM UP: come partecipare, nessun prezzo di spesa',
   13: 'pubblicità app EKOM UP: offerte riservate e coupon, nessun prezzo di spesa qui (le offerte riservate vere stanno nella pagina dopo)',
 },
 # Guardate una per una il 2026-09-24, leggendo il volantino per intero (7 pagine).
 'lidlfv24': {
   5: 'pubblicità storytelling sulle zucchine Cladi (raccolta, QR code), nessun prezzo',
   6: 'pubblicità premio "Sicurezza Alimentare 2026" per la frutta e verdura, nessun prezzo',
 },
}
