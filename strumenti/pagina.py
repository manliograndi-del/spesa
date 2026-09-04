# -*- coding: utf-8 -*-
"""Genera la pagina web da pubblicare.

Prodotti e prezzi da dati.py, lista di partenza da lista.py.

Due scelte volute, chieste da Manlio il 2026-09-02 dopo aver provato la
prima versione:

1. TEMA CHIARO FISSO. Niente blocco `prefers-color-scheme: dark`: il suo
   telefono è in modalità notte e la pagina gli si apriva nera («così non
   si può vedere»). Sfondo bianco dichiarato esplicitamente, così tiene
   anche se chi ospita la pagina è scuro.
2. BOTTONI IN CIMA. I prodotti sono bottoni in testa alla pagina; toccarne
   uno riempie la lista qui sotto, già ordinata dal meno caro. Prima erano
   schede da aprire e chiudere una per una, e per arrivare al tonno
   toccava scorrere.

La lista vive in localStorage, non sul server: vedi NOTE.md.
"""
import json, os, glob
from dati import PRODOTTI, VOLANTINI, UNITA, D
from lista import PARTENZA

# ---------------------------------------------------------------------------
# Le scritte dell'interfaccia, nelle lingue che si possono scegliere.
#
# CAMBIA SOLO L'INVOLUCRO, MAI LA SOSTANZA. Restano in italiano, in tutte le
# lingue: i nomi dei prodotti (li scrive Manlio e servono a cercare dentro
# volantini italiani), i nomi delle insegne, la descrizione di ogni offerta
# come sta sul volantino, le condizioni («PREZZO SOCI», «con la carta Lidl
# Plus»), i periodi di validità e le parole lette dall'OCR. Tradurre quelle
# vorrebbe dire riscrivere il volantino, e su un prezzo un'imprecisione costa.
#
# L'italiano è la lingua di riserva: una chiave che manca in un'altra lingua
# esce in italiano invece di sparire.
# ---------------------------------------------------------------------------
LINGUE = {
 'it': {
  'spiega': '<h2>Come leggerla</h2>\n<p>I prezzi sono <b>letti a mano</b>, uno per uno, dalle pagine dei volantini: le scritte grandi il computer non le legge. Il confronto è <b>per unità</b> e cambia col prodotto — la carne al chilo, il latte al litro, le uova all\'uovo, il detersivo a lavaggio.</p>\n<p>Se <b>aggiungi un prodotto nuovo</b>, i prezzi non ce li ha ancora: ti dice in quali pagine compare la parola, e il prezzo lo leggi tu aprendo la pagina. Puoi mettere <b>più nomi separati da virgola</b> — <i>yogurt, yogurth, vasetti</i> — e trova le pagine dove c\'è almeno uno.</p>\n<p>Le righe segnate <span class="ev">da controllare</span> vengono da riassunti trovati online e possono essere sbagliate. Certi prezzi valgono <b>solo con la tessera</b> — soci Coop, Lidl Plus, Bennet Club, SpesAmica — e sta scritto nella riga.</p>\n<p>Ogni riga <b>apre il volantino</b> alla pagina giusta, in una scheda nuova.</p>',
  'nome': 'Italiano', 'sigla': 'IT',
  'titolo': 'La lista della spesa',
  'sottotitolo': 'Tocca un prodotto: qui sotto compaiono le offerte, dalla più conveniente in giù. Volantini di Lidl, Eurospin, MD, Bennet, Ipercoop e Carrefour Iper.',
  'agg_ph': 'Nome del prodotto, o più nomi separati da virgola',
  'agg_aria': 'Nomi del prodotto da aggiungere, separati da virgola',
  'agg_btn': 'Aggiungi', 'piu': '+ aggiungi',
  'cambia': 'Cambia nome', 'togli': 'Togli «{x}» dalla lista', 'salva': 'Salva',
  'rin_aria': 'Nomi del prodotto, separati da virgola',
  'cerca_anche': 'cerca anche:',
  'st_condivisa': 'Lista condivisa: quello che cambi lo vede anche chi ha il link.',
  'st_solo': 'Questa copia è solo tua: le modifiche restano su questo telefono.',
  'st_salvando': 'Sto salvando per tutti…',
  'st_salvata': 'Salvata. La vedono tutti quelli che hanno il link.',
  'st_conflitto': "Nel frattempo l'ha cambiata qualcun altro: fra un attimo vedi la sua.",
  'st_lettore': "Puoi solo guardare la lista di chi te l'ha mandata: le tue modifiche restano su questo telefono.",
  'st_errore': 'Non sono riuscito a salvarla per tutti. Resta su questo telefono.',
  'conta_off': '{n} {parola} dal volantino · {m} pagine da guardare',
  'off_una': 'offerta letta', 'off_tante': 'offerte lette',
  'conta_pag_una': '{n} pagina lo nomina', 'conta_pag': '{n} pagine lo nominano',
  'f_prezzi': 'Prezzi letti dal volantino',
  'f_altre': 'Altre pagine che lo nominano', 'f_pagine': 'Pagine da guardare',
  'meno_caro': 'il meno caro', 'da_controllare': 'da controllare',
  'confezione': '{p} € la confezione',
  'apri': 'Apri la pagina {n} del volantino',
  'senza_pagina': '{f} — pagina non individuata',
  'pag': 'pag. {n}', 'altre_pag': 'Mostra le altre {n} pagine',
  'niente_pag': 'Il computer non ha letto questa parola in nessuna pagina. Può esserci lo stesso: prova a chiamare il prodotto in un altro modo, con una parola più comune.',
  'lista_vuota': 'La lista è vuota. Tocca «+ aggiungi» per rimetterci qualcosa.',
  'manda_tit': 'Mandami la tua lista',
  'manda_cond': 'Se la lista è condivisa non serve: la leggo da solo dalla pagina. Serve solo su una copia che gira per conto suo, come il file salvato sul telefono.',
  'manda_solo': 'Questa copia non è collegata alle altre: quello che cambi qui non arriva a me. Tocca il bottone e incolla nella chat, ci sono anche i nomi alternativi.',
  'manda_btn': 'Copia la mia lista',
  'manda_ok': 'Copiata. Adesso incollala nella chat.',
  'manda_no': 'Non sono riuscito a copiarla da solo: tienila premuta qui sotto, «Seleziona tutto», copia.',
  'manda_aria': 'La tua lista, da copiare',
  'vol_tit': 'I volantini', 'vol_pag': '{n} pag.',
  'letto': 'letti il {d}',
  'pie': 'I numeri di pagina sono quelli dei volantini.',
  'lingua_aria': 'Lingua delle scritte',
  'u_kg': 'al kg', 'u_l': 'al litro', 'u_uovo': "all'uovo", 'u_rotolo': 'al rotolo', 'u_lav': 'a lavaggio',
 },
 'en': {
  'spiega': '<h2>How to read it</h2>\n<p>Prices are <b>read by hand</b>, one by one, from the leaflet pages: a computer cannot read the big display type. The comparison is <b>per unit</b> and changes with the product — meat per kg, milk per litre, eggs per egg, detergent per wash.</p>\n<p>If you <b>add a new product</b>, it has no prices yet: it tells you which pages mention the word, and you read the price by opening the page. You can enter <b>several names separated by commas</b> — <i>yogurt, yogurth, vasetti</i> — and it finds pages containing at least one.</p>\n<p>Rows marked <span class="ev">needs checking</span> come from summaries found online and may be wrong. Some prices apply <b>only with the shop\'s card</b> — soci Coop, Lidl Plus, Bennet Club, SpesAmica — and the row says so.</p>\n<p>Every row <b>opens the leaflet</b> at the right page, in a new tab. Product names and offer details stay in Italian: they are quoted from Italian leaflets.</p>',
  'nome': 'English', 'sigla': 'EN',
  'titolo': 'The shopping list',
  'sottotitolo': 'Tap a product: the offers appear below, cheapest first. Leaflets from Lidl, Eurospin, MD, Bennet, Ipercoop and Carrefour Iper. Product names and offer details stay in Italian — they come from Italian leaflets.',
  'agg_ph': 'Product name, or several names separated by commas',
  'agg_aria': 'Names of the product to add, separated by commas',
  'agg_btn': 'Add', 'piu': '+ add',
  'cambia': 'Change name', 'togli': 'Remove “{x}” from the list', 'salva': 'Save',
  'rin_aria': 'Product names, separated by commas',
  'cerca_anche': 'also searches:',
  'st_condivisa': 'Shared list: what you change is seen by everyone with the link.',
  'st_solo': 'This copy is yours alone: changes stay on this phone.',
  'st_salvando': 'Saving for everyone…',
  'st_salvata': 'Saved. Everyone with the link sees it.',
  'st_conflitto': 'Someone else changed it meanwhile: you will see their version in a moment.',
  'st_lettore': 'You can only view the list you were sent: your changes stay on this phone.',
  'st_errore': 'I could not save it for everyone. It stays on this phone.',
  'conta_off': '{n} {parola} from the leaflet · {m} pages to check',
  'off_una': 'offer read', 'off_tante': 'offers read',
  'conta_pag_una': '{n} page mentions it', 'conta_pag': '{n} pages mention it',
  'f_prezzi': 'Prices read from the leaflet',
  'f_altre': 'Other pages that mention it', 'f_pagine': 'Pages to check',
  'meno_caro': 'cheapest', 'da_controllare': 'needs checking',
  'confezione': '€{p} per pack',
  'apri': 'Open page {n} of the leaflet',
  'senza_pagina': '{f} — page not identified',
  'pag': 'p. {n}', 'altre_pag': 'Show the other {n} pages',
  'niente_pag': 'The computer did not read this word on any page. It may still be there: try another word for the product, a more common one.',
  'lista_vuota': 'The list is empty. Tap “+ add” to put something back.',
  'manda_tit': 'Send me your list',
  'manda_cond': 'Not needed when the list is shared: I read it from the page myself. It only helps on a copy that runs on its own, like the file saved on your phone.',
  'manda_solo': 'This copy is not connected to the others: what you change here does not reach me. Tap the button and paste it into the chat — the alternative names come too.',
  'manda_btn': 'Copy my list',
  'manda_ok': 'Copied. Now paste it into the chat.',
  'manda_no': 'I could not copy it myself: press and hold the text below, “Select all”, copy.',
  'manda_aria': 'Your list, to copy',
  'vol_tit': 'The leaflets', 'vol_pag': '{n} pp.',
  'letto': 'read on {d}',
  'pie': 'Page numbers are the leaflets\' own.',
  'lingua_aria': 'Interface language',
  'u_kg': 'per kg', 'u_l': 'per litre', 'u_uovo': 'per egg', 'u_rotolo': 'per roll', 'u_lav': 'per wash',
 },
 'fr': {
  'spiega': '<h2>Comment la lire</h2>\n<p>Les prix sont <b>lus à la main</b>, un par un, sur les pages des prospectus : les gros caractères, un ordinateur ne les lit pas. La comparaison se fait <b>à l\'unité</b> et change selon le produit — la viande au kilo, le lait au litre, les œufs à l\'œuf, la lessive au lavage.</p>\n<p>Si vous <b>ajoutez un produit</b>, il n\'a pas encore de prix : la page vous dit où le mot apparaît, et vous lisez le prix en ouvrant la page. Vous pouvez mettre <b>plusieurs noms séparés par des virgules</b> — <i>yogurt, yogurth, vasetti</i> — et elle trouve les pages qui en contiennent au moins un.</p>\n<p>Les lignes marquées <span class="ev">à vérifier</span> viennent de résumés trouvés en ligne et peuvent être fausses. Certains prix ne valent <b>qu\'avec la carte du magasin</b> — soci Coop, Lidl Plus, Bennet Club, SpesAmica — et la ligne le précise.</p>\n<p>Chaque ligne <b>ouvre le prospectus</b> à la bonne page, dans un nouvel onglet. Les noms des produits et le détail des offres restent en italien : ils sont cités des prospectus italiens.</p>',
  'nome': 'Français', 'sigla': 'FR',
  'titolo': 'La liste de courses',
  'sottotitolo': "Touchez un produit : les offres apparaissent ci-dessous, de la moins chère à la plus chère. Prospectus de Lidl, Eurospin, MD, Bennet, Ipercoop et Carrefour Iper. Les noms des produits et le détail des offres restent en italien : ils viennent de prospectus italiens.",
  'agg_ph': 'Nom du produit, ou plusieurs noms séparés par des virgules',
  'agg_aria': 'Noms du produit à ajouter, séparés par des virgules',
  'agg_btn': 'Ajouter', 'piu': '+ ajouter',
  'cambia': 'Changer le nom', 'togli': 'Retirer « {x} » de la liste', 'salva': 'Enregistrer',
  'rin_aria': 'Noms du produit, séparés par des virgules',
  'cerca_anche': 'cherche aussi :',
  'st_condivisa': 'Liste partagée : ce que vous changez est vu par tous ceux qui ont le lien.',
  'st_solo': 'Cette copie est à vous seul : les modifications restent sur ce téléphone.',
  'st_salvando': 'Enregistrement pour tous…',
  'st_salvata': 'Enregistrée. Tous ceux qui ont le lien la voient.',
  'st_conflitto': "Quelqu'un d'autre l'a modifiée entre-temps : vous verrez sa version dans un instant.",
  'st_lettore': 'Vous pouvez seulement consulter la liste reçue : vos modifications restent sur ce téléphone.',
  'st_errore': "Je n'ai pas réussi à l'enregistrer pour tous. Elle reste sur ce téléphone.",
  'conta_off': '{n} {parola} du prospectus · {m} pages à regarder',
  'off_una': 'offre lue', 'off_tante': 'offres lues',
  'conta_pag_una': '{n} page le mentionne', 'conta_pag': '{n} pages le mentionnent',
  'f_prezzi': 'Prix lus sur le prospectus',
  'f_altre': 'Autres pages qui le mentionnent', 'f_pagine': 'Pages à regarder',
  'meno_caro': 'le moins cher', 'da_controllare': 'à vérifier',
  'confezione': '{p} € le paquet',
  'apri': 'Ouvrir la page {n} du prospectus',
  'senza_pagina': '{f} — page non identifiée',
  'pag': 'p. {n}', 'altre_pag': 'Afficher les {n} autres pages',
  'niente_pag': "L'ordinateur n'a lu ce mot sur aucune page. Il peut quand même y être : essayez un autre mot, plus courant.",
  'lista_vuota': 'La liste est vide. Touchez « + ajouter » pour y remettre quelque chose.',
  'manda_tit': 'Envoyez-moi votre liste',
  'manda_cond': "Inutile si la liste est partagée : je la lis moi-même sur la page. Cela ne sert que sur une copie autonome, comme le fichier enregistré sur le téléphone.",
  'manda_solo': "Cette copie n'est pas reliée aux autres : ce que vous changez ici ne me parvient pas. Touchez le bouton et collez dans la conversation, les autres noms viennent aussi.",
  'manda_btn': 'Copier ma liste',
  'manda_ok': 'Copiée. Collez-la maintenant dans la conversation.',
  'manda_no': "Je n'ai pas réussi à la copier : appuyez longuement sur le texte ci-dessous, « Tout sélectionner », copiez.",
  'manda_aria': 'Votre liste, à copier',
  'vol_tit': 'Les prospectus', 'vol_pag': '{n} p.',
  'letto': 'lus le {d}',
  'pie': 'Les numéros de page sont ceux des prospectus.',
  'lingua_aria': "Langue de l'interface",
  'u_kg': 'le kg', 'u_l': 'le litre', 'u_uovo': "l'œuf", 'u_rotolo': 'le rouleau', 'u_lav': 'le lavage',
 },
 'es': {
  'spiega': '<h2>Cómo leerla</h2>\n<p>Los precios están <b>leídos a mano</b>, uno por uno, de las páginas de los folletos: la letra grande el ordenador no la lee. La comparación es <b>por unidad</b> y cambia con el producto — la carne al kilo, la leche al litro, los huevos al huevo, el detergente al lavado.</p>\n<p>Si <b>añades un producto nuevo</b>, todavía no tiene precios: te dice en qué páginas aparece la palabra, y el precio lo lees abriendo la página. Puedes poner <b>varios nombres separados por comas</b> — <i>yogurt, yogurth, vasetti</i> — y encuentra las páginas donde hay al menos uno.</p>\n<p>Las filas marcadas <span class="ev">por comprobar</span> vienen de resúmenes encontrados en internet y pueden estar equivocadas. Algunos precios valen <b>solo con la tarjeta de la tienda</b> — soci Coop, Lidl Plus, Bennet Club, SpesAmica — y la fila lo dice.</p>\n<p>Cada fila <b>abre el folleto</b> por la página correcta, en una pestaña nueva. Los nombres de los productos y el detalle de las ofertas siguen en italiano: están citados de folletos italianos.</p>',
  'nome': 'Español', 'sigla': 'ES',
  'titolo': 'La lista de la compra',
  'sottotitolo': 'Toca un producto: debajo aparecen las ofertas, de la más barata en adelante. Folletos de Lidl, Eurospin, MD, Bennet, Ipercoop y Carrefour Iper. Los nombres de los productos y el detalle de las ofertas siguen en italiano: vienen de folletos italianos.',
  'agg_ph': 'Nombre del producto, o varios nombres separados por comas',
  'agg_aria': 'Nombres del producto a añadir, separados por comas',
  'agg_btn': 'Añadir', 'piu': '+ añadir',
  'cambia': 'Cambiar el nombre', 'togli': 'Quitar «{x}» de la lista', 'salva': 'Guardar',
  'rin_aria': 'Nombres del producto, separados por comas',
  'cerca_anche': 'busca también:',
  'st_condivisa': 'Lista compartida: lo que cambies lo ve todo el que tenga el enlace.',
  'st_solo': 'Esta copia es solo tuya: los cambios se quedan en este teléfono.',
  'st_salvando': 'Guardando para todos…',
  'st_salvata': 'Guardada. La ve todo el que tenga el enlace.',
  'st_conflitto': 'Mientras tanto la ha cambiado otra persona: en un momento verás la suya.',
  'st_lettore': 'Solo puedes mirar la lista que te han enviado: tus cambios se quedan en este teléfono.',
  'st_errore': 'No he podido guardarla para todos. Se queda en este teléfono.',
  'conta_off': '{n} {parola} del folleto · {m} páginas que mirar',
  'off_una': 'oferta leída', 'off_tante': 'ofertas leídas',
  'conta_pag_una': '{n} página lo nombra', 'conta_pag': '{n} páginas lo nombran',
  'f_prezzi': 'Precios leídos del folleto',
  'f_altre': 'Otras páginas que lo nombran', 'f_pagine': 'Páginas que mirar',
  'meno_caro': 'el más barato', 'da_controllare': 'por comprobar',
  'confezione': '{p} € el paquete',
  'apri': 'Abrir la página {n} del folleto',
  'senza_pagina': '{f} — página no identificada',
  'pag': 'pág. {n}', 'altre_pag': 'Mostrar las otras {n} páginas',
  'niente_pag': 'El ordenador no ha leído esta palabra en ninguna página. Puede estar igualmente: prueba a llamar al producto de otra manera, con una palabra más común.',
  'lista_vuota': 'La lista está vacía. Toca «+ añadir» para volver a poner algo.',
  'manda_tit': 'Mándame tu lista',
  'manda_cond': 'No hace falta si la lista es compartida: la leo yo mismo de la página. Solo sirve en una copia que va por su cuenta, como el archivo guardado en el teléfono.',
  'manda_solo': 'Esta copia no está conectada con las otras: lo que cambies aquí no me llega. Toca el botón y pégala en el chat, van también los nombres alternativos.',
  'manda_btn': 'Copiar mi lista',
  'manda_ok': 'Copiada. Ahora pégala en el chat.',
  'manda_no': 'No he podido copiarla yo: mantén pulsado el texto de abajo, «Seleccionar todo», copia.',
  'manda_aria': 'Tu lista, para copiar',
  'vol_tit': 'Los folletos', 'vol_pag': '{n} pág.',
  'letto': 'leídos el {d}',
  'pie': 'Los números de página son los de los folletos.',
  'lingua_aria': 'Idioma de la interfaz',
  'u_kg': 'el kg', 'u_l': 'el litro', 'u_uovo': 'el huevo', 'u_rotolo': 'el rollo', 'u_lav': 'el lavado',
 },
}

PDF     = {c: f for c, _, _, f, _, _ in VOLANTINI}
MODELLO = {c: m for c, _, _, _, _, m in VOLANTINI}

def indirizzo(chiave, n):
    """L'indirizzo pubblico di una pagina del volantino, per renderla cliccabile.
    Senza numero di pagina non c'e niente da aprire: torna None e la riga resta
    scritta e basta."""
    if not n or chiave not in MODELLO:
        return None
    return MODELLO[chiave].format(n=n)
PERIODO = {c: p for c, _, p, _, _, _ in VOLANTINI}

offerte = [dict(cat=cat, ins=ins, rep=rep, pro=pro, fmt=fmt, prezzo=pre,
                unitario=round(pre / qta, 3), pag=pag, pdf=PDF[chiave],
                url=indirizzo(chiave, pag),
                periodo=PERIODO[chiave], dubbio=(fon == D), note=note)
           for cat, ins, chiave, rep, pro, fmt, qta, pre, pag, fon, note in PRODOTTI]

idx = json.load(open('indice.json', encoding='utf-8'))
validi = {(os.path.basename(os.path.dirname(f)), int(os.path.basename(f)[:-4]))
          for f in glob.glob('pg/*/*.jpg')}
pagine = sorted((dict(ins=r['insegna'], periodo=r['validita'], pdf=PDF.get(r['chiave'], ''),
                      pag=r['pagina'], parole=r['parole'],
                      url=indirizzo(r['chiave'], r['pagina']))
                 for r in idx if (r['chiave'], r['pagina']) in validi),
                key=lambda r: (r['ins'], r['periodo'], r['pag']))

volantini = [v for v in (dict(ins=i, periodo=p, pdf=f,
                              pagine=len([x for x in pagine if x['pdf'] == f]))
                         for c, i, p, f, _, _ in VOLANTINI) if v['pagine']]

partenza = [dict(nome=n, parole=p, cat=c) for n, p, c in PARTENZA]

# LA LISTA CHE COMANDA E QUELLA CHE HANNO LORO.
# Manlio e la moglie aggiungono e tolgono prodotti dalla pagina pubblicata. Se
# l'aggiornamento settimanale dei volantini ripartisse da PARTENZA, gliela
# cancellerebbe tutta a ogni giro. Quindi: prima di rigenerare, si legge la
# lista dalla pagina viva (lista_attuale.py la tira fuori e la scrive qui) e si
# riparte da quella. PARTENZA serve solo se il file non c'e, cioe la prima volta.
lista_viva = 'lista-attuale.json'
if os.path.exists(lista_viva):
    salvata = json.load(open(lista_viva, encoding='utf-8'))
    if isinstance(salvata, list) and salvata:
        partenza = salvata
        print(f'lista ripresa dalla pagina viva: {len(partenza)} prodotti')

DATI = json.dumps(dict(offerte=offerte, pagine=pagine, volantini=volantini,
                       partenza=partenza, unita={k: v[0] for k, v in UNITA.items()},
                       letto='4 settembre 2026'),
                  ensure_ascii=False, separators=(',', ':'))
LISTA0 = json.dumps(partenza, ensure_ascii=False, separators=(',', ':'))
LINGUE_JSON = json.dumps(LINGUE, ensure_ascii=False, separators=(',', ':'))

HTML = r'''<title>Spesa</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Asap:wght@400;500;600;700&family=Oswald:wght@500;600;700&display=swap">
<style>
/* Tema chiaro unico e dichiarato: nessun blocco scuro, perché la pagina
   si apriva nera sul telefono di Manlio in modalità notte. */
:root{
  --carta:#FFFFFF;
  --pannello:#F6F5F2;
  --inchiostro:#1B1B1A;
  --tenue:#6E6C66;
  --linea:#E5E3DD;
  --linea-forte:#CFCCC4;
  --rosso:#D40D2B;
  --su-rosso:#FFFFFF;
  --verde:#1E7A4B;
  --verde-tenue:#E6F3EC;
  --ambra:#8A5A08;
  --ambra-tenue:#FCF2DE;
  --f-testo:'Asap',ui-sans-serif,system-ui,'Segoe UI',sans-serif;
  --f-prezzo:'Oswald','Arial Narrow',ui-sans-serif,sans-serif;
  color-scheme:light;
}
*{box-sizing:border-box}
html{background:var(--carta)}
body{background:var(--carta);color:var(--inchiostro);font-family:var(--f-testo);
  font-size:16px;line-height:1.45;-webkit-text-size-adjust:100%}
button{font-family:var(--f-testo);color:inherit}
:focus-visible{outline:3px solid var(--rosso);outline-offset:2px}
.guscio{max-width:800px;margin:0 auto;padding:0 15px 60px}

/* ---- selettore della lingua, in alto a destra ---- */
.testa-alta{display:flex;align-items:flex-start;justify-content:space-between;gap:14px}
.lingue{display:flex;gap:0;margin-top:18px;flex:0 0 auto;border:1.5px solid var(--linea-forte);
  border-radius:99px;overflow:hidden;background:var(--carta)}
.lingue button{background:none;border:0;border-left:1px solid var(--linea);cursor:pointer;
  padding:7px 11px;font-size:12.5px;font-weight:700;letter-spacing:.06em;color:var(--tenue);
  min-height:36px;line-height:1}
.lingue button:first-child{border-left:0}
.lingue button[aria-pressed="true"]{background:var(--rosso);color:var(--su-rosso)}

/* ---- testa ---- */
header{padding:20px 0 2px}
h1{font-family:var(--f-prezzo);font-weight:700;font-size:26px;letter-spacing:.01em;
  line-height:1.05;margin:0;text-transform:uppercase}
h1 span{display:block;color:var(--rosso);font-size:12px;letter-spacing:.16em;margin-bottom:6px}
.sottotitolo{color:var(--tenue);margin:8px 0 0;font-size:14px;max-width:62ch}

/* ---- barra dei prodotti ---- */
.barra{position:sticky;top:0;z-index:20;background:var(--carta);
  padding:12px 0 12px;border-bottom:2px solid var(--inchiostro);margin-top:14px}
.tasti{display:flex;flex-wrap:wrap;gap:8px}
.tasto{background:var(--carta);border:1.5px solid var(--linea-forte);border-radius:99px;
  padding:10px 15px;font-size:15px;font-weight:600;cursor:pointer;line-height:1.1;
  min-height:44px;white-space:nowrap}
.tasto[aria-pressed="true"]{background:var(--rosso);border-color:var(--rosso);color:var(--su-rosso)}
.tasto.agg{border-style:dashed;color:var(--tenue);font-weight:500}

/* ---- aggiunta ---- */
.form-agg{display:none;gap:8px;margin-top:10px}
.form-agg.on{display:flex}
.form-agg input{flex:1;min-width:0;background:var(--carta);color:var(--inchiostro);
  border:1.5px solid var(--rosso);border-radius:10px;padding:12px 13px;
  font-family:var(--f-testo);font-size:16px}
.form-agg input:focus{outline:none}
.form-agg button{background:var(--rosso);color:var(--su-rosso);border:0;border-radius:10px;
  padding:0 18px;font-size:15px;font-weight:600;cursor:pointer;min-height:46px}

/* ---- intestazione del risultato ---- */
.capo{display:flex;align-items:baseline;justify-content:space-between;gap:10px;
  flex-wrap:wrap;margin:20px 0 2px}
.capo h2{font-family:var(--f-prezzo);text-transform:uppercase;letter-spacing:.02em;
  font-size:22px;font-weight:600;margin:0}
.capo .quanti{color:var(--tenue);font-size:13px;font-variant-numeric:tabular-nums}
.sinonimi{margin:6px 0 0;font-size:13.5px;color:var(--tenue);display:flex;
  flex-wrap:wrap;gap:6px;align-items:baseline}
.sinonimi em{font-style:normal;background:var(--pannello);border:1px solid var(--linea);
  border-radius:99px;padding:2px 9px;font-size:13px;color:var(--inchiostro)}
.gestisci{display:flex;gap:9px;margin:12px 0 0;flex-wrap:wrap}
.gestisci button{background:var(--carta);border:1.5px solid var(--linea-forte);border-radius:9px;
  padding:10px 16px;font-size:14.5px;font-weight:600;cursor:pointer;min-height:44px}
.gestisci .togli{border-color:var(--rosso);color:var(--rosso)}
.form-rin{display:none;gap:8px;margin-top:10px}
.form-rin.on{display:flex}
.form-rin input{flex:1;min-width:0;border:1.5px solid var(--rosso);border-radius:10px;
  padding:12px 13px;font-family:var(--f-testo);font-size:16px;background:var(--carta);
  color:var(--inchiostro)}
.form-rin input:focus{outline:none}
.form-rin button{background:var(--rosso);color:var(--su-rosso);border:0;border-radius:10px;
  padding:0 18px;font-size:15px;font-weight:600;cursor:pointer;min-height:46px}

/* ---- elenco prezzi ---- */
.fascia{font-family:var(--f-prezzo);text-transform:uppercase;letter-spacing:.06em;
  font-size:12.5px;font-weight:600;color:var(--tenue);margin:22px 0 0}
.prezzo-riga{display:grid;grid-template-columns:1fr auto;gap:3px 14px;
  padding:13px 0;border-top:1px solid var(--linea)}
.prezzo-riga:first-of-type{border-top:1.5px solid var(--inchiostro)}
.prezzo-riga .nome{margin:0;font-size:16.5px;font-weight:600;line-height:1.25}
.prezzo-riga .sotto{margin:3px 0 0;color:var(--tenue);font-size:13.5px}
.prezzo-riga .sotto b{color:var(--inchiostro);font-weight:600}
.prezzo-riga .val{grid-row:1/3;text-align:right;font-family:var(--f-prezzo);
  font-variant-numeric:tabular-nums;line-height:1;white-space:nowrap}
.prezzo-riga .val .n{display:block;font-size:27px;font-weight:700;color:var(--rosso)}
.prezzo-riga .val .u{display:block;font-family:var(--f-testo);font-size:10.5px;
  letter-spacing:.08em;text-transform:uppercase;color:var(--tenue);margin-top:4px}
.prezzo-riga .coda{grid-column:1/-1;margin:7px 0 0;display:flex;flex-wrap:wrap;gap:6px;
  align-items:center}
.bollo{font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;font-weight:700;
  border-radius:5px;padding:3px 8px}
.bollo.meno{background:var(--verde-tenue);color:var(--verde)}
.bollo.dubbio{background:var(--ambra-tenue);color:var(--ambra)}
.prezzo-riga .nota{grid-column:1/-1;margin:6px 0 0;font-size:13.5px;color:var(--tenue)}
.prezzo-riga .dove{grid-column:1/-1;margin:6px 0 0;font-size:13px;color:var(--tenue);
  border-left:3px solid var(--linea);padding-left:9px}
a.dove.apri{display:inline-block;margin-top:8px;color:var(--rosso);font-weight:600;
  text-decoration:underline;text-underline-offset:3px;border-left:0;padding:7px 0;
  min-height:34px}
a.dove.apri::after{content:' \2197'}

/* ---- elenco pagine ---- */
.pag-riga{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
  padding:11px 0;border-top:1px solid var(--linea);font-size:14.5px}
.pag-riga:first-of-type{border-top:1.5px solid var(--inchiostro)}
.pag-riga .ins{font-weight:600}
.pag-riga .per{display:block;color:var(--tenue);font-size:12.5px;font-weight:400}
.pag-riga .np{font-family:var(--f-prezzo);font-size:19px;font-weight:600;
  font-variant-numeric:tabular-nums;white-space:nowrap}
a.pag-riga{text-decoration:none;color:inherit}
a.pag-riga.apribile{padding:13px 0;min-height:48px}
a.pag-riga.apribile .ins{color:var(--rosso);text-decoration:underline;text-underline-offset:3px}
a.pag-riga.apribile .np{color:var(--rosso)}
a.pag-riga.apribile .np::after{content:' \2197';font-family:var(--f-testo);font-size:13px}
.altre{width:100%;margin-top:12px;background:var(--pannello);border:1.5px solid var(--linea);
  border-radius:10px;padding:12px;font-size:14.5px;font-weight:600;cursor:pointer;min-height:46px}
.vuoto{color:var(--tenue);font-size:14.5px;margin:14px 0 0;background:var(--pannello);
  border-radius:10px;padding:14px}

/* ---- coda ---- */
.manda{margin-top:30px;border:2px solid var(--inchiostro);border-radius:12px;padding:16px}
.manda h2{font-family:var(--f-prezzo);text-transform:uppercase;font-size:15px;
  letter-spacing:.04em;margin:0 0 8px}
.manda p{font-size:14px;margin:0 0 12px;color:var(--tenue)}
.manda button{background:var(--inchiostro);color:var(--carta);border:0;border-radius:10px;
  padding:13px 18px;font-size:15px;font-weight:600;cursor:pointer;min-height:48px;width:100%}
.manda textarea{display:none;width:100%;margin-top:12px;min-height:150px;resize:vertical;
  font-family:ui-monospace,'SF Mono',Menlo,monospace;font-size:13px;line-height:1.5;
  background:var(--pannello);color:var(--inchiostro);border:1.5px solid var(--linea);
  border-radius:10px;padding:11px}
.manda textarea.on{display:block}
.manda .esito{font-size:13.5px;margin:10px 0 0;color:var(--verde);font-weight:600;min-height:1.2em}
.spiega{margin-top:34px;background:var(--pannello);border-radius:12px;padding:16px 16px 4px}
.spiega h2{font-family:var(--f-prezzo);text-transform:uppercase;font-size:15px;
  letter-spacing:.04em;margin:0 0 10px}
.spiega p{font-size:14px;margin:0 0 12px}
.spiega .ev{color:var(--ambra);font-weight:700}
.vol{list-style:none;padding:0;margin:10px 0 0;display:grid;gap:1px;background:var(--linea);
  border:1px solid var(--linea);border-radius:10px;overflow:hidden}
.vol li{background:var(--carta);padding:11px 13px;display:flex;justify-content:space-between;
  align-items:baseline;gap:12px;font-size:14px}
.vol .i{font-weight:600}
.vol .p{color:var(--tenue);font-size:13px}
.vol .n{color:var(--tenue);font-size:12.5px;font-variant-numeric:tabular-nums;white-space:nowrap}
footer{margin-top:28px;padding-top:14px;border-top:1px solid var(--linea);
  color:var(--tenue);font-size:13px}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>

<div class="guscio">
<header>
  <div class="testa-alta">
    <h1><span>Torino · Corso Siracusa</span><span id="h-titolo"></span></h1>
    <div class="lingue" id="lingue" role="group"></div>
  </div>
  <p class="sottotitolo" id="h-sottotitolo"></p>
</header>

<div class="barra">
  <div class="tasti" id="tasti" role="group" aria-label="Scegli il prodotto"></div>
  <form class="form-agg" id="form-agg">
    <input id="nuovo" type="text" placeholder="Nome del prodotto, o più nomi separati da virgola"
           autocomplete="off" aria-label="Nomi del prodotto da aggiungere, separati da virgola">
    <button type="submit">Aggiungi</button>
  </form>
  <p class="stato" id="stato-lista" role="status"></p>
</div>

<div id="risultato"></div>

<section class="manda" id="riquadro-manda">
  <h2 id="h-manda"></h2>
  <p id="perche-manda"></p>
  <button type="button" id="btn-copia"></button>
  <p class="esito" id="esito" role="status"></p>
  <textarea id="testo-lista" readonly aria-label="La tua lista, da copiare"></textarea>
</section>

<section class="spiega">
  <div id="spiega"></div>
  <h2 style="margin-top:18px" id="h-volantini"></h2>
  <ul class="vol" id="vol"></ul>
</section>

<footer><span id="h-letto"></span> <span id="h-pie"></span></footer>
</div>

<script>
const DATI = __DATI__;

/* La lista non e piu solo mia: vive DENTRO questa pagina pubblicata, cosi la
   vedono e la cambiano tutti quelli che hanno il link. Quando qualcuno la
   tocca, la pagina si ripubblica con la lista nuova dentro e ogni schermo
   aperto si ricarica su quella. Vedi NOTE.md per il perche di questa strada
   invece della memoria sul server. */
const LISTA_PUBBLICATA = __LISTA__;
const TEMPLATE = __TEMPLATE__;

/* Vero solo nella copia pubblicata su Claude, dove la lista e davvero
   condivisa e comanda quella dentro la pagina. Sul sito e falso: li dentro non
   c'e niente che possa aggiornare la lista incorporata, quindi comanda quella
   che l'utente si e fatto nel suo browser, altrimenti le sue modifiche
   sparirebbero a ogni ricaricamento. */
const CONDIVISA = __CONDIVISA__;
const CHIAVE = 'spesa.lista.v1';

/* LE SCRITTE CAMBIANO, I DATI NO. Restano in italiano in tutte le lingue i
   nomi dei prodotti, le insegne, la descrizione delle offerte e le loro
   condizioni: vengono dai volantini italiani e servono a cercarci dentro.
   Tradurli vorrebbe dire riscrivere il volantino, e su un prezzo
   un'imprecisione costa. */
const T = __LINGUE__;
const CHIAVE_LINGUA = 'spesa.lingua.v1';

function leggiLingua() {
  try {
    const g = localStorage.getItem(CHIAVE_LINGUA);
    if (g && T[g]) return g;
  } catch (e) { /* niente memoria: si parte in italiano */ }
  try {
    const n = (navigator.language || '').slice(0, 2).toLowerCase();
    if (T[n]) return n;
  } catch (e) { /* nemmeno la lingua del telefono: italiano */ }
  return 'it';
}
let lingua = leggiLingua();

/* L'italiano fa da rete: una chiave che manca in un'altra lingua esce in
   italiano invece di lasciare un buco. */
function t(chiave, valori) {
  let testo = (T[lingua] && T[lingua][chiave]) || T.it[chiave] || '';
  if (valori) for (const k in valori) testo = testo.split('{' + k + '}').join(valori[k]);
  return testo;
}

/* Le unita arrivano dai dati in italiano: qui si traducono per l'etichetta. */
const CHIAVI_UNITA = { 'al kg': 'u_kg', 'al litro': 'u_l', "all'uovo": 'u_uovo',
                       'al rotolo': 'u_rotolo', 'a lavaggio': 'u_lav' };
const unitaDi = cat => t(CHIAVI_UNITA[DATI.unita[cat]] || 'u_kg');

/* Rimette insieme il documento intero con dentro una lista nuova. L'ordine
   conta: prima la lista, poi il template. Al contrario, il template appena
   infilato porterebbe dentro un altro __LISTA__ e verrebbe riempito quello
   sbagliato. Le barre si spezzano in <\/ perche il tag di chiusura dello
   script, scritto per esteso dentro una stringa, chiuderebbe lo script per
   davvero: il browser lo cerca nel testo, non gli importa che sia in una
   stringa o in un commento. */
function documento(nuova) {
  const l = JSON.stringify(nuova).split('</').join('<\\/');
  const t = JSON.stringify(TEMPLATE).split('</').join('<\\/');
  /* Il modello va SEMPRE per ultimo: appena infilato porta dentro una copia di
     tutti gli altri segnaposto, e da quel momento replace() troverebbe quelli
     invece dei veri. Chi si ripubblica e sempre la copia condivisa. */
  return TEMPLATE
    .replace('__LISTA__', () => l)
    .replace('__CONDIVISA__', () => 'true')
    .replace('__TEMPLATE__', () => t);
}

const norm = s => (s || '').toLowerCase()
  .normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/['\u2019]/g, ' ');
/* i detersivi stanno sotto i 20 centesimi a lavaggio: con due decimali
   diventerebbero tutti «0,14 €» e non si distinguerebbero piu */
const eur = n => (n < 1 ? n.toFixed(3) : n.toFixed(2)).replace('.', ',');

/* Iniziale maiuscola sul nome che si legge, chiesto da Manlio: scriveva
   «biscotti» e se lo ritrovava minuscolo in mezzo agli altri. Si tocca solo la
   prima lettera, non ogni parola: «Olio d'oliva» deve restare cosi, e
   text-transform:capitalize del CSS lo storpierebbe in «Olio D'oliva».
   Le parole con cui si cerca restano minuscole: tanto il confronto le
   abbassa comunque. */
const maiuscola = t => (t || '').charAt(0).toUpperCase() + (t || '').slice(1);

/* Dove la lista e condivisa comanda quella dentro la pagina: e quella che
   vedono tutti, e viene aggiornata ripubblicando. Dove non lo e (il sito, il
   file) comanda quella che l'utente si e fatto: nessuno aggiornera mai quella
   incorporata, che li vale solo come punto di partenza. */
function leggiLista() {
  const dentro = Array.isArray(LISTA_PUBBLICATA) && LISTA_PUBBLICATA.length
    ? LISTA_PUBBLICATA.map(riaggancia) : null;
  if (CONDIVISA && dentro) return dentro;
  try {
    const g = localStorage.getItem(CHIAVE);
    if (g) { const v = JSON.parse(g); if (Array.isArray(v) && v.length) return v.map(riaggancia); }
  } catch (e) { /* memoria non disponibile: si riparte da quella incorporata */ }
  return dentro || DATI.partenza.map(p => ({ ...p }));
}

/* Una lista salvata da una versione vecchia della pagina puo avere prodotti
   senza categoria — quando i prezzi letti a mano coprivano solo carne, tonno e
   salmone. Qui si riattaccano ai prezzi che nel frattempo sono arrivati, senza
   toccare i nomi che l'utente si e scelto. Chi ha aggiunto un prodotto suo che
   non corrisponde a niente resta com'e. */
function riaggancia(v) {
  if (!v || !v.nome) return v;
  v = { ...v, nome: maiuscola(v.nome) };
  if (v.cat) return v;
  const nomi = [v.nome].concat(v.parole || []).map(norm);
  const seme = DATI.partenza.find(x =>
    nomi.includes(norm(x.nome)) || (x.parole || []).some(w => nomi.includes(norm(w))));
  if (!seme) return v;
  const parole = (v.parole || []).slice();
  seme.parole.forEach(p => { if (!parole.some(x => norm(x) === norm(p))) parole.push(p); });
  return { nome: maiuscola(v.nome), parole, cat: seme.cat };
}
function salvaLocale() {
  try { localStorage.setItem(CHIAVE, JSON.stringify(lista)); }
  catch (e) { /* la pagina funziona lo stesso, solo non ricorda */ }
}

let ART = null;          // la capacita di ripubblicare, se questa vista ce l'ha
let soloMio = true;      // finche non sappiamo il contrario, la lista e solo qui
let attesa = null;       // per non ripubblicare a ogni singolo tocco

function stato(testo, brutto) {
  const e = document.getElementById('stato-lista');
  if (!e) return;
  e.textContent = testo;
  e.className = 'stato' + (brutto ? ' brutto' : '');
}

/* Si ripubblica dopo un attimo, non a ogni tocco: chi ne toglie tre di fila
   fa una pubblicazione sola invece di tre, e gli altri schermi si ricaricano
   una volta sola. */
function salva() {
  salvaLocale();
  if (!ART || soloMio || !TEMPLATE) return;
  stato(t('st_salvando'));
  clearTimeout(attesa);
  attesa = setTimeout(async () => {
    try {
      await ART.publish(documento(lista));
      stato(t('st_salvata'));
    } catch (err) {
      const c = err && err.code;
      if (c === 'conflict') {
        /* qualcun altro ha salvato nel frattempo: ogni schermo si ricarica
           sulla sua versione, quindi qui non si insiste */
        stato(t('st_conflitto'));
      } else if (c === 'not_writer' || c === 'not_granted') {
        soloMio = true;
        stato(t('st_lettore'), true);
      } else {
        stato(t('st_errore'), true);
      }
    }
  }, 1200);
}


let lista = leggiLista();
let scelto = 0;
let tutteLePagine = false;

const offerteDi = v => v.cat ? DATI.offerte.filter(o => o.cat === v.cat) : [];

/* Le pagine dei volantini dove compare almeno uno dei nomi del prodotto.
   Se non ha nomi alternativi si cerca il nome stesso. */
const pagineDi = v => {
  const termini = (v.parole && v.parole.length ? v.parole : [v.nome]).map(norm);
  return DATI.pagine.filter(p => {
    const dentro = norm(p.parole);
    return termini.some(t => dentro.includes(t));
  });
};

/* tutti i nomi di un prodotto: quello sul bottone piu gli altri con cui cercarlo */
function nomiDi(v) {
  const out = [v.nome];
  (v.parole || []).forEach(p => { if (norm(p) !== norm(v.nome)) out.push(p); });
  return out;
}

/* Un prodotto si puo chiamare in piu modi, e il volantino ne usa uno solo:
   «detersivo» o «lavatrice», «carne di bue» o «bovino». Qui si scrivono tutti,
   separati da virgola, e la pagina cerca le pagine dove compare ALMENO UNO.
   Il primo nome e quello che si legge sul bottone, gli altri lavorano sotto.
   Se uno dei nomi e gia noto (uno dei dodici di partenza, o una delle sue
   parole), si porta dietro anche i prezzi letti a mano e le sue parole. */
function costruisci(testo) {
  const termini = testo.split(/[,;]+/).map(x => x.trim()).filter(Boolean);
  if (!termini.length) return null;
  let seme = null;
  for (const t of termini) {
    const n = norm(t);
    seme = DATI.partenza.find(x => norm(x.nome) === n || (x.parole || []).some(w => norm(w) === n));
    if (seme) break;
  }
  const parole = [];
  for (const p of termini.concat(seme ? seme.parole : [])) {
    if (!parole.some(x => norm(x) === norm(p))) parole.push(p);
  }
  return { nome: maiuscola(termini[0]), parole, cat: seme ? seme.cat : null };
}

/* ---------- barra dei prodotti ---------- */
function disegnaTasti() {
  const box = document.getElementById('tasti');
  box.textContent = '';
  lista.forEach((v, i) => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'tasto'; b.textContent = v.nome;
    b.setAttribute('aria-pressed', String(i === scelto));
    b.onclick = () => {
      scelto = i; tutteLePagine = false;
      document.getElementById('form-agg').classList.remove('on');
      disegna();
    };
    box.appendChild(b);
  });
  const piu = document.createElement('button');
  piu.type = 'button'; piu.className = 'tasto agg'; piu.textContent = t('piu');
  piu.onclick = () => {
    const f = document.getElementById('form-agg');
    f.classList.add('on');
    document.getElementById('nuovo').focus();
  };
  box.appendChild(piu);
}

/* ---------- righe ---------- */
function rigaPrezzo(o, primo) {
  const d = document.createElement('article');
  d.className = 'prezzo-riga';
  d.innerHTML = `<div><p class="nome"></p><p class="sotto"></p></div>
    <p class="val"><span class="n"></span><span class="u"></span></p>
    <div class="coda"></div>`;
  d.querySelector('.nome').textContent = o.pro;
  const s = d.querySelector('.sotto');
  s.innerHTML = '<b></b> · <span></span> · <span></span>';
  s.querySelector('b').textContent = o.ins;
  s.querySelectorAll('span')[0].textContent = o.fmt;
  s.querySelectorAll('span')[1].textContent = t('confezione', { p: eur(o.prezzo) });
  d.querySelector('.val .n').textContent = eur(o.unitario) + ' €';
  d.querySelector('.val .u').textContent = unitaDi(o.cat);
  const coda = d.querySelector('.coda');
  if (primo) { const x = document.createElement('span'); x.className = 'bollo meno'; x.textContent = t('meno_caro'); coda.appendChild(x); }
  if (o.dubbio) { const x = document.createElement('span'); x.className = 'bollo dubbio'; x.textContent = t('da_controllare'); coda.appendChild(x); }
  if (!coda.children.length) coda.remove();
  if (o.note) {
    const n = document.createElement('p'); n.className = 'nota'; n.textContent = o.note;
    d.appendChild(n);
  }
  d.appendChild(dove(o));
  return d;
}

/* La riga che dice dov'e l'offerta. Se so l'indirizzo della pagina diventa un
   collegamento che apre il volantino a quella pagina: prima c'era scritto
   «pagina 16» e Manlio doveva arrangiarsi. Si apre in una scheda nuova, cosi
   non perde la lista. */
function dove(o) {
  if (!o.url) {
    const p = document.createElement('p');
    p.className = 'dove';
    p.textContent = t('senza_pagina', { f: o.pdf });
    return p;
  }
  const a = document.createElement('a');
  a.className = 'dove apri';
  a.href = o.url;
  a.target = '_blank';
  a.rel = 'noopener noreferrer';
  a.textContent = t('apri', { n: o.pag });
  return a;
}

function rigaPagina(p) {
  const d = document.createElement(p.url ? 'a' : 'div');
  d.className = 'pag-riga' + (p.url ? ' apribile' : '');
  if (p.url) { d.href = p.url; d.target = '_blank'; d.rel = 'noopener noreferrer'; }
  d.innerHTML = `<span><span class="ins"></span><span class="per"></span></span><span class="np"></span>`;
  d.querySelector('.ins').textContent = p.ins;
  d.querySelector('.per').textContent = p.periodo;
  d.querySelector('.np').textContent = t('pag', { n: p.pag });
  return d;
}

/* ---------- pagina ---------- */
function disegna() {
  disegnaTasti();
  const out = document.getElementById('risultato');
  out.textContent = '';
  if (!lista.length) {
    const v0 = document.createElement('p'); v0.className = 'vuoto'; v0.textContent = t('lista_vuota'); out.appendChild(v0);
    return;
  }
  if (scelto >= lista.length) scelto = lista.length - 1;

  const v = lista[scelto];
  const off = offerteDi(v), pag = pagineDi(v);

  const capo = document.createElement('div');
  capo.className = 'capo';
  capo.innerHTML = '<h2></h2><span class="quanti"></span>';
  capo.querySelector('h2').textContent = v.nome;
  capo.querySelector('.quanti').textContent = off.length
    ? t('conta_off', { n: off.length, parola: t(off.length === 1 ? 'off_una' : 'off_tante'), m: pag.length })
    : t(pag.length === 1 ? 'conta_pag_una' : 'conta_pag', { n: pag.length });
  out.appendChild(capo);

  const altri = nomiDi(v).slice(1);
  if (altri.length) {
    const p = document.createElement('p');
    p.className = 'sinonimi';
    p.innerHTML = '<span></span> ';
    p.querySelector('span').textContent = t('cerca_anche');
    altri.forEach(a => {
      const c = document.createElement('em');
      c.textContent = a;
      p.appendChild(c);
    });
    out.appendChild(p);
  }

  const g = document.createElement('div');
  g.className = 'gestisci';
  const bRin = document.createElement('button');
  bRin.type = 'button'; bRin.textContent = t('cambia');
  const bTog = document.createElement('button');
  bTog.type = 'button'; bTog.className = 'togli';
  bTog.textContent = t('togli', { x: v.nome });
  bTog.onclick = () => {
    lista.splice(scelto, 1);
    if (scelto > 0) scelto--;
    salva(); disegna();
  };
  g.append(bRin, bTog);
  out.appendChild(g);

  const fr = document.createElement('form');
  fr.className = 'form-rin';
  fr.innerHTML = '<input type="text"><button type="submit"></button>';
  fr.querySelector('input').setAttribute('aria-label', t('rin_aria'));
  fr.querySelector('button').textContent = t('salva');
  const inp = fr.querySelector('input');
  fr.onsubmit = ev => {
    ev.preventDefault();
    const t = inp.value.trim();
    if (!t) return;
    const v2 = costruisci(t);
    if (!v2) return;
    lista[scelto] = v2;
    salva(); disegna();
  };
  bRin.onclick = () => {
    fr.classList.add('on');
    inp.value = nomiDi(v).join(', ');
    inp.focus(); inp.select();
  };
  out.appendChild(fr);

  if (off.length) {
    const f = document.createElement('p');
    f.className = 'fascia'; f.textContent = t('f_prezzi');
    out.appendChild(f);
    off.forEach((o, i) => out.appendChild(rigaPrezzo(o, i === 0)));
  }

  const f2 = document.createElement('p');
  f2.className = 'fascia';
  f2.textContent = off.length ? t('f_altre') : t('f_pagine');
  out.appendChild(f2);

  if (pag.length) {
    const quante = tutteLePagine ? pag.length : 10;
    pag.slice(0, quante).forEach(p => out.appendChild(rigaPagina(p)));
    if (pag.length > quante) {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'altre';
      b.textContent = t('altre_pag', { n: pag.length - quante });
      b.onclick = () => { tutteLePagine = true; disegna(); };
      out.appendChild(b);
    }
  } else {
    const p = document.createElement('p');
    p.className = 'vuoto';
    p.textContent = t('niente_pag');
    out.appendChild(p);
  }
}

/* ---------- volantini in fondo ---------- */
const ul = document.getElementById('vol');
DATI.volantini.forEach(v => {
  const li = document.createElement('li');
  li.innerHTML = `<span><span class="i"></span> <span class="p"></span></span><span class="n"></span>`;
  li.querySelector('.i').textContent = v.ins;
  li.querySelector('.p').textContent = v.periodo;
  li.querySelector('.n').textContent = t('vol_pag', { n: v.pagine });
  ul.appendChild(li);
});

document.getElementById('form-agg').onsubmit = ev => {
  ev.preventDefault();
  const c = document.getElementById('nuovo');
  const t = c.value.trim();
  if (!t) return;
  const v2 = costruisci(t);
  if (!v2) return;
  lista.push(v2);
  scelto = lista.length - 1;
  tutteLePagine = false;
  c.value = '';
  document.getElementById('form-agg').classList.remove('on');
  salva(); disegna();
};

/* La lista vive solo qui dentro (localStorage) e non torna indietro a chi ha fatto
   la pagina. Questo bottone la impacchetta in testo da incollare in chat. La
   textarea non e un ripiego per il telefono: negli artifact la scrittura negli
   appunti puo essere negata senza dire niente, e allora il testo dev'essere li
   pronto da selezionare a mano. */
function listaInTesto() {
  const righe = lista.map(v => {
    const altri = nomiDi(v).slice(1);
    return '- ' + v.nome + (altri.length ? '  (anche: ' + altri.join(', ') + ')' : '');
  });
  return 'LA MIA LISTA DELLA SPESA — ' + lista.length +
         (lista.length === 1 ? ' prodotto' : ' prodotti') + '\n' + righe.join('\n');
}

const btnCopia = document.getElementById('btn-copia');
const areaLista = document.getElementById('testo-lista');
const esito = document.getElementById('esito');
btnCopia.onclick = async () => {
  const testo = listaInTesto();
  areaLista.value = testo;
  areaLista.classList.add('on');
  try {
    await navigator.clipboard.writeText(testo);
    esito.textContent = t('manda_ok');
  } catch (e) {
    esito.textContent = t('manda_no');
    areaLista.focus();
    areaLista.select();
  }
};

disegnaLingue();
traduciFissi();

/* Il riquadro per rimandarmi la lista a mano ha senso solo dove la lista non e
   condivisa: se lo e, la leggo dalla pagina pubblicata senza chiedere niente. */
/* Riempie tutto quello che non passa da disegna(): testa, spiegazione, riquadri.
   Si richiama a ogni cambio di lingua. */
function traduciFissi() {
  document.documentElement.lang = lingua;
  const metti = (id, testo) => { const e = document.getElementById(id); if (e) e.textContent = testo; };
  metti('h-titolo', t('titolo'));
  metti('h-sottotitolo', t('sottotitolo'));
  metti('h-volantini', t('vol_tit'));
  metti('h-manda', t('manda_tit'));
  metti('h-letto', t('letto', { d: DATI.letto }));
  metti('h-pie', t('pie'));
  metti('btn-copia', t('manda_btn'));
  const sp = document.getElementById('spiega');
  if (sp) sp.innerHTML = t('spiega');          // testo mio, non di chi apre
  const n = document.getElementById('nuovo');
  if (n) { n.placeholder = t('agg_ph'); n.setAttribute('aria-label', t('agg_aria')); }
  const ab = document.querySelector('#form-agg button');
  if (ab) ab.textContent = t('agg_btn');
  const ta = document.getElementById('testo-lista');
  if (ta) ta.setAttribute('aria-label', t('manda_aria'));
  const vol = document.getElementById('vol');
  if (vol) [...vol.children].forEach((li, i) => {
    const v = DATI.volantini[i];
    if (v) li.querySelector('.n').textContent = t('vol_pag', { n: v.pagine });
  });
  aggiornaRiquadroManda();
}

function disegnaLingue() {
  const box = document.getElementById('lingue');
  if (!box) return;
  box.setAttribute('aria-label', t('lingua_aria'));
  box.textContent = '';
  for (const k of Object.keys(T)) {
    const b = document.createElement('button');
    b.type = 'button';
    b.textContent = T[k].sigla;
    b.title = T[k].nome;
    b.setAttribute('aria-pressed', String(k === lingua));
    b.onclick = () => {
      lingua = k;
      try { localStorage.setItem(CHIAVE_LINGUA, k); } catch (e) { /* non la ricordera */ }
      disegnaLingue(); traduciFissi(); disegna();
    };
    box.appendChild(b);
  }
}

function aggiornaRiquadroManda() {
  const r = document.getElementById('riquadro-manda');
  const p = document.getElementById('perche-manda');
  if (!r) return;
  r.style.display = soloMio ? '' : 'none';
  if (p) p.textContent = soloMio ? t('manda_solo') : t('manda_cond');
}

disegna();

/* Va in fondo, DOPO che «lista» e stata creata e la pagina disegnata una prima
   volta. Messo prima, chiamava disegna() quando «lista» non esisteva ancora e
   moriva li: i bottoni comparivano lo stesso (li disegnava la chiamata in
   fondo) ma sotto non usciva niente. La capacita, dove c'e, arriva comunque
   dopo il primo giro di questo script: la pagina deve funzionare gia prima e
   accendersi quando arriva. */
(async () => {
  try {
    ART = window.claude && claude.use ? await claude.use('artifact') : null;
  } catch (e) { ART = null; }
  if (ART) {
    soloMio = false;
    stato(t('st_condivisa'));
    lista = leggiLista();
  } else {
    stato(t('st_solo'));
  }
  aggiornaRiquadroManda();
  disegna();
})();
</script>'''

# ---------------------------------------------------------------------------
# Il documento contiene una copia di se stesso, cosi puo ripubblicarsi con una
# lista nuova dentro senza perdere la capacita di rifarlo la volta dopo.
#
#   CORPO    = la pagina come la vuole il servizio (senza <html>/<head>: li
#              mette lui), con dentro i due segnaposto
#   COMPLETO = lo stesso, ma documento intero: e questo che la pagina
#              ripubblica di sua iniziativa, e quindi e questo che si porta
#              dietro come modello
#
# I segnaposto restano NON risolti dentro COMPLETO: e proprio quello che
# permette alla generazione dopo di riempirli di nuovo. Prima la lista e poi il
# modello, altrimenti il modello appena infilato porta dentro un altro
# __LISTA__ e si riempie quello sbagliato.
# ---------------------------------------------------------------------------
def racchiudi(testo):
    """JSON da mettere dentro un <script>: </script> va spezzato o chiude il tag."""
    return json.dumps(testo, ensure_ascii=False).replace('</', '<\\/')

CORPO = HTML.replace('__DATI__', DATI).replace('__LINGUE__', LINGUE_JSON)

INTESTA = ('<!doctype html>\n<html lang="it">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           '<style>body{margin:0}img{max-width:100%}</style>\n')
COMPLETO = (INTESTA + CORPO + '\n</body>\n</html>\n').replace(
    '</style>\n\n<div class="guscio">', '</style>\n</head>\n<body>\n<div class="guscio">', 1)

def riempi(modello):
    """Riempie SOLO la prima occorrenza di ogni segnaposto.

    I due segnaposto compaiono due volte ciascuno: una e quella vera, in cima
    allo script, l'altra e la stringa dentro documento() che serve a
    sostituirla la volta dopo. Riempiendole tutte e due si rompe documento() e
    il file cresce di 200 KB inutili. La prima e sempre quella vera, perche le
    due costanti sono dichiarate sopra la funzione; in JavaScript replace() con
    una stringa si ferma alla prima da solo, quindi le due parti si comportano
    allo stesso modo."""
    # il modello per ultimo: vedi documento() nello script, stessa trappola
    return (modello
            .replace('__LISTA__', LISTA0, 1)
            .replace('__CONDIVISA__', 'true', 1)
            .replace('__TEMPLATE__', racchiudi(COMPLETO), 1))

open('out/pagina.html', 'w', encoding='utf-8').write(riempi(CORPO))

# Copia che si apre a doppio clic, senza account e senza rete. Non puo
# ripubblicare (non c'e nessun window.claude), quindi niente modello e niente
# lista condivisa: li la lista e di chi apre e resta nel suo browser.
open('out/spesa-da-sola.html', 'w', encoding='utf-8').write(
    COMPLETO.replace('__LISTA__', LISTA0, 1)
            .replace('__TEMPLATE__', '""', 1)
            .replace('__CONDIVISA__', 'false', 1))

# ---------------------------------------------------------------------------
# La versione per il sito vero (GitHub Pages). Li dentro non esiste
# window.claude, quindi la pagina non potra mai ripubblicarsi: il modello e
# peso morto e lo si toglie (230 KB in meno). Ha invece il manifest e il suo
# service worker, per potersi installare sul telefono e funzionare in negozio
# senza segnale.
# ---------------------------------------------------------------------------
TESTA_SITO = ('<link rel="manifest" href="./manifest.webmanifest">\n'
              '<meta name="theme-color" content="#FFFFFF">\n'
              '<meta name="apple-mobile-web-app-title" content="Spesa">\n')
CODA_SITO = '''<script>
/* Un service worker suo, in questa cartella. Serve a due cose: tenere la
   pagina disponibile senza rete (in negozio il segnale e pessimo) e togliere
   di mezzo quello della Palestra, che ha lo scope sopra e senza rete
   servirebbe l'app della palestra al posto di questa. */
if ('serviceWorker' in navigator) {
  addEventListener('load', () => navigator.serviceWorker.register('./sw.js').catch(() => {}));
}
</script>
'''
sito = (COMPLETO
        .replace('<meta name="viewport" content="width=device-width, initial-scale=1">\n',
                 '<meta name="viewport" content="width=device-width, initial-scale=1">\n' + TESTA_SITO, 1)
        .replace('\n</body>\n</html>\n', '\n' + CODA_SITO + '</body>\n</html>\n', 1)
        .replace('__LISTA__', LISTA0, 1)
        .replace('__TEMPLATE__', '""', 1)
        .replace('__CONDIVISA__', 'false', 1))
open('out/sito.html', 'w', encoding='utf-8').write(sito)
print('sito:', len(sito) // 1024, 'KB (senza la copia di se stessa)')


# ---------------------------------------------------------------------------
# CONTROLLO OBBLIGATORIO, non un lusso.
#
# Il 2026-09-03 un commento conteneva il tag di chiusura dello script scritto
# per esteso. Il browser lo cerca nel testo e non gli importa che sia dentro un
# commento: ha chiuso lo script a meta e tutte e tre le pagine sono uscite
# morte, quella gia in mano a Manlio compresa. Da fuori sembravano a posto —
# intestazione, riquadri, tutto — solo senza prodotti.
#
# Qui si spezza ogni file dove il browser lo spezzerebbe e si controlla che
# ogni pezzo sia JavaScript valido e che quello grosso contenga davvero la
# funzione che disegna la pagina. Se non torna, il file NON si consegna.
# ---------------------------------------------------------------------------
def controlla(percorso):
    import re, subprocess, tempfile
    testo = open(percorso, encoding='utf-8').read()
    pezzi = re.findall(r'<script>(.*?)</script>', testo, re.S)
    if not pezzi:
        raise SystemExit(f'{percorso}: nessuno script trovato')
    for n, pezzo in enumerate(pezzi):
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as t:
            t.write(pezzo); tmp = t.name
        esito = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        os.unlink(tmp)
        if esito.returncode != 0:
            riga = esito.stderr.strip().split(chr(10))
            raise SystemExit(f'{percorso}: il pezzo {n} non e JavaScript valido\n  '
                             + chr(10).join('  ' + r for r in riga[:4]))
    if 'function disegna' not in pezzi[0]:
        raise SystemExit(f'{percorso}: lo script principale e stato tagliato prima di '
                         'disegna(). Quasi certamente c\'e un tag di chiusura scritto '
                         'per esteso in un commento o in una stringa.')
    print(f'  {os.path.basename(percorso):24s} {len(pezzi)} script, tutti validi')

print('controllo che le pagine non siano spezzate:')
for f in ('out/pagina.html', 'out/sito.html', 'out/spesa-da-sola.html'):
    controlla(f)

print('scritta —', len(riempi(CORPO)) // 1024, 'KB;', len(partenza), 'prodotti in lista,',
      len(offerte), 'prezzi,', len(pagine), 'pagine indicizzate')
