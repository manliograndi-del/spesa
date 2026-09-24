/* LA MAPPA DELL'AIUTO ALL'APERTURA (2026-09-24). Manlio, con un
   disegno fatto a mano: «questa immagine di Help ci sia aprendo il sito, e
   basta; che non si arrivi a una pagina con già dei prodotti». Fumetti con
   la freccia verso i due pallini in alto e verso i quattro tasti del menù.

   Qui si controlla quello che, rompendosi, non si vede rileggendo:
   - all'apertura c'è la mappa, con cinque fumetti che dicono qualcosa, e
     niente prodotti né offerte: la griglia è giù e nessun tasto è acceso;
   - ogni fumetto trova il suo tasto, e la sua freccia parte (le misure le dà
     un telefono finto: jsdom non impagina), quella dei pallini verso l'alto;
   - le frecce non si toccano (non rubano il dito ai tasti sotto);
   - «Prodotti» toglie mappa e frecce, fa salire la griglia e si accende;
   - il titolo «Spesa» la riporta; dopo «Cerca» o «Personale», «Prodotti»
     porta alla pagina dei prodotti, non di nuovo alla mappa (idem da
     «Grandi marche»).              */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const file = process.argv[2] || 'out/sito.html';
const html = fs.readFileSync(file, 'utf8');
const errori = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously', pretendToBeVisual: true,
  url: 'https://manliograndi-del.github.io/spesa/',
  virtualConsole: new VirtualConsole().on('jsdomError',
    e => errori.push(String(e.detail || e.message).split('\n')[0])),
  beforeParse(w) {
    w.scrollTo = () => {};
    /* Un telefono finto da 390×844: i pallini in cima, il menù in fondo,
       tutto il resto in mezzo. Basta per sapere da dove a dove va la freccia. */
    const rett = (l, t, wd, h) => ({ left: l, top: t, right: l + wd, bottom: t + h, width: wd, height: h, x: l, y: t });
    w.Element.prototype.getBoundingClientRect = function () {
      if (this.matches && this.matches('header .pallini')) return rett(300, 20, 80, 40);
      if (this.closest && this.closest('#riga-cerca')) {
        const i = [...this.parentNode.children].indexOf(this);
        return rett(10 + 95 * Math.max(i, 0), 780, 90, 56);
      }
      return rett(20, 300, 160, 120);
    };
  },
});

setTimeout(() => {
  const w = dom.window, d = w.document;
  const male = [];
  if (errori.length) male.push('errori nella pagina: ' + errori.join(' / '));
  try { w.eval('chiudiNovita()'); } catch (e) {}
  w.eval('frecceAiuto()');
  const ris = d.getElementById('risultato');
  const barra = d.querySelector('.barra');
  const acceso = () => [...d.querySelectorAll('#riga-cerca button')].filter(b => b.getAttribute('aria-pressed') === 'true');
  const frecce = () => d.getElementById('frecce-aiuto');

  const mappa = ris.querySelector('.mappa-aiuto');
  if (!mappa) { console.error('  ✗ all\'apertura non c\'è la mappa dell\'aiuto'); process.exit(1); }
  if (ris.querySelector('.prezzo-riga, .banda')) male.push('all\'apertura si vedono già delle offerte');
  if (!barra.classList.contains('giu')) male.push('all\'apertura la griglia dei prodotti è su');
  if (acceso().length) male.push('all\'apertura è acceso «' + acceso()[0].textContent.trim() + '»');
  if (d.querySelector('#tasti .tasto[aria-pressed="true"]')) male.push('all\'apertura c\'è un prodotto acceso');

  const fumetti = [...mappa.querySelectorAll('.fumetto')];
  const dove = w.eval('FUMETTI.map(f => f.dove)');
  if (fumetti.length !== 5) male.push('i fumetti sono ' + fumetti.length + ', non cinque');
  fumetti.forEach(f => {
    const t = f.querySelector('b'), x = f.querySelector('span');
    if (!t || !t.textContent.trim() || !x || x.textContent.trim().length < 10)
      male.push('un fumetto non dice niente: «' + f.textContent.trim() + '»');
    if (/\d+,\d\d|€/.test(f.textContent)) male.push('un fumetto ha dentro un prezzo: «' + f.textContent.trim() + '»');
  });
  dove.forEach(s => {
    const el = s === 'pallini' ? d.querySelector('header .pallini') : d.querySelector(s);
    if (!el) male.push('il tasto del fumetto «' + s + '» non c\'è');
  });
  // i quattro tasti del menù hanno ognuno il suo fumetto
  [...d.querySelectorAll('#riga-cerca button')].forEach(b => {
    if (!dove.some(s => s !== 'pallini' && d.querySelector(s) === b))
      male.push('«' + b.textContent.trim() + '» non ha il suo fumetto');
  });

  const svg = frecce();
  if (!svg) male.push('le frecce non ci sono');
  else {
    /* Dal 2026-09-24 (Manlio: «nuvolette più organiche») ogni fumetto è un
       palloncino con la coda a punta: una forma chiusa sola per fumetto. */
    const vie = [...svg.querySelectorAll('g path')];
    if (vie.length !== fumetti.length) male.push('i palloncini sono ' + vie.length + ' per ' + fumetti.length + ' fumetti');
    if (vie.some(p => !/Z$/.test(p.getAttribute('d')) || /NaN/.test(p.getAttribute('d'))))
      male.push('un palloncino non è una forma chiusa');
    const su = vie.filter(p => p.getAttribute('data-verso') === 'su');
    if (su.length !== 1) male.push('le code verso l\'alto sono ' + su.length + ', ne va una (ai pallini)');
  }
  if (!/#frecce-aiuto\{[^}]*pointer-events:none/.test(html)) male.push('le frecce rubano il dito ai tasti sotto');

  // «Prodotti»: via la mappa, su la griglia
  d.getElementById('vai-prodotti').click();
  if (ris.querySelector('.mappa-aiuto')) male.push('toccando «Prodotti» la mappa resta');
  /* Dal 2026-09-24 anche il benvenuto è un fumetto (Manlio: «trasformare
     anche questo in una nuvoletta… e si ricordi che toccando le schede esce
     la foto del volantino»): dopo «Prodotti» c'è UN palloncino, il suo. */
  const vieBv = frecce() ? [...frecce().querySelectorAll('g path')] : [];
  if (vieBv.length !== 1 || vieBv[0].getAttribute('class') !== 'p-bv')
    male.push('toccando «Prodotti» i palloncini sono ' + vieBv.length + ', ne va uno (il benvenuto)');
  const fBv = ris.querySelector('.benvenuto .fumetto');
  if (!fBv) male.push('il benvenuto non è un fumetto');
  else if (!/volantino/.test(fBv.textContent)) male.push('il fumetto del benvenuto non dice che toccando un\'offerta si vede il volantino');
  if (barra.classList.contains('giu')) male.push('toccando «Prodotti» la griglia non sale');
  if (d.getElementById('vai-prodotti').getAttribute('aria-pressed') !== 'true') male.push('toccando «Prodotti» non si accende');
  if (!ris.querySelector('.benvenuto')) male.push('toccando «Prodotti» non c\'è «Tocca un prodotto»');

  // il titolo la riporta, anche da un prodotto
  d.querySelector('#tasti .tasto:not(.agg)').click();
  if (frecce()) male.push('toccato un prodotto, il fumetto del benvenuto resta disegnato');
  d.getElementById('vai-inizio').click();
  if (!ris.querySelector('.mappa-aiuto')) male.push('toccando il titolo da un prodotto la mappa non torna');
  if (!barra.classList.contains('giu')) male.push('tornata la mappa, la griglia resta su');

  // da «Cerca» e da «Personale» si esce ai prodotti, non alla mappa
  for (const sel of ['#riga-cerca .trova', '#riga-cerca .marchi', '#vai-personale']) {
    d.getElementById('vai-inizio').click();
    d.querySelector(sel).click();
    if (ris.querySelector('.mappa-aiuto') && !ris.closest('[hidden]'))
      male.push('aprendo ' + sel + ' la mappa resta sotto');
    if (frecce()) male.push('aprendo ' + sel + ' le frecce restano');
    d.getElementById('vai-prodotti').click();
    if (ris.querySelector('.mappa-aiuto')) male.push('da ' + sel + ', «Prodotti» riporta alla mappa invece che ai prodotti');
    if (barra.classList.contains('giu')) male.push('da ' + sel + ', «Prodotti» non fa salire la griglia');
  }

  if (male.length) { male.forEach(m => console.error('  ✗ ' + m)); process.exit(1); }
  console.log('  mappa dell\'aiuto: ' + fumetti.length + ' fumetti con la freccia, nessun prodotto; «Prodotti» la toglie, «Spesa» la riporta');
  process.exit(0);
}, 800);
