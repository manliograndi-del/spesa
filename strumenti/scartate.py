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
}
