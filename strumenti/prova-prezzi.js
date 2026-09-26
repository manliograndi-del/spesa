/* La pagina dei prezzi più bassi (storia/prezzi.html, fatta da prezzi.py):
   si apre senza errori, ha le categorie, e per ognuna le settimane vanno dalla
   più recente in giù, il primo prezzo di ogni settimana è davvero il più
   basso, e nessuna settimana è nel futuro (il «più basso» di una settimana
   che deve ancora venire sarebbe falso).

       node prova-prezzi.js <progetto>/storia/prezzi.html */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');

const errori = [];
const vc = new VirtualConsole()
  .on('jsdomError', e => errori.push(String(e.message)))
  .on('error', (...a) => errori.push(a.join(' ')));
const dom = new JSDOM(fs.readFileSync(process.argv[2], 'utf8'),
  { runScripts: 'dangerously', virtualConsole: vc, url: 'https://manliograndi-del.github.io/spesa/storia/prezzi.html' });

setTimeout(() => {
  const w = dom.window, d = w.document;
  const male = [];
  if (errori.length) male.push('errori: ' + errori.join(' ;; '));
  const sel = d.getElementById('cat');
  const cat = sel ? [...sel.querySelectorAll('option')].map(o => o.value) : [];
  if (cat.length < 50) male.push('troppo poche categorie: ' + cat.length);
  const D = w.eval('D');
  const oggi = D.oggi;
  const num = s => parseFloat(s.replace(/\./g, '').replace(',', '.'));
  let settimane = 0;
  cat.forEach(c => {
    sel.value = c;
    sel.dispatchEvent(new w.Event('change'));
    const blocchi = [...d.querySelectorAll('#elenco .settimana')];
    if (!blocchi.length) male.push(c + ': nessuna settimana');
    const lunedi = D.dati[c].s.map(s => s.w);
    if (lunedi.some((x, i) => i && x >= lunedi[i - 1])) male.push(c + ': settimane fuori ordine');
    if (lunedi.some(x => x > oggi)) male.push(c + ': una settimana nel futuro');
    blocchi.forEach(b => {
      settimane++;
      const prezzi = [...b.querySelectorAll('.prezzo b')].map(x => num(x.textContent));
      if (prezzi.some(p => !(p > 0))) male.push(c + ': un prezzo che non è un numero');
      if (prezzi.some(p => p < prezzi[0])) male.push(c + ': il primo non è il più basso');
    });
    /* Il grafico: un punto per settimana, la linea se sono almeno due, e il
       valore scritto è quello della settimana mostrata sotto (all'inizio
       l'ultima, cioè questa). */
    const punti = d.querySelectorAll('#grafico svg circle').length;
    if (punti !== lunedi.length) male.push(c + ': ' + punti + ' punti per ' + lunedi.length + ' settimane');
    if (lunedi.length > 1 && !d.querySelector('#grafico svg polyline')) male.push(c + ': manca la linea');
    const scritto = d.querySelector('#grafico .valore');
    const sotto = d.querySelector('#scelta .prezzo b');
    if (!scritto || !sotto || scritto.textContent !== sotto.textContent)
      male.push(c + ': il valore sul grafico non è quello della settimana sotto');
    const primaSett = d.querySelector('#scelta .quando span');
    const ultima = d.querySelector('#elenco .settimana .quando span');
    if (!primaSett || !ultima || primaSett.textContent !== ultima.textContent)
      male.push(c + ': all\'inizio il grafico non mostra la settimana più recente');
    /* Le marche proprie dei discount non si scrivono, come nella Spesa. */
    d.querySelectorAll('#elenco .marca').forEach(m => {
      if (Object.values(D.proprie).some(l => l.includes(m.textContent)))
        male.push(c + ': si vede la marca propria «' + m.textContent + '»');
    });
  });
  console.log(`prezzi.html: ${cat.length} categorie, ${settimane} settimane`);
  if (male.length) { console.log('  MALE ' + male.slice(0, 15).join('\n  MALE ')); process.exit(1); }
  console.log('  tutto a posto');
  process.exit(0);
}, 800);
