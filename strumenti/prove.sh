#!/bin/bash
# Tutte le prove sulle pagine appena generate. Da lanciare dalla cartella di
# lavoro, dove sta out/. Se una fallisce si ferma: una pagina che non passa
# NON si pubblica.
#
# Serve jsdom, e va installato NEL PROGETTO (node cerca node_modules accanto
# allo script, non accanto alla cartella di lavoro):
#     cd <progetto> && npm install
set -e
S="$(cd "$(dirname "$0")" && pwd)"
for f in out/sito.html out/pagina.html out/spesa-da-sola.html; do
  echo "########## $f"
  node "$S/prova.js" "$f"
  node "$S/prova-collegamenti.js" "$f"
  node "$S/prova-quando.js" "$f"
  node "$S/prova-scorrimento.js" "$f"
  if [ "$f" = out/pagina.html ]; then
    node "$S/prova-testi.js" "$f" --condivisa
  else
    node "$S/prova-testi.js" "$f"
  fi
done
echo "########## un telefono con una lista vecchia"
node "$S/prova-arrivi.js" out/sito.html

echo "########## la lista salvata di prima"
node "$S/prova-maiuscole.js"
echo
echo "tutte le prove passate."
