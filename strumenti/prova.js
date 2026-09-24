/* Apre la pagina in un browser finto e controlla che faccia quello che deve.
   Serve perche i due guasti peggiori (uno script chiuso a meta da un commento,
   e un pezzo che partiva prima che la lista esistesse) non si vedevano ne
   rileggendo il codice ne controllando la sintassi: la pagina usciva bella e
   muta. Questo la apre, clicca i bottoni e guarda se escono i prezzi.

       cd /tmp/dom && node .../prova.js <file.html>   (serve: npm install jsdom) */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');

const file = process.argv[2];
const errori = [];
const vc = new VirtualConsole()
  .on('jsdomError', e => errori.push(String(e.detail && e.detail.stack || e.message).split('\n').slice(0,3).join(' | ')))
  .on('error', (...a) => errori.push('console.error: ' + a.join(' ')));

const dom = new JSDOM(fs.readFileSync(file, 'utf8'),
  { runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    url: 'https://manliograndi-del.github.io/spesa/' });

setTimeout(() => {
  const d = dom.window.document;
  const tasti = [...d.querySelectorAll('#tasti .tasto')].filter(b => !b.classList.contains('agg'));
  const ris = d.getElementById('risultato');
  let male = 0;

  const dimmi = (ok, testo) => { console.log(`  ${ok ? '·' : 'MALE'} ${testo}`); if (!ok) male++; };

  console.log(file.split('/').pop());
  dimmi(errori.length === 0, errori.length ? 'errori: ' + errori.join(' ;; ') : 'nessun errore');
  dimmi(tasti.length > 0, `${tasti.length} bottoni dei prodotti`);
  /* All'apertura NON c'è un prodotto scelto (Manlio, 2026-09-24: «non mi
     piace che arrivi direttamente al Manzo con una lunga lista sotto»): c'è
     la pagina di benvenuto, che dice di toccare un prodotto, e nessun
     bottone acceso. */
  const bv = ris && ris.querySelector('.benvenuto');
  dimmi(!!bv && /Tocca un prodotto/.test(bv.textContent)
        && !ris.querySelector('.prezzo-riga') && !tasti.some(b => b.getAttribute('aria-pressed') === 'true'),
        bv ? 'all\'apertura la pagina di benvenuto, nessun prodotto acceso' : 'all\'apertura manca la pagina di benvenuto');

  // clicco ogni bottone e pretendo prezzi, o una riga che dica che non ce ne
  // sono. L'elenco delle pagine sotto le offerte non c'è più dal 2026-09-23
  // sera (Manlio: «togli anche l'elenco delle pagine sotto le offerte»).
  for (const b of tasti) {
    errori.length = 0;
    b.dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true }));
    const prezzi = ris.querySelectorAll('.prezzo-riga').length;
    const detto = ris.querySelector('.vuoto');
    const pagine = ris.querySelectorAll('.pag-riga, .altre').length;
    dimmi(errori.length === 0 && (prezzi > 0 || !!detto) && pagine === 0,
          `«${b.textContent}»: ${prezzi} prezzi` + (prezzi ? '' : ', «' + (detto ? detto.textContent : 'niente') + '»') +
          (pagine ? ', e l\'elenco delle pagine c\'è ancora' : '') +
          (errori.length ? ' — ' + errori.join(' ;; ') : ''));
  }
  /* Il titolo «Spesa» riporta alla pagina di benvenuto. */
  d.getElementById('vai-inizio').dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true, cancelable: true }));
  dimmi(!!ris.querySelector('.benvenuto') && !ris.querySelector('.prezzo-riga'),
        'toccando il titolo si torna alla pagina di benvenuto');
  console.log(male ? `  ${male} cose non vanno\n` : '  tutto a posto\n');
  process.exit(male ? 1 : 0);
}, 2500);
