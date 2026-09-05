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
  ('Carne di bue',        'bovino manzo scottona roastbeef hamburger macinato fettine bistecca costata reale', 'kg'),
  ('Vitello',             'vitello vitellone fesa tagliata', 'kg'),
  ('Suino',               'suino maiale lonza coppa braciole arista spezzato costine nodini involtini', 'kg'),
  ('Pollo',               'pollo petto alette fusi sovracosce cosce filettini nuggets', 'kg'),
  ('Tacchino',            'tacchino fesa spinacine', 'kg'),
  ('Salsiccia',           'salsiccia salamella luganega bocconcini', 'kg'),
  ('Prosciutto crudo',    'crudo prosciutto stagionato daniele parma speck', 'kg'),
  ('Prosciutto cotto',    'cotto prosciutto praga', 'kg'),
  ('Salame',              'salame salamino negronetto cacciatore ungherese milano', 'kg'),
  ('Mortadella',          'mortadella bologna', 'kg'),
  ('Bresaola',            'bresaola punta anca', 'kg'),
  ('Pancetta e bacon',    'pancetta bacon guanciale cubetti', 'kg'),
 ]),
 ('Pesce', [
  ('Tonno',               'tonno tonnetto pinne gialle yellowfin', 'kg'),
  ('Salmone',             'salmone filetto affumicato sashimi saku', 'kg'),
  ('Merluzzo e baccalà',  'merluzzo baccala nasello platessa filetti bianchi', 'kg'),
  ('Gamberi',             'gamberi gamberetti mazzancolle code', 'kg'),
  ('Calamari e seppie',   'calamari seppie totano anelli moscardini', 'kg'),
  ('Bastoncini di pesce', 'bastoncini findus capitan', 'kg'),
 ]),
 ('Freschi', [
  ('Latte',               'latte uht scremato intero microfiltrato', 'litro'),
  ('Yogurt',              'yogurt yoghurt kefir vasetti skyr fermenti greco', 'kg'),
  ('Burro',               'burro', 'kg'),
  ('Uova',                'uova uovo albume medie', 'uovo'),
  ('Mozzarella',          'mozzarella ciliegine bocconcini fiordilatte bufala', 'kg'),
  ('Formaggio',           'formaggio formaggi caciotta provola sottilette stracchino asiago emmental pecorino', 'kg'),
  ('Grana e parmigiano',  'grana parmigiano reggiano padano', 'kg'),
  ('Formaggi spalmabili', 'philadelphia spalmabile robiola certosa formaggino', 'kg'),
  ('Ricotta',             'ricotta mascarpone', 'kg'),
 ]),
 ('Dispensa', [
  ('Pasta',               'pasta spaghetti penne fusilli maccheroni tortellini gnocchi ravioli lasagne semola', 'kg'),
  ('Riso',                'riso arborio carnaroli basmati parboiled', 'kg'),
  ('Farina',              'farina semola manitoba', 'kg'),
  ('Pane',                'pane pancarre bauletto piadina focaccia grissini crackers', 'kg'),
  ('Pomodoro e passata',  'passata pelati polpa pomodoro concentrato datterini', 'kg'),
  ("Olio d'oliva",        'oliva extravergine evo frantoio', 'litro'),
  ('Olio di semi',        'semi girasole arachide mais', 'litro'),
  ('Zucchero',            'zucchero canna dolcificante', 'kg'),
  ('Legumi in scatola',   'fagioli ceci lenticchie piselli legumi borlotti cannellini', 'kg'),
  ('Sughi pronti',        'sugo ragu pesto salsa arrabbiata', 'kg'),
  ('Verdure in scatola',  'mais carciofini olive funghi sottaceti capperi cetriolini', 'kg'),
 ]),
 ('Colazione e dolci', [
  ('Caffè',               'caffe macinato capsule cialde moka solubile espresso', 'kg'),
  ('Tè e tisane',         'the tisane camomilla infuso deteina', 'kg'),
  ('Biscotti',            'biscotti frollini gocciole pavesini digestive wafer cookies oro', 'kg'),
  ('Merendine',           'merendine brioche croissant plumcake girelle pancake', 'kg'),
  ('Cereali',             'cereali fiocchi muesli flakes avena', 'kg'),
  ('Marmellata',          'marmellata confettura composta', 'kg'),
  ('Miele',               'miele acacia millefiori', 'kg'),
  ('Cioccolato',          'cioccolato cioccolata tavoletta praline ovetti cacao', 'kg'),
  ('Creme spalmabili',    'nutella nocciolata crema spalmabile', 'kg'),
 ]),
 ('Surgelati e gelati', [
  ('Verdure surgelate',   'minestrone spinaci surgelate surgelati piselli bieta', 'kg'),
  ('Pizza surgelata',     'pizza margherita surgelata', 'kg'),
  ('Gelato',              'gelato coni cornetti vaschetta ghiaccioli stecco', 'kg'),
 ]),
 ('Frutta e verdura', [
  ('Frutta',              'mele pere uva banane arance pesche kiwi frutta mirtilli fragole', 'kg'),
  ('Verdura',             'zucchine melanzane pomodori peperoni carote cipolle verdura finocchi', 'kg'),
  ('Insalata in busta',   'insalata iceberg rucola songino misticanza cuori', 'kg'),
  ('Patate',              'patate patata', 'kg'),
 ]),
 ('Bevande', [
  ('Acqua',               'acqua naturale frizzante minerale effervescente', 'litro'),
  ('Vino',                'vino doc docg chardonnay barbera prosecco lambrusco', 'litro'),
  ('Birra',               'birra lager weiss doppio malto', 'litro'),
  ('Succhi e bibite',     'succo nettare aranciata cola bibita gassosa limonata', 'litro'),
 ]),
 ('Casa e igiene', [
  ('Detersivo lavatrice', 'lavatrice detersivo caps capsule dash dixan omino bucato', 'lavaggio'),
  ('Detersivo lavastoviglie', 'lavastoviglie pastiglie finish fairy brillantante', 'lavaggio'),
  ('Ammorbidente',        'ammorbidente coccolino lenor vernel', 'lavaggio'),
  ('Carta igienica',      'igienica rotoloni scottonelle rotoli', 'rotolo'),
  ('Carta cucina e tovaglioli', 'asciugatutto tovaglioli fazzoletti cucina strappi', 'rotolo'),
  ('Sapone e bagnoschiuma', 'bagnoschiuma sapone docciaschiuma intimo mani', 'litro'),
  ('Shampoo',             'shampoo balsamo capelli', 'litro'),
  ('Dentifricio',         'dentifricio collutorio spazzolino mentadent colgate', 'litro'),
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
