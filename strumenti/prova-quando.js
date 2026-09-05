/* Controlla che le offerte non ancora cominciate non si spaccino per offerte
   di oggi: devono stare in fondo all'elenco, portare il bollo «vale dal ...»
   e non prendersi mai il bollo «il meno caro».

   Serve perche i volantini nuovi si leggono in anticipo. Il 2026-09-05 sono
   entrati quelli dell'Eurospin (dal 10) e dell'MD (dall'8): senza questo
   sarebbero finiti in cima, e Manlio avrebbe letto un prezzo che in cassa non
   gli avrebbero fatto.

       node prova-quando.js out/sito.html                 */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const errori = [];
const dom = new JSDOM(fs.readFileSync(process.argv[2], 'utf8'), {
  runScripts: 'dangerously', pretendToBeVisual: true,
  url: 'https://manliograndi-del.github.io/spesa/',
  virtualConsole: new VirtualConsole().on('jsdomError', e => errori.push(String(e.detail || e.message).split('\n')[0])),
});
setTimeout(() => {
  const d = dom.window.document;
  const guai = [];
  let visti = 0, futuri = 0;
  for (const b of [...d.querySelectorAll('.tasto')].filter(x => !x.classList.contains('agg'))) {
    const nome = b.textContent.trim();
    b.click();
    const righe = [...d.querySelectorAll('.prezzo-riga')].map(r => ({
      dopo: /vale dal/.test(r.textContent),
      meno: !!r.querySelector('.bollo.meno'),
    }));
    visti += righe.length;
    futuri += righe.filter(r => r.dopo).length;
    const primoFuturo = righe.findIndex(r => r.dopo);
    const ultimoValido = righe.map(r => r.dopo).lastIndexOf(false);
    if (primoFuturo !== -1 && primoFuturo < ultimoValido)
      guai.push(`«${nome}»: un'offerta non ancora valida sta sopra una che vale oggi`);
    righe.forEach((r, i) => {
      if (r.dopo && r.meno) guai.push(`«${nome}»: riga ${i + 1} non vale ancora e ha il bollo «il meno caro»`);
    });
  }
  console.log(`  righe guardate: ${visti}, di cui non ancora valide: ${futuri}`);
  const vol = [...d.querySelectorAll('#vol li')]
    .filter(li => /non ancora cominciato/.test(li.textContent))
    .map(li => li.querySelector('.i').textContent);
  console.log('  volantini segnati «non ancora cominciato»: ' + (vol.join(', ') || 'nessuno'));
  if (errori.length) guai.push('errori in pagina: ' + errori.join(' | '));
  if (guai.length) {
    console.log('\nNON VA:'); guai.forEach(g => console.log('  ✗ ' + g));
    process.exit(1);
  }
  console.log('  ogni offerta sta al posto giusto');
  process.exit(0);
}, 2500);
