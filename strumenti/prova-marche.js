/* I due tasti in cima, «Cerca un prodotto o una marca» e «GRANDI MARCHE».
   Manlio, 2026-09-23: «devono essere delle stesse dimensioni, Grandi Marche
   messo a destra; deve portare a una pagina dove ci sono solo i tasti delle
   grandi marche e non un tasto di ricerca; l'altro ha una pagina dove c'è
   solo la ricerca». Qui si controlla:
   - GRANDI MARCHE sta a destra del tasto rosso, e la regola li fa larghi uguali;
   - dal tasto GRANDI MARCHE: le pillole ci sono, la casella no;
   - toccata una marca escono le sue offerte;
   - dal tasto rosso: la casella c'è, le pillole no — anche passando
     direttamente dall'uno all'altro senza chiudere.                        */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const file = process.argv[2] || 'out/sito.html';
const html = fs.readFileSync(file, 'utf8');
const errori = [];
const vc = new VirtualConsole().on('jsdomError',
  e => errori.push(String(e.detail || e.message).split('\n')[0]));
const dom = new JSDOM(html, { runScripts: 'dangerously', pretendToBeVisual: true,
  virtualConsole: vc, url: 'https://manliograndi-del.github.io/spesa/' });

setTimeout(() => {
  const d = dom.window.document;
  const male = [];
  if (errori.length) male.push('errori nella pagina: ' + errori.join(' / '));
  const riga = d.getElementById('riga-cerca');
  const tasti = [...riga.querySelectorAll('button')];
  const rosso = riga.querySelector('.trova'), gm = riga.querySelector('.marchi');
  if (!rosso || !gm) { console.error('MANCA uno dei due tasti'); process.exit(1); }
  if (tasti.indexOf(gm) < tasti.indexOf(rosso)) male.push('GRANDI MARCHE non sta a destra');
  if (!/\.riga-cerca \.tasto\.trova,\.riga-cerca \.tasto\.marchi\{flex:1 1 0/.test(html))
    male.push('manca la regola che fa i due tasti larghi uguali');

  const q = d.getElementById('q'), marche = d.getElementById('marche');
  gm.click();
  const gm2 = () => d.querySelector('#riga-cerca .marchi');
  const rosso2 = () => d.querySelector('#riga-cerca .trova');
  if (marche.hidden || !marche.querySelector('button')) male.push('GRANDI MARCHE: niente pillole');
  if (!q.hidden) male.push('GRANDI MARCHE: la casella di ricerca si vede');
  const una = marche.querySelector('button:not(:disabled)');
  if (una) {
    una.click();
    if (!d.querySelectorAll('#trovati .prezzo-riga').length) male.push('toccata una marca, nessuna offerta');
  }
  rosso2().click();   // dritto alla ricerca, senza chiudere
  if (q.hidden) male.push('ricerca: la casella non si vede');
  if (!marche.hidden) male.push('ricerca: si vedono le grandi marche');
  if (q.value) male.push('ricerca: la casella è rimasta piena della marca di prima');
  if (rosso2().textContent !== 'Cerca') male.push('il tasto dice «' + rosso2().textContent + '», non «Cerca»');
  if (rosso2().getAttribute('aria-pressed') !== 'true') male.push('nella ricerca «Cerca» non è rosso');
  if (gm2().getAttribute('aria-pressed') !== 'false') male.push('nella ricerca GRANDI MARCHE non è bianco');
  if (!d.querySelector('.barra').hidden) male.push('nella ricerca si vedono ancora le categorie');
  if (!d.querySelector('.spiega').hidden) male.push('nella ricerca c\'è ancora in fondo l\'elenco dei volantini');
  // il titolo riporta all'inizio
  d.getElementById('vai-inizio').dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true, cancelable: true }));
  if (!d.getElementById('ricerca').hidden) male.push('toccando il titolo la ricerca resta aperta');
  if (d.querySelector('.barra').hidden || d.querySelector('.spiega').hidden) male.push('dopo il titolo le categorie o il fondo non tornano');
  if (rosso2().getAttribute('aria-pressed') !== 'false' || gm2().getAttribute('aria-pressed') !== 'false')
    male.push('all\'inizio i due tasti non sono bianchi tutti e due');
  gm2().click(); gm2().click();
  if (!d.getElementById('ricerca').hidden) male.push('GRANDI MARCHE non si chiude');

  if (male.length) { console.error('MALE:\n  ' + male.join('\n  ')); process.exit(1); }
  console.log('  i due tasti: grandi uguali, GRANDI MARCHE a destra, marche senza casella, ricerca senza marche');
  process.exit(0);
}, 400);
