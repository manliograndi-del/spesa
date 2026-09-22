# -*- coding: utf-8 -*-
"""I marchi dei supermercati, pronti da infilare nella pagina.

Chiesti da Manlio il 2026-09-22: «al posto delle pillole con scritto il nome
dei vari supermercati, mettici i veri loghi». In `strumenti/loghi/` c'è un
file SVG per insegna, e in `FONTI.txt` accanto c'è scritto da dove viene
ognuno e a che licenza. Per aggiungerne uno basta metterlo lì: qui lo trova
da solo. Per toglierlo basta cancellarlo: la pagina torna alla pillola col
nome scritto.

TRE COSE CHE QUESTO FILE DEVE FARE, e per cui esiste:

1. **Rinominare gli id dentro ogni SVG.** Nella pagina finiscono uno accanto
   all'altro dentro lo stesso documento, e due loghi che hanno tutti e due un
   `id="A"` (succede: li esportano da programmi diversi) si rubano le
   sfumature e le maschere a vicenda. Ogni id diventa `l-<insegna>-<id>`.

2. **Togliere larghezza e altezza fisse**, lasciando il `viewBox`: dentro la
   pagina il logo deve stare alto quanto gli si dice, non 136 px.

3. **Fermarsi con un errore se un file non è un SVG.** Un logo scaricato male
   (una pagina d'errore salvata col nome giusto) finirebbe dentro la pagina e
   la spaccherebbe in silenzio.

Va bene anche un'immagine normale (.png, .webp, .jpg) quando di quel marchio
non esiste un disegno libero: diventa un `<img>` con l'immagine scritta dentro
l'indirizzo, così la pagina resta un file solo e funziona senza rete. Il
disegno (SVG) è meglio perché non sgrana, ma non sempre c'è.

Se di un marchio si ha solo un'immagine a un colore pieno, `vettore.py`
accanto a questo file la trasforma in un disegno:

    python3 -m vettore <immagine> <insegna>
"""
import base64, os, re, unicodedata

QUI = os.path.dirname(os.path.abspath(__file__))
CARTELLA = os.path.join(QUI, 'loghi')


def chiave(insegna):
    """«Carrefour Iper» -> «carrefour-iper», «Mercatò» -> «mercato»."""
    piatto = unicodedata.normalize('NFKD', insegna).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', piatto.lower()).strip('-')


def _ripulisci(testo, nome):
    if '<svg' not in testo:
        raise SystemExit(
            'strumenti/loghi/%s.svg non e un SVG (forse e una pagina di errore '
            'salvata col nome giusto). Cancellalo o riscaricalo.' % nome)

    # via tutto quello che sta prima dello <svg>: dichiarazione XML, DOCTYPE,
    # commenti dell'editore con cui e stato fatto
    testo = testo[testo.index('<svg'):]

    # gli id: prima si raccolgono, poi si rinominano ovunque compaiano
    ids = set(re.findall(r'\sid="([^"]+)"', testo))
    for vecchio in sorted(ids, key=len, reverse=True):
        nuovo = 'l-%s-%s' % (nome, re.sub(r'[^A-Za-z0-9_-]', '', vecchio))
        testo = testo.replace('id="%s"' % vecchio, 'id="%s"' % nuovo)
        testo = testo.replace('url(#%s)' % vecchio, 'url(#%s)' % nuovo)
        testo = testo.replace('href="#%s"' % vecchio, 'href="#%s"' % nuovo)

    # niente misure fisse: dentro la pagina il logo si adatta
    apertura = re.match(r'<svg[^>]*>', testo).group(0)
    senza = re.sub(r'\s(?:width|height)="[^"]*"', '', apertura)
    if 'viewBox' not in senza:
        m = re.search(r'\swidth="([\d.]+)"', apertura), re.search(r'\sheight="([\d.]+)"', apertura)
        if m[0] and m[1]:
            senza = senza[:-1] + ' viewBox="0 0 %s %s">' % (m[0].group(1), m[1].group(1))
    # sta dentro un bottone: non deve prendersi il fuoco ne farsi leggere,
    # il nome dell'insegna e scritto accanto per chi usa un lettore di schermo
    senza = senza[:-1] + ' aria-hidden="true" focusable="false" preserveAspectRatio="xMidYMid meet">'
    testo = senza + testo[len(apertura):]

    # meno spazi: di questi ne entrano otto in una pagina che si porta anche
    # una copia di se stessa
    testo = re.sub(r'>\s+<', '><', testo).strip()
    return testo


TIPI = {'.png': 'image/png', '.webp': 'image/webp',
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg'}


def _immagine(percorso, tipo):
    """Un'immagine normale diventa un <img> con dentro l'immagine stessa:
    nessuna richiesta alla rete, e la pagina resta un file solo."""
    with open(percorso, 'rb') as fp:
        dati = base64.b64encode(fp.read()).decode('ascii')
    return ('<img alt="" aria-hidden="true" src="data:%s;base64,%s">' % (tipo, dati))


def carica():
    fuori = {}
    if not os.path.isdir(CARTELLA):
        return fuori
    for f in sorted(os.listdir(CARTELLA)):
        nome, est = os.path.splitext(f)
        est = est.lower()
        percorso = os.path.join(CARTELLA, f)
        if est == '.svg':
            with open(percorso, encoding='utf-8') as fp:
                fuori[nome] = _ripulisci(fp.read(), nome)
        elif est in TIPI:
            fuori[nome] = _immagine(percorso, TIPI[est])
    return fuori


LOGHI = carica()

if __name__ == '__main__':
    for k, v in LOGHI.items():
        print('%-16s %6d byte' % (k, len(v)))
    print('%d marchi' % len(LOGHI))
