# Spesa — offerte dei supermercati

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

## La pagina delle novità — fatta, poi messa via

Fatta il 2026-09-05 e **tolta lo stesso giorno**, su richiesta di Manlio: «sono
andato a vedere la pagina novità ed è vuota per adesso, lasciala perdere e
togli anche il pulsante». Aveva ragione — il diario era partito quella mattina,
e una pagina che non ha niente da dire è solo un tasto in più.

**`novita.py` e il diario restano.** `storia.py` continua a segnare cosa cambia
a ogni giro, quindi quando la pagina tornerà avrà una storia vera da
raccontare invece di ricominciare da zero. Per rimetterla: `python3 -m novita`,
copiare `out/novita.html` nel progetto, rimettere il tasto `.novita` nella riga
in alto di `pagina.py` e il file nell'elenco di `sw.js`.

Quello che segue è come è fatta, per quando servirà.


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

E `quanto()` conta anche i cambi di padrone, non solo le offerte che si
muovono: il più conveniente può cambiare **senza che nessuna offerta cambi**,
semplicemente perché quella di ieri è scaduta stanotte. Senza contarlo, il
giorno in cui scade il volantino dell'Eurospin il diario direbbe «niente di
nuovo».

**Una pagina vuota non si può giudicare.** Il diario è partito oggi, quindi non
c'era niente da mostrare: per guardarla davvero le ho costruito un diario finto
con offerte vere — un volantino che arriva, due prezzi che si muovono, un
capovolgimento — e poi l'ho cancellato.

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

## Se un domani diventa un'app

Manlio non legge codice e verifica tutto aprendo una pagina sul telefono, quindi
il naturale seguito è una paginetta come la Palestra. **Il telefono non può
scaricarsi i volantini da solo**: i siti dei supermercati non concedono CORS e
servirebbe una libreria per i PDF che in negozio, senza rete, non si carica.
I dati vanno scritti qui dentro da Claude quando i volantini cambiano, e la
pagina si limita a mostrarli.
