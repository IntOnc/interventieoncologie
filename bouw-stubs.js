// Bouwt een vindbare pagina per kaart en per techniekpagina, plus sitemap.xml.
// Elke stub bevat echte inhoud voor zoekmachines en linkvoorbeelden, en stuurt
// een bezoeker met JavaScript door naar de interactieve versie.
// Gebruik: node bouw-stubs.js   (na elke wijziging van content.json)

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const BASIS = 'https://www.interventieoncologie.nl/';
const d = JSON.parse(fs.readFileSync('content.json', 'utf8'));

function kaal(html) {
  return String(html || '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
}
function esc(t) {
  return String(t || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function schrijf(relpad, inhoud) {
  const vol = path.join('.', relpad);
  fs.mkdirSync(path.dirname(vol), { recursive: true });
  fs.writeFileSync(vol, inhoud);
}

function pagina({ pad, hash, titel, oms, kop, sub, lead, blokken, taalAlt }) {
  const url = BASIS + pad;
  const app = BASIS + hash;
  return `<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(titel)}</title>
<meta name="description" content="${esc(oms)}">
<link rel="canonical" href="${esc(url)}">
${taalAlt ? `<link rel="alternate" hreflang="en" href="${esc(taalAlt)}">` : ''}
<meta property="og:site_name" content="Interventie Oncologie">
<meta property="og:type" content="article">
<meta property="og:title" content="${esc(titel)}">
<meta property="og:description" content="${esc(oms)}">
<meta property="og:url" content="${esc(url)}">
<meta name="twitter:card" content="summary">
<script>location.replace(${JSON.stringify(app)});</script>
<style>
  body{font:16px/1.6 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
       color:#0f1e2e;background:#f6f8fa;margin:0;padding:28px 18px}
  main{max-width:760px;margin:0 auto;background:#fff;border:1px solid #e3e9ef;border-radius:14px;padding:22px 24px}
  h1{font-size:22px;line-height:1.25;margin:0 0 6px}
  .sub{color:#5a6b7b;margin:0 0 16px}
  h2{font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:#5a6b7b;margin:20px 0 6px}
  ul{padding-left:18px} li{margin-bottom:5px}
  a{color:#0b5563} .knop{display:inline-block;margin-top:18px;background:#0b5563;color:#fff;
       text-decoration:none;border-radius:9px;padding:9px 16px;font-weight:700}
  .voet{max-width:760px;margin:14px auto 0;color:#5a6b7b;font-size:12px}
</style>
</head>
<body>
<main>
  <h1>${esc(kop)}</h1>
  <p class="sub">${esc(sub)}</p>
  <p>${esc(lead)}</p>
  ${blokken}
  <a class="knop" href="${esc(app)}">Open de interactieve kaart</a>
</main>
<p class="voet">Interventie Oncologie. Deze pagina is een samenvatting; de volledige kaart met literatuur, richtlijnen en lopende studies staat in de interactieve versie.</p>
</body>
</html>
`;
}

let paden = [];

// Kaarten
d.index.forEach(rij => {
  const c = d.cards[rij.id];
  const nl = c.nl;
  const lit = ['guides', 'core', 'latest']
    .flatMap(k => (nl[k] || []).map(p => ({ t: p[0], u: p[2], sk: Number(p[4]) || 0, j: p[1] })))
    .sort((a, b) => b.sk - a.sk).slice(0, 8);
  const blokken =
    `<h2>Wanneer geschikt</h2><ul>${(nl.crit || []).slice(0, 6).map(x => `<li>${esc(kaal(x))}</li>`).join('')}</ul>` +
    `<h2>Belangrijkste literatuur</h2><ul>${lit.map(x =>
      `<li><a href="${esc(x.u)}" rel="noopener">${esc(x.t)}</a> <span style="color:#5a6b7b">${esc(x.j)}</span></li>`).join('')}</ul>`;
  const pad = 'kaart/' + rij.id + '/';
  schrijf(pad + 'index.html', pagina({
    pad, hash: '#/nl/kaart/' + rij.id,
    titel: nl.title + ' · Interventie Oncologie',
    oms: kaal(nl.bl).slice(0, 300),
    kop: nl.title, sub: kaal(rij.sub && rij.sub.nl ? rij.sub.nl : ''),
    lead: kaal(nl.bl), blokken,
    taalAlt: BASIS + '#/en/kaart/' + rij.id
  }));
  paden.push(pad);
});

// Techniekpagina's
(d.techpages || []).forEach(tp => {
  const nl = tp.nl;
  const blokken = `<h2>Wat het doet</h2><ul>${(nl.works || []).slice(0, 6).map(x => `<li>${esc(kaal(x))}</li>`).join('')}</ul>`;
  const pad = 'techniek/' + tp.id + '/';
  schrijf(pad + 'index.html', pagina({
    pad, hash: '#/nl/techniek/' + tp.id,
    titel: nl.title + ' · Interventie Oncologie',
    oms: kaal(nl.lead).slice(0, 300),
    kop: nl.title, sub: kaal(nl.lead),
    lead: kaal(nl.intro || ''), blokken,
    taalAlt: BASIS + '#/en/techniek/' + tp.id
  }));
  paden.push(pad);
});

// Sitemap en robots
const vandaag = d.bijgewerkt || '';
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${[''].concat(paden).map(p => `  <url><loc>${BASIS}${p}</loc><lastmod>${vandaag}</lastmod></url>`).join('\n')}
</urlset>
`;
fs.writeFileSync('sitemap.xml', sitemap);
fs.writeFileSync('robots.txt', `User-agent: *\nAllow: /\nSitemap: ${BASIS}sitemap.xml\n`);

// Wijzigingenlijst: per commit vergelijken wat er inhoudelijk veranderde
function lees(sha) {
  try { return JSON.parse(execSync(`git show ${sha}:content.json`, { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 })); }
  catch (e) { return null; }
}
function sleutelVan(it) { return (it[2] || '') + '|' + (it[0] || ''); }
function tekstVan(kaart, pos) {
  return JSON.stringify([kaart.bl, kaart.crit, kaart.results, kaart.lim, kaart.alts, pos || null]);
}
// Een veldwaarde (string, lijst of pos-object) omzetten naar leesbare platte tekst voor de voor/na-vergelijking.
function platveld(v) {
  if (v == null) return '';
  let s;
  if (Array.isArray(v)) s = v.map(x => (typeof x === 'string' ? x : '')).join(' • ');
  else if (typeof v === 'object') s = ['g', 'l', 'v'].map(k => v[k] || '').filter(Boolean).join(' • ');
  else s = String(v);
  s = s.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
  return s.length > 1600 ? s.slice(0, 1600) + '…' : s;
}
try {
  const log = execSync('git log --date=short --pretty=format:%H%x09%ad%x09%s -- content.json', { encoding: 'utf8' })
    .split('\n').filter(Boolean).map(r => { const [sha, datum, ...rest] = r.split('\t'); return { sha, datum, subject: rest.join(' ').trim() }; });
  log.reverse();                       // oudste eerst
  const regels = [];
  let vorige = null;
  for (const c of log) {
    const nu = lees(c.sha);
    if (!nu) continue;
    if (vorige) {
      const _start = regels.length;    // regels die in deze commit ontstaan, krijgen straks de commit-boodschap als aanleiding
      const kort = id => {
        const rij = (d.index || []).find(x => x.id === id);
        return rij && rij.kort ? rij.kort.nl : ((d.cards[id] && d.cards[id].nl.title) || id);
      };
      for (const id of Object.keys(nu.cards)) {
        if (!vorige.cards[id]) { regels.push({ datum: c.datum, kaart: id, kort: kort(id), type: 'nieuw', wat: nu.cards[id].nl.title }); continue; }
        const nieuweHier = [];       // publicaties die in deze commit aan deze kaart zijn toegevoegd
        for (const lijst of ['guides', 'core', 'latest', 'ongoing']) {
          const oud = new Map((vorige.cards[id].nl[lijst] || []).map(x => [sleutelVan(x), x]));
          const nieuwe = new Map((nu.cards[id].nl[lijst] || []).map(x => [sleutelVan(x), x]));
          for (const [k, x] of nieuwe) if (!oud.has(k)) {
            regels.push({ datum: c.datum, kaart: id, kort: kort(id), type: lijst === 'guides' ? 'richtlijn' : 'toegevoegd', lijst, wat: x[0], bron: x[2] });
            if (lijst === 'core' || lijst === 'latest') nieuweHier.push({ wat: x[0], bron: x[2] });
          }
          for (const [k, x] of oud) if (!nieuwe.has(k))
            regels.push({ datum: c.datum, kaart: id, kort: kort(id), type: 'verwijderd', lijst, wat: x[0] });
        }
        // welke tekstvelden zijn veranderd
        const ov = vorige.cards[id].nl, nv = nu.cards[id].nl;
        const ev = vorige.cards[id].en || {}, env = nu.cards[id].en || {};
        const oPos = (vorige.pos || {})[id] && vorige.pos[id].nl, nPos = (nu.pos || {})[id] && nu.pos[id].nl;
        const oPosE = (vorige.pos || {})[id] && vorige.pos[id].en, nPosE = (nu.pos || {})[id] && nu.pos[id].en;
        const gelijk = (x, y) => JSON.stringify(x || null) === JSON.stringify(y || null);
        const velden = [];
        for (const f of ['bl', 'crit', 'results', 'lim', 'alts']) if (!gelijk(ov[f], nv[f])) velden.push(f);
        if (!gelijk(oPos, nPos)) velden.push('pos');
        const a = tekstVan(ov, oPos);
        const b = tekstVan(nv, nPos);
        if (a !== b) {
          const diff = velden.map(f => {
            const ovl = f === 'pos' ? oPos : ov[f], nvl = f === 'pos' ? nPos : nv[f];
            const evl = f === 'pos' ? oPosE : ev[f], envl = f === 'pos' ? nPosE : env[f];
            return { veld: f, oud: { nl: platveld(ovl), en: platveld(evl) }, nieuw: { nl: platveld(nvl), en: platveld(envl) } };
          }).filter(dd => dd.oud.nl !== dd.nieuw.nl || dd.oud.en !== dd.nieuw.en);
          regels.push({ datum: c.datum, kaart: id, kort: kort(id), type: 'tekst', wat: nu.cards[id].nl.title, velden, naaraanleiding: nieuweHier.slice(0, 4), diff });
        }
      }
      for (let k = _start; k < regels.length; k++) if (c.subject) regels[k].reden = c.subject;
    }
    vorige = nu;
  }
  // een verwijderde en toegevoegde regel met dezelfde titel op dezelfde dag is een correctie
  const perDag = {};
  regels.forEach(r => { const k = r.datum + '|' + r.kaart + '|' + r.wat; (perDag[k] = perDag[k] || []).push(r); });
  const samen = [];
  const gedaan = new Set();
  for (const r of regels) {
    const k = r.datum + '|' + r.kaart + '|' + r.wat;
    if (gedaan.has(k)) continue;
    const groep = perDag[k];
    if (groep.length > 1 && groep.some(x => x.type === 'toegevoegd') && groep.some(x => x.type === 'verwijderd')) {
      samen.push(Object.assign({}, groep.find(x => x.type === 'toegevoegd'), { type: 'bijgewerkt' }));
      gedaan.add(k);
    } else { samen.push(r); }
  }
  regels.length = 0; regels.push(...samen);
  regels.reverse();                    // nieuwste eerst
  fs.writeFileSync('wijzigingen.json', JSON.stringify({ bijgewerkt: vandaag, regels: regels.slice(0, 500) }, null, 1));
  console.log('wijzigingen.json:', regels.length, 'inhoudelijke wijzigingen');
} catch (e) {
  console.log('wijzigingen.json overgeslagen:', e.message);
}

// Controle: kernpublicaties met een uitkomst-ontwerp horen een aantal patienten te hebben
const UITKOMST = ['meta_rct', 'rct3', 'rct', 'meta', 'prosp', 'retro'];
const zonderN = [];
for (const rij of d.index) {
  const c = d.cards[rij.id];
  for (const lijst of ['core', 'latest']) {
    (c.nl[lijst] || []).forEach((it, i) => {
      const m = it[6];
      if (m && UITKOMST.includes(m.d) && !m.n) zonderN.push(`${rij.id} ${lijst}[${i}] :: ${(it[0] || '').slice(0, 60)}`);
    });
  }
}
if (zonderN.length) {
  console.log('\nLET OP, ' + zonderN.length + ' kernpublicatie(s) met een uitkomst-ontwerp maar zonder aantal patienten:');
  zonderN.forEach(x => console.log('  - ' + x));
  console.log('Vul het veld n in het zevende element aan, of zet het ontwerp op review/serie als dat klopt.\n');
}

console.log('stubs geschreven:', paden.length, '| sitemap:', paden.length + 1, 'adressen');
