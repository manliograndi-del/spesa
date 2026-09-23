/* LE OFFERTE DI UN VOLANTINO SOLO. Fino al 2026-09-23 sera ci si arrivava
   dall'elenco dei volantini in fondo alla pagina, coi due tasti «Le offerte»
   e «Il volantino» chiesti da Manlio il 2026-09-18. Quel giorno Manlio ha
   fatto togliere l'elenco («questo immenso elenco c'è in praticamente tutte
   le pagine, io lo toglierei dappertutto»); il pannello resta, raggiungibile
   dall'indirizzo con «#volantino=» in coda, per chi aveva quella scheda aperta.

   Qui si controlla:
   - l'elenco in fondo non torna;
   - l'indirizzo apre SOLO le offerte di quel volantino: se mostrasse anche le
     altre, uno andrebbe al Lidl a cercare un prezzo del Bennet;
   - le offerte escono dalla meno cara in giu, divise per reparto, e SENZA
     bollino verde: li dentro «il meno caro» vorrebbe dire «di questo
     negozio» e si leggerebbe «di tutti» (stessa regola della ricerca);
   - il pannello NON sta dentro la barra appiccicata (la lezione del cassetto:
     dentro, il telefono si pianta a ogni scorrimento);
   - chiuso il pannello, la ricerca torna a cercare fra TUTTE le offerte.   */
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const file = process.argv[2] || 'out/sito.html';
const testo = fs.readFileSync(file, 'utf8');
const SITO = 'https://manliograndi-del.github.io/spesa/';
const male = [];

function apri(indirizzo, quando) {
  /* window.open in jsdom non esiste: la pagina se ne accorge e ripiega sul
     pannello qui, che e proprio quello che deve fare quando la scheda nuova
     non si apre. Gli «errori» di jsdom su window.open non sono errori della
     pagina, quindi si tengono da parte a parte. */
  const errori = [];
  const vc = new VirtualConsole().on('jsdomError', e => {
    const m = String(e.detail || e.message).split('\n')[0];
    if (!/window\.open|Not implemented/i.test(m)) errori.push(m);
  });
  const dom = new JSDOM(testo, {
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc, url: indirizzo,
  });
  setTimeout(() => quando(dom.window, dom.window.document, errori), 1200);
}

apri(SITO, (w, d, errori) => {
  if (errori.length) male.push('errori nella pagina: ' + errori.join(' / '));
  if (d.querySelector('#vol, .vol-tasti, .spiega'))
    male.push('in fondo c\'è ancora l\'elenco dei volantini');

  // un volantino che oggi ha offerte valide
  const pdf = w.eval('(DATI.volantini.find(v => DATI.offerte.some(o => o.pdf === v.pdf && !nascosta(o))) || {}).pdf');
  if (!pdf) { console.error('nessun volantino con offerte valide oggi: la prova non prova niente'); process.exit(1); }
  const attese = w.eval('DATI.offerte.filter(o => o.pdf === ' + JSON.stringify(pdf)
                        + ' && !nascosta(o)).length');
  const insegna = w.eval('DATI.volantini.find(v => v.pdf === ' + JSON.stringify(pdf) + ').ins');

  apri(SITO + '#volantino=' + encodeURIComponent(pdf), (w2, d2, errori2) => {
    if (errori2.length) male.push('errori aprendo l\'indirizzo: ' + errori2.join(' / '));
    const pannello = d2.getElementById('ricerca');
    if (!pannello || pannello.hidden) male.push('l\'indirizzo non apre le offerte del volantino');
    if (d2.querySelector('.barra').contains(pannello))
      male.push('IL PANNELLO STA DENTRO LA BARRA: si ripianta come il cassetto');
    if (!d2.getElementById('risultato').hidden)
      male.push('l\'elenco di prima resta li sotto a confondere');

    const mostrate = [...d2.querySelectorAll('#trovati .prezzo-riga')];
    if (!mostrate.length) male.push('il pannello si apre vuoto');
    if (mostrate.length !== Math.min(attese, 40))
      male.push('mostra ' + mostrate.length + ' righe invece di ' + Math.min(attese, 40));
    const estranee = mostrate.filter(r => r.querySelector('.marchio').textContent.trim() !== insegna);
    if (estranee.length)
      male.push('fra le offerte di ' + insegna + ' ce ne sono ' + estranee.length + ' di altri negozi');

    /* In ordine di prezzo DENTRO OGNI REPARTO, come nella ricerca: il prezzo
       per unita del detersivo (a lavaggio) e quello della carne (al chilo) non
       si confrontano fra loro, e le offerte escono raggruppate per categoria. */
    let fuoriOrdine = 0, ultimo = null, dentro = null;
    [...d2.querySelectorAll('#trovati > *')].forEach(el => {
      if (el.classList.contains('fascia')) { dentro = el.textContent; ultimo = null; return; }
      if (!el.classList.contains('prezzo-riga')) return;
      const v = parseFloat(el.querySelector('.val .n').textContent.replace(',', '.'));
      if (ultimo !== null && v < ultimo) fuoriOrdine++;
      ultimo = v;
    });
    if (fuoriOrdine) male.push(fuoriOrdine + ' offerte non sono in ordine di prezzo dentro il loro reparto');
    if (dentro === null) male.push('le offerte non sono divise per reparto');

    if (d2.querySelectorAll('#trovati .bollo.meno').length)
      male.push('C\'E UN BOLLINO VERDE fra le offerte di un volantino solo: direbbe una cosa falsa');
    if (!d2.getElementById('quanti-trovati').textContent.includes(insegna))
      male.push('il pannello non dice di quale volantino sono le offerte');

    /* Scrivendo nella casella si restringe DENTRO il volantino, non fuori. */
    const q = d2.getElementById('q');
    q.value = 'pasta';
    q.dispatchEvent(new w2.Event('input'));
    const strette = [...d2.querySelectorAll('#trovati .prezzo-riga')];
    if (strette.length > mostrate.length)
      male.push('scrivendo una parola le offerte aumentano invece di restringersi');
    if (strette.some(r => r.querySelector('.marchio').textContent.trim() !== insegna))
      male.push('cercando dentro il volantino escono offerte di altri negozi');

    /* Chiuso il pannello, la ricerca normale torna a cercare fra TUTTE le
       offerte, non dentro l'ultimo volantino guardato. */
    d2.getElementById('chiudi-ricerca').dispatchEvent(new w2.Event('click'));
    if (d2.getElementById('risultato').hidden) male.push('chiudendo, l\'elenco dei prodotti non torna');
    const cer = [...d2.querySelectorAll('.tasto')].find(b => b.textContent.includes('Cerca'));
    cer.dispatchEvent(new w2.Event('click'));
    q.value = 'mozzarella';
    q.dispatchEvent(new w2.Event('input'));
    const negozi = new Set([...d2.querySelectorAll('#trovati .prezzo-riga')]
      .map(r => r.querySelector('.marchio').textContent.trim()));
    if (negozi.size < 2)
      male.push('dopo aver guardato un volantino la ricerca resta chiusa dentro quello');

    if (male.length) { male.forEach(x => console.error('  ✗ ' + x)); process.exit(1); }
    console.log('  l\'elenco dei volantini in fondo non c\'è');
    console.log('  «' + insegna + '»: ' + attese + ' offerte sue, mostrate ' + mostrate.length
                + ', tutte di quel volantino, senza bollino verde');
    process.exit(0);
  });
});
