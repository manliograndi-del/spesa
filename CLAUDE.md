# Spesa — memoria di progetto

Leggi tutto questo file prima di toccare qualsiasi cosa. È corto apposta.

- **Questo file descrive com'è il progetto OGGI**, non come ci si è arrivati.
- **Il perché delle scelte** sta in `NOTE.md`. Leggilo **prima di rifare qualcosa
  che sembra mancare**: quasi sempre è già stato provato, e c'è scritto com'è
  andata.
- **Chi ha chiesto cosa e quando, versione per versione**, sta in
  `archivio/CLAUDE-fino-al-2026-09-24.md`, cioè il vecchio `CLAUDE.md` copiato
  identico, e poi in `registro.txt`. Vai lì quando una regola qui ti sembra
  strana e vuoi sapere com'è nata.
- **Come si tiene questo file.** Quando una cosa è fatta, la togli da «Da fare»
  e scrivi una riga in `registro.txt`. Se il lavoro ha cambiato una regola,
  riscrivi la regola al presente: niente «(TOLTA il…)», niente «dal 23 sera».
  Se c'è una storia da raccontare, va in `NOTE.md`.
- **`AGENTS.md` è una copia identica di questo file** e serve ad Antigravity,
  l'altro programma che Manlio prova. Ogni volta che cambi questo file fai
  `cp CLAUDE.md AGENTS.md`.

## Chi è l'utente e come lavora

Manlio. **Non legge il codice e non usa il terminale.** Verifica il lavoro in un
solo modo: apre l'indirizzo sul telefono (un Android: le prove in Chromium
valgono anche per lui) e guarda se l'app fa quello che deve.

- **Spiegagli cosa cambia PER LUI, non cosa hai fatto tu.** Quanto lavoro è
  costato non è un risultato. Una volta gli ho raccontato pagine lette,
  controlli e percentuali, e lui: «io ti ho chiesto di migliorare
  un'applicazione».
- Non chiedergli di leggere un diff, un file o un numero di riga.
- Per lui un file in una cartella temporanea **non esiste**: se deve averlo,
  gli serve un indirizzo pubblico.
- Detta al telefono frasi brevi, a volte con parole storpiate. Vuole
  risultati, non il racconto delle prove. Per le modifiche grafiche gli
  bastano 3 o 4 schermate (mandate con SendUserFile) prima di pubblicare.
- Scrivi in italiano. Non lasciare mai il repository in uno stato che non
  funziona fra una sessione e l'altra.
- **I testi che ha scritto lui** (fumetti, Aiuto) non si cambiano senza
  chiederglielo.

## Cos'è e dove sta

Una pagina che cerca i prodotti che interessano a lui nei volantini dei
supermercati vicini a casa (Torino, corso Siracusa). Ogni prodotto è un tasto:
lo tocchi ed escono le offerte, dalla più conveniente in giù, col prezzo per
unità. I prodotti si scelgono da un catalogo diviso per reparti.

Si pubblica in due posti, **e vanno aggiornati tutti e due**:
- il sito, `https://manliograndi-del.github.io/spesa/`, con un commit su `main`;
- il link Claude, cioè l'artifact
  `https://claude.ai/code/artifact/a6782ea0-6822-4026-87e7-705012966595`
  (lo usa anche sua moglie, e ci vive la lista condivisa). Si aggiorna con
  `Artifact`, `file_path` = `out/pagina.html` e lo stesso `url`.

**GitHub Pages pubblica solo da `main`.** Claude Code lavora spesso su un ramo
assegnato dalla sessione: se fai commit e push lì il sito NON cambia, anche se
le prove passano. È successo due volte (17 e 23 settembre). **Prima di dire
«pubblicato»:** `git push origin HEAD:main` (fast-forward, sicuro), poi scarica
`https://manliograndi-del.github.io/spesa/index.html?<numero a caso>` e
confrontalo byte per byte col file appena pubblicato. Che il push sia riuscito
non basta.

## Vincoli tecnici — non si cambiano senza chiederglielo

1. **I prezzi si leggono a occhio dalle pagine dei volantini.** L'OCR non legge
   le scritte grandi: serve solo a trovare la pagina. I riassunti che si
   trovano online sbagliano (tre errori documentati in NOTE.md).
2. **Non si pubblicano i PDF né le immagini dei volantini**, solo collegamenti
   ai siti di chi li pubblica.
3. **Il tag di chiusura dello script non si scrive mai per intero** dentro il
   codice della pagina, nemmeno nei commenti: spezza la pagina a metà senza
   nessun errore visibile.
4. **Nel CSS non esiste `prefers-color-scheme: dark`.** Il telefono di Manlio è
   in modalità notte e la pagina gli si apriva nera.
5. **Prima di rigenerare si legge la lista viva dalla pagina pubblicata**
   (Artifact `read` con `path` = `index.html`, poi `python3 -m lista_attuale
   <file>`). Se non si riesce, o la lista esce vuota, ci si ferma e non si
   pubblica: rigenerare a vuoto cancella la loro lista di prodotti.
6. **A ogni rilascio si alza il numero di cache in `sw.js`** (`spesa-v110` →
   `spesa-v111`), se no resta in giro la copia vecchia.
7. Il progetto della palestra (`manliograndi-del/palestra`) **non si tocca**.
8. **`index.html` è generato**: non si modifica a mano, perché alla
   rigenerazione successiva la modifica sparisce. Si cambia `pagina.py`.

## Come si rifà

    cd <progetto> && npm install
    apt-get install -y tesseract-ocr tesseract-ocr-ita
    export PYTHONPATH=<progetto>/strumenti
    python3 -m scarica <chiave>          # le pagine del volantino
    bash <progetto>/strumenti/leggi.sh   # OCR di ogni pagina
    python3 -m indice                    # aggiorna indice.json
    python3 -m pagina                    # le tre copie in out/
    python3 -m storia                    # il diario del giorno: PRIMA del commit
    python3 -m novita                    # la pagina Novità
    python3 -m stampa                    # il PDF del catalogo
    python3 -m lette [chiave]            # quante pagine lette / quali mai aperte
    python3 -m pulisci [--fai]           # cosa scade / toglie lo scaduto
    bash <progetto>/strumenti/prove.sh   # TUTTE le prove
    python3 -m pulizia out/sito.html     # codice rimasto in giro
    python3 -m registro "testo"          # una riga in registro.txt
    python3 -m prezzi [--tutto]          # l'archivio dei prezzi (lo fa già storia)

Poi `cp out/sito.html index.html`, `cp out/novita.html novita.html`,
`cp out/catalogo.pdf catalogo.pdf`, alzi `sw.js`, fai commit e push su `main`,
verifichi byte per byte e ripubblichi l'artifact.

- **`prove.sh` è il comando che conta: una pagina che non passa non si
  pubblica.** Una prova può fallire perché è cambiato il calendario e non per
  un guasto (il 24 settembre nessun volantino era «in arrivo»). Prima di
  correggere la prova controlla nel codice quale dei due casi è.
- **`python3 -m storia` va lanciato prima del commit**: confronta l'ultimo
  commit con quello che c'è nella cartella. `storia/stato.json` resta fuori dal
  repository («le fotografie no, le differenze sì»; `.gitignore` non si tocca).
  Se manca, `storia.py` rifà la fotografia da git (`fotografia()` sul `dati.py`
  dell'ultimo commit) e riempie uno per uno i giorni rimasti indietro, ognuno
  col `dati.py` di quel giorno. Un giorno può avere novità vere anche senza
  prezzi nuovi, perché a mezzanotte scade un volantino e il meno caro cambia.
  **`stessa()` confronta i nomi per parole in ordine alfabetico**: senza questo
  controllo, spostare la marca in un nome produrrebbe una «sparita» più una
  «nuova», cioè una novità falsa.
- `python3 -m pagina` fa tre copie: `out/sito.html` (il sito, con Umami),
  `out/pagina.html` (il link Claude) e `out/spesa-da-sola.html` (si apre con
  un doppio clic, senza rete).

**Quale prova controlla cosa** (quando cambi una regola, aggiorna la sua prova):
`prova.js` in generale e mappa/benvenuto · `prova-mappa.js` i fumetti (con un
telefono finto, perché jsdom non impagina) · `prova-intestazione.js` la banda,
il benvenuto, niente «i» · `prova-marche.js` Grandi marche, l'ordine del menù,
la griglia che sale e scende, la tastiera · `prova-multinazionali.js` le 14
ditte · `prova-personale.js` il carrello e l'ordine del menù ·
`prova-meno-caro.js` verde, sbiadite, riga del formato nascosta, nessun numero
scritto due volte (`.p2` mai uguale al prezzo grande) · `prova-sconto.js` ·
`prova-bollini.js` bollini e pagina del volantino sopra l'elenco ·
`prova-giorni.js` il cerchietto (vuole sempre una cifra) · `prova-sintesi.js` ·
`prova-titoli.js` nessuna parola inventata o persa, nessun trattino in vista ·
`prova-negozi.js` · `prova-look.js` (rifà il contrasto di tutti e cento) ·
`prova-aiuto.js` (l'Aiuto nomina i tasti) · `prova-novita.js` la pagina Novità
· `prova-novita-pagina.js` (in «Cosa c'è di nuovo» nessun prezzo) ·
`prova-collegamenti.js` (classi `dove apri`, `target=_blank`) ·
`prova-volantini.js` · `prova-visite.js` · `prova-storia.py` ·
`prova-prezzi.js` (la pagina dei prezzi più bassi). Le prove
riconoscono il negozio da `.marchio` (non più da `.sotto b`) e i bottoni che
non sono prodotti dalla classe `agg`.

## L'archivio dei prezzi (fuori dalla Spesa)

Chiesto da Manlio il 26/9: «un database di tutti i prodotti per avere
settimana per settimana i prezzi più bassi», **fuori dalla pagina**. Sta in
`https://manliograndi-del.github.io/spesa/storia/prezzi.html` e **l'app non lo
collega**.
- `strumenti/prezzi.py` rilegge `dati.py` in ogni commit (con `git archive`),
  più la cartella di adesso; di ogni volantino vale **l'ultima copia** in cui
  compare (quella corretta). Non si legge nessun volantino in più.
- Scrive tre file in `storia/`: `prezzi.csv` (una riga per offerta: l'archivio
  vero), `prezzi.json` (ultimo commit letto e il giorno in cui è comparso ogni
  volantino) e `prezzi.html` (la pagina). **L'archivio cresce e basta**: un
  volantino che git non ha più resta nel CSV.
- **Si rifà da solo alla fine di `python3 -m storia`** (`atexit`, e se sbaglia
  lo dice e non ferma niente): il giro delle 7 aggiunge già `storia/` al
  commit, quindi la Routine non è cambiata.
- La pagina: una categoria del catalogo alla volta, le settimane da lunedì a
  domenica dalla più recente, per ognuna l'offerta più bassa per unità fra
  quelle valide almeno un giorno, più le altre quattro. **Parte dalla
  settimana del 4 settembre e si ferma a quella in corso** (prima e dopo il
  «più basso» sarebbe finto). Marche proprie dei discount nascoste come
  nell'app; «Con tessera o app» quando serve.
- Le categorie vecchie passano da `RINOMINATE`, e la carne e il pesce lavorati
  di prima del 23/9 vanno nelle loro categorie. Volantini di un'altra zona:
  `ESCLUSI`; righe sbagliate già scadute: `RIGHE_SBAGLIATE` (lì, non in git).

## La Routine giornaliera

Si chiama «Spesa — controllo giornaliero dei volantini». Le istruzioni passo
per passo (traccia nel registro, cosa scade, cosa è uscito, i tre casi, fonti,
pubblicazione, messaggio) stanno nel suo prompt, non qui. **Se questo file e il
prompt non dicono la stessa cosa, vale questo file.**

- Il cron è **in UTC**: `0 5 * * *` fa partire la Routine alle 7 italiane con
  l'ora legale. **Il 25 ottobre 2026 torna l'ora solare**: quel giorno va
  rimesso `0 6 * * *` con `update_trigger`. L'ultima domenica di marzo si fa il
  contrario.
- Dal 10 settembre la Routine arriva in fondo quasi sempre. Un «pubblicato» nel
  registro però non basta: controlla sempre che il lavoro sia arrivato su `main`.

## Insegne, negozi e fonti

Sono **tredici** (Penny, Aldi ed Esselunga aggiunte il 26/9, chieste da
Manlio). L'elenco vero è `VOLANTINI` in `dati.py`, e i
volantini annunciati ma non ancora letti stanno in `VOLANTINI_ATTESI` (in
tabella «prezzi non ancora letti»). Da lì si tolgono appena entrano in
`VOLANTINI`.

| Insegna | Negozio / edizione | Fonte |
|---|---|---|
| Lidl | **ogni negozio ha il suo volantino**. I 15 Lidl di Torino (il più vicino: **via Monfalcone 92**, IT00516, 600 m) hanno la versione **«KA»** più lo speciale **«Fresca e conveniente»**; la versione «NAZ» ha prezzi diversi (ali di pollo 1,69 invece di 1,45) | **ufficiale (trovata il 24/9, da usare)**: `https://endpoints.leaflets.schwarz/v4/overview?client_locale=lidl/it-IT` elenca tutti i volantini con i negozi (`regions`: `store` = IT00xxx, `offer_region`); il dettaglio è `…/v4/flyer?flyer_identifier=<slug>&client=lidl`: date, PDF, **immagini delle pagine** (`imgproxy.leaflets.schwarz`) e **le parole di ogni pagina** (`keyWords`). Il 24/9 la «KA» aveva 54 pagine, anteprimavolantino 52. I negozi: `https://live.api.schwarz/odj/stores-api/v2/myapi/stores-frontend/stores?country_code=IT&limit=250&offset=…` con l'header `x-apikey` scritto nella pagina del sito Lidl (`/s/storesearch-frontend/…/base.js`). Finora: anteprimavolantino.it (la versione giusta, KA) |
| Eurospin | **ogni negozio ha il suo volantino**. Il più vicino: **via Rio de Janeiro 25** (codice 100029, alias `torino-7`, 1,7 km) | **ufficiale (trovata il 24/9, da usare)**: il visore `digitalflyer.eurospin.it`. Token: POST `/oauth/token` (`grant_type=client_credentials`, `scope=read write`) con l'utente/password scritti nel codice della pagina (`apiAuthorizationCode`); poi `/api/eurospin/eurospin-italia/stores/torino-7/promotions` → `…/promotions/<alias>/contents-light?typeCode=FLY` → il **PDF** `https://digitalflyer.eurospin.it/files/<uniqueId>/<name>`, **col testo dentro** (prezzi compresi). Il 24/9: uguale a quello letto (22 pagine). Finora: anteprimavolantino.it |
| MD | **ogni negozio ha l'edizione della sua zona, e a Torino ce ne sono quattro**: «nord-atm-na-gastro» (**corso Sebastopoli 227/A**, id 1147, **300 m**), «nord-atm-gastro» (via Gorizia 148/A, 700 m), «nord-macel-gastro» e «nord-macel-na-gastro» (quelle con la macelleria al banco). **Quella letta da anteprimavolantino il 18/9 non è nessuna delle quattro**: macelleria, una pagina intera di gastronomia, frittelle, pomodori/patate e una birra non sono quelli di corso Sebastopoli | **ufficiale (trovata il 24/9, da usare)**: POST `https://www.mdspa.it/punti_vendita_admin/get_pv.php` con `pv=<id>` → `zonanome`; il PDF è `https://www.mdspa.it/cdn/upload/presente/volantini/<zonanome>/volantino.pdf` (senza testo: si legge a occhio). I negozi vicini: `…/punti_vendita_admin/listnew.php?latitudine=…&longitudine=…&luogocercare=Torino`. **Dal 25/9 `md22` è l'edizione di corso Sebastopoli** (36 pagine): il PDF sta in `PDF` di `dati.py` e le pagine si aprono dalle immagini ufficiali `volantino.mdspa.it/volantino/<numero>/md-volantino-page-{n}.jpg` (il numero, 3557 per il 22/9, sta nella pagina `volantino.mdspa.it/nord_atm_nogas.html`, che è la stessa edizione) |
| Bennet | **non tutti i volantini Bennet sono nazionali**: «14 Giorni Mai Visti» (24/9-7/10) è SOLO LOMBARDIA (retro-copertina: Albano S. Alessandro, Antegnate, Brugherio, Cantù, Lecco… zero Piemonte), scoperto e scartato il 25/9. A Torino: **via San Paolo** (0009) e via G. Bruno (0113), volantino attivo confermato «Un mondo di bellezza» (bennet1709, 17-30/9, già letto) | **ufficiale (trovata il 24/9, non ancora usata)**: `www.bennet.com/flyer`, **solo con un browser vero** (a un curl risponde «Access Denied»; anche il selettore negozio `bennet.com/storefinder/...` ha dato 403 il 25/9). I volantini sono PDF col testo dentro su `bennet-cdn.thron.com/delivery/public/document/bennet/<id>/c82oyu/WEB/volantino`; lo stesso volantino c'è anche su `nativa.bennet.volantinopiu.com/volantino<id>00.html`. **trovavolantini.it** cercato per nome negozio («Torino Via San Paolo») ha confermato il volantino giusto il 25/9. Finora: anteprimavolantino.it — **controllare SEMPRE l'ultima pagina (elenco punti vendita) prima di leggere un volantino Bennet trovato lì**: pesca anche edizioni di altre regioni. Anche **bennet.com/flyer mostra i volantini di tutte le regioni senza dire dove valgono**: la prova è solo l'elenco dei negozi in fondo al PDF. «Offerte Extra» (`bennetextra24`, «valida in tutti i Bennet») è letto dal PDF ufficiale, che il `…/document/…/volantino` rimanda a `bennet-cdn.thron.com/static/<nome>.pdf`: quell'indirizzo, con `#page={n}`, è anche il collegamento delle righe (non ci sono immagini delle pagine) |
| Carrefour Iper | **i negozi di Torino** (corso Montecucco 108, corso Turati 75, Grugliasco via Crea 10…) **hanno l'edizione PIEMONTE**. Quella letta il 15/9 da anteprimavolantino era l'edizione **LOMBARDIA** («Il meglio della Lombardia»): una decina di pagine con prodotti o prezzi diversi, e **in Piemonte «Grandi Marche» finisce il 25/9, non il 28** | **ufficiale (trovata il 24/9, da usare)**: `https://www.carrefour.it/volantino/<negozio>/<codice>` (il codice sta in `UrlVolantini` di `…/StoreLocator-GetAll`) elenca i volantini con le date; le pagine: `…/Volantini-Pages?storeId=I001&editionId=<id>&endDate=…` → immagini `gdodig-car.youroperator.it/volantini/iper_…/…_02_PIEMONTE/mobile/…_<n>_sliderzoom.jpg`. La stessa pagina ha anche **l'elenco delle offerte scritto** (prodotto e prezzo). Il 24/9 era già uscito il successore: **«50 prodotti al 50%» dal 29/9 al 12/10**, più «Speciale Coca-Cola», «Speciale Aia», «Speciale Unilever» e «Punti Sprint Payback». **Dal 25/9 `carriper15` è l'edizione Piemonte** e le sue pagine si aprono dalle immagini ufficiali. **Il PDF di ogni edizione, col testo dentro**: `gdodig-car.youroperator.it/api/v1/geteditions/dwnpdfedition.php?id_edizione=<editionId>` (così sono stati letti `carriper29` e gli speciali). Gli speciali (Coca-Cola, Unilever, Aia) hanno una sola edizione per tutti, anche se la cartella si chiama LOMBARDIA |
| Mercatò | **via Filadelfia 232, Mercatò semplice** (confermato da lui). Il più vicino è un Mercatò Local, che ha un volantino diverso | **ufficiale (trovata il 24/9, da usare)**: la pagina del negozio `https://www.mymercato.it/punti-vendita/piemonte/mercato-torino-via-filadelfia` contiene l'elenco `flyers` (titolo, date, PDF su `cdn.dimar.it/volantini/<id>/<id>_volantino.pdf`, col testo dentro). Il 24/9: «Al costo conviene sempre» (17-30/9, 20 pagine, uguale a quello letto) e «Promo L'Oréal» (17-30/9, 2 pagine), letta il 25/9 (`mercatoreal17`: collegamento al PDF con `#page={n}`). Il volantino principale finora: kimbino.it, indirizzi firmati in `strumenti/pagine_mercato.py` |
| Ekom | il volantino è uguale in tutta Torino (diversa solo la Toscana). **A volte esce su carta prima che online** | **il sito ufficiale** `ekomdiscount.it/volantini` (l'ha segnalato Manlio), non kimbino. La pagina vuole un browser vero, ma l'API si legge con un curl normale: `ekomdiscount.it/ebsn/api/leaflet/search?parent_leaflet_type_id=1` → `{baseLocation}{n}.png`, n da 0. Indirizzi in `strumenti/pagine_ekom.py`, da rifare a ogni volantino |
| Ipercoop (Nova Coop) | Nova Coop stampa **14 edizioni**, una per zona, con qualche prezzo diverso. La nostra è **«TORINO - COLLEGNO»**, scritta sul frontespizio (id 28831 per il 24/9). L'elenco completo è nel commento di `VOLANTINI` | volantinopiu. **Il nuovo esiste prima che l'elenco del negozio lo mostri**: si provano gli id uno per uno su `ipercoop.volantinopiu.com/volantino<id>00pv24.html` (`<title>` e date). `promoipercoop.it` è il sito sbagliato |
| Pam | **corso Orbassano 212** (store 71, pv 2311), un «PAM Supermercati». **Non i «PAM Panorama»**: id vicini, prezzi diversi. Di solito due volantini per periodo, il principale e «Occasioni Extra» | elenco per negozio: POST `https://coeus.ppapi.it/api/v2_2/post/query?noCache=1&typeUuid=flyer` con `typeUuid=flyer&fields[0]=slug&fields[1]=name&limit=30&orders[publishedAt]=desc&relationshipQueries[flyer_store][$in][0]=71` (header Origin/Referer `https://www.pampanorama.it`). «con APP» = solo con l'app Pam Perte Plus, e il volantino non stampa il prezzo senza app. I nuovi si trovano prima provando gli id su `pam.volantinopiu.com/volantino<id>00pv2311.html` |
| Conad | **via Cesana 78** (codice 009843), il Conad «normale» più vicino. I Conad City e i Superstore hanno volantini loro | la scheda del negozio `conad.it/ricerca-negozi/conad-via-cesana-78-10139-torino--009843` (si scarica con un curl normale), che contiene i PDF ufficiali; `scarica.py` li legge da solo. **Servono due indirizzi**: il PDF va in `PDF` dentro `dati.py` (per scaricare le pagine), il visore `volantini.conad.it/<nome>/<id>/{n}` va in `VOLANTINI` (per il collegamento: il PDF sul telefono si apre dall'inizio). Il numero del PDF avanza di uno a ogni volantino (`2026…20PCONADPIEMONTE` = 24/9-7/10). «Perché conviene» ripete il principale |
| Penny | **ogni negozio ha il suo volantino, ma a Torino cambia solo la pagina 5** (pane in alcuni, gastronomia in altri). Il nostro: **corso Corsica 7** (volantino 1693379, 1,9 km) | **ufficiale**: il visore Shopfully del sito penny.it. L'elenco per zona: `https://d3k4i39zecu9l5.cloudfront.net/v1/it_it/5b50951b-b644-4f17-9904-335fac1f50fd/flyers?lat=…&lng=…` con l'header `x-api-key: eeb8526b-4f6e-48f3-8c86-d60e8c9a6d88` (scritto nel codice del visore); il PDF, col testo dentro, è `lastPubblication.pdf_url`. **Il visore si apre sempre dalla prima pagina**, quindi le pagine si vedono da anteprimavolantino (`_PAGINE_PENNY_24` in `dati.py`), tranne la 5, che apre il PDF ufficiale. «Solo con PENNYCard» = tessera |
| Aldi | un volantino a settimana, da lunedì a domenica, uguale in tutta Italia. Accanto alle offerte stampa i prezzi fissi «dal nostro assortimento» (nella nota: «Prezzo fisso Aldi») e i «Quantità limitata» del bazar; dalla pagina 24 in poi è tutto non alimentare. Le pagine hanno dei riquadri vuoti, vuoti anche nel testo ufficiale | **ufficiale**: `volantino.aldi.it` (Publitas) rimanda al volantino in corso; `/<nome>/spreads.json` dà le pagine (`images.at1600`, da mettere dopo `https://view.publitas.com`) e `/<nome>/data.json` il PDF. aldi.it risponde 403 a un curl. Gli indirizzi stanno in `strumenti/pagine_aldi.py`. «Dal nostro assortimento» = prezzo fisso, non un'offerta |
| Esselunga | **ogni zona ha la sua edizione**: quella di anteprimavolantino è la LOMBARDA (l'ultima pagina elenca solo negozi lombardi, Parma e Piacenza; a Torino cambiano vini, formaggi, verdura e qualche prezzo). **Torino è la «Zona3»**. Il negozio preso: **corso Traiano** (TRA); a Torino ci sono anche corso Bramante (BRA) e Porta Nuova (TOP). Di solito due volantini per periodo, il principale e un catalogo | **ufficiale**: esselunga.it risponde a fatica (502 a intermittenza: si riprova) e vuole un negozio scelto. L'elenco dei volantini di un negozio: `esselunga.it/it-it/promozioni/volantini.<nome>.<codice>.html` (i link «sfoglia»). Il visore è FlippingBook: `esselunga.it/cdn/volantini/promozioni-<id>/Zona3-SS-Vol1/index.html#{n}`, che è anche il collegamento delle righe (si apre alla pagina giusta, dentro un riquadro; con `#page/{n}` si apriva alla prima). Le pagine: `…/files/assets/common/page-html5-substrates/page{nnnn}_4.jpg`, **ma su molte pagine le scritte stanno a parte**, in `…/files/assets/common/page-vectorlayers/{nnnn}.svg`: si leggono sovrapponendo le due. Controllo: `services/istituzionale35/digital-grid.condition:nav_menu.abbrev:TRA.page:0.rows:100.codPromo:<codice>.onlyInFlyer:true.json` dà le offerte del negozio col prezzo. «Sconto Fìdaty» = solo con la carta Fìdaty |

I negozi di Pam (corso Orbassano), Conad (via Cesana), Ipercoop
(Torino-Collegno) e MD (corso Sebastopoli) li ha confermati lui il 25/9 («sono
davvero i miei negozi», «per ora va bene qualsiasi cosa»).

**Dove vuole arrivare** (Manlio, 25/9): l'applicazione deve diventare **il più
generica possibile per la città di Torino**. Quali supermercati tenere, e se
mettere più volantini (più edizioni) per ciascuna insegna, lo deciderà lui più
avanti: fino ad allora non si aggiungono né tolgono insegne o edizioni di
testa propria, ma quando si sceglie come fare una cosa si preferisce la strada
che funziona per tutta Torino, non solo per corso Siracusa.

Regole comuni sulle fonti:
- **La fonte risponde 200 anche per pagine che non esistono**, con
  un'immagine da 1,2 KB: conta la dimensione, non il codice di risposta
  (`scarica.py` fa già così).
- Un volantino di **soli sconti percentuali**, senza un prezzo di partenza,
  non si usa. I volantini Ipercoop/Expert non alimentari (abbigliamento,
  elettronica, finanziamenti) restano fuori.
- Se fra il volantino vecchio e il nuovo c'è un buco di giorni, il nuovo si
  legge lo stesso in anticipo, con la data in `inizio`.
- Se Manlio manda foto di un volantino di carta, si legge da quelle: le righe
  restano senza il collegamento alla pagina.

## Come si leggono i volantini — la parte che ho sbagliato tre volte

- **Si leggono per intero, pagina per pagina.** Non si usa l'indice delle
  parole per aprire solo le pagine che rispondono: così trovi solo quello che
  hai già pensato di cercare. Le pizze, il Mercatò e il pesce sono stati lo
  stesso errore tre volte, e Manlio se n'è accorto tutte e tre da fuori.
- **Una categoria con zero o una sola offerta è quasi sempre un buco mio**, non
  il mondo.
- **Si comincia dai volantini che durano di più**, non da quelli più
  trascurati.
- **Cercare i volantini nuovi è un'altra cosa rispetto a guardare le
  scadenze.** Le insegne pubblicano volantini che si sovrappongono (il Bennet
  «Dolce Buongiorno» è rimasto invisibile per sei giorni). A ogni giro si
  guarda anche cosa è USCITO.
- **Una pagina si scarta solo dopo averla APERTA**, mai dal titolo o
  dall'OCR: così avevo perso un'intera pagina di pescheria. Le pagine scartate
  (quaderni, pubblicità, punti premio, non alimentari) vanno in
  `strumenti/scartate.py` col motivo. Regola sua: «una volta che l'hai vista,
  lasciala perdere».
- `python3 -m lette` dice quante pagine sono coperte. Ogni volantino con prezzi
  va letto al 100%.

Come si scrive una riga in `dati.py`:
- **Nome – Marca, aggiunte.** La marca va **sempre dopo « – »**: è da lì che la
  pagina la prende. Se la marca non c'è (carne, frutta, molti discount) o non
  sei sicuro che lo sia, niente trattino. Se la marca È il prodotto
  (Coca-Cola), il nome diventa la variante («Zero»); se resta vuoto non si
  divide.
- **Lo sconto si scrive nella nota come lo stampa il volantino** («−30%, prima
  3,29»): da lì nasce il bollino dello sconto.
- **Le condizioni si scrivono con le parole che `condizioni()` riconosce**, se
  no il bollino non nasce: tessera, app («solo con l'app Pam Perte Plus»), Lidl
  Plus, soci Ipercoop, MD Buona Spesa Card, carta EKOM UP, Carta Insieme Conad
  («Solo titolari»), 1+1, «più ne prendi», surgelato, al banco, non in tutti i
  negozi. **Quando c'è, nella nota va anche il prezzo senza tessera.**
- **EUROSPIN: «OFFERTA Family» e il logo «Eurospin Family» vogliono dire SOLO
  CON LA CARTA.** Nota: «Offerta Family: solo con la carta Eurospin Family,
  senza tessera 2,49.» La pagina gialla e blu «OFFERTE Family · ALTRE OFFERTE»
  si segna tutta così per prudenza («lasciale pure come le hai messe per
  sicurezza»). Vale anche per i volantini dopo.
- **1+1**: nel formato va quello che porti via («2 × 300 g (1+1)»), nella nota
  il prezzo di una confezione sola. Il perché è in NOTE.md.
- **Se un conto è ambiguo** (peso sgocciolato, prezzo valido solo comprandone
  tre, «shampoo O balsamo» con due formati allo stesso prezzo), si sceglie il
  numero che NON fa sembrare l'offerta più conveniente di quanto sia (di solito
  il formato più piccolo) e lo si scrive nella nota. **Una novità falsa è
  peggio di nessuna novità: manda uno in negozio.**
- Un prodotto venduto «al pezzo» senza peso indicato **resta fuori**: non c'è
  un prezzo per unità onesto da scrivere.
- In uno speciale (per esempio Lidl Frutta e Verdura) le offerte identiche a
  quelle del volantino generale **non si riscrivono**.
- **Le date si scrivono sulla riga SOLO se l'offerta vale per una parte del
  volantino** (weekend, «solo dal 28», pescheria Pam divisa in due settimane).
  Se una data è difficile da leggere, si sceglie la più prudente.
- Nelle righe di pescheria Eurospin va scritto nella nota che non tutti i
  punti vendita hanno la pescheria.

## Trappole già pagate: `dati.py` si ferma da solo se le rifai. Non togliere i controlli

- **Righe doppie** (stessa insegna, stesso prodotto, stesso formato).
- **Date copiate dal volantino su una riga**: la fanno passare per «offerta
  ristretta» e le mettono il bollo rosso «solo dal … al …» sbagliato.
- **Categorie che non esistono nel catalogo**: il prezzo verrebbe caricato ma
  non lo vedrebbe nessuno, e nessuno se ne accorgerebbe.
- **Carne e pesce lavorati nelle categorie del fresco.** Würstel, hamburger,
  polpette, cotolette, nuggets, spiedini, affettati al forno, pesce impanato,
  salmone affumicato e collutorio hanno categorie loro (**Würstel, Preparati,
  Affettati, Panati, Salmone affumicato, Collutorio**), mai Manzo, Vitello,
  Suino, Pollo, Tacchino, Merluzzo, Pesce, Calamari, Gamberi, Salmone o
  Dentifricio. «Cotolette e nodini» di suino sono carne fresca (l'eccezione è
  scritta lì). Carne, salmone e verdure miste **in scatola** vanno in
  **Conserve**; chorizo e capocollo stagionato in **Salame**.

## Com'è fatta la pagina oggi

### I colori vogliono dire una cosa sola
**Rosso** = «premi qui», sui tasti e sul prodotto acceso. **Verde** = il meno
caro. **Blu** = giorni che mancano; **ambra** = ultimi tre giorni. **Beige** =
condizioni. Per sconti e fumetti non si usano rosso, verde né ambra. Si tocca
solo quello che ha gli angoli arrotondati: le bande squadrate non si toccano.

### Apertura
- **La mappa «Come si usa»** (`mappaAiuto()`, `FUMETTI` in `pagina.py`) compare
  all'apertura e ogni volta che si tocca il titolo «Spesa». La griglia dei
  prodotti resta giù e nessun tasto del menù è acceso. Ci sono cinque fumetti.
  **I testi sono SUOI:** «In alto — L'ingranaggio sceglie i tuoi supermercati,
  la N le novità»; «Prodotti — Scegli le categorie di prodotti che ti
  interessano: appariranno liste di prodotti cliccabili per vedere le
  immagini»; «Cerca — Ricerca a testo libero»; «Grandi marche — Scegli per
  marca»; «Il mio carrello — Fai la tua lista della spesa».
  - Sono **a scaletta, uno per riga**: Prodotti a sinistra e Cerca a destra,
    con le code lungo i bordi; poi Grandi marche e il carrello, stretti fra le
    due code, col carrello più in basso, a destra della coda di Grandi marche.
  - **La coda esce da un lato, mai dal mezzo** (`coda`), e si assottiglia fino
    alla punta come una virgola: due curve che si chiudono (`palloncino()`).
    Dalla parte del bordo continua la curva **senza salti di direzione**, e
    quale sia quella parte lo dice la posizione, non l'ordine dei punti. Dall'altra
    parte c'è lo spigolo. Niente freccia; la punta si ferma 11 px sopra il tasto.
  - Colori giallo, verde, azzurro, lilla, pesca (`.p-alto` … `.p-per`), col
    bordo della stessa tinta più scuro e la scritta `#27231F` fissa, uguali con
    ogni look. Mai rosso.
  - `adattaMappa()` fa stare tutti i fumetti sopra il menù su ogni telefono:
    prima rimpicciolisce il testo (da 16 a 12,5 px), poi lo spazio fra i
    fumetti, poi il testo fino a 11,5. Provato da 360×640 a 412×915.
  - Il disegno (`#frecce-aiuto`) sta fermo, sotto il testo, non si tocca
    (`pointer-events:none`), si rifà quando la pagina scorre o cambia misura e
    sparisce quando si lascia la mappa.
  - «Prodotti» fa salire la griglia e porta al benvenuto. Cerca, Grandi marche
    e Il mio carrello vanno alla loro sezione. Dopo non si rivede la mappa,
    tranne toccando «Spesa».
  - **Toccare un fumetto fa quello che fa il suo tasto** (molti toccavano i
    fumetti invece dei tasti); «In alto» apre l'ingranaggio. Il testo dei
    fumetti (anche del benvenuto) **non si seleziona** (`user-select:none`).
    La prova è in `prova.js`.
- **Il benvenuto** (`benvenuto()`, `scelto = -1`, nessun prodotto acceso) è un
  fumetto verde un po' trasparente (`.p-bv`, `fill-opacity` .6, `FUMETTO_BV`
  in `frecceAiuto()`) con la coda che scende alla griglia. Testo: «Tocca un
  prodotto qui sotto» / «Escono le sue offerte, dalla più conveniente.» /
  «Tocca un'offerta per vedere la foto del volantino.» / «"Organizza i
  prodotti" sceglie quali tenere.». Se nella stessa visita si tocca di nuovo
  «Prodotti», si torna al prodotto che si stava guardando.
- **Una pagina «Oggi»** (una riga per prodotto col meno caro) è un'idea sua
  per dopo: non farla senza chiederglielo.

### In cima
- Il titolo «Spesa» (`#vai-inizio`, riporta alla mappa, anche dalla pagina
  Novità) e il sottotitolo «Offerte grande distribuzione».
- A destra **due pallini** da 32 px, bianchi col bordo:
  - l'**ingranaggio** (`#apri-config`) apre «Configurazione» (`#buio-config`):
    prima i supermercati, uno per marchio, da toccare per toglierli o
    rimetterli, poi i tasti **Colori della pagina** (`#apri-look`), **Aiuto**
    (`#apri-aiuto`) e **Cosa c'è di nuovo** (`#apri-novita-app`);
  - la **N** (`.pallino.novita`) apre la pagina Novità. Non è rossa.
- **Non ci sono più e non si rimettono**: «Torino · corso Siracusa», la
  «Data di riferimento», i quattro tasti in cima e la riga «I tuoi prodotti
  (N)». I vecchi tasti sono **nascosti con `hidden`, non tolti** (le finestre
  funzionano e le prove le aprono). Serve la regola `[hidden]{display:none}`,
  perché `hidden` da solo non vince su `display:flex`.

### Forme
Sono **rettangoli arrotondati** i tasti: 10 px per i tasti piccoli (prodotti,
catalogo, parole del carrello, «Aggiungi», «Personalizza supermercati»,
«Mostra tutte», caselle di testo, supermercati in Configurazione, grandi
marche) e 14 px per il menù e i tasti grandi («Fatto», «Ho capito»,
«Chiudi»). **Restano tondi** i bollini dentro le schede e i due pallini in alto.
Le schede hanno angoli da 16 px e il prezzo grande è da 26 px. Tutte le
finestre (Configurazione, Colori, Aiuto, Cosa c'è di nuovo, Cerca, catalogo)
stanno **fuori dalla `.barra`** e se ne apre una alla volta.

### Il menù in basso
`#riga-cerca`, `position:fixed` in fondo. **Ordine: Prodotti, Grandi marche,
Il mio carrello, Cerca.** Quattro rettangoli uguali con angoli da 14 px,
l'icona sopra la scritta, alti circa 54 px. Quello della sezione aperta è
**rosso pieno**, gli altri no. «Grandi marche» e «Il mio carrello» vanno sempre
su due righe (due `<span class="riga-gm">`). Toccare il tasto già acceso non
chiude niente: riporta in cima alla stessa sezione. Sotto i 380 px la
scritta del menù scende a 13 px. Il tasto Cerca è `.tasto.trova`.

### La griglia dei prodotti
- La `.barra` è `position:fixed` sopra il menù (`--menu-alto`): quattro caselle
  per riga, larghe uguali, testo da 13 px, alte 34 px, angoli da 10 px. Se un
  nome non ci sta lo misura `sistemaBarra()` (anche quando arriva il
  carattere): quel nome prende due caselle e va in fondo (`.lunga`, `order`).
  **I nomi non si accorciano.** L'ultima casella è sempre «+ altri prodotti /
  Organizza i prodotti».
- La griglia occupa al massimo un terzo dello schermo (dentro scorre). La
  pagina lascia in fondo lo spazio che serve (`--barra-alta`) e in cima non
  resta niente di fermo (`altaFissa()` = 0). Il prodotto acceso è rosso pieno.
- **Sale e scende** in un quarto di secondo con la classe `.giu` sulla
  `.barra`, **non con `hidden`**: il link Claude aggiunge da solo
  `[hidden]{display:none!important}` e così niente si anima. Le prove guardano
  la classe.
- Toccando «+ altri prodotti» la pagina torna in cima, dove si apre il catalogo.

### Il catalogo («Organizza i prodotti»)
- **Un prodotto si toglie spegnendolo nel catalogo.** Non c'è una casella per
  nomi nuovi. I prodotti scritti a mano in passato stanno in cima, sotto «I
  tuoi, fuori catalogo». Le cose strane si mettono in «Il mio carrello».
- **In fondo al catalogo, prima di «Fatto», ci sono i supermercati**
  (`#negozi-cat`), gli stessi della Configurazione: `disegnaNegozi()` li
  disegna in tutti e due i posti e toccarne uno lo toglie ovunque. Nella
  Configurazione restano.
- Le voci aggiunte il 23/9 (Würstel, Preparati, Affettati, Salmone
  affumicato, Collutorio) non sono nella lista di Manlio: se gli servono le
  accende lui dal catalogo. Il catalogo ha 71 voci.
- Con il testo da 13 px non ci stanno Salmone affumicato, Verdure surgelate,
  Ammorbidente, Bagnoschiuma, Carta igienica, Lavastoviglie, Asciugatutto e
  Olio di semi: prendono due caselle e non si accorciano.
- **I nomi delle categorie sono di UNA parola**, con cinque eccezioni motivate:
  Olio d'oliva, Olio di semi, Carta igienica, Verdure surgelate (diversa da
  Verdura, che è la fresca) e Salmone affumicato. «Prosciutto» vale per crudo e
  cotto. «Panati» comprende bastoncini, croccole, fishburger, fritto misto e
  tempura.
- **La tabella `RINOMINATE` in `catalogo.py` non si cancella mai.** I nomi
  vecchi sono salvati nei telefoni di Manlio e di sua moglie, e anche
  `storia.py` la usa (senza, 393 offerte «cambierebbero reparto», che sarebbe
  una novità falsa). Il riaggancio avviene per nome e per parole del volantino
  (per questo fra le parole del pesce manca apposta «pesce»). I prodotti che
  qualcuno ha rinominato a modo suo non vengono toccati.
- **Le `parole` con cui si cerca nei volantini non si toccano**: il nome corto
  serve solo al bottone.
- Manlio deve correggere a penna `catalogo.pdf`. Quando manda le correzioni si
  riportano in `strumenti/catalogo.py` e si rifà il PDF con `python3 -m stampa`.

### Le offerte di un prodotto
- Sopra c'è **solo una banda rossa bassa** (`.banda` in `disegna()`, ~24 px,
  larga quanto lo schermo, squadrata) col nome in bianco al centro. Niente «i»,
  niente scritte, niente tasti.
- **La riga di sintesi** (`sintesi()`) c'è **solo se la scheda verde non è fra
  le prime tre**: al massimo due righe-tasto, una verde «Oggi il meno caro: MD,
  16,90 € al kg» e una blu «Da domani conviene di più: …» (o «dopodomani», o
  «giovedì 25»). Toccandole si scende alla loro scheda.
- **Ordine di prezzo e basta**, senza eccezioni in fondo. **Il bollino verde e
  la scheda verde** (`.prezzo-riga.vince`: fondo `--pannello`, bordo verde) vanno
  **una volta sola, al meno caro che si può comprare OGGI**, che non sempre è la
  prima riga. **Non c'è un riquadro separato in cima** e non va rimesso.
- **Le offerte non ancora cominciate sono sbiadite, non nascoste**
  (`.prezzo-riga.dopo`, `opacity:.82`, prezzo in grigio `--tenue`). Anche
  quelle valide solo in una parte del volantino, col bollo rosso «solo dal … al
  …». Prima del loro giorno non sono mai «il meno caro».
- Le offerte scadute spariscono da sole. **Decide la data del telefono di chi
  guarda**, non il programma.
- Un prodotto senza offerte ha una riga sola: «Nei volantini di adesso non ci
  sono offerte per questo prodotto» (oppure «…sono tutti scaduti…»). **Sotto
  le offerte non c'è l'elenco delle pagine** che nominano il prodotto, e le
  parole delle pagine non entrano nella pagina.

### La scheda di un'offerta (`.prezzo-riga`)
- **In alto a sinistra** (`.coda`): il **marchio** del negozio (`.marchio`), il
  **cerchietto dei giorni**, lo **sconto**. Tutte le pillole della scheda sono
  alte 24 px (logo 17 px).
  - Cerchietto: **conta oggi compreso**, quindi l'ultimo giorno dice «1 oggi» e
    mai «0». Blu, ambra negli ultimi tre giorni. Al tocco lungo dice anche la
    data.
  - Le offerte non ancora cominciate hanno al suo posto il **calendarietto**
    (`.parte .cal`: striscia blu col mese, sotto il giorno).
  - **Sconto** (`sconto()`, `.angolo .sconto`): la percentuale stampata, o calcolata da «Prima
    2,99». **Mai** se il «prima» è al kg o all'etto, né sui 1+1. «Senza tessera»
    non è uno sconto. Pastiglia scura; il «prima» sta nel `title`.
- **Il titolo** (`titolo()`): sopra, in maiuscoletto scuro, la **marca**; poi il
  nome (peso 500, non grassetto); poi in grigio le aggiunte, che se sono corte
  non vanno a capo a metà. Non si ripete quello che la scheda dice già (al
  banco, 3+1, il peso). **Le marche proprie dei discount non si scrivono**
  (Milbona, Sol&Mar, Il Podere, La Fattoria, Sapor di Cascina…: l'elenco è
  `MARCHE_PROPRIE` in `marche_proprie.py`, per insegna; nel dubbio una marca resta).
  Le marche proprie dei supermercati (Esselunga, Conad, Coop…) e quelle
  dell'Ekom restano: non le ha chieste. Nella pagina vanno `marca`, `nome` e `agg`; **`pro`
  resta intero** perché Cerca e Grandi marche cercano lì.
- **Bollini delle condizioni** (`condizioni()`): Con tessera, Al banco,
  Surgelato (non nelle categorie surgelate), 1+1, Più ne prendi, Non in tutti
  i negozi, Con carta Family. «Con tessera» si scrive con la parola
  dell'insegna: Pam «Solo con app», Lidl «Con Lidl Plus», Ipercoop «Solo
  soci». «Al banco» non compare se lo dice già il formato. **Pillole beige**
  (`brevi()`, peso 600), solo cose importanti e brevi: «Senza tessera 3,49 €»
  (con l'unità se la nota ce l'ha: «… € al kg»), cos'è davvero il prodotto (al massimo 26
  caratteri e mai se è già nel nome), Peso (non) sgocciolato, «Una sola 1,79
  €», Quantità limitata. **Mai il prezzo all'etto** (è un numero ripetuto). La
  nota intera resta nei dati e non si mostra: **niente «Dettagli»**.
- **I prezzi stanno a destra, a metà altezza della scheda, uno sopra l'altro**:
  sopra quello per unità («8,69/kg», `unitaCorta()`), sotto la confezione
  (`.val .p2`, «1,39 · 160 g», solo la prima parte del formato, tagliata a «, »
  o « (» e mai alla virgola dei decimali). **Niente «€» sulle schede**
  (resta nelle frasi e nelle pillole). **Se i due numeri sono uguali** (cose
  sfuse, al banco) **il secondo non si scrive**: il confronto si fa sui numeri
  come sono scritti (`eur`). Sulle offerte sfuse (`FORMATO_BANALE`) il peso non
  si scrive. Il grassetto pieno è solo per i prezzi.
- La riga «Formato · fino al» (`.sotto`) è `.solo-voce`: la leggono solo il
  lettore di schermo e le prove.
- **Toccando la scheda in qualunque punto** (`.apribile`) si apre **la pagina
  del volantino sopra l'elenco** (`#vol-sopra`): in cima insegna, numero di
  pagina e «Apri sul sito»; in basso il tasto rosso **«Chiudi»** (58 px,
  sempre in vista). Chiudono anche il tasto indietro del telefono
  (`pushState`/`popstate`) ed Esc. L'immagine viene dal sito di chi pubblica
  (vincolo 2); per il Conad c'è il suo visore in un riquadro. I volantini che
  esistono solo in PDF (Bennet «Offerte Extra», Mercatò «Promo L'Oréal»:
  indirizzo `….pdf#page={n}`) non si vedono qui dentro: compare «Questo
  volantino c’è solo in PDF…» col tasto bianco «Aprilo alla pagina N», che
  apre il PDF fuori alla pagina giusta. Se l'immagine non arriva compare
  «Aprila sul sito». Il foglietto rosso non si vede più; `dove(o)`
  serve solo quando manca l'indirizzo della pagina, e il collegamento vero
  tiene `target=_blank`.

### Cerca
Cerca fra **tutte** le offerte lette (marca, formato, insegna, note), non nel
catalogo. I risultati escono mentre si scrive. La pagina contiene solo la
casella: niente categorie, niente scritte sotto, niente «Fatto» (è nascosto
perché lo usano le prove). Nei risultati (anche di Grandi marche) il nome di
ogni categoria (`.fascia`) è nel colore del testo, non nel grigio tenue. **Nei risultati non c'è il verde.** Il pannello sta
**fuori dalla `.barra`**: se le cresce dentro qualcosa, il telefono si blocca a
ogni scorrimento. Due pannelli non stanno aperti insieme. La casella prende il
fuoco (e si apre la tastiera) **solo quando la griglia è scesa**
(`fuocoAGrigliaScesa()`: aspetta `transitionend` per al massimo 350 ms). Se si
scrive il nome di una grande ditta escono tutti i suoi marchi.

### Grandi marche
- **46 marche italiane + 14 grandi ditte** (Coca-Cola, Procter & Gamble,
  Nestlé, Unilever, Mondelēz, Henkel, Lactalis, Heineken, Carlsberg,
  Colgate-Palmolive, Danone, PepsiCo, Haleon, Reckitt), in tutto 60 riquadri
  uguali, quattro per riga, che stanno in una schermata da 390×844. Le marche
  sono in `GRANDI_MARCHE` in `pagina.py`. L'altezza la decide il telefono:
  (schermo − `--sopra-sotto` 186 px) / `--righe` (lo imposta `disegnaMarche`),
  fra 34 e 54 px; sotto i 34 px si scorre. La casella `#q` è nascosta: toccando
  una marca ci si scrive dentro il nome, ed è così che si cerca. Niente
  categorie. Toccando
  una marca la pagina scende da sola ai risultati. **Niente verde.**
- Si cerca **a parola intera** (`cercaMarca`: «AIA» trovava il maiale). Per le
  ditte si cercano **tutti i loro marchi** (`MULTINAZIONALI` in `pagina.py`).
  Si mettono solo marchi che sono sicuramente di quella ditta OGGI: niente
  Algida/Magnum sotto Unilever, Tropicana sotto PepsiCo, Air Wick/Calgon sotto
  Reckitt; Kellogg's, Mars e Kimberly-Clark restano fuori. Anche la Ferrero ha
  i suoi marchi. Casi particolari: `=Dove` (maiuscole, e solo nel nome),
  `Moretti@Birra`. **Le capsule «compatibili» si tolgono da ogni ricerca per
  marca.** Quando si aggiunge una ditta si controllano le parole sulle offerte
  vere («Maggi» trovava un vino, «Cornetto» il Mulino Bianco). Fini e Moretti
  come marche restano fuori.
- **Le marche senza offerte non si tolgono, si SPENGONO** (tratteggiate,
  sbiadite, non si toccano). Lo decide il telefono con la sua data. Se una
  resta spenta per settimane, si scrive nel registro.
- **I marchi veri ci sono tutti e 46**, uno per file in `strumenti/marchi/`
  (nome in minuscolo coi trattini, `.webp`; le fonti e come scaricarli quando i
  siti bloccano sono in `marchi/FONTI.txt`). Il marchio Ferrero è la scritta
  marrone FERRERO del sito ufficiale, non il logo con le tre stelle. **Ogni marchio va guardato prima
  di metterlo**: le ricerche automatiche ne hanno presi di sbagliati. Fondo
  bianco fisso, nome nascosto dentro. Se il file manca, compare il nome
  scritto.

### Il mio carrello (nel codice e nelle prove si chiama ancora «Personale»)
- Si scrivono parole e il tasto «Aggiungi» le trasforma in pillole. Per ogni
  pillola si vede **il più conveniente** e, toccandola, tutte le offerte. Si
  apre una pillola alla volta, e rossa è solo quella; la × la toglie. Una
  parola già presente (anche con maiuscole diverse) non si aggiunge due volte.
- Le offerte di una parola sono quelle di Cerca (devono esserci tutte le parole
  scritte), meno i supermercati tolti qui e quelli tolti in Configurazione.
- Il più conveniente (`piuConveniente`) si sceglie **nel reparto con più
  offerte per quella parola** (non si confronta un prezzo al pezzo con uno al
  kg), fra quelle **comprabili oggi**; se oggi non ce n'è, il meno caro in
  assoluto. Niente verde.
- «Personalizza supermercati» vale solo qui e mostra solo i negozi tenuti in
  Configurazione. Non ci sono categorie.

### Configurazione dei supermercati
Si ricordano **quelli TOLTI** (così un'insegna nuova compare da sola). Un
negozio tolto viene trattato come scaduto (`nascosta()`) e sparisce ovunque:
prezzi, meno caro, ricerca, grandi marche.
**Non si possono togliere tutti.** Niente contatore «7 su 7».

### I marchi dei supermercati
Stanno in `strumenti/loghi/`, un file per insegna in minuscolo e senza accenti
(`lidl.svg`, `pam.webp`…). Ci sono tutte e tredici; le fonti sono in
`loghi/FONTI.txt`. Basta mettere o togliere il file: `loghi.py` lo trova da
solo, e se manca compare il nome scritto nei colori dell'insegna. Un PNG o WEBP
diventa un'immagine dentro la pagina; se è a tinte piatte, `python3 -m vettore
<immagine> <insegna> [numero di tinte]` lo trasforma in SVG (così sono nati
Ekom, Ipercoop e Mercatò, che ha due tinte). Gli id dentro ogni SVG vengono
rinominati (`l-<insegna>-<id>`), se no i loghi si rubano le sfumature a vicenda.
Fondo bianco fisso e nome nascosto dentro (`.solo-voce`): è così che le prove
riconoscono il negozio. I marchi restano di chi li ha, e il piede della pagina
lo dice.

### Colori (i cento look)
Il tasto è «Colori della pagina» e la finestra si chiama «Scegli il look».
`strumenti/look.py` calcola i cento look da `palette.json` (il file Figma di
Manlio): non si scrivono a mano, e per aggiungerne basta aggiungere palette.
Verde e ambra non cambiano mai; segue la palette solo l'accento (il rosso).
**Nessun look può essere illeggibile**: `verifica()` controlla il contrasto WCAG
di sette coppie di colori e ferma la generazione. **Sulle pagine chiare
l'accento regge 7:1 come il testo** (`ACCENTO_CHIARO`): la tinta della palette,
scurita; a 4.5 i tasti accesi sembravano sbiaditi. La pagina parte senza look
(«Originale»). I 12 look scuri vengono da palette scure e non hanno niente a
che fare con `prefers-color-scheme` (vincolo 4).

### Finestre, Novità e piede
- **Aiuto**: non si apre mai da sola e si può sempre riaprire. Il testo l'ha
  approvato Manlio. Dice quali sono i negozi e di chi è la copia (solo tua o
  condivisa).
- **Cosa c'è di nuovo** si apre da sola alla prima visita e racconta
  **l'interfaccia, mai i prezzi**. Le novità nuove vanno in fondo a
  `NOVITA_PAGINA` in `pagina.py` con la data davanti all'id; si segnano come
  viste per **id più grande**, non per l'ultima dell'elenco.
- **La pagina Novità** (`novita.py`, `novita.html`): prima «Volantini
  aggiornati» (nuovi, riletti, finiti; tasti Oggi / 3 giorni / 7 giorni), poi
  la tabella di tutti i volantini (in corso, in arrivo, appena finiti), poi il
  diario dei prezzi. **Ogni volantino si sfoglia toccando la sua riga**: si
  apre sopra la pagina con le frecce ‹ ›, lo scorrimento col dito, il tasto
  «Chiudi» e «pagina 3 di 52». Gli indirizzi li fornisce `pagine_di`, il numero
  di pagine `indice.json`, il Conad usa il suo visore e i volantini solo PDF
  (`solopdf`) mostrano il tasto «Aprilo alla pagina N». Quelli finiti non si
  aprono. Funziona solo sul sito.
- **In fondo alla pagina c'è solo il piede**: la data dei volantini e «i
  marchi restano di chi li ha». L'elenco dei volantini non si rimette senza
  chiederglielo. Il pannello delle offerte di un solo volantino esiste ancora,
  ma ci si arriva solo con `#volantino=` nell'indirizzo.

### Visite (Umami)
Lo script sta in `TESTA_SITO` in `pagina.py` (`UMAMI_ID`
`47de14e6-6f92-4ce2-891f-6e37b37062aa`), con `defer` e `data-domains` =
manliograndi-del.github.io: solo sul sito, niente cookie. Le visite si guardano
su cloud.umami.is con l'account di Manlio. Il service worker lascia passare le
richieste verso altri siti, quindi non interferisce. **Non incollarlo a mano
in `index.html`.** La prova è `prova-visite.js`.

### Cosa resta sul telefono (`localStorage`)
`spesa.negozi.v1` (negozi tolti), `spesa.look.v1`, `spesa.personale.v1`,
`spesa.personale.negozi.v1`. Il sito e il link Claude sono indirizzi diversi,
quindi anche sullo stesso telefono hanno due memorie separate.

### Deciso di NO: non riproporre
«Dove conviene questa settimana» («no, io non aggiungerei niente»), la versione
coi tasti sotto le categorie, un riquadro del meno caro in cima, «Dettagli»,
l'elenco dei volantini in fondo e quello delle pagine sotto le offerte, la «i»
accanto al prodotto (con «Elimina» e «Cambia nome»), i sinonimi modificabili,
il contatore dei negozi, la riga «letto a occhio dal volantino».

## Stato e da fare (aggiornato il 2026-09-26)

**Pubblicato:** `sw.js` **v121**, link Claude versione 111 (la versione la dice il registro).

**Scadenze**: `lidl24`, `lidlfv24`, `mercato17`, `mercatoreal17` e
`bennet1709` il 30/9; `md22`, `eurospin24`, `bennetextra24` e `aldi28`
(che comincia il 28/9) il 4/10;
`ekom22` il 5/10; `ipercoop24`, `pam24`, `pamextra24`, `conad24`, `penny24`,
`esselunga24` ed `esselungaaut24` il 7/10;
`carriper29` e `carrcoca15` il 12/10; `carrunilever29` il 22/10; `carraia29`
il 15/11. **Il Carrefour Iper «15-25 settembre» è scaduto ed è stato
tolto il 26/9**: dal 26 al 28/9 il Carrefour Iper ha solo lo speciale
Coca-Cola (`carrcoca15`), poi dal 29/9 arriva `carriper29» già caricato.
`VOLANTINI_ATTESI` è vuoto. Offerte valide solo per una parte del periodo, già segnate riga per
riga: `lidl24` (24-27 o 28-30), il «Doppio weekend» di `eurospin24` (25-27/9 e
2-4/10) e la sua frutta di pagina 12 (dal 28), il «Weekend più Uno» di `md22`
(2-5/10), la pescheria di `pam24` (24-30/9 e 1-7/10), il latte Coop di
`ipercoop24` (28/9-4/10), il «96 ore scontate» di `carriper29` (1-4/10 e
8-11/10), la pagina 2 di `carraia29` (dal 23/10), il venerdì-sabato 25-26/9 e
quello del 2-3/10 di `penny24`, il weekend 2-4/10 di `aldi28`. Tutti i volantini con prezzi
sono letti al 100%. Controllate il 26/9 le dieci insegne di prima sulle fonti
ufficiali per volantini nuovi non ancora in `VOLANTINI`: niente trovato.

**Da fare**
- Le fonti ufficiali sono in uso per Carrefour Iper, MD, Bennet «Offerte
  Extra» e Mercatò «Promo L'Oréal». Restano su anteprimavolantino: Lidl
  (stessa edizione, le 2 pagine in più della versione ufficiale sono
  pubblicità), Eurospin e Bennet «Un mondo di bellezza»; Mercatò principale
  su kimbino. Si passano alle fonti ufficiali al prossimo volantino di
  ciascuna (Lidl ha le immagini delle pagine, Eurospin solo il PDF: si apre
  con `#page=` come il Bennet).
- **Il tasto «Aprilo alla pagina N» dei volantini solo PDF non funziona sul
  suo telefono** (provato da lui il 25/9 con i Kinderini del Bennet: «non si
  apre, ma non importa»). Probabile causa: Chrome per Android non ha un
  lettore di PDF, scarica il file e ignora `#page=`. Una strada da provare
  quando capita: mostrare la pagina dentro la finestra con pdf.js, se il sito
  del PDF lo permette (CORS). Non è urgente.
- **Il 25 ottobre**: la Routine va rimessa a `0 6 * * *`.
- Aspettano lui: le correzioni a penna del catalogo; reinstallare l'icona dal
  nuovo indirizzo e mandare il link alla moglie (da verificare se l'ha già
  fatto).

**Domande aperte da fargli, una alla volta, quando capita**
1. Alla prima visita si apre anche «Cosa c'è di nuovo» con tutte le novità dal
   15 settembre, molte delle quali parlano di cose che non esistono più. La
   togliamo per chi arriva la prima volta? (È una sua regola: serve il suo sì.)
2. Sul link Claude la pagina del volantino si vede, o compare «Aprila sul sito»?
3. Nel carrello, toccando una pillola preferisce andare in Cerca con quella
   parola?
4. Banchi all'etto: accanto al prezzo all'etto c'è scritto «al pezzo», che non
   è giusto.
5. Il 23/9 ha detto «i tasti sono rimasti tutti rossi» e io l'ho interpretato
   come le pillole del carrello: se intendeva altro, va ricontrollato.

## File del progetto

- `index.html`, `novita.html`, `catalogo.pdf`: generati. `sw.js`: la cache.
- `indice.json`: le parole di ogni pagina di ogni volantino (serve agli
  strumenti). `storia/`: il diario, un file al giorno, e l'archivio dei
  prezzi (`prezzi.csv`, `prezzi.json`, `prezzi.html`).
- `strumenti/`: `dati.py` (`VOLANTINI`, `PDF`, `VOLANTINI_ATTESI` e i prezzi in `PRODOTTI`), `catalogo.py`, `pagina.py`,
  `storia.py`, `novita.py`, `scarica.py`, `indice.py`, `lette.py`,
  `scartate.py`, `pulisci.py`, `stampa.py`, `look.py` + `palette.json`,
  `prezzi.py` (l'archivio dei prezzi), `marche_proprie.py`,
  `loghi/`, `marchi/`, `vettore.py`, `registro.py`, `prove.sh` + `prova-*.js`.
- `registro.txt`: una riga per ogni cosa fatta. `NOTE.md`: il perché.
  `archivio/`: le versioni vecchie di questo file.
