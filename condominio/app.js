"use strict";
/* Sito del condominio: accesso per alloggio, lettere dell'amministratore, assemblee,
   osservazioni al rappresentante di scala (o bacheca automatica) e sondaggi.
   I dati stanno su Supabase; le regole di accesso sono in supabase/schema.sql. */

const DOMINIO_EMAIL = "alloggi.condominio.example"; // uguale a strumenti/prepara.py
const TIPI = { convocazione: "Convocazione", ordinaria: "Spese ordinarie", riscaldamento: "Riscaldamento", verbale: "Verbale", altro: "Altro" };
const ESITI = { "": "Da discutere", approvato: "Approvato", respinto: "Respinto", rinviato: "Rinviato" };
const MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"];
const VOTI = [["fav", "Favorevole"], ["contr", "Contrario"], ["ns", "Non so"]];

/* ---------- utilità ---------- */
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const isDate = (s) => typeof s === "string" && /^\d{4}-\d{2}-\d{2}$/.test(s);
const oggi = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; };
const parseD = (s) => { const [y, m, d] = s.split("-").map(Number); return new Date(y, m - 1, d); };
const fmtD = (s, o = { day: "numeric", month: "long", year: "numeric" }) => (isDate(s) ? new Intl.DateTimeFormat("it-IT", o).format(parseD(s)) : "");
const fmtS = (s) => fmtD(String(s || "").slice(0, 10), { day: "numeric", month: "short", year: "numeric" });
const fmtL = (s) => fmtD(s, { weekday: "long", day: "numeric", month: "long", year: "numeric" });
const giorni = (d) => Math.round((parseD(d) - parseD(oggi())) / 86400000);
const short = (t, n = 60) => (t.length > n ? t.slice(0, n - 2) + "…" : t);
const val = (id) => document.getElementById(id)?.value ?? "";
const nomeFile = (n) => n.replace(/\.[a-z0-9]+$/i, "").replace(/[_]+/g, " ");
const sicuro = (n) => n.normalize("NFKD").replace(/[^\w.\-]+/g, "_").slice(-80) || "file";
function gestioneDa(d, mese) {
  const dt = parseD(d), y = dt.getFullYear();
  if (mese === 1) return String(y);
  return dt.getMonth() + 1 >= mese ? `${y}/${y + 1}` : `${y - 1}/${y}`;
}

/* ---------- stato ---------- */
const CFG = window.CONDOMINIO || {};
let sb = null;
const S = { pronto: false, nonCollegato: false, accesso: null, utente: null, io: null, imp: null, alloggi: [], lettere: [], assemblee: [], punti: [], oss: [], cond: [], miei: {}, conti: {} };
const UI = { docGest: null, docTipo: "tutti", tab: "nuove", sharing: null, prep: null, editing: null, confirm: null, files: {}, busy: false, toast: null, erroreAccesso: "", nuovaLettera: false };

const allog = (id) => S.alloggi.find((a) => a.id === id);
const modo = (scala) => (S.imp?.modo_scala?.[String(scala)] === "automatica" ? "automatica" : "rappresentante");
const rappDi = (scala) => S.alloggi.find((a) => a.scala === scala && a.rappresentante);
const nomeRapp = (scala) => rappDi(scala)?.nome_rappresentante || "il rappresentante";
const isRapp = () => !!S.io?.rappresentante;
const isGestore = () => !!S.io?.gestore;
const assById = (id) => S.assemblee.find((a) => a.id === id);
const puntoById = (id) => S.punti.find((p) => p.id === id);
const letteraById = (id) => S.lettere.find((l) => l.id === id);
const puntiDi = (aid) => S.punti.filter((p) => p.assemblea_id === aid).sort((a, b) => a.numero - b.numero);
const condDi = (pid) => S.cond.filter((c) => c.punto_id === pid);
const scalaDi = (alloggioId) => allog(alloggioId)?.scala;
const bachecaDi = (pid) => S.oss.filter((o) => o.punto_id === pid && modo(scalaDi(o.alloggio_id)) === "automatica");
const conto = (id) => S.conti[id] || { fav: 0, contr: 0, ns: 0 };
const etichettaAlloggio = (id) => { const a = allog(id); return a ? `Scala ${a.scala}, interno ${a.interno}` : ""; };
function prossima() {
  const t = oggi();
  return S.assemblee.filter((a) => a.data_riferimento >= t).sort((a, b) => (a.data_riferimento < b.data_riferimento ? -1 : 1))[0] || null;
}
// Documenti utili per un'assemblea: gli allegati della convocazione e le lettere di spese arrivate nei 75 giorni prima.
function documentiDi(a) {
  const out = [];
  const conv = letteraById(a.lettera_id);
  if (conv) conv.allegati.forEach((f) => out.push({ lettera: conv, file: f }));
  const da = new Date(parseD(a.data_riferimento) - 75 * 86400000).toISOString().slice(0, 10);
  S.lettere.filter((l) => l.id !== a.lettera_id && ["ordinaria", "riscaldamento"].includes(l.tipo) && l.arrivata >= da && l.arrivata <= a.data_riferimento)
    .forEach((l) => l.allegati.forEach((f) => out.push({ lettera: l, file: f })));
  return out;
}

/* ---------- dati ---------- */
const q = (p) => p.then((r) => { if (r.error) throw r.error; return r.data; });

async function avvio() {
  if (!CFG.supabaseUrl || !CFG.supabaseKey || !window.supabase) { S.nonCollegato = true; S.pronto = true; render(); return; }
  sb = window.supabase.createClient(CFG.supabaseUrl, CFG.supabaseKey);
  try {
    const { data } = await sb.auth.getSession();
    if (data.session) { S.utente = data.session.user; await carica(); } else await caricaAccesso();
  } catch (e) { await esci(); toast(errore(e), true); }
  S.pronto = true; render();
}
async function caricaAccesso() {
  try { S.accesso = await q(sb.rpc("pagina_accesso")); } catch { S.accesso = { nome: "", alloggi: [] }; }
  document.title = S.accesso.nome || "Sito del condominio";
}
async function carica() {
  const [alloggi, imp, lettere, assemblee, punti, oss, cond, voti, conti] = await Promise.all([
    q(sb.from("alloggi").select("*")),
    q(sb.from("impostazioni").select("*").maybeSingle()),
    q(sb.from("lettere").select("*").order("arrivata", { ascending: false })),
    q(sb.from("assemblee").select("*")),
    q(sb.from("punti").select("*")),
    q(sb.from("osservazioni").select("*").order("creata_il")),
    q(sb.from("condivisioni").select("*").order("creata_il")),
    q(sb.from("voti").select("*")),
    q(sb.rpc("conteggi")),
  ]);
  Object.assign(S, { alloggi, imp, lettere, assemblee, punti, oss, cond });
  S.io = alloggi.find((a) => a.user_id === S.utente.id) || null;
  S.miei = Object.fromEntries(voti.map((v) => [v.oggetto_id, v.scelta]));
  S.conti = Object.fromEntries((conti || []).map((c) => [c.oggetto_id, c]));
  document.title = imp?.nome || "Sito del condominio";
}
async function esci() {
  try { await sb?.auth.signOut(); } catch { /* sessione già scaduta */ }
  Object.assign(S, { utente: null, io: null, imp: null, alloggi: [], lettere: [], assemblee: [], punti: [], oss: [], cond: [], miei: {}, conti: {} });
  await caricaAccesso();
}
function errore(e) {
  const m = e?.message || "";
  if (/Accesso negato/.test(m)) return "Non hai il permesso per questa operazione.";
  if (/chiuso/.test(m)) return "Il sondaggio è chiuso.";
  if (/JWT|token|session/i.test(m)) return "La sessione è scaduta: entra di nuovo.";
  if (/fetch|network/i.test(m)) return "Connessione assente: controlla internet e riprova.";
  return "Operazione non riuscita. Riprova tra poco." + (m ? ` (${m.slice(0, 120)})` : "");
}
function toast(t, bad = false) { UI.toast = { t, bad }; render(); clearTimeout(toast.h); toast.h = setTimeout(() => { UI.toast = null; render(); }, 5000); }
async function azione(fn, ok) {
  if (UI.busy) return;
  UI.busy = true; render();
  try { await fn(); await carica(); if (ok) toast(ok); } catch (e) { toast(errore(e), true); } finally { UI.busy = false; render(); }
}

/* ---------- routing e render ---------- */
function route() {
  const h = decodeURIComponent(location.hash.slice(1)); let m;
  if ((m = h.match(/^(doc|ass|punto)-([0-9a-f-]{36})$/))) return { name: m[1], id: m[2] };
  return { name: ["documenti", "assemblee", "osservazioni", "bacheca", "impostazioni"].includes(h) ? h : "home" };
}
function render() {
  const saved = {};
  document.querySelectorAll("#app input[id], #app textarea[id], #app select[id]").forEach((el) => { if (el.type !== "file") saved[el.id] = el.type === "checkbox" ? el.checked : el.value; });
  const act = document.activeElement?.id;
  let html;
  if (!S.pronto) html = `<div class="in"><p class="caricamento">Caricamento…</p></div>`;
  else if (S.nonCollegato) html = `<div class="in accesso"><div class="accesso-card"><h1>Sito non ancora collegato</h1><p>Manca il collegamento al database: compila <code>config.js</code> con indirizzo e chiave del progetto Supabase.</p></div></div>`;
  else if (!S.utente) html = viewAccesso();
  else if (!S.io) html = `<div class="in accesso"><div class="accesso-card"><h1>Account non collegato</h1><p>Questo account non corrisponde a nessun alloggio.</p><div class="row-btns"><button class="btn" data-act="esci">Esci</button></div></div></div>`;
  else html = header() + `<main class="in">${view()}</main>`;
  document.getElementById("app").innerHTML = html + (UI.toast ? `<div class="toast ${UI.toast.bad ? "bad" : ""}" role="status">${esc(UI.toast.t)}</div>` : "");
  for (const [id, v] of Object.entries(saved)) { const el = document.getElementById(id); if (el && !el.dataset.fresco) { if (el.type === "checkbox") el.checked = v; else el.value = v; } }
  if (act) document.getElementById(act)?.focus({ preventScroll: true });
}

function viewAccesso() {
  const al = S.accesso?.alloggi || [];
  const scale = [...new Set(al.map((a) => a.scala))];
  const scelta = Number(document.getElementById("acc-scala")?.value) || scale[0];
  return `<div class="in accesso"><div class="accesso-card">
    <h1>${esc(S.accesso?.nome || "Sito del condominio")}</h1>
    <p>Lo spazio dei proprietari per prepararsi alle assemblee.</p>
    <ul><li><b>Tutte le lettere, i preventivi e i consuntivi dell'amministratore.</b></li><li><b>Per ogni assemblea: i punti da discutere, con i documenti allegati.</b></li><li><b>La possibilità di dire la propria sui punti e di allegare preventivi.</b></li></ul>
    <p class="note"><b>Non sostituisce niente.</b> Le comunicazioni ufficiali continuano ad arrivare per posta, come sempre.</p>
    ${al.length ? `<form class="form" data-form="accedi">
      <div class="riga2"><label>Scala<select id="acc-scala" data-change="render">${scale.map((s) => `<option value="${s}">Scala ${s}</option>`).join("")}</select></label>
      <label>Interno<select id="acc-int">${al.filter((a) => a.scala === scelta).map((a) => `<option value="${esc(a.interno)}">${esc(a.interno)}</option>`).join("")}</select></label></div>
      <label>Password<input type="password" id="acc-pw" class="password" autocomplete="current-password" autocapitalize="none" autocorrect="off" spellcheck="false" placeholder="come sul bigliettino"></label>
      <label class="check"><input type="checkbox" id="acc-mostra" data-change="mostra-pw"> Mostra la password</label>
      ${UI.erroreAccesso ? `<p class="errore" role="alert">${esc(UI.erroreAccesso)}</p>` : ""}
      <div class="row-btns"><button class="btn primary" type="submit" ${UI.busy ? "disabled" : ""}>${UI.busy ? "Accesso…" : "Entra"}</button></div>
      <p class="small muted">La password è sul bigliettino consegnato al tuo alloggio. Se l'hai persa, chiedine una nuova al gestore del sito.</p>
    </form>` : `<p class="note">Il sito non è ancora pronto: gli alloggi non sono stati creati.</p>`}
  </div></div>`;
}
function header() {
  const r = route().name;
  const cur = { doc: "documenti", ass: "assemblee", punto: "home" }[r] || r;
  const nuove = isRapp() ? S.oss.filter((o) => scalaDi(o.alloggio_id) === S.io.scala && o.stato === "nuova").length : 0;
  const tabs = [["home", "Prossima assemblea"], ["documenti", "Documenti"], ["assemblee", "Assemblee"]];
  if (modo(S.io.scala) === "automatica") tabs.push(["bacheca", "Bacheca"]);
  else tabs.push(["osservazioni", isRapp() ? `Osservazioni ricevute${nuove ? ` <span class="count">${nuove}</span>` : ""}` : "Le mie osservazioni"]);
  if (isGestore()) tabs.push(["impostazioni", "Impostazioni"]);
  const ruoli = [isRapp() && "rappresentante", isGestore() && "gestore"].filter(Boolean).join(" · ");
  return `<header class="top"><div class="in top-in">
    <a href="#home" class="brand-name">${esc(S.imp?.nome || "Condominio")}</a>
    <div class="who"><span><b>Scala ${S.io.scala}, interno ${esc(S.io.interno)}</b>${ruoli ? ` · ${ruoli}` : ""}</span><button class="btn quiet" data-act="esci">Esci</button></div>
  </div><nav class="nav" aria-label="Sezioni"><div class="in">${tabs.map(([k, l]) => `<a href="#${k}" class="${cur === k ? "on" : ""}"${cur === k ? ' aria-current="page"' : ""}>${l}</a>`).join("")}</div></nav></header>`;
}
function view() {
  const r = route();
  if (r.name === "doc") return viewDoc(r.id);
  if (r.name === "ass") return viewAss(r.id);
  if (r.name === "punto") return viewPunto(r.id);
  if (r.name === "documenti") return viewDocumenti();
  if (r.name === "assemblee") return viewAssemblee();
  if (r.name === "bacheca") return viewBacheca();
  if (r.name === "osservazioni") return isRapp() ? viewRicevute() : viewMie();
  if (r.name === "impostazioni" && isGestore()) return viewImpostazioni();
  return viewHome();
}

/* ---------- pezzi comuni ---------- */
function calBlock(d) {
  const dt = parseD(d);
  return `<div class="cal" aria-hidden="true"><div class="cal-m">${MESI[dt.getMonth()].slice(0, 3)}</div><div class="cal-d">${dt.getDate()}</div><div class="cal-w">${new Intl.DateTimeFormat("it-IT", { weekday: "short" }).format(dt)}</div></div>`;
}
function convRows(a) {
  const riga = (lab, c) => (c && isDate(c.data) ? `<dt>${lab}</dt><dd>${esc(fmtL(c.data))}${c.ora ? `, ore ${esc(c.ora)}` : ""}${c.luogo ? ` — ${esc(c.luogo)}` : ""}</dd>` : "");
  return `<dl class="conv">${riga("1ª conv.", a.prima)}${riga("2ª conv.", a.seconda)}</dl>`;
}
const docChip = (l) => `<span class="chip t-${l.tipo}">${TIPI[l.tipo] || "Altro"}</span>`;
const fileBtn = (f, da) => `<button class="file" data-act="apri" data-v="${esc(f.percorso)}"><span class="file-ico">${/\.pdf$/i.test(f.nome) ? "PDF" : "FOTO"}</span><span class="file-name">${esc(nomeFile(f.nome))}</span>${da ? `<span class="file-from">${esc(da)}</span>` : ""}</button>`;
function docItem(l) {
  return `<a class="item" href="#doc-${l.id}"><span class="item-title">${esc(l.oggetto || TIPI[l.tipo])}</span><span class="item-side">${esc(fmtS(l.data_lettera || l.arrivata))}</span>
    <span class="item-meta">${docChip(l)}<span>Gestione ${esc(l.gestione)}</span>${l.allegati.length ? `<span>${l.allegati.length} ${l.allegati.length === 1 ? "allegato" : "allegati"}</span>` : ""}</span></a>`;
}
function odgList(a) {
  const fut = a.data_riferimento >= oggi();
  return `<ol class="odg">${puntiDi(a.id).map((p) => {
    const bits = [];
    if (p.esito) bits.push(`<span class="chip ${p.esito === "approvato" ? "c-ok" : p.esito === "respinto" ? "c-no" : "c-wait"}">${ESITI[p.esito]}</span>`);
    const cs = condDi(p.id), bb = bachecaDi(p.id);
    if (cs.length) bits.push(`<span>${cs.length} ${cs.length === 1 ? "osservazione condivisa" : "osservazioni condivise"}</span>`);
    if (bb.length) bits.push(`<span>${bb.length} ${bb.length === 1 ? "messaggio" : "messaggi"} in bacheca</span>`);
    if (fut && cs.some((c) => c.domanda && c.aperto)) bits.push(`<span class="chip c-new">Sondaggio aperto</span>`);
    return `<li><a href="#punto-${p.id}"><span class="odg-n">${p.numero}.</span><span class="odg-t">${esc(p.titolo)}</span>${bits.length ? `<span class="odg-d">${bits.join("")}</span>` : ""}</a></li>`;
  }).join("") || `<li class="empty">Nessun punto.</li>`}</ol>`;
}
function bars(c, mio) {
  const t = c.fav + c.contr + c.ns;
  const bar = (k, lab) => { const n = c[k], pc = t ? Math.round((n / t) * 100) : 0; return `<div class="bar v-${k}"><span>${lab}</span><span class="bar-track"><span class="bar-fill" style="width:${pc}%"></span></span><span class="num">${n} · ${pc}%</span></div>`; };
  return `<div class="bars">${bar("fav", "Favorevoli")}${bar("contr", "Contrari")}${bar("ns", "Non so")}</div><div class="status"><span>${t} ${t === 1 ? "alloggio ha" : "alloggi hanno"} risposto</span>${mio ? `<span>Il tuo voto: ${VOTI.find((v) => v[0] === mio)[1]}</span>` : ""}</div>`;
}
function condCard(c, conLink) {
  const p = puntoById(c.punto_id), a = p && assById(p.assemblea_id);
  const fut = a && a.data_riferimento >= oggi();
  const mia = isRapp() && c.scala === S.io.scala && fut;
  const mio = S.miei[c.id];
  let html = `<article class="share"><div class="share-head"><b>${esc(nomeRapp(c.scala))}</b><span>rappresentante Scala ${c.scala}</span><span>${esc(fmtS(c.creata_il))}</span>
    ${conLink && p ? `<a href="#punto-${p.id}">Punto ${p.numero}: ${esc(short(p.titolo))}</a>` : ""}</div>
    <p class="share-text">${esc(c.testo)}</p>${c.allegati.length ? `<div class="files">${c.allegati.map((f) => fileBtn(f, "allegato da un condomino")).join("")}</div>` : ""}`;
  if (c.domanda) {
    const aperto = c.aperto && fut;
    html += `<div class="poll"><div class="poll-q">${esc(c.domanda)}</div>
      ${aperto ? `<div class="votes" role="group" aria-label="Il tuo voto">${VOTI.map(([k, l]) => `<button class="vote v-${k} ${mio === k ? "on" : ""}" data-act="vota" data-id="${c.id}" data-v="${k}" aria-pressed="${mio === k}" ${UI.busy ? "disabled" : ""}>${l}</button>`).join("")}</div>
      <p class="small muted">Un voto per alloggio, che puoi cambiare finché il sondaggio è aperto. Non è un voto ufficiale: serve a capire cosa ne pensano i proprietari.</p>` : `<span class="chip">Sondaggio chiuso</span>`}
      ${bars(conto(c.id), mio)}</div>`;
  }
  if (c.inoltrata) html += `<div class="status"><span class="chip c-ok">Inoltrata all'amministratore il ${esc(fmtS(c.inoltrata))}</span></div>`;
  if (mia) {
    html += `<div class="row-btns">${!c.inoltrata ? `<button class="btn primary" data-act="prep" data-id="${c.id}">Prepara per l'amministratore</button>` : ""}${c.domanda && c.aperto ? `<button class="btn quiet" data-act="chiudi" data-id="${c.id}">Chiudi il sondaggio</button>` : ""}</div>`;
    if (UI.prep === c.id) html += prepBox(c);
  }
  return html + `</article>`;
}
function testoAmm(c) {
  const p = puntoById(c.punto_id), a = assById(p.assemblea_id), k = conto(c.id);
  const t = k.fav + k.contr + k.ns;
  const oggetto = `Assemblea del ${fmtD(a.data_riferimento)} – osservazione dei condomini sul punto ${p.numero}`;
  const corpo = `Gentile Amministratore,

in vista dell'assemblea del ${fmtD(a.data_riferimento)}, Le segnalo un'osservazione dei condomini sul punto ${p.numero} dell'ordine del giorno ("${p.titolo}"):

${c.testo}
${c.domanda ? `\nSondaggio tra i proprietari sul sito del condominio (indicativo, non vincolante): "${c.domanda}" — ${k.fav} favorevoli, ${k.contr} contrari, ${k.ns} non so, su ${t} alloggi che hanno risposto.\n` : ""}
Le chiedo, se possibile, di tenerne conto nella preparazione dell'assemblea.

Cordiali saluti,
${nomeRapp(c.scala)} – rappresentante Scala ${c.scala}`;
  return { oggetto, corpo };
}
function prepBox(c) {
  const { oggetto, corpo } = testoAmm(c);
  const mail = S.imp?.email_amministratore || "";
  const href = `mailto:${encodeURIComponent(mail)}?subject=${encodeURIComponent(oggetto)}&body=${encodeURIComponent(corpo)}`;
  return `<div class="prep"><b>Email per l'amministratore${mail ? ` (${esc(mail)})` : ""}</b>
    <p class="small muted">Il testo è già pronto. Aprilo nella tua email e invialo, oppure copialo. Poi segna l'osservazione come inoltrata.</p>
    <textarea id="prep-${c.id}" readonly>Oggetto: ${esc(oggetto)}\n\n${esc(corpo)}</textarea>
    <div class="row-btns"><a class="btn primary" href="${esc(href)}">Apri nella mia email</a><button class="btn" data-act="copia" data-id="${c.id}">Copia il testo</button><button class="btn" data-act="inoltrata" data-id="${c.id}">Segna come inoltrata</button><button class="btn quiet" data-act="prep-chiudi">Chiudi</button></div></div>`;
}
function bachecaCard(o, conLink) {
  const p = puntoById(o.punto_id), mio = S.miei[o.id], k = conto(o.id);
  const a = p && assById(p.assemblea_id), aperto = a && a.data_riferimento >= oggi();
  return `<article class="share"><div class="share-head"><b>${esc(etichettaAlloggio(o.alloggio_id))}${o.alloggio_id === S.io.id ? " (tu)" : ""}</b><span>${esc(fmtS(o.creata_il))}</span>${conLink && p ? `<a href="#punto-${p.id}">Punto ${p.numero}: ${esc(short(p.titolo))}</a>` : ""}</div>
    <p class="share-text">${esc(o.testo)}</p>${o.allegati.length ? `<div class="files">${o.allegati.map((f) => fileBtn(f)).join("")}</div>` : ""}
    <div class="votes" role="group" aria-label="Il tuo parere">${VOTI.map(([v, l]) => `<button class="vote mini v-${v} ${mio === v ? "on" : ""}" ${aperto ? `data-act="vota" data-id="${o.id}" data-v="${v}"` : "disabled"} aria-pressed="${mio === v}">${l}<span class="n">${k[v]}</span></button>`).join("")}</div>
    ${o.alloggio_id === S.io.id && aperto ? `<div>${conferma("cancella-oss", o.id, "Cancella il mio messaggio")}</div>` : ""}</article>`;
}
function conferma(act, id, label) {
  const armato = UI.confirm === act + id;
  return `<button class="btn ${armato ? "primary" : "quiet"} danger" data-act="${act}" data-id="${id}">${armato ? "Conferma" : label}</button>`;
}
function scelti(chiave) {
  const fs = UI.files[chiave] || [];
  return fs.length ? `<div class="scelti">${fs.map((f, i) => `<span>${esc(f.name)}<button data-act="file-via" data-id="${chiave}" data-v="${i}" aria-label="Togli ${esc(f.name)}">×</button></span>`).join("")}</div>` : "";
}
function ossForm(pid) {
  const a = prossima();
  if (!a) return "";
  const auto = modo(S.io.scala) === "automatica";
  const k = pid || "x";
  const rapp = rappDi(S.io.scala);
  return `<section class="panel"><h3>${auto ? "Scrivi in bacheca" : isRapp() ? "Aggiungi una tua osservazione" : "Scrivi un'osservazione al tuo rappresentante"}</h3>
    <p class="small muted">${auto ? "Il messaggio compare subito in bacheca, visibile a tutti i proprietari con la tua scala e il tuo interno."
      : isRapp() ? "La trovi tra le osservazioni nuove: da lì puoi condividerla con tutti."
      : rapp ? `La legge solo ${esc(rapp.nome_rappresentante || "il rappresentante")}, rappresentante della Scala ${S.io.scala}. Se la ritiene di interesse generale la condivide con tutti, senza il tuo nome, e può aprire un sondaggio.`
      : `La Scala ${S.io.scala} non ha ancora un rappresentante: la tua osservazione verrà letta quando sarà indicato.`}</p>
    <div class="form">${pid ? "" : `<label>Su quale punto?<select id="os-pt">${puntiDi(a.id).map((p) => `<option value="${p.id}">${p.numero}. ${esc(short(p.titolo, 70))}</option>`).join("")}</select></label>`}
      <label>${auto ? "Il tuo messaggio" : "La tua osservazione"}<textarea id="os-t-${k}" maxlength="4000" placeholder="Una proposta, un dubbio, un'informazione utile…"></textarea></label>
      <label>Allega preventivi o documenti (PDF o foto, facoltativo)<input type="file" id="os-f-${k}" data-file="${k}" accept="application/pdf,image/jpeg,image/png,image/webp" multiple></label>
      ${scelti(k)}
      <div class="row-btns"><button class="btn primary" data-act="invia-oss" data-id="${k}" ${UI.busy ? "disabled" : ""}>${UI.busy ? "Invio…" : auto ? "Pubblica in bacheca" : "Invia"}</button></div></div></section>`;
}

/* ---------- pagine ---------- */
function viewHome() {
  const a = prossima();
  const auto = modo(S.io.scala) === "automatica";
  const nuove = isRapp() ? S.oss.filter((o) => scalaDi(o.alloggio_id) === S.io.scala && o.stato === "nuova").length : 0;
  let extra = "";
  if (a) {
    const pids = new Set(puntiDi(a.id).map((p) => p.id));
    const aperti = S.cond.filter((c) => pids.has(c.punto_id) && c.domanda && c.aperto);
    const bacheca = S.oss.filter((o) => pids.has(o.punto_id) && modo(scalaDi(o.alloggio_id)) === "automatica").slice(-3).reverse();
    if (aperti.length) extra += `<section><h2>Sondaggi aperti</h2>${aperti.map((c) => condCard(c, true)).join("")}</section>`;
    if (bacheca.length) extra += `<section><div class="sec-head"><h2>Ultimi messaggi in bacheca</h2>${auto ? `<a class="small" href="#bacheca">Tutta la bacheca</a>` : ""}</div>${bacheca.map((o) => bachecaCard(o, true)).join("")}</section>`;
  }
  const ultimi = S.lettere.slice(0, 4);
  return `${nuove ? `<div class="note"><b>${nuove} ${nuove === 1 ? "osservazione nuova" : "osservazioni nuove"}</b> dalla Scala ${S.io.scala}. <a href="#osservazioni">Guardale</a>: ti basta scegliere se condividerle.</div>` : ""}
  <section><div class="sec-head"><h2>Prossima assemblea</h2>${a && a.lettera_id ? `<a class="small" href="#doc-${a.lettera_id}">Lettera di convocazione</a>` : ""}</div>
  ${a ? `<div class="panel"><div class="next">${calBlock(a.data_riferimento)}<div class="form" style="gap:10px">
      <div class="row-btns"><span class="chip t-convocazione">Assemblea ${esc(a.tipo)}</span><span class="small muted">${giorni(a.data_riferimento) > 1 ? `tra ${giorni(a.data_riferimento)} giorni` : giorni(a.data_riferimento) === 1 ? "domani" : "oggi"}</span></div>${convRows(a)}</div></div>
      <div><h3 style="margin-bottom:8px">Ordine del giorno</h3>${odgList(a)}</div>
      <p class="small muted">Riassunto ricavato in automatico dalla lettera. Fa fede la convocazione arrivata per posta.</p></div>`
    : `<div class="empty">Nessuna assemblea in programma. Quando arriva una convocazione, qui compaiono la data e i punti da discutere.</div>`}</section>
  ${extra}
  <section><div class="sec-head"><h2>Ultimi documenti arrivati</h2><a class="small" href="#documenti">Tutti i documenti</a></div>
  ${ultimi.length ? `<div class="list">${ultimi.map(docItem).join("")}</div>` : `<div class="empty">Ancora nessuna lettera dell'amministratore.</div>`}</section>`;
}
function viewDocumenti() {
  const gs = [...new Set(S.lettere.map((l) => l.gestione))].sort().reverse();
  if (!gs.length) return `<section><h1>Documenti</h1><div class="empty">Ancora nessuna lettera dell'amministratore.</div></section>${isGestore() ? formLettera() : ""}`;
  const g = gs.includes(UI.docGest) ? UI.docGest : gs[0];
  const inG = S.lettere.filter((l) => l.gestione === g);
  const list = UI.docTipo === "tutti" ? inG : inG.filter((l) => l.tipo === UI.docTipo);
  return `<section><h1>Documenti</h1><p class="muted">Le lettere dell'amministratore con i loro allegati, divise per anno di gestione.</p></section>
  <section><div class="filters" role="group" aria-label="Anno di gestione">${gs.map((x) => `<button data-act="dgest" data-v="${esc(x)}" class="${x === g ? "on" : ""}">Gestione ${esc(x)}</button>`).join("")}</div>
  <div class="filters" role="group" aria-label="Tipo">${["tutti", ...Object.keys(TIPI)].map((t) => { const n = t === "tutti" ? inG.length : inG.filter((l) => l.tipo === t).length; return n || t === "tutti" ? `<button data-act="dtipo" data-v="${t}" class="${t === UI.docTipo ? "on" : ""}">${t === "tutti" ? "Tutti" : TIPI[t]} (${n})</button>` : ""; }).join("")}</div>
  ${list.length ? `<div class="list">${list.map(docItem).join("")}</div>` : `<div class="empty">Nessun documento di questo tipo nella gestione ${esc(g)}.</div>`}</section>
  ${isGestore() ? formLettera() : ""}`;
}
function formLettera() {
  if (!UI.nuovaLettera) return `<section><div class="row-btns"><button class="btn" data-act="nuova-lettera">Aggiungi una lettera a mano</button><span class="small muted">Se una lettera non è arrivata per email.</span></div></section>`;
  const tipo = val("nl-tipo") || "altro";
  const conv = tipo === "convocazione";
  return `<section class="panel"><h2>Aggiungi una lettera a mano</h2><div class="form">
    <div class="grid2"><label>Data della lettera<input type="date" id="nl-data" value="${oggi()}"></label>
    <label>Tipo<select id="nl-tipo" data-change="render">${Object.entries(TIPI).map(([k, v]) => `<option value="${k}" ${k === tipo ? "selected" : ""}>${v}</option>`).join("")}</select></label></div>
    <label>Oggetto<input type="text" id="nl-ogg" placeholder="Es. Convocazione assemblea ordinaria"></label>
    <label>Testo (facoltativo)<textarea id="nl-testo"></textarea></label>
    <label>PDF della lettera e allegati<input type="file" id="nl-file" data-file="nl" accept="application/pdf,image/jpeg,image/png,image/webp" multiple></label>${scelti("nl")}
    ${conv ? `<div class="grid2"><label>Assemblea<select id="nl-atipo"><option value="ordinaria">Ordinaria</option><option value="straordinaria">Straordinaria</option></select></label></div>
    <div class="grid2"><label>1ª convocazione: data<input type="date" id="nl-pd"></label><label>Ora<input type="time" id="nl-po"></label></div>
    <label>1ª convocazione: luogo<input type="text" id="nl-pl"></label>
    <div class="grid2"><label>2ª convocazione: data<input type="date" id="nl-sd"></label><label>Ora<input type="time" id="nl-so"></label></div>
    <label>2ª convocazione: luogo<input type="text" id="nl-sl"></label>
    <label>Punti dell'ordine del giorno, uno per riga<textarea id="nl-punti" placeholder="Approvazione del rendiconto…&#10;Preventivo dei lavori…"></textarea></label>` : ""}
    <div class="row-btns"><button class="btn primary" data-act="salva-lettera" ${UI.busy ? "disabled" : ""}>Pubblica la lettera</button><button class="btn quiet" data-act="nuova-lettera">Annulla</button></div></div></section>`;
}
function viewDoc(id) {
  const l = letteraById(id);
  if (!l) return `<div class="empty">Documento non trovato. <a href="#documenti">Torna ai documenti</a></div>`;
  const a = S.assemblee.find((x) => x.lettera_id === id) || S.assemblee.find((x) => x.verbale_id === id);
  const sintesi = l.tipo === "convocazione" && a ? `<div class="summary"><span class="label">In sintesi (ricavato in automatico dalla lettera)</span>${convRows(a)}<ol>${puntiDi(a.id).map((p) => `<li>${esc(p.titolo)}</li>`).join("")}</ol></div>` : "";
  const ed = UI.editing === "doc-" + id;
  return `<div class="crumbs"><a href="#documenti">Documenti</a><span>›</span><span>Gestione ${esc(l.gestione)}</span></div>
  <section><div class="row-btns">${docChip(l)}</div><h1>${esc(l.oggetto || TIPI[l.tipo])}</h1></section>
  ${a ? `<div class="note">${l.tipo === "verbale" ? "Verbale" : "Convocazione"} dell'assemblea del ${esc(fmtD(a.data_riferimento))}. <a href="#ass-${a.id}">Vai all'assemblea</a></div>` : ""}
  <article class="letter"><dl class="letter-head"><dt>Data</dt><dd>${esc(fmtD(l.data_lettera || l.arrivata))}</dd><dt>Arrivo</dt><dd>${esc(fmtD(l.arrivata))}</dd></dl>
    ${l.testo_email ? `<div class="letter-body">${esc(l.testo_email)}</div>` : ""}
    ${l.allegati.length ? `<div class="files"><span class="label">Allegati</span>${l.allegati.map((f) => fileBtn(f)).join("")}</div>` : ""}
    ${sintesi}</article>
  ${isGestore() ? `<section class="panel"><h3>Correzioni (gestore)</h3>${ed ? `<div class="form">
      <label>Oggetto<input type="text" id="ed-ogg" value="${esc(l.oggetto)}"></label>
      <div class="grid2"><label>Tipo<select id="ed-tipo">${Object.entries(TIPI).map(([k, v]) => `<option value="${k}" ${k === l.tipo ? "selected" : ""}>${v}</option>`).join("")}</select></label>
      <label>Anno di gestione<input type="text" id="ed-gest" value="${esc(l.gestione)}"></label></div>
      <div class="row-btns"><button class="btn primary" data-act="salva-doc" data-id="${id}">Salva</button><button class="btn quiet" data-act="modifica" data-v="">Annulla</button></div></div>`
    : `<div class="row-btns"><button class="btn" data-act="modifica" data-v="doc-${id}">Correggi oggetto, tipo o anno</button>${conferma("elimina-doc", id, "Elimina la lettera")}</div>`}</section>` : ""}`;
}
function viewAssemblee() {
  const list = [...S.assemblee].sort((x, y) => (x.data_riferimento < y.data_riferimento ? 1 : -1));
  if (!list.length) return `<section><h1>Assemblee</h1><div class="empty">Ancora nessuna assemblea. Ogni convocazione dell'amministratore ne crea una, con i suoi punti.</div></section>`;
  const gs = [...new Set(list.map((a) => a.gestione))];
  return `<section><h1>Assemblee</h1><p class="muted">Per ogni anno di gestione, le riunioni con la data e i punti. Per quelle passate trovi l'esito e il verbale.</p></section>` +
    gs.map((g) => `<section><h2>Gestione ${esc(g)}</h2><div class="list">${list.filter((a) => a.gestione === g).map((a) => {
      const fut = a.data_riferimento >= oggi();
      return `<a class="item" href="#ass-${a.id}"><span class="item-title">Assemblea ${esc(a.tipo)} del ${esc(fmtD(a.data_riferimento))}</span><span class="item-side">${fut ? `tra ${giorni(a.data_riferimento)} giorni` : ""}</span>
        <span class="item-meta"><span>${puntiDi(a.id).length} punti</span>${fut ? `<span class="chip c-new">Prossima</span>` : a.verbale_id ? `<span class="chip t-verbale">Verbale disponibile</span>` : ""}</span></a>`;
    }).join("")}</div></section>`).join("");
}
function viewAss(id) {
  const a = assById(id);
  if (!a) return `<div class="empty">Assemblea non trovata. <a href="#assemblee">Torna alle assemblee</a></div>`;
  const docs = documentiDi(a);
  const ed = UI.editing === "ass-" + id;
  const c = (k) => a[k] || {};
  return `<div class="crumbs"><a href="#assemblee">Assemblee</a><span>›</span><span>Gestione ${esc(a.gestione)}</span></div>
  <section><h1>Assemblea ${esc(a.tipo)} del ${esc(fmtD(a.data_riferimento))}</h1>${convRows(a)}
  <div class="row-btns">${a.lettera_id ? `<a class="btn" href="#doc-${a.lettera_id}">Lettera di convocazione</a>` : ""}${a.verbale_id ? `<a class="btn" href="#doc-${a.verbale_id}">Verbale</a>` : ""}</div></section>
  <section><h2>Ordine del giorno</h2>${odgList(a)}</section>
  ${docs.length ? `<section><h2>Documenti per questa assemblea</h2><div class="files">${docs.map((d) => fileBtn(d.file, "lettera del " + fmtS(d.lettera.data_lettera || d.lettera.arrivata))).join("")}</div></section>` : ""}
  ${isGestore() ? `<section class="panel"><h3>Correzioni (gestore)</h3>${ed ? `<div class="form">
    <div class="grid2"><label>Tipo<select id="ea-tipo"><option value="ordinaria">Ordinaria</option><option value="straordinaria" ${a.tipo === "straordinaria" ? "selected" : ""}>Straordinaria</option></select></label><label>Anno di gestione<input type="text" id="ea-gest" value="${esc(a.gestione)}"></label></div>
    <div class="grid2"><label>1ª conv. data<input type="date" id="ea-pd" value="${esc(c("prima").data || "")}"></label><label>Ora<input type="time" id="ea-po" value="${esc(c("prima").ora || "")}"></label></div>
    <label>1ª conv. luogo<input type="text" id="ea-pl" value="${esc(c("prima").luogo || "")}"></label>
    <div class="grid2"><label>2ª conv. data<input type="date" id="ea-sd" value="${esc(c("seconda").data || "")}"></label><label>Ora<input type="time" id="ea-so" value="${esc(c("seconda").ora || "")}"></label></div>
    <label>2ª conv. luogo<input type="text" id="ea-sl" value="${esc(c("seconda").luogo || "")}"></label>
    <div class="row-btns"><button class="btn primary" data-act="salva-ass" data-id="${id}">Salva</button><button class="btn quiet" data-act="modifica" data-v="">Annulla</button></div></div>`
    : `<div class="row-btns"><button class="btn" data-act="modifica" data-v="ass-${id}">Correggi date e luogo</button>${conferma("elimina-ass", id, "Elimina l'assemblea")}</div>
    <div class="form"><label>Aggiungi un punto<input type="text" id="np-${id}" placeholder="Titolo del punto"></label><div class="row-btns"><button class="btn" data-act="aggiungi-punto" data-id="${id}">Aggiungi</button></div></div>`}</section>` : ""}`;
}
function viewPunto(id) {
  const p = puntoById(id);
  if (!p) return `<div class="empty">Punto non trovato. <a href="#home">Torna alla prossima assemblea</a></div>`;
  const a = assById(p.assemblea_id), fut = a.data_riferimento >= oggi();
  const docs = documentiDi(a), cs = condDi(id), bb = bachecaDi(id);
  const auto = modo(S.io.scala) === "automatica";
  const ed = UI.editing === "punto-" + id;
  return `<div class="crumbs"><a href="#ass-${a.id}">Assemblea del ${esc(fmtD(a.data_riferimento))}</a><span>›</span><span>Punto ${p.numero}</span></div>
  <section><div class="row-btns"><span class="odg-n">Punto ${p.numero}</span>${p.esito ? `<span class="chip ${p.esito === "approvato" ? "c-ok" : p.esito === "respinto" ? "c-no" : "c-wait"}">${ESITI[p.esito]}</span>` : ""}</div><h1>${esc(p.titolo)}</h1></section>
  ${docs.length ? `<section><h2>Documenti e preventivi</h2><div class="files">${docs.map((d) => fileBtn(d.file, "lettera del " + fmtS(d.lettera.data_lettera || d.lettera.arrivata))).join("")}</div></section>` : ""}
  ${cs.length || !auto ? `<section><h2>Osservazioni condivise</h2>${cs.length ? cs.map((c) => condCard(c, false)).join("") : `<div class="empty">Ancora nessuna osservazione condivisa su questo punto.</div>`}</section>` : ""}
  ${bb.length || auto ? `<section><h2>Bacheca</h2>${bb.length ? bb.map((o) => bachecaCard(o, false)).join("") : `<div class="empty">Ancora nessun messaggio su questo punto.</div>`}</section>` : ""}
  ${fut && !(isRapp() && !auto) ? ossForm(id) : ""}
  ${fut && isRapp() && !auto ? `<div class="note">Le osservazioni della Scala ${S.io.scala} su questo punto le trovi in <a href="#osservazioni">Osservazioni ricevute</a>.</div>` : ""}
  ${isGestore() ? `<section class="panel"><h3>Correzioni (gestore)</h3>${ed ? `<div class="form">
    <div class="grid2"><label>Numero<input type="number" min="1" id="ep-num" value="${p.numero}"></label><label>Esito<select id="ep-esito">${Object.entries(ESITI).map(([k, v]) => `<option value="${k}" ${k === p.esito ? "selected" : ""}>${v}</option>`).join("")}</select></label></div>
    <label>Titolo<textarea id="ep-tit">${esc(p.titolo)}</textarea></label>
    <div class="row-btns"><button class="btn primary" data-act="salva-punto" data-id="${id}">Salva</button><button class="btn quiet" data-act="modifica" data-v="">Annulla</button></div></div>`
    : `<div class="row-btns"><button class="btn" data-act="modifica" data-v="punto-${id}">Correggi il punto o segna l'esito</button>${conferma("elimina-punto", id, "Elimina il punto")}</div>`}</section>` : ""}`;
}
function statoMio(o) {
  if (o.stato === "nuova") return `<span class="chip c-wait">Inviata a ${esc(nomeRapp(scalaDi(o.alloggio_id)))}</span>${conferma("cancella-oss", o.id, "Ritira")}`;
  if (o.stato === "archiviata") return `<span class="chip">Letta, non condivisa</span>`;
  const c = S.cond.find((x) => x.osservazione_id === o.id);
  return `<span class="chip c-ok">Condivisa con tutti</span>${c?.inoltrata ? `<span class="chip c-ok">Inoltrata all'amministratore</span>` : ""}<a href="#punto-${o.punto_id}">Vedi</a>`;
}
function viewMie() {
  const mie = S.oss.filter((o) => o.alloggio_id === S.io.id).reverse();
  return `<section><h1>Le mie osservazioni</h1><p class="muted">Quello che hai scritto a ${esc(nomeRapp(S.io.scala))}, rappresentante della Scala ${S.io.scala}, e cosa ne ha fatto.</p></section>
  <section>${mie.length ? `<div class="list">${mie.map((o) => { const p = puntoById(o.punto_id); return `<div class="obs"><div class="obs-head"><b>Punto ${p?.numero ?? ""}</b><span>${esc(short(p?.titolo || "", 70))}</span><span>${esc(fmtS(o.creata_il))}</span></div><p class="obs-text">${esc(o.testo)}</p>${o.allegati.length ? `<div class="files">${o.allegati.map((f) => fileBtn(f)).join("")}</div>` : ""}<div class="status">${statoMio(o)}</div></div>`; }).join("")}</div>` : `<div class="empty">Non hai ancora scritto osservazioni.</div>`}</section>
  ${ossForm(null)}`;
}
function viewRicevute() {
  const mie = S.oss.filter((o) => scalaDi(o.alloggio_id) === S.io.scala).reverse();
  const gruppi = { nuove: mie.filter((o) => o.stato === "nuova"), condivise: mie.filter((o) => o.stato === "condivisa"), archiviate: mie.filter((o) => o.stato === "archiviata") };
  const nomi = { nuove: "Nuove", condivise: "Condivise", archiviate: "Non condivise" };
  const a = prossima(), pids = new Set(a ? puntiDi(a.id).map((p) => p.id) : []);
  const miei = S.cond.filter((c) => c.scala === S.io.scala && pids.has(c.punto_id));
  return `<section><h1>Osservazioni ricevute</h1><p class="muted">Le osservazioni dei proprietari della Scala ${S.io.scala}. Le vedi solo tu. Per ognuna scegli se condividerla con tutti (senza nome e interno) o lasciarla dov'è.</p></section>
  <section><div class="filters" role="group" aria-label="Stato">${Object.keys(gruppi).map((k) => `<button data-act="tab" data-v="${k}" class="${UI.tab === k ? "on" : ""}">${nomi[k]} (${gruppi[k].length})</button>`).join("")}</div>
  ${gruppi[UI.tab].length ? `<div class="list">${gruppi[UI.tab].map(ossCard).join("")}</div>` : `<div class="empty">${UI.tab === "nuove" ? "Nessuna osservazione nuova. Non devi fare niente." : "Nessuna."}</div>`}</section>
  ${miei.length ? `<section><h2>Le tue condivisioni per la prossima assemblea</h2><p class="small muted">Da qui prepari l'email per l'amministratore: il testo è già scritto.</p>${miei.map((c) => condCard(c, true)).join("")}</section>` : ""}
  ${ossForm(null)}`;
}
function ossCard(o) {
  const p = puntoById(o.punto_id);
  let html = `<div class="obs"><div class="obs-head"><b>${esc(etichettaAlloggio(o.alloggio_id))}</b><span>${esc(fmtS(o.creata_il))}</span>${p ? `<a href="#punto-${p.id}">Punto ${p.numero}: ${esc(short(p.titolo, 55))}</a>` : ""}</div>
    <p class="obs-text">${esc(o.testo)}</p>${o.allegati.length ? `<div class="files">${o.allegati.map((f) => fileBtn(f)).join("")}</div>` : ""}`;
  if (o.stato === "nuova") {
    html += UI.sharing === o.id ? `<div class="prep"><b>Condividi con tutti i proprietari</b>
        <label>Testo che vedranno (senza nome e interno; puoi correggerlo)<textarea id="sh-t-${o.id}">${esc(o.testo)}</textarea></label>
        <label class="check"><input type="checkbox" id="sh-p-${o.id}" checked> Apri un sondaggio (Favorevole / Contrario / Non so)</label>
        <label>Domanda del sondaggio<input type="text" id="sh-q-${o.id}" value="Siete d'accordo con questa proposta?"></label>
        <div class="row-btns"><button class="btn primary" data-act="condividi" data-id="${o.id}" ${UI.busy ? "disabled" : ""}>Condividi</button><button class="btn quiet" data-act="share" data-id="">Annulla</button></div></div>`
      : `<div class="row-btns"><button class="btn primary" data-act="share" data-id="${o.id}">Condividi con tutti</button><button class="btn" data-act="archivia" data-id="${o.id}">Non condividere</button></div>`;
  } else html += `<div class="status">${o.stato === "condivisa" ? `<span class="chip c-ok">Condivisa</span><a href="#punto-${o.punto_id}">Vedi</a>` : `<span class="chip">Non condivisa</span><button class="btn quiet" data-act="ripristina" data-id="${o.id}">Rimetti tra le nuove</button>`}</div>`;
  return html + `</div>`;
}
function viewBacheca() {
  const a = prossima();
  const pids = new Set(a ? puntiDi(a.id).map((p) => p.id) : []);
  const ms = S.oss.filter((o) => pids.has(o.punto_id) && modo(scalaDi(o.alloggio_id)) === "automatica").reverse();
  return `<section><h1>Bacheca</h1><p class="muted">I messaggi dei proprietari sui punti della prossima assemblea, visibili a tutti. Su ognuno puoi dire se sei favorevole.</p></section>
  <section>${ms.length ? ms.map((o) => bachecaCard(o, true)).join("") : `<div class="empty">${a ? "Ancora nessun messaggio." : "Nessuna assemblea in programma."}</div>`}</section>${ossForm(null)}`;
}
function viewImpostazioni() {
  const imp = S.imp || {};
  const scale = [...new Set(S.alloggi.map((a) => a.scala))].sort();
  return `<section><h1>Impostazioni</h1><p class="muted">Visibili solo al gestore del sito.</p></section>
  <section class="panel"><h2>Condominio</h2><div class="form">
    <label>Nome<input type="text" id="im-nome" value="${esc(imp.nome || "")}"></label>
    <label>Email dell'amministratore<input type="email" id="im-mail" value="${esc(imp.email_amministratore || "")}"></label>
    <p class="small muted">Il sito pubblica solo le email che arrivano da questo indirizzo. Serve anche per inoltrare le osservazioni.</p>
    <label>L'anno di gestione inizia il 1°<select id="im-mese">${MESI.map((m, i) => `<option value="${i + 1}" ${imp.mese_inizio === i + 1 ? "selected" : ""}>${m}</option>`).join("")}</select></label>
  </div></section>
  ${scale.map((s) => { const r = rappDi(s); return `<section class="panel"><h2>Scala ${s}</h2><div class="form">
    <label>Come funzionano le osservazioni<select id="im-modo-${s}"><option value="rappresentante">Con il rappresentante di scala</option><option value="automatica" ${modo(s) === "automatica" ? "selected" : ""}>Bacheca automatica, senza rappresentante</option></select></label>
    <div class="grid2"><label>Rappresentante<select id="im-rapp-${s}"><option value="">Nessuno</option>${S.alloggi.filter((a) => a.scala === s).sort((x, y) => x.interno.localeCompare(y.interno, "it", { numeric: true })).map((a) => `<option value="${a.id}" ${r?.id === a.id ? "selected" : ""}>Interno ${esc(a.interno)}</option>`).join("")}</select></label>
    <label>Nome da mostrare<input type="text" id="im-nome-${s}" value="${esc(r?.nome_rappresentante || "")}" placeholder="Es. Renzo"></label></div>
  </div></section>`; }).join("")}
  <div class="row-btns"><button class="btn primary" data-act="salva-imp" ${UI.busy ? "disabled" : ""}>Salva le impostazioni</button></div>
  <p class="small muted">Password nuove per un alloggio e creazione degli alloggi si fanno con lo strumento <code>prepara.py</code> (vedi LEGGIMI).</p>`;
}

/* ---------- azioni ---------- */
async function carica_file(chiave, prefisso) {
  const out = [];
  for (const f of UI.files[chiave] || []) {
    if (f.size > 20 * 1024 * 1024) throw new Error(`"${f.name}" supera 20 MB`);
    const percorso = `${prefisso}/${crypto.randomUUID().slice(0, 8)}-${sicuro(f.name)}`;
    await q(sb.storage.from("documenti").upload(percorso, f, { contentType: f.type || "application/pdf" }));
    out.push({ nome: f.name.slice(0, 120), percorso });
  }
  return out;
}
const ACT = {
  esci: async () => { await esci(); location.hash = ""; render(); },
  dgest: (d) => { UI.docGest = d.v; UI.docTipo = "tutti"; render(); },
  dtipo: (d) => { UI.docTipo = d.v; render(); },
  tab: (d) => { UI.tab = d.v; render(); },
  modifica: (d) => { UI.editing = d.v || null; render(); },
  share: (d) => { UI.sharing = d.id || null; render(); },
  prep: (d) => { UI.prep = d.id; render(); },
  "prep-chiudi": () => { UI.prep = null; render(); },
  "nuova-lettera": () => { UI.nuovaLettera = !UI.nuovaLettera; UI.files.nl = []; render(); },
  "file-via": (d) => { UI.files[d.id].splice(+d.v, 1); render(); },
  apri: async (d) => {
    const w = window.open("", "_blank");
    try {
      const { signedUrl } = await q(sb.storage.from("documenti").createSignedUrl(d.v, 600));
      if (w) w.location.href = signedUrl; else location.href = signedUrl;
    } catch (e) { w?.close(); toast("Il documento non si apre: " + errore(e), true); }
  },
  copia: async (d) => {
    const el = document.getElementById("prep-" + d.id);
    try { await navigator.clipboard.writeText(el.value); toast("Testo copiato: incollalo nella tua email."); }
    catch { el.select(); toast("Testo selezionato: copialo con Ctrl+C o tenendo premuto."); }
  },
  vota: (d) => azione(() => q(sb.rpc("vota", { oggetto: d.id, scelta_voto: S.miei[d.id] === d.v ? null : d.v }))),
  chiudi: (d) => azione(() => q(sb.rpc("aggiorna_condivisione", { cond: d.id, chiudi: true, segna_inoltrata: false })), "Sondaggio chiuso: i risultati restano visibili."),
  inoltrata: (d) => azione(async () => { await q(sb.rpc("aggiorna_condivisione", { cond: d.id, chiudi: false, segna_inoltrata: true })); UI.prep = null; }, "Segnata come inoltrata all'amministratore."),
  archivia: (d) => azione(() => q(sb.rpc("cambia_stato_osservazione", { oss: d.id, nuovo_stato: "archiviata" })), "Lasciata da parte. Chi l'ha scritta vede che l'hai letta."),
  ripristina: (d) => azione(async () => { await q(sb.rpc("cambia_stato_osservazione", { oss: d.id, nuovo_stato: "nuova" })); UI.tab = "nuove"; }),
  condividi: (d) => azione(async () => {
    const conPoll = document.getElementById("sh-p-" + d.id)?.checked;
    await q(sb.rpc("condividi", { oss: d.id, testo_condiviso: val("sh-t-" + d.id), domanda_sondaggio: conPoll ? val("sh-q-" + d.id) || "Siete d'accordo con questa proposta?" : null }));
    UI.sharing = null;
  }, "Condivisa con tutti i proprietari."),
  "invia-oss": (d) => {
    const k = d.id, testo = val("os-t-" + k).trim();
    const punto = k === "x" ? val("os-pt") : k;
    if (!testo) return toast("Scrivi il testo prima di inviarlo.", true);
    const auto = modo(S.io.scala) === "automatica";
    azione(async () => {
      const allegati = await carica_file(k, `osservazioni/${S.io.id}`);
      await q(sb.from("osservazioni").insert({ alloggio_id: S.io.id, punto_id: punto, testo, allegati }));
      const el = document.getElementById("os-t-" + k); if (el) el.value = "";
      UI.files[k] = [];
    }, auto ? "Pubblicato in bacheca." : `Inviata a ${nomeRapp(S.io.scala)}.`);
  },
  "cancella-oss": (d) => azione(() => q(sb.from("osservazioni").delete().eq("id", d.id)), "Cancellato."),
  "salva-imp": () => azione(async () => {
    const modi = {};
    const scale = [...new Set(S.alloggi.map((a) => a.scala))];
    scale.forEach((s) => { modi[s] = val("im-modo-" + s); });
    await q(sb.from("impostazioni").update({ nome: val("im-nome").trim() || "Condominio", email_amministratore: val("im-mail").trim().toLowerCase(), mese_inizio: +val("im-mese"), modo_scala: modi }).eq("id", 1));
    for (const s of scale) await q(sb.rpc("imposta_rappresentante", { s, alloggio: val("im-rapp-" + s) || null, nome: val("im-nome-" + s) }));
  }, "Impostazioni salvate."),
  "salva-doc": (d) => {
    const gestione = val("ed-gest").trim();
    if (!/^\d{4}(\/\d{4})?$/.test(gestione)) return toast("Scrivi l'anno di gestione come 2025/2026 oppure 2026.", true);
    azione(async () => { await q(sb.from("lettere").update({ oggetto: val("ed-ogg").trim(), tipo: val("ed-tipo"), gestione }).eq("id", d.id)); UI.editing = null; }, "Lettera corretta.");
  },
  "elimina-doc": (d) => azione(async () => { await q(sb.from("lettere").delete().eq("id", d.id)); location.hash = "documenti"; }, "Lettera eliminata."),
  "salva-ass": (d) => {
    const conv = (p) => { const data = val(`ea-${p}d`); return isDate(data) ? { data, ora: val(`ea-${p}o`), luogo: val(`ea-${p}l`).trim() } : null; };
    const prima = conv("p"), seconda = conv("s");
    if (!prima && !seconda) return toast("Serve almeno una data di convocazione.", true);
    azione(async () => { await q(sb.from("assemblee").update({ tipo: val("ea-tipo"), gestione: val("ea-gest").trim(), prima, seconda, data_riferimento: (seconda || prima).data }).eq("id", d.id)); UI.editing = null; }, "Assemblea corretta.");
  },
  "elimina-ass": (d) => azione(async () => { await q(sb.from("assemblee").delete().eq("id", d.id)); location.hash = "assemblee"; }, "Assemblea eliminata."),
  "aggiungi-punto": (d) => {
    const titolo = val("np-" + d.id).trim();
    if (!titolo) return toast("Scrivi il titolo del punto.", true);
    const numero = Math.max(0, ...puntiDi(d.id).map((p) => p.numero)) + 1;
    azione(async () => { await q(sb.from("punti").insert({ assemblea_id: d.id, numero, titolo })); document.getElementById("np-" + d.id).value = ""; }, "Punto aggiunto.");
  },
  "salva-punto": (d) => {
    const titolo = val("ep-tit").trim();
    if (!titolo) return toast("Il punto deve avere un titolo.", true);
    azione(async () => { await q(sb.from("punti").update({ titolo, numero: Math.max(1, +val("ep-num") || 1), esito: val("ep-esito") }).eq("id", d.id)); UI.editing = null; }, "Punto corretto.");
  },
  "elimina-punto": (d) => { const a = puntoById(d.id)?.assemblea_id; azione(async () => { await q(sb.from("punti").delete().eq("id", d.id)); location.hash = "ass-" + a; }, "Punto eliminato."); },
  "salva-lettera": () => {
    const data = val("nl-data"), tipo = val("nl-tipo"), oggetto = val("nl-ogg").trim();
    if (!isDate(data) || !oggetto) return toast("Servono la data e l'oggetto della lettera.", true);
    let assemblea = null;
    if (tipo === "convocazione") {
      const conv = (p) => { const d = val(`nl-${p}d`); return isDate(d) ? { data: d, ora: val(`nl-${p}o`), luogo: val(`nl-${p}l`).trim() } : null; };
      const prima = conv("p"), seconda = conv("s");
      const punti = val("nl-punti").split("\n").map((s) => s.replace(/^\s*\d+\s*[.)\-–]\s*/, "").trim()).filter(Boolean);
      if (!prima && !seconda) return toast("Per una convocazione serve almeno la data di una convocazione.", true);
      assemblea = { tipo: val("nl-atipo"), prima, seconda, punti };
    }
    azione(async () => {
      const slug = oggetto.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 40) || "lettera";
      const allegati = await carica_file("nl", `lettere/${data}_${slug}-${crypto.randomUUID().slice(0, 6)}`);
      const mese = S.imp?.mese_inizio || 10;
      const rif = assemblea ? (assemblea.seconda || assemblea.prima).data : data;
      const [lettera] = await q(sb.from("lettere").insert({ arrivata: oggi(), data_lettera: data, oggetto, testo_email: val("nl-testo").trim(), tipo, gestione: gestioneDa(rif, mese), allegati }).select());
      if (assemblea) {
        const [ass] = await q(sb.from("assemblee").insert({ tipo: assemblea.tipo, gestione: gestioneDa(rif, mese), prima: assemblea.prima, seconda: assemblea.seconda, data_riferimento: rif, lettera_id: lettera.id }).select());
        if (assemblea.punti.length) await q(sb.from("punti").insert(assemblea.punti.map((titolo, i) => ({ assemblea_id: ass.id, numero: i + 1, titolo }))));
      }
      UI.nuovaLettera = false; UI.files.nl = [];
    }, "Lettera pubblicata.");
  },
};
const CONFERME = new Set(["elimina-doc", "elimina-ass", "elimina-punto", "cancella-oss"]);
document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-act]");
  if (!b) return;
  e.preventDefault();
  const a = b.dataset.act;
  if (CONFERME.has(a) && UI.confirm !== a + b.dataset.id) { UI.confirm = a + b.dataset.id; render(); return; }
  UI.confirm = null;
  ACT[a]?.(b.dataset, b);
});
document.addEventListener("change", (e) => {
  const t = e.target;
  if (t.dataset.file) { UI.files[t.dataset.file] = [...(UI.files[t.dataset.file] || []), ...t.files].slice(0, 8); t.value = ""; render(); }
  else if (t.dataset.change === "mostra-pw") document.getElementById("acc-pw").type = t.checked ? "text" : "password";
  else if (t.dataset.change === "render") render();
});
document.addEventListener("submit", async (e) => {
  if (e.target.dataset.form !== "accedi") return;
  e.preventDefault();
  const scala = Number(val("acc-scala")), interno = val("acc-int"), pw = val("acc-pw").trim().toLowerCase();
  const a = (S.accesso?.alloggi || []).find((x) => x.scala === scala && x.interno === interno);
  if (!a || !pw) { UI.erroreAccesso = "Scegli scala e interno e scrivi la password."; render(); return; }
  UI.busy = true; UI.erroreAccesso = ""; render();
  const { data, error } = await sb.auth.signInWithPassword({ email: `${a.id.toLowerCase()}@${DOMINIO_EMAIL}`, password: pw });
  if (error) {
    UI.busy = false;
    UI.erroreAccesso = /invalid/i.test(error.message) ? "Password non corretta. Controlla il bigliettino, trattini compresi." : errore(error);
    render(); return;
  }
  S.utente = data.user;
  try { await carica(); } catch (err) { toast(errore(err), true); }
  UI.busy = false; location.hash = "home"; render();
});
window.addEventListener("hashchange", () => { UI.editing = null; UI.prep = null; UI.sharing = null; UI.confirm = null; render(); window.scrollTo(0, 0); });
avvio();
