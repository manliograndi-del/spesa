/* Le grandi ditte in «Grandi marche», con tutti i loro marchi.

   Manlio, 2026-09-24: «ci sono prodotti come la Coca-Cola e tutti i suoi
   marchi, Sprite eccetera, giganti del pulito come quelli che fanno Dash,
   oppure Nestlé… per ognuna non cercare solo il nome della ditta ma anche i
   marchi che produce».

   Qui si controlla, con offerte finte messe apposta nei dati (le vere
   cambiano ogni settimana):
   - toccando «Coca-Cola» esce anche la Fanta;
   - le capsule «compatibili Nespresso» NON sono Nestlé (ma restano Kimbo);
   - il tonno Moretti NON è Heineken, la birra Moretti sì;
   - «dove» scritto in una nota NON è Dove (Unilever), il bagnoschiuma Dove sì;
   - scrivendo «coca cola» in «Cerca» esce anche la Fanta;
   - ogni ditta ha il suo riquadro col marchio, e nessun marchio sta sotto
     due ditte.                                                              */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const errori = [];
const dom = new JSDOM(fs.readFileSync(process.argv[2], 'utf8'), {
  runScripts: 'dangerously', pretendToBeVisual: true,
  url: 'https://manliograndi-del.github.io/spesa/',
  beforeParse(w) { w.scrollTo = () => {}; },
  virtualConsole: new VirtualConsole()
    .on('jsdomError', e => errori.push(String(e.detail || e.message).split('\n')[0])),
});
setTimeout(() => {
  const w = dom.window, d = w.document;
  const male = [];
  const gruppi = w.eval('Object.keys(DATI.marcheParole).filter(g => g !== "Ferrero")');
  if (gruppi.length < 10) male.push('le grandi ditte sono solo ' + gruppi.length + ', ne servono almeno dieci');

  // offerte finte, copiate da una vera che vale oggi
  w.eval(`(() => {
    const base = DATI.offerte.find(o => !nascosta(o));
    const finta = (pro, cat, note) => Object.assign({}, base, { pro, cat, note: note || '', marca: undefined, nome: undefined, agg: undefined });
    DATI.offerte.push(
      finta('Aranciata – Fanta', 'Bibite'),
      finta('Capsule caffè compatibili Nespresso, 30 capsule – Kimbo', 'Caffè'),
      finta('Trancetti di tonno all\\'olio – Moretti', 'Tonno'),
      finta('Birra Baffo d\\'Oro – Moretti', 'Birra'),
      finta('Bagnoschiuma – Neutro Roberts', 'Bagnoschiuma', 'Vale dove c\\'è il reparto profumeria.'),
      finta('Bagnoschiuma idratante – Dove', 'Bagnoschiuma'));
  })()`);
  const trova = (m, pro) => w.eval('cercaMarca(' + JSON.stringify(m) + ')').some(o => o.pro === pro);
  if (!trova('Coca-Cola', 'Aranciata – Fanta')) male.push('«Coca-Cola» non trova la Fanta');
  if (trova('Nestlé', 'Capsule caffè compatibili Nespresso, 30 capsule – Kimbo')) male.push('le capsule compatibili Nespresso finiscono sotto Nestlé');
  if (!trova('Kimbo', 'Capsule caffè compatibili Nespresso, 30 capsule – Kimbo')) male.push('le capsule Kimbo compatibili Nespresso non sono più Kimbo');
  if (trova('Heineken', 'Trancetti di tonno all\'olio – Moretti')) male.push('il tonno Moretti finisce sotto Heineken');
  if (!trova('Heineken', 'Birra Baffo d\'Oro – Moretti')) male.push('la birra Moretti non è sotto Heineken');
  if (trova('Unilever', 'Bagnoschiuma – Neutro Roberts')) male.push('un «dove» nella nota finisce sotto Unilever (Dove)');
  if (!trova('Unilever', 'Bagnoschiuma idratante – Dove')) male.push('il bagnoschiuma Dove non è sotto Unilever');
  const daCerca = w.eval('cercaOfferte("coca cola")').some(o => o.pro === 'Aranciata – Fanta');
  if (!daCerca) male.push('scrivendo «coca cola» in «Cerca» la Fanta non esce');

  // nessun marchio sotto due ditte
  const visti = {};
  gruppi.forEach(g => w.eval('DATI.marcheParole[' + JSON.stringify(g) + ']').forEach(p => {
    const k = p.replace(/^=/, '').replace(/@.*/, '').toLowerCase();
    if (visti[k] && visti[k] !== g) male.push('«' + k + '» sta sotto ' + visti[k] + ' e sotto ' + g);
    visti[k] = g;
  }));

  // ogni ditta ha il suo riquadro col marchio
  d.getElementById('chiudi-novita').dispatchEvent(new w.Event('click'));
  d.querySelector('#riga-cerca .marchi').click();
  const riquadri = [...d.querySelectorAll('#marche button')];
  gruppi.forEach(g => {
    const b = riquadri.find(x => (x.title || x.textContent).startsWith(g) || x.textContent === g);
    if (!b) male.push('manca il riquadro di ' + g);
    else if (!b.classList.contains('col-logo')) male.push(g + ' non ha il marchio');
  });

  if (errori.length) male.push('errori nella pagina: ' + errori.join(' / '));
  if (male.length) { console.error('MALE:\n  ' + male.join('\n  ')); process.exit(1); }
  console.log('  ' + gruppi.length + ' grandi ditte coi loro marchi; Fanta sotto Coca-Cola, niente capsule compatibili né tonno Moretti né «dove» per sbaglio');
  process.exit(0);
}, 2500);
