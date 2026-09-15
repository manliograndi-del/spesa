# Spesa — memoria di progetto

Leggi tutto questo file prima di toccare qualsiasi cosa.
La storia lunga, col perché di ogni scelta, sta in **`NOTE.md`** (1200 righe):
vacci quando questo file non basta, e **prima di rifare qualcosa che sembra
mancare** — quasi sempre è già stato provato e c'è scritto com'è andata.

## Chi è l'utente e come lavora

Manlio. **Non legge il codice** e non usa il terminale. Verifica il lavoro in un
solo modo: apre l'indirizzo sul telefono e guarda se l'app fa quello che deve.

Conseguenze operative, e non sono formalità:
- **Spiegagli cosa cambia PER LUI, non cosa hai fatto tu.** Il 2026-09-06 gliel'ho
  raccontata al contrario — pagine lette, controlli aggiunti, percentuali — e lui:
  «io da quello che c'è scritto non lo capisco, io ti ho chiesto di migliorare
  un'applicazione». Aveva ragione. Quanto lavoro è costato non è un risultato.
- Non chiedergli di leggere un diff, un file, un numero di riga.
- Un file in una cartella temporanea, per lui, **non esiste**: se deve averlo,
  serve un indirizzo pubblico.
- Scrivi in italiano.
- Non lasciare mai il repo in uno stato non funzionante fra una sessione e l'altra.

## Cos'è

Una pagina che cerca i prodotti suoi nei volantini dei supermercati vicini a
casa (Torino, corso Siracusa). Ogni prodotto è un bottone: lo tocchi ed escono
le offerte, dalla più conveniente in giù, col prezzo per unità. Chi non trova
quello che vuole lo accende da un catalogo di 67 voci diviso per reparto.

Pubblicata in due posti, **e vanno aggiornati tutti e due**:
- il sito, `https://manliograndi-del.github.io/spesa/` — un commit su `main`
- l'artifact, il link che ha anche sua moglie — `Artifact` con lo stesso URL

## Vincoli tecnici — non negoziabili senza chiederglielo

1. **I prezzi si leggono a occhio dalle pagine dei volantini.** L'OCR non legge
   le scritte grandi: serve a trovare la pagina, non il prezzo. I riassunti
   online sbagliano — tre errori trovati e documentati in NOTE.md.
2. **Non si pubblicano i PDF né le immagini dei volantini.** Solo collegamenti
   ai siti di chi li mette online.
3. **Mai scrivere il tag di chiusura dello script per esteso** dentro il codice
   della pagina, commenti compresi: spezza la pagina a metà, in silenzio.
4. **Nel CSS non esiste `prefers-color-scheme: dark`.** Il telefono di Manlio è
   in modalità notte e la pagina gli si apriva nera.
5. **Prima di rigenerare, si legge la lista viva dalla pagina pubblicata.** Se
   non si riesce a leggerla, ci si ferma senza pubblicare: rigenerare a vuoto
   cancella la lista di prodotti loro.
6. **A ogni rilascio si alza il numero di cache in `sw.js`** (`spesa-v29` →
   `spesa-v30`), se no resta in giro la copia vecchia.
7. Il progetto della palestra (`manliograndi-del/palestra`) **non si tocca**.

## Come si rifà

    export PYTHONPATH=<progetto>/strumenti
    python3 -m scarica <chiave>    # le pagine del volantino
    bash <progetto>/strumenti/leggi.sh    # OCR di ogni pagina
    python3 -m indice              # aggiorna indice.json
    python3 -m pagina              # le tre copie in out/
    python3 -m storia              # il diario delle novità del giorno
    python3 -m novita              # la pagina delle novità (tasto in alto a destra)
    python3 -m stampa              # il PDF del catalogo da stampare
    python3 -m lette               # quante pagine ho letto davvero
    bash <progetto>/strumenti/prove.sh    # TUTTE le prove
    python3 -m pulizia out/sito.html      # codice rimasto in giro

Poi `cp out/sito.html index.html`, `cp out/novita.html novita.html`,
`cp out/catalogo.pdf catalogo.pdf`, alza `sw.js`, commit, push, e ripubblica
l'artifact.

**`prove.sh` è il comando che conta.** Una pagina che non passa non si pubblica.
Serve `npm install` dentro il progetto.

## Come si leggono i volantini — la parte che ho sbagliato tre volte

**Si leggono per intero, pagina per pagina.** NON si interroga l'indice delle
parole per aprire solo le pagine che rispondono: così si trova soltanto quello
che si è già pensato di cercare. Le pizze, Mercatò e il pesce sono lo stesso
errore tre volte, e Manlio se n'è accorto tutte e tre da fuori.

- **Una categoria con zero o una sola offerta è quasi sempre un buco mio, non il
  mondo.** Se sei supermercati su sette non hanno la pizza, non è il mondo.
- **Prima i volantini che durano**, non i più trascurati: leggere 52 pagine di
  un volantino che scade fra quattro giorni è tempo buttato.
- **`python3 -m lette`** dice la copertura, e `lette <chiave>` elenca le pagine
  mai aperte. Al 2026-09-09: 160 pagine lette su 313. Mercatò, Carrefour Iper e
  il Bennet «Dolce Buongiorno» sono al 100%, letti per intero.
- **Cercare i volantini nuovi non è la stessa cosa che guardare le scadenze.**
  `pulisci.py` dice solo cosa sta scadendo di quello che hai già. Le insegne però
  pubblicano volantini che si sovrappongono: il Bennet «Dolce Buongiorno» è
  uscito il 3 settembre mentre il Bennet vecchio era ancora valido, e per sei
  giorni non l'ha visto nessuno. **A ogni giro guarda anche cosa è USCITO**, non
  solo cosa muore.
- Una pagina di quaderni, pubblicità o punti premio **si scarta**, e si scrive
  in `strumenti/scartate.py` col motivo, così non torna nell'elenco delle cose
  da fare. Regola sua: «una volta che l'hai vista, lasciala perdere».
  **Ma si scarta solo dopo averla APERTA**, mai dal titolo o dall'OCR: è così
  che mi ero perso una pagina intera di pescheria del Bennet.

## Trappole già pagate, che il programma adesso blocca da solo

`dati.py` si ferma con un errore se ne rifai una. Non toglierle.

- **Righe doppie** (stessa insegna, stesso prodotto, stesso formato): rileggendo
  un volantino ne ho riscritte dieci, e la stessa offerta compariva due volte.
- **Date ripetute dal volantino**: scrivere su una riga le stesse date del
  volantino che la contiene la fa passare per «offerta ristretta», e una
  ristretta non ancora cominciata **non si mostra affatto**. Mi ha reso
  invisibili 22 righe senza che niente lo segnalasse. Le date sulla riga
  servono solo al caso vero (la pagina «Weekend più uno» dell'MD).
- **Categorie fuori catalogo**: un prezzo in una categoria che non esiste
  verrebbe caricato e non mostrato a nessuno, in silenzio.

## Regole della pagina decise con lui

- **L'elenco è in ordine di prezzo e basta.** Niente eccezioni in fondo. Il
  bollino verde «il meno caro» va al meno caro **che vale oggi**, che può non
  essere la prima riga.
- **Ogni riga dice fino a quando vale.** I volantini durano periodi diversi.
- Le offerte scadute spariscono da sole: il giudizio lo dà il browser di chi
  guarda, con la sua data, non il programma che genera.
- **«Cerca fra i prezzi» cerca fra TUTTE le offerte, non nel catalogo.** È il
  tasto tratteggiato accanto a «+ altri prodotti», ed è un'altra cosa dalla
  casella dentro il cassetto: quella accende i prodotti della lista, questa
  trova una singola offerta fra tutte quelle lette (marca, formato, insegna,
  note). Chiesto il 2026-09-15: «trovare esattamente un singolo prodotto fra
  tutte le offerte». Due regole sue, da non cambiare:
  - **nei risultati NON c'è il bollino verde «il meno caro»**. Lì dentro il
    verde vorrebbe dire «il meno caro di quello che hai scritto», e uno
    leggerebbe «il meno caro della categoria»: una novità falsa.
  - **il pannello sta FUORI dalla `.barra`**, per la stessa ragione del
    cassetto: la barra è appiccicata in alto e se le cresce dentro qualcosa
    il telefono si blocca a ogni scorrimento.
  Cassetto e ricerca **non stanno aperti insieme**: aprirne uno chiude l'altro.
  - **il tasto è rosso pieno e su una riga tutta sua** (`.tasto.trova`), dal
    2026-09-15: tratteggiato e grigio come «+ altri prodotti» Manlio non lo
    vedeva. Rosso pieno **in mezzo alle pastiglie** non si poteva: lì il rosso
    pieno vuol dire «prodotto acceso». Da solo, largo quanto lo schermo, no.
    Il bottone **tiene anche la classe `agg`**: è con quella che tutte le
    prove riconoscono i bottoni che non sono prodotti della lista.
- **Una novità falsa è peggio di nessuna novità: manda uno in negozio.** Vale
  per il diario e per i prezzi: se un conto è ambiguo (peso sgocciolato, prezzo
  valido solo comprandone tre), si sceglie il numero che NON fa sembrare
  l'offerta più conveniente di quello che è, e lo si scrive nella nota.

## Dove va Manlio

**Mercatò di via Filadelfia 232**, insegna Mercatò semplice — confermato da lui
il 2026-09-05, non dedotto. A Torino ci sono anche Mercatò Local, Big ed Extra,
con volantini diversi: il più vicino a corso Siracusa è un Local, quindi la
distanza da sola avrebbe scelto il negozio sbagliato.

## Da fare adesso (aggiornato il 2026-09-15)

- **È uscito il nuovo Lidl (dal 17 al 23 settembre, 36 pagine)** e oggi è stato
  letto per intero e pubblicato, in anticipo — al 15 settembre non era ancora
  cominciato, ma le pagine vere c'erano già sulla fonte. 56 righe nuove in
  `dati.py`: molte pagine erano nella sezione «formato XXL» e «Super Offerte»,
  con prodotti veri (carne, pesce, salumi, formaggi, vino) a fianco di roba
  senza prezzo utile (barrette proteiche, cosmetici, abbigliamento, utensili da
  giardino, specialità orientali, fiori) — tutta scartata e segnata in
  `scartate.py`. La chiave è `lidl17`.
- **Il Lidl vecchio (`lidl`, quello del 3-9 settembre) è stato tolto**: era
  scaduto da tre giorni. Righe di `VOLANTINI` e `PRODOTTI` cancellate da
  `dati.py`.
- **`lidl10` (10-16 settembre) scade domani, 16 settembre**: è coperto dal
  nuovo `lidl17` che comincia il 17, senza buchi. Quando `lidl10` risulta
  scaduto da più di due giorni, va tolto con `pulisci --fai` come sempre da
  `dati.py`, `VOLANTINI` e `scartate.py`.
- **Mercatò (`mercato`) e il Bennet Dolce Buongiorno (`bennet0903`) scadono
  anche loro domani, 16 settembre**, e oggi non è stato trovato nessun
  successore su kimbino.it (Mercatò) né su anteprimavolantino.it (Bennet):
  normale, è il caso «scade ma la fonte non ha ancora pubblicato il
  sostituto» — non è un problema, si ricontrolla domani. `bennet0903` è
  comunque già coperto dal Bennet generale (`bennet10`, fino al 23), quindi
  chi cerca offerte Bennet le trova lo stesso; per Mercatò invece non c'è
  ancora un sostituto pronto — **controllare la fonte kimbino.it nei prossimi
  giorni**.
- **Il Carrefour Iper (`carriper15`, 15-28 settembre) è a posto, non
  riaprire la questione.** L'ultima pagina del suo volantino elenca gli
  ipermercati in cui vale e Torino non c'è: il 2026-09-07 Manlio ha detto che
  è sbagliato fermarsi lì — «le offerte ci sono a Torino e valgono davvero».
  In NOTE.md c'è per esteso.
- **Copertura letta: 358 pagine su 358, il 100%.** Tutti i volantini in
  `dati.py` sono stati letti per intero (mercato, bennet0903, bennet10,
  lidl10, lidl17, eurospin10, md08, carriper15). Non resta niente indietro.
- **L'Ipercoop non ha più un volantino con prezzi.** L'unico Nova Coop in
  corso («Scegli tu Grandi Marche», 10-23 settembre) è tutto sconti
  percentuali su intere linee di marca, senza mai un prezzo di base: non
  utilizzabile. **Da controllare di nuovo fra qualche giorno** se esce un
  Sottocosto o un Extra offerte veri.
- **Scadenze da tenere d'occhio nei prossimi giorni**: `md08` ed `eurospin10`
  scadono il 20 settembre, `bennet10` il 23, `lidl17` il 23 (occhio: la
  «Panetteria» del Lidl 17-23 vale solo dal 17 al 20, e alcune offerte
  «Il meglio del lunedì» valgono solo dal 21 al 23 — già segnato nelle note
  delle singole righe). La pagina Oktoberfest del Bennet (pagine 20-21 di
  `bennet10`) scade il 4 ottobre, non il 23 come il resto — occhio quando si
  ributta il volantino.
- **Il giro automatico non funziona, e non è un mistero da risolvere leggendo
  il codice**: parte, lavora pochi minuti e non lascia traccia. In NOTE.md c'è
  quello che si sa e quello che non si sa, e perché a mano riesce. Finché non lo
  si vede arrivare in fondo più volte di fila, **i volantini si mettono a
  mano**. **Il 2026-09-10 e il 2026-09-15 la sessione da Routine è arrivata in
  fondo**: ha letto un volantino per intero (o più) e pubblicato entrambe le
  volte. Sono due tentativi riusciti, non ancora una garanzia.
- **Il diario delle novità è stato riacceso il 2026-09-10**, ma il problema
  descritto allora **non è ancora risolto**: `storia/stato.json` è in
  `.gitignore` di proposito, quindi ogni sessione nuova (clone pulito) parte
  senza fotografia e scrive «prima fotografia» invece del giorno vero. È
  successo di nuovo il 2026-09-15: il diario di oggi **non risulterà come
  giorno con novità vere**, anche se il Lidl nuovo aveva 56 righe. Non ho
  toccato `.gitignore`: è una scelta loro, scritta apposta («le fotografie no,
  le differenze sì»). Da decidere con Manlio se e come fare arrivare
  `stato.json` da una sessione all'altra, ora che il tasto Novità è acceso
  davvero.
- **Manlio deve correggere a penna il catalogo** (`catalogo.pdf`, 67 voci): le
  sue correzioni vanno riportate in `strumenti/catalogo.py`. Se le manda,
  applicarle e rifare il PDF con `python3 -m stampa`.
- **Restano a lui**: reinstallare l'icona dal nuovo indirizzo e mandare il link
  alla moglie.

## File del progetto

- `index.html` — il sito pubblicato (generato, non si modifica a mano)
- `catalogo.pdf` — il foglio da stampare e correggere
- `indice.json` — le parole di ogni pagina di ogni volantino, committato
- `storia/` — il diario, un file per giorno
- `strumenti/` — catalogo, dati, pagina, storia, lette, scartate, stampa, prove
- `NOTE.md` — la storia lunga e il perché di ogni scelta
