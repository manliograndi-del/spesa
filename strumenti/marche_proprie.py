# -*- coding: utf-8 -*-
# LE MARCHE DEI DISCOUNT NON SI SCRIVONO (Manlio, 2026-09-26: «i discount
# hanno delle marche proprie, come Milbona per il latte di Lidl… questi nomi
# non hanno molto senso: toglili tutti»). Sulla scheda resta solo il nome del
# prodotto; nei dati la marca c'è ancora (`pro` intero), così Cerca la trova.
# Solo marche che sono sicuramente dell'insegna: nel dubbio si lascia.
MARCHE_PROPRIE = {
    'Lidl': {'Milbona', 'Italiamo', 'Deluxe', 'Sol&Mar', 'Crownfield', 'Freshona',
             'Puerto Dorado', 'Certossa', 'Sondey', 'Delser', 'Fin Carré', 'Mister Choc',
             'Idee Gustose', 'Gastronomia di Mare', 'Mare Gioioso', 'Latteria',
             'Latteria Free From', 'Chef Select', 'Dal Salumiere', 'Solevita', 'Alesto',
             'Pilos', 'Combino', 'Vitasia', 'Snack Day', 'Bellarom', 'Kania', 'Cien', 'W5',
             'Formil', 'Saskia', 'Freeway', 'Baresa', 'Nixe', 'Ocean Sea', 'Gelatelli',
             'Trattoria Alfredo', 'Harvest Basket', 'Favorina', 'Perlenbacher', 'Vemondo'},
    'Eurospin': {'Land', 'Ondina', 'La Badia', 'Dolciando', 'Amo Essere', 'Amo Essere Veg',
                 'Fresche Fette', 'Best Bräu', 'La Fiorita', 'Tre Mulini', 'Fior di Natura',
                 'Spesa Intelligente', 'Delizie dal Sole', 'Pizzeria da Pietro'},
    'MD': {'La Fattoria', 'Buona Spesa!', 'Le Specialità di Beppe', 'Vivo Meglio', 'Gustato',
           "Ca' Bianca", "Lettere dall'Italia", 'Malga Paradiso', 'Pasta Reale', 'Le Bon',
           'La Dolce', 'Flou', 'La Delicata', 'Poseidon', 'Fish&Fine', 'Le Tradizionali',
           'Semì', 'Naturali Bontà', 'Jolie', 'Playtime', 'Midi CiaoCiò',
           'Pasticceria del Centro', 'Arca', 'Manusol', 'Apisol', 'Tenute Varvari',
           'Le Cortigiane', 'Mega Soft', 'Cliosan', 'Neoveda'},
    'Aldi': {'Il Podere', 'I Colori del Sapore', 'Regione che vai', 'Milsani', 'La Cesta',
             'Il Tagliere del Re', "Buon'Ora", 'Gourmet', 'Blu Mares', 'Lyttos', 'Gut Bio',
             'Bio Natura', 'Primis', 'Bonlà', 'Happy Harvest', "King's Crown", 'Le Gusto',
             'Cucina', 'American', 'Almare Seafood', 'Splendid', 'Multinorm', 'Choceur',
             'Primana', 'Good Choice', 'All Seasons', 'Denovo', 'Costellore', 'Bergkönig',
             "Rio d'Oro", 'Kokett', 'Buffalo', 'Lacura'},
    'Penny': {'Penny', 'Sapor di Cascina', 'Le Specialità Cuor di Terra', 'Gran Mare',
              'Welless', 'Gli Allegri Sapori', 'ValBontà', 'Ortomio', 'Natura è',
              'Momenti di Mare', 'Fior di Pasta', 'La Filiera in Tavola', 'Chocolà',
              'Le Gelizie', 'Funny Drink'},
}
