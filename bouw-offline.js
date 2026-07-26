// Bouwt een enkel HTML-bestand uit index.html + content.json.
// Voor lokaal bekijken zonder webserver. De site zelf draait op index.html + content.json.
const fs=require('fs');
const shell=fs.readFileSync('index.html','utf8');
const data=fs.readFileSync('content.json','utf8');
const inline=`
let SITE={}, ORGANS={}, DISEASES={}, TECHS={}, INDEX=[], CARDS={}, POS={}, TECHPAGES=[];
let editorialNL='', editorialEN='';
const __INGEBAKKEN__ = ${data};
async function laadInhoud(){
  const d = __INGEBAKKEN__;
  SITE=d.site; ORGANS=d.organs; DISEASES=d.diseases; TECHS=d.techs;
  INDEX=d.index; CARDS=d.cards; POS=d.pos; TECHPAGES=d.techpages;
  editorialNL=d.editorial.nl; editorialEN=d.editorial.en;
  for(const id of Object.keys(CARDS)){ CARDS[id].nl.editorial=editorialNL; CARDS[id].en.editorial=editorialEN; }
  current = INDEX[0].id;
  document.getElementById('bijgewerkt').textContent = d.bijgewerkt;
}
function toonLaadfout(e){ console.error(e); }
`;
const a=shell.indexOf('// ============ INHOUD ============');
const b=shell.indexOf('// ============ SITE CHROME');
if(a<0||b<0){ console.error('markers niet gevonden'); process.exit(1); }
const out=shell.slice(0,a)+inline+shell.slice(b);
fs.writeFileSync('interventieoncologie-offline.html',out);
console.log('interventieoncologie-offline.html geschreven:',(out.length/1024).toFixed(0),'kB');
