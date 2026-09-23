/* Lo sconto in percentuale sulle schede (Manlio, 2026-09-23: «questa cifra in
   percentuale andrebbe messa fra il cerchietto dei giorni e l'icona del
   volantino»). Qui si controlla:
   - dove la nota dice «−30%» o «Sconto del 30%», la scheda mostra «−30%»;
   - lo sconto sta DOPO il cerchietto dei giorni e PRIMA del foglietto;
   - dove la nota non dice niente di sconti, il bollino non c'è;
   - un «prima» riferito al prezzo al kg non diventa uno sconto.          */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const file = process.argv[2] || 'out/sito.html';
const dom = new JSDOM(fs.readFileSync(file, 'utf8'), { runScripts: 'dangerously',
  pretendToBeVisual: true, virtualConsole: new VirtualConsole(),
  url: 'https://manliograndi-del.github.io/spesa/' });
setTimeout(() => {
  const w = dom.window, d = w.document, D = w.eval('DATI');
  const male = [];
  let viste = 0, con = 0;
  D.offerte.forEach(o => {
    const n = o.note || '';
    const m = n.match(/^\s*[−–-]\s?(\d{1,2})\s?%/) || n.match(/[Ss]conto(?: soci)?(?: del)? (\d{1,2})\s?%/);
    if (m && o.sconto !== +m[1]) male.push(`«${o.pro}»: la nota dice ${m[1]}%, la scheda ${o.sconto}`);
    if (!/%|[Pp]rima/.test(n) && o.sconto) male.push(`«${o.pro}»: sconto ${o.sconto}% inventato`);
    if (/al kg, prima|all'etto, prima|al litro, prima/.test(n) && !m && o.sconto)
      male.push(`«${o.pro}»: sconto calcolato su un prezzo al kg`);
  });
  // sulle schede vere: ordine e testo
  const tasti = [...d.querySelectorAll('.barra .tasto:not(.agg)')];
  tasti.forEach(t => {
    t.click();
    d.querySelectorAll('#risultato .prezzo-riga').forEach(r => {
      viste++;
      const s = r.querySelector('.angolo .sconto');
      if (!s) return;
      con++;
      if (!/^−\d{1,2}%$/.test(s.textContent)) male.push('bollino scritto male: ' + s.textContent);
      const figli = [...s.parentNode.children];
      const i = figli.indexOf(s);
      const giorni = figli.findIndex(e => e.classList.contains('giorni') || e.classList.contains('parte'));
      const foglio = figli.findIndex(e => e.classList.contains('dove'));
      if (giorni >= 0 && giorni > i) male.push('lo sconto sta prima del cerchietto');
      if (foglio >= 0 && foglio < i) male.push('lo sconto sta dopo il foglietto');
    });
  });
  if (!con) male.push('nessuna scheda mostra uno sconto');
  if (male.length) { console.error('MALE:\n  ' + [...new Set(male)].slice(0, 15).join('\n  ')); process.exit(1); }
  console.log(`  sconti: ${D.offerte.filter(o => o.sconto).length} offerte; sulle schede dei prodotti in lista ${con} su ${viste}, fra il cerchietto e il foglietto`);
  process.exit(0);
}, 500);
