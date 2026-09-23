/* I TITOLI DELLE OFFERTE: LA MARCA PER PRIMA (Manlio, 2026-09-23 sera, scelta
   A: la marca su una riga sua, sopra il nome). Si controlla:
   - su OGNI offerta, marca + nome + aggiunte usano solo parole del nome
     scritto nei dati: la scheda non inventa niente;
   - e non ne perde di importanti: quello che manca può essere solo ciò che la
     scheda dice già altrove (al banco, 3+1, il peso accanto al prezzo);
   - il trattino « – » non si vede più in nessuna scheda, e la marca sta
     sopra il nome;
   - le offerte che nei dati hanno la marca dopo il trattino la mostrano.   */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const file = process.argv[2] || 'out/sito.html';
const errori = [];
const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
  runScripts: 'dangerously', pretendToBeVisual: true,
  url: 'https://manliograndi-del.github.io/spesa/',
  virtualConsole: new VirtualConsole().on('jsdomError', e => errori.push(String(e.detail || e.message).split('\n')[0])),
});
setTimeout(() => {
  const w = dom.window, d = w.document;
  const male = [];
  if (errori.length) male.push('errori nella pagina: ' + errori.join(' / '));
  const parole = s => (s || '').toLowerCase().match(/[\p{L}\p{N}]+/gu) || [];
  const offerte = w.eval('DATI.offerte');
  let conMarca = 0, perse = 0;
  offerte.forEach(o => {
    const scritte = [o.marca || '', o.nome || o.pro].concat(o.agg || []).join(' ');
    const dati = new Set(parole(o.pro));
    const inventate = parole(scritte).filter(p => !dati.has(p));
    if (inventate.length) male.push('«' + o.pro + '»: la scheda scrive parole che non ci sono (' + inventate.join(', ') + ')');
    const viste = new Set(parole(scritte));
    const mancano = parole(o.pro).filter(p => !viste.has(p));
    const giaDette = new Set(parole([o.fmt].concat(o.bolli || []).join(' ') + ' al banco'));
    const davvero = mancano.filter(p => !giaDette.has(p));
    if (davvero.length) { perse++; male.push('«' + o.pro + '»: la scheda perde ' + davvero.join(', ')); }
    if (/ – /.test(o.pro) && !o.marca) male.push('«' + o.pro + '»: ha la marca dopo il trattino ma non la mostra');
    if (o.marca) conMarca++;
    if (/ – /.test(o.nome || '') || / – /.test(o.marca || '')) male.push('«' + o.pro + '»: il trattino resta nel titolo');
  });
  if (conMarca < offerte.length / 2) male.push('solo ' + conMarca + ' offerte su ' + offerte.length + ' hanno la marca');

  // sulle schede vere: niente trattini, marca sopra il nome
  let schede = 0, marche = 0;
  [...d.querySelectorAll('.barra .tasto:not(.agg)')].forEach(t => {
    t.click();
    d.querySelectorAll('#risultato .prezzo-riga .nome').forEach(n => {
      schede++;
      if (/ – /.test(n.textContent)) male.push('una scheda mostra ancora il trattino: ' + n.textContent);
      const m = n.querySelector('.marca');
      if (m) { marche++; if (n.firstChild !== m) male.push('la marca non sta in cima al titolo: ' + n.textContent); }
    });
  });
  if (!marche) male.push('nessuna scheda mostra la marca');
  if (male.length) { console.error('MALE:\n  ' + [...new Set(male)].slice(0, 20).join('\n  ')); process.exit(1); }
  console.log(`  titoli: ${conMarca} offerte su ${offerte.length} con la marca; sulle schede dei prodotti ${marche} su ${schede}`);
  console.log('  nessuna parola inventata né persa, nessun trattino in vista');
  process.exit(0);
}, 800);
