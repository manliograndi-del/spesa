/* Prova il tasto delle lingue: le scritte devono cambiare, i dati restare
   italiani. Controlla anche che non resti un buco da qualche parte. */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const errori = [];
const dom = new JSDOM(fs.readFileSync(process.argv[2], 'utf8'), {
  runScripts: 'dangerously', pretendToBeVisual: true,
  url: 'https://manliograndi-del.github.io/spesa/',
  virtualConsole: new VirtualConsole().on('jsdomError', e => errori.push(String(e.detail || e.message).split('\n')[0])),
});
setTimeout(() => {
  const d = dom.window.document, W = dom.window;
  const lingue = [...d.querySelectorAll('#lingue button')];
  console.log('tasti lingua:', lingue.map(b => b.textContent).join(' '));
  let male = 0;
  const dimmi = (ok, x) => { console.log(`  ${ok ? '·' : 'MALE'} ${x}`); if (!ok) male++; };

  for (const b of lingue) {
    errori.length = 0;
    b.dispatchEvent(new W.MouseEvent('click', { bubbles: true }));
    const sigla = b.textContent;
    const titolo = d.getElementById('h-titolo').textContent;
    const spiega = d.getElementById('spiega').textContent;
    const btnAgg = d.querySelector('#form-agg button').textContent;
    // apro un prodotto e guardo etichette e dati
    const p = [...d.querySelectorAll('#tasti .tasto')].find(x => x.textContent === 'Carne di bue');
    p.dispatchEvent(new W.MouseEvent('click', { bubbles: true }));
    const unita = d.querySelector('.prezzo-riga .val .u').textContent;
    const nomeProd = d.querySelector('.prezzo-riga .nome').textContent;
    const cambia = d.querySelector('.gestisci button').textContent;
    const vuoti = [...d.querySelectorAll('#h-titolo,#h-sottotitolo,#h-volantini,#h-manda,#h-letto,#h-pie')]
                   .filter(e => !e.textContent.trim()).length;
    console.log(`\n[${sigla}] «${titolo}» · agg:«${btnAgg}» · unità:«${unita}» · «${cambia}»`);
    dimmi(errori.length === 0, errori.length ? 'errori: ' + errori.join(' ;; ') : 'nessun errore');
    dimmi(vuoti === 0, `${vuoti} scritte fisse rimaste vuote`);
    dimmi(spiega.length > 200, `spiegazione tradotta (${spiega.length} caratteri)`);
    dimmi(nomeProd.includes('hamburger') || nomeProd.includes('bovino') || nomeProd.includes('Le Specialità'),
          `il dato resta italiano: «${nomeProd.slice(0, 46)}»`);
    dimmi(d.querySelectorAll('.prezzo-riga').length === 11, `11 prezzi ancora tutti lì`);
  }
  // e la lingua si ricorda?
  console.log('\nlingua salvata:', W.localStorage.getItem('spesa.lingua.v1'));
  console.log(male ? `\n${male} cose non vanno` : '\ntutto a posto');
  process.exit(male ? 1 : 0);
}, 2500);
