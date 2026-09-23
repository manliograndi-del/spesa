# -*- coding: utf-8 -*-
"""Il catalogo: tutto quello che si può accendere, diviso per reparto.

Chiesto da Manlio il 2026-09-05: invece di aggiungere prodotti scrivendone il
nome — che era scomodo, e la lista poi bisognava rimandarmela — c'è un elenco
già pronto e ognuno accende i suoi. Nessuno deve più chiedere niente a nessuno.

Ogni voce ha:
  nome     quello che si legge sul bottone
  parole   come la stessa cosa è scritta sui volantini. Servono a due cose:
           trovare le pagine dove compare, e riagganciare una lista salvata
           prima. Vanno minuscole e senza accenti: il confronto le abbassa.
  reparto  come nel negozio, perché il cassetto si guarda a colpo d'occhio
  unita    con che metro si confrontano i prezzi di questa categoria

L'UNITÀ NON È UN DETTAGLIO. Confrontare il detersivo al chilo dà un numero
vero e inutile: quello che conta è quanto costa un lavaggio. Il latte va al
litro, le uova all'uovo, la carta igienica al rotolo. Sbagliare l'unità qui
significa mettere in cima all'elenco l'offerta sbagliata.
"""

# reparto, [(nome, parole, unità)]
REPARTI = [
 ('Macelleria e salumi', [
  ('Manzo',               'bovino manzo scottona roastbeef macinato fettine bistecca costata reale', 'kg'),
  ('Vitello',             'vitello vitellone fesa tagliata', 'kg'),
  ('Suino',               'suino maiale lonza coppa braciole arista spezzato costine nodini involtini', 'kg'),
  ('Pollo',               'pollo petto alette fusi sovracosce cosce filettini', 'kg'),
  ('Tacchino',            'tacchino fesa spinacine', 'kg'),
  ('Salsiccia',           'salsiccia salamella luganega bocconcini', 'kg'),
  ('Prosciutto',          'prosciutto crudo cotto stagionato daniele parma speck praga', 'kg'),
  ('Salame',              'salame salamino negronetto cacciatore ungherese milano', 'kg'),
  ('Mortadella',          'mortadella bologna', 'kg'),
  ('Bresaola',            'bresaola punta anca', 'kg'),
  ('Pancetta',            'pancetta bacon guanciale cubetti', 'kg'),
  # LE CARNI LAVORATE HANNO CATEGORIE LORO (Manlio, 2026-09-23, scelta «A»
  # fra due): prima stavano con la carne fresca e il «meno caro» del Suino
  # erano i würstel, quello del Manzo le polpettine. Un bollino verde così
  # manda in negozio a comprare la cosa sbagliata.
  ('Würstel',             'wurstel wudy wuber frankfurter', 'kg'),
  ('Preparati',           'hamburger polpette polpettine cotolette cotoletta cordon nuggets spiedini bombette kebab rolle', 'kg'),
  ('Affettati',           'arrosto forno affettato affettati', 'kg'),
 ]),
 ('Pesce', [
  ('Tonno',               'tonno tonnetto pinne gialle yellowfin', 'kg'),
  ('Salmone',             'salmone filetto sashimi saku', 'kg'),
  # Due parole apposta, come «Verdure surgelate»: «Affumicato» da solo non si
  # capirebbe. Costa tre o quattro volte il salmone fresco: insieme, il
  # confronto non aveva senso.
  ('Salmone affumicato',  'affumicato affumicata', 'kg'),
  ('Merluzzo',            'merluzzo baccala nasello platessa filetti bianchi', 'kg'),
  ('Gamberi',             'gamberi gamberetti mazzancolle code', 'kg'),
  ('Calamari',            'calamari seppie totano anelli moscardini', 'kg'),
  # Era «Bastoncini»: dal 2026-09-23 ci stanno anche croccole, fishburger,
  # filetti impanati, fritto misto e tempura, tolti dal merluzzo, dai
  # calamari e dai gamberi freschi.
  ('Panati',              'bastoncini findus capitan croccole panato panati impanati fishburger pastella tempura', 'kg'),
  # Chiesta da Manlio il 2026-09-05: sui volantini c'erano orata a 8,90 al kg,
  # branzino, polpo, vongole, verdesca, scampi — offerte vere che non avevano
  # nessuna casa e restavano fuori. Una voce sola per tutto cio che non e tonno,
  # salmone, merluzzo, gamberi o calamari: scelta sua fra quattro proposte.
  # NIENTE la parola «pesce» qui dentro: e in mezzo mondo («bastoncini di
  # pesce», «sugo di pesce», «zuppa di pesce») e tirerebbe dentro pagine che
  # con questa voce non c'entrano. Meglio i nomi delle bestie.
  ('Pesce',               'orata branzino spigola sgombro verdesca trota cefalo alaccia polpo vongole cozze scampi spada sogliola dentice ricciola gallinella lupino', 'kg'),
 ]),
 ('Freschi', [
  ('Latte',               'latte uht scremato intero microfiltrato', 'litro'),
  ('Yogurt',              'yogurt yoghurt kefir vasetti skyr fermenti greco', 'kg'),
  ('Burro',               'burro', 'kg'),
  ('Uova',                'uova uovo albume medie', 'uovo'),
  ('Mozzarella',          'mozzarella ciliegine bocconcini fiordilatte bufala', 'kg'),
  ('Formaggio',           'formaggio formaggi caciotta provola sottilette stracchino asiago emmental pecorino', 'kg'),
  ('Grana',               'grana parmigiano reggiano padano', 'kg'),
  ('Spalmabili',          'philadelphia spalmabile robiola certosa formaggino', 'kg'),
  ('Ricotta',             'ricotta mascarpone', 'kg'),
 ]),
 ('Dispensa', [
  ('Pasta',               'pasta spaghetti penne fusilli maccheroni tortellini gnocchi ravioli lasagne semola', 'kg'),
  ('Riso',                'riso arborio carnaroli basmati parboiled', 'kg'),
  ('Farina',              'farina semola manitoba', 'kg'),
  ('Pane',                'pane pancarre bauletto piadina focaccia grissini crackers', 'kg'),
  ('Pomodoro',            'passata pelati polpa pomodoro concentrato datterini', 'kg'),
  ("Olio d'oliva",        'oliva extravergine evo frantoio', 'litro'),
  ('Olio di semi',        'semi girasole arachide mais', 'litro'),
  ('Zucchero',            'zucchero canna dolcificante', 'kg'),
  ('Legumi',              'fagioli ceci lenticchie piselli legumi borlotti cannellini', 'kg'),
  ('Sughi',               'sugo ragu pesto salsa arrabbiata', 'kg'),
  ('Conserve',            'mais carciofini olive funghi sottaceti capperi cetriolini', 'kg'),
 ]),
 ('Colazione e dolci', [
  ('Caffè',               'caffe macinato capsule cialde moka solubile espresso', 'kg'),
  ('Tè',                  'the tisane camomilla infuso deteina', 'kg'),
  ('Biscotti',            'biscotti frollini gocciole pavesini digestive wafer cookies oro', 'kg'),
  ('Merendine',           'merendine brioche croissant plumcake girelle pancake', 'kg'),
  ('Cereali',             'cereali fiocchi muesli flakes avena', 'kg'),
  ('Marmellata',          'marmellata confettura composta', 'kg'),
  ('Miele',               'miele acacia millefiori', 'kg'),
  ('Cioccolato',          'cioccolato cioccolata tavoletta praline ovetti cacao', 'kg'),
  ('Creme',               'nutella nocciolata crema spalmabile', 'kg'),
 ]),
 ('Surgelati e gelati', [
  ('Verdure surgelate',   'minestrone spinaci surgelate surgelati piselli bieta', 'kg'),
  # «margherita» da sola non si può usare: sui volantini è una moka Bialetti e
  # un fiore. Trovata così dalla pagina delle pagine di Manlio.
  ('Pizza',               'pizza surgelata', 'kg'),
  ('Gelato',              'gelato coni cornetti vaschetta ghiaccioli stecco', 'kg'),
 ]),
 ('Frutta e verdura', [
  ('Frutta',              'mele pere uva banane arance pesche kiwi frutta mirtilli fragole', 'kg'),
  ('Verdura',             'zucchine melanzane pomodori peperoni carote cipolle verdura finocchi', 'kg'),
  ('Insalata',            'insalata iceberg rucola songino misticanza cuori', 'kg'),
  ('Patate',              'patate patata', 'kg'),
 ]),
 ('Bevande', [
  ('Acqua',               'acqua naturale frizzante minerale effervescente', 'litro'),
  ('Vino',                'vino doc docg chardonnay barbera prosecco lambrusco', 'litro'),
  ('Birra',               'birra lager weiss doppio malto', 'litro'),
  ('Bibite',              'succo nettare aranciata cola bibita gassosa limonata', 'litro'),
 ]),
 ('Casa e igiene', [
  ('Lavatrice',           'lavatrice detersivo caps capsule dash dixan omino bucato', 'lavaggio'),
  ('Lavastoviglie',       'lavastoviglie pastiglie finish fairy brillantante', 'lavaggio'),
  ('Ammorbidente',        'ammorbidente coccolino lenor vernel', 'lavaggio'),
  ('Carta igienica',      'igienica rotoloni scottonelle rotoli', 'rotolo'),
  ('Asciugatutto',        'asciugatutto tovaglioli fazzoletti cucina strappi', 'rotolo'),
  ('Bagnoschiuma',        'bagnoschiuma sapone docciaschiuma intimo mani', 'litro'),
  ('Shampoo',             'shampoo balsamo capelli', 'litro'),
  ('Dentifricio',         'dentifricio spazzolino mentadent colgate', 'litro'),
  ('Collutorio',          'collutorio listerine', 'litro'),
 ]),
]

# unità -> (come si legge sotto il prezzo, come si chiama la quantità)
METRI = {
 'kg':       ('al kg',      'kg'),
 'litro':    ('al litro',   'litri'),
 'uovo':     ("all'uovo",   'uova'),
 'rotolo':   ('al rotolo',  'rotoli'),
 'lavaggio': ('a lavaggio', 'lavaggi'),
}

CATALOGO = [dict(nome=n, parole=p.split(), reparto=rep, unita=u)
            for rep, voci in REPARTI for n, p, u in voci]

NOMI = [v['nome'] for v in CATALOGO]
UNITA = {v['nome']: METRI[v['unita']] for v in CATALOGO}

assert len(NOMI) == len(set(NOMI)), 'due voci del catalogo si chiamano uguale'

# I NOMI VECCHI, E PERCHE' QUESTO ELENCO NON SI CANCELLA.
# Il 2026-09-22 Manlio ha fatto accorciare i nomi: «i bottoni delle categorie
# tengono troppo posto, tutte le categorie che hanno piu di una parola, se e
# possibile, devono essere ridotte a una sola parola, e prosciutto crudo e
# cotto riuniti; le cose surgelate, e inutile dire che sono surgelate».
# Ma i nomi vecchi non sono solo nostri: sono scritti nella LISTA SALVATA nel
# telefono di Manlio e in quello di sua moglie. Senza questa tabella, il loro
# bottone «Prosciutto crudo» resterebbe li con quel nome lungo, e «Pesce
# fresco» non si riaggancerebbe affatto — il riaggancio va per nome e per
# parole del volantino, e fra le parole del pesce la parola «pesce» non c'e
# apposta (tirerebbe dentro i bastoncini e i sughi).
# Quindi: chi ha un bottone che si chiama ancora come il catalogo di prima se
# lo ritrova col nome nuovo, senza perdere niente. Chi si e' rinominato un
# prodotto a modo suo non viene toccato.
# Vale anche per storia.py: senza, il diario del giorno del cambio avrebbe
# annunciato che 1387 offerte «hanno cambiato reparto». Una novita' falsa.
RINOMINATE = {
 'Carne di bue':              'Manzo',
 'Prosciutto crudo':          'Prosciutto',
 'Prosciutto cotto':          'Prosciutto',
 'Pancetta e bacon':          'Pancetta',
 'Merluzzo e baccalà':        'Merluzzo',
 'Calamari e seppie':         'Calamari',
 'Bastoncini di pesce':       'Panati',
 'Bastoncini':                'Panati',
 'Pesce fresco':              'Pesce',
 'Grana e parmigiano':        'Grana',
 'Formaggi spalmabili':       'Spalmabili',
 'Pomodoro e passata':        'Pomodoro',
 'Legumi in scatola':         'Legumi',
 'Sughi pronti':              'Sughi',
 'Verdure in scatola':        'Conserve',
 'Tè e tisane':               'Tè',
 'Creme spalmabili':          'Creme',
 'Pizza surgelata':           'Pizza',
 'Insalata in busta':         'Insalata',
 'Succhi e bibite':           'Bibite',
 'Detersivo lavatrice':       'Lavatrice',
 'Detersivo lavastoviglie':   'Lavastoviglie',
 'Carta cucina e tovaglioli': 'Asciugatutto',
 'Sapone e bagnoschiuma':     'Bagnoschiuma',
}

_fuori = sorted(set(RINOMINATE.values()) - set(NOMI))
if _fuori:
    raise SystemExit('nomi nuovi che nel catalogo non esistono: ' + ', '.join(_fuori))
_restati = sorted(set(RINOMINATE) & set(NOMI))
if _restati:
    raise SystemExit('nomi vecchi ancora nel catalogo: ' + ', '.join(_restati))
