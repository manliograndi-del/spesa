/* IL CONTEGGIO DELLE VISITE (Umami, 2026-09-24). Qui si controlla che:
   - sul SITO ci sia lo script di Umami, UNO solo, nella testa della pagina,
     con l'id del sito di Manlio e limitato al suo indirizzo (data-domains),
     così le prove e le copie aperte dal disco non contano visite finte;
   - che parta dopo la pagina (defer) e non la rallenti;
   - che sul link Claude e nella copia da aprire a doppio clic NON ci sia:
     lì gli script di altri siti non passano o non c'è niente da contare.  */
const fs = require('fs');
const file = process.argv[2] || 'out/sito.html';
const html = fs.readFileSync(file, 'utf8');
const tag = html.match(/<script[^>]*cloud\.umami\.is[^>]*>/g) || [];
const male = [];
if (/sito\.html$/.test(file)) {
  if (tag.length !== 1) male.push('sul sito gli script di Umami sono ' + tag.length + ', non uno');
  else {
    const t = tag[0];
    if (!/data-website-id="47de14e6-6f92-4ce2-891f-6e37b37062aa"/.test(t)) male.push('manca l\'id del sito di Manlio');
    if (!/data-domains="manliograndi-del\.github\.io"/.test(t)) male.push('lo script conterebbe anche le prove e le copie dal disco (manca data-domains)');
    if (!/\sdefer[\s>]/.test(t)) male.push('lo script non è «defer»: rallenterebbe l\'apertura');
    const testa = html.indexOf('</head>');
    if (testa < 0 || html.indexOf(t) > testa) male.push('lo script non sta nella testa della pagina');
  }
} else if (tag.length) male.push('lo script di Umami c\'è anche in ' + file.split('/').pop() + ': deve stare solo sul sito');
if (male.length) { male.forEach(m => console.error('  ✗ ' + m)); process.exit(1); }
console.log('  conteggio visite: ' + (tag.length ? 'Umami sul sito, solo sul suo indirizzo' : 'niente, com\'è giusto qui'));
