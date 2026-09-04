/* Controlla che la pagina non dica cose false su se stessa: la data dev'essere
   una sola, e la frase sulla lista deve dire la verita per QUESTA copia. */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const dom = new JSDOM(fs.readFileSync(process.argv[2], 'utf8'), {
  runScripts: 'dangerously', pretendToBeVisual: true,
  url: 'https://manliograndi-del.github.io/spesa/',
  virtualConsole: new VirtualConsole(),
});
setTimeout(() => {
  const d = dom.window.document;
  const letto = d.getElementById('letto').textContent;
  const pie = d.getElementById('pie').textContent;
  const lista = d.getElementById('p-lista').textContent;
  const scaduti = [...d.querySelectorAll('#vol .p')].filter(e => /scaduto/.test(e.textContent));
  console.log('  in mezzo:', letto);
  console.log('  in fondo:', pie);
  const d1 = (letto.match(/\d+ \w+ \d{4}/) || [''])[0];
  const d2 = (pie.match(/\d+ \w+ \d{4}/) || [''])[0];
  console.log('  le due date combaciano:', d1 === d2 && !!d1);
  console.log('  parla di volantini e non di PDF:', /volantini\./.test(pie));
  console.log('  frase sulla lista:', lista.slice(0, 72) + '…');
  console.log('  volantini segnati scaduti:', scaduti.map(e => e.textContent.split('—')[0].trim()).join(', ') || 'nessuno');
  process.exit(0);
}, 2000);
