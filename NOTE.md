# Spesa — offerte dei supermercati

> **Le regole da sapere prima di toccare qualcosa stanno in `CLAUDE.md`**, che è
> corto e si legge da solo all'avvio di una sessione. Questo file è la storia
> lunga: il perché di ogni scelta, cosa è stato provato e com'è andato. Vacci
> quando CLAUDE.md non basta, e **prima di rifare qualcosa che sembra mancare**.

Progetto separato dalla Palestra, chiesto da Manlio il 2026-09-02.
Vive in questa cartella per non toccare `index.html`, che è l'app della palestra.

## Cosa vuole

**Non vuole che sia Claude a cercare i prodotti.** L'ha detto chiaramente a metà
lavoro: gli bastano **i volantini scaricati** da guardare da solo e uno strumento
per cercare a modo suo. La ricerca la fa lui.

**L'Excel non serve più**: il 2026-09-02 ha detto «il file Excel puoi anche non
farlo». `strumenti/build_xlsx.py` e `cache_vals.py` restano lì e funzionano, ma
non fanno più parte della consegna. Non rifarlo se non lo richiede.

**Vuole una pagina con dodici prodotti a scelta**, da cambiare e da allungare
con un «+». È la forma finale del lavoro.

**Zona:** Torino, quartiere Santa Rita (corso Siracusa). Il civico non serve.
Di Mercatò ci sono punti vendita vicini: via Filadelfia, via Gaidano, corso
Brunelleschi.

**Insegne:** MD · Eurospin · Carrefour Iper · Bennet · Ipercoop · Lidl
Il 2026-09-02 ha detto di **togliere Carrefour Market e mettere Ipercoop**.
**Mercatò c'è dal 2026-09-05** ed è l'insegna dove Manlio va quasi tutti i
giorni: è quella che conta di più. Il punto vendita di riferimento è via
Filadelfia 232, il più vicino a corso Siracusa.

**Prodotti che gli interessano sempre:** carne di bue in confezioni grandi,
tonno, salmone. Resta da chiarire quale salmone (affumicato, fresco o surgelato):
gliel'ho chiesto e non ha ancora risposto.

## Com'è andata il 2026-09-02

Consegnati: 8 PDF (277 pagine), `offerte-supermercati-torino.xlsx` con tre
fogli — guida, 24 prodotti suoi col prezzo al chilo, indice cercabile di tutte
le pagine — e **una pagina web pubblicata**, che è quello che ha chiesto per
ultimo: voleva un indirizzo da mandare **anche a sua moglie, da un altro posto**.

## Casa propria: dal 2026-09-04 la Spesa ha il suo sito

Stava dentro il progetto della Palestra, quindi sotto `/palestra/spesa/`, e le
due app si pestavano i piedi: il manifest della Palestra dichiara
`"scope": "./"` e si prendeva tutto quello che stava sotto, Spesa compresa.
Toccando l'icona della Palestra partiva la Spesa. Ho messo un `id` esplicito a
tutte e due — rimedio giusto — ma Manlio ha chiesto la separazione vera, e ha
ragione: **finché stanno nello stesso progetto GitHub, stanno per forza sotto
lo stesso indirizzo**, perché GitHub Pages pubblica un progetto sotto il nome
del progetto.

Adesso la Spesa è un progetto suo:

    manliograndi-del/spesa  →  https://manliograndi-del.github.io/spesa/

Niente più sovrapposizione: scope diversi, service worker diversi, identità
diverse. **Il vecchio indirizzo sotto `/palestra/spesa/` non esiste più**: il 2026-09-04
Manlio ha scelto di cancellare la cartella invece di lasciarci un rimando, e
adesso quell'indirizzo risponde «pagina non trovata». Il progetto della palestra
è tornato a essere solo l'app della palestra.

Il controllo giornaliero è stato spostato qui lo stesso giorno
(`trig_01UMkRYxHXJfPBSEZLo7Snzb`): se qualcuno lo modifica, deve puntare a
**questo** progetto, non più a `palestra/spesa/`.

Il sito lo pubblica il ramo `main` di QUESTO progetto, dalla radice.

## L'indirizzo che conta è il sito, non l'artifact

Il 2026-09-03 Manlio ha detto: «questa pagina non deve essere un artefatto tuo,
voglio l'indirizzo internet della pagina». Ha ragione. Il giorno dopo il
progetto è diventato suo e l'indirizzo si è accorciato.

    https://manliograndi-del.github.io/spesa/     ← QUESTO
    https://claude.ai/code/artifact/a6782ea0-6822-4026-87e7-705012966595  (secondario)

Il sito lo pubblica il ramo **`main`** di questo progetto, dalla radice: per
mandare in linea una modifica bisogna portarla lì, non basta il ramo di lavoro.
**Vanno aggiornate tutte e due le copie**: il sito con un commit su `main`,
l'artifact ripubblicandolo. Aggiornarne una sola lascia l'altra a raccontare
i prezzi della settimana scorsa — successo il 2026-09-04.

**La rinuncia, scelta da lui sapendola:** sul sito non c'è nessun server, quindi
la lista torna a essere una per telefono. La lista condivisa vive solo
sull'artifact. Se dicono che le liste non combaciano, è questo, non un baco.

### `CONDIVISA`: chi comanda, la pagina o il browser

Ogni copia porta una costante `CONDIVISA`. Dove è **vera** (solo l'artifact)
comanda la lista incorporata nella pagina: è quella che vedono tutti e viene
aggiornata ripubblicando. Dove è **falsa** (sito e file) comanda quella salvata
nel browser di chi apre, e la incorporata vale solo come punto di partenza.

Senza questa distinzione **sul sito le modifiche sparivano a ogni
ricaricamento**: la lista incorporata non è vuota, quindi vinceva sempre lei,
e lì non c'è niente che possa aggiornarla. Trovato rileggendo, prima che se ne
accorgesse Manlio.

**L'ordine delle sostituzioni è delicato.** Sia `riempi()` in Python sia
`documento()` in JavaScript devono riempire `__TEMPLATE__` **per ultimo**:
appena infilato, il modello porta dentro una copia di tutti gli altri
segnaposto, e da quel momento la sostituzione dopo trova quelli invece dei
veri. Successo davvero con `__CONDIVISA__`: veniva riempito dentro la copia e
la pagina rigenerata restava con un `__CONDIVISA__` scoperto, cioè rotta. Il
controllo in Node che rigenera tre volte e guarda cosa esce è l'unico modo per
accorgersene senza mandarla in mano a loro.

`pagina.py` sforna tre versioni dalla stessa fonte:

| file | dove va | differenza |
|---|---|---|
| `out/sito.html` | `spesa/index.html`, il sito | 219 KB, niente copia di sé (lì non potrà mai ripubblicarsi), ha manifest e service worker |
| `out/pagina.html` | l'artifact | 445 KB, con la copia di sé per la lista condivisa |
| `out/spesa-da-sola.html` | da mandare per posta | come il sito ma tutto in un file |

### MAI scrivere il tag di chiusura dello script per esteso

Il guaio peggiore di tutta la sessione, il 2026-09-03. In un **commento** dentro
lo script c'era il tag di chiusura scritto per esteso. Il browser lo cerca nel
testo e non gli importa che sia dentro un commento: ha chiuso lo script a metà.
**Tutte e tre le pagine sono uscite morte** — quella sul sito, quella di Claude
e il file — e quella di Claude era già in mano a Manlio.

Da fuori sembravano perfette: intestazione, riquadri, testi, tutto al posto
giusto. Mancavano solo i bottoni dei prodotti e i prezzi, perché il pezzo di
programma che li disegna stava dopo il taglio. È esattamente il tipo di guasto
che non si vede rileggendo il codice: l'ha visto Manlio aprendo il sito.

`pagina.py` adesso **non consegna un file senza averlo controllato**: spezza
ogni pagina dove la spezzerebbe il browser, passa ogni pezzo a `node --check` e
verifica che quello grosso contenga `function disegna`. Se non torna, si ferma
con un errore invece di scrivere il file. Provato rimettendo il guasto apposta:
lo prende.

Se devi nominare quel tag in un commento, scrivilo spezzato o giragli intorno a
parole. Vale anche per le stringhe: `racchiudi()` in Python e `documento()` in
JavaScript spezzano ogni `</` in `<\/` proprio per questo.

### L'iniziale maiuscola, e perché non bastava cambiare i dati

Manlio ha aggiunto quattro prodotti scrivendoli minuscoli e poi ha chiesto la
maiuscola. Io li ho messi maiuscoli in `lista.py` — e lui **continuava a
vederli minuscoli**, giustamente: sul sito comanda la lista salvata nel suo
browser, non quella incorporata nella pagina. Qualunque cosa pubblichi, i suoi
nomi restano i suoi.

Quindi la maiuscola la mette **la pagina**, non i dati: `maiuscola()` in
`pagina.py` agisce quando si aggiunge o si rinomina un prodotto **e** su ogni
lista letta dalla memoria, così le liste già salvate si sistemano da sole senza
che nessuno tocchi niente.

**Solo la prima lettera, e in JavaScript.** `text-transform: capitalize` del CSS
maiuscolizza ogni parola e storpierebbe «Olio d'oliva» in «Olio D'oliva».

La regola generale, che vale per ogni cosa del genere: **se il cambiamento deve
vedersi anche su una lista già salvata, va fatto nel codice della pagina, non
nei dati di partenza.** Altrimenti lo vedono solo i telefoni nuovi.
`strumenti/prova-maiuscole.js` prova esattamente questo: finge una lista salvata
coi nomi minuscoli e controlla come esce.

### Le righe aprono il volantino alla pagina giusta

Chiesto da Manlio il 2026-09-04: leggere «pagina 16» e doversi arrangiare non
serviva a niente. Adesso sia le righe dei prezzi sia quelle dell'elenco pagine
sono **collegamenti** che aprono l'immagine di quella pagina, in una scheda
nuova.

Non si ospita niente: si punta all'immagine originale, dove il volantino sta
già. Il sesto campo di `VOLANTINI` in `dati.py` è il modello dell'indirizzo, con
`{n}` al posto del numero. **Le due fonti numerano diversamente** — anteprima­
volantino riempie di zeri (due cifre per certi volantini, cinque per altri, senza
una logica), volantinopiu no — quindi a ogni volantino nuovo il modello va
ricontrollato insieme alle date, e provato.

`strumenti/prova-collegamenti.js` clicca ogni prodotto, raccoglie tutti gli
indirizzi e controlla che siano ben formati e che si aprano in una scheda nuova;
poi vale la pena provarne una dozzina con `curl` e pretendere 200. Un modello
sbagliato non dà errore: dà righe che portano a una pagina bianca.

Le righe senza numero di pagina (quelle prese dai riassunti online) restano
scritte e non cliccabili, ed è giusto: non so a quale pagina puntare.

### Il tasto delle lingue: fatto e tolto

Il 2026-09-04 Manlio ha chiesto un tasto per cambiare lingua alle scritte,
lasciando in italiano i dati che vengono dai volantini. È stato fatto — quattro
lingue, tasto in alto a destra — e **poche ore dopo ha chiesto di toglierlo**.
Tolto.

Resta scritto qui perché non venga rimesso per iniziativa di qualcun altro: non
è stato tolto perché funzionava male, ma perché non lo voleva. Se un domani lo
richiede, sta nella storia del progetto al commit «Un tasto per le lingue» e si
riprende da lì invece di rifarlo.

Quello che vale la pena ricordare comunque, se si ritocca l'interfaccia: **le
scritte si possono cambiare, i dati no**. Nomi dei prodotti, insegne,
descrizione delle offerte e loro condizioni vengono dai volantini italiani e
servono a cercarci dentro; su un prezzo un'imprecisione la si paga alla cassa.

### `prova.js`: aprire la pagina per davvero, sempre

Il 2026-09-03 la pagina è uscita rotta **tre volte di fila**, e ogni volta
sembrava a posto da fuori:

1. un commento conteneva il tag di chiusura dello script scritto per esteso →
   script tagliato a metà, niente bottoni;
2. il blocco che accende la lista condivisa stava **prima** di
   `let lista = leggiLista()` → chiamava `disegna()` quando `lista` non esisteva
   ancora e moriva lì;
3. una mia sostituzione di testo aveva **cancellato `pagineDi`**: avevo
   rimpiazzato un pezzo di sorgente delimitandolo da due commenti, e quella
   funzione stava in mezzo. I bottoni comparivano, cliccandoli non usciva
   niente.

Nessuno dei tre si vedeva rileggendo il codice, e il controllo di sintassi ne
prendeva solo il primo. Li ha visti Manlio, aprendo il sito. Tre volte.

`strumenti/prova.js` apre la pagina in un browser finto (jsdom), **clicca ogni
bottone** e pretende che escano prezzi o pagine. Va lanciato su tutte e tre le
copie **prima di pubblicare**, sempre:

    cd /tmp/dom && npm install jsdom
    node prova.js .../out/sito.html
    node prova.js .../out/pagina.html
    node prova.js .../out/spesa-da-sola.html

Esce con errore se qualcosa non va. Il controllo dentro `pagina.py` (node
--check) resta, ma da solo non basta: una pagina può essere sintatticamente
perfetta e muta.

**Attenzione alle sostituzioni di testo su `pagina.py`**: delimitare un pezzo
da rimpiazzare con due commenti lontani cancella tutto quello che ci sta in
mezzo. È successo. Meglio sostituzioni corte e mirate, e comunque `prova.js`
dopo.

### Le due app si pestavano i piedi: `id` nel manifest

Il 2026-09-04 Manlio ha detto che toccando l'icona della **Palestra** gli partiva
la **Spesa**, che Chrome gli diceva «Palestra è già installata» quando provava a
installare la Spesa, e che la Palestra non la trovava più fra le applicazioni.

Causa: il manifest della Palestra dichiara `"scope": "./"`, cioè **tutto quello
che sta sotto `/palestra/`** — e la Spesa ci sta dentro. Nessuno dei due manifest
dichiarava un `id`, quindi il browser se lo ricavava da solo e trattava le due
pagine come la stessa applicazione.

Rimedio: `"id"` esplicito in tutti e due, **uguale a quello che il browser già
calcolava** (`/palestra/index.html` e `/palestra/spesa/`), così non nasce
un'applicazione nuova e non si perde quella installata; si mette solo per
iscritto un'identità che prima era implicita e ambigua.

**Lo scope resta sovrapposto e non si può evitare**: GitHub Pages pubblica tutto
sotto `/palestra/`, e la Spesa deve stare lì dentro. Fra due scope che
combaciano vince il più specifico, quindi `/palestra/spesa/` è della Spesa. È
l'`id` a tenerle separate come applicazioni.

**Se un domani si aggiunge una terza app in una cartella di qui, dalle subito il
suo `id`**, o si ricasca in questo.

Attenzione: il manifest sta nella lista dei file messi in cache da tutti e due i
service worker. Cambiandolo **va alzato il numero di cache di entrambi**, o i
telefoni continuano a servirsi la versione vecchia.

Quello che questa correzione **non** può fare è sistemare un telefono dove
l'installazione sbagliata c'è già: lì bisogna disinstallare e reinstallare.

### Il service worker della Spesa è obbligatorio

`spesa/sw.js` non è un lusso. Quello della Palestra sta alla radice, il suo
scope copre anche `/palestra/spesa/`, e **senza rete servirebbe l'index.html
della Palestra al posto della Spesa** (guarda il suo `catch`: ricade su
`./index.html`). Uno registrato più in basso vince sul suo scope, quindi questo
toglie di mezzo il problema — e in più tiene la Spesa disponibile in negozio,
dove il segnale è pessimo. Se lo modifichi, **alza il numero di cache**
(`spesa-v1`), come per la Palestra.

Le icone sono un carrello rosso su fondo bianco, di proposito diverse da quelle
della Palestra che sono rosse piene: sulla schermata Home non si confondono.

**La pagina si chiama «Spesa»**, chiesto il 2026-09-03: è il `<title>`, cioè il
nome che si legge sotto l'icona quando la si installa sulla schermata Home del
telefono. Non cambiarlo per farlo più descrittivo — è il nome dell'app per
loro. L'icona è il carrello 🛒 e resta quella: si ritrova per l'icona.

**Le pagine pubblicate nascono private**: perché la moglie la apra, lui deve
condividerla dal menu della pagina stessa. Gliel'ho detto; se dice che lei non
la vede, è quasi sicuramente quello.

**La moglie non vive con lui** (detto il 2026-09-02): apre da un'altra casa, da
un altro telefono, e non ha niente di installato. Per questo esiste anche
`out/spesa-da-sola.html`, che `strumenti/pagina.py` scrive accanto alla pagina
pubblicata: è lo stesso identico contenuto ma con `<!doctype>`, `<head>` e
`<body>` attorno, perché quelli **il servizio li mette da sé alla pagina
pubblicata e il file grezzo non ce li ha**. Quel file si apre a doppio clic,
senza account e senza rete — i caratteri di Google non si caricano e scende ai
caratteri di sistema, tutto il resto funziona perché dati e codice sono dentro.
Si manda per posta o WhatsApp. **Non si perde niente rispetto al link**: la
lista sta comunque nel browser di chi apre, quindi era già una copia a testa.

La pagina la genera `strumenti/pagina.py` da `strumenti/dati.py` (i prezzi letti
a mano) e `strumenti/lista.py` (i dodici prodotti di partenza). Per aggiornarla
si ripubblica **lo stesso percorso di file** in una sessione che l'ha già
pubblicata, oppure si passa l'URL qui sopra come `url`: altrimenti esce un
artifact nuovo con un indirizzo diverso e il link della moglie muore.

### Com'è fatta la pagina, e perché

Manlio ha provato la prima versione e l'ha bocciata: «è brutto e non è comodo
da navigare», «così non si può vedere». Due cose da non rifare:

- **Niente tema scuro.** Il suo telefono è in modalità notte e la pagina gli si
  apriva nera. Adesso c'è **un solo tema chiaro**, sfondo bianco, e nel CSS
  **non esiste** il blocco `prefers-color-scheme: dark`. Se lo rimetti, si
  riapre nera da lui. Lo sfondo è dichiarato su `html` e su `body`, perché
  senza, la pagina prende quello di chi la ospita.
- **I prodotti sono bottoni in cima**, dentro una barra `sticky`: se ne tocca
  uno e la lista di sotto si riempie subito, già ordinata dal meno caro. Prima
  erano schede da aprire e chiudere una alla volta e per arrivare al tonno
  bisognava scorrere. Il «+ aggiungi» è l'ultimo bottone della fila.

Bersagli grandi (44-46 px) come nella Palestra: si usa in piedi, in negozio.

### La lista adesso vive DENTRO la pagina pubblicata

Cambiata il 2026-09-03. Manlio ha chiesto che la lista sia una sola per lui e
sua moglie, che ognuno possa aggiungere e togliere, e che le sue modifiche
arrivino anche a me senza doverle reincollare.

Si usa la capacità **`artifact`**, non `db`: `db` avrebbe reso l'artifact
interno all'organizzazione e la moglie non sarebbe più entrata (vedi sotto). Con
`artifact` la pagina, quando qualcuno tocca la lista, **ripubblica se stessa**
con la lista nuova dentro, e ogni schermo aperto si ricarica su quella.

**Il documento contiene una copia di se stesso.** `TEMPLATE` è il documento
intero con i due segnaposto `__LISTA__` e `__TEMPLATE__` ancora dentro, non
risolti: è quello che permette alla generazione dopo di rifare la stessa cosa.
`documento()` riempie **prima la lista e poi il modello** — al contrario, il
modello appena infilato porterebbe dentro un altro `__LISTA__` e verrebbe
riempito quello sbagliato.

Tre trappole, tutte già pagate:

1. **I segnaposto compaiono due volte**: quello vero in cima allo script e la
   stringa dentro `documento()` che serve a sostituirlo. `riempi()` in
   `pagina.py` usa `count=1` e JavaScript si ferma da solo alla prima. Senza,
   `documento()` si rompe e il file cresce di 200 KB inutili.
2. **`</script>` dentro la stringa chiuderebbe il tag per davvero**: si scrive
   `<\/`. Lo fanno sia `racchiudi()` in Python sia `documento()` in JavaScript,
   e devono restare d'accordo.
3. **Il documento ripubblicato deve essere intero** (doctype, head, body), che
   invece al file dato allo strumento Artifact li mette il servizio. Per questo
   il modello è `COMPLETO` e non `CORPO`.

Il punto fisso è provato: rigenerando tre volte il modello resta identico e il
documento non cresce (445 KB). Se tocchi questa parte, riprova così — è un
controllo che si fa in Node in un minuto e ti risparmia una pagina rotta in mano
a loro.

Chi apre in sola lettura riceve `not_writer`: le sue modifiche restano nel
browser e la riga di stato in cima glielo dice. La stessa cosa vale per il file
`spesa-da-sola.html`, dove `window.claude` non esiste proprio.

### Cambiando prodotto si torna all'inizio dell'elenco

Manlio, 2026-09-05: scorreva i prezzi del tonno, toccava «Suino», e si
ritrovava **in mezzo** all'elenco del suino. La pagina cambiava sotto ma la
finestra restava dov'era.

`inCima()` riporta al **primo prezzo**, non in cima alla pagina: la barra dei
bottoni è appiccicata in alto e resta lì, così si vede insieme quale bottone è
acceso e da dove parte l'elenco. Non si muove se si è già sopra quel punto, e
non si muove se si ritocca il bottone già acceso.

Il taglio a zero della meta va fatto **prima** del confronto «sono già sopra?»:
con una meta negativa quella domanda risponde sempre no, e la pagina chiederebbe
di scorrere anche stando ferma in cima. Trovato da `prova-scorrimento.js`, non
rileggendo.

**Quella prova ha dovuto fingere l'impaginazione.** jsdom non impagina: lasciato
fare, ogni misura viene zero, il conto torna per caso e la prova passa senza
aver controllato niente. Le misure gliele diamo noi — elenco a 420 dall'alto,
barra alta 150 — e si pretende esattamente 262. Una prova che non può fallire
non è una prova.

### I prodotti nuovi arrivano anche su chi ha già la sua lista

Il 2026-09-05 Manlio ha aperto il sito cercando lo yogurt di cui gli avevo
appena parlato e **non c'era**. Non era un buco nei dati: sul suo telefono la
lista aveva nove bottoni, con dentro «Dentifricio» che si era aggiunto lui, e
senza i quattro prodotti chiesti il 4 settembre — biscotti, yogurt, marmellata,
cioccolato.

È la conseguenza diretta di `CONDIVISA`: sul sito comanda la lista salvata nel
browser, e appena uno la tocca quella comanda per sempre. I prodotti aggiunti
dopo non arrivavano più a chi si era già fatto la sua.

Adesso `aggiungiNuovi()` mette in fondo alla lista salvata i prodotti della
lista pubblicata che **quel telefono non ha mai visto**. La memoria di cosa ha
visto sta in `spesa.visti.v1`, a parte dalla lista: ci finisce ogni nome
pubblicato e ogni nome che la lista ha avuto, e **ci resta anche dopo che il
prodotto è stato tolto**. Senza quella memoria ogni cancellazione sarebbe stata
annullata al ricaricamento dopo, che è il baco opposto e peggiore.

Due dettagli che sembrano piccoli e non lo sono:

- **La lista unita si salva subito**, dentro `aggiungiNuovi()`, senza aspettare
  che l'utente tocchi qualcosa. Al caricamento dopo i nuovi risultano già
  visti, quindi non verrebbero riaggiunti: sparirebbero un'altra volta.
- **La prima volta la memoria dei visti non c'è.** Allora valgono per visti i
  prodotti che la lista ha in quel momento — così i mancanti sono davvero
  prodotti mai arrivati fin lì, non prodotti tolti apposta prima che questa
  memoria esistesse.

`prova-arrivi.js` rifà esattamente il suo caso: telefono con la lista di nove,
Dentifricio compreso; devono arrivare i quattro, restare il suo, e una
Marmellata tolta apposta non deve tornare all'apertura dopo.

### `lista_attuale.py`: non cancellargli la lista

**Il pericolo grosso di tutta questa architettura.** L'aggiornamento
settimanale rigenera la pagina; se ripartisse da `lista.py` cancellerebbe la
lista che si sono fatti loro. Quindi prima si legge la pagina viva
(strumento Artifact, action "read"), si passa a `lista_attuale.py`, che scrive
`lista-attuale.json`, e `pagina.py` riparte da quello. `lista.py` serve solo la
prima volta.

Se la lista non si riesce a leggere, **fermarsi**: meglio prezzi vecchi che una
lista cancellata.

### Perché NON si è usata la memoria sul server (`db`)

`db` sarebbe più semplice da scrivere, ma **un artifact che dichiara `db`
diventa interno all'organizzazione** e non si condivide fuori. Sul piano Pro di
Manlio l'organizzazione è lui solo: la moglie resterebbe fuori, che è la cosa
che ha chiesto fin dall'inizio di poter fare. Per questo si è presa la strada
più scomoda della pagina che si ripubblica.

`localStorage` (chiave `spesa.lista.v1`) resta solo come ripiego, per la copia
che gira come file. Letture e scritture in try/catch: in navigazione privata la
memoria può mancare e la pagina deve funzionare lo stesso.

**Il baco che ha fatto venire fuori tutto**: Manlio aveva tolto la carta
igienica e se la ritrovava. Non era un baco nel togliere (provato in Node,
funziona): aveva **due copie**, il link e il file, ognuna con la sua memoria.
Togliere in una non toccava l'altra. Con la lista dentro la pagina il problema
non esiste più.

### Tutte e dodici le categorie hanno i prezzi

Il 2026-09-02 Manlio ha chiesto i prezzi anche per le nove categorie che avevo
messo io. Adesso `dati.py` ha **68 righe su 12 categorie**, tutte lette
guardando le pagine — nessuna inventata, nessuna dedotta dall'OCR.

Ogni prodotto di `lista.py` ha il campo `cat` che punta alla categoria di
`dati.py`. Il legame è esplicito e serve: cercando per testo, «olio» pescava i
tonni all'olio d'oliva e sembravano offerte sull'olio. Un prodotto aggiunto a
mano dalla pagina non ha categoria, ma se quello che scrive combacia col nome o
con una parola di uno dei dodici, `costruisci()` glielo attacca da sola.

**Le unità non sono tutte il chilo.** `UNITA` in `dati.py` dice per ogni
categoria come si confronta: chilo per carne, tonno, salmone, caffè, pasta,
pollo e formaggio; **litro** per latte e olio; **uovo**, **rotolo** e
**lavaggio** per le altre tre. Al chilo il detersivo darebbe un numero vero e
inutile. I detersivi stanno sotto i 20 centesimi a lavaggio, per questo `eur()`
nella pagina usa tre decimali sotto l'euro: con due diventavano tutti «0,14 €».

Due righe confrontano di proposito cose non identiche, e lo dicono nelle note:
l'ammorbidente Coccolino sta fra i detersivi (si usa in aggiunta, non al posto)
e il caffè in capsule sta col macinato (al chilo costa cinque volte tanto). E la
carta igienica Regina è «4 rotoloni pari a 12 rotoli»: il conto usa i 12
dichiarati sul pacco, e la nota dice quanto fa sui 4 veri.

### Sotto il nome del prodotto non ci va niente

Manlio, 2026-09-05, con una foto e l'evidenziatore: sottotitolo, riga «questa
copia è solo tua», conteggio delle offerte, sinonimi e «Cambia nome» tutti
segnati da togliere. «Toglierei tutto quello che c'è scritto dopo carne di bue
e lascerei solo una piccola scritta o un'icona per cancellarla.»

Adesso accanto al nome ci sono **due soli bottoni**: il bollino «i», che apre
conteggio, sinonimi e cambio nome, e una **crocetta** per togliere il prodotto.
La crocetta **chiede conferma lì dov'è**, con «Togli» e «Lascia»: è piccola e
sta accanto al nome, un tocco per sbaglio non deve far sparire un prodotto. Non
si usa la finestrella di sistema, che sul telefono arriva da tutt'altra parte.

Sotto i bottoni la riga di stato dice **solo le novità di adesso** («Aggiunti
alla tua lista: …»). «Questa copia è solo tua» è vero per sempre e occupava due
righe di schermo: è finito dietro il bollino in cima.

**IL BOLLINO IN CIMA HA UCCISO LA PAGINA, per venti minuti.** Il codice che
collega i bollini faceva `b.closest('h2').nextElementSibling`. Il bollino nuovo
sta in un `h1`, quindi `closest('h2')` ha dato niente, l'errore ha fermato tutto
lo script e la pagina è uscita **muta** — bottoni compresi. Stesso guasto del
tag di chiusura scritto per esteso: da fuori sembra a posto e non funziona
niente. Adesso cerca `h1, h2`; se un bollino finisce in un `h3` va aggiunto lì.

`prova-intestazione.js` pretende che a pagina appena aperta si vedano solo il
nome, il bollino e la crocetta, e che «Lascia» non cancelli niente.

### Una categoria con una sola offerta è quasi sempre un buco mio

Manlio, 2026-09-05: «delle pizze generalmente tutti i volantini offrono
un'offerta di pizza e qua ne hai trovate solo una». Aveva ragione: ce n'erano
**otto**, e ne avevo filata una.

Il motivo non era il programma. **Due di quelle pizze le avevo già lette a
occhio** — la pagina 12 dell'MD e la 15 dell'Eurospin — ma quel giorno «Pizza
surgelata» non era ancora una categoria, e sono passate sotto gli occhi senza
finire da nessuna parte. Le altre cinque stavano su pagine che non avevo aperto.

**Il controllo che ne esce**, e che va rifatto a ogni giro: guardare le
categorie con zero o una sola offerta e chiedersi se è credibile. Alcune lo
sono davvero (le uova sono in offerta da uno solo), altre no: se sei
supermercati su sette non hanno la pizza, non è il mondo, sono io.

`indice.json` serve proprio a questo: cercare la parola dice subito in quali
pagine guardare, e le pagine sono ordinate per quante parole ci si sono trovate.

Quel giro ha riempito anche **Gelato** (dieci offerte), **Burro**, **Bastoncini
di pesce** e **Calamari e seppie**, che erano vuote: stavano tutte sulle stesse
pagine di surgelati che avevo saltato.

**Due pizze non si possono mettere**: il volantino Ipercoop, per la Roncadin e
la Pinsa, stampa solo «sconto 50%» e nessun prezzo. Senza prezzo non c'è riga.

### Le pagine da guardare: parole intere, non pezzi di parola

Manlio, 2026-09-05: «per pizza surgelata appaiono sotto un elenco di pagine del
volantino nel quale la pizza non c'entra per niente. Prova a individuare
motivo».

Il motivo: `pagineDi()` cercava il termine **dentro** il testo della pagina, in
qualunque posizione. Così «oro» (che sta lì per Oro Saiwa) lo trovava dentro
«loro», «cola» dentro «piccola», «anca» dentro «bianca». Per i biscotti erano
**69 pagine, di cui 45 rumore**.

Adesso il confronto è a **parola intera**, su un insieme invece che su una
stringa: più preciso e più veloce. Biscotti passa da 69 pagine a 24, Tonno a 19.

Restano le pagine che nominano il prodotto **per davvero ma di sfuggita** — una
ricetta che cita la pizza, una mozzarella «per pizza». Quelle non si possono
togliere senza capire il senso della frase, e l'OCR non lo capisce. Perciò:

- le pagine sono **ordinate per quante parole ci ho trovato**, le più forti in
  cima (una che ha «pizza, surgelata» parla di pizze surgelate; una che ha solo
  «pizza» può essere una ricetta);
- **ogni riga dice cosa ci ha trovato**: «ci ho trovato: pizza, surgelata». Così
  si giudica invece di indovinare.

E una parola è stata tolta dal catalogo: **«margherita»**. Sui volantini è una
moka Bialetti e un fiore, non una pizza — trovata proprio guardando quell'elenco.

`prova-pagine.js` pretende che nessuna pagina entri per un pezzo di parola, che
le più forti stiano in cima e che ogni riga dica cosa ha trovato.

### Il catalogo e il cassetto

Chiesto da Manlio il 2026-09-05, dopo aver visto tre proposte disegnate e
provate col dito (ha scelto la prima, il cassetto per reparti, con dentro la
ricerca della seconda).

Il problema che risolve, con le sue parole: «il sistema di copiare la lista e
poi inviartela è scomodo, inefficiente, e può essere fatto solo da me».
Aggiungere un prodotto voleva dire scriverne il nome e poi aspettare che io ne
leggessi i prezzi. Adesso **il catalogo è già pronto e ognuno accende i suoi**,
sul suo telefono, senza chiedere niente a nessuno.

`catalogo.py` tiene **66 voci in 9 reparti**, ognuna con nome, parole del
volantino e **unità di confronto**. È l'unico posto dove stanno le categorie:
prima `UNITA` era una lista a parte dentro `dati.py` e a ogni categoria nuova
bisognava ricordarsi di aggiungerla in due posti. `dati.py` adesso si ferma con
un errore chiaro se un prezzo finisce in una categoria che il catalogo non ha —
prima quel prezzo si caricava e non lo vedeva nessuno, in silenzio.

**Le categorie grosse si sono divise, e questo rompe le liste salvate.**
«Detersivo» è diventato lavatrice, lavastoviglie e ammorbidente; «Formaggio»
ha lasciato andare mozzarella, grana, spalmabili e ricotta; «Suino» ha lasciato
andare tutti i salumi. Serviva: un elenco che mescola parmigiano e mozzarella
mette in cima l'offerta sbagliata. Ma chi aveva il bottone «Detersivo» si
sarebbe ritrovato un prodotto senza più nessun prezzo. Perciò `riaggancia()`
**butta una categoria che il catalogo non conosce** e riprova ad agganciare dal
nome. Non toglierlo.

Il cassetto sta dentro la barra, chiuso. Chi non tocca «+ altri prodotti» non
si accorge nemmeno che il catalogo esiste — era la ragione per cui questa
proposta ha vinto sulle altre due. La ricerca filtra **anche sulle parole del
volantino**: «bovino» trova «Carne di bue». La casella per scrivere un nome
libero non è sparita, è finita in fondo al cassetto: serve per quello che nel
catalogo non c'è.

**IL CASSETTO NON VA DENTRO LA BARRA APPICCICATA.** Ci stava, ed è durato
mezza giornata: la barra è `position:sticky`, quindi aprendo il cassetto
diventava più alta dello schermo, e il telefono doveva rifarne i conti a ogni
tocco e a ogni scorrimento. Manlio: «escono solo le prime categorie, poi la
pagina resta bloccata per un tempo abbastanza lungo». Ci si metteva anche il
riempimento a rate — i nove reparti infilati uno per uno, con un ricalcolo per
ognuno mentre la roba cresceva — e la tastiera che saltava su perché la casella
di ricerca prendeva il fuoco da sola.

Tre rimedi, tutti e tre necessari: il cassetto **fuori** dalla barra, i reparti
messi dentro **in un colpo solo** con un `DocumentFragment`, e **niente focus**
all'apertura (chi vuole cercare tocca la casella; la tastiera che copre mezzo
schermo mentre uno si guarda i reparti è il contrario di quello che serve).

**Questo guasto in un browser finto non si vede**, perché lì non si impagina
niente. Quindi `prova-cassetto.js` non misura la lentezza, che è l'effetto:
controlla che il cassetto **non sia dentro `.barra`** e che la casella non
prenda il fuoco, cioè le due cause.

`prova-cassetto.js` apre, cerca, accende, spegne e richiude, e pretende che un
prodotto acceso dal cassetto mostri davvero i suoi prezzi.

### Trappole del leggere i volantini per il catalogo

**Certe pagine hanno date loro, e adesso si sanno dire.** Nel volantino MD
dell'8-20 settembre la pagina 35 è un «Weekend più uno» valido **18-21
settembre**. Prima quelle pagine si saltavano; il 2026-09-05 Manlio ha chiesto
di farle per bene, e una riga di `PRODOTTI` può avere **due campi in più in
fondo**, primo e ultimo giorno. Le righe senza restano come sono: `Offerta` è
una namedtuple con valori vuoti di scorta, e nessuna delle 230 righe già
scritte è stata toccata.

Un'offerta con date sue **si vede solo nei giorni in cui vale**, e in quei
giorni porta un bollo rosso «solo dal 18 al 21 settembre». Un **volantino
intero** non ancora cominciato invece resta visibile in fondo con «vale dal»:
quello è voluto, serve a sapere cosa arriva, e lì è tutto il volantino e si
vede. La differenza è deliberata, non una svista.

**Ogni riga dice fino a quando vale.** I volantini durano periodi diversi —
Lidl una settimana, Carrefour due, Ipercoop dieci giorni — e guardando un
prezzo non si sapeva se valeva ancora domani. `prova-quando.js` pretende che
NESSUNA riga sia senza durata.

**Le pagine si scelgono con l'OCR, non a caso.** Contando quante parole di ogni
categoria vuota compaiono in ogni pagina si ottiene l'elenco delle pagine che
rendono di più: la 26 del Carrefour da sola ha riempito acqua, vino, birra e
bibite. Leggere in quell'ordine cambia il lavoro di una giornata.

**Conviene leggere prima i volantini che durano.** Il 2026-09-05 il vecchio
Eurospin e il vecchio MD scadevano il giorno dopo: leggerne le pagine per le
categorie nuove sarebbe stato lavoro buttato.

### Più nomi per lo stesso prodotto

Chiesto da Manlio il 2026-09-02: «ci sono delle cose che possono essere salvate
con più di un nome». È il motivo per cui i dodici di partenza avevano già una
lista di `parole` — il volantino scrive «bovino» dove lui dice carne di bue, e
«lavatrice» dove dice detersivo. Fino a quel giorno però quel meccanismo era
solo mio: nella pagina non si vedeva e non si poteva usare.

Adesso nel campo si scrivono **più nomi separati da virgola** e `costruisci()`
li spezza: il primo diventa l'etichetta del bottone, tutti insieme sono i
termini di ricerca in OR. Gli altri nomi si vedono sotto il titolo come
pastiglie, e «Cambia nome» riapre il campo con tutti quanti dentro, separati da
virgola, così si correggono.

Se **uno qualsiasi** dei nomi scritti combacia con un prodotto di partenza (col
nome o con una delle sue parole), il prodotto si porta dietro anche la categoria
dei prezzi e le parole di quel seme. Così chi scrive «bovino» o «caffe» a mano
ritrova i prezzi invece delle sole pagine.

### `riaggancia()`: le liste salvate prima

Chi aveva già usato la pagina ha in `localStorage` una lista fatta quando solo
carne, tonno e salmone avevano i prezzi: quei prodotti sono salvati con
`cat: null` e, senza fare niente, resterebbero **senza prezzi per sempre** anche
dopo che i prezzi sono arrivati. `riaggancia()` gira su ogni prodotto letto
dalla memoria e, se non ha categoria, cerca un seme che combaci per nome o per
parola e gliela attacca — senza toccare i nomi che l'utente si è scelto. Un
prodotto aggiunto da lui che non corrisponde a niente resta senza, ed è giusto.

**Non togliere `riaggancia()`**: ogni volta che si aggiungono categorie nuove a
`dati.py` serve di nuovo, o chi ha la pagina in uso non le vede mai.

### «Ma io li ho cambiati nella pagina, perché devo ridirteli?»

Domanda di Manlio, ed è giusta. La risposta è che la lista sta in `localStorage`
sul suo telefono e **non torna indietro a chi ha fatto la pagina**: non esiste un
canale. L'unico modo per vederla davvero sarebbe la capacità `db`, che però
chiude la pagina dentro l'organizzazione e taglia fuori la moglie — vedi sopra.

Il rimedio è il riquadro **«Mandami la tua lista»** in fondo alla pagina: un
bottone impacchetta la lista in testo (nome più i nomi alternativi) e la copia,
lui la incolla in chat. È l'unico ponte che c'è, quindi **non toglierlo**: senza,
ogni volta bisogna chiedergli di riscrivere a mano quello che ha già scritto,
e infatti la seconda volta si è spazientito.

La `textarea` sotto il bottone **non è un di più**: negli artifact la scrittura
negli appunti può essere negata in silenzio, e in quel caso il testo deve
restare lì da selezionare a mano. Il `catch` scrive cosa fare.

### I volantini nuovi si leggono in anticipo, e si vede

Chiesto da Manlio: prendere il volantino nuovo **il giorno prima** che scada il
vecchio. Il 2026-09-05 quella regola ha mostrato il suo lato scomodo: Eurospin
e MD scadevano il 6, ma i volantini nuovi partivano l'**8** (MD) e il **10**
(Eurospin). Metterli dentro e basta avrebbe fatto comparire in cima all'elenco,
col bollo «il meno caro», prezzi che in cassa non gli avrebbero fatto per altri
cinque giorni.

Quindi `VOLANTINI` ha un campo in più, **`inizio`**: se c'è ed è nel futuro, la
pagina mette quelle righe **in fondo** al loro elenco, toglie loro il bollo «il
meno caro» e ci scrive sopra **«vale dal 10 settembre»**; nell'elenco dei
volantini l'insegna esce segnata «non ancora cominciato». `prova-quando.js`
controlla proprio questo: nessuna riga non ancora valida sopra una valida, e
nessuna col bollo del più conveniente.

**Scaduto e «non ancora» li decide la pagina, non il generatore.** Le due date
finiscono nel documento e il confronto con oggi lo fa il browser di chi apre.
Se il giudizio fosse congelato al giorno della generazione, il 7 settembre la
pagina avrebbe continuato a dare per buone le offerte scadute il 6 finché
qualcuno non la rigenerava — e chi rigenera, per ora, non è affidabile. Così il
peggio che può capitare è che manchino offerte nuove, mai che ne compaiano di
finite. `prova-quando.js` lo prova fingendo la data: `node prova-quando.js
out/sito.html 2026-09-07`. Quando una categoria resta senza prezzi perché sono
tutti scaduti, la pagina lo dice invece di mostrare il vuoto.

`VOLANTINI` è diventato una lista di **namedtuple**. Aggiungere un campo a delle
tuple nude avrebbe fatto saltare in una volta gli otto punti che le
spacchettavano per posizione; con i nomi, chi non usa il campo nuovo non se ne
accorge. Il prossimo campo si aggiunge senza paura.

### I volantini si rinnovano da soli

Chiesto il 2026-09-03: prendere il volantino nuovo **il giorno prima** che
scada il vecchio, e cancellare il vecchio **due giorni dopo** che è scaduto per
non farne collezione.

`VOLANTINI` in `dati.py` ha adesso un quinto campo, l'**ultimo giorno di
validità**. `pulisci.py` lo legge e dice cosa rinnovare e cosa buttare;
con `--fai` cancella davvero pagine, OCR e PDF. I due giorni di tolleranza
servono a poter ancora controllare l'offerta di ieri contro lo scontrino.

C'è una **Routine giornaliera** (`trig_01UMkRYxHXJfPBSEZLo7Snzb`, ogni giorno
alle 04:00 UTC) che apre una sessione nuova, esegue `pulisci.py` e, se non c'è
niente da fare, **si ferma senza scrivere a nessuno** — è il caso normale. Se
invece qualcosa scade, rifà il giro e ripubblica. Il prompt della Routine
contiene tutti i passi; è il posto da correggere se il giro cambia.

**Il 2026-09-04 non funzionava, e il perché è istruttivo.** La Routine è partita
due volte, ha lavorato cinque minuti, e non ha pubblicato niente: nessun commit,
nessuna ripubblicazione. Manlio l'aveva chiesto lui stesso — «non so se funziona
la cosa che toglie i volantini vecchi e mette quelli nuovi» — e aveva ragione a
dubitare.

Le cause erano tre, tutte perché **la sessione che parte non trova quello che
serve già pronto**:

1. **`indice.json` non stava nel progetto.** Viveva nella cartella di lavoro
   della sessione che l'aveva costruito, e quella cartella sparisce. Senza,
   `pagina.py` non parte proprio. Adesso `indice.json` è dentro il progetto e
   `indice.py` lo **aggiorna** invece di rifarlo: si scarica e si legge soltanto
   il volantino nuovo. Rifarli tutti e sette voleva dire ~240 pagine da scaricare
   e passare all'OCR, cinque minuti buoni prima ancora di cominciare.
2. **`pagina.py` guardava i file `pg/*/*.jpg`** per sapere quali pagine
   esistono. Senza le immagini sul disco l'elenco veniva vuoto. Adesso si fida
   dell'indice, che contiene solo pagine esistite davvero.
3. **Le date dei volantini erano scritte in tre posti** (`dati.py`, `indice.py`,
   `scarica.sh`) e le copie divergevano. Adesso stanno solo in `dati.py`:
   `indice.py` e `scarica.py` le leggono da lì.

**La regola che ne esce:** tutto ciò che serve per rigenerare la pagina deve
stare **dentro il progetto**, perché la sessione che rigenera parte da un clone
e da niente altro. Se un passo dipende da un file che non è committato, quel
passo non funzionerà mai in automatico — e fallirà in silenzio.

**Il rinnovo del 2026-09-04, fatto a mano ma con la strada nuova**, è la prova
che il giro funziona: via il Carrefour Iper del 20 agosto (scaduto il 3), letti
a occhio 14 prezzi dalle pagine del suo sostituto, e sul sito in linea si
contano 126 prezzi e sette volantini, nessuno scaduto. Prima erano 113 e otto,
con quello vecchio ancora in elenco.

**La prova del 2026-09-05 è andata male.** La Routine è partita alle 04:07, ha
lavorato **diciassette minuti** (324.000 gettoni, 5,28 dollari) e ha finito
senza nessun commit, nessuna ripubblicazione e nessun messaggio — il terzo
giro a vuoto di fila, e di nuovo in silenzio, che è la cosa che il prompt le
vietava esplicitamente. Le riparazioni del giorno prima le hanno dato più
strada da fare, non l'hanno fatta arrivare in fondo.

**`registro.txt` serve a smettere di tirare a indovinare.** Dal 2026-09-05 il
controllo giornaliero scrive una riga a ogni passo (`python3 -m registro
"clonato"`) e la spinge sul progetto. Se domani lì dentro c'è «clonato» e non
c'è «pubblicato», si sa che clone e spinta funzionano e il guaio sta in mezzo;
se non c'è nemmeno «clonato», il guaio è prima. È il modo più stupido che
funziona, ed è l'unico: una sessione partita da sola non lascia niente da
rileggere.

**Quello che si sa e quello che non si sa.** Si sa che ha lavorato sul serio
(diciassette minuti e quel consumo non sono un giro a vuoto) e che non ha
pubblicato. Non si sa dove si sia fermata: la sessione che parte da una Routine
non lascia niente da leggere qui, e finché è così ogni diagnosi è un'ipotesi.
**Perciò il rinnovo non si lascia più solo a lei.** Finché non la si vede
arrivare in fondo almeno una volta, i volantini nuovi si mettono a mano — come
il 4 e il 5 settembre — e la Routine vale come tentativo, non come garanzia.
Dirlo a Manlio in questi termini, non promettergli che «adesso funziona».

**I PDF non si accumulano da nessuna parte**: vivono nella cartella di lavoro
della sessione, che è temporanea e sparisce da sola. Le copie che ha Manlio sono
quelle nella chat, sul suo telefono, e quelle le cancella lui.

### L'aggiornamento delle offerte

Manlio ha chiesto che **anche la moglie possa aggiornare le offerte dal suo
telefono**. Non si può, e non è un limite da aggirare: aggiornare vuol dire
riscaricare i volantini, rifare l'OCR e rileggere le pagine a occhio. Una pagina
web non lo può fare — i siti dei supermercati non concedono CORS, e comunque i
prezzi grandi l'OCR non li legge.

Quello che invece funziona: **ripubblicando l'artifact, chi ha il link vede i
prezzi nuovi ricaricando**, senza che nessuno debba mandare niente a nessuno.
Nella pagina c'è una sezione che lo dice, con la data dei volantini letti
(campo `letto` in `pagina.py`, **da aggiornare a ogni giro**). Il file
`spesa-da-sola.html` invece resta fermo: è la copia di riserva, non il canale
di aggiornamento.

**Mercatò c'è, dal 2026-09-05.** Per tre giorni non c'era, e la ragione era
sbagliata: avevo guardato il sito loro (che carica il volantino con JavaScript
e non espone né PDF né immagini) e VolantinoFacile (identificativo per pagina
non prevedibile), e mi ero fermato lì. Manlio è tornato sull'argomento —
«le offerte del mercato sono per me quasi indispensabili, quasi tutti i giorni
vado a fare la spesa lì» — e cercando davvero, alla terza fonte, il volantino
c'era: **kimbino.it**, 36 pagine intere a 1550 px, l'unica fonte che lo pubblica
per intero.

Lezione, la stessa della pizza: **quando manca qualcosa che il mondo ha di
sicuro, il buco è mio.** Tutti i supermercati fanno il volantino; se non lo
trovo, ho guardato nel posto sbagliato o l'ho chiamato col nome sbagliato — su
anteprimavolantino c'è un `ins-mercato` che sembra lui e invece è INS Mercato,
un'altra insegna. Non archiviare un'insegna dopo due tentativi.

**Come si prendono le pagine.** Il volantino sta su

    https://www.kimbino.it/mercato/mercato-volantino-da-giovedi-<GG-MM-AAAA>-6<ID>/

e dentro quella pagina ci sono gli indirizzi delle immagini. Sono **firmati**:
un codice calcolato sull'indirizzo intero, quindi la pagina 12 non si ricava
dalla 11 e lo schema con `{n}` non esiste. Per questo — e solo per questo
volantino — c'è `strumenti/pagine_mercato.py`, l'elenco delle 36 pagine in
ordine, e `Volantino` ha un campo `pagine` che dove c'è vince sull'indirizzo a
schema. Si rifanno **a ogni volantino nuovo**, insieme alle date: si tengono
gli indirizzi che contengono `/0x0/` (le pagine intere; quelli con `240x240`
sono le miniature) e si ordinano per il numero prima di `.jpg`.

**Quale Mercatò: via Filadelfia 232, e non è una deduzione.** Ce ne sono quattro
insegne (Mercatò, Local, Big, Extra) con volantini diversi, e a Torino ci sono
quattordici punti vendita. Il primo giorno l'avevo scelto io, per distanza; il
2026-09-05 Manlio ha chiesto di vederli tutti — «fammeli vedere che te lo
dico» — **e ha confermato via Filadelfia 232**. Adesso è un fatto, non una
supposizione: chi riprende in mano il progetto non deve ricalcolarlo.

**La distanza da sola avrebbe sbagliato.** Il punto vendita più vicino a corso
Siracusa è via Demargherita (0,4 km), ma è un **Mercatò Local**, che ha un
volantino suo: se avessi tirato a indovinare col metro avrei caricato i prezzi
di un altro negozio. Quando la scelta cambia i dati e solo lui la sa, si
chiede.

Se un giorno dicesse che va in un altro, va cambiato il volantino, non solo le
date — e va guardata l'insegna, non solo il nome della via.

**L'Ipercoop di Torino è Nova Coop**, non la Coop nazionale: il volantino è
quello piemontese. Si prende da `novacoop.it`, che rimanda a
`negozi.volantinopiu.com/ccno-8001120004796.html` (punto vendita di via Livorno
49). Lì le pagine hanno indirizzi **prevedibili**, molto più comodi degli altri:

    https://resources.volantinopiu.it/flyer/2/8/4/8/0/pagine/<N>.jpg

cioè le cifre dell'identificativo del volantino separate da barre. Attenzione:
in quella pagina **il titolo di ogni volantino sta prima della sua immagine, non
dopo** — leggendolo al contrario ho scaricato per sbaglio il volantino degli
zaini di scuola e quello dei frigoriferi. Controllare sempre le parole che
l'OCR tira fuori: se saltano fuori «quaderni» e «zaino», è quello sbagliato.
Dei cinque volantini Nova Coop, quelli di spesa sono **Sottocosto** ed
**Extra offerte**.

**La fonte risponde 200 anche quando la pagina non c'è.** Il 2026-09-05
`volantino-eurospin-2026-09-07-p-01.jpg` ha risposto **200 con un'immagine da
1,2 KB**: non esisteva. E anche i 403 arrivano con un corpo di quella misura.
In più, chiedendo tante pagine di fila, il sito ne molla qualcuna con una
risposta da ~12 KB che sembra un errore e non lo è: rallentando torna buona.
Perciò `scarica.py` **guarda la dimensione, non il codice** — sotto i 20 KB non
è una pagina di volantino — e riprova tre volte prima di rinunciare. Contare le
pagine fermandosi al primo buco dà numeri sbagliati: l'Eurospin risultava di 5
pagine invece di 22.

**Da Ipercoop molti prezzi sono riservati ai soci Coop** e sul volantino ci sono
tutti e due, barrato e scontato. Nell'Excel e nella pagina ho messo il prezzo
soci scrivendolo nelle note, perché è quello che paga lui se ha la tessera.

## La pagina delle novità — messa via, e rimessa il 2026-09-10

Fatta il 2026-09-05 e **tolta lo stesso giorno**, su richiesta di Manlio: «sono
andato a vedere la pagina novità ed è vuota per adesso, lasciala perdere e
togli anche il pulsante». Aveva ragione — il diario era partito quella mattina,
e una pagina che non ha niente da dire è solo un tasto in più.

**Rimessa il 2026-09-10**, quando lui ha detto «mi sembra ora di implementarli».
Nel frattempo il diario aveva accumulato due giornate vere, e la seconda non era
poca roba: il 9 settembre il più conveniente è cambiato in **dieci** categorie.

**Una cosa è stata cambiata rimettendola: adesso si apre dove c'è qualcosa.**
Prima partiva sempre da «Oggi», e oggi era vuoto — cioè si sarebbe riaperta
esattamente com'era il giorno in cui lui l'aveva bocciata. È la stessa lezione
dello Storico della Palestra, che si apriva sul mese corrente e il 2026-09-01,
col mese nuovo ancora vuoto, gli ha fatto credere di aver perso tutti i dati.
Qui capita più spesso ancora, perché i volantini non cambiano tutti i giorni.
Adesso, se oggi non c'è niente, parte da «Ultimi 7 giorni»; i due tasti restano
tutti e due e si passa dall'uno all'altro. **Non rimetterlo su «Oggi» fisso.**

Il tasto sta in alto a destra e punta all'**indirizzo completo** del sito, non a
`./novita.html`: la copia di Claude non ha una cartella accanto a sé e un
collegamento relativo di là porterebbe nel vuoto. `novita.html` sta anche
nell'elenco di `sw.js`, così in negozio si apre senza rete.

**Va rigenerata a ogni giro**, subito dopo `storia`: `python3 -m novita` e poi
`cp out/novita.html <progetto>/novita.html`. Se te ne dimentichi, il tasto resta
ma racconta la settimana scorsa.


Chiesta da Manlio il 2026-09-05: le novità dell'ultimo giorno e, volendo,
quelle dei sette precedenti, in una pagina che si apre in un'altra finestra col
suo tasto in cima alla pagina dei prezzi.

`novita.py` legge i file che `storia.py` lascia in `storia/` — uno per giorno,
scritto solo quando è successo qualcosa — e ne fa `novita.html`, statica come
tutto il resto. Il tasto **Novità** sta in alto a destra e punta all'indirizzo
completo, così funziona anche dalla copia di Claude, che non ha una cartella
accanto a sé.

**L'ordine dei blocchi non è estetico.** In cima **il più conveniente che ha
cambiato padrone**: è l'unica novità che cambia dove si va a fare la spesa.
Poi i volantini arrivati e finiti, i prezzi scesi e saliti (con quanto), le
offerte nuove e quelle finite, e in fondo in grigio gli spostamenti di reparto.

**Il conto del più conveniente deve guardare le date.** La prima versione non lo
faceva, e appena entrate le sette offerte del «Weekend più uno» il diario ha
annunciato che il pollo più conveniente erano dei würstel a 2,29 — veri, ma
validi dal 18 settembre, tredici giorni dopo. **Una novità falsa è peggio di
nessuna novità: manda uno in negozio.**

**Il 2026-09-10 il problema di `stato.json` è diventato vero, non più solo
teorico.** Finché il tasto Novità era spento non faceva danno che ogni sessione
nuova partisse senza fotografia; da quando è acceso, sì. Quel giorno due
sessioni diverse hanno rigenerato `storia` nello stesso pomeriggio: la prima
(quella che ha rimesso il tasto) aveva una fotografia vera di qualche ora prima
e ha scritto un giorno vero; la seconda (questa, una Routine su un clone
nuovo) è partita senza `stato.json` — è nel `.gitignore` apposta — e ha scritto
sopra una «prima fotografia», perdendo il confronto. Risultato: il 10 settembre
non compare in `storia/` come giorno con novità, anche se quel giorno sono
stati letti per intero quattro volantini (Bennet, Lidl, MD, Eurospin) e il
prezzo più conveniente sarà cambiato in diverse categorie. Nessun dato è
sbagliato — la pagina dei prezzi era ed è corretta — solo il diario di quel
giorno è muto. **Non ho tolto `stato.json` dal `.gitignore`**: è scritto
apposta («le fotografie no, le differenze sì»), e cambiarlo da solo senza
chiederlo sarebbe rifare la stessa cosa che ha già sbagliato altre volte questo
progetto — decidere per lui una cosa che lui aveva scelto di proposito. Se le
sessioni automatiche continuano a scrivere sul repo più volte al giorno da
cloni diversi, prima o poi va deciso con Manlio come far arrivare `stato.json`
da una sessione alla successiva (committarlo comunque? un artifact a parte?
accettare che ogni tanto un giorno resti muto?).

E `quanto()` conta anche i cambi di padrone, non solo le offerte che si
muovono: il più conveniente può cambiare **senza che nessuna offerta cambi**,
semplicemente perché quella di ieri è scaduta stanotte. Senza contarlo, il
giorno in cui scade il volantino dell'Eurospin il diario direbbe «niente di
nuovo».

**Una pagina vuota non si può giudicare.** Il diario è partito oggi, quindi non
c'era niente da mostrare: per guardarla davvero le ho costruito un diario finto
con offerte vere — un volantino che arriva, due prezzi che si muovono, un
capovolgimento — e poi l'ho cancellato.

## L'elenco è in ordine di prezzo e basta

Dal 2026-09-05. Prima le offerte dei volantini **non ancora cominciati**
venivano spinte in fondo all'elenco, qualunque prezzo avessero: l'idea era che
un prezzo che oggi non ti fanno non deve stare in cima. Manlio l'ha guardato e
ha detto il contrario: «quando si aggiungono nuove cose vanno in fondo anche se
hanno un prezzo più basso, dovrebbero proprio essere in ordine di prezzo».

Ha ragione, e la ragione è che **un elenco ordinato per prezzo che in fondo non
lo è più non è un elenco ordinato**: chi lo legge non sa più se sta guardando i
prezzi o le date, e il prezzo più basso finisce dove nessuno guarda.

**Quello che non si è perso.** La data non stava nell'ordine, stava nel bollo
rosso «vale dal ...», e quello è rimasto. Si è spostato solo *dove* è scritta
l'informazione, non se c'è.

**Il bollo verde ha cambiato significato, e andava fatto.** «Il meno caro» era
la prima riga; adesso è **il meno caro fra quelli che valgono oggi**, che con
l'ordine nuovo può non essere la prima. Senza questa modifica il verde sarebbe
finito su un prezzo che in cassa non fanno ancora — l'errore peggiore che
questa pagina possa fare — oppure su nessuno. `menoCaroOggi()` in `pagina.py`.

`prova-quando.js` prima *pretendeva* la vecchia regola, quindi è stata riscritta
insieme al codice: adesso controlla che l'elenco sia in ordine crescente senza
eccezioni e che il bollo verde stia sull'offerta giusta. Si lancia anche
fingendo un altro giorno (`node prova-quando.js out/sito.html 2026-09-11`), ed è
così che si vede che la regola tiene anche quando i volantini futuri diventano
presenti.

## Il foglio da correggere a penna

`python3 -m stampa` fa `out/catalogo.pdf`: le 66 voci del catalogo con le
parole che il computer cerca nei volantini, una casella da spuntare a sinistra
e, a destra, quante offerte ha oggi quella voce. Chiesto da Manlio il
2026-09-05: «sai gli umani servono ancora a qualcosa».

**Ha ragione, ed è l'unico controllo che una macchina non può fare.** Se manca
la parola «bovino», la carne di bue in offerta non si trova — e nessuna prova
automatica se ne accorge, perché non è un guasto: è una parola che non c'è. Lo
può giudicare solo chi in quei negozi ci va.

**La colonna dei numeri serve a leggere il foglio.** Uno zero non è un errore:
o quella voce questa settimana non è in offerta da nessuna parte, o le parole
sono sbagliate. Chi corregge distingue i due casi, io no.

La prima volta l'avevo fatto con uno script buttato via dopo l'uso, e alla
richiesta dopo non c'era più. Adesso è uno strumento come gli altri e **va
rilanciato a ogni modifica del catalogo**, se no il foglio stampato racconta un
catalogo che non esiste più.

Il PDF sta anche **committato nel progetto** come `catalogo.pdf`, quindi ha un
indirizzo pubblico: `https://manliograndi-del.github.io/spesa/catalogo.pdf`.
Serve perché Manlio non usa il terminale: un file in una cartella temporanea,
per lui, non esiste. Va ricommittato quando cambia.

## Il pesce, e la terza volta che il buco era mio

Il 2026-09-05 Manlio: «continuo a notare una poca quantità di offerte di
merluzzo e di gamberi». Gamberi **zero**, merluzzo **due**, con sette volantini
in casa. Era di nuovo un buco mio, il terzo dopo le pizze e Mercatò.

**Dove stava.** Non avevo mai aperto la pagina 3 del Bennet — una pescheria
intera, sottocosto — né la pagina «Pesce» del Carrefour. Non erano pagine
difficili: erano pagine che non avevo guardato. Adesso gamberi 5, merluzzo 9,
bastoncini 3, calamari e seppie 4, e per strada sono venuti fuori altri 40
prezzi (surgelati, yogurt, gelati) sulle stesse pagine.

**Come si trovano le pagine giuste senza riscaricare tutto.** `indice.json` ha
già le parole di ogni pagina di ogni volantino, anche quando le immagini non
sono più sul disco. Si interroga quello per sapere *quali* pagine parlano di
una certa cosa, e si riscaricano solo quelle. Sette pagine invece di
trecentotrentadue.

**La regola, ormai confermata tre volte:** *una categoria con zero o una sola
offerta è quasi sempre un buco mio, non il mondo.* Tutti i supermercati
vendono pesce. Se non lo trovo, non ho guardato.

### Niente righe doppie

Rileggendo i volantini per il pesce ho riscritto da capo dieci prodotti del
Carrefour che avevo già letto in una sessione precedente. **I prezzi
combaciavano tutti** — la rilettura confermava la prima, il che è di per sé una
buona notizia sul metodo — ma nell'elenco la stessa offerta compariva due
volte, e chi guarda pensa che siano due negozi.

Adesso `dati.py` si ferma da solo se due righe hanno stessa insegna, stesso
prodotto e stesso formato. Provato piantandone uno finto. Il confronto non è
sulla riga intera apposta: due righe che dicono la stessa cosa con una nota
diversa restano un doppione.

### Quello che il catalogo non sa ancora dire

Sulle stesse pagine ci sono offerte vere che **non hanno una casa**: orata,
branzino, polpo, vongole, pesce spada, trota, cefalo, scampi. Il catalogo ha
Gamberi, Merluzzo e baccalà, Calamari e seppie, Salmone, Tonno, Bastoncini —
e basta. Non le ho messe da nessuna parte a forza: infilare l'orata dentro
«Merluzzo e baccalà» vorrebbe dire che il confronto non vuol più dire niente.
Serve una voce nuova (**Pesce fresco**, o due: pesce azzurro e pesce bianco) e
la decisione è di Manlio, che ha il catalogo stampato in mano.

## Perché certe cose non le guardo — misurato, non intuito

Il 2026-09-05 Manlio, dopo il terzo buco trovato da lui: «cosa sta succedendo,
alcune cose non le guardi perché». Il numero non l'avevo mai calcolato:

**79 pagine lette su 332. Il 23%.**

**Il difetto è nel metodo, non nella fatica.** Fino a oggi aprivo una pagina
solo se una PAROLA me la faceva trovare: cercavo «pizza» nell'indice OCR e
leggevo le pagine che rispondevano. Così si trova **solo quello che si è già
pensato di cercare** — e per definizione non si trova mai quello a cui non si
è pensato. Pizze, Mercatò e pesce sono lo stesso errore tre volte, e nessuno
dei tre era difficile: erano tutti dietro una pagina che non avevo aperto.

Peggio: l'OCR legge male le scritte grandi, quindi anche la ricerca per parola
salta pagine che *parlano* di quel prodotto. Due filtri in fila, e passa poco.

**`python3 -m lette`** adesso dice la percentuale per volantino, e
`python3 -m lette <chiave>` elenca i numeri delle pagine mai lette. Non è una
prova che fallisce, è un promemoria: il 100% non è l'obiettivo (ci sono pagine
di pentole e di quaderni), ma serve a non credere di aver guardato tutto quando
si è guardato un quarto. Conta «letta» una pagina che ha almeno un prezzo:
sbaglia per difetto, ed è la parte giusta da cui sbagliare.

**La cura vera è leggere i volantini per intero, pagina per pagina, invece di
interrogarli.** Mercatò oggi è al 66% perché è l'unico letto così.

## Le pagine da lasciar perdere

Regola di Manlio, 2026-09-05, subito dopo aver visto che leggo un quarto delle
pagine: «una volta che hai visto una pagina piena di quaderni o di pubblicità o
di offerte che danno solo punti premio, lasciala perdere».

`strumenti/scartate.py` tiene l'elenco delle pagine **guardate e scartate**, col
motivo scritto per esteso. `lette.py` le conta come fatte, così spariscono
dalle cose da fare e non le riapro il mese prossimo. Prima una pagina di pentole
restava per sempre nell'elenco del lavoro da fare, indistinguibile da una mai
aperta.

**La riga che non si può oltrepassare:** si scarta solo dopo aver **aperto** la
pagina. Mai dal titolo, mai dall'OCR. È esattamente saltando pagine senza
guardarle che mi sono perso la pescheria del Bennet, che dall'OCR sembrava una
pagina qualunque.

E il motivo va scritto: «pentole, pile, calze» serve fra un mese a capire se lo
scarto era giusto; «niente» non serve a nessuno.

### Mercatò è il primo volantino finito: 36 pagine su 36

Le sei pagine saltate dal primo giro erano birra, vino, merendine, sapone,
dentifricio — **cinque categorie che per Mercatò risultavano vuote** — più sei
pagine davvero da buttare (cartoleria, raccolta punti FILA, pentole).

Il totale è passato dal 23% al 27%. Sembra poco, ma è tutto concentrato dove
serve: il negozio dove Manlio va quasi tutti i giorni adesso è completo, e da
lì sono usciti 62 prezzi nuovi e cinque nuovi primati.

**L'ordine giusto in cui leggerli è per scadenza, non per grandezza.** Avevo
cominciato dall'Ipercoop Extra perché era il più trascurato (8% di 57 pagine),
e scade il 9 settembre: cinquantadue pagine per quattro giorni di validità.
Prima i volantini che durano.

## «Volevo dire al Mercatò»

Il 2026-09-05, dopo che avevo cercato il pesce dappertutto: Manlio chiedeva
poco merluzzo e pochi gamberi **da Mercatò**, non in generale. Con le 36 pagine
tutte lette la risposta è certa, e stavolta **il buco non è mio**: in quel
volantino il pesce sono nove offerte su tre pagine — sei tonni in scatola, due
salmoni, un merluzzo — e gamberi zero. **Mercatò non mette il banco pescheria
sul volantino**: ha macelleria (p. 22), salumi (21) e formaggi (20), pescheria
no. I gamberi a 11,90 e l'orata a 8,90 vengono dal Bennet e dal Carrefour, che
il banco ce l'hanno.

Vale la pena scriverlo perché è il primo caso in cui «poche offerte» era vero.
Quello che ha reso possibile dirlo con certezza è aver letto il volantino
intero: prima non avrei potuto distinguere «non c'è» da «non l'ho guardato».

### La voce «Pesce fresco»

Scelta da Manlio fra quattro proposte. Ci stanno orata, branzino, sgombro,
verdesca, trota, cefalo, polpo, vongole, scampi, spada: venti offerte che
**vedevo e lasciavo fuori** perché non avevano dove stare. Nelle parole della
voce **non c'è «pesce»**: è in mezzo mondo (bastoncini di pesce, sugo di pesce,
zuppa di pesce) e tirerebbe dentro pagine che non c'entrano. Meglio i nomi
delle bestie.

### Le date di un'offerta si scrivono solo se diverse da quelle del volantino

Guasto introdotto e trovato lo stesso giorno. Sulle righe dell'Eurospin nuovo
avevo ricopiato a mano le date del volantino che le contiene. Sembra innocuo:
non lo è. La pagina legge «ha date sue» come **offerta ristretta**, e
un'offerta ristretta non ancora cominciata **non si mostra affatto** — regola
giusta, che serve a non mandare Manlio a chiedere un prezzo valido tre giorni.

Risultato: **22 righe invisibili**, fra cui i gamberi e i bastoncini di
merluzzo appena aggiunti per rispondere a lui. Nessuna prova falliva, perché
per il programma erano offerte legittime nascoste apposta.

Adesso `dati.py` si ferma se una riga ripete le date del suo volantino.
Provato piantandone una. Le date sulla riga restano per il caso vero: la pagina
«Weekend più uno» dell'MD, valida dal 18 al 21 dentro un volantino che va
dall'8 al 20.

## Il Carrefour: l'elenco dei negozi spaventa, ma le offerte a Torino ci sono

Il 2026-09-07, leggendo il volantino Carrefour per intero, sull'ultima pagina ho
trovato l'elenco degli ipermercati in cui le offerte valgono:

    ASSAGO, CARUGATE, GALLARATE V.LE MILANO 163, GALLARATE MALPENSA, LIMBIATE,
    PADERNO DUGNANO, PAVIA, GIUSSANO, DOMODOSSOLA, NOVARA GIULIO CESARE,
    GAVIRATE, TAVERNERIO, LUINO, UDINE.

Torino non c'è, e il piè di pagina delle pagine non alimentari sembra dirlo
dall'altro verso: «SOLO I PRODOTTI NON ALIMENTARI CONTRASSEGNATI CON QUESTO
SIMBOLO SONO DISPONIBILI ANCHE NEI PUNTI VENDITA PIÙ PICCOLI», e lì Torino c'è.
Ho concluso che a Torino valesse solo il non alimentare, ho lasciato i prezzi e
ho messo un avviso in fondo alla pagina.

**Manlio ha detto che è sbagliato**, lo stesso giorno: «le offerte ci sono a
Torino e valgono davvero». Lui in quei negozi ci va e alla cassa ci paga; io
avevo solo la lettura di un elenco stampato. **L'avviso è stato tolto.**

**Non rimetterlo.** Chi rilegge quel volantino ritroverà lo stesso elenco e
farà lo stesso ragionamento: è scritto qui apposta perché si fermi prima. Se
un domani si volesse riaprire la questione, non si riapre leggendo meglio la
pagina — si chiede a lui, che è l'unico che può sapere cosa gli fanno pagare.

La regola generale, che vale oltre questo caso: **su cosa succede davvero in
negozio, l'ultima parola è di chi ci entra.** Io posso leggere il volantino;
lui ci fa la spesa. Dove le due cose non combaciano, vince lui, e quello che
resta da fare è scriverlo qui.

Quello che invece **resta vero e utile** di quella lettura è la data: vedi
sotto.

## Il Carrefour scadeva il 13, non il 17

Stessa lettura, stesso giorno. `dati.py` diceva `2026-09-17` con scritto «fine
stimata» nel periodo: la copertina dice **«DAL 4 AL 13 SETTEMBRE»**. La stima
teneva in vita le offerte quattro giorni oltre la fine, e il 14 settembre la
pagina avrebbe dato per buoni prezzi finiti — proprio la cosa che il giudizio
lasciato al browser serve a evitare. Adesso è la data vera.

Il volantino ha anche una pagina «96 ORE (S)CONTATE» valida solo dal 10 al 13:
è il secondo caso di offerta ristretta dopo il «Weekend più uno» dell'MD, e si
scrive allo stesso modo, coi due campi in fondo alla riga.

## La prova che non provava più niente

`prova-maiuscole.js` aveva incollato dentro il percorso assoluto della cartella
di lavoro della sessione che l'aveva scritta. Quella cartella se n'è andata con
la sessione, quindi da allora l'**ultimo passo di `prove.sh` moriva sempre** con
un ENOENT — e `prove.sh` è il comando che decide se si pubblica. Adesso il file
si passa da fuori come in tutte le altre prove, e `prove.sh` glielo passa.
L'indirizzo finto dentro la prova puntava ancora a `/palestra/spesa/`, che non
esiste dal 2026-09-04: corretto anche quello.

Regola che ne esce: **niente percorsi della cartella di lavoro dentro gli
strumenti.** Vive quanto la sessione, e muore in silenzio.

## Il controllo giornaliero guardava solo le scadenze, non gli arrivi

Il 2026-09-09 Manlio ha chiesto come stessero andando gli aggiornamenti
automatici. Guardando invece di ricordare:

- la Routine c'e, e attiva, e parte tutte le mattine verso le 04:07 UTC;
- l'ultima partenza (9 settembre) e durata **quattro minuti**, 117.000 gettoni,
  0,88 dollari, su Sonnet, e il sistema la segna «riuscita»;
- in `registro.txt` l'ultima riga e del **5 settembre**, e l'ultimo commit sul
  progetto e quello fatto a mano il 7. Quel giorno c'era da fare: due volantini
  scaduti da tre giorni e tre in scadenza.

«Riuscita» vuol dire che la sessione e partita e si e chiusa, **non** che il
lavoro sia stato fatto. E il prompt le dice che la primissima cosa da scrivere
nel registro, appena clonato, e «clonato»: quella riga non c'e. Quindi non si e
fermata alla fine, si e fermata vicino all'inizio. Piu di cosi non si sa: una
sessione partita dal timer non lascia niente che si possa riaprire da qui.

**Il buco di progettazione, invece, si vede ed e grosso.** `pulisci.py` risponde
a una domanda sola: «di quello che ho gia, cosa scade?». Non chiede mai «e uscito
qualcosa di nuovo?». Cosi il volantino Bennet «Dolce Buongiorno» del 3 settembre
e rimasto fuori per sei giorni: il Bennet vecchio era ancora valido, quindi per
`pulisci` non c'era niente da fare, e nessuno e andato a guardare. L'ho trovato
il 9 settembre cercando il *sostituto* del Bennet in scadenza.

**Le insegne pubblicano volantini che si sovrappongono.** Bennet ne aveva due
insieme: quello generale (27 agosto-9 settembre) e questo a tema colazione
(3-16 settembre). Non e un caso raro ed e esattamente quello che la domanda
«cosa scade?» non puo vedere.

### Perche a mano riesce e da sola no

Manlio: «se l'aggiornamento lo sai fare manuale perche non dovresti farlo anche
automatico». La domanda e giusta e la risposta non e «e difficile»:

1. **La misura del lavoro.** Leggere un volantino intero vuol dire aprire 36
   immagini una per una e scriverne i prezzi a mano: qui, oggi, sono state ore e
   centinaia di migliaia di gettoni. Quattro minuti non sono «poco tempo», sono
   un altro ordine di grandezza.
2. **Il costo di partenza.** Prima di poter cominciare, la sessione automatica
   deve leggere CLAUDE.md e NOTE.md (millequattrocento righe fra i due), clonare,
   installare jsdom e tesseract. E la partenza a freddo di ogni singolo giorno.
3. **Nessuno la guarda.** Qui, quando mi fermo, Manlio mi rimette in riga. Li non
   c'e nessuno, e il prompt le concede una via d'uscita legittima («se non c'e
   niente da fare, fermati e non scrivere a nessuno») che da fuori e
   indistinguibile dall'essersi arresa.

**La conseguenza pratica, e la cosa da non dimenticare:** finche il giro
automatico non lo si vede arrivare in fondo almeno una volta, **vale come
tentativo, non come garanzia**, e i volantini nuovi si mettono a mano. Era gia
scritto qui il 5 settembre e resta vero.

La strada che ha senso non e chiedergli di fare tutto: e **spezzarlo in due**.
Accorgersi che e uscito un volantino nuovo costa minuti e lo puo fare da sola;
leggerlo pagina per pagina costa ore e conviene farlo in una sessione dove
Manlio c'e. Meglio una sveglia che dice «e uscito il Bennet nuovo, dimmi quando»
che una che promette tutto e tace.

## La pulizia dei volantini vecchi: dove si accumulano davvero

Manlio, 2026-09-09: «anche se non li vedo piu e importante fare pulizia dei
volantini vecchi altrimenti in poco tempo avremo una montagna di volantini».
Ha ragione, e vale la pena scrivere **dove** cresce la montagna, perche non e
dove sembra.

Non nei PDF e nelle immagini: quelli vivono nella cartella di lavoro della
sessione e spariscono da soli. Cresce in tre posti dentro il progetto:

- le righe in `VOLANTINI` e i loro prezzi in `PRODOTTI` dentro `dati.py`;
- le pagine in **`indice.json`**, che e il file grosso: le 55 pagine di Eurospin
  e MD tolte il 9 settembre erano un sesto dell'archivio;
- le pagine in `scartate.py`, che valgono solo per quel volantino.

`indice.py` la pulizia la fa gia da solo (`righe = [r for r in righe if
r['chiave'] in META]`): basta togliere il volantino da `dati.py` e rilanciarlo.
Gli altri due si tolgono a mano, ed e la parte che si dimentica.

## Il giro automatico ce l'ha fatta — e le due cose che glielo impedivano

**Il 2026-09-10 il controllo giornaliero e arrivato in fondo da solo, per la
prima volta.** In un'ora: letti per intero quattro volantini (Bennet nuovo 35
pagine, Lidl nuovo 58, MD 35, Eurospin 22 — centocinquanta pagine), buttati
Bennet e Ipercoop scaduti con le loro 115 righe di prezzo, sito e catalogo
pubblicati, prove passate, CLAUDE.md e NOTE.md aggiornati. Ha perfino unito da
sola un commit che un'altra sessione aveva spinto nel frattempo. I prezzi sono
passati da 937 a 1171.

**Cosa gli mancava davvero: il progetto.** Fino al 9 settembre la sessione della
sveglia nasceva vuota e doveva chiedere lei la repository con `add_repo`; quel
9 settembre e fallita proprio li e l'ha scritto a Manlio. Il 10 Manlio ha
**attaccato `manliograndi-del/spesa` alla Routine** (nella configurazione
dell'ambiente, non nel prompt), e da quel momento la sessione parte col clone
gia in mano. Era quello il muro, non il modello ne il tempo.

**La seconda trappola: l'ora della sveglia.** Il 12 settembre e partita alle
04:06 UTC ed e morta in **otto secondi** con «You've hit your weekly limit ·
resets 5am (UTC)». Il limite settimanale si azzera alle 05:00 UTC: la sveglia
suonava **54 minuti prima**, cioe nel minuto peggiore possibile della settimana.
Anche l'11 settembre era andata cosi (ha scritto «clonato» e si e fermata).
Spostata a **06:06 UTC**, dopo l'azzeramento. Se un domani la si rimette
all'alba, si ricasca: il tetto e settimanale e finisce sempre di notte.

**La morale, che vale oltre questo progetto:** per tre giorni ho cercato la
causa nel posto sbagliato — il modello, il tempo, la dimensione del lavoro —
mentre erano due cose di configurazione, entrambe fuori dal codice e
invisibili da dentro. Il registro non ha risolto niente da solo, ma e servito
esattamente a questo: senza quelle righe con l'ora non avrei potuto distinguere
«si e arresa» da «non e mai partita».

**Cosa resta vero:** un giro che legge 150 pagine costa un'ora di lavoro e una
fetta seria del budget settimanale. Non si puo fare tutti i giorni. Il caso
normale deve restare «niente da fare, mi fermo».

## La rete

**Serve l'accesso di rete aperto.** Con l'impostazione predefinita (*Trusted*)
tutti i siti dei supermercati e tutti i portali di volantini rispondono
`EGRESS_BLOCKED`, Wikipedia compresa: passa solo la ricerca web, che gira
sull'infrastruttura di Anthropic. Manlio l'ha messa su **Full** quel giorno:
claude.ai/code → icona a nuvola sopra la casella del messaggio → ingranaggio
sull'ambiente → *Network access* → Full. **Vale dalla sessione dopo, non su
quella in corso.**

## Come si rifà

Gli strumenti sono in `strumenti/`. Serve
`apt-get install -y tesseract-ocr tesseract-ocr-ita`. Si lavora in una cartella
qualsiasi, con `strumenti/` nel `PYTHONPATH`:

    export PYTHONPATH=<progetto>/strumenti
    python3 -m scarica <chiave>     # pagine del volantino, indirizzi da dati.py
    bash <progetto>/strumenti/leggi.sh   # OCR di ogni pagina scaricata
    python3 -m indice               # aggiorna indice.json DENTRO il progetto
    python3 -m pagina               # le tre copie in out/
    python3 -m storia               # il diario delle novità del giorno
    bash <progetto>/strumenti/prove.sh   # TUTTE le prove, si ferma alla prima che fallisce
    python3 -m pulizia out/sito.html     # cerca il codice rimasto in giro

**`prove.sh` è il comando che conta**: le prove singole si lanciano da sole solo
per capire un guasto. Serve `npm install` **dentro il progetto**, perché node
cerca `node_modules` accanto allo script e non accanto alla cartella di lavoro.

**A ogni volantino nuovo si tocca solo `dati.py`**: la riga in `VOLANTINI` (con
l'ultimo giorno e l'indirizzo delle pagine) e le righe dei prezzi in `PRODOTTI`,
lette a occhio dalle pagine. `scarica.py` e `indice.py` leggono le date da lì, e
la data in fondo alla pagina la calcola `pagina.py` da sola.

`pdf.py` fa un PDF per volantino, se serve guardarlo tutto intero. **Non si
committa**: le pagine non sono nostre.

Le pagine stanno su `anteprimavolantino.it/public/uploads/AAAA/MM/` col nome
`volantino-<insegna>-<AAAA-MM-GG>-p-<NN>.jpg`. **Il numero di pagina ha 2 cifre
per certi volantini e 5 per altri**, senza una logica: si guarda l'articolo
dell'insegna e si copia il nome della prima pagina.

## Trappole trovate provando

- **LibreOffice non funziona qui**: `soffice` parte ma dà "source file could not
  be loaded" su qualsiasi file, quindi `recalc.py` della skill xlsx va sempre in
  timeout. openpyxl scrive le formule senza il valore calcolato, e certi lettori
  (soprattutto da telefono) mostrerebbero la colonna del prezzo al chilo vuota.
  `cache_vals.py` infila il valore dentro l'XML accanto alla formula: si tengono
  tutti e due. **Va rilanciato ogni volta che si risalva il file con openpyxl**,
  perché il salvataggio butta via i valori.
- **`xargs -P` non funziona** su questa macchina per l'OCR: gira per nove minuti
  e produce file da zero byte. In sequenza fa 1,3 s a pagina e va benissimo.
  Per i download invece `xargs -P 12` va (sono in attesa di rete, non di CPU).
- **Il browser non passa dal proxy**: Chromium dà `ERR_CONNECTION_RESET` su
  qualsiasi HTTPS perché non c'è `certutil` per mettergli il certificato nello
  store NSS. Con `curl` va tutto. Non perderci tempo.
- **Bennet risponde 403 a curl** sul proprio sito (protezione anti-robot). Le
  sue pagine si prendono lo stesso da anteprimavolantino.
- **Nel codice Python non si scrive `all''olio`**: non è una stringa SQL, Python
  concatena e viene fuori `allolio`. Usare le virgolette doppie.

## Perché i riassunti online non bastano

Provati prima di scaricare i volantini, e **sbagliano**. Tre errori trovati
confrontandoli con la pagina vera:

- Lidl, rollata di bovino: scritto «7,99 al kg», in realtà 7,99 la confezione da
  600 g, cioè **13,32 al kg**
- Lidl, salmone: scritto «150 g a 8,99», in realtà **500 g** a 8,99
- Eurospin, macinato di bovino: scritto «6,99 al kg», sul volantino **8,99**

Le righe che nell'Excel restano di seconda mano sono segnate in giallo e dicono
"DA CONTROLLARE". Tutte le altre le ho lette una per una dalle pagine.

## Il Carrefour Iper del 15 settembre: «Grandi Marche», come Bennet il 10/9

Il 2026-09-14 la Routine ha trovato il nuovo Carrefour Iper (dal 15 al 28
settembre, 50 pagine) alla terza mattina di ricerca — il 12 e il 13 non era
ancora uscito. Letto per intero: come il Bennet generale del 10 settembre, il
tema di copertina («Grandi Marche», sconti fino al 50% su intere linee di
marca) copre le prime 11 pagine senza mai stampare un prezzo di base, quindi
sono scartate. I prezzi veri stanno nelle pagine di reparto — Carne (12),
Pesce (13), Ortofrutta (14), Salumi e formaggi (15-16), Freschi del banco
frigo (17-19) — più qualcosa sparso in Colazione (21), Alimentari confezionati
(22-24) e Bevande (25-26, 29). 46 righe nuove in `dati.py`.

**L'ultima pagina elenca di nuovo gli ipermercati dove valgono le offerte, e
Torino non c'è** (Assago, Carugate, Gallarate, Limbiate, Paderno Dugnano,
Pavia, Giussano, Domodossola, Novara, Gavirate, Tavernerio, Udine). È lo stesso
elenco già visto il 2026-09-07 sul volantino precedente: Manlio ha detto allora
che è sbagliato dedurne che le offerte non valgano a Torino, quindi questa
volta non è stato rimesso nessun avviso e non gliel'ho richiesto. Se un domani
la lista dovesse davvero cambiare qualcosa, lo dirà lui.

Il resto del volantino (pagine 27-28, 30-49) è aperitivi, cura persona, cura
casa, casalinghi, elettronica, abbigliamento ed elettrodomestici: guardato pagina
per pagina e scartato, coi motivi in `scartate.py`.

## Il Lidl «XXL» ha prodotti veri, non solo confezioni grandi (2026-09-15)

Il volantino Lidl del 17-23 settembre aveva molte pagine intere marcate «XXL»
e «Super Offerte»: a un'occhiata sembrano solo confezioni maggiorate (Manlio
non le vuole, non è quello il punto), ma dentro c'erano prezzi veri di prodotti
normali — salmone, coppa di suino, tonno, vino, formaggio — venduti in formato
grande a un prezzo per chilo comunque competitivo. Non sono state scartate a
priori: si leggono come tutte le altre, prezzo e formato, e si giudica riga per
riga se il prezzo per unità è buono, non dal bollino «XXL» sulla confezione.

Lo stesso volantino aveva anche un blocco enorme di pagine non alimentari
(sport, bellezza, casa, giardino, moda, specialità orientali, fiori): quelle
sì scartate, coi motivi in `scartate.py` — sono il grosso delle 19 pagine
scartate su 36.

## Se un domani diventa un'app

Manlio non legge codice e verifica tutto aprendo una pagina sul telefono, quindi
il naturale seguito è una paginetta come la Palestra. **Il telefono non può
scaricarsi i volantini da solo**: i siti dei supermercati non concedono CORS e
servirebbe una libreria per i PDF che in negozio, senza rete, non si carica.
I dati vanno scritti qui dentro da Claude quando i volantini cambiano, e la
pagina si limita a mostrarli.

## «Cerca fra i prezzi» — 2026-09-15

Manlio: «C'è la possibilità di fare una casella cerca per trovare esattamente un
singolo prodotto fra tutte le offerte che c'hai». C'erano 1253 prezzi dentro la
pagina e l'unico modo di arrivare a uno era accendere la sua categoria e
scorrere.

**Non è la casella che c'era già.** Dentro il cassetto ce n'era una, ma cerca
nel **catalogo** — serve ad accendere le voci della lista, e trova «Carne di
bue», non «Hamburger di bovino – Aia da 400 g». Quella nuova cerca fra le
**offerte**: nome del prodotto, insegna, categoria, formato e note, tutte
parole insieme e in qualsiasi ordine («tonno rio» → 2 righe). Le parole di una
lettera sola non contano, se no la prima lettera battuta tirava su tutto.

Tre cose decise mentre la facevo, e il perché:

- **Nei risultati non c'è il bollino verde «il meno caro».** In un elenco
  qualsiasi il verde direbbe «il meno caro fra quelli che hai scritto», ma uno
  lo legge come «il meno caro della categoria» — e quello, in negozio, è
  mandare qualcuno a comprare la cosa sbagliata. Vale la regola di sempre: se
  il numero è ambiguo, non si mette. La prova `prova-cerca.js` conta i bollini
  verdi nei risultati e **pretende che siano zero**.
- **Il pannello sta fuori dalla `.barra`**, come il cassetto e per lo stesso
  motivo già pagato: la barra è `position:sticky` e farci crescere dentro un
  pannello lungo bloccava la pagina a ogni tocco. La prova lo verifica
  risalendo i genitori del pannello.
- **Cassetto e ricerca non stanno aperti insieme.** Sono due pannelli lunghi
  sotto la stessa barra: aperti insieme non si capiva più dove si era.

I risultati escono in ordine di prezzo unitario, raggruppati per categoria, 40
alla volta con «Mostra le altre N» — lo stesso passo dell'elenco normale.
Le offerte scadute o non ancora cominciate sono fuori, con lo stesso `nascosta()`
del resto della pagina: il giudizio lo dà sempre il browser di chi guarda.

Provato in jsdom su tutte e tre le copie: «mozzarella» 17 righe, «tonno rio» 2,
«barilla» 7, «nutella» 3, «zzz» e «a» nessuna con la frase che lo spiega.

### Il tasto, poche ore dopo

«Il pulsante ricerca è poco visibile, secondo me dovrebbe essere rosso o
comunque più visibile.» Aveva ragione: l'avevo fatto uguale a «+ altri
prodotti», tratteggiato e grigio, e in mezzo a tredici pastiglie di prodotti
non lo vedeva nessuno.

Rosso sì, ma **non in fila con le pastiglie**: lì dentro il rosso pieno
significa già «prodotto acceso», e un quattordicesimo bottone rosso in mezzo
agli altri si sarebbe letto come una voce della lista accesa per sbaglio. Sta
su **una riga tutta sua**, largo quanto lo schermo (`flex:0 0 100%`), rosso
pieno, 48 px di altezza. Lì il rosso torna a voler dire «premi qui».

Il bottone **conserva la classe `agg`** anche se non è più tratteggiato:
otto prove (`prova.js`, `prova-quando.js`, `prova-scorrimento.js`,
`prova-intestazione.js`, `prova-pagine.js`, `prova-collegamenti.js`,
`prova-arrivi.js`, `prova-maiuscole.js`) filtrano con
`!classList.contains('agg')` per tenere fuori i bottoni che non sono prodotti.
Togliendogliela, per un momento ce l'ho avuta tolta, il tasto «Cerca» è finito
in mezzo ai prodotti in tutte quante: passavano lo stesso, ma
`prova-quando.js` ci cliccava sopra come se fosse una categoria e
`prova-maiuscole.js` lo contava fra i nomi. Nessuna si è lamentata — è il tipo
di rottura silenziosa che questo progetto paga caro. Il rosso arriva da
`.tasto.trova`, scritta **dopo** `.tasto.agg` nel foglio di stile: stessa
specificità, vince l'ultima.

`prova-cerca.js` adesso pretende anche che il tasto sia rosso e su una riga
sua, leggendo il CSS della pagina: se qualcuno gli rimette il grigio, si ferma.

## Il diario era fermo al 9 settembre — 2026-09-15

Manlio ha aperto Novità e mi ha mandato la fotografia: «Ultimi 7 giorni»
mostrava **mercoledì 9 settembre**, e «Oggi» era vuoto. Sei giorni di niente,
mentre in quei sei giorni erano entrati un Bennet, due Lidl, un Carrefour Iper
e trecento prezzi.

**Il perché era già scritto qui e non era stato risolto.** `storia/stato.json`
— la fotografia di com'era ieri — è in `.gitignore` di proposito: «le
fotografie no, le differenze sì». Ma ogni sessione parte da un **clone
pulito**, quindi la fotografia non c'è mai, e `storia.py` rispondeva «prima
fotografia: da domani ci sarà qualcosa da confrontare». Domani non arrivava
mai: la sessione moriva, la fotografia con lei, e la notte dopo era di nuovo
«prima fotografia». Un ciclo che si autoconsumava, in silenzio, tutte le
notti.

**La soluzione non è salvare la fotografia: è non averne bisogno.** La
fotografia non è un dato, è una **lettura di `strumenti/dati.py`** — e
`dati.py` nel repository c'è, con tutta la sua storia. Se `stato.json` manca,
adesso `storia.py` chiede a git l'ultimo commit che ha toccato i prezzi, ne
tira fuori l'intera cartella `strumenti/` con `git archive`, e la legge in un
processo a parte. Serve tutta la cartella e non solo `dati.py`: `dati` importa
`catalogo` e `pagine_mercato`, e devono essere quelli di allora. A leggerli è
il `fotografia()` di **adesso**, caricato per percorso con `importlib` mentre
la cartella vecchia sta prima nel `sys.path`: le due fotografie vanno
confrontate fra loro, quindi devono avere la stessa forma, non quella che
aveva `storia.py` quel giorno.

**E i giorni in mezzo si riempiono uno per uno.** Prima il confronto era
sempre e solo «ieri contro oggi». Adesso, se fra la fotografia e oggi ci sono
dei giorni scoperti, per ognuno si riprende il `dati.py` in vigore *quel*
giorno e si scrive il suo file. Non è pignoleria: **un giorno può avere
novità vere senza che nessuno tocchi i prezzi.** A mezzanotte un volantino
scade e il più conveniente di una categoria diventa un altro — l'11 settembre
è esattamente questo, un giorno con una sola riga: i frollini dell'Eurospin
diventati i biscotti più convenienti perché quelli di prima erano scaduti.
Ammucchiando tutto sull'ultimo giorno, quella novità avrebbe avuto la data
sbagliata.

Recuperati così i giorni **10, 11, 13, 14 e 15 settembre** (il 12 non era
successo niente, e infatti non c'è il file). Nessun numero è inventato: sono
gli stessi conti di sempre, fatti sui `dati.py` veri di quei giorni presi da
git.

**Una conseguenza da ricordare:** `python3 -m storia` adesso va lanciato
**prima** di committare. Se si committa per primi, l'ultimo commit è già lo
stato nuovo e il confronto viene vuoto. Nell'ordine scritto in CLAUDE.md
(`pagina`, `storia`, `novita`, poi commit) è già così.

## Leggere un volantino intero vuol dire per TUTTO il catalogo, non solo per i bottoni accesi (2026-09-16)

Leggendo il Mercatò nuovo (17-30 settembre) mi sono fermato, a metà, alle
sole categorie che oggi sono accese sui bottoni di Manlio (dodici). Sbagliato:
il catalogo ne ha **67**, e la pagina stessa lo dice — «non tutte le voci del
catalogo hanno già i prezzi... le sto leggendo a mano, un reparto per volta:
compariranno senza che tu debba fare niente». Se mi fermo alle categorie
accese oggi, quando Manlio (o sua moglie) ne accende una nuova dal cassetto
la trova vuota anche se il volantino letto quel giorno aveva il prezzo giusto
sotto gli occhi. Rileggendo le stesse venti pagine col catalogo intero in
mano sono uscite altre trenta righe buone: salumi al banco (prosciutto,
salame, mortadella, pancetta — categorie loro, non «Formaggio»), pesce fresco,
vino, frutta e verdura di stagione, pasta, riso, farina, pane, caffè, e
qualche voce di cura casa e persona. **La domanda giusta, pagina per pagina,
non è «c'entra con un bottone acceso» ma «c'entra con una delle 67 voci».**

Dentro questo stesso errore, tre categorie sono state sbagliate al primo
giro perché assomigliano a «Formaggio» ma hanno una voce propria nel
catalogo: la ricotta va in **Ricotta**, il Grana Padano in **Grana e
parmigiano**, la mozzarella (bufala, fior di latte, ciliegine) in
**Mozzarella**, la robiola e il Philadelphia in **Formaggi spalmabili**. La
regola: prima di scrivere la categoria, si guarda `catalogo.py` per le parole
chiave — «formaggio» da solo prende solo quello che non ha una casa più
precisa.

**Lo stesso prodotto può comparire identico in due volantini consecutivi
dello stesso negozio**, quando il fornitore ripete la stessa referenza da un
periodo all'altro: qui è successo con una pancetta Cavalier Umberto Boschi,
scritta uguale (stessa insegna, stesso prodotto, stesso formato) nel Mercatò
3-16 e nel Mercatò 17-30, solo col prezzo cambiato. Il controllo delle righe
doppie di `dati.py` **non guarda la chiave del volantino**, quindi si è
fermato subito con «riga doppia», anche se i due volantini non si
sovrappongono nel tempo. Giusto così: tenuta solo la riga nuova (il prezzo di
adesso), tolta quella vecchia — due righe uguali per lo stesso prodotto
reale, anche a distanza di volantini, confonderebbero comunque chi guarda.

### Rilanciare `storia` due volte nello stesso giorno — 2026-09-16

Il giro automatico di stamattina ha trovato un difetto nel recupero scritto
ieri, e l'ha trovato usandolo. Aveva lanciato `python3 -m storia`, poi aveva
aggiunto altre righe a `dati.py` e l'aveva rilanciato: **il secondo giro si era
confrontato con la fotografia che aveva scritto il primo**, cioè con se stesso,
e il file del giorno era rimasto con le ultime cinque righe invece che con
tutta la giornata. Se n'è accorto e ha riscritto il file a mano — ma il difetto
era nel codice, non nel file, e sarebbe tornato la volta dopo.

Adesso, se la fotografia porta già la data di oggi, il paragone non è più con
lei: si riprende dall'**ultimo commit di un giorno precedente**. Il metro giusto
è sempre «l'ultimo giorno pubblicato», e quello sta in git. Provato lanciandolo
tre volte di fila: riscrive tre volte lo stesso giorno, intero e identico.

Nota di contorno: nello stesso passaggio sono state rimesse a posto quattro
righe di commento dove erano rimaste in chiaro delle sequenze `è` invece
delle lettere accentate. Nelle stringhe funzionavano, nei commenti erano solo
sporcizia da leggere.

### «Pubblicato» che non arriva: due sessioni avevano spinto sul ramo sbagliato — 2026-09-17

Il sito pubblico legge da `origin/main`. Il registro del 15 e del 16
settembre diceva «pubblicato: ... verificato online», e l'Artifact era stato
davvero ripubblicato — ma il `git push` di quelle due sessioni era andato su
un ramo con un altro nome (uno di quelli che l'ambiente di lavoro assegna
automaticamente a ogni sessione), non su `main`. Il sito è rimasto fermo a
`sw.js` v27 per giorni, senza il Mercatò 17-30, il Carrefour Iper, il Bennet
e il Lidl, mentre il registro raccontava tutto come riuscito. Scoperto solo
il 17 settembre confrontando `git log origin/main` con quello del ramo di
lavoro: 36 commit di differenza, tutti solo da un lato — un fast-forward
pulito, nessun lavoro perso, ma **36 commit che il sito non aveva mai visto**.

Sistemato spingendo quel ramo su `main` (fast-forward, senza perdere storia)
e controllando `sw.js` sul sito online per essere sicuri che il numero di
cache corrispondesse.

La lezione non è di codice, è di controllo: **scrivere «pubblicato» nel
registro senza aver verificato che il push sia arrivato su `main` non è una
verifica, è una speranza.** Il passo 7 dice già di controllare l'indirizzo
pubblico dopo aver pubblicato — farlo davvero, guardando un numero che cambia
a ogni rilascio (`sw.js`, o un prodotto nuovo nella pagina), non solo
guardare che il comando `git push` non abbia dato errore: un push può
riuscire perfettamente e andare comunque nel posto sbagliato.

## I due tasti su ogni volantino — 2026-09-18

Manlio: «visto che alla fine c'è l'elenco dei supermercati, ci fosse anche un
tasto, anzi due tasti: uno per vedere le offerte, l'altro per vedere il
volantino. Immagino che sarebbe migliore per la navigazione che si aprissero in
pagine nuove».

L'elenco in fondo c'era dal principio, ma era **roba da leggere e basta**:
insegna, periodo, quante pagine. Le offerte di quel volantino erano dentro la
pagina — sparse fra i bottoni dei prodotti — e per vederle tutte insieme non
c'era modo. Il volantino vero si apriva solo partendo da una riga di prezzo
(«Apri la pagina 12 del volantino»): chi non aveva un prezzo davanti non aveva
nessuna porta.

Adesso ogni riga ha due tasti, larghi uguali:

- **«Le offerte (N)»** — le offerte lette da quel volantino, divise per
  reparto, dalla meno cara in giù dentro ognuno.
- **«Il volantino ↗»** — la prima pagina del volantino sul sito di chi lo
  pubblica. **L'indirizzo si prende da `indice.json`**, cioè da pagine che
  esistono davvero, non dal modello con dentro il numero: così il tasto non
  può portare su un indirizzo inventato.

Le scelte fatte mentre lo facevo, e il perché:

- **Riusa il pannello della ricerca, non ne apre uno nuovo.** Quel pannello sta
  già **fuori dalla `.barra`** (dentro, la barra `sticky` cresce e il telefono
  si pianta a ogni scorrimento: lezione del cassetto, pagata due volte) e le
  sue righe **non portano il bollino verde**. Qui il verde sarebbe una bugia
  ancora più diretta che nella ricerca: vorrebbe dire «il meno caro di questo
  negozio» e si leggerebbe «il meno caro di tutti». Il titolo del pannello dice
  sempre **quale** volantino si sta guardando — di Lidl ce ne sono due validi
  insieme, e di Bennet pure.
- **Il numero sul tasto è quello che vale OGGI**, contato dal browser di chi
  guarda con la sua data, come tutto il resto della pagina. Un volantino
  scaduto non ha un tasto: al suo posto c'è la scritta spenta «offerte
  scadute». Un tasto che promette 116 offerte e ne apre zero è peggio di
  nessun tasto.
- **La pagina nuova si apre con `#volantino=...` in coda all'indirizzo**, ed è
  la pagina stessa che, trovandosela, apre il pannello da sola e scorre fin lì.
  Niente pagine generate in più: una sola pagina che sa aprirsi in due modi.
  Chiudendo il pannello la coda sparisce dall'indirizzo, se no chi ricarica
  quella scheda se lo ritrova aperto.
- **Se la scheda nuova non si apre, il pannello si apre lì.** Dentro la copia
  di Claude la pagina vive in una cornice che a volte la scheda nuova non la
  lascia aprire: meglio un tasto che funziona in un modo un po' diverso di un
  tasto che non fa niente. Il tasto è un `<a>` con l'indirizzo vero, quindi
  «apri in una scheda nuova» col dito tenuto premuto funziona comunque.
- **Scrivendo nella casella si cerca DENTRO quel volantino**, non fuori: è la
  stessa casella, con un altro invito scritto sopra. Chiudendo, torna a cercare
  fra tutte le offerte.

La prova nuova è `prova-volantini.js`, e gira su tutte e tre le copie: controlla
che ogni riga abbia i suoi tasti, che «Il volantino» porti a uno dei tre siti
che i volantini li pubblicano davvero, che «Le offerte» apra **solo** quelle di
quel volantino (contate una per una), che siano in ordine dentro ogni reparto,
che non ci sia nessun bollino verde, che il pannello non finisca dentro la barra
e che lo stesso indirizzo con la coda, aperto da zero, faccia la stessa cosa.

## Ekom, insegna nuova — 2026-09-18

Manlio: «visto che ci sei aggiungi anche ekom». Otto insegne invece di sette.

**Niente trappola Mercatò, per fortuna.** A Torino gli Ekom sono una dozzina
(i più vicini a corso Siracusa: via Castelgomberto 127 e via Tripoli 79) ma il
volantino è **lo stesso per tutti**: l'unica versione diversa è quella della
Toscana, che si riconosce dal nome. Non c'è da scegliere il negozio come col
Mercatò di via Filadelfia.

**La fonte è kimbino**, la stessa del Mercatò, e ha lo stesso difetto: firma
ogni immagine con un codice calcolato sull'indirizzo, quindi lo schema con
`{n}` non esiste e le pagine vanno elencate una per una — `pagine_ekom.py`,
gemello di `pagine_mercato.py`. Anteprimavolantino l'Ekom non ce l'ha.

### Il «1+1», e perché le righe dicono «2 × 300 g»

Il volantino dell'8-21 settembre è un **1+1**: due pagine intere (2 e 3) dove
ogni prodotto porta scritto «1 PEZZO 3,99 €» e sotto «2 PEZZI 3,99 €». Il
secondo pezzo è gratis, e **il volantino stesso conta il prezzo al chilo su
due confezioni** (300 g a 3,99 diventano «AL KG 6,63 €», che è 600 g a 3,99).

La regola di casa dice: se un conto è ambiguo, si sceglie il numero che NON fa
sembrare l'offerta più conveniente di quello che è. Qui però non è ambiguo, è
**condizionato**: chi ne prende due quel prezzo lo paga davvero. Scrivere solo
il prezzo di una confezione avrebbe fatto sembrare l'Ekom più caro di quello
che è, che è l'errore uguale e contrario.

Quindi: **la riga dice nel formato che sono due** — «2 × 300 g (1+1)» — così il
prezzo per unità è vero per quello che si compra davvero, e **la nota dice
sempre quanto costa una confezione sola**, con il suo prezzo al chilo. Chi ne
vuole una paga il doppio al chilo e lo legge lì, prima di andare in negozio.
Niente bollino verde rubato con un numero che vale solo a metà.

### Cos'altro c'era dentro, e cosa è rimasto fuori

Letto per intero, 16 pagine, 138 prezzi. Scartate due pagine sole: la
copertina e il concorso a premi della carta EKOM UP (in `scartate.py`).

- **Pagina 13: offerte solo con la carta EKOM UP.** Trattate come le MD Buona
  Spesa Card: prezzo della tessera, e nella nota il prezzo pieno.
- **Pagina 9: banco salumi, formaggi e macelleria.** Il volantino avverte che
  valgono **solo nei punti vendita col banco servito** — sta scritto in ogni
  nota, perché un Ekom senza banco quel prosciutto non te lo taglia. I prezzi
  sono stampati all'etto: qui diventano al chilo (×10), come li confronta la
  pagina.
- **Lasciati fuori di proposito**: le fette biscottate (sotto «Biscotti»
  sarebbero il meno caro per forza, e non sono biscotti), i «salumi light» e
  «le insalate» senza grammatura (nessun prezzo per unità onesto), i piatti
  pronti, il Condisano Dante (non si capisce dall'immagine se è olio di semi o
  misto), la maionese, gli snack e il cibo per cani e gatti: nessuna categoria
  del catalogo li copre.
- **Nasello** messo sotto «Merluzzo e baccalà» con la nota «è nasello, non
  merluzzo», come si è sempre fatto con i quasi-uguali (l'hamburger misto
  suino/bovino sotto la carne di bue).

Il volantino **scade il 21 settembre**, tre giorni dopo averlo letto: si è
fatto lo stesso perché senza non ci sarebbe stata nessuna offerta Ekom, e il
successore (dal 22) esce fra pochi giorni. Su kimbino il successore non c'era
ancora il 18.

## La finestra «Cosa c'è di nuovo» — 2026-09-18

Manlio: «la prima volta che uno apre la pagina sarebbe carino che ci fosse una
finestra novità che elenca le novità che ci sono state, a partire dalla casella
di ricerca; naturalmente sono novità inerenti l'interfaccia e le possibilità,
non i prodotti».

**Sono due cose diverse, e la pagina adesso le tiene separate:**

- il tasto **«Novità»** in alto a destra porta al **diario dei prezzi**: cosa è
  cambiato nelle offerte, giorno per giorno. Invecchia da solo e si rifà a ogni
  giro;
- la **finestra** che si apre alla prima apertura racconta **cosa si può fare
  adesso che prima non si poteva**: la casella di ricerca, i due tasti sui
  volantini, un'insegna in più. Non ci vanno prezzi. La prova
  `prova-novita-pagina.js` **cerca il simbolo dell'euro dentro la finestra e
  pretende che non ci sia**: se un giorno qualcuno ci infila un'offerta, la
  finestra diventa un doppione del diario e comincia a mentire da sola quando
  quell'offerta scade.

L'elenco parte dalla casella di ricerca, come ha chiesto lui, ed è in ordine di
tempo: si legge come una storia di cosa è arrivato.

### Perché non si rivede più (e come farla tornare per una cosa sola)

Ogni novità ha un **id che comincia con la sua data** (`2026-09-15-cerca`).
Chiudendo, il browser di chi guarda si segna l'id dell'**ultima della lista**;
alla prossima apertura compaiono **solo quelle con l'id più grande**, cioè
quelle arrivate dopo. Così:

- chi apre per la prima volta le vede tutte;
- chi le ha già viste non vede più niente;
- chi torna dopo che ne è stata aggiunta una vede **solo quella nuova**.

Il confronto fra due date scritte in quel modo è un confronto fra due scritte:
niente elenchi da tenere, niente conti. **Le novità nuove si mettono in fondo**
a `NOVITA_PAGINA`, in `pagina.py`, con la data del giorno davanti all'id.

Se il browser non lascia leggere né scrivere (navigazione privata, memoria
piena) la finestra si comporta come per uno nuovo: si apre. Meglio una volta di
troppo che una pagina che si rompe, ed è la stessa regola della lista.

### Due dettagli che sembrano niente e non lo sono

- **Il fuoco sul tasto non deve muovere la pagina.** Mettendolo normalmente, la
  finestra si apriva già scorsa in fondo: si vedeva l'ultima novità e il titolo
  no. Adesso il fuoco arriva con `preventScroll` e la finestra parte dall'alto.
- **«Ho capito» resta sempre attaccato in fondo** (`position:sticky`). Con tre
  novità il tasto finiva sotto il bordo e per chiudere bisognava indovinare che
  si poteva scorrere dentro la finestra. Una finestra che non si capisce come
  si chiude è una trappola, e chi la trova è uno che voleva solo vedere i
  prezzi.

Si chiude in tre modi: il tasto, il buio intorno, il tasto Esc. Toccare dentro
la finestra no.

## Il Bennet «Un mondo di bellezza» aveva spesa vera — 2026-09-19

Il volantino sembrava, dal titolo e dalle prime 17 pagine, tutto shampoo,
creme e cura persona: si poteva pensare di scartarlo in fretta. Non si è
fatto, per la regola di leggere ogni volantino intero senza saltare pagine
sul sospetto — e da pagina 18 in poi c'era una sezione «Il prezzo più basso»
e una «Prodotti indispensabili» piene di pasta, formaggi, salumi, vino,
acqua, surgelati: quasi 90 prezzi veri, metà dei quali di generi alimentari.
Se si fosse scartato il volantino dal titolo, sarebbe stato lo stesso errore
già pagato tre volte (pizze, Mercatò, pesce) con un nome diverso.

**Molte offerte «cura persona» hanno un solo prezzo per due formati diversi**
(«shampoo 250 ml O balsamo 200 ml», stesso prezzo): non è un'offerta 1+1 come
l'Ekom, è il volantino che non distingue. Si è scelto sempre il formato più
piccolo per il conto al litro — il numero che non fa sembrare l'offerta più
conveniente di quanto sia — e scritto nella nota quale altro formato costa
uguale.

**Trappola evitata mentre si scaricavano le pagine**: `scarica.py` era stato
lanciato una volta da dentro `/tmp/lavoro` con una copia di `dati.py`
incollata lì per comodità (`cp strumenti/dati.py .`). Quella copia è rimasta
sul disco, e lanciando `pulisci` da quella cartella con `PYTHONPATH` puntato
a `strumenti/`, Python ha importato **la copia vecchia in `/tmp/lavoro`**
invece del modulo vero (una cartella nel path precede il `PYTHONPATH`), e
`pulisci` continuava a vedere i tre volantini scaduti che invece erano già
stati tolti. Rimossa la copia, `pulisci` è tornato a dire il vero. La lezione:
non lasciare mai copie di `dati.py` fuori da `strumenti/`, nemmeno per un
comando solo.

## La pagina Novità: prima i volantini, poi i prezzi — 2026-09-19

Manlio: «nella pagina novità sarebbe bene che apparissero prima di tutto i
volantini aggiornati, così uno sa l'ultimo giorno e l'ultima settimana cosa è
stato aggiornato; penso che sarebbe bene mettere anche tre giorni. Sarebbe poi
eccezionale se mettessi una tabellina nella quale appaiono tutti i supermercati
e l'intervallo di validità dei loro volantini presenti e di quelli che sai
anche futuri».

La pagina adesso è in tre pezzi, in quest'ordine:

1. **Volantini aggiornati** — cosa è cambiato NEI VOLANTINI nella finestra
   scelta (oggi / 3 giorni / 7 giorni);
2. **Tutti i volantini** — la tabella, sempre uguale: non dipende dalla
   finestra, dice com'è messo il mondo adesso;
3. **Novità dei prezzi** — il diario di prima, giorno per giorno.

I tasti sono diventati tre: **Oggi, 3 giorni, 7 giorni**.

### «Aggiornato» non vuol dire «volantino nuovo»

La trappola da evitare: il diario segna `volantini_arrivati` quando una
**chiave** nuova entra in `dati.py`. Il Bennet «Un mondo di bellezza» è entrato
nell'elenco il 18 settembre e i suoi 102 prezzi sono stati letti il 19: per il
diario il 19 settembre non era «arrivato» niente, ma per chi guarda quello è
esattamente il giorno in cui quel volantino è stato aggiornato.

Quindi il riquadro conta **tre cose**, con tre bollini diversi:

- **nuovo** — il volantino è entrato adesso nell'elenco;
- **letto** — ci sono entrati prezzi suoi (`offerte_nuove` raggruppate per
  volantino: il numero è quanti);
- **finito** — è scaduto e non c'è più.

I volantini nuovi e finiti **non si scrivono più dentro il blocco del giorno**:
sarebbero la stessa cosa detta due volte nella stessa schermata.

### La tabella

Tre gruppi, perché è così che si guarda: **In corso adesso** (ordinati per
quando finiscono, così il primo è quello che sta per scadere), **In arrivo**
(per quando cominciano) e **Appena finiti**. Ogni riga: negozio, il nome del
volantino solo se serve a distinguerlo da un altro della stessa insegna
(«Frutta e Verdura», «Un mondo di bellezza»), le date e **quanto manca**
— «finisce domani» in rosso, «ancora 4 giorni» in verde, «fra 3 giorni» in
ambra.

Dettagli pagati guardandola sul telefono:

- **Il mese si scrive una volta sola** quando è lo stesso («17 → 30 set»):
  scriverlo due volte rubava la riga alla colonna di destra e «ancora 4 giorni»
  andava a capo.
- **Le date vere restano attaccate alla riga** (`data-inizio`, `data-fino`):
  quello che si legge è accorciato, e la prova deve poter controllare sul vero
  che un volantino non sia finito nel gruppo sbagliato.
- **Gli «appena finiti» la tabella se li ricorda dal diario**, non da
  `dati.py`: da lì spariscono quando si fa pulizia, e senza questo uno non
  capisce più dove sia andato a finire un negozio che c'era la settimana prima.

### I volantini che so ma non ho ancora letto

`VOLANTINI_ATTESI`, in `dati.py`: insegna, periodo, date, e dove l'ho trovato.
Non hanno prezzi e non entrano in nessun confronto — servono solo alla tabella,
segnati **«prezzi non ancora letti»**. Senza, un buco di quattro giorni fra un
volantino e il successivo sembrerebbe un buco vero anche quando so già che
verrà coperto. `dati.py` si ferma se un atteso ha la stessa insegna e le stesse
date di un volantino già letto, così il doppione non può restare lì.

La prova è `prova-novita.js`, dentro `prove.sh`: controlla che il riquadro dei
volantini stia davvero in cima, che i tre tasti cambino qualcosa, che nessun
volantino compaia in due gruppi e che nessuno scaduto finisca fra quelli in
corso.

## L'Ekom stampa prima di pubblicare online — 2026-09-19

Manlio, con in mano il volantino di carta preso in negozio: «non so che
versione del volantino tu abbia, non c'è questo», e la foto di una pagina
Surgelati con filetti di merluzzo Alaska 400 g a 1,99, tentacoli di totano
gigante, minestrone a 0,79, patate stick, pizza formato pala, churros.

**Nessuno di quei prodotti era nel volantino che avevo letto** (`ekom08`,
8-21 settembre), la cui pagina Surgelati ha bastoncini Ocean Blu, tubi di
totano da 700 g, zuppa di pesce, Maxibon. Due cose da escludere, e le ho
escluse prima di rispondere:

1. **Non è una differenza di regione.** L'Ekom pubblica anche un'edizione
   Toscana: ho scaricato anche quella e la sua pagina Surgelati è **identica**
   a quella generale. Quindi non era il caso Mercatò (insegne diverse con
   volantini diversi).
2. **Non era un volantino che mi era sfuggito.** Kimbino, volantinofacile,
   offertolino, promoqui, doveconviene e il sito Ekom: quel giorno avevano
   tutti e solo l'8-21 settembre.

Poi la copertina, fotografata da lui: **«I PIÙ EKONOMICI», dal 22 settembre
al 5 ottobre**. Era il volantino successivo, **già in mano ai clienti tre
giorni prima di comparire online**.

**La lezione, che vale per tutte le insegne:** «non l'ho trovato online» non
vuol dire «non esiste». La carta può precedere il web di giorni, e chi entra
in negozio ha in mano offerte che nessun sito ha ancora pubblicato. Quando
qualcosa non torna, **la fonte da credere è quella che ha in mano Manlio**, e
la domanda da fargli è una sola: *che date ci sono sulla copertina?*

Intanto il volantino sta in `VOLANTINI_ATTESI` con le sue date vere: nella
tabella delle Novità si vede «in arrivo», segnato «prezzi non ancora letti».
Così chi guarda sa che dal 22 l'Ekom è coperto, e sa anche che i suoi prezzi
non ci sono ancora — che è esattamente la verità.

## L'Eurospin che colma da solo il suo buco — 2026-09-20

Il 17 settembre avevo segnato in `VOLANTINI_ATTESI` un Eurospin dal 24
settembre al 4 ottobre, trovato su anteprimavolantino ma senza pagine vere
ancora online: buco di 4 giorni dopo la fine di `eurospin10` (20 settembre).
Il 20 settembre, il giorno stesso in cui `eurospin10` scadeva, l'ho ricontrollato
e le pagine c'erano: **22 pagine vere**, lette per intero lo stesso giorno.
Nessun buco da tenere d'occhio, per una volta.

Un dettaglio tecnico da ricordare per il prossimo Eurospin: gli indirizzi
delle pagine di `eurospin10` usano due cifre (`p-01.jpg` ... `p-22.jpg`),
quelli di `eurospin24` cinque (`p-00001.jpg` ... `p-00022.jpg`). **La fonte
non numera sempre allo stesso modo anche per la stessa insegna**: quando gli
indirizzi a due cifre rispondono 403, prima di concludere che il volantino
non è online si prova anche lo schema a cinque cifre.

Il volantino era per metà un concorso a premi a tema Bluey (giocattoli,
abbigliamento, elettronica, mobili, viaggi): pagine scartate perché non
alimentari, ma **non tutta la parte Bluey era da buttare** — in mezzo c'erano
anche un latte, un succo d'arancia, una pasta e un rotolo di carta a tema,
prezzi veri con l'unico difetto di avere un cane blu sulla confezione. Tenuti,
con nota che è una confezione a tema e in un caso (le banane) segnalando che
costava più delle banane normali segnate due pagine prima nello stesso
volantino — per non far sembrare conveniente quello che non lo è.

La pagina «Frutta e verdura / Pescheria» aveva in fondo un lungo elenco di
punti vendita aderenti: non tutti gli Eurospin hanno banco pescheria. Torino
compare più volte nell'elenco (con e senza il simbolo che segna «niente
pescheria»), quindi le offerte di frutta e verdura sono state prese come
sempre, e quelle di pescheria con una nota che dice di controllare che il
punto vendita abbia il banco — stessa logica già usata per il Carrefour Iper
il 2026-09-07 (Torino non compariva nell'elenco degli ipermercati ma
l'offerta valeva lo stesso: qui è il contrario, l'elenco esiste apposta per
dire dove NON vale tutto).

Infine, una pagina «Doppio weekend di follia» con offerte valide solo dal
venerdì alla domenica, due weekend diversi dentro lo stesso volantino
(25-27 settembre e 2-4 ottobre): stessa gestione del «Weekend più uno»
dell'MD, date scritte riga per riga e mai uguali a quelle del volantino
intero (altrimenti `dati.py` le tratterebbe come normali e non come
ristrette, o peggio ancora — se scritte uguali al volantino — il programma
si ferma da solo con l'errore già visto il 2026-09-05).

## Il tasto «Aiuto» — 2026-09-21

Manlio: «fammi anche una piccola finestra di help, la metti con un pulsantino
con scritto sopra aiuto di fianco a quello di novità. **Prima di aggiungerla
fammi vedere il testo**».

E questa è la parte che conta: **il testo l'ha letto e approvato prima che lo
scrivessi nella pagina**. Ha tolto un blocco, «Due cose da sapere» (i prezzi
letti a mano, le righe «da controllare»), e il resto è passato così com'era.
Da rifare allo stesso modo la prossima volta: una finestra che spiega la pagina
la deve approvare chi la pagina la usa, non chi la scrive.

**Tre finestre, tre lavori diversi**, e non vanno mescolate:

- **«Aiuto»** (nuova): come si usa la pagina. Non si apre mai da sola, si
  riapre quante volte si vuole, non si ricorda niente. È lì per quando serve.
- **«Cosa c'è di nuovo»**: si apre da sola la prima volta e racconta cosa è
  cambiato nell'interfaccia. Vista una volta, non torna più.
- **«Novità»** (il tasto rosso): porta al diario dei prezzi e dei volantini.

**Il tasto è vuoto, non rosso pieno.** In questa pagina il rosso pieno vuol
dire «premi qui adesso» — «Novità» e «Cerca fra i prezzi» — e un aiuto non è
una cosa da premere adesso: è una cosa da trovare quando si è in difficoltà.
Bordo rosso e scritta rossa bastano a farlo vedere senza chiamare.

Riusa lo stesso vestito della finestra delle novità (`.buio` + `.finestra`),
quindi anche le due cose imparate lì: il fuoco sul tasto arriva con
`preventScroll` e «Ho capito» resta attaccato in fondo, sempre visibile.

La prova è `prova-aiuto.js`, dentro `prove.sh`: controlla che il tasto stia in
cima e non dentro la barra, che la finestra **non** si apra da sola, che si
riapra sempre, che dentro ci siano davvero le otto spiegazioni e che le due
finestre non stiano aperte insieme.

## Lidl 24-30 settembre, e dove trovare l'Ekom in anteprima — 2026-09-22

**Il Lidl annunciato il 21/9 su anteprimavolantino era ancora senza pagine
vere** (indirizzi delle immagini a 404): il 22/9, un giorno dopo, le 52 pagine
c'erano tutte, indirizzo `volantino-lidl-2026-09-24-p-{n:05d}.jpg`. Confermato
che erano davvero 52 e non di più: la pagina 53 risponde 403 con un corpo da
1242 byte, la firma del «non esiste» già vista con Mercatò ed Ekom.

**CORRETTO più tardi lo stesso giorno — quanto scritto qui sopra su kimbino era
incompleto, e ha fatto perdere un giorno.** Manlio ha segnalato
`ekomdiscount.it/volantini`: il volantino «I più ekonomici» (22 settembre-5
ottobre) c'era già online **lì**, con tutte le 16 pagine, lo stesso giorno in
cui kimbino non lo sapeva ancora. **`kimbino.it/ekom/` non è affidabile per
l'Ekom**: è una fonte di terzi che a volte è indietro rispetto al sito
ufficiale, non il contrario. **Da qui in poi, per l'Ekom si controlla prima
`ekomdiscount.it/volantini`, il sito ufficiale — kimbino resta solo un
secondo controllo.**

**Perché un fetch semplice non basta.** `ekomdiscount.it` è un'app
Javascript: `curl` o `WebFetch` vedono solo il guscio vuoto della pagina (circa
1,9 KB), mai i volantini veri. Serve un browser vero. Con Playwright
(Chromium preinstallato in `/opt/pw-browsers`, va aperto con
`ignore_https_errors=True` per il proxy dell'ambiente) e ascoltando le
richieste di rete durante il caricamento, si vede che la pagina chiama:

    https://www.ekomdiscount.it/ebsn/api/leaflet/search?parent_leaflet_type_id=1

che risponde in JSON **senza bisogno del browser**: basta un `curl` normale.
Dentro c'è la lista dei volantini in corso, con `fromDate`/`toDate` e un
`baseLocation` per ciascuno; le pagine sono `{baseLocation}{n}.png`, **`n` da
0** (la pagina 1 stampata è `0.png`, come per Mercatò e per l'Ekom dell'8-21).
Va ricontrollato che il numero di pagine non cambi da un volantino all'altro:
si controlla come sempre guardando quando l'indirizzo smette di rispondere
200 (qui: 403 con un corpo piccolo).

Questa è anche una fonte diversa da kimbino per **scaricare** le pagine, non
solo per **sapere** che il volantino esiste: gli indirizzi vanno in
`pagine_ekom.py`, la stessa lista di prima ma con la nuova base.

## Il tasto «Look»: cento vestiti per la pagina (2026-09-22)

Manlio ha mandato un PDF di Figma con **cento combinazioni di colori** e ha
chiesto: analizzale, ricavane cento palette per il sito, e metti un tasto
«Look» per sceglierle.

### Tirare fuori i cento colori dal PDF

Il PDF non aveva i codici dei colori come testo: le quattro caselle di ogni
combinazione erano immagini. Tre strade provate, in ordine:

1. `pypdf` per leggere il testo: si piantava (`_cffi_backend` mancante,
   risolto con `pip install cffi`), ma il testo dei codici non c'era comunque.
2. Rendere la pagina con PyMuPDF e **pescare il colore a pixel** dal centro di
   ogni casella. Funziona, ma caselle vicine di colore simile si fondevano:
   la soglia di distinzione è scesa da 12 a 3 e si campiona su più righe.
   Le caselle bianche venivano buttate via da un filtro «troppo chiaro»:
   tolto, il bianco è un colore come un altro.
3. L'OCR dei codici esadecimali scritti sotto le caselle, con la lista di
   caratteri ristretta a `0-9A-F`, per **incrociare** i due risultati.

Il controllo finale: il codice letto dall'OCR e il colore pescato a pixel non
devono discostarsi di più di 25 su 255 per canale. Dove non tornava, ha vinto
il pixel. Il risultato sta in `strumenti/palette.json`: cento combinazioni con
nome, famiglia e quattro colori — 11 monocromatici, 16 neutri, 17 tranquilli,
16 romantici, 13 giocose, 15 vivaci, 12 stagionali.

### Da quattro colori a una pagina intera

Una palette di quattro colori non è una pagina: la pagina ha carta, pannelli,
inchiostro, righe, l'accento dei prodotti accesi, il verde del «meno caro»,
l'ambra degli avvisi. `strumenti/look.py` fa la traduzione, e le scelte sono
queste:

- **Chiaro o scuro lo decide la palette**, non il telefono. Se il colore più
  chiaro dei quattro è comunque scuro (luminosità sotto 0.45), il look nasce
  scuro: sono 12 su 100. Attenzione: questo **non** rimette in ballo
  `prefers-color-scheme`, che nel CSS continua a non esistere (vincolo 4) —
  la pagina non diventa mai scura da sola, diventa scura solo se lui sceglie
  un look scuro.
- **La carta non è mai un colore pieno**: è il colore più chiaro mescolato
  all'86% di bianco (o il più scuro con il 35% di nero, nei look di notte).
  Un fondo saturo su tutto lo schermo stanca in tre secondi.
- **L'accento è il più saturo dei quattro**, spinto finché non arriva a 4,5
  volte il contrasto minimo sul fondo. È il colore del «prodotto acceso» e del
  tasto «Cerca fra i prezzi»: se non si vede, la pagina non si usa.
- **Il verde e l'ambra non seguono la palette.** In questa pagina il verde
  vuol dire «il meno caro» e l'ambra «attenzione alla data»: sono
  informazioni, non decorazione. Cambia solo la loro tinta, quel tanto che
  serve a starci sopra il fondo scelto. Un look che facesse diventare blu il
  bollino del meno caro sarebbe un look che mente.
- **Il pannello si stacca dalla carta finché il testo non ci sta sopra
  comodo**: al primo giro dieci look non passavano il controllo, e il
  pannello si avvicina alla carta un passo per volta finché il testo non
  arriva a 6 volte il minimo.

### Il controllo, che è la parte seria

`look.py` misura sette accoppiate per ognuno dei cento look (testo su carta,
testo su pannello, accento su carta, scritta sull'accento, verde sul suo
fondo, ambra sul suo fondo, testo tenue su carta) con la regola del contrasto
WCAG, e **`verifica()` si ferma con un errore** se anche uno solo resta sotto
il minimo. Gira a ogni generazione della pagina, quindi un look illeggibile
non può arrivare pubblicato. Il più tirato dei cento, al momento, è «Cool
revival» sull'accoppiata accento/sfondo: sta esattamente sul minimo.

La prova `prova-look.js` rifà gli stessi conti **in JavaScript sulla pagina
vera**, e controlla anche: che le righe siano 101 (i cento più «Originale»),
che ognuna mostri le sue quattro strisce di colore, che scegliere cambi
davvero `--rosso`, che la scelta sopravviva alla ricarica, che esista almeno
un look scuro, che «Originale» rimetta tutto com'era, e — la più importante —
**che la pagina appena aperta non abbia nessun look addosso**: chi non ha mai
scelto niente deve vedere la pagina di sempre.

### Come sta in pagina

Tasto vuoto in cima, prima di «Aiuto», stesso vestito delle altre finestre
(`.buio` + `.finestra` + «Fatto» attaccato in fondo), **fuori dalla `.barra`**
per la solita ragione del cassetto. Le tre finestre non stanno aperte insieme:
aprirne una chiude le altre. L'elenco si costruisce solo quando si apre — cento
righe con quattro strisce l'una sono 400 elementi, e costruirli all'apertura
della pagina si sentirebbe sul telefono.

La scelta sta in `localStorage` (`spesa.look.v1`) e si applica cambiando le
variabili CSS su `documentElement`, più il `theme-color` della barra del
browser. Niente foglio di stile in più, niente pagine generate in più: i cento
look sono un pezzo di dati dentro `DATI`, circa 30 KB.

## Il riquadro del meno caro, i giorni che mancano, e la cima più vuota — 2026-09-22

Tre richieste di Manlio nello stesso pomeriggio, tutte sulla stessa cosa:
**far arrivare prima la risposta**.

### «Il meno caro in una pillola, e le offerte non ancora cominciate sbiadite»

Prima ha chiesto «descrivicelo solo il meno caro, in un riquadrino colorato»
e ho fatto un riquadro verde in cima ai prezzi, prima dell'elenco. Poi, senza
averlo ancora visto, si è spiegato meglio: «che il prodotto meno caro venisse
messo in una pillola, con un bordo e con un colore che la evidenzi, magari lo
stesso colore del fondo ma un po' più forte. E che le offerte che non sono
ancora cominciate apparissero sbiadite».

**Il riquadro separato è stato tolto.** Era durato mezz'ora e non l'ha mai
visto, ed è giusto così: diceva le stesse identiche cose della riga
sottostante — nome, negozio, formato, prezzo della confezione, scadenza, nota,
collegamento — due volte di fila. La stessa risposta scritta due volte non è
due risposte.

Adesso c'è **una** cosa sola: la riga del meno caro è una pastiglia, fondo
`--pannello` (che è letteralmente «lo stesso colore del fondo ma un po' più
forte»), bordo verde, angoli tondi, staccata dalle vicine. E le offerte che
devono ancora cominciare sono a `opacity:.72`.

Le due richieste si tengono per mano più di quanto sembri. Il riquadro in
cima serviva a una cosa sola che la pastiglia da sola non faceva: **il meno
caro che vale oggi non è sempre la prima riga**, perché l'elenco è in ordine
di prezzo e sopra ci possono stare offerte che partono lunedì. Sbiadendo
quelle, la pastiglia si trova da sola anche quando è la terza: le righe sopra
si vedono che non contano. Il problema che il riquadro risolveva l'ha
risolto la sbiadatura.

Sbiadite **non vuol dire nascoste**: un prezzo che parte lunedì serve saperlo,
e 0,72 è il punto in cui si legge ancora. Più giù il prezzo diventa un
suggerimento.

La pastiglia **non compare** nei risultati di «Cerca fra i prezzi» né nelle
offerte di un singolo volantino, esattamente come il bollino verde e per la
stessa ragione già scritta più su: lì «il meno caro» vorrebbe dire «di quello
che hai cercato» o «di questo negozio», e si leggerebbe «di tutti».

Il fondo `--pannello` ha costretto a stringere una vite nel generatore dei
look. Verde, blu e ambra erano portati a 4,5 di contrasto **sulla carta**, e
basta; sulla pastiglia stanno invece sul pannello, che è un gradino più
scuro. Adesso vengono spinti anche contro il pannello, e `_tinta()` — che
calcola i fondi tenui dei bollini — stende la tinta *finché* tutto quello che
ci finisce sopra resta leggibile. Otto misure nuove in `MISURE`; i look che
non passavano si sono aggiustati da soli.

### «Quella dove c'è scritto 6.80, usala piccola per i giorni che mancano»

Ha mandato quattro schermate di riquadri Material, fra cui l'anello del
traffico dati di Google Fi: numero grande dentro, anello che si consuma
intorno. Adesso ogni offerta ha il suo, piccolo, a destra sotto il prezzo —
pastiglia del meno caro compresa.

Due scelte che non vanno cambiate:

- **Il numero conta oggi.** Un'offerta che scade stasera dice «1 oggi», non
  «0». Uno zero su una riga ancora valida si legge «è finita», e fa saltare
  un'offerta buona: è la stessa regola della novità falsa, al contrario.
- **Blu, e ambra negli ultimi tre giorni.** Non rosso: in questa pagina il
  rosso pieno vuol dire «premi qui» o «prodotto acceso», e un anello rosso
  su ogni riga lo svuoterebbe di senso. L'ambra è già il colore delle date da
  guardare, e resta ambra in tutti i cento look.

Le offerte che devono ancora cominciare non hanno l'anello: lì il numero
direbbe quanto manca alla *fine* mentre la riga dice quando comincia, e due
numeri che dicono cose diverse sulla stessa riga sono peggio di nessun numero.

Nel frattempo gli angoli di tutta la pagina si sono ammorbiditi nella stessa
direzione delle schermate che ha mandato: pannelli e riquadri a 20-24 px, i
bollini e i tastini dei volantini diventati pastiglie tonde, i bottoni larghi
a pillola.

### «Togli Torino corso Siracusa e il bollino i»

Erano le due uniche cose in cima che non servivano a fare niente: dove sono i
negozi lo sa già lui. Tolte tutte e due. Quello che stava dietro il bollino
(se questa copia è solo sua o condivisa) è finito in fondo alla finestra
«Aiuto», che è il posto delle spiegazioni. Il bollino «i» accanto al *nome
del prodotto* è un'altra cosa e resta dov'è.

### Un baco trovato di rimbalzo

Aggiungendo tre novità nello stesso giorno, la finestra «Cosa c'è di nuovo»
ha ricominciato ad aprirsi a ogni apertura. Il motivo: chiudendola si
segnava come «vista» l'**ultima dell'elenco**, ma il confronto fra id è
alfabetico e `2026-09-22-look` viene *dopo* `2026-09-22-giorni`. Adesso si
segna l'id più grande, non l'ultimo. Finché le novità erano una al giorno il
baco non poteva vedersi.

### Tre rifiniture dello stesso pomeriggio (2026-09-22, sera)

**«Apri la pagina del volantino» è diventato un'icona.** Era una riga intera
di scritta maiuscola su *ogni* offerta, e le offerte per un prodotto sono
venti. Adesso è una pastiglietta col foglietto del volantino, il numero della
pagina e la freccia, in fila con gli altri bollini. La frase intera resta nel
`title` e nell'`aria-label`: chi tiene premuto o usa un lettore di schermo la
sente tutta. Quando l'offerta non ha l'indirizzo della pagina resta la riga
scritta in fondo — un'icona che non apre niente è una presa in giro.

**«Vale dal 24 settembre» è diventato un tondino**, su richiesta sua: «potrebbe
anche lui diventare un'icona rotonda come quella dei giorni di validità, con
al centro il numero del giorno e sotto il nome del mese». Sta nello stesso
angolo del cerchietto dei giorni, e non si pestano mai i piedi: o un'offerta è
cominciata e conta quanto le resta, o deve cominciare e dice quando. La riga
scritta continua comunque a dire «vale dal 24 settembre al 30 settembre», che
è la versione lunga per chi la vuole.

**Il prezzo di un'offerta che non è ancora cominciata è grigio.** Manlio: «si
nota poco che non sono ancora attivi». Aveva ragione, e il motivo era preciso:
il numero rosso grande è la cosa che si vede di più della riga, e continuava a
gridare «sono qui» anche quando in cassa quel prezzo non lo facevano. Adesso è
`--tenue`, e la riga è salita da 0,72 a 0,82 di opacità — sbiadire *tutto* di
più avrebbe reso illeggibile anche quello che serve leggere.

## L'impaginazione a schede — 2026-09-22 (sera)

Manlio ha mandato la schermata di un'altra versione della pagina — fatta da
un altro programma, su un indirizzo suo — e ha detto: «manteniamo pure tutte
le iconcine che abbiamo fatto fino adesso, ma la pagina deve avere questo
look. L'impaginazione è più bella così, con tutto messo in pillole e
ordinato». Prima di toccare niente gli ho fatto quattro domande, perché nella
schermata c'erano tre cose che nella nostra applicazione non esistono.

**Cosa ha deciso lui:**

- **La scelta dei negozi non si fa.** Nella schermata c'erano un tasto
  «Negozi» e la riga «Supermercati selezionati: 7 su 7 — Modifica». Gliel'ho
  offerta funzionante e ha detto di no, due volte: «non mi interessa, non
  metterla». Quindi non c'è, e non va rimessa perché «c'era nella foto».
- **Il negozio è un marchio, non un nome.** «Al posto del nome del negozio e
  dell'intero indirizzo, che non mi interessa niente, mettici il marchio dei
  supermercati.» I marchi veri sono di chi li ha e questa pagina non li
  pubblica (stessa regola per cui non pubblica le pagine dei volantini):
  quello che c'è è il nome dell'insegna scritto nei suoi colori, dentro una
  pillola con fondo e scritta fissati tutti e due — così si legge uguale con
  qualunque dei cento look addosso.
- **La marca del prodotto resta dov'è.** Nella schermata era una pillola a
  parte («Tre Mulini», «Divella»). Da noi sta attaccata al nome del prodotto
  in `dati.py`, su 1235 righe, e lui ha detto di lasciarla lì.
- **Solo i tondini, non le date scritte.** La schermata aveva pillole «Inizia
  il 24/09» e «Fino al 05/10»; noi avevamo appena fatto i tondini. Ha scelto i
  tondini. La data per esteso resta comunque scritta nella riga sotto il nome.
- **Il tasto «Look» resta**, e i cento look continuano a colorare anche questa
  impaginazione: i colori sono una cosa, la disposizione un'altra.

**Una cosa che ha chiesto prima e che qui non c'è:** la riga «Torino (corso
Siracusa)» in cima. Nella schermata c'era, ma poche ore prima me l'aveva fatta
togliere («è inutile»). Un'istruzione detta vale più di un dettaglio in una
figura: non l'ho rimessa, e gliel'ho detto.

**Due cose imparate rifacendola:**

1. **A due colonne, sul telefono, la scheda si strozza.** A 390 px il nome del
   prodotto andava a capo ogni due parole e i prezzi finivano schiacciati.
   Sotto i 560 px la scheda va in colonna e i prezzi scendono su una riga
   loro.
2. **Il negozio non sta più in `.sotto b`.** Tre prove lo cercavano lì per
   sapere di che insegna fosse un'offerta; adesso lo cercano in `.marchio`.
   Chi tocca la scheda si ricordi che quelle prove leggono il DOM vero.

## I marchi veri dei supermercati — 2026-09-22 (notte)

Manlio: «al posto delle pillole con scritto il nome dei vari supermercati,
mettici i veri loghi». Giusto: un marchio si riconosce con la coda dell'occhio,
un nome scritto va letto.

**Dove li abbiamo presi.** Wikimedia Commons ne ha tre a licenza libera
(Lidl, MD, Eurospin: tutti «pubblico dominio», perché sono scritte e forme
semplici, sotto la soglia del diritto d'autore). Carrefour e Ipercoop ci sono
ma quel giorno Wikimedia rispondeva **429** a ogni richiesta da questo
indirizzo: non è che manchino, vanno ripresi con calma un altro giorno.
Di Mercatò e Ekom su Commons non c'è niente. Il **Bennet** e l'**Ekom** li ha
mandati Manlio.

**Il caso Ekom, che ha insegnato una cosa nuova.** Quello che ha mandato era
un'immagine, non un disegno: a schermo grande sgranerebbe. Da lì è nato
`strumenti/vettore.py`, che da una figura a un colore pieno tira fuori un
disegno vero. Tre cose che non si potevano indovinare:

1. **`potrace.Bitmap` si rovescia da solo** nel suo costruttore. Per far
   disegnare il pieno gli si passa il vuoto. Passandogli il pieno esce un
   rettangolo, che è il fondo della figura.
2. **Gli si passa un array di veri/falsi, non di 0 e 1.** Con i numeri il suo
   confronto interno (`data > 127`) li considera tutti vuoti, e di nuovo esce
   un rettangolo. Due volte lo stesso risultato sbagliato per due motivi
   diversi: la prima volta ho pensato che il logo fosse troppo complicato.
3. **Si traccia in grande e si rimpicciolisce.** Sui bordi curvi di una
   scritta a pennello, tracciare alla dimensione della figura lascia gradini;
   al doppio vengono lisci. Il risultato pesa 13 KB e non sgrana mai.

**Due scelte di sostanza.**

- **La pastiglia del marchio ha il fondo bianco fisso**, anche con un look
  scuro addosso. I loghi hanno i loro colori: su fondo nero il Lidl sparisce e
  l'MD diventa un'altra cosa. Il bianco è l'unico fondo su cui un marchio è
  ancora sé stesso, e questa è l'unica cosa della pagina che i cento look non
  toccano.
- **Dentro la pastiglia il nome c'è sempre**, nascosto alla vista. Un logo,
  per chi non lo vede, è un buco; ed è anche il modo con cui le prove sanno di
  che negozio è un'offerta.

I marchi restano di chi li ha. Stanno lì per far riconoscere il negozio di
un'offerta letta dal suo volantino, e il piede della pagina lo dice.

## L'Ipercoop, finalmente coi prezzi — 2026-09-22 (notte fonda)

Manlio, dopo che gli avevo spiegato che l'Ipercoop c'era solo in tabella come
«in arrivo dal 24»: «Allora fai che mettere subito quello del 24». Il 24 era
fra due giorni. Nell'elenco pubblico del negozio non c'era. È saltato fuori
lo stesso, ed è questa la cosa da ricordare.

### Il volantino c'era già, solo non si vedeva

Il canale Nova Coop (`negozi.volantinopiu.com/ccno-8001120004796.html`, quello
linkato da `novacoop.it`) mostrava ancora i soliti tre volantini vecchi.
Kimbino scriveva in grande «Ipercoop volantino dal 24/09/2026», ma è un titolo
esca: dentro c'erano solo i volantini del 10. Anteprimavolantino, promoqui,
doveconviene: niente.

Però ogni volantino del canale si apre con un indirizzo fatto così:

    negozi.volantinopiu.com/redirect<id>.html?id_pv=24
       → ipercoop.volantinopiu.com/volantino<id>00pv24.html

Quel secondo indirizzo **risponde per qualunque id**, anche per i volantini che
il canale non elenca ancora. Quindi basta chiedere gli id uno per uno partendo
dal più alto che si conosce e guardare il `<title>` e le date:

    for i in range(28786, 28960):
        curl -s "https://ipercoop.volantinopiu.com/volantino{i}00pv24.html"
        # <title>IperCoop Novacoop - Extra offerte</title>
        # Dal 24/09/2026 al 07/10/2026

Sono venuti fuori subito: «Tendenze d'Autunno» (24/9-21/10, non alimentare) e
**«Extra offerte», dal 24 settembre al 7 ottobre**, che è il volantino della
spesa vera, quello che aspettavamo da due settimane. Era stato caricato il 22
alle 18, poche ore prima. **Da rifare così ogni volta che serve un Nova Coop
prima che compaia nell'elenco.**

### Quattordici edizioni, e i prezzi non sono gli stessi

Di «Extra offerte» ci sono quattordici id consecutivi, 28831-28844, tutti
«IperCoop Novacoop». Non sono copie: confrontando le pagine, il latte Arborea
costa 1,39 in una e 1,45 in un'altra, le uova 1,95 o 1,74.

**La zona è stampata sul frontespizio**, in mezzo alla pagina, sotto le foto:
«TORINO - COLLEGNO», «NOVARA - GALLIATE», «Via Polesine, 2 - CHIERI»... Si
legge ritagliando quella striscia dalla copertina di ognuna. L'elenco:

    28831 TORINO - COLLEGNO     28838 Cuorgnè
    28832 NOVARA - GALLIATE     28839 Cuneo
    28833 Borgomanero           28840 Crevoladossola
    28834 Casale Monferrato     28841 Pinerolo
    28835 Borgosesia            28842 Biella
    28836 Chieri                28843 Gravellona Toce
    28837 Ciriè                 28844 Beinasco

Abbiamo preso **28831, Torino - Collegno**, perché Manlio vive a Torino.
**Ma c'è una cosa da chiedergli**: l'Ipercoop di **Beinasco** (Strada Torino
34/36) è più vicino a corso Siracusa di quello di Torino via Livorno 51, e ha
la sua edizione, la 28844, con qualche prezzo diverso. Se dice che va lì, basta
cambiare l'id nell'indirizzo dentro `VOLANTINI` e rileggere le poche pagine
che cambiano.

Nota di metodo: il primo id del gruppo è anche quello del negozio del canale.
Vale per «Scegli tu Grandi Marche» (28380, primo dei quattordici Novacoop) e
vale per questo. Ma **non ci si fida della posizione**: si guarda il
frontespizio, che è scritto nero su bianco.

### Cosa c'era dentro

47 pagine, lette tutte. 152 prezzi in `dati.py`, in quasi ogni reparto:
macelleria, banco taglio, pescheria, formaggi, salumi, surgelati, dispensa,
bevande, ortofrutta, panetteria, casa e igiene. 21 pagine scartate: fiori,
giardinaggio, fai da te, auto, casalinghi, libri, elettrodomestici Expert,
tre pagine di raccolta bollini Alessi dove i prodotti hanno solo il numero di
bollini e nessun prezzo, e le due «Grandi Marche Selection», che sono quelle
che per due settimane mi avevano fatto dire «l'Ipercoop non ha prezzi»: solo
«-30% su tutta la linea», senza il prezzo di partenza.

Tre cose decise leggendo, tutte e tre nella direzione di non gonfiare l'offerta:

- **Le pagine «1,2,3 più compri meno paghi»** danno tre prezzi: uno, due o tre
  pezzi. In riga va **il prezzo di UN pezzo**, e la nota dice cosa si paga
  prendendone due o tre. Il prezzo da tre pezzi è vero solo se ne compri tre.
- **Le pagine «1+1»** seguono la regola dell'Ekom: nel formato c'è quanta roba
  si porta via («2 × 680 g (1+1)»), nella nota quanto costa una confezione
  sola.
- **Il tonno in vaso e in scatola** l'ho contato sul peso lordo, come fa il
  volantino, ma scrivendo nella nota che sgocciolato è meno: il peso
  sgocciolato non è stampato e inventarlo sarebbe peggio.

I prezzi **«solo per i soci»** e gli sconti soci sono segnati riga per riga col
prezzo senza tessera nella nota, esattamente come la MD Buona Spesa Card e la
carta EKOM UP. Il latte microfiltrato Coop a 1,19 **vale solo dal 28 settembre
al 4 ottobre**, e quelle date stanno sulla riga.

Da oggi le insegne con prezzi veri sono otto su otto, e l'Ipercoop ha anche il
suo marchio vero nelle schede.

## Lo stesso numero scritto due volte — 2026-09-22 (sera)

Manlio, guardando le schede: «ci sono dei prodotti col prezzo al kg che
corrisponde al prezzo al pezzo, soprattutto nei salumi ma anche negli altri
prodotti da banco, che chiaramente non sono confezionati. Puoi toglierli nel
caso in cui coincidano».

Aveva ragione ed era un difetto vecchio, nato quando la scheda ha preso i due
prezzi: quello **per unità** (il numero grande rosso, «12,99 € al kg») e quello
**della confezione** («12,99 € al pezzo», più il «12,99 € la confezione» nella
riga del formato). Per una confezione da 500 g i due numeri dicono due cose
diverse e servono tutti e due. Ma per una carne venduta **al kg**, o per un
salume al banco, la confezione non esiste: la quantità è 1 kg, quindi il conto
prezzo/quantità ridà lo stesso numero di partenza, e la scheda lo ripeteva
tre volte in tre posti.

Erano **296 offerte su 1387**: macelleria 61, ortofrutta 60, gastronomia 51,
freschi 24, dispensa 24, salumi 21, pescheria 16. Un quinto di tutto.

La regola adesso: se il prezzo scritto della confezione e quello per unità
sono **la stessa scritta**, si scrive una volta sola. Sparisce il secondo
prezzo e sparisce il «… € la confezione»; resta «Formato: al kg · fino al 28
settembre» e il numero grande.

Due dettagli che valgono più di quanto sembri:

- **Si confrontano le scritte, non i numeri.** `eur(o.prezzo) ===
  eur(o.unitario)`, non `o.prezzo === o.unitario`: 12,67 e 12,670001 sono due
  numeri diversi per il computer e la stessa cosa per chi guarda la pagina.
  Confrontando i numeri interi sarebbero rimaste in giro schede col doppione
  proprio dove il conto non torna esatto.
- **La prova è stata cambiata, non tolta.** `prova-meno-caro.js` pretendeva che
  ogni scheda dicesse quanto costa la confezione: con la regola nuova sarebbe
  fallita su un quinto delle offerte. Adesso controlla le due strade — o c'è
  la scritta e allora c'è anche il secondo prezzo, o non c'è né l'una né
  l'altro — che è più forte di prima: prende anche il caso opposto, un secondo
  prezzo mostrato senza dire cos'è.

**Rimasto aperto**, e glielo ho chiesto: i banchi venduti **all'etto**. Lì i
numeri sono diversi (2,59 all'etto, 25,90 al kg), quindi la regola non scatta,
ma la scritta «al pezzo» è sbagliata lo stesso — un etto non è un pezzo. Lui
ha detto «poi vediamo se è difficile farli togliere anche in altri casi»:
questo è il primo degli altri casi.

## I bottoni che si mangiavano lo schermo — 2026-09-22 (notte)

Manlio: «mi hanno fatto notare che i bottoni delle categorie tengono troppo
posto, bisogna assolutamente rimpicciolirli… tutte le categorie che hanno più
di una parola, se è possibile, devono essere ridotte a una sola parola, e
prosciutto crudo e cotto riuniti; le cose surgelate, è inutile dire che sono
surgelate. Credo che in tal modo quasi si possa raddoppiare il numero di
alimenti visualizzabili».

Tre cose insieme, e la terza è quella che costava di più in spazio.

### I nomi

Su 67 voci, 23 avevano più di una parola. Adesso ne restano quattro, e ognuna
ha il suo motivo scritto:

- **Olio d'oliva** e **Olio di semi**: accorciarli li confonderebbe fra loro.
- **Carta igienica**: «Igienica» da sola non si legge come niente.
- **Verdure surgelate**: «Verdure» si confonderebbe con **Verdura**, la
  categoria della verdura fresca. Qui il «surgelate» non è inutile: è l'unica
  cosa che distingue le due voci. Questa è l'eccezione a quello che ha chiesto,
  e gliel'ho detta.

Prosciutto crudo e cotto sono diventati **Prosciutto**, una voce sola con le
parole di tutti e due. «Carne di bue» è diventato **Manzo**, «Succhi e bibite»
**Bibite**, «Detersivo lavatrice» e «Detersivo lavastoviglie» **Lavatrice** e
**Lavastoviglie**, «Carta cucina e tovaglioli» **Asciugatutto**, «Sapone e
bagnoschiuma» **Bagnoschiuma**, «Pesce fresco» **Pesce**. In tutto 393 righe di
prezzo hanno cambiato l'etichetta della categoria.

### Perché esiste `RINOMINATE`, e perché non si cancella

I nomi vecchi non sono solo nostri: **sono scritti nella lista salvata nel loro
telefono**. Senza una tabella dei nomi vecchi succedevano due cose, tutte e due
brutte:

1. Il bottone di Manlio avrebbe continuato a chiamarsi «Prosciutto crudo»,
   cioè il nome lungo che volevamo togliere, per sempre.
2. **«Pesce fresco» non si sarebbe riagganciato affatto.** Il riaggancio di una
   categoria sparita va per nome e per parole del volantino, e fra le parole
   del pesce la parola «pesce» **non c'è apposta** — tirerebbe dentro i
   bastoncini di pesce e i sughi di pesce. Quindi «Pesce fresco» non avrebbe
   trovato «Pesce» e sarebbe rimasto un bottone morto.

La tabella tocca **solo** chi ha ancora esattamente il nome che aveva il
catalogo: chi si è rinominato un prodotto a modo suo se lo tiene.

E serve anche a `storia.py`: il diario confronta la fotografia di ieri con
quella di oggi, e un'offerta il cui `cat` cambia viene raccontata come «ha
cambiato reparto». Senza tradurre la fotografia vecchia, il diario del giorno
del cambio avrebbe annunciato **393 traslochi** — «Prosciutto crudo diventa
Prosciutto» ventisei volte. Una novità falsa, e di quelle grosse.

### Lo spazio

Le pastiglie erano alte 44 px con la scritta da 15: due file di bottoni si
mangiavano mezzo schermo del telefono prima ancora di far vedere un prezzo.
Adesso sono alte 34 con la scritta da 14 e 6 px di distanza. Con i nomi di una
parola, in una riga ce ne stanno circa il doppio — che è esattamente quello
che aveva previsto lui.

Le schede delle offerte hanno perso un po' d'aria (padding, margini, il prezzo
grande da 28 a 26 px): **stessa roba, meno spazio**, nessuna informazione
tolta.

### Il tasto rosso

Sempre quella sera: «la scritta "cerca fra i prezzi di tutte le offerte" può
anche essere su una pillola con dimensioni diminuite in verticale». Gli ho
proposto tre scritte e ha scelto **«Cerca un prodotto o una marca»**. La
pastiglia è passata da 54 a 42 px ed è tonda come le altre.

Si perde il «fra TUTTE le offerte», che era lì apposta per distinguerlo dalla
casella dentro «+ altri prodotti». Per questo quella spiegazione **è rimasta
nell'Aiuto** e nella casella che si apre («Scrivi un prodotto, una marca, un
negozio…»). `prova-aiuto.js` controlla che l'Aiuto chiami il tasto col nome
che il tasto ha davvero: se un domani si cambia di nuovo la scritta, la prova
si accorge che l'Aiuto è rimasto indietro.

## Il Pam — 2026-09-22 (notte)

Manlio: «Mettiamoci anche il Pam che a Torino ce ne sono. Tantissimi fai tutte
le cose necessarie per metterlo.»

### Quale Pam

Il sito `pampanorama.it` è un'app che chiede tutto a `coeus.ppapi.it`. Ci sono
due chiamate che servono:

    POST https://coeus.ppapi.it/api/v2_2/post/query?noCache=0&typeUuid=store
         limit=100&typeUuid=store&fields[0]=slug&fields[1]=name&fields[2]=description
         &metadatas[0]=address&metadatas[1]=latitude&metadatas[2]=longitude
         &metadataQueries[latitude][$between][0]=44.98 … [1]=45.12
         &metadataQueries[longitude][$between][0]=7.55 … [1]=7.75
       → i negozi in un riquadro della mappa

    POST https://coeus.ppapi.it/api/v2_2/post/query?noCache=1&typeUuid=flyer
         typeUuid=flyer&fields[0]=slug&fields[1]=image&fields[2]=name&limit=30
         &orders[publishedAt]=desc&relationshipQueries[flyer_store][$in][0]=<id negozio>
       → i volantini di QUEL negozio, con link volantinopiu, pdf e date

Basta un `curl` normale con `Origin` e `Referer` di pampanorama.it.

A Torino ci sono 35 Pam fra Pam, Pam Local, Pam Superstore e Panorama. Il più
vicino a corso Siracusa è il **Pam di corso Orbassano 212**, a 400 metri
(store 71, codice punto vendita 2311). Dopo vengono il Pam Local di piazza
Santa Rita (1 km) e il Pam di corso Cosenza (1,2 km).

### Pam e Panorama non hanno lo stesso volantino

Per il 10-23 settembre volantinopiu aveva sette id: 28603-28605 «PAM Panorama
- Sotto Prezzo», **28606 «PAM Supermercati - Sotto Prezzo»**, 28607-28608
«PAM Panorama - Occasioni Extra», **28609 «PAM Supermercati - Occasioni
Extra»**. Per corso Orbassano l'API dava 28606 e 28609: i «Supermercati».
I Panorama sono altri negozi con altri prezzi, e non vanno mescolati.

### Quelli dal 24 c'erano già, come per l'Ipercoop

Il 22 l'elenco del negozio dava ancora solo quelli che scadevano il 23.
Chiedendo gli id uno per uno (stesso trucco dell'Ipercoop, con `pv2311`):

    pam.volantinopiu.com/volantino<id>00pv2311.html   → <title> e «valido Dal … al …»

sono usciti 28804-28810 e 28848-28849, tutti dal 24 settembre al 7 ottobre.
I due «PAM Supermercati» sono **28807** («Tante offerte a 1, 2, 3 euro», 20
pagine) e **28849** («Occasioni Extra», 27 pagine). Le immagini stanno dove
stanno quelle dell'Ipercoop: `resources.volantinopiu.it/flyer/2/8/8/0/7/pagine/<n>.jpg`.

### Com'è fatto

- **«con APP»** su un prezzo vuol dire che vale solo con l'app Pam Perte Plus.
  Il volantino non stampa quanto costa senza app: nella nota c'è scritto
  «Solo con l'app Pam Perte Plus», come per la MD Buona Spesa Card, ma senza
  il prezzo pieno perché non c'è.
- Tante offerte sono «gusti e grammature assortiti» allo stesso prezzo: il
  conto è sempre sul formato più piccolo, così non sembra più conveniente di
  quello che è.
- La pescheria (pagina 11 di `pam24`) è divisa in due settimane: quattro
  offerte valgono dal 24 al 30 settembre, quattro dall'1 al 7 ottobre. Le date
  sono sulle righe (sono diverse da quelle del volantino, quindi `dati.py` non
  si ferma).
- Il Mini Babybel stampa «al kg € 2,19», che è il prezzo della confezione da
  100 g: al chilo sono 21,90. Scritto nella nota.
- Tre offerte stavano identiche in tutti e due i volantini (confettura Zuegg,
  2 Croccole Findus, minestrone Findus): scritte una volta sola, in `pam24`.
- I banchi all'etto (salumi, formaggi, pesce, carne) sono righe «all'etto»
  come quelle dell'MD: resta aperta con Manlio la questione della scritta
  «al pezzo» su quelle righe.

### Una prova da sistemare

Cercando «tonno», `prova-cerca.js` pretendeva che tutti i risultati fossero in
fila per prezzo. Ma la ricerca li divide per categoria (una fascia per ognuna),
e da oggi «tonno» trova anche la pizza tonno e cipolla del Pam, che è una
Pizza e sta in fondo nella sua fascia. La pagina era giusta, la prova no:
adesso controlla l'ordine dentro ogni fascia.

## La cima con due pallini, e il Conad — 2026-09-22 (notte)

### I due pallini

Manlio: «per 4 bottoni che ci sono in alto non devono più esserci. Rimangono
solo la possibilità di un tasto novità, e di un tasto rotondo con tanti colori
per fare cambiare i colori, e un altro rotondo con dentro scritto news su due
righe; questi tasti tondi devono essere messi accanto al titolo superiore sulla
destra». E subito dopo: «devono essere piccolini. Al limite scrivi solo N al
centro».

Quindi: due tondi da 32 px accanto al titolo. La ruota è un `conic-gradient`
di colori fissi (non le variabili del look: con un look addosso deve dire
ancora «colori»). La N è rossa piena come il vecchio tasto «Novità», e apre la
stessa pagina. «Aiuto» e «Novità app» non hanno più un tasto: le finestre
restano nel codice, perché le prove le usano e perché potrebbero tornare.

Il sottotitolo è diventato «Offerte grande distribuzione», come ha chiesto.

### Lo scorrimento alle grandi marche

«Quando si fa clic su un grande marchio la pagina scrolli per far vedere in
alto i risultati.» Con 46 pillole il pannello occupa uno schermo intero, e le
offerte della marca toccata comparivano sotto, dove non le guardava nessuno.
Adesso, dopo il tocco, `scrollIntoView` porta in cima la riga «N offerte…».

### La versione di prova

«Prova a farne anche una versione con i due tasti, cerca un prodotto o una
marca e grandi marche, messe sotto le categorie.» Non l'ho fatta come
artifact separato: un artifact nuovo ha un indirizzo suo e **una lista di
prodotti sua**, quindi lui l'avrebbe vista vuota o diversa e il confronto non
sarebbe stato alla pari. È invece `prova-tasti-sotto.html` sullo stesso sito:
stesso indirizzo di casa, stessa lista. La fa `variante.py` spostando una
riga di `out/sito.html`. Si butta appena lui sceglie.

### Il Conad

«Ops mi spiace dirlo ma a Torino c'è anche Conad.»

**Quale.** Il cercanegozi di conad.it, con «Corso Siracusa 100, Torino»,
mette in fila: Conad via Cesana 78 (2,7 km), Conad City via Bardonecchia 5/c
(3,3 km), Conad corso Telesio (3,6 km), Conad City corso Francia 31/b... In
Piemonte ci sono volantini diversi per Conad, Conad City e Superstore, quindi
il negozio conta: si è preso il Conad «normale» più vicino, via Cesana.
L'ultima pagina del volantino elenca i negozi dove vale, e via Cesana 78 c'è.

**La fonte è Conad stesso.** La scheda del negozio
(`conad.it/ricerca-negozi/conad-via-cesana-78-10139-torino--009843`) si scarica
con un `curl` normale e dentro ci sono gli indirizzi dei PDF:

    https://www.conad.it/assets/common/volantini/cno/v20262/20262620PCONADPIEMONTE.pdf
    https://www.conad.it/assets/common/volantini/cno/vperch/PERCHECONVIENEPPN20PI.pdf

Il primo è il volantino (24 pagine, 24 settembre-7 ottobre), il secondo un
foglio «Perché conviene» che ripete tre sue offerte. È la prima insegna presa
direttamente da chi il volantino lo fa, in PDF: `scarica.py` ha imparato a
scaricare il PDF una volta sola e a farne le immagini delle pagine (serve
`pymupdf`, che c'è). Il collegamento di ogni riga porta al PDF sul sito Conad,
alla sua pagina (`#page=n`).

**Com'è fatto.** «Solo titolari» è la Carta Insieme Conad (segnata riga per
riga col prezzo senza tessera). «Bassi e fissi» sono prezzi fissi di Conad, non
promozioni. Tante offerte «vari tipi, un esempio: …»: il prezzo è scritto
sull'esempio, e la nota lo dice. La pescheria vale solo nei negozi col banco.

### La Routine

Il prompt della Routine notturna nominava sette insegne e le fonti di prima
(kimbino per Ekom, niente per Pam e Conad). Riscritto con le dieci insegne e,
per ognuna, dove si trova il volantino nuovo. Più una regola: se prompt e
CLAUDE.md dicono cose diverse, vale CLAUDE.md, che è più recente.

### L'ingranaggio e la scelta dei supermercati (stessa notte)

Mezz'ora dopo, Manlio: «ci dovrebbe essere anche un tasto per scegliere i
supermercati. Appare l'elenco completo e tu scegli quello che vuoi. Si
potrebbe fare un pallino unico di configurazione che porta a una pagina con i
colori, i supermercati e le altre opzioni… No, mi sono sbagliato, ci vanno due
pallini, uno di configurazione e l'altro novità».

La scelta dei negozi era stata chiesta e rifiutata due volte il 22 mattina
(era scritto in CLAUDE.md «non si fa e non si mette»). Stavolta l'ha chiesta
lui, in chiaro: si fa, e la regola in CLAUDE.md è cambiata.

Come è fatta:
- la ruota dei colori è diventata un **ingranaggio**; apre «Configurazione»,
  una finestra come quelle di Aiuto e Look;
- dentro, i dieci **marchi** in fila: pieni con la spunta verde quelli tenuti,
  grigi e tratteggiati quelli tolti; sotto, «Colori della pagina», «Aiuto» e
  «Cosa c'è di nuovo», che prima erano tasti in cima;
- la scelta sta nel telefono (`spesa.negozi.v1`) e si ricordano i negozi
  **tolti**: un'insegna nuova (com'erano Pam e Conad) compare da sola a tutti;
- la pagina tratta un'offerta di un negozio tolto come una scaduta: la regola
  sta in un posto solo (`nascosta`) e vale per prezzi, «il meno caro»,
  ricerca e grandi marche senza toccare nient'altro;
- non si possono togliere tutti: all'ultimo compare «Almeno un supermercato
  deve restare».

I pallini e lo scorrimento delle grandi marche, che lui diceva di non vedere,
erano già online dalle 23:33: li aveva guardati prima della pubblicazione.

## Il controllo del 23 settembre: niente da leggere, ma due bug trovati

Giro di routine: tutte e dieci le insegne controllate sulla fonte, nessun
volantino nuovo che non fosse già in `dati.py`. Il lavoro vero è stato pulire
`eurospin10` e `md08` (scaduti da tre giorni, coperti da `eurospin24` e
`md22` senza buchi) e sistemare due bug trovati facendolo.

**Il cerchietto dei giorni, sull'ultimo giorno, non si spiegava al tocco
lungo.** `pagina.py`, funzione `cerchioGiorni`: quando `resta === 1` il
`title` era `'Ultimo giorno: scade oggi'`, senza nessuna cifra dentro. La
prova `prova-giorni.js` controlla `/\d/.test(cer.title)` — vuole sempre un
numero — e non l'aveva mai beccato perché non era mai capitato, in una prova,
che un'offerta scadesse esattamente oggi. Oggi ne scadevano tre insieme
(bennet10, lidl17, lidlfv17) e la prova ha finalmente trovato il buco.
Corretto aggiungendo la data anche lì: `'Ultimo giorno: scade oggi, ' +
soloGiorno(o.fino)`.

**`variante.py` guardava nel posto sbagliato.** Cercava e scriveva sempre
dentro `strumenti/out/` (la cartella dello script stesso, presa con
`os.path.dirname(os.path.abspath(__file__))`), invece che in `out/` dentro
la cartella da cui si lancia il comando — cosa che fanno tutti gli altri
script (`pagina.py`, `novita.py`, `stampa.py` usano un `out/` relativo). La
routine gira da `/tmp/lavoro`, quindi `python3 -m variante` falliva sempre
con «file non trovato» finché non si lanciava da un posto preciso dentro il
repository. Tolto il `QUI` sbagliato, ora usa `out/` come gli altri.

Guardati anche, e lasciati fuori, due volantini Ipercoop non alimentari
trovati interrogando gli id vicini a quello letto («Extra offerte», 28831):
28792 «Tendenze d'Autunno» (abbigliamento ed elettronica Expert, dal 24
settembre al 21 ottobre) e 28868 «Grandi marche a tasso zero» (finanziamenti
Expert). Stesso motivo delle «Grandi Marche Selection» di Ipercoop già viste:
niente prezzo di spesa vera.

## Il volantino Conad si apriva intero — 2026-09-23

Manlio: «il volantino Conad non fa vedere la pagina ma il volantino completo».
Il collegamento di ogni riga Conad era il PDF sul sito Conad con `#page=n`:
sul computer il visore dei PDF salta alla pagina, sul telefono no — il PDF si
apre dall'inizio, o si scarica. Il numero di pagina si perdeva.

La pagina del volantino su conad.it («Guarda il volantino») mostra le pagine
con Yumpu, e i suoi tasti di condivisione portano a
`https://volantini.conad.it/volantino-freschi-di-convenienza-conad-piemonte/71286440`.
Lì ogni pagina ha un indirizzo suo, `.../71286440/5`: provato con un browser
da telefono, apre la pagina 5 (affiancata alla 4, come nel volantino di carta).

Quindi adesso le due cose stanno separate: in `VOLANTINI` l'indirizzo del
visore, per chi apre dal telefono; in `PDF` (sempre in `dati.py`) il PDF da cui
`scarica.py` fa le immagini per leggerle. È anche più pulito dal lato del
copyright: il collegamento porta al visore ufficiale di Conad.

## Marchi, cerchietti e icone alla stessa altezza — 2026-09-23

Manlio: «porta le pillole dei marchi alla dimensione del cerchio dei giorni e
del volantino che hanno di fianco in altezza; inoltre per le promozioni non
ancora iniziate cerca di fare stare il numero del giorno e la sigla del mese
all'interno del cerchio in modo che abbia sempre la stessa altezza».

- La pillola del marchio era più alta del cerchietto (imbottitura sopra e
  sotto più il logo). Adesso dentro `.coda` è alta 30 px fissi, come
  l'anello dei giorni e l'icona del volantino; il logo è alto 21 px.
- Il tondino «parte il…» aveva il numero dentro l'anello e il mese sotto,
  fuori: era alto più degli altri e la riga ballava. Adesso numero e mese sono
  in `.dentro`, una colonna centrata sopra l'anello (numero 11,5 px, mese
  7 px). Misurato col browser su tutte le offerte che partono il 24: il testo
  sta da 5 px sotto il bordo alto a 6 px sopra quello basso.
- `prova-giorni.js` legge ancora `.num` e `.mese`: le classi sono rimaste.

## Via la versione coi tasti sotto — 2026-09-23

Manlio, dopo averle guardate tutte e due: «lascia perdere la versione con i
tasti sotto, elimina completamente». Resta la pagina com'era, coi due tasti
sopra le categorie. Cancellati `prova-tasti-sotto.html` dal sito e
`strumenti/variante.py`; tolti i due passi dalle istruzioni e dalla Routine.
