// Collegamento al database Supabase del condominio.
// Sono dati pubblici per natura (la "publishable key" serve proprio al sito):
// a proteggere i dati sono le password degli alloggi e le regole in supabase/schema.sql.
window.CONDOMINIO = {
  supabaseUrl: "https://ytfjghvsbslawffhzybg.supabase.co",
  supabaseKey: "sb_publishable_RQ72ZTedPwNgBvp_9tP90A_TzuHlo5K",
  // Il condominio ha due blocchi, "Interno 2" e "Interno 4", con alloggi numerati da 1 a 20.
  etichette: { scala: "Interno", alloggio: "alloggio" },
};
