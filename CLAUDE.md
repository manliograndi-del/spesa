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
- **In fondo, ogni volantino dell'elenco ha due tasti** (chiesti il 2026-09-18):
  **«Le offerte (N)»** apre le offerte lette da quel volantino, divise per
  reparto, e **«Il volantino ↗»** apre la sua prima pagina sul sito di chi lo
  pubblica. Tutti e due in una **pagina nuova**, come ha chiesto lui. Regole da
  non cambiare: il numero sul tasto è quello che vale **oggi** (un volantino
  scaduto non ha il tasto, ha la scritta spenta «offerte scadute»); dentro
  quelle offerte **non c'è il bollino verde**, che lì vorrebbe dire «il meno
  caro di questo negozio» e si leggerebbe «di tutti»; il pannello è quello
  della ricerca, che sta **fuori dalla `.barra`**. La pagina nuova è la pagina
  stessa con `#volantino=...` in coda: non ci sono pagine generate in più.
- **La finestra «Cosa c'è di nuovo» si apre alla prima apertura** (chiesta il
  2026-09-18) e racconta **l'interfaccia, non i prezzi**: cosa si può fare
  adesso che prima non si poteva, a partire dalla casella di ricerca. I prezzi
  nuovi restano nel tasto «Novità» in alto a destra. **Dentro non ci vanno
  offerte né prezzi**, e la prova `prova-novita-pagina.js` se ne accorge. Le
  novità nuove si aggiungono in fondo a `NOVITA_PAGINA` in `pagina.py`, con la
  data davanti all'id: chi le ha già viste vedrà comparire **solo quella
  nuova**.
- **Una novità falsa è peggio di nessuna novità: manda uno in negozio.** Vale
  per il diario e per i prezzi: se un conto è ambiguo (peso sgocciolato, prezzo
  valido solo comprandone tre), si sceglie il numero che NON fa sembrare
  l'offerta più conveniente di quello che è, e lo si scrive nella nota.

## Dove va Manlio

**Mercatò di via Filadelfia 232**, insegna Mercatò semplice — confermato da lui
il 2026-09-05, non dedotto. A Torino ci sono anche Mercatò Local, Big ed Extra,
con volantini diversi: il più vicino a corso Siracusa è un Local, quindi la
distanza da sola avrebbe scelto il negozio sbagliato.

## Da fare adesso (aggiornato il 2026-09-18)

- **Fatta il 2026-09-18 la finestra «Cosa c'è di nuovo»**, chiesta da Manlio:
  si apre da sola la prima volta e elenca le novità della pagina (casella di
  ricerca, Ekom, due tasti sui volantini). Chi l'ha già vista non la rivede;
  chi torna dopo una novità nuova vede solo quella.

- **Aggiunta l'insegna Ekom il 2026-09-18**, chiesta da Manlio. Volantino
  «1+1» dell'8-21 settembre (`ekom08`), letto per intero: 16 pagine, 138
  prezzi. **Scade il 21 settembre**: il successore (dal 22) su kimbino non
  c'era ancora il 18, **da cercare nei prossimi giorni**. La fonte è kimbino
  come per il Mercatò, quindi gli indirizzi delle pagine stanno uno per uno in
  `strumenti/pagine_ekom.py` e **vanno rifatti a ogni volantino nuovo**. A
  Torino ci sono più Ekom ma **il volantino è lo stesso per tutti** (l'unico
  diverso è quello della Toscana): niente da scegliere come col Mercatò.
  **Le pagine 1+1**: la riga dice nel formato che sono due confezioni
  («2 × 300 g (1+1)») e la nota dice quanto costa una confezione sola — in
  NOTE.md c'è il perché, non cambiarlo senza chiederglielo.

- **Fatti il 2026-09-18 i due tasti su ogni volantino in fondo alla pagina**,
  chiesti da Manlio: «Le offerte» e «Il volantino», tutti e due in una pagina
  nuova. Pubblicati sul sito e sull'artifact, `sw.js` a v38. In NOTE.md c'è il
  perché di ogni scelta; la prova nuova è `prova-volantini.js`, dentro
  `prove.sh`.

- **Il 2026-09-17 il ramo `main` era rimasto indietro di 36 commit**: le
  sessioni del 15 e 16 settembre avevano lavorato e pubblicato l'Artifact, ma
  avevano spinto (`git push`) su un ramo secondario invece che su `main`, e il
  sito pubblico (che legge da `main`) era rimasto fermo a `sw.js` v27 per
  giorni, senza il Mercatò 17-30, il Carrefour Iper, il Bennet e il Lidl.
  **Sistemato oggi** portando `main` avanti fino a quel lavoro (fast-forward,
  nessun commit perso) e verificato che il sito online lo mostri davvero. **Da
  qui in poi: dopo ogni `git push`, controllare che sia andato su `main` (non
  su un ramo con un altro nome) prima di dire che è pubblicato.**
- **Uscito e preso un volantino Lidl in più, non un successore**: uno
  speciale «Frutta e Verdura» di 7 pagine, `lidlfv17`, valido come il Lidl
  generale (17-23 settembre) ma con offerte sue, aggiuntive. Letto per intero:
  12 prezzi nuovi (mele, susine, cavoli, aglio, rape rosse, uva, cetrioli
  snack, limoni). Tre suoi prodotti (Pere Williams, Patate Selenella, Zucca
  Butternut, Uva di Mazzarrone, Carote del Fucino, Pesche) ripetevano
  identici, stesso prezzo, quelli già letti nel Lidl generale 17-23: non
  riscritti, sennò `dati.py` si ferma per riga doppia. Tre prodotti (Cetrioli
  lunghi, Mango, Fichi freschi) erano «al pezzo» senza un peso indicato:
  nessun prezzo per unità onesto da scrivere, lasciati fuori. Una pagina
  scartata (pubblicità del premio «Sicurezza Alimentare»), in `scartate.py`.
- **Letto per intero il 2026-09-18: MD nuovo, dal 22 settembre al 4 ottobre**
  (`md22`, 37 pagine). 131 prezzi nuovi, in quasi tutti i reparti (macelleria,
  gastronomia, freschi, surgelati, dispensa, bevande, casa, più uno speciale
  Sardegna e un weekend «Weekend più Uno» valido solo dal 2 al 5 ottobre — le
  date sono scritte sulle singole righe). Alcuni prezzi valgono solo con la
  MD Buona Spesa Card: scritto nella nota di ogni riga, col prezzo pieno
  accanto. 13 pagine scartate (accessori cucina, casalingo, cura persona,
  tessile, e-mobility, viaggi, una pagina ricetta): in `scartate.py`.
- **Trovato ma non ancora letto: Bennet nuovo, «Un mondo di bellezza», dal 17
  al 30 settembre** (`bennet1709`). Uscito mentre `bennet10` (10-23) era
  ancora valido — la stessa sovrapposizione del «Dolce Buongiorno» di
  settembre, che aveva già fatto perdere sei giorni. Non è solo bellezza: da
  pagina 18 in poi ci sono alimentari, surgelati e casa. Aggiunto a
  `VOLANTINI` con l'indirizzo delle 27 pagine, ma **nessuna ancora letta**:
  **va letto per intero nei prossimi giorni**, prima che `bennet10` scada.
- **Trovato, da tenere d'occhio: Eurospin dal 24 settembre al 4 ottobre**
  (`volantino-eurospin-dal-24-settembre-2026` su anteprimavolantino), non
  ancora aggiunto a `dati.py`. **C'è un buco di 4 giorni** fra la fine di
  `eurospin10` (20 settembre) e questo (24 settembre): controllare nei
  prossimi giorni se esce qualcosa che lo riempie, prima di prenderlo.
- **Carrefour Iper, Ipercoop: nessuna novità il 2026-09-18.** Carrefour Iper
  fermo a `carriper15` (fino al 28); Ipercoop/Nova Coop ancora solo «Scegli tu
  Grandi Marche», tutto sconti percentuali senza un prezzo di base: non
  utilizzabile. **Da controllare di nuovo fra qualche giorno.**
- **Mercatò vecchio (`mercato`), Bennet Dolce Buongiorno (`bennet0903`) e
  Lidl (`lidl10`) sono scaduti il 16 settembre**, e sono già coperti
  (rispettivamente da `mercato17`, `bennet10` e `lidl17`, senza buchi): il
  2026-09-18 `pulisci` li segna ancora "da rinnovare" (−2 giorni, non ancora
  −3) per il margine di due giorni voluto da Manlio. **Da togliere il primo
  giorno utile** con `pulisci --fai`, da `dati.py`, `VOLANTINI` e
  `scartate.py`.
- **Il Carrefour Iper (`carriper15`, 15-28 settembre) è a posto, non
  riaprire la questione.** L'ultima pagina del suo volantino elenca gli
  ipermercati in cui vale e Torino non c'è: il 2026-09-07 Manlio ha detto che
  è sbagliato fermarsi lì — «le offerte ci sono a Torino e valgono davvero».
  In NOTE.md c'è per esteso.
- **Copertura letta: tutti i volantini con prezzi in `dati.py` al 100%**
  (mercato, bennet0903, bennet10, lidl10, lidl17, lidlfv17, eurospin10, md08,
  carriper15, mercato17, md22). `bennet1709` è appena trovato, 0 pagine lette.
- **Scadenze da tenere d'occhio nei prossimi giorni**: `md08` ed `eurospin10`
  scadono il 20 settembre, `bennet10` il 23, `lidl17` e `lidlfv17` il 23
  (occhio: nel Lidl 17-23 la «Panetteria» vale solo dal 17 al 20, e alcune
  offerte «Il meglio del lunedì» valgono solo dal 21 al 23 — già segnato
  nelle note delle singole righe). `mercato17` scade il 30, `bennet1709` pure.
  `md22` scade il 4 ottobre. La pagina Oktoberfest del Bennet (pagine 20-21 di
  `bennet10`) scade il 4 ottobre, non il 23 come il resto — occhio quando si
  ributta il volantino.
- **Il giro automatico non funziona, e non è un mistero da risolvere leggendo
  il codice**: parte, lavora pochi minuti e non lascia traccia. In NOTE.md c'è
  quello che si sa e quello che non si sa, e perché a mano riesce. Finché non lo
  si vede arrivare in fondo più volte di fila, **i volantini si mettono a
  mano**. **Il 2026-09-10, il 2026-09-15, il 2026-09-16, il 2026-09-17 e il
  2026-09-18 la sessione da Routine è arrivata in fondo**: ha letto un
  volantino per intero (o più) e pubblicato — ma il 17 settembre si è
  scoperto che le pubblicazioni del 15 e del 16 non erano davvero arrivate al
  sito (vedi sopra): un «pubblicato» nel registro non basta, va controllato
  che sia finito su `main`. Il 2026-09-18, dopo il push, verificato che
  `index.html` scaricato dal sito online combaciasse byte per byte col file
  appena pubblicato.
- **Il buco del diario è chiuso (2026-09-15), e `.gitignore` non si tocca.**
  `storia/stato.json` resta fuori dal repository — «le fotografie no, le
  differenze sì» — ma **non serve più che sopravviva**: se manca, `storia.py`
  **rifà la fotografia da git**, tirando fuori `strumenti/` dall'ultimo commit
  che ha toccato `dati.py` e leggendolo con il `fotografia()` di adesso. La
  fotografia è solo una lettura di `dati.py`, e `dati.py` nel repository c'è.
  In più `storia.py` **riempie i giorni rimasti indietro uno per uno**, con la
  loro data e col `dati.py` in vigore quel giorno: un giorno può avere novità
  vere **senza che nessuno tocchi i prezzi**, perché a mezzanotte un volantino
  scade e il più conveniente di quella categoria diventa un altro. Così sono
  stati recuperati i giorni dal 10 al 15 settembre, che erano vuoti.
  **Da qui in poi `python3 -m storia` va lanciato PRIMA di committare**: il
  confronto è fra l'ultimo commit e quello che c'è adesso nella cartella.
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
