/* IL TASTO «LOOK» E LE CENTO PALETTE, chiesti da Manlio il 2026-09-22 a partire
   dal libretto Figma delle 100 combinazioni di colori.

   La prova che conta è la PRIMA: i colori della pagina non sono decorazione.
   Se un look rende il prezzo poco staccato dallo sfondo, quel look non è un
   gusto diverso, è una pagina che non si legge — e questa pagina si legge in
   negozio, con la luce che c'è. Quindi ogni look viene misurato qui dentro con
   la regola del contrasto, uno per uno, come già fa look.py quando li
   costruisce: due controlli invece di uno, perché i colori li ha scelti un
   programma e nessuno li guarda tutti e cento a occhio.

   Poi: il tasto c'è, la finestra si apre, scegliere cambia davvero, si torna
   all'originale, la scelta resta, e la pagina NON parte con un look addosso
   (quella sarebbe la modalità scura automatica, vietata da anni qui dentro). */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const file = process.argv[2] || 'out/sito.html';
const male = [];
const errori = [];
const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
  runScripts: 'dangerously', pretendToBeVisual: true,
  url: 'https://manliograndi-del.github.io/spesa/',
  virtualConsole: new VirtualConsole().on('jsdomError',
    e => errori.push(String(e.detail || e.message).split('\n')[0])),
});

/* La regola del contrasto, scritta qui e non presa da nessuna parte: se un
   giorno look.py cambia i conti, questa prova non cambia con lui. */
const canale = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
function luce(h) {
  const n = parseInt(h.replace('#', ''), 16);
  return 0.2126 * canale((n >> 16) & 255) + 0.7152 * canale((n >> 8) & 255) + 0.0722 * canale(n & 255);
}
function contrasto(a, b) {
  const x = luce(a), y = luce(b);
  return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
}
const MISURE = [
  ['testo/sfondo', 'inchiostro', 'carta', 7],
  ['testo tenue/sfondo', 'tenue', 'carta', 4.5],
  ['accento/sfondo', 'rosso', 'carta', 4.5],
  ['scritta dentro il bottone acceso', 'su-rosso', 'rosso', 4.5],
  ['verde del «meno caro»', 'verde', 'carta', 4.5],
  ['ambra degli avvisi', 'ambra', 'carta', 4.5],
  ['testo/pannello', 'inchiostro', 'pannello', 6],
];

setTimeout(() => {
  const w = dom.window, d = w.document;
  if (errori.length) male.push('errori nella pagina: ' + errori.join(' / '));

  const look = w.eval('DATI.look');
  if (!look || look.length < 90) {
    console.error('MANCANO i look: ne trovo', look ? look.length : 0);
    process.exit(1);
  }

  /* 1. TUTTI I LOOK SI LEGGONO. */
  let peggiore = { c: 99, chi: '' };
  look.forEach(l => {
    MISURE.forEach(([nome, a, b, minimo]) => {
      if (!l.v[a] || !l.v[b]) { male.push(l.nome + ': manca il colore ' + (l.v[a] ? b : a)); return; }
      const c = contrasto(l.v[a], l.v[b]);
      if (c < minimo - 0.01)
        male.push('«' + l.nome + '»: ' + nome + ' è ' + c.toFixed(1) + ':1, ne serve ' + minimo);
      if (c / minimo < peggiore.c) peggiore = { c: c / minimo, chi: l.nome + ' — ' + nome };
    });
    /* Sulle pagine chiare l'accento regge 7:1 come il testo (Manlio,
       2026-09-26: «poco contrasto… un colore più scuro nelle combinazioni
       chiare»). */
    if (!l.notte && contrasto(l.v.rosso, l.v.carta) < 6.99)
      male.push('«' + l.nome + '»: l\'accento su una pagina chiara è sbiadito ('
        + contrasto(l.v.rosso, l.v.carta).toFixed(1) + ':1, ne serve 7)');
    if (!Array.isArray(l.base) || l.base.length < 3)
      male.push('«' + l.nome + '» non ha le sue tinte da mostrare');
  });

  /* 2. La pagina NON parte con un look addosso. */
  if (d.documentElement.style.getPropertyValue('--carta'))
    male.push('la pagina parte già con un look: deve partire com\'è sempre stata');

  /* 3. Il tasto e la finestra. */
  const tasto = d.getElementById('apri-look');
  const buio = d.getElementById('buio-look');
  if (!tasto || !buio) { console.error('MANCA il tasto Look o la sua finestra'); process.exit(1); }
  if (!d.getElementById('buio-config').contains(tasto)) male.push('il tasto dei colori non sta nella configurazione');
  if (d.querySelector('.barra').contains(buio)) male.push('LA FINESTRA STA DENTRO LA BARRA');
  if (!buio.hidden) male.push('la finestra dei look si apre da sola');

  d.getElementById('chiudi-novita').dispatchEvent(new w.Event('click'));
  tasto.dispatchEvent(new w.Event('click'));
  if (buio.hidden) male.push('toccando «Look» non si apre niente');
  const righe = [...d.querySelectorAll('#voci-look .look-riga')];
  if (righe.length !== look.length + 1)
    male.push('le righe sono ' + righe.length + ' invece di ' + (look.length + 1) + ' (i look più l\'originale)');
  if (righe[0].getAttribute('data-look') !== '')
    male.push('la prima riga non è «Originale»: da un look non si tornerebbe indietro');
  righe.forEach(r => {
    if (r.querySelectorAll('.strisce i').length < 3)
      male.push('una riga senza le sue tinte in vista');
  });

  /* 4. Scegliere cambia davvero, e la scelta resta. */
  const prova = look.find(l => !l.notte) || look[0];
  d.querySelector('[data-look="' + prova.id + '"]').dispatchEvent(new w.Event('click'));
  const messo = d.documentElement.style.getPropertyValue('--rosso').trim();
  if (messo.toUpperCase() !== prova.v.rosso.toUpperCase())
    male.push('scegliendo «' + prova.nome + '» il colore non cambia (' + messo + ')');
  let salvato = null;
  try { salvato = w.localStorage.getItem('spesa.look.v1'); } catch (e) {}
  if (salvato !== prova.id) male.push('la scelta non viene ricordata');
  if (d.querySelector('[data-look="' + prova.id + '"]').getAttribute('aria-pressed') !== 'true')
    male.push('il look scelto non è segnato nell\'elenco');

  /* 5. Un look scuro esiste e fa davvero una pagina scura. */
  const notte = look.find(l => l.notte);
  if (!notte) male.push('nessun look scuro: le palette scure sono state sbiancate');
  else if (luce(notte.v.carta) > 0.25) male.push('il look «' + notte.nome + '» è segnato scuro ma ha lo sfondo chiaro');

  /* 6. Si torna all'originale. */
  righe[0].dispatchEvent(new w.Event('click'));
  if (d.documentElement.style.getPropertyValue('--carta'))
    male.push('«Originale» non toglie il look');

  if (male.length) { male.forEach(x => console.error('  ✗ ' + x)); process.exit(1); }
  console.log('  look: ' + look.length + ' (' + look.filter(l => l.notte).length + ' scuri), tutti leggibili');
  console.log('  il più tirato: ' + peggiore.chi + ' (a ' + peggiore.c.toFixed(2) + ' volte il minimo)');
  console.log('  si sceglie, si ricorda, si torna indietro');
  process.exit(0);
}, 1500);
