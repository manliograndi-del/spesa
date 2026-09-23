/* La riga in cima a ogni prodotto, SOLO QUANDO SERVE (Manlio, 2026-09-23,
   punto 3: «va bene la prima»). Per ogni prodotto della lista si controlla:
   - «Oggi il meno caro» c'è se e solo se la scheda verde NON è la prima, e
     dice il negozio e il prezzo della scheda verde;
   - «Da … conviene di più» c'è se e solo se un'offerta che parte nei
     prossimi giorni costa meno (come si legge) della scheda verde;
   - se non c'è niente da dire, la riga non c'è affatto;
   - toccando una riga la pagina scende (qui: chiede di scorrere).       */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const file = process.argv[2] || 'out/sito.html';
const dom = new JSDOM(fs.readFileSync(file, 'utf8'), { runScripts: 'dangerously',
  pretendToBeVisual: true, virtualConsole: new VirtualConsole(),
  url: 'https://manliograndi-del.github.io/spesa/' });
setTimeout(() => {
  const w = dom.window, d = w.document;
  let scorsi = 0;
  w.scrollTo = () => { scorsi++; };
  const male = [];
  let conRiga = 0, senza = 0, oggi = 0, dopo = 0;
  const tasti = [...d.querySelectorAll('.barra .tasto:not(.agg)')];
  tasti.forEach(t => {
    t.click();
    const r = d.getElementById('risultato');
    const schede = [...r.querySelectorAll('.prezzo-riga')];
    const s = r.querySelector('.sintesi');
    if (!schede.length) { if (s) male.push(t.textContent + ': riga senza offerte'); return; }
    const verde = schede.find(x => x.classList.contains('vince'));
    const num = x => parseFloat(x.querySelector('.val .n').textContent.replace(',', '.'));
    const futura = schede.find(x => x.classList.contains('dopo'));
    const vuoleOggi = verde && schede[0] !== verde;
    const vuoleDopo = futura && (!verde || num(futura) < num(verde));
    const bo = s && s.querySelector('.sint.oggi'), bd = s && s.querySelector('.sint.dopo');
    if (!!bo !== !!vuoleOggi) male.push(t.textContent + ': «Oggi il meno caro» ' + (bo ? 'c\'è e non serve' : 'manca'));
    if (!!bd !== !!vuoleDopo) male.push(t.textContent + ': «Da … conviene di più» ' + (bd ? 'c\'è e non serve' : 'manca'));
    if (!vuoleOggi && !vuoleDopo && s) male.push(t.textContent + ': la riga c\'è senza niente da dire');
    const negozio = x => (x.querySelector('.marchio .solo-voce') || x.querySelector('.marchio')).textContent.trim();
    if (bo) {
      oggi++;
      if (!bo.textContent.includes(negozio(verde)) || !bo.textContent.includes(verde.querySelector('.val .n').textContent.trim()))
        male.push(t.textContent + ': «Oggi» non dice la scheda verde');
      const prima = scorsi; bo.click();
      if (scorsi === prima) male.push(t.textContent + ': toccando «Oggi» la pagina non scende');
    }
    if (bd) {
      dopo++;
      if (!/^Da (domani|dopodomani|\w+ \d+)/.test(bd.textContent.trim())) male.push(t.textContent + ': non dice quando parte: ' + bd.textContent);
      if (!bd.textContent.includes(negozio(futura)) || !bd.textContent.includes(futura.querySelector('.val .n').textContent.trim()))
        male.push(t.textContent + ': «Da …» non dice l\'offerta che parte');
    }
    if (s) conRiga++; else senza++;
  });
  if (male.length) { console.error('MALE:\n  ' + [...new Set(male)].slice(0, 15).join('\n  ')); process.exit(1); }
  console.log(`  riga in cima: su ${tasti.length} prodotti c'è in ${conRiga} (oggi ${oggi}, prossimi giorni ${dopo}), manca in ${senza} dove non serve`);
  process.exit(0);
}, 500);
