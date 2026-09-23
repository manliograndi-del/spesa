/* La scelta dei supermercati, chiesta da Manlio il 2026-09-22 notte: «un tasto
   per scegliere i supermercati: appare l'elenco completo e tu scegli quello
   che vuoi». Sta nella finestra della configurazione (l'ingranaggio in cima).

   Qui si controlla quello che, se si rompe, non si vede rileggendo:
   - l'elenco ha TUTTE le insegne dei volantini, e all'inizio sono tutte tenute;
   - togliendone una, le sue offerte spariscono dai prezzi e dalla ricerca
     (l'elenco dei volantini in fondo non c'è più dal 2026-09-23 sera);
   - la scelta si ricorda (resta sul telefono) e rimettendola torna tutto;
   - non si possono togliere tutte: la pagina resterebbe senza un prezzo.     */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const file = process.argv[2] || 'out/sito.html';
const html = fs.readFileSync(file, 'utf8');

function apri(storage) {
  const errori = [];
  const vc = new VirtualConsole().on('jsdomError',
    e => errori.push(String(e.detail || e.message).split('\n')[0]));
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    url: 'https://manliograndi-del.github.io/spesa/',
    beforeParse(w) { Object.entries(storage || {}).forEach(([k, v]) => w.localStorage.setItem(k, v)); },
  });
  return { dom, errori };
}

const negozioDi = r => {
  const m = r.querySelector('.marchio');
  return m ? m.textContent.trim() : '';
};

const { dom, errori } = apri();
setTimeout(() => {
  const w = dom.window, d = w.document;
  const male = [];
  if (errori.length) male.push('errori nella pagina: ' + errori.join(' / '));

  const ing = d.querySelector('header #apri-config');
  if (!ing) { console.error('MANCA l\'ingranaggio della configurazione'); process.exit(1); }
  const buio = d.getElementById('buio-config');
  if (!buio.hidden) male.push('la configurazione si apre da sola');
  if (d.querySelector('.barra').contains(buio)) male.push('LA FINESTRA STA DENTRO LA BARRA');
  d.getElementById('chiudi-novita').dispatchEvent(new w.Event('click'));
  ing.dispatchEvent(new w.Event('click'));
  if (buio.hidden) male.push('toccando l\'ingranaggio non si apre niente');

  const tasti = () => [...d.querySelectorAll('#negozi button')];
  const insegne = [...new Set(d.defaultView.eval('DATI.volantini.map(v => v.ins)'))];
  if (tasti().length !== insegne.length)
    male.push('i supermercati in elenco sono ' + tasti().length + ' invece di ' + insegne.length);
  if (tasti().some(b => b.getAttribute('aria-pressed') !== 'true'))
    male.push('all\'inizio non sono tutti tenuti');

  const conta = ins => [...d.querySelectorAll('#risultato .prezzo-riga')]
    .filter(r => negozioDi(r) === ins).length;

  // la prima insegna che ha offerte sul prodotto acceso
  const vittima = insegne.find(i => conta(i) > 0);
  if (!vittima) male.push('nessuna insegna ha offerte sul primo prodotto: la prova non prova niente');
  else {
    const prima = conta(vittima);
    tasti().find(b => b.title === vittima).dispatchEvent(new w.Event('click'));
    if (conta(vittima)) male.push('tolto «' + vittima + '», le sue offerte restano nei prezzi');
    const b = tasti().find(x => x.title === vittima);
    if (b.getAttribute('aria-pressed') !== 'false') male.push('il tasto tolto non si vede spento');
    const salvato = w.localStorage.getItem('spesa.negozi.v1') || '';
    if (salvato.indexOf(vittima) < 0) male.push('la scelta non resta sul telefono');

    // dalla ricerca
    d.querySelector('.tasto.trova').dispatchEvent(new w.Event('click'));
    const q = d.getElementById('q');
    q.value = vittima; q.dispatchEvent(new w.Event('input'));
    const trovati = [...d.querySelectorAll('#trovati .prezzo-riga')].filter(r => negozioDi(r) === vittima);
    if (trovati.length) male.push('tolto «' + vittima + '», la ricerca lo trova ancora');

    // riaperta la pagina con la scelta salvata, il negozio resta tolto
    const due = apri({ 'spesa.negozi.v1': salvato });
    setTimeout(() => {
      const d2 = due.dom.window.document;
      const ancora = [...d2.querySelectorAll('#risultato .prezzo-riga')].filter(r => negozioDi(r) === vittima).length;
      if (ancora) male.push('riaprendo la pagina il negozio tolto torna');

      // rimesso, torna tutto
      tasti().find(x => x.title === vittima).dispatchEvent(new w.Event('click'));
      d.getElementById('chiudi-ricerca').dispatchEvent(new w.Event('click'));
      if (conta(vittima) !== prima) male.push('rimesso «' + vittima + '», le offerte non tornano tutte');

      // non si tolgono tutti
      insegne.forEach(i => { const x = tasti().find(t => t.title === i); if (x) x.dispatchEvent(new w.Event('click')); });
      if (!tasti().some(x => x.getAttribute('aria-pressed') === 'true'))
        male.push('si possono togliere TUTTI i supermercati: la pagina resta vuota');
      if (!d.getElementById('avviso-negozi').textContent) male.push('togliendo l\'ultimo non dice niente');

      console.log('  supermercati in elenco: ' + insegne.length + ', provato a togliere: ' + vittima);
      if (male.length) { male.forEach(m => console.log('  ✗ ' + m)); process.exit(1); }
      console.log('  la scelta dei supermercati fa quello che deve');
      process.exit(0);
    }, 1200);
    return;
  }
  male.forEach(m => console.log('  ✗ ' + m)); process.exit(1);
}, 1200);
