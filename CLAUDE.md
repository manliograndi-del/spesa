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
- **Una novità falsa è peggio di nessuna novità: manda uno in negozio.** Vale
  per il diario e per i prezzi: se un conto è ambiguo (peso sgocciolato, prezzo
  valido solo comprandone tre), si sceglie il numero che NON fa sembrare
  l'offerta più conveniente di quello che è, e lo si scrive nella nota.

## Dove va Manlio

**Mercatò di via Filadelfia 232**, insegna Mercatò semplice — confermato da lui
il 2026-09-05, non dedotto. A Torino ci sono anche Mercatò Local, Big ed Extra,
con volantini diversi: il più vicino a corso Siracusa è un Local, quindi la
distanza da sola avrebbe scelto il negozio sbagliato.

## Da fare adesso (aggiornato il 2026-09-10)

- **Il Carrefour è a posto, non riaprire la questione.** L'ultima pagina del suo
  volantino elenca gli ipermercati in cui vale e Torino non c'è: il 2026-09-07
  ho concluso che a Torino valessero solo i non alimentari e ho messo un avviso
  in pagina. **Manlio ha detto che è sbagliato** — «le offerte ci sono a Torino
  e valgono davvero» — e l'avviso è stato tolto. Chi rilegge quel volantino
  ritroverà l'elenco e rifarà lo stesso ragionamento: fermati qui. In NOTE.md
  c'è per esteso.
- **Bennet e MD e Eurospin sono stati letti per intero il 2026-09-10** (bennet10,
  lidl10, md08, eurospin10: tutti 100%). Copertura totale: 278/308 pagine (90%).
  Resta indietro solo il **Lidl vecchio** (`lidl`, sottocosto fino al 12
  settembre): 6/36 pagine, ma scade fra due giorni — non vale la pena
  finirlo, si butta quando scade (vedi sotto).
- **L'Ipercoop non ha più un volantino con prezzi.** Il Sottocosto e l'Extra
  offerte sono scaduti il 9; l'unico volantino Nova Coop in corso il 10
  settembre («Scegli tu Grandi Marche», 10-23 settembre) è tutto sconti
  percentuali su intere linee di marca, senza mai un prezzo di base: non si
  può calcolare un prezzo vero, quindi non è stato usato. **Da controllare di
  nuovo fra qualche giorno** se esce un Sottocosto o un Extra offerte veri.
- **Anche il nuovo Bennet generale (bennet10, 10-23 settembre) è per lo più
  sconti percentuali** senza prezzo di base (pagine 1-13, 21-23 in parte):
  scartate. I prezzi veri stanno nelle pagine del banco fresco, pescheria,
  frutta e verdura, panetteria e nella sezione «prodotto acceleratore»
  (pagine 14-19, 30-31). La pagina Oktoberfest (20-21) scade il 4 ottobre, non
  il 23 come il resto — occhio quando si ributta il volantino.
- **Quando scadono `lidl` (12 settembre) e `lidl10` (16 settembre)**: togliere
  le loro righe da `dati.py`, `VOLANTINI` e `scartate.py` con `pulisci --fai`
  come sempre. `bennet10` scade il 23, `md08` ed `eurospin10` il 20.
- **Resta senza prezzi solo il Vitello... anzi no: trovato.** Il Bennet nuovo
  (bennet10, pagina 15) ha «Coscia a pezzi di vitello» a 17,99 al kg e «Reale
  con osso di vitello» a 9,49 al kg. Aggiornare la nota in cima a questo file
  quando si conferma che compare in pagina.
- **Il giro automatico non funziona, e non è un mistero da risolvere leggendo
  il codice**: parte, lavora quattro minuti e non lascia traccia. In NOTE.md c'è
  quello che si sa e quello che non si sa, e perché a mano riesce. Finché non lo
  si vede arrivare in fondo almeno una volta, **i volantini si mettono a mano**.
  **Il 2026-09-10 la sessione da Routine è arrivata in fondo per la prima
  volta**: ha letto quattro volantini per intero e pubblicato. Non è ancora
  una garanzia — è un tentativo riuscito — ma è la prima prova che si può fare.
- **Il diario delle novità è stato riacceso il 2026-09-10** da un'altra sessione
  (su richiesta diretta di Manlio) **e questo ha smascherato il problema che
  prima non faceva danno**: `storia/stato.json` è in `.gitignore` di proposito,
  quindi ogni sessione nuova (clone pulito) parte senza fotografia e scrive
  «prima fotografia» invece del giorno vero. La sessione di oggi ha rigenerato
  `storia` due volte (una dell'altra sessione, una di questa) e la seconda ha
  perso il confronto della prima: il 10 settembre in `storia/` **non risulterà
  come giorno con novità vere**, anche se ne aveva parecchie (quattro volantini
  aggiornati). Non ho toccato `.gitignore`: è una scelta loro, scritta apposta
  («le fotografie no, le differenze sì»). Da decidere con Manlio se e come
  fare arrivare `stato.json` da una sessione all'altra, ora che il tasto
  Novità è acceso davvero.
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
