# -*- coding: utf-8 -*-
"""La lista di partenza, cioè quella con cui nasce la pagina la prima volta.

Dal 2026-09-02 la lista **vive dentro la pagina pubblicata** e la modificano
sia Manlio sia sua moglie: questa serve solo a far nascere la prima versione.
Dopo, comanda quella pubblicata, e questo file non la tocca più.

È la lista che Manlio mi ha incollato quel giorno, meno la carta igienica che
aveva tolto, più il suino che aveva aggiunto e i quattro del 4 settembre.

QUI CI SONO SOLO I NOMI. Le parole con cui si cerca nei volantini stanno nel
catalogo, e ci stanno una volta sola. Fino al 2026-09-05 erano scritte anche
qui, e si erano già rovinate: «Formaggio» cercava ancora *parmigiano*, *grana*
e *mozzarella*, che nel frattempo erano diventate categorie a sé. Una pagina
nata da questa lista avrebbe rimesso il parmigiano fra i formaggi generici e
sballato il confronto. Trovato cercando il codice rimasto in giro dopo le
modifiche, non provando la pagina: da fuori non si vedeva.
"""
from catalogo import CATALOGO

NOMI_DI_PARTENZA = [
 'Carne di bue', 'Tonno', 'Salmone', 'Suino', 'Pollo', 'Formaggio', 'Uova',
 "Olio d'oliva",
 # aggiunti da Manlio il 2026-09-04, con l'iniziale maiuscola come ha chiesto
 'Biscotti', 'Yogurt', 'Marmellata', 'Cioccolato',
]

_per_nome = {v['nome']: v for v in CATALOGO}
_mancanti = [n for n in NOMI_DI_PARTENZA if n not in _per_nome]
if _mancanti:
    raise SystemExit('nomi di partenza che non stanno nel catalogo: ' + ', '.join(_mancanti))

PARTENZA = [(n, _per_nome[n]['parole'], n) for n in NOMI_DI_PARTENZA]
