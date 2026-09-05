# -*- coding: utf-8 -*-
"""Cerca il codice rimasto in giro dopo le modifiche.

Manlio, 2026-09-05: «sono state fatte molte modifiche e potrebbe essere
rimasto codice spurio». Ha ragione a sospettarlo: in quattro giorni sono
spariti un tasto delle lingue, una casella per aggiungere prodotti, tre
categorie di prezzi e un modo intero di scegliere.

Guarda quattro cose, e le guarda sulla PAGINA GENERATA, non sul programma
che la genera — è lì che il codice morto pesa davvero:

  1. classi CSS scritte e mai usate (comprese quelle costruite a pezzi)
  2. funzioni e costanti JavaScript dichiarate e mai chiamate
  3. identificatori HTML cercati dal programma e non presenti (o viceversa)
  4. file in strumenti/ che nessuno nomina

Gli identificatori usati SOLO dalle prove non sono orfani: le prove sono un
uso legittimo, e vengono lette anche loro.

Non è un giudice: segnala, e chi legge decide. Certe classi le mette il
browser, certi nomi servono solo alle prove.

    python3 -m pulizia out/sito.html
"""
import os, re, sys

QUI = os.path.dirname(os.path.abspath(__file__))
PROGETTO = os.path.dirname(QUI)

def pezzi(html):
    stile = '\n'.join(re.findall(r'<style>(.*?)</style>', html, re.S))
    script = '\n'.join(re.findall(r'<script>(.*?)</script>', html, re.S))
    corpo = re.sub(r'<(style|script)>.*?</\1>', '', html, flags=re.S)
    return stile, script, corpo

def classi_css(stile):
    stile = re.sub(r'/\*.*?\*/', '', stile, flags=re.S)
    fuori = {}
    for regola in re.findall(r'([^{}]+)\{', stile):
        for c in re.findall(r'\.([A-Za-z][\w-]*)', regola):
            fuori.setdefault(c, regola.strip().split('\n')[0][:60])
    return fuori

def testi_delle_prove():
    """Anche le prove cercano gli identificatori della pagina, e sono un uso
    legittimo: senza questo, `pulizia` segnalava come «mai cercato» un id che
    serviva soltanto a `prova-intestazione.js`. Un attrezzo che grida al lupo
    smette di essere letto."""
    fuori = []
    for f in os.listdir(QUI):
        if f.startswith('prova') and f.endswith(('.js', '.py')):
            fuori.append(open(os.path.join(QUI, f), encoding='utf-8').read())
    return '\n'.join(fuori)

def controlla(percorso):
    html = open(percorso, encoding='utf-8').read()
    prove = testi_delle_prove()
    stile, script, corpo = pezzi(html)
    trovati = []

    # 1. classi CSS mai usate
    usate = set(re.findall(r'class="([^"]*)"', corpo))
    usate = {c for gruppo in usate for c in gruppo.split()}
    usate |= set(re.findall(r"className\s*=\s*'([^']*)'", script))
    usate |= set(re.findall(r'classList\.(?:add|remove|toggle|contains)\(\s*[\'"]([\w-]+)', script))
    usate |= set(re.findall(r'class=\\?"([\w -]+)\\?"', script))
    # Le classi si costruiscono anche a pezzi: `'pag-riga' + (p.url ? ' apribile' : '')`.
    # La prima versione di questo attrezzo dava «.apribile mai usata» ed era falso.
    # Quindi vale come uso anche una parola sola fra apici, ovunque nello script.
    usate |= {w for w in re.findall(r"['\"]\s*([\w-]+)\s*['\"]", script)}
    usate = {c for gruppo in usate for c in str(gruppo).split()}
    for c, dove in sorted(classi_css(stile).items()):
        if c not in usate:
            trovati.append(('classe CSS mai usata', f'.{c}', dove))

    # 2. funzioni e costanti JavaScript mai richiamate
    senza_commenti = re.sub(r'/\*.*?\*/', '', script, flags=re.S)
    senza_commenti = re.sub(r'^\s*//.*$', '', senza_commenti, flags=re.M)
    nomi = set(re.findall(r'^function\s+([A-Za-z_]\w*)', senza_commenti, re.M))
    nomi |= set(re.findall(r'^const\s+([A-Za-z_]\w*)\s*=', senza_commenti, re.M))
    for n in sorted(nomi):
        quante = len(re.findall(r'\b' + re.escape(n) + r'\b', senza_commenti))
        if quante <= 1:
            trovati.append(('nome JavaScript dichiarato e mai usato', n, ''))

    # 3. identificatori cercati e non presenti
    presenti = set(re.findall(r'id="([\w-]+)"', corpo))
    cercati = set(re.findall(r"getElementById\('([\w-]+)'\)", script))
    for i in sorted(cercati - presenti):
        trovati.append(('il programma cerca un id che non c\'è', '#' + i, ''))
    for i in sorted(presenti - cercati):
        if not re.search(r'[\'"#]' + re.escape(i) + r'\b', script + prove):
            trovati.append(('id scritto e mai cercato', '#' + i, ''))

    return trovati

def file_orfani():
    testi = {}
    for base, _, files in os.walk(PROGETTO):
        if '/.git' in base or 'node_modules' in base:
            continue
        for f in files:
            if f.endswith(('.py', '.js', '.sh', '.md', '.json', '.html')):
                try:
                    testi[os.path.join(base, f)] = open(os.path.join(base, f),
                                                        encoding='utf-8', errors='ignore').read()
                except OSError:
                    pass
    fuori = []
    for f in sorted(os.listdir(QUI)):
        if f.startswith('__') or not f.endswith(('.py', '.js', '.sh')):
            continue
        gambo = f.rsplit('.', 1)[0]
        citato = any(f in t or (f.endswith('.py') and re.search(r'\b' + re.escape(gambo) + r'\b', t))
                     for p, t in testi.items() if os.path.basename(p) != f)
        if not citato:
            fuori.append(f)
    return fuori

def python_orfani():
    """Nomi definiti in cima a un modulo e mai nominati da nessun altro file.

    Cerca solo le maiuscole (le costanti) e i `def`: sono quelle che restano in
    giro dopo una modifica, tipo la UNITA che stava in dati.py quando le
    categorie sono passate al catalogo."""
    fuori = []
    moduli = {}
    for f in sorted(os.listdir(QUI)):
        if f.endswith('.py') and not f.startswith(('__', 'prova')):
            moduli[f] = open(os.path.join(QUI, f), encoding='utf-8').read()
    tutto = '\n'.join(v for v in moduli.values())
    for f, testo in moduli.items():
        senza = re.sub(r'"""..*?"""', '', testo, flags=re.S)
        nomi = set(re.findall(r'^([A-Z][A-Z_0-9]{2,})\s*=', senza, re.M))
        nomi |= set(re.findall(r'^def ([a-z_]\w*)', senza, re.M))
        for n in sorted(nomi):
            altrove = len(re.findall(r'\b' + re.escape(n) + r'\b', tutto))
            proprio = len(re.findall(r'\b' + re.escape(n) + r'\b', senza))
            if altrove == proprio and proprio <= 1:
                fuori.append(f'{f}: {n}')
    return fuori

if __name__ == '__main__':
    percorsi = sys.argv[1:] or ['out/sito.html']
    guasti = 0
    for percorso in percorsi:
        trovati = controlla(percorso)
        print(f'== {percorso}')
        if not trovati:
            print('   niente da buttare')
        for tipo, nome, dove in trovati:
            print(f'   {tipo}: {nome}' + (f'   ({dove})' if dove else ''))
        guasti += len(trovati)
    orfani = file_orfani()
    print('== file in strumenti/ che nessuno nomina')
    print('   ' + (', '.join(orfani) if orfani else 'nessuno'))
    py = python_orfani()
    print('== nomi Python definiti e mai usati')
    print('   ' + ('\n   '.join(py) if py else 'nessuno'))
    print(f'\n{guasti} segnalazioni sulla pagina, {len(orfani)} file orfani, '
          f'{len(py)} nomi Python inutilizzati.')
