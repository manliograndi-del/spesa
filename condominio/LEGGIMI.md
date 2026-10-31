# Sito del condominio

Indirizzo: **spesato.it/condominio**

- `index.html`, `app.js`, `stile.css`: il sito.
- `config.js`: indirizzo e chiave pubblica del database (Supabase).
- `supabase/schema.sql`: tabelle e regole di accesso, da incollare una volta in Supabase.
- `strumenti/prepara.py`: crea gli account dei 40 alloggi e i bigliettini con le password.
- `lettore/`: legge le email dell'amministratore e le pubblica sul sito. Gira da solo ogni ora su GitHub (`.github/workflows/condominio-lettere.yml`).

Il codice è pubblico, ma non contiene password né chiavi segrete. I dati (lettere, osservazioni, voti) stanno su Supabase e li vede solo chi entra con la password di un alloggio.

## Messa in funzione (una volta sola)

### 1. Database (Supabase, gratis)
1. Vai su supabase.com, scegli **Start your project** ed entra con il tuo account GitHub.
2. **New project**: nome `condominio`, una password del database (conservala), regione **Europe (Frankfurt)**. Aspetta un paio di minuti.
3. Menu **SQL Editor**, poi **New query**: incolla tutto il contenuto di `supabase/schema.sql` e premi **Run**. Deve comparire "Success".
4. Menu **Authentication**, impostazioni di accesso: **disattiva le nuove iscrizioni** ("Allow new users to sign up"). Gli account li crea solo `prepara.py`.
5. **Project Settings**, sezione **API Keys** (o **Data API**): ti servono tre cose:
   - l'indirizzo del progetto (Project URL, tipo `https://abcd.supabase.co`);
   - la chiave **publishable** (`sb_publishable_…`): è pubblica, va in `config.js`;
   - la chiave **secret** (`sb_secret_…`): è segreta, non va mai nel sito né in chat pubbliche.

### 2. Account degli alloggi e bigliettini
Sul computer, con Python installato:
```
SUPABASE_URL=https://abcd.supabase.co SUPABASE_SERVICE_KEY=sb_secret_... python prepara.py --nome-bigliettini "Condominio ..." alloggi --scala1 20 --scala2 20
SUPABASE_URL=... SUPABASE_SERVICE_KEY=... python prepara.py gestore S1-07       # il tuo alloggio
SUPABASE_URL=... SUPABASE_SERVICE_KEY=... python prepara.py nome "Condominio ..."
```
(Su Windows si scrive prima `set SUPABASE_URL=...` e `set SUPABASE_SERVICE_KEY=...`, poi il comando.)

Le password finiscono in `riservato/bigliettini.html`: stampalo, ritaglia e metti ogni bigliettino nella buca giusta. Per una password persa: `python prepara.py nuova-password S1-07`.

### 3. Casella per le lettere (Gmail, gratis)
1. Crea un Gmail apposta, per esempio `lettere.condominio...@gmail.com`.
2. Attiva la **verifica in due passaggi**, poi crea una **password per le app** (Account Google > Sicurezza > Password per le app). È quella che usa il lettore.
3. Chiedi all'amministratore di mettere questo indirizzo in copia quando manda le lettere.

### 4. Lettore automatico (GitHub)
Nel repository `spesa`: **Settings > Secrets and variables > Actions > New repository secret**, e crea:

| Nome | Valore |
|---|---|
| `CONDOMINIO_IMAP_UTENTE` | l'indirizzo Gmail |
| `CONDOMINIO_IMAP_PASSWORD` | la password per le app di Gmail |
| `CONDOMINIO_SUPABASE_URL` | l'indirizzo del progetto Supabase |
| `CONDOMINIO_SUPABASE_SECRET_KEY` | la chiave secret di Supabase |

Per provarlo subito: scheda **Actions > Lettere del condominio > Run workflow**.

### 5. Ultimi ritocchi dal sito
Entra con la password del tuo alloggio, poi apri **Impostazioni**: email dell'amministratore (il lettore accetta solo le sue email), mese di inizio della gestione, rappresentante di ogni scala, oppure bacheca automatica.

## Note
- Supabase gratuito si sospende dopo una settimana senza attività: il lettore, che lo usa ogni ora, lo tiene attivo.
- Se una lettera non arriva per email, il gestore può aggiungerla a mano da **Documenti > Aggiungi una lettera a mano**.
- Le convocazioni ufficiali restano quelle per posta: il sito serve solo a informarsi e a discutere.
