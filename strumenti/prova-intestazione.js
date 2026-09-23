/* Sopra le offerte di un prodotto non c'è niente: niente nome ripetuto,
   niente «i», niente «Offerte ordinate…».

   Manlio, 2026-09-23 sera: «dato che la categoria di prodotti si capisce già
   perché il tasto è acceso, non si potrebbe togliere l'intestazione con il
   nome ripetuto in alto, e soprattutto quella scritta che i prodotti sono
   ordinati in ordine di prezzo»; e subito dopo: «i prodotti si potrebbero
   togliere deselezionandoli nella lista; la personalizzazione dei sinonimi
   forse è un po' troppo complicata… se vogliono mettere una cosa strana la
   possono mettere nella parte personalizzata».

   Qui si controlla:
   - sopra le offerte non c'è l'intestazione, né la «i», né il suo pannello
     («Elimina prodotto», «Cambia nome», i sinonimi), né la scritta;
   - un prodotto si toglie spegnendolo in «Organizza i prodotti», e si
     rimette riaccendendolo;
   - un prodotto che uno si era scritto a mano (fuori catalogo) sta in cima
     al catalogo, acceso, e si può spegnere: se no non si toglierebbe più;
   - nel catalogo non c'è più la casella per scrivere nomi nuovi.           */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const errori = [];
const SUO = { nome: 'Lievito madre', parole: ['lievitomadre'], cat: null };
const dom = new JSDOM(fs.readFileSync(process.argv[2], 'utf8'), {
  runScripts: 'dangerously', pretendToBeVisual: true,
  url: 'https://manliograndi-del.github.io/spesa/',
  beforeParse(w) { w.scrollTo = () => {}; },
  virtualConsole: new VirtualConsole()
    .on('jsdomError', e => errori.push(String(e.detail || e.message).split('\n')[0])),
});
setTimeout(() => {
  const d = dom.window.document;
  const guai = [];
  /* Un prodotto scritto a mano, come se l'avesse fatto qualcuno quando c'era
     la casella: si mette nella lista che la pagina sta usando (quella del
     telefono sul sito, quella condivisa sul link Claude). */
  dom.window.eval('lista.push(' + JSON.stringify(SUO) + '); disegna();');
  const prodotti = () => [...d.querySelectorAll('#tasti .tasto')]
    .filter(b => !b.classList.contains('agg')).map(b => b.textContent.trim());

  if (!prodotti().length) guai.push('la pagina è muta: nessun bottone dei prodotti');
  const r = d.getElementById('risultato');
  for (const [che, sel] of [['l\'intestazione col nome', '.capo'], ['la «i»', '.info'],
                            ['«Elimina prodotto»', '.elimina'], ['«Cambia nome»', '.gestisci'],
                            ['i sinonimi', '.sinonimi'], ['il conteggio', '.quanti']])
    if (r.querySelector(sel)) guai.push('sopra le offerte c\'è ancora ' + che);
  if (/Offerte ordinate/.test(r.textContent)) guai.push('c\'è ancora «Offerte ordinate dal prezzo…»');
  if (d.getElementById('form-agg') || d.getElementById('nuovo'))
    guai.push('nel catalogo c\'è ancora la casella per scrivere nomi nuovi');

  // il tasto in fondo alla griglia si chiama «Organizza i prodotti»
  const org = d.querySelector('.barra .tasto.agg');
  if (!org || org.textContent.trim() !== 'Organizza i prodotti')
    guai.push('l\'ultimo tasto della griglia dice «' + (org ? org.textContent.trim() : 'niente') + '»');
  org.click();
  const scaffale = () => [...d.querySelectorAll('#scaffali .tasto')];
  const trova = n => scaffale().find(b => b.textContent.trim() === n);

  // il prodotto scritto a mano sta in cima, acceso
  const primoReparto = d.querySelector('#scaffali .reparto');
  if (!primoReparto || !/fuori catalogo/.test(primoReparto.textContent))
    guai.push('i prodotti fuori catalogo non stanno in cima al catalogo');
  const suo = trova(SUO.nome);
  if (!suo || suo.getAttribute('aria-pressed') !== 'true')
    guai.push('«' + SUO.nome + '», scritto a mano, non si vede acceso nel catalogo');
  else {
    suo.click();
    if (prodotti().includes(SUO.nome)) guai.push('spegnendo «' + SUO.nome + '» resta nella lista');
    if (trova(SUO.nome)) guai.push('spento, «' + SUO.nome + '» resta nel catalogo (non si potrebbe riaccendere comunque)');
  }

  // un prodotto del catalogo si spegne e si riaccende
  const prima = prodotti().length;
  trova('Pollo').click();
  if (prodotti().includes('Pollo')) guai.push('spegnendo «Pollo» nel catalogo resta fra i prodotti');
  trova('Pollo').click();
  if (!prodotti().includes('Pollo')) guai.push('riaccendendo «Pollo» non torna');
  if (prodotti().length !== prima) guai.push('spegni e riaccendi: i prodotti erano ' + prima + ', sono ' + prodotti().length);
  console.log('  sopra le offerte: niente intestazione, niente «i», niente scritta');
  console.log('  «Organizza i prodotti»: si spegne e si riaccende; lo scritto a mano si toglie dal catalogo');

  if (errori.length) guai.push('errori in pagina: ' + errori.join(' | '));
  if (guai.length) { console.log('\nNON VA:'); guai.forEach(g => console.log('  ✗ ' + g)); process.exit(1); }
  process.exit(0);
}, 2500);
