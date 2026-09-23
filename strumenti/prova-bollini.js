/* Le note diventano bollini brevi (Manlio, 2026-09-23: «le note gialle
   diventano bollini brevi, e tolgo i numeri ripetuti»). Qui si controlla:
   - un'offerta con tessera, app o soci ha il suo bollino, e quelle Pam
     dicono «Solo con app»;
   - un 1+1 ha il bollino «1+1»;
   - NESSUN NUMERO DELLA NOTA SI PERDE: ogni prezzo scritto nella nota o sta
     ancora nei dettagli, o è lo stesso numero di un prezzo della scheda, o è
     il «prima» dello sconto che ha il suo bollino;
   - sulla scheda la nota è chiusa, «Dettagli» la apre e la richiude.     */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const file = process.argv[2] || 'out/sito.html';
const dom = new JSDOM(fs.readFileSync(file, 'utf8'), { runScripts: 'dangerously',
  pretendToBeVisual: true, virtualConsole: new VirtualConsole(),
  url: 'https://manliograndi-del.github.io/spesa/' });
setTimeout(() => {
  const w = dom.window, d = w.document, D = w.eval('DATI');
  const male = [];
  const num = t => parseFloat(t.replace(',', '.'));
  const eur = w.eval('eur');
  D.offerte.forEach(o => {
    const n = o.note || '', b = o.bolli || [];
    if (/Lidl Plus|Buona Spesa Card|Carta Insieme|EKOM UP|SpesAmica|CARTA BENNET|Fidelity Card|Perte Plus|soci Coop/.test(n)
        && !b.some(x => /tessera|app|Lidl Plus|soci/.test(x)))
      male.push(`«${o.pro}» (${o.ins}): la nota dice tessera ma il bollino non c'è`);
    if (o.ins === 'Pam' && /Perte Plus/.test(n) && !b.includes('Solo con app'))
      male.push(`«${o.pro}»: Pam con app senza «Solo con app»`);
    if (/\d\s*\+\s*\d/.test(o.fmt) && !b.some(x => /^\d\+\d$/.test(x)))
      male.push(`«${o.pro}»: ${o.fmt} senza il bollino 1+1`);
    if (o.det && o.det.length > n.length) male.push(`«${o.pro}»: i dettagli sono più lunghi della nota`);
    /* Nessun numero perso. */
    /* I numeri come la scheda li scrive: «uguale» vuol dire uguale a quello
       che si legge. */
    const noti = [eur(o.prezzo), eur(o.unitario)].map(num);
    const re = /(\d+,\d+)/g;
    let m;
    while ((m = re.exec(n))) {
      if (o.det.includes(m[1])) continue;
      /* Il «prima» dello sconto (anche al kg, «prima 2,69, cioè 33,63 al
         kg») sta nel bollino dello sconto. */
      if (o.sconto && /[Pp]rima (?:[\d,]+,? cioè )?$/.test(n.slice(Math.max(0, m.index - 25), m.index))) continue;
      if (noti.includes(num(m[1]))) continue;
      male.push(`«${o.pro}»: il numero ${m[1]} della nota è sparito (${n})`);
    }
  });
  /* Sulle schede vere. */
  let schede = 0, aperte = 0, bolli = 0;
  const tasti = [...d.querySelectorAll('.barra .tasto:not(.agg)')];
  tasti.forEach(t => {
    t.click();
    d.querySelectorAll('#risultato .prezzo-riga').forEach(r => {
      schede++;
      bolli += r.querySelectorAll('.cond .bollo.cond').length;
      const nota = r.querySelector('.nota'), bt = r.querySelector('.dettagli');
      if (!nota && bt) male.push('«Dettagli» senza niente da aprire');
      if (!nota) return;
      if (!bt) { male.push('una nota senza il tasto «Dettagli»'); return; }
      if (!nota.hidden) male.push('una nota è aperta prima di toccare «Dettagli»');
      bt.click();
      if (nota.hidden || bt.getAttribute('aria-expanded') !== 'true') male.push('«Dettagli» non apre la nota');
      else aperte++;
      bt.click();
      if (!nota.hidden) male.push('«Dettagli» non richiude la nota');
    });
  });
  if (!aperte) male.push('nessuna scheda ha «Dettagli»');
  if (!bolli) male.push('nessuna scheda ha bollini');
  if (male.length) { console.error('MALE:\n  ' + [...new Set(male)].slice(0, 15).join('\n  ')); process.exit(1); }
  const conNota = D.offerte.filter(o => o.note).length, conDet = D.offerte.filter(o => o.det).length;
  console.log(`  bollini: note lunghe da ${conNota} a ${conDet}; sulle schede dei prodotti in lista ${bolli} bollini, ${aperte} «Dettagli» provati su ${schede}`);
  process.exit(0);
}, 500);
