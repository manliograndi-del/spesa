# Spesa — memoria di progetto

Leggi tutto questo file prima di toccare qualsiasi cosa.
La storia lunga, col perché di ogni scelta, sta in **`NOTE.md`** (1200 righe):
vacci quando questo file non basta, e **prima di rifare qualcosa che sembra
mancare** — quasi sempre è già stato provato e c'è scritto com'è andata.

**Esiste anche `AGENTS.md`, copia di questo file** fatta il 2026-09-22 perché
Manlio prova il progetto con un altro programma (Antigravity) oltre a Claude.
**Chi aggiorna questo file aggiorni anche quello**, almeno la parte «Da fare
adesso»: se restano diversi, la prossima sessione — di uno dei due programmi —
parte da informazioni vecchie.

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

**GitHub Pages pubblica solo da `main`.** Chi lavora dentro Claude Code parte
spesso da un ramo di lavoro diverso (assegnato dalla sessione, non scelto):
committare e spingere lì NON aggiorna il sito, anche se le prove passano e
tutto sembra a posto. Il 2026-09-23 `main` era rimasto indietro di nuovo
(stessa cosa del 17 settembre, vedi NOTE.md): il lavoro del giorno prima era
tutto sul ramo di lavoro e mai arrivato a `main`. **Prima di dire «pubblicato»,
porta sempre `main` avanti fino al ramo di lavoro** (`git push origin
HEAD:main`, un fast-forward: sicuro, non riscrive storia) e verifica scaricando
`index.html` dal sito e confrontandolo byte per byte col file appena
pubblicato — non basta che il push sia andato a buon fine.

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
    python3 -m variante            # la versione di prova (prova-tasti-sotto.html), finché c'è
    python3 -m stampa              # il PDF del catalogo da stampare
    python3 -m lette               # quante pagine ho letto davvero
    bash <progetto>/strumenti/prove.sh    # TUTTE le prove
    python3 -m pulizia out/sito.html      # codice rimasto in giro

Poi `cp out/sito.html index.html`, `cp out/novita.html novita.html`,
`cp out/catalogo.pdf catalogo.pdf`, `cp out/prova-tasti-sotto.html .` (finché c'è la prova), alza `sw.js`, commit, push, e ripubblica
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
- **Se il prezzo per unità e quello della confezione sono lo stesso numero,
  si scrive una volta sola** (chiesto il 2026-09-22: «ci sono dei prodotti col
  prezzo al kg che corrisponde al prezzo al pezzo, soprattutto nei salumi ma
  anche negli altri prodotti da banco, che chiaramente non sono confezionati;
  puoi toglierli nel caso in cui coincidano»). Riguarda tutto quello che si
  vende sfuso — al kg, al banco: lì la confezione non esiste, e ripetere
  «12,99 € al kg» e «12,99 € al pezzo» era lo stesso numero due volte.
  Sparisce sia il secondo prezzo (`.val .p2`) sia il «… € la confezione»
  nella riga del formato; resta «Formato: al kg · fino al 28 settembre».
  Il confronto si fa sui numeri **come vengono scritti** (`eur`), non sui
  decimali interi. Sono 296 offerte su 1387. La prova è `prova-meno-caro.js`,
  che adesso controlla le due strade: o c'è scritto quanto costa la
  confezione e allora il secondo prezzo c'è, o non c'è né l'uno né l'altro.
  **Resta da decidere con lui** il caso dei banchi all'etto (il prosciutto a
  2,59 all'etto e 25,90 al kg): lì i numeri sono diversi, ma la scritta
  «al pezzo» non è giusta — un etto non è un pezzo.
- **I nomi delle categorie sono di UNA PAROLA SOLA** (chiesto il 2026-09-22:
  «i bottoni delle categorie tengono troppo posto, bisogna assolutamente
  rimpicciolirli… tutte le categorie che hanno più di una parola, se è
  possibile, devono essere ridotte a una sola parola, e prosciutto crudo e
  cotto riuniti; le cose surgelate, è inutile dire che sono surgelate»).
  Su 66 voci ne restano quattro con due parole, e ognuna ha il suo motivo:
  **Olio d'oliva** e **Olio di semi** (accorciarli li confonderebbe fra loro),
  **Carta igienica** (da sola «Igienica» non si legge) e **Verdure surgelate**
  (da sola «Verdure» si confonderebbe con la **Verdura** fresca, che è un'altra
  categoria). **Prosciutto crudo e cotto sono una voce sola, «Prosciutto».**
  - **La tabella `RINOMINATE` in `catalogo.py` non si cancella mai.** I nomi
    vecchi sono scritti nella lista salvata nel telefono di Manlio e in quello
    di sua moglie: la tabella fa sì che il loro bottone prenda il nome nuovo
    senza perdere niente. Senza, «Pesce fresco» non si riaggancerebbe affatto
    (il riaggancio va per nome e per parole del volantino, e fra le parole del
    pesce la parola «pesce» non c'è apposta). Chi si è rinominato un prodotto
    a modo suo non viene toccato.
  - Serve anche a **`storia.py`**, che la usa per tradurre la fotografia
    vecchia prima di confrontarla: senza, il diario avrebbe annunciato che
    393 offerte «hanno cambiato reparto». Una novità falsa.
  - **Le parole con cui si cerca nei volantini non si toccano**: il nome corto
    è solo quello che si legge sul bottone. La ricerca nelle pagine usa le
    `parole`, non il nome (per questo «Pesce» può chiamarsi così senza tirare
    dentro i bastoncini e i sughi di pesce).
- **Le pastiglie dei prodotti sono basse 34 px, non 44** (stessa richiesta):
  scritta da 14 px, poco imbottitura, 6 px fra una e l'altra. Anche le schede
  delle offerte sono più compatte (meno aria, non meno roba): stesso
  contenuto, angoli 16 px, prezzo grande 26 px.
- **Il tasto rosso si chiama «Cerca un prodotto o una marca»** ed è una
  pastiglia alta 42 px (scelto da lui il 2026-09-22 fra tre proposte; prima
  diceva «Cerca fra i prezzi di tutte le offerte», che era lungo il doppio).
  Quello che la scritta non dice più — che cerca fra **tutte** le offerte
  lette, non fra i prodotti della lista — **resta scritto nell'Aiuto** e nella
  casella che si apre. Se si cambia ancora il nome del tasto, va cambiato
  anche l'Aiuto: `prova-aiuto.js` controlla che i due combacino.
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
- **La pagina Novità comincia dai volantini, non dai prezzi** (chiesto il
  2026-09-19): in cima il riquadro **«Volantini aggiornati»** (nuovi, riletti,
  finiti) sulla finestra scelta — i tasti sono **Oggi / 3 giorni / 7 giorni** —
  poi la **tabella di tutti i volantini** (in corso, in arrivo, appena finiti)
  e solo dopo il diario dei prezzi. I volantini che so in arrivo ma non ho
  ancora letto stanno in **`VOLANTINI_ATTESI`** in `dati.py` e in tabella sono
  segnati «prezzi non ancora letti»: si tolgono di lì appena il volantino
  entra in `VOLANTINI`. La prova è `prova-novita.js`.
- **L'impaginazione è a schede, decisa il 2026-09-22 su una schermata che ha
  mandato lui**: «l'impaginazione è più bella così, con tutto messo in pillole
  e ordinato». In cima il marchio della pagina (quadratino rosso «S»), il
  titolo **«Spesa»**, il sottotitolo, i quattro tasti (Look, Novità app,
  Aiuto, Novità) e la riga **«Data di riferimento: …»**. Poi il tasto rosso
  **«Cerca fra i prezzi di tutte le offerte»**, largo quanto lo schermo e
  **fuori dalla barra appiccicata**. Poi «I tuoi prodotti (N)» con le
  pastiglie. Regole da non cambiare:
  - **Ogni offerta è una scheda** (`.prezzo-riga`), con in cima il marchio del
    negozio e i bollini, poi nome, formato e prezzo della confezione, la nota
    in un riquadro ambra e a destra i due prezzi (al pezzo e per unità).
    **In fondo alla scheda non c'è niente**: la scritta «Vedi tutte le offerte
    del volantino» c'era e Manlio l'ha fatta togliere lo stesso giorno,
    «è inutile» — quelle offerte si aprono dal tasto del volantino in fondo
    alla pagina.
  - **Il negozio è un MARCHIO, non una scritta** (`.marchio`, chiesto il
    2026-09-22: «mettici il marchio dei supermercati»). Dove il marchio c'è
    davvero (cinque su otto) è quello vero, da `strumenti/loghi/`; dove non
    c'è, è il nome dell'insegna scritto nei suoi colori, con fondo e scritta
    fissati tutti e due così da leggersi uguale con qualunque look. Le prove
    riconoscono il negozio da `.marchio`, non più da `.sotto b`.
  - **La scelta dei negozi C'È, dentro la configurazione** (chiesta da lui il
    2026-09-22 notte: «ci dovrebbe essere anche un tasto per scegliere i
    supermercati: appare l'elenco completo e tu scegli quello che vuoi»).
    Prima, lo stesso giorno, era stata chiesta e rifiutata due volte: adesso
    l'ha chiesta lui, e vale questo. Ancora NIENTE contatore «7 su 7» in cima.
  - **Sotto i 560 px la scheda va in colonna**: i prezzi scendono su una riga
    loro. A due colonne, sul telefono, il nome andava a capo ogni due parole.
  - Nessuna riga dice più **«letto a occhio dal volantino»**: tolta su sua
    richiesta.
- **In cima NON c'è più «Torino · corso Siracusa» né il bollino «i»**
  (tolti il 2026-09-22 su richiesta sua: «è inutile»). Quello che stava
  dietro quel bollino — com'è fatta questa copia, se è solo sua o condivisa —
  è in fondo alla finestra «Aiuto». Il bollino «i» accanto al NOME DEL
  PRODOTTO è un'altra cosa e resta.
- **In cima NON c'è più nemmeno la riga «Data di riferimento: …»** (tolta il
  2026-09-22 su richiesta sua, come «Torino · corso Siracusa» prima di lei:
  spazio occupato da una cosa che non si tocca per fare niente). La data del
  telefono continua a comandare quello che conta — cosa è scaduto, quanti
  giorni mancano, quale offerta si può comprare oggi — solo non è più scritta
  lì in mezzo.
- **Il tasto dei cento look si chiama «Colori»** (chiesto il 2026-09-22:
  «sostituisci la scritta look con Colori, basta cambiarla nel tasto»).
  **Dentro la finestra resta «Scegli il look»**: gliel'ho chiesto e ha detto
  che lì va bene.
- **In cima non ci sono più i quattro tasti (Colori, Novità app, Aiuto,
  Novità) né la riga «I tuoi prodotti (N) · Tocca per confrontare i prezzi»**
  (chiesto il 2026-09-22: «togli anche i quattro bottoni superiori, lascia le
  funzioni, poi troveremo un altro posto dove metterle»). Sono **nascosti con
  `hidden`, non tolti**: le finestre funzionano ancora e le prove le aprono.
  **Da fare con lui: trovare dove rimetterli.** ATTENZIONE: `hidden` da
  solo non basta su un elemento che nel CSS ha `display:flex` — fino al
  2026-09-22 sera sul telefono si vedevano ancora, mentre le prove (che
  guardano l'attributo) dicevano di no. Ci vuole la regola `[hidden]{display:none}`.
- **Il tasto «GRANDI MARCHE»** (tutto maiuscolo, chiesto il 2026-09-22) sta
  accanto a quello rosso, vuoto col bordo rosso. Apre il pannello della
  ricerca con **46 pillole di grandi marche italiane** (20, poi 40, poi 46 con quelle spente) (`GRANDI_MARCHE` in
  `pagina.py`); toccandone una la casella si riempie col nome e restano solo
  le offerte di quella marca. Regole:
  - si cerca **a parola intera** (`cercaMarca`): «AIA» come pezzo di parola
    trovava anche il «maiale»;
  - le marche sono scelte fra quelle che **compaiono davvero** nei volantini;
    Ferrero era nella lista ma quel giorno aveva zero offerte valide ed è
    stata sostituita da Saiwa. **Quando si rileggono i volantini, guardare
    che nessuna pillola resti vuota**;
  - come nella ricerca, **niente bollino verde** nei risultati.
  - **Le pillole hanno il MARCHIO VERO dove c'è** (chiesto il 2026-09-22):
    32 su 46, uno per file in `strumenti/marchi/` (nome della marca in
    minuscolo con i trattini, `.webp`), fonti in `marchi/FONTI.txt`. Come per
    i supermercati: fondo bianco fisso, nome nascosto dentro per chi non vede
    e per le prove, e se il file manca la pillola resta col nome scritto.
    **Ogni marchio è stato guardato prima di metterlo**: le ricerche automatiche
    ne avevano presi di sbagliati (un'«AIA» di compagnie aeree, una «Star» di
    un'altra azienda). Per aggiungerne uno basta mettere il file lì.
  - **Con le grandi marche aperte le categorie (la `.barra` coi prodotti)
    non si vedono** (chiesto il 2026-09-22: «non ha senso, non devono
    apparire»). Tornano appena si chiude il pannello. Con la ricerca normale
    (tasto rosso) restano come prima.
  - **Le marche senza offerte non si tolgono: si SPENGONO** (chiesto il
    2026-09-22: «metti anche Ferrero e quelle che non appaiono, facendo i
    pulsanti disattivati e di un colore molto più tenue»). Sono 46 pillole;
    quelle senza nessuna offerta valida sono tratteggiate e sbiadite e non si
    toccano. **Lo decide il telefono di chi guarda, con la sua data**, ogni
    volta che apre il pannello: un volantino che scade le spegne, uno nuovo
    le riaccende al primo aggiornamento. Non serve fare niente a mano. Fini e
    Moretti restano FUORI: non erano vuote, trovavano la cosa sbagliata
    («piselli fini», un tonno Moretti).
- **In cima, a destra del titolo, ci sono solo DUE PALLINI** da 32 px
  (chiesto il 2026-09-22 notte, dopo un primo giro con la ruota dei colori:
  «ci vanno due pallini, uno di configurazione e l'altro novità»):
  - l'**ingranaggio** (`#apri-config`) apre la finestra **«Configurazione»**
    (`#buio-config`, fuori dalla `.barra`, mai aperta insieme a un'altra):
    in cima **i supermercati**, uno per marchio, da toccare per toglierli o
    rimetterli; sotto i tasti **Colori della pagina** (`#apri-look`),
    **Aiuto** (`#apri-aiuto`) e **Cosa c'è di nuovo** (`#apri-novita-app`);
  - la **N** rossa (`.pallino.novita`) apre il diario delle novità.
  **I supermercati tolti** stanno in `localStorage` (`spesa.negozi.v1`), cioè
  sul telefono di chi guarda: Manlio e sua moglie possono tenerne di diversi.
  Si ricordano i TOLTI, non i tenuti, così un'insegna nuova compare da sola.
  Un'offerta di un negozio tolto è trattata come scaduta (`nascosta`), quindi
  sparisce da prezzi, «meno caro», ricerca e grandi marche; i suoi volantini
  spariscono dall'elenco in fondo. **Non si possono togliere tutti.** La prova
  è `prova-negozi.js`. **Il sottotitolo è «Offerte grande distribuzione».**
- **Toccando una grande marca la pagina scorre da sola ai risultati**
  (chiesto il 2026-09-22): le 46 pillole occupano uno schermo, e senza lo
  scorrimento le offerte restavano sotto, fuori vista.
- **C'è una VERSIONE DI PROVA con i due tasti (rosso e GRANDI MARCHE) SOTTO le
  categorie** invece che sopra (chiesta il 2026-09-22: «prova a farne anche
  una versione»). È `prova-tasti-sotto.html` sul sito, fatta da
  `strumenti/variante.py` a partire da `out/sito.html`: stessa pagina, una riga
  spostata. Sta sullo stesso sito, quindi legge la stessa lista del telefono.
  **Quando Manlio sceglie**: se vuole questa, si sposta la riga in `pagina.py`;
  in tutti e due i casi poi si cancellano `variante.py` e la prova sul sito.
- **Il meno caro è una pastiglia dentro l'elenco, e le offerte non ancora
  cominciate sono sbiadite** (chiesto il 2026-09-22: «che il prodotto meno
  caro venisse messo in una pillola, con un bordo e con un colore che la
  evidenzi, magari lo stesso colore del fondo ma un po' più forte» e «che le
  offerte che non sono ancora cominciate apparissero sbiadite»).
  - La pastiglia è `.prezzo-riga.vince`: fondo `--pannello` (lo sfondo della
    pagina un gradino più forte, come ha chiesto), bordo verde, angoli tondi.
    **Una sola per prodotto**, sulla riga che ha il bollino verde: è la meno
    cara **che si può comprare oggi**, che può non essere la prima riga.
  - Le sbiadite sono `.prezzo-riga.dopo`, `opacity:.82`, **col prezzo in
    grigio** (`--tenue` invece del rosso, chiesto il 2026-09-22: «si nota poco
    che non sono ancora attivi»). **Sbiadite, non nascoste**: un prezzo che
    parte lunedì serve saperlo, e sotto quel valore non si legge più.
  - **Un riquadro separato in cima non c'è e non va rimesso**: c'era per
    mezz'ora il 2026-09-22 e diceva le stesse identiche cose della pastiglia,
    due volte di fila. Con le righe future sbiadite, la pastiglia si trova da
    sola anche quando non è la prima.
  - Nei risultati di «Cerca fra i prezzi» e nelle offerte di un singolo
    volantino la pastiglia **non c'è**, come il bollino verde e per la stessa
    ragione. La prova è `prova-meno-caro.js`.
- **Ogni offerta ha il cerchietto dei giorni che mancano** (chiesto il
  2026-09-22, ispirato ai riquadri Material che ha mandato lui: «quella dove
  c'è scritto 6.80, usala piccola per indicare quanti giorni mancano»).
  Regole da non cambiare:
  - **il numero conta OGGI COMPRESO**: l'ultimo giorno dice «1 oggi», mai
    «0» — uno zero su un'offerta ancora valida si leggerebbe «è finita»;
  - **le offerte che devono ancora cominciare non ce l'hanno**: lì il numero
    direbbe una cosa e la riga un'altra. Al suo posto, nello stesso angolo,
    hanno il **tondino di quando partono** (`.parte`): il giorno grande
    dentro, il mese sotto, chiesto il 2026-09-22 al posto della pastiglia
    «vale dal 24 settembre»;
  - **blu finché c'è tempo, ambra negli ultimi tre giorni.** Non rosso: il
    rosso, in questa pagina, vuol dire «premi qui».
  La prova è `prova-giorni.js`.
- **Le novità della pagina si segnano per id PIÙ GRANDE, non per ultima
  dell'elenco.** Il confronto è alfabetico: due novità dello stesso giorno
  scritte in ordine di importanza (`-look` dopo `-giorni`) facevano tornare
  la finestra a ogni apertura. Sistemato il 2026-09-22.
- **«Apri la pagina … del volantino» è un'icona, non una scritta** (chiesta
  il 2026-09-22). È una pastiglietta col foglietto del volantino, il numero
  della pagina e la freccia, in fila con gli altri bollini: la frase intera
  resta nel `title` e nell'`aria-label`. Sta ancora nel `dove(o)` di
  `pagina.py` e tiene le classi `dove apri`, con cui la riconosce
  `prova-collegamenti.js`. Quando l'offerta non ha l'indirizzo della pagina
  resta la riga scritta in fondo: un'icona che non apre niente è una presa
  in giro.
- **I marchi dei supermercati stanno in `strumenti/loghi/`** (chiesti il
  2026-09-22: «al posto delle pillole col nome, mettici i veri loghi»). Un
  file per insegna, chiamato come l'insegna in minuscolo e senza accenti
  (`lidl.svg`, `md.svg`, `ekom.svg`...). **Per aggiungerne uno basta metterlo
  lì**, per toglierlo basta cancellarlo: `loghi.py` lo trova da solo e la
  pagina torna alla pillola col nome scritto. In `loghi/FONTI.txt` c'è scritto
  da dove viene ognuno. Regole:
  - **Va bene anche un `.png` o un `.webp`** quando di quel marchio non c'è un
    disegno libero: diventa un'immagine scritta dentro l'indirizzo, così la
    pagina resta un file solo. Se l'immagine è a **un colore pieno**,
    `python3 -m vettore <immagine> <insegna>` la trasforma in un disegno che
    non sgrana (è così che è nato `ekom.svg`).
  - **Gli id dentro ogni SVG vengono rinominati** (`l-<insegna>-<id>`): otto
    loghi nello stesso documento con lo stesso `id="A"` si rubano sfumature e
    maschere a vicenda.
  - **La pastiglia del marchio ha il fondo BIANCO fisso**, anche nei look
    scuri: i loghi hanno i loro colori e su fondo nero sparirebbero.
  - **Dentro c'è sempre il nome scritto**, nascosto alla vista (`.solo-voce`):
    un logo, per chi non lo vede, è un buco. È anche il modo con cui le prove
    riconoscono di che negozio è un'offerta.
  - **I marchi restano di chi li ha**: stanno lì per far riconoscere il
    negozio, e il piede della pagina lo dice.
  - **Ci sono tutte e dieci** dal 2026-09-22 (la nona è Pam, `pam.webp`, la decima Conad, `conad.svg`). Wikimedia continuava a dare 429,
    quindi gli ultimi tre sono arrivati da altrove: Carrefour dal suo sito
    (SVG vero), Ipercoop e Mercatò disegnati da un'immagine con `vettore`.
    **Il Mercatò ha due tinte** (scritta blu, fascia arancione): è per lui che
    `vettore` accetta il numero di tinte come terzo argomento.
- **Il tasto «Look» sta in cima, prima di «Aiuto»** (chiesto il 2026-09-22) e
  apre l'elenco dei cento look: tocchi una riga e la pagina si ricolora subito.
  I cento look **non si scrivono a mano**: li calcola `strumenti/look.py` dalle
  cento combinazioni del file Figma che ha mandato lui, salvate in
  `strumenti/palette.json` (quattro colori per combinazione, con nome e
  famiglia). Regole da non cambiare:
  - **Il verde «il meno caro» resta verde e l'ambra degli avvisi resta ambra**
    in tutti i look: cambia solo la tinta, non il significato. Il colore
    dell'accento (il rosso «prodotto acceso») è l'unico che segue la palette.
  - **Nessun look può risultare illeggibile.** `look.py` misura il contrasto
    (la regola WCAG) di sette accoppiate e `verifica()` si ferma con un errore
    se anche uno solo non arriva al minimo; gira a ogni generazione della
    pagina. I look scuri (12 su 100) sono quelli delle palette già scure: non
    c'entrano con `prefers-color-scheme`, che nel CSS **continua a non
    esistere** (vincolo 4).
  - **La pagina NON parte con un look addosso.** Chi non ha mai scelto vede
    l'originale; la scelta sta in `localStorage` (`spesa.look.v1`) e con
    «Originale» si torna indietro.
  - Il pannello è una finestra come le altre, **fuori dalla `.barra`**, e le
    tre finestre (novità, aiuto, look) **non stanno aperte insieme**.
  La prova è `prova-look.js`, che rifà i conti del contrasto in JavaScript su
  tutti e cento.
- **Il tasto «Aiuto» sta in cima, accanto a «Novità»** (chiesto il 2026-09-21)
  e apre una finestra che spiega come si usa la pagina. **Non si apre mai da
  sola e si riapre sempre**: è il contrario della finestra «Cosa c'è di
  nuovo». Il tasto è **vuoto, non rosso pieno**: il rosso pieno qui vuol dire
  «premi qui adesso», e l'aiuto non lo è. **Il testo l'ha letto e approvato
  Manlio prima che lo mettessi**: se va cambiato, si rifà così. La prova è
  `prova-aiuto.js`.
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

**Pam di corso Orbassano 212** (aggiunto il 2026-09-22, chiesto da lui: «a
Torino ce ne sono tantissimi»): è il Pam più vicino a corso Siracusa, a 400
metri, ed è un Pam «normale». Si legge il volantino dei **«PAM Supermercati»**,
non quello dei **Pam Panorama**, che ha id suoi e prezzi suoi. Non gliel'ho
chiesto: è il più vicino, e a Torino i Pam normali hanno tutti lo stesso
volantino. Se lui va in un Panorama, va cambiato.

**Conad di via Cesana 78** (aggiunto il 2026-09-22, «a Torino c'è anche
Conad»): è il Conad «normale» più vicino, a 2,7 km (codice negozio 009843). I
Conad City (via Bardonecchia 5/c, 3,3 km) e i Superstore hanno volantini loro.
Non gliel'ho chiesto: se va in un City, va cambiato.

## Da fare adesso (aggiornato il 2026-09-23)

- **Rifatto il 2026-09-23 il marchio EKOM** con l'immagine vera mandata da
  Manlio («il logo di Ekom in realtà è questo»): riquadro arancione, lettere
  in caselle bianche, «IL DISCOUNT VICINO A TE.». Quello di prima era una
  scritta rossa inclinata, sbagliata. `loghi/ekom.svg`, fatto con `vettore`.
- **Controllo del 23 settembre: niente di nuovo da leggere, solo pulizia.**
  Controllate tutte e dieci le insegne sulla fonte (anteprimavolantino per
  Lidl/Eurospin/MD/Bennet/Carrefour Iper, kimbino per Mercatò, l'API ufficiale
  per Ekom, volantinopiu per Ipercoop e Pam, il sito Conad): nessun volantino
  nuovo che non fosse già dentro `dati.py`. Bennet10, Lidl17 e Lidlfv17
  scadevano oggi ma sono già coperti senza buchi da bennet1709 e lidl24.
  - **Tolti `eurospin10` (10-20 settembre) e `md08` (8-20 settembre)**, scaduti
    da tre giorni e già coperti da `eurospin24` e `md22`: 215 righe di prezzo
    in meno da `PRODOTTI`, le loro voci tolte anche da `scartate.py`.
  - **Trovato e corretto un avviso sbagliato**: il cerchietto dei giorni,
    sull'ultimo giorno di un'offerta, diceva solo «Ultimo giorno: scade oggi»
    al tocco lungo, senza il numero — la prova `prova-giorni.js` lo controlla
    (vuole sempre una cifra) e con tre volantini che scadevano lo stesso
    giorno l'ha beccato per la prima volta. Ora dice anche la data.
  - **Trovato e corretto un bug in `variante.py`**: cercava e scriveva sempre
    dentro `strumenti/out/` invece che nella cartella dove giri i comandi,
    quindi non funzionava se non lanciato da un posto preciso. Sistemato per
    farlo comportare come `pagina.py` e gli altri.
  - **Guardati e lasciati fuori due volantini Ipercoop non alimentari**:
    «Tendenze d'Autunno» (abbigliamento ed elettronica, Expert) e «Grandi
    marche a tasso zero» (finanziamenti Expert): nessun prezzo di spesa vera.
  - Pubblicato: sito (verificato byte per byte) e artifact col catalogo
    pulito. `sw.js` a v68.

- **CHIUSA: il CONAD è dentro, la decima insegna** (chiesto da Manlio il
  2026-09-22 notte). Letto per intero **«Freschi di convenienza» dal 24
  settembre al 7 ottobre** (`conad24`, 24 pagine, 136 prezzi), edizione
  Piemonte del Conad di via Cesana 78. Sei pagine scartate in `scartate.py`.
  - **La fonte è quella UFFICIALE**: la scheda del negozio su conad.it
    (`conad.it/ricerca-negozi/conad-via-cesana-78-10139-torino--009843`)
    elenca i volantini, che sono **PDF sul sito Conad stesso**. `scarica.py`
    adesso sa leggerli: lo scarica una volta e ne fa le immagini delle pagine.
    Il collegamento di ogni riga è il PDF sul sito Conad con `#page=n`.
  - **«Solo titolari»** = solo con la Carta Insieme Conad: segnato riga per
    riga col prezzo senza tessera nella nota.
  - Il foglio «Perché conviene» ripete tre offerte di `conad24` agli stessi
    prezzi: guardato e lasciato fuori.
  - **Il volantino successivo** si trova sulla stessa scheda del negozio:
    i nomi dei PDF vanno avanti di uno (`20262619PCONADPIEMONTE` era il 10-23
    settembre, `20262620...` il 24 settembre-7 ottobre).
- **La Routine notturna è stata aggiornata il 2026-09-22** con le dieci
  insegne e la fonte di ognuna (Ekom dal sito ufficiale, Ipercoop e Pam da
  volantinopiu cercando gli id, Conad dal sito Conad). Prima conosceva solo
  sette insegne e le fonti vecchie.
- **CHIUSA: il PAM è dentro, la nona insegna** (chiesto da Manlio il
  2026-09-22 sera, «fai tutte le cose necessarie per metterlo»). Letti per
  intero i due volantini **dal 24 settembre al 7 ottobre**: `pam24` «Tante
  offerte a 1, 2, 3 euro» (20 pagine, 124 prezzi) e `pamextra24` «Occasioni
  Extra» (27 pagine, 123 prezzi). Copertura 47/47, 6 pagine scartate in
  `scartate.py`. Marchio vero in `strumenti/loghi/pam.webp`.
  - **Come si trovano**: Pam mette i volantini su volantinopiu come Nova Coop.
    L'elenco per negozio lo dà l'API del suo sito, `coeus.ppapi.it` (POST
    `post/query?typeUuid=flyer` con `relationshipQueries[flyer_store][$in][0]=71`,
    71 = corso Orbassano, codice pv 2311). Quelli nuovi, prima che l'elenco li
    mostri, si trovano chiedendo gli id uno per uno su
    `pam.volantinopiu.com/volantino<id>00pv2311.html` e leggendo `<title>`
    e date: i nostri sono i **«PAM Supermercati»**, non i «PAM Panorama».
  - **«con APP»** vuol dire che il prezzo vale solo con l'app Pam Perte Plus:
    segnato riga per riga nella nota, come la MD Buona Spesa Card. Il
    volantino **non stampa** il prezzo senza app.
  - La pescheria di `pam24` (pagina 11) ha metà offerte **solo dal 24 al 30
    settembre** e metà **solo dall'1 al 7 ottobre**: date scritte riga per riga.
  - `pam24` e `pamextra24` scadono il **7 ottobre**.
- **CHIUSA: l'IPERCOOP è dentro.** Il 2026-09-22 è stato letto per intero il
  volantino **«Extra offerte» dal 24 settembre al 7 ottobre** (`ipercoop24`,
  47 pagine, 152 prezzi nuovi): è il primo Ipercoop con prezzi veri da quando
  esiste il progetto. Sul canale pubblico del negozio **non c'era ancora**:
  volantinopiu lo aveva già caricato ma non lo mostrava, e si è trovato
  interrogando gli id uno per uno su
  `ipercoop.volantinopiu.com/volantino<id>00pv24.html`. **Da rifare così ogni
  volta che serve un volantino Nova Coop prima che esca nell'elenco.**
  - **Nova Coop stampa QUATTORDICI edizioni dello stesso volantino**, una per
    zona, e qualche prezzo cambia fra l'una e l'altra (il latte Arborea va da
    1,39 a 1,45). **La zona è scritta sul frontespizio**, in mezzo alla pagina.
    La nostra è la PRIMA del gruppo, **id 28831, «TORINO - COLLEGNO»**.
    L'elenco completo sta nel commento di `VOLANTINI` in `dati.py`.
  - **Da chiedere a Manlio**: l'Ipercoop di **Beinasco** (Strada Torino 34/36,
    Le Fornaci) è più vicino a corso Siracusa di quello di Torino via Livorno,
    e ha la sua edizione (id 28844) con qualche prezzo diverso. Finché non lo
    dice lui si usa Torino.
  - 21 pagine scartate (fiori, giardinaggio, fai da te, auto, casalinghi,
    libri, elettrodomestici, tre pagine di raccolta bollini senza prezzi, e le
    due «Grandi Marche Selection» che hanno solo sconti percentuali): in
    `scartate.py`. Copertura 47/47.
  - Gli sconti e i prezzi **«solo per i soci»** sono segnati riga per riga col
    prezzo senza tessera nella nota, come si fa con la MD Buona Spesa Card e
    con la carta EKOM UP. Le pagine **«1+1»** e **«1,2,3 più compri meno
    paghi»** seguono le regole già scritte: nel formato c'è quanta roba si
    porta via, e il prezzo è quello che NON fa sembrare l'offerta più
    conveniente di quello che è (una confezione sola).
  - Il latte microfiltrato Coop a 1,19 **vale solo dal 28 settembre al 4
    ottobre**: le date sono scritte sulla riga.
- **Messi il 2026-09-22 i marchi veri di TUTTE E OTTO le insegne.** Le
  pillole col nome scritto non si vedono più da nessuna parte.
- **Rifatta l'impaginazione il 2026-09-22 (`sw.js` v52)**: schede al posto
  delle righe, marchi dei negozi, titolo «Spesa», data di riferimento, tasto
  rosso della ricerca in cima. Sopra c'è la regola per esteso.
- **Fatto il 2026-09-22 (`sw.js` v50)**: la pastiglia del «meno caro»
  nell'elenco, le offerte non ancora cominciate sbiadite col prezzo grigio e
  col tondino del giorno in cui partono, il cerchietto dei giorni che mancano
  su ogni offerta, «apri la pagina del volantino» ridotto a un'icona, gli
  angoli più morbidi in tutta la pagina (pannelli, bollini e tasti tondi come
  i riquadri Material che ha mandato lui) e la riga «Torino · corso Siracusa»
  tolta dalla cima col suo bollino.

- **Fatto il 2026-09-22 il tasto «Look»**: cento look ricavati dalle cento
  combinazioni di colori che ha mandato Manlio (il PDF di Figma). Pubblicato
  su sito e artifact, `sw.js` a v48. Se un giorno arrivassero altre palette,
  si aggiungono a `strumenti/palette.json` e basta: il resto si rifà da solo.
- **Letto per intero il 2026-09-22: Lidl dal 24 al 30 settembre** (`lidl24`,
  52 pagine, trovato già con le pagine pubblicate — annunciato il 21/9 ma
  ancora senza pagine vere, oggi c'erano). 93 prezzi nuovi in `dati.py`, in
  quasi tutti i reparti (macelleria, salumi, formaggi, pesce, surgelati,
  dispensa, bevande, casa, colazione, ortofrutta). 27 pagine scartate
  (abbigliamento e stivali bambini, attrezzi auto e fai-da-te Parkside,
  elettrodomestici SilverCrest, fiori e piante, viaggi Lidl, pubblicità varie):
  in `scartate.py`. Diverse offerte valgono solo **dal 24 al 27** o solo
  **dal 28 al 30**, non tutto il periodo: le date sono scritte riga per riga.
  `lidl17` e `lidlfv17` (17-23 settembre) restano validi altri due giorni,
  **nessun buco**. Copertura: 52/52 pagine lette.
- **CHIUSA: letto per intero il 2026-09-22 l'Ekom «I più ekonomici» (22
  settembre-5 ottobre)** (`ekom22`, 16 pagine). Non l'avevo trovato da solo —
  kimbino.it/ekom/ non lo sapeva ancora — **è stato Manlio a segnalare il
  link giusto**, `ekomdiscount.it/volantini`, il sito ufficiale. Da lì in poi
  la fonte per l'Ekom è quella, non più kimbino: in NOTE.md c'è scritto come
  leggerla (serve un browser vero, non un fetch semplice, ma le pagine si
  prendono con un `curl` normale una volta trovato l'indirizzo dell'API).
  102 prezzi nuovi in `dati.py`. 3 pagine scartate (copertina, concorso a
  premi, pubblicità app): in `scartate.py`. Alcune offerte valgono solo con
  la carta EKOM UP, segnato riga per riga come per la MD Buona Spesa Card.
  Copertura: 16/16 pagine lette.
- **Ipercoop: sistemato, vedi in cima.** `promoipercoop.it` non c'entrava
  niente: era il sito sbagliato.
- **Mercatò, Bennet, Eurospin, MD, Carrefour Iper: nessuna novità** il
  2026-09-22, controllati tutti sulla fonte (anteprimavolantino, kimbino).

- **Fatto il 2026-09-21 il tasto «Aiuto»** in cima accanto a «Novità», col
  testo approvato da Manlio prima di metterlo. Pubblicato su sito e artifact.

- **L'ora del controllo automatico è stata spostata alle 7 del mattino**
  (chiesto da Manlio il 2026-09-21). La Routine si chiama «Spesa — controllo
  giornaliero dei volantini» e adesso ha `0 5 * * *`: **il cron è in UTC**, e
  con l'ora legale (UTC+2) parte alle 7 italiane — nei fatti fra le 7:05 e le
  7:15, perché il servizio ha qualche minuto di ritardo. **Attenzione al
  25 ottobre 2026**: quel giorno torna l'ora solare (UTC+1) e `0 5 * * *`
  diventerebbe **le 6 del mattino**. Quel giorno, o subito dopo, va rimesso a
  `0 6 * * *` con `update_trigger`, se no il giro parte un'ora prima di quanto
  vuole lui. Stessa cosa al contrario l'ultima domenica di marzo.

- **Ekom «I più ekonomici» (22 settembre-5 ottobre): ancora non online, 3° giorno
  di fila che si controlla senza trovarlo** (19, 20, 21 settembre — kimbino
  invariato all'8-21, ekom.it ancora 503). `ekom08` scade oggi 21 settembre:
  da domani, finché non esce il successore, **non ci saranno offerte Ekom** in
  lista. Detto a Manlio. **Da fare: appena esce online si legge per intero;
  se lui manda le foto delle pagine di carta, si legge da quelle.**
- **Eurospin e MD: niente da fare.** `eurospin10` e `md08` sono scaduti il 20
  settembre ma i loro successori (`eurospin24`, `md22`) erano già dentro
  `dati.py` da prima: nessun buco, nessuna offerta persa. Restano in `dati.py`
  finché non si fa un giro di pulizia (le offerte scadute spariscono da sole
  dalla pagina, per data del browser di chi guarda: non è urgente toglierle).
- **Ipercoop: sistemato il 2026-09-22, vedi in cima** (era il sito sbagliato).
- **Mercatò, Bennet, Carrefour Iper: nessuna novità** il 2026-09-21, controllati
  tutti sulla fonte.

- **CHIUSA: il volantino Ekom di carta era il successivo.** Il 2026-09-19
  Manlio ha fotografato una pagina «Surgelati» (filetti di merluzzo Alaska
  400 g a 1,99, tentacoli di totano gigante, minestrone 450 g a 0,79, patate
  stick, pizza formato pala, churros) che **non era nel volantino 8-21
  settembre** che avevo letto. Verificato che non fosse una differenza di
  regione (la pagina Surgelati dell'edizione Toscana è identica a quella
  generale) e che online non ci fosse altro: kimbino, volantinofacile,
  offertolino, promoqui, doveconviene e il sito Ekom avevano solo l'8-21.
  Poi lui ha fotografato la copertina: **«I PIÙ EKONOMICI», dal 22 settembre
  al 5 ottobre**. Quindi **l'Ekom stampa il volantino prima di pubblicarlo
  online**, e questo è il primo caso visto nel progetto: la fonte era giusta,
  era solo in ritardo. Messo in `VOLANTINI_ATTESI` con le sue date vere, così
  in tabella si vede «in arrivo, prezzi non ancora letti».
  **Da fare: appena esce online (kimbino, come per l'8-21) si legge per
  intero e si toglie da `VOLANTINI_ATTESI`.** Se il 22 non è ancora online,
  Manlio manda le foto delle pagine e si legge da quelle: i prezzi si leggono
  a occhio comunque, cambia solo che quelle righe non avranno il collegamento
  alla pagina del volantino. **Ricontrollato il 2026-09-20: ancora non
  online** (kimbino invariato all'8-21, sito ekom.it 503).

- **Rifatta il 2026-09-19 la pagina Novità**, come ha chiesto Manlio: prima i
  volantini aggiornati (con il tasto «3 giorni» nuovo), poi la tabella di
  tutti i volantini con le date di validità, poi le novità dei prezzi. Solo
  `novita.html` è cambiata: la pagina dei prezzi è rimasta identica, e
  l'artifact non è stato ripubblicato perché il suo tasto «Novità» punta già
  al sito.

- **Letto per intero il 2026-09-19: Bennet «Un mondo di bellezza», dal 17 al
  30 settembre** (`bennet1709`, 27 pagine). Non è solo bellezza: da pagina 18
  in poi c'era un bel po' di spesa vera — pasta, riso, formaggi, salumi,
  surgelati, vino, acqua, oltre a shampoo, saponi e dentifrici. Circa 87
  prezzi nuovi in `dati.py`. 14 pagine scartate (styling capelli, creme viso,
  depilazione, deodoranti, rasoi uomo, assorbenti, integratori, pubblicità):
  in `scartate.py`. Diverse offerte «shampoo O balsamo» hanno lo stesso
  prezzo per due formati diversi: il conto è sempre sul formato più piccolo,
  per non sembrare più conveniente di quanto sia — stessa regola delle pagine
  1+1 dell'Ekom.
- **Tolti il 2026-09-19 i tre volantini scaduti da tre giorni**: `mercato`,
  `bennet0903` e `lidl10` (già coperti senza buchi dai loro successori). 596
  righe di prezzo in meno da `dati.py`, le loro voci tolte anche da
  `scartate.py`.

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
- **CHIUSA: trovato e letto per intero l'Eurospin dal 24 settembre al 4
  ottobre** (`eurospin24`, 22 pagine), il giorno stesso in cui scadeva
  `eurospin10`: colma da solo il buco di 4 giorni che era segnato qui.
  ~140 prezzi nuovi in `dati.py`. Gran parte delle pagine erano un concorso a
  tema Bluey (giocattoli, abbigliamento, viaggi): scartate le pagine non
  alimentari (16-21), tenuti i pochi alimentari Bluey (latte, succo, pasta,
  asciugatutto) che restavano offerte vere. Pagina 12 (Frutta e verdura più
  Pescheria) ha un elenco di punti vendita aderenti: Torino ne ha diversi,
  alcuni senza reparto pescheria — segnato nella nota delle righe di
  pescheria. Pagina 22, «Doppio weekend di follia», ha offerte ristrette a
  due fine settimana (25-27 settembre e 2-4 ottobre): date scritte riga per
  riga, come per il «Weekend più uno» dell'MD.
- **Carrefour Iper: nessuna novità.** Fermo a `carriper15` (fino al 28).
  **Ipercoop: il sito `promoipercoop.it` risponde ancora 503** (visto il
  2026-09-19 e di nuovo il 2026-09-20, due giorni di fila) — da riprovare.
  L'ultima cosa vista era ancora solo «Scegli tu Grandi Marche», sconti
  percentuali senza un prezzo di base, non utilizzabile.
- **`md08` è scaduto il 20 settembre e non ha ancora un successore in
  `dati.py` diverso da quello già dentro.** Il successore (`md22`, dal 22) è
  già dentro: **c'è solo un giorno di buco** (il 21), niente da fare finché
  non si avvicina.
- **Il Carrefour Iper (`carriper15`, 15-28 settembre) è a posto, non
  riaprire la questione.** L'ultima pagina del suo volantino elenca gli
  ipermercati in cui vale e Torino non c'è: il 2026-09-07 Manlio ha detto che
  è sbagliato fermarsi lì — «le offerte ci sono a Torino e valgono davvero».
  In NOTE.md c'è per esteso.
- **Copertura letta: tutti i volantini con prezzi in `dati.py` sono al 100%**
  (bennet10, lidl17, lidlfv17, eurospin10, eurospin24, md08, carriper15,
  mercato17, md22, ekom08, bennet1709, lidl24, ekom22, ipercoop24).
- **Scadenze da tenere d'occhio nei prossimi giorni**: `md08`, `eurospin10` ed
  `ekom08` sono scaduti (20 e 21 settembre) ma i loro successori sono già
  dentro `dati.py`: da togliere con `pulisci --fai` appena il programma lo
  permette, non è urgente. `bennet10`, `lidl17` e `lidlfv17` scadono il 23
  (occhio: nel Lidl 17-23 la «Panetteria» vale solo dal 17 al 20, e alcune
  offerte «Il meglio del lunedì» valgono solo dal 21 al 23 — già segnato
  nelle note delle singole righe). `mercato17` e `bennet1709` scadono il 30,
  `lidl24` anche (occhio: alcune sue offerte valgono solo dal 24 al 27 o solo
  dal 28 al 30, non tutto il periodo — già segnato riga per riga). `md22`
  scade il 4 ottobre, `eurospin24` anche. `ekom22` scade il 5 ottobre, `ipercoop24` il 7 (dentro c'è il latte
  microfiltrato Coop che vale solo dal 28 settembre al 4 ottobre). La
  pagina Oktoberfest del Bennet (pagine 20-21 di `bennet10`) scade il 4
  ottobre, non il 23 come il resto — occhio quando si ributta il volantino.
  Il weekend Eurospin 25-27 settembre e quello del 2-4 ottobre (vedi sopra)
  valgono solo quei giorni, non tutto il periodo di `eurospin24`.
- **Il giro automatico non funziona, e non è un mistero da risolvere leggendo
  il codice**: parte, lavora pochi minuti e non lascia traccia. In NOTE.md c'è
  quello che si sa e quello che non si sa, e perché a mano riesce. Finché non lo
  si vede arrivare in fondo più volte di fila, **i volantini si mettono a
  mano**. **Il 2026-09-10, il 2026-09-15, il 2026-09-16, il 2026-09-17, il
  2026-09-18, il 2026-09-19, il 2026-09-20, il 2026-09-21 e il 2026-09-22 la
  sessione da Routine è arrivata in fondo**: ha letto un volantino per intero
  (o più) e pubblicato — ma il 17 settembre si
  è scoperto che le pubblicazioni del 15 e del 16 non erano davvero arrivate
  al sito (vedi sopra): un «pubblicato» nel registro non basta, va controllato
  che sia finito su `main`. Dal 2026-09-18 in poi, dopo ogni push, verificato
  che `index.html` scaricato dal sito online combaci byte per byte col file
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
- `strumenti/` — catalogo, dati, pagina, storia, lette, scartate, stampa, prove,
  look (i cento look) e `palette.json` (le cento combinazioni di partenza)
- `NOTE.md` — la storia lunga e il perché di ogni scelta
