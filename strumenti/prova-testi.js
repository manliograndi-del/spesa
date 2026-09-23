/* Controlla che la pagina non dica cose false su se stessa: la data dev'essere
   quella dei volantini, e la frase su chi vede la lista deve dire la verita
   per QUESTA copia.

       node prova-testi.js out/sito.html
       node prova-testi.js out/pagina.html --condivisa

   La frase sulla lista NON dipende da come e stato generato il file: la decide
   la pagina quando parte, guardando se il servizio di Claude le risponde. In un
   browser finto non risponde mai, quindi senza --condivisa anche la copia di
   Claude direbbe «solo tua» — vero per come e stata aperta, non per com'e
   davvero. Con --condivisa si finge che risponda, ed e cosi che va provata. */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const file = process.argv[2];
const condivisa = process.argv.includes('--condivisa');
const errori = [];
const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
  runScripts: 'dangerously', pretendToBeVisual: true,
  url: 'https://manliograndi-del.github.io/spesa/',
  beforeParse(w) {
    if (condivisa) w.claude = { use: async () => ({ publish: async () => {} }) };
  },
  virtualConsole: new VirtualConsole()
    .on('jsdomError', e => errori.push(String(e.detail || e.message).split('\n')[0])),
});
setTimeout(() => {
  const d = dom.window.document;
  /* Dal 2026-09-23 sera il riquadro in fondo non c'è più (Manlio: «lo
     toglierei dappertutto»): la data resta solo nel piede, e la frase su chi
     vede la lista sta nell'Aiuto («Questa copia»). */
  const letto = dom.window.eval('DATI.letto');
  const pie = d.getElementById('pie').textContent;
  const lista = d.getElementById('dove-vive').textContent;
  console.log('  copia provata come:', condivisa ? 'condivisa (di Claude)' : 'solo tua (sito o file)');
  console.log('  letti il:', letto);
  console.log('  in fondo:', pie);
  const d2 = (pie.match(/\d+ \w+ \d{4}/) || [''])[0];
  const dice_condivisa = /condivisa/.test(lista);
  const guai = [];
  if (!letto || d2 !== letto) guai.push(`la data in fondo non è quella dei volantini: «${d2}» e «${letto}»`);
  if (!/volantini\./.test(pie)) guai.push('il piede parla ancora di PDF');
  if (!/marchi .*restano di chi li ha/.test(pie)) guai.push('il piede non dice più di chi sono i marchi');
  if (!lista.trim()) guai.push('l\'Aiuto non dice di chi è questa copia');
  if (dice_condivisa !== condivisa)
    guai.push(`dice «${dice_condivisa ? 'condivisa' : 'solo tua'}» ma questa copia e l'altra cosa`);
  console.log('  la data in fondo è quella dei volantini:', d2 === letto && !!letto, `(${d2})`);
  console.log('  frase sulla copia:', lista.slice(0, 72) + '…');
  if (errori.length) guai.push('errori in pagina: ' + errori.join(' | '));
  if (guai.length) {
    console.log('\nNON VA:'); guai.forEach(g => console.log('  ✗ ' + g));
    process.exit(1);
  }
  console.log('  tutto vero');
  process.exit(0);
}, 2000);
