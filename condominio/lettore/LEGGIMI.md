# Lettore delle lettere dell'amministratore

Controlla la casella email del sito, prende le lettere dell'amministratore con i PDF allegati e capisce:

- il **tipo** di lettera (convocazione, spese ordinarie, riscaldamento, verbale, altro);
- l'**anno di gestione**;
- per le convocazioni: **prima e seconda convocazione** (data, ora, luogo) e i **punti dell'ordine del giorno**.

Il risultato finisce nella cartella `uscita/`: una sottocartella per lettera con i PDF e una scheda `lettera.json`, più un `archivio.json` con tutto. Il sito leggerà da lì.

## Come capisce le lettere

1. **Regole** (sempre, gratis, senza internet): cerca "ordine del giorno", i punti numerati 1, 2, 3…, le date di prima e seconda convocazione. Con le lettere di un amministratore, che usa sempre lo stesso modello, di solito bastano.
2. **Modello locale** (solo se le regole non trovano i punti): un piccolo modello di intelligenza artificiale che gira sul computer con [Ollama](https://ollama.com). Nessun costo e nessun dato inviato fuori.

Le scansioni (PDF senza testo) vengono lette solo se è installato `ocrmypdf` con la lingua italiana.

## Installazione (una volta sola)

1. Installa **Python 3** da python.org (su Windows spunta "Add Python to PATH").
2. Apri il terminale nella cartella del lettore e scrivi:
   ```
   pip install -r requirements.txt
   ```
3. Per il modello locale: installa **Ollama** da ollama.com, poi scrivi:
   ```
   ollama pull qwen2.5:3b
   ```
   Pesa circa 2 GB e va bene su un computer con 8 GB di RAM. Con 16 GB puoi usare `qwen2.5:7b`, più preciso. Su un computer vecchio, `qwen2.5:1.5b`. Per cambiarlo, modifica `OLLAMA_MODELLO` in `config.txt`.
4. Copia `config.esempio.txt` come `config.txt` e compila indirizzo e password della casella.

## Uso

Prova su un PDF:
```
python lettore.py prova convocazione.pdf
```

Controlla la posta e salva le lettere nuove:
```
python lettore.py posta
```

Opzioni: `--motore regole` (solo regole), `--motore ollama` (solo modello locale), `--motore auto` (predefinito: regole, poi modello se serve).

Per farlo girare da solo, per esempio ogni ora: su Windows con l'Utilità di pianificazione, su Mac/Linux con `cron`. Il computer deve essere acceso: le lettere arrivate mentre è spento vengono lette alla prima accensione.

## Sicurezza

- Vengono lette solo le email il cui mittente è `EMAIL_AMMINISTRATORE`. Se il server di posta segnala che il mittente è falso (`dkim=fail` o `dmarc=fail`), la lettera viene scartata.
- Le email scartate o di altri mittenti restano non lette nella casella.
- `config.txt` contiene la password: non pubblicarlo.
