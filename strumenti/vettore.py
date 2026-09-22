# -*- coding: utf-8 -*-
"""Da un'immagine di un marchio a un disegno (SVG) che non sgrana.

    python3 -m vettore <immagine> <insegna> [quante tinte]
    python3 -m vettore ekom.png ekom        # scrive strumenti/loghi/ekom.svg
    python3 -m vettore mercato.png mercato 2  # marchio a due colori

Serve quando di un marchio non esiste un disegno libero da scaricare e si ha
solo una figura. Il 2026-09-22 e successo con l'EKOM: Manlio ha mandato il
marchio come immagine e da li e uscito il disegno che sta nella pagina.

VA BENE PER I MARCHI A TINTE PIENE — che sono quasi tutti: una scritta o una
forma in uno o due colori su fondo bianco o trasparente. Quante tinte cercare
si dice come terzo argomento. Con un marchio sfumato, o con una fotografia
dentro, questo non lo sa fare: meglio l'immagine com'e (`loghi.py` accetta
anche .png e .webp).

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


def _tinte(a, pieno, quante):
    """Le `quante` tinte più ripetute del marchio, dalla più scura alla più
    chiara: si disegnano in quest'ordine così una tinta chiara stesa sopra non
    cancella quella sotto."""
    chi, conto = np.unique(a[:, :, :3][pieno].reshape(-1, 3), axis=0,
                           return_counts=True)
    ordine = conto.argsort()[::-1]
    scelte = []
    for i in ordine:
        c = chi[i]
        # due tinte che si somigliano sono la stessa tinta con i bordi sfumati
        if any(abs(int(c[k]) - int(v[k])) < 60 for v in scelte for k in (0, 1, 2)) \
                and any(all(abs(int(c[k]) - int(v[k])) < 60 for k in (0, 1, 2))
                        for v in scelte):
            continue
        scelte.append(c)
        if len(scelte) == quante:
            break
    return sorted(scelte, key=lambda c: int(c[0]) + int(c[1]) + int(c[2]))


def _traccia(maschera, ingrandimento, minimo, tolleranza):
    """Da una maschera di veri/falsi al tracciato SVG. `~maschera`: vedi la
    nota 1 qui sopra."""
    tracciato = potrace.Bitmap(~maschera).trace(
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
    return ''.join(pezzi)


def disegna(percorso, colori=1, ingrandimento=2, minimo=12, tolleranza=0.5):
    """Torna l'SVG del marchio: un tracciato per ogni tinta che ha dentro.

    `colori=1` basta per i marchi a una tinta sola (EKOM, Ipercoop). Il
    Mercatò ne ha due — la scritta blu e la fascia arancione — e con una sola
    verrebbe tutto blu.
    """
    base = Image.open(percorso).convert('RGBA')
    im = base.resize((base.width * ingrandimento, base.height * ingrandimento),
                     Image.LANCZOS) if ingrandimento > 1 else base
    a = np.array(im)
    # il pieno: quello che non e trasparente e non e bianco
    pieno = (a[:, :, 3] > 110) & ~((a[:, :, :3] > 235).all(axis=2))
    if not pieno.any():
        raise SystemExit('%s: non ci trovo niente da disegnare' % percorso)

    ys, xs = np.where(pieno)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    alto, largo = y1 - y0, x1 - x0

    def n(v):
        return ('%.1f' % (v / ingrandimento)).rstrip('0').rstrip('.')

    strati = []
    if colori <= 1:
        tinta = _tinte(a, pieno, 1)[0]
        strati.append(('#%02X%02X%02X' % tuple(tinta),
                       _traccia(pieno[y0:y1, x0:x1], ingrandimento, minimo, tolleranza)))
    else:
        scelte = _tinte(a, pieno, colori)
        # ogni pixel va alla tinta che gli somiglia di piu
        dist = np.stack([np.abs(a[:, :, :3].astype(int) - t.astype(int)).sum(axis=2)
                         for t in scelte])
        vicina = dist.argmin(axis=0)
        for i, t in enumerate(scelte):
            maschera = pieno & (vicina == i)
            if maschera.sum() < 50:
                continue
            strati.append(('#%02X%02X%02X' % tuple(t),
                           _traccia(maschera[y0:y1, x0:x1], ingrandimento,
                                    minimo, tolleranza)))

    # «evenodd»: i buchi delle lettere (la pancia della O) restano buchi
    dentro = ''.join('<path fill="%s" fill-rule="evenodd" d="%s"/>' % (c, d)
                     for c, d in strati if d)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s">%s</svg>'
            % (n(largo), n(alto), dentro))


def main(argomenti):
    if len(argomenti) < 2:
        raise SystemExit(__doc__.strip().splitlines()[2].strip())
    immagine, insegna = argomenti[0], argomenti[1]
    quante = int(argomenti[2]) if len(argomenti) > 2 else 1
    svg = disegna(immagine, colori=quante)
    fuori = os.path.join(QUI, 'loghi', insegna + '.svg')
    with open(fuori, 'w', encoding='utf-8') as f:
        f.write(svg)
    print('%s — %d byte' % (fuori, len(svg)))


if __name__ == '__main__':
    main(sys.argv[1:])
