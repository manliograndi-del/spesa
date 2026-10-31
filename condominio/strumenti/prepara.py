"""Prepara gli accessi del sito del condominio: un account per alloggio.

Va usato dal gestore sul proprio computer, con la chiave segreta di Supabase
(Project Settings > API Keys > secret / service_role). La chiave non va mai
pubblicata né messa nel sito.

    python prepara.py alloggi --scala1 20 --scala2 20     # crea gli alloggi e le password
    python prepara.py nuova-password S1-07                # password nuova per un alloggio
    python prepara.py gestore S1-07                       # dà a un alloggio il ruolo di gestore
    python prepara.py nome "Condominio dei Tigli"         # nome del condominio

Le password finiscono in riservato/password.csv e riservato/bigliettini.html
(da stampare, ritagliare e mettere nelle buche). Tienili per te.
"""

import argparse
import csv
import html
import json
import os
import secrets
import sys
import urllib.error
import urllib.request
from pathlib import Path

DOMINIO_EMAIL = "alloggi.condominio.example"   # uguale a quello in index.html
PAROLE = """acqua albero aria arancia autunno barca bosco campo cane casa cielo collina conchiglia
duna estate faro fiore fiume foglia fragola gatto giardino grano isola lago lampone luna mare
mela melograno montagna nave neve nuvola oliva onda orto pane pera pesca pino pioggia porto
prato quercia riva rosa sale sasso sole stella strada tavolo tetto torre treno uva valle vela
vento vigna""".split()


def email_di(alloggio):
    return f"{alloggio.lower()}@{DOMINIO_EMAIL}"


def nuova_password():
    return f"{secrets.choice(PAROLE)}-{secrets.choice(PAROLE)}-{secrets.randbelow(900) + 100}"


class Supabase:
    def __init__(self, url, chiave):
        self.url, self.chiave = url.rstrip("/"), chiave

    def chiama(self, metodo, percorso, corpo=None, intestazioni=None):
        h = {"apikey": self.chiave, "Authorization": f"Bearer {self.chiave}", "Content-Type": "application/json"}
        h.update(intestazioni or {})
        dati = json.dumps(corpo).encode() if corpo is not None else None
        richiesta = urllib.request.Request(self.url + percorso, data=dati, headers=h, method=metodo)
        try:
            with urllib.request.urlopen(richiesta, timeout=60) as r:
                testo = r.read()
                return json.loads(testo) if testo else None
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"{metodo} {percorso}: {e.code} {e.read().decode(errors='replace')[:300]}") from e

    def alloggi(self):
        return {a["id"]: a for a in self.chiama("GET", "/rest/v1/alloggi?select=*")}


def salva_password(cartella, righe, nome, indirizzo):
    """Aggiorna password.csv e rigenera i bigliettini da stampare."""
    cartella.mkdir(exist_ok=True)
    csv_path = cartella / "password.csv"
    tutte = {}
    if csv_path.exists():
        with csv_path.open(encoding="utf-8") as f:
            tutte = {r["alloggio"]: r for r in csv.DictReader(f)}
    for r in righe:
        tutte[r["alloggio"]] = r
    ordinate = sorted(tutte.values(), key=lambda r: (int(r["scala"]), int(r["interno"]) if r["interno"].isdigit() else 999, r["interno"]))
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["alloggio", "scala", "interno", "password"])
        w.writeheader()
        w.writerows(ordinate)
    carte = "".join(f"""<div class="c"><b>{html.escape(nome)}</b><span>Sito del condominio</span>
<p>{html.escape(indirizzo)}</p><dl><dt>Scala</dt><dd>{r['scala']}</dd><dt>Interno</dt><dd>{html.escape(r['interno'])}</dd>
<dt>Password</dt><dd class="p">{html.escape(r['password'])}</dd></dl><small>Personale per il tuo alloggio: non darla ad altri.</small></div>"""
                    for r in ordinate)
    (cartella / "bigliettini.html").write_text(f"""<!doctype html><html lang="it"><meta charset="utf-8"><title>Bigliettini</title>
<style>body{{font-family:system-ui,sans-serif;margin:10mm}}.g{{display:grid;grid-template-columns:1fr 1fr;gap:6mm}}
.c{{border:1px dashed #888;padding:5mm;break-inside:avoid;display:flex;flex-direction:column;gap:2mm}}.c b{{font-size:14pt}}
.c span,.c small{{color:#555}}dl{{display:grid;grid-template-columns:auto 1fr;gap:1mm 4mm;margin:0}}dt{{color:#555}}dd{{margin:0;font-weight:700}}
.p{{font-family:ui-monospace,monospace;font-size:13pt}}p{{margin:0;font-family:ui-monospace,monospace}}</style>
<div class="g">{carte}</div></html>""", encoding="utf-8")
    return cartella / "bigliettini.html"


def crea_alloggi(sb, args):
    esistenti = sb.alloggi()
    nuovi = []
    for scala, quanti in ((1, args.scala1), (2, args.scala2)):
        for n in range(1, quanti + 1):
            alloggio = f"S{scala}-{n:02d}"
            if alloggio in esistenti:
                continue
            password = nuova_password()
            utente = sb.chiama("POST", "/auth/v1/admin/users", {"email": email_di(alloggio), "password": password, "email_confirm": True})
            sb.chiama("POST", "/rest/v1/alloggi", {"id": alloggio, "scala": scala, "interno": str(n), "user_id": utente["id"]},
                      {"Prefer": "return=minimal"})
            nuovi.append({"alloggio": alloggio, "scala": str(scala), "interno": str(n), "password": password})
            print("Creato", alloggio)
    if not nuovi:
        print("Gli alloggi esistono già: niente da fare.")
        return
    print("Bigliettini:", salva_password(Path(args.cartella), nuovi, args.nome_bigliettini, args.indirizzo))


def cambia_password(sb, args):
    alloggio = args.alloggio.upper()
    a = sb.alloggi().get(alloggio)
    if not a or not a["user_id"]:
        sys.exit(f"Alloggio {alloggio} non trovato.")
    password = nuova_password()
    sb.chiama("PUT", f"/auth/v1/admin/users/{a['user_id']}", {"password": password})
    print(f"Nuova password per {alloggio}: {password}")
    salva_password(Path(args.cartella), [{"alloggio": alloggio, "scala": str(a["scala"]), "interno": a["interno"], "password": password}],
                   args.nome_bigliettini, args.indirizzo)


def imposta_gestore(sb, args):
    alloggio = args.alloggio.upper()
    if alloggio not in sb.alloggi():
        sys.exit(f"Alloggio {alloggio} non trovato.")
    sb.chiama("PATCH", f"/rest/v1/alloggi?id=eq.{alloggio}", {"gestore": True}, {"Prefer": "return=minimal"})
    print(f"{alloggio} ora è gestore: vedrà la pagina Impostazioni.")


def imposta_nome(sb, args):
    sb.chiama("PATCH", "/rest/v1/impostazioni?id=eq.1", {"nome": args.nome}, {"Prefer": "return=minimal"})
    print("Nome del condominio:", args.nome)


def main():
    p = argparse.ArgumentParser(description="Prepara gli accessi del sito del condominio.")
    p.add_argument("--cartella", default="riservato", help="dove salvare password e bigliettini")
    p.add_argument("--nome-bigliettini", default="Condominio")
    p.add_argument("--indirizzo", default="spesato.it/condominio")
    s = p.add_subparsers(dest="comando", required=True)
    a = s.add_parser("alloggi")
    a.add_argument("--scala1", type=int, default=20)
    a.add_argument("--scala2", type=int, default=20)
    s.add_parser("nuova-password").add_argument("alloggio")
    s.add_parser("gestore").add_argument("alloggio")
    s.add_parser("nome").add_argument("nome")
    args = p.parse_args()
    url, chiave = os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not chiave:
        sys.exit("Imposta SUPABASE_URL e SUPABASE_SERVICE_KEY (vedi LEGGIMI).")
    sb = Supabase(url, chiave)
    try:
        {"alloggi": crea_alloggi, "nuova-password": cambia_password, "gestore": imposta_gestore, "nome": imposta_nome}[args.comando](sb, args)
    except RuntimeError as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
