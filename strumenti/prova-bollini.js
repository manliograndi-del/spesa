/* Le note diventano bollini brevi (Manlio, 2026-09-23: «le note gialle
   diventano bollini brevi, e tolgo i numeri ripetuti»), e il resto della
   nota non si mostra più («toglierei del tutto la scritta dettagli»). Qui si
   controlla:
   - un'offerta con tessera, app o soci ha il suo bollino, e quelle Pam
     dicono «Solo con app»;
   - un 1+1 ha il bollino «1+1»;
   - sulle schede non c'è né «Dettagli» né il riquadro della nota;
   - TOCCANDO UNA SCHEDA si apre la pagina del volantino sopra l'elenco
     (immagine, o il visore per il Conad), col tasto «Chiudi» che la chiude
     (Manlio, 2026-09-23).                                               */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const file = process.argv[2] || 'out/sito.html';
const dom = new JSDOM(fs.readFileSync(file, 'utf8'), { runScripts: 'dangerously',
  pretendToBeVisual: true, virtualConsole: new VirtualConsole(),
  url: 'https://manliograndi-del.github.io/spesa/' });
setTimeout(() => {
  const w = dom.window, d = w.document, D = w.eval('DATI');
  const male = [];
  D.offerte.forEach(o => {
    const n = o.note || '', b = o.bolli || [];
    if (/Lidl Plus|Buona Spesa Card|Carta Insieme|EKOM UP|SpesAmica|CARTA BENNET|Fidelity Card|Perte Plus|soci Coop/.test(n)
        && !b.some(x => /tessera|app|Lidl Plus|soci/.test(x)))
      male.push(`«${o.pro}» (${o.ins}): la nota dice tessera ma il bollino non c'è`);
    if (o.ins === 'Pam' && /Perte Plus/.test(n) && !b.includes('Solo con app'))
      male.push(`«${o.pro}»: Pam con app senza «Solo con app»`);
    /* L'«Offerta Family» dell'Eurospin vale solo con la carta Eurospin
       Family (Manlio, 2026-09-24: «offerta Family e il logo Eurospin Family
       vogliono dire che si possono acquistare con lo sconto solo con la
       carta»). */
    if (o.ins === 'Eurospin' && /Eurospin Family/.test(n) && !b.includes('Con carta Family'))
      male.push(`«${o.pro}»: offerta Family senza «Con carta Family»`);
    /* Il prezzo senza tessera è una pillola sua, con la sua unità se ce l'ha
       (Manlio, 2026-09-23: «se è davvero importante e breve, in un'altra
       pillola beige»). */
    const st = n.match(/[Ss]enza tessera (\d+(?:,\d+)?)( al kg| al litro| all'etto)?/);
    if (st && !b.includes('Senza tessera ' + st[1] + ' €' + (st[2] || '')))
      male.push(`«${o.pro}»: manca «Senza tessera ${st[1]} €${st[2] || ''}»`);
    b.forEach(x => { if (/\d,\s|,\s*€/.test(x)) male.push(`«${o.pro}»: numero scritto male, «${x}»`); });
    b.forEach(x => { if (x.length > 34) male.push(`«${o.pro}»: pillola troppo lunga, «${x}»`); });
    if (/\d\s*\+\s*\d/.test(o.fmt) && !b.some(x => /^\d\+\d$/.test(x)))
      male.push(`«${o.pro}»: ${o.fmt} senza il bollino 1+1`);
  });
  /* Sulle schede vere. */
  let schede = 0, aperte = 0, bolli = 0;
  const sopra = d.getElementById('vol-sopra');
  const tasti = [...d.querySelectorAll('.barra .tasto:not(.agg)')];
  tasti.forEach(t => {
    t.click();
    d.querySelectorAll('#risultato .prezzo-riga').forEach((r, i) => {
      schede++;
      bolli += r.querySelectorAll('.cond .bollo.cond').length;
      if (r.querySelector('.dettagli, .nota')) male.push('c\'è ancora «Dettagli» o la nota');
      if (i > 2) return;                    // ne basta qualcuna per prodotto
      if (!r.classList.contains('apribile')) { male.push('una scheda non si apre toccandola'); return; }
      r.querySelector('.nome').click();
      if (sopra.hidden) { male.push('toccando la scheda il volantino non si apre'); return; }
      const f = sopra.querySelector('#foglio-vol img, #foglio-vol iframe');
      if (!f) male.push('il volantino si apre vuoto');
      if (!/pagina \d+/.test(d.getElementById('titolo-vol').textContent))
        male.push('in cima non dice che pagina è');
      if (!d.getElementById('fuori-vol').href) male.push('manca «Apri sul sito»');
      if (!/^Chiudi$/.test(d.getElementById('chiudi-vol').textContent.trim())) male.push('manca il tasto «Chiudi»');
      d.getElementById('chiudi-vol').click();
      if (!sopra.hidden) male.push('«Chiudi» non chiude');
      else aperte++;
    });
  });
  /* Il foglietto in cima alla scheda apre la stessa finestra, non un'altra
     scheda del browser. */
  const a = d.querySelector('#risultato .prezzo-riga a.dove.apri');
  if (a) {
    a.click();
    if (sopra.hidden) male.push('il foglietto non apre la pagina sopra l\'elenco');
    d.getElementById('chiudi-vol').click();
  }
  if (!aperte) male.push('nessuna scheda provata');
  if (!bolli) male.push('nessuna scheda ha bollini');
  if (male.length) { console.error('MALE:\n  ' + [...new Set(male)].slice(0, 15).join('\n  ')); process.exit(1); }
  console.log(`  bollini: ${bolli} sulle ${schede} schede dei prodotti in lista, niente «Dettagli»; ${aperte} schede toccate aprono il volantino e «Chiudi» lo chiude`);
  process.exit(0);
}, 500);
