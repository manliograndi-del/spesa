# -*- coding: utf-8 -*-
"""Da un'immagine di un marchio a un disegno (SVG) che non sgrana.

    python3 -m vettore <immagine> <insegna>
    python3 -m vettore ekom.png ekom      # scrive strumenti/loghi/ekom.svg

Serve quando di un marchio non esiste un disegno libero da scaricare e si ha
solo una figura. Il 2026-09-22 e successo con l'EKOM: Manlio ha mandato il
marchio come immagine e da li e uscito il disegno che sta nella pagina.

VA BENE SOLO PER I MARCHI A UN COLORE PIENO — che sono quasi tutti: una
scritta o una forma in una tinta sola su fondo bianco o trasparente. Con un
marchio sfumato, o a piu colori, questo non lo sa fare: meglio l'immagine
com'e (`loghi.py` accetta anche .png e .webp).

TRE COSE IMPARATE FACENDOLO, che se si tolgono non funziona piu:

1. **`potrace.Bitmap` si rovescia da solo** (`self.invert()` nel suo
   costruttore): per far disegnare il PIENO gli si passa il VUOTO. Passandogli
   il pieno esce un rettangolo, che e il fondo.
2. **Gli si passa un array di veri/falsi.** Con numeri 0 e 1 il suo confronto
   interno (`data > 127`) li considera tutti vuoti, e il risultato e di nuovo
   un rettangolo.
3. **Si traccia in grande e si rimpicciolisce il risultato.** Sui bordi curvi
   di una scritta a pennello, tracciare alla dimensione dell'immagine lascia
   gradini; al doppio vengono lisci.
"""
import os, sys

import numpy as np
import potrace
from PIL import Image

QUI = os.path.dirname(os.path.abspath(__file__))


def disegna(percorso, colore=None, ingrandimento=2, minimo=12, tolleranza=0.5):
    """Torna l'SVG del marchio: un solo tracciato, del colore che ha dentro."""
    base = Image.open(percorso).convert('RGBA')
    im = base.resize((base.width * ingrandimento, base.height * ingrandimento),
                     Image.LANCZOS) if ingrandimento > 1 else base
    a = np.array(im)
    # il pieno: quello che non e trasparente e non e bianco
    pieno = (a[:, :, 3] > 110) & ~((a[:, :, :3] > 235).all(axis=2))
    if not pieno.any():
        raise SystemExit('%s: non ci trovo niente da disegnare' % percorso)

    if colore is None:
        tinte = a[:, :, :3][pieno]
        # la tinta piu ripetuta, non la media: la media di rosso e bianco e rosa
        chi, quante = np.unique(tinte.reshape(-1, 3), axis=0, return_counts=True)
        colore = '#%02X%02X%02X' % tuple(chi[quante.argmax()])

    ys, xs = np.where(pieno)
    ritaglio = pieno[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    alto, largo = ritaglio.shape

    # ~ritaglio: vedi la nota 1 qui sopra
    tracciato = potrace.Bitmap(~ritaglio).trace(
        turdsize=minimo * ingrandimento, alphamax=1.0,
        opticurve=True, opttolerance=tolleranza)

    def n(v):
        return ('%.1f' % (v / ingrandimento)).rstrip('0').rstrip('.')

    pezzi = []
    for curva in tracciato.curves:
        p = curva.start_point
        d = ['M%s %s' % (n(p.x), n(p.y))]
        for s in curva:
            if s.is_corner:
                d.append('L%s %sL%s %s' % (n(s.c.x), n(s.c.y),
                                           n(s.end_point.x), n(s.end_point.y)))
            else:
                d.append('C%s %s %s %s %s %s'
                         % (n(s.c1.x), n(s.c1.y), n(s.c2.x), n(s.c2.y),
                            n(s.end_point.x), n(s.end_point.y)))
        d.append('Z')
        pezzi.append(''.join(d))

    # «evenodd»: i buchi delle lettere (la pancia della O) restano buchi
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s">'
            '<path fill="%s" fill-rule="evenodd" d="%s"/></svg>'
            % (n(largo), n(alto), colore, ''.join(pezzi)))


def main(argomenti):
    if len(argomenti) < 2:
        raise SystemExit(__doc__.strip().splitlines()[2].strip())
    immagine, insegna = argomenti[0], argomenti[1]
    svg = disegna(immagine)
    fuori = os.path.join(QUI, 'loghi', insegna + '.svg')
    with open(fuori, 'w', encoding='utf-8') as f:
        f.write(svg)
    print('%s — %d byte' % (fuori, len(svg)))


if __name__ == '__main__':
    main(sys.argv[1:])
