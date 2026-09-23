/* La sezione «Personale», chiesta da Manlio il 2026-09-23: parole sue fatte
   pillole, sotto il riepilogo delle offerte (all'inizio solo la più
   conveniente per parola, col tasto tutte), e una scelta dei supermercati
   che vale solo lì. Tutto resta sul telefono di chi la usa.
   Qui si controlla quello che, se si rompe, non si vede rileggendo:
   - il quarto tasto c'è, apre la sezione e diventa rosso;
   - una parola aggiunta diventa una pillola e resta anche riaprendo la pagina;
   - sotto c'è UNA offerta per parola, e col tasto ci sono tutte;
   - togliere un supermercato qui lo toglie dal riepilogo, ma NON dalla
     ricerca generale;
   - la × toglie la parola;
   - niente bollino verde nel riepilogo.                                    */
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
    beforeParse(w) {
      Object.entries(storage || {}).forEach(([k, v]) => w.localStorage.setItem(k, v));
      w.HTMLElement.prototype.scrollIntoView = function () {};
      w.scrollTo = () => {};
    },
  });
  return { dom, errori };
}
const negozioDi = r => { const m = r.querySelector('.marchio'); return m ? m.textContent.trim() : ''; };

const { dom, errori } = apri();
setTimeout(() => {
  const w = dom.window, d = w.document;
  const male = [];
  const per = d.getElementById('vai-personale');
  if (!per) { console.error('MANCA il tasto «Personale»'); process.exit(1); }
  const ordine = [...d.querySelectorAll('#riga-cerca button')].map(b => b.textContent);
  if (ordine.join('|') !== 'Prodotti|Cerca|Grandi marche|Personale') male.push('i tasti sono ' + ordine.join(', '));
  per.click();
  const sez = d.getElementById('personale');
  if (sez.hidden) male.push('«Personale» non apre la sezione');
  if (d.getElementById('vai-personale').getAttribute('aria-pressed') !== 'true') male.push('«Personale» non diventa rosso');
  if (d.getElementById('vai-prodotti').getAttribute('aria-pressed') !== 'false') male.push('nel Personale «Prodotti» resta rosso');
  if (!d.querySelector('.barra').hidden) male.push('nel Personale si vedono le categorie');
  if (d.querySelector('.barra').contains(sez)) male.push('la sezione sta dentro la barra');

  const scrivi = parola => {
    d.getElementById('parola-pers').value = parola;
    d.getElementById('form-pers').dispatchEvent(new w.Event('submit', { cancelable: true }));
  };
  scrivi('tonno'); scrivi('mozzarella'); scrivi('Tonno');   // l'ultima è doppia
  const pillole = [...d.querySelectorAll('#pillole-pers .nome-pers')].map(b => b.textContent);
  if (pillole.join('|') !== 'tonno|mozzarella') male.push('pillole: ' + pillole.join(', '));
  const salvate = JSON.parse(w.localStorage.getItem('spesa.personale.v1') || '[]');
  if (salvate.join('|') !== 'tonno|mozzarella') male.push('le parole non restano sul telefono');

  const blocco = p => [...d.querySelectorAll('.blocco-pers')].find(b => b.dataset.parola === p);
  const b1 = blocco('tonno');
  if (!b1) male.push('manca il riepilogo di «tonno»');
  else {
    const righe = b1.querySelectorAll('.prezzo-riga');
    if (righe.length !== 1) male.push('all\'inizio «tonno» ha ' + righe.length + ' offerte invece di una');
    const t = b1.querySelector('button.altre');
    if (!t) male.push('manca il tasto per vedere tutte le offerte');
    else {
      const n = +(t.textContent.match(/\d+/) || [0])[0];
      t.click();
      const tutte = blocco('tonno').querySelectorAll('.prezzo-riga').length;
      if (tutte !== n) male.push('col tasto «tonno» mostra ' + tutte + ' offerte invece di ' + n);
      console.log('  «tonno»: 1 all\'inizio, ' + tutte + ' col tasto');
    }
  }
  if (d.querySelectorAll('#riepilogo-pers .bollo.meno, #riepilogo-pers .prezzo-riga.vince').length)
    male.push('C\'È IL BOLLINO VERDE nel riepilogo');

  // i supermercati di questa sezione
  d.getElementById('apri-negozi-pers').click();
  const bottoni = [...d.querySelectorAll('#negozi-pers button')];
  if (bottoni.length < 2) male.push('l\'elenco dei supermercati ha ' + bottoni.length + ' voci');
  const nei = [...blocco('tonno').querySelectorAll('.prezzo-riga')].map(negozioDi);
  const vittima = nei[0];
  const bv = bottoni.find(b => b.textContent.trim() === vittima);
  if (bv) {
    bv.click();
    const dopo = [...blocco('tonno').querySelectorAll('.prezzo-riga')].map(negozioDi);
    if (dopo.includes(vittima)) male.push('tolto «' + vittima + '», il riepilogo lo mostra ancora');
    if (JSON.parse(w.localStorage.getItem('spesa.negozi.v1') || '[]').includes(vittima))
      male.push('toglierlo qui lo ha tolto anche dalla configurazione generale');
    // la ricerca generale lo trova ancora
    d.getElementById('riga-cerca').querySelector('.trova').click();
    const q = d.getElementById('q'); q.value = 'tonno';
    q.dispatchEvent(new w.Event('input'));
    if (![...d.querySelectorAll('#trovati .prezzo-riga')].some(r => negozioDi(r) === vittima))
      male.push('tolto nel Personale, «' + vittima + '» sparisce anche dalla ricerca generale');
    if (!sez.hidden) male.push('aprendo Cerca la sezione personale resta aperta');
    d.getElementById('vai-personale').click();
    console.log('  tolto «' + vittima + '» solo nel Personale: via dal riepilogo, resta nella ricerca');
  } else male.push('non trovo nell\'elenco il supermercato ' + vittima);

  // la × toglie
  const x = [...d.querySelectorAll('#pillole-pers .pillola-pers')]
    .find(p => p.querySelector('.nome-pers').textContent === 'mozzarella').querySelector('.via-pers');
  x.click();
  if (blocco('mozzarella')) male.push('tolta «mozzarella», il suo riepilogo resta');
  if (errori.length) male.push('errori nella pagina: ' + errori.join(' / '));

  // riaprendo la pagina restano parole e supermercati
  const salvato = {};
  for (let i = 0; i < w.localStorage.length; i++) { const k = w.localStorage.key(i); salvato[k] = w.localStorage.getItem(k); }
  const due = apri(salvato);
  setTimeout(() => {
    const d2 = due.dom.window.document;
    d2.getElementById('vai-personale').click();
    const p2 = [...d2.querySelectorAll('#pillole-pers .nome-pers')].map(b => b.textContent);
    if (p2.join('|') !== 'tonno') male.push('riaprendo la pagina le pillole sono: ' + (p2.join(', ') || 'nessuna'));
    if (vittima && [...d2.querySelectorAll('.blocco-pers .prezzo-riga')].some(r => negozioDi(r) === vittima))
      male.push('riaprendo la pagina il supermercato tolto è tornato');
    if (male.length) { console.error('MALE:\n  ' + male.join('\n  ')); process.exit(1); }
    console.log('  la sezione personale fa quello che deve, e resta sul telefono');
    process.exit(0);
  }, 400);
}, 400);
