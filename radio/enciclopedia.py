"""Etere: costruisce enciclopedia_it.json, l'indice delle radio italiane che hanno una voce su it.wikipedia,
abbinate (quando possibile) alle radio ascoltabili su Etere.
Ingresso: .cache/wiki_indice.json (voci lette da it.wikipedia: titolo, Wikidata, anni, area, sede, editore, motto),
stazioni.json e schede.json (catalogo di Etere). Il testo delle schede si legge dal vivo da Wikipedia nella pagina."""
import json, os, re, unicodedata
QUI = os.path.dirname(os.path.abspath(__file__))
leggi = lambda f: json.load(open(os.path.join(QUI, f), encoding='utf-8'))

def norma(t):
    t = unicodedata.normalize('NFD', (t or '').lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '', t)

def chiavi(titolo):
    base = re.sub(r'\s*\(.*?\)\s*', ' ', titolo).strip()
    k = {norma(base)}
    n = norma(base)
    if n.startswith('radio'): k.add(n[5:])
    else: k.add('radio' + n)
    extra = {'rdsemittenteradiotelevisiva': ['rds', 'rdsradiodimensionesuono', 'rds100grandisuccessi'], 'rds': ['rds', 'rdsradiodimensionesuono', 'rds100grandisuccessi'],
             'radio105': ['radio105network', '105'], 'radiomontecarlo': ['radiomontecarlofm', 'rmc', 'radiomontecarloitalia'],
             'radiom2o': ['m2o', 'radiom2o'], 'radioitalia': ['radioitaliasolomusicaitaliana'], 'inblu': ['inblu2000', 'radioinblu'],
             'radiofreccia': ['radiofreccia', 'freccia'], 'radiozeta': ['radiozetalitaliana', 'radiozeta'],
             'virginradio': ['virginradioitalia', 'virginradio'], 'rtl1025': ['rtl1025', 'rtl1025hitradio']}
    for x in list(k):
        k.update(extra.get(x, []))
    return {x for x in k if len(x) > 3}

indice = leggi('.cache/wiki_indice.json')
italiane = []
for f in ('stazioni.json', 'altre.json'):          # il globo carica entrambi i file
    st = leggi(f); C = st['campi']
    italiane += [dict(zip(C, r)) for r in st['radio'] if r[C.index('paese')] == 'IT']
schede = leggi('schede.json')['schede']
per_qid, per_wiki = {}, {}
for uuid, s in schede.items():
    if s.get('paese') != 'IT': continue
    if s.get('wikidata'): per_qid.setdefault(s['wikidata'], []).append(uuid)
    w = (s.get('wikipedia') or {}).get('url', '')
    if 'it.wikipedia.org/wiki/' in w:
        per_wiki.setdefault(w.split('/wiki/')[1].replace('_', ' '), []).append(uuid)
per_uuid = {r['uuid']: r for r in italiane}
per_nome = {}
for r in italiane:
    per_nome.setdefault(norma(r['nome']), []).append(r['uuid'])

def migliore(uuids):
    uu = [u for u in uuids if u in per_uuid]
    return max(uu, key=lambda u: per_uuid[u]['ascolti'] or 0) if uu else None

# correzioni a mano dopo un controllo: voce -> nome esatto della radio su Etere (None = nessun flusso giusto)
A_MANO = {'Controradio (Bari)': None, 'Controradio (Firenze)': 'Controradio',   # controradio.it è quella di Firenze
          'Rai Radio 2': 'RAI 2', 'Rai Radio 1 Sport': 'Radio RaiSport', 'Radio Kiss Kiss': 'Radio Kiss Kiss + 1',
          'Rai Radio 3': None, 'Radio Padova': None}
per_nome_esatto = {}
for r in italiane: per_nome_esatto.setdefault(r['nome'], []).append(r['uuid'])

usate, out, come = set(), [], {'wikidata': 0, 'wikipedia': 0, 'nome': 0, 'inizio': 0, 'nessuno': 0}
for t, q, anno, fine, area, sede, chiusa, web, editore, motto in indice:
    u, via = None, 'nessuno'
    if t in A_MANO:
        u = migliore(per_nome_esatto.get(A_MANO[t], [])) if A_MANO[t] else None
        via = 'a mano'; come.setdefault(via, 0)
        q_, chiusa_ = q, True                         # salta le ricerche automatiche
    else: q_, chiusa_ = q, chiusa
    from urllib.parse import unquote
    if t not in A_MANO and q and per_qid.get(q): u, via = migliore(per_qid[q]), 'wikidata'
    if t not in A_MANO and not u and per_wiki.get(t): u, via = migliore(per_wiki[t]), 'wikipedia'
    if not u and not chiusa_:
        cand = [x for k in chiavi(t) for x in per_nome.get(k, [])]
        if cand: u, via = migliore(cand), 'nome'
    if not u and not chiusa_:                     # «Radio Bruno - Made in Italy»: il nome inizia con quello della voce
        ks = [k for k in chiavi(t) if len(k) >= 7]
        cand = [x for n, uu in per_nome.items() for k in ks if n.startswith(k) and not n[len(k):len(k)+1].isdigit() for x in uu]
        if cand: u, via = migliore(cand), 'inizio'
    if not u and via != 'a mano': via = 'nessuno'
    come[via] += 1
    voce = {'t': t, 'nome': re.sub(r'\s*\(.*?\)\s*$', '', t), 'q': q, 'dal': anno, 'al': fine, 'area': area, 'sede': sede,
            'chiusa': chiusa, 'web': web, 'editore': editore, 'motto': motto}
    if u:
        r = per_uuid[u]; usate.add(u)
        voce.update({'uuid': u, 'etichette': r['generi'] or '', 'ascolti': r['ascolti'] or 0, 'sito': r['sito'] or ''})
    out.append(voce)
out.sort(key=lambda v: norma(v['nome']))
json.dump({'fonte': 'it.wikipedia.org (voci delle emittenti radiofoniche italiane), catalogo radio-browser di Etere',
           'aggiornato': '2026-11-26', 'radio': out},
          open(os.path.join(QUI, 'enciclopedia_it.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(out), 'voci;', come)
for v in out:
    if v.get('uuid'): print('  ', v['t'], '->', per_uuid[v['uuid']]['nome'])
print('SENZA:', ', '.join(v['t'] for v in out if not v.get('uuid') and not v['chiusa']))
