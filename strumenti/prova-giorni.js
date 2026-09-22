/* IL CERCHIETTO DEI GIORNI CHE MANCANO, chiesto da Manlio il 2026-09-22 con
   in mano le schermate dei riquadri Material: «quella dove c'è scritto 6.80,
   potresti utilizzarla messa in ogni offerta, magari piccola, per indicare
   quanti giorni mancano».

   Qui si controlla quello che, sbagliando, manderebbe uno in negozio a vuoto
   o gli farebbe saltare un'offerta buona:
   - il numero conta OGGI COMPRESO: l'ultimo giorno dice «1 oggi», mai «0»;
   - il conto torna con la data scritta nella riga, riga per riga;
   - le offerte che devono ancora cominciare NON hanno il cerchietto: lì il
     numero direbbe una cosa (quanto manca alla fine) mentre la riga ne dice
     un'altra (quando comincia);
   - negli ultimi tre giorni diventa ambra, che in questa pagina è il colore
     di «attenzione alla data»;
   - il cerchietto c'è anche nel riquadro del meno caro e dice lo stesso
     numero della sua riga nell'elenco.                                    */
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

const GIORNO = 86400000;
const MESI = ('gennaio febbraio marzo aprile maggio giugno luglio agosto '
  + 'settembre ottobre novembre dicembre').split(' ');

setTimeout(() => {
  const w = dom.window, d = w.document;
  if (errori.length) male.push('errori nella pagina: ' + errori.join(' / '));
  try { w.eval('chiudiNovita()'); } catch (e) {}

  const oggi = w.eval('OGGI_ISO');
  const alGiorno = iso => Date.parse(iso + 'T00:00:00Z');

  /* La data scritta nella riga («fino al 5 ottobre») ridiventa una data. */
  function finoDa(testo) {
    const m = testo.match(/fino al (\d+) (\w+)/);
    if (!m) return null;
    const mese = MESI.indexOf(m[2]) + 1;
    if (!mese) return null;
    const anno = Number(oggi.slice(0, 4)) + (mese < Number(oggi.slice(5, 7)) ? 1 : 0);
    return anno + '-' + String(mese).padStart(2, '0') + '-' + String(Number(m[1])).padStart(2, '0');
  }

  let conCerchio = 0, senza = 0, ambra = 0, ultimi = 0, inizi = 0;
  const tasti = [...d.querySelectorAll('#tasti .tasto:not(.agg)')];
  if (!tasti.length) { console.error('NESSUN prodotto in lista'); process.exit(1); }

  tasti.forEach(t => {
    t.dispatchEvent(new w.Event('click'));
    [...d.querySelectorAll('#risultato .prezzo-riga')].forEach(r => {
      const testo = r.querySelector('.sotto').textContent;
      const cer = r.querySelector('.giorni');
      const futura = /vale dal|vale dall/.test(testo);
      if (futura) {
        if (cer) male.push('un\'offerta non ancora cominciata ha il cerchietto dei giorni: ' + testo.slice(0, 60));
        /* Al suo posto ha il tondino di quando comincia: giorno dentro,
           mese sotto. Chiesto da Manlio il 2026-09-22. */
        const parte = r.querySelector('.parte');
        const m = testo.match(/vale dall?[' ](\d+) (\w+)/);
        if (!parte) {
          male.push('un\'offerta non ancora cominciata non dice quando comincia: ' + testo.slice(0, 60));
        } else if (m) {
          const g = parte.querySelector('.num').textContent;
          const mese = parte.querySelector('.mese').textContent;
          if (Number(g) !== Number(m[1]))
            male.push('il tondino dice il giorno ' + g + ' ma la riga dice il ' + m[1]);
          if (m[2].slice(0, 3).toLowerCase() !== mese.toLowerCase())
            male.push('il tondino dice «' + mese + '» ma la riga dice «' + m[2] + '»');
          inizi++;
        }
        /* E il prezzo è grigio, non rosso: «si nota poco che non sono ancora
           attivi». Qui si controlla che la riga porti la classe giusta. */
        if (!r.classList.contains('dopo'))
          male.push('un\'offerta non ancora cominciata non è segnata come tale');
        senza++;
        return;
      }
      if (r.querySelector('.parte'))
        male.push('un\'offerta già valida ha il tondino di quando comincia: ' + testo.slice(0, 60));
      if (!cer) { senza++; return; }
      conCerchio++;
      const n = Number(cer.querySelector('.num').textContent);
      if (!(n >= 1)) male.push('il cerchietto dice «' + cer.querySelector('.num').textContent + '»: deve contare anche oggi');
      const fino = finoDa(testo);
      if (fino) {
        const atteso = Math.round((alGiorno(fino) - alGiorno(oggi)) / GIORNO) + 1;
        if (n !== atteso)
          male.push('il cerchietto dice ' + n + ' ma la riga dice ' + testo.match(/fino al [^·]*/)[0].trim()
                    + ' (attesi ' + atteso + ')');
      }
      const poco = cer.classList.contains('poco');
      if (n <= 3) { ultimi++; if (!poco) male.push('mancano ' + n + ' giorni e il cerchietto non è ambra'); }
      else if (poco) male.push('mancano ' + n + ' giorni e il cerchietto è già ambra');
      if (poco) ambra++;
      const parola = cer.querySelector('.gg').textContent;
      if (n === 1 && parola !== 'oggi') male.push('l\'ultimo giorno non dice «oggi» ma «' + parola + '»');
      if (n > 1 && parola !== 'giorni') male.push('dice «' + parola + '» invece di «giorni»');
      if (!/\d/.test(cer.title)) male.push('il cerchietto non si spiega al tocco lungo');
    });

    /* La pastiglia del meno caro ha il suo cerchietto come tutte le altre. */
    const vince = d.querySelector('#risultato .prezzo-riga.vince');
    if (vince && !vince.querySelector('.giorni'))
      male.push(t.textContent + ': la pastiglia del meno caro non dice quanti giorni restano');
  });

  if (!conCerchio) male.push('nessuna offerta ha il cerchietto dei giorni');

  if (male.length) { male.forEach(m => console.error('  ✗ ' + m)); process.exit(1); }
  console.log('  cerchietto dei giorni: su ' + conCerchio + ' offerte (' + senza
              + ' senza, perché devono ancora cominciare o non hanno una fine)');
  console.log('  il conto torna con le date scritte; ' + ultimi + ' negli ultimi tre giorni, in ambra');
  console.log('  ' + inizi + ' offerte non ancora cominciate, col tondino del giorno in cui partono');
}, 700);
