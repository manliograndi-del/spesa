/* LA PASTIGLIA DEL MENO CARO, chiesta da Manlio il 2026-09-22: «descrivici
   solo il meno caro, in un riquadrino colorato» e poi, più preciso: «che il
   prodotto meno caro venisse messo in una pillola, con un bordo e con un
   colore che la evidenzi, magari lo stesso colore del fondo ma un po' più
   forte». E insieme: «che le offerte che non sono ancora cominciate
   apparissero sbiadite».

   Quello che si controlla qui è quello che, rompendosi, non si vede
   rileggendo il codice:
   - la pastiglia c'è ed è UNA SOLA: due «meno caro» nella stessa lista
     sarebbero due risposte alla stessa domanda;
   - è l'offerta che vale OGGI, non la prima riga: se fosse una che comincia
     fra una settimana manderebbe uno in negozio a chiedere un prezzo che non
     gli fanno ancora;
   - la pastiglia non è mai una riga sbiadita, e le sbiadite sono tutte e
     sole quelle che devono ancora cominciare;
   - NON c'è né nei risultati di «Cerca fra i prezzi» né nelle offerte di un
     singolo volantino, per la stessa ragione per cui lì non c'è il bollino
     verde: lì «il meno caro» vorrebbe dire «di quello che hai cercato» e si
     leggerebbe «di tutti». Una novità falsa manda uno in negozio.          */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const file = process.argv[2] || 'out/sito.html';
const male = [];
const errori = [];
const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
  runScripts: 'dangerously', pretendToBeVisual: true,
  url: 'https://manliograndi-del.github.io/spesa/',
  virtualConsole: new VirtualConsole().on('jsdomError',
    e => errori.push(String(e.detail || e.message).split('\n')[0])),
});

setTimeout(() => {
  const w = dom.window, d = w.document;
  if (errori.length) male.push('errori nella pagina: ' + errori.join(' / '));
  try { w.eval('chiudiNovita()'); } catch (e) {}

  const tasti = [...d.querySelectorAll('#tasti .tasto:not(.agg)')];
  if (!tasti.length) { console.error('NESSUN prodotto in lista'); process.exit(1); }

  let conPastiglia = 0, sbiadite = 0;
  tasti.forEach(t => {
    t.dispatchEvent(new w.Event('click'));
    const out = d.getElementById('risultato');
    const righe = [...out.querySelectorAll('.prezzo-riga')];
    const vince = righe.filter(r => r.classList.contains('vince'));
    const bollini = [...out.querySelectorAll('.prezzo-riga .bollo.meno')];

    if (vince.length > 1) male.push(t.textContent + ': ' + vince.length + ' pastiglie invece di una');
    if (vince.length !== bollini.length)
      male.push(t.textContent + ': pastiglie ' + vince.length + ', bollini verdi ' + bollini.length);

    /* Le sbiadite sono tutte e sole quelle che devono ancora cominciare. */
    righe.forEach(r => {
      const futura = /vale dal|vale dall/.test(r.querySelector('.sotto').textContent);
      const pallida = r.classList.contains('dopo');
      if (futura && !pallida) male.push(t.textContent + ': un\'offerta non ancora cominciata non è sbiadita');
      if (!futura && pallida) male.push(t.textContent + ': è sbiadita un\'offerta che vale già');
      if (pallida) sbiadite++;
    });

    if (!vince.length) return;
    conPastiglia++;
    const r = vince[0];
    if (r.classList.contains('dopo'))
      male.push(t.textContent + ': IL MENO CARO È UN\'OFFERTA CHE DEVE ANCORA COMINCIARE');
    if (!bollini.length || bollini[0].closest('.prezzo-riga') !== r)
      male.push(t.textContent + ': il bollino verde non sta sulla pastiglia');

    /* Dentro c'è tutto quello che serve per andarci. */
    const dentro = r.textContent;
    if (!/meno caro/i.test(dentro)) male.push(t.textContent + ': la pastiglia non dice cos\'è');
    if (!r.querySelector('.val .n').textContent.trim())
      male.push(t.textContent + ': senza prezzo per unità');
    if (!r.querySelector('.sotto b').textContent.trim())
      male.push(t.textContent + ': non dice in che negozio');
    if (!/la confezione/.test(dentro))
      male.push(t.textContent + ': non dice quanto costa la confezione');
    if (!r.querySelector('.quando'))
      male.push(t.textContent + ': non dice fino a quando vale');
    const link = r.querySelector('a.dove');
    if (link && link.target !== '_blank')
      male.push(t.textContent + ': il collegamento non apre una scheda nuova');
  });

  if (!conPastiglia) male.push('nessun prodotto ha la pastiglia del meno caro');
  if (!sbiadite) male.push('nessuna offerta sbiadita: o non ce ne sono da venire, o la classe non arriva');

  /* NEI RISULTATI DELLA RICERCA NO. */
  w.eval('apriRicerca(true)');
  const q = d.getElementById('q');
  q.value = 'tonno';
  q.dispatchEvent(new w.Event('input'));
  const trovati = d.getElementById('trovati');
  if (trovati.querySelector('.prezzo-riga.vince'))
    male.push('LA PASTIGLIA COMPARE NELLA RICERCA: lì «il meno caro» vorrebbe dire un\'altra cosa');
  if (trovati.querySelector('.bollo.meno'))
    male.push('il bollino verde compare nella ricerca');

  /* NELLE OFFERTE DI UN SINGOLO VOLANTINO NEMMENO. */
  const pdf = w.eval('DATI.volantini.filter(v => DATI.offerte.some(o => o.pdf === v.pdf))[0].pdf');
  w.eval('apriVolantino(' + JSON.stringify(pdf) + ')');
  if (trovati.querySelector('.prezzo-riga.vince'))
    male.push('LA PASTIGLIA COMPARE NELLE OFFERTE DI UN VOLANTINO: lì vorrebbe dire '
              + '«il meno caro di questo negozio» e si leggerebbe «di tutti»');

  if (male.length) { male.forEach(m => console.error('  ✗ ' + m)); process.exit(1); }
  console.log('  pastiglia del meno caro: ' + conPastiglia + ' prodotti su ' + tasti.length
              + ', sempre l\'offerta che vale oggi');
  console.log('  ' + sbiadite + ' offerte sbiadite, tutte e sole quelle che devono ancora cominciare');
}, 700);
