# Publiceren (autonoom)

Dit is de werkwijze voor een onderhoudsronde die autonoom draait: zij beslist zelf
welke geverifieerde voorstellen erin gaan, publiceert zelf en stuurt achteraf een
korte samenvatting. Kenneth hoeft niets goed te keuren en uploadt niets. Neem elk
voorstel op waarvan je de cijfers uit het abstract hebt geverifieerd en dat
relevant en niet-dubbel is; laat weg wat je niet kon verifiëren en meld dat in de
samenvatting.

## Wat je nodig hebt

Het publicatietoken staat in de opdracht van de geplande taak. Het geeft alleen
schrijfrechten op dit ene repo. Zet het nooit in een bestand dat je commit, en
herhaal het niet in je antwoord of in het overzicht.

## Belangrijk over de omgeving

`api.github.com` is in deze omgeving afgeschermd en antwoordt met een foutmelding
over `add_repo`. Git over https werkt wel. Gebruik dus git, nooit de GitHub API.
Ook `curl` naar willekeurige hosts is meestal geblokkeerd; gebruik WebFetch om te
controleren of een wijziging live staat.

## Abstract verifiëren, met terugval

Cijfers komen alleen op de kaart als je ze zelf op een opgehaalde pagina hebt
gelezen. De volgorde is: bij een bekend PMID het abstract met letterlijke getallen
via PubTator3, en de exacte citatie via Crossref (`works/DOI`). Springer-bladen
(CVIR, CVIR Oncology) leveren via Crossref vaak een abstract mee, Elsevier-bladen
(JVIR, JCO, J Hepatol, Eur Urol, Lancet-titels) meestal niet.

Geeft Crossref geen abstract terug bij een DOI van een doorgaans toegankelijke
uitgever (`link.springer.com`, `mdpi.com`, `nature.com`, `frontiersin.org`,
`karger.com`, `academic.oup.com`, `pubs.rsna.org`, `dirjournal.org`), haal dan
eerst de artikelpagina zelf op met WebFetch (bijvoorbeeld
`https://link.springer.com/article/DOI`) en lees het abstract daar, voordat je het
als niet te verifiëren markeert. Deze terugval ving de UroCCR-studie (n°177) in
CVIR op, die wel op de Springer-pagina stond maar niet in Crossref.

Voor Elsevier-bladen blijft de Crossref-plus-PubTator3-route nodig. Staat een
artikel nog niet in PubMed (geen PMID te vinden, vaak bij zeer recente nummers),
noteer het dan onder NIET GEVERIFIEERD met titel, DOI en kaart, zodat een volgende
ronde het oppakt zodra het geïndexeerd is. Deze regel staat ook in de prompt van
elke geplande onderhoudsronde (STAP 2, BRONREGELS).

## Stappen

1. Kloon het repo met het token in de URL, in een lege map buiten je werkmap.
2. Pas `content.json` aan met een script, nooit met de hand. Het bestand is ruim
   1 MB en is opgeslagen zonder witruimte, dus laden met `json.load`, wijzigen,
   en terugschrijven met `ensure_ascii=False` en `separators=(',',':')`.
3. Zet het veld `bijgewerkt` op de datum van vandaag.
4. Voer de controles hieronder uit. Faalt er een, push dan niet en meld het.
5. Commit met een beschrijvende Nederlandse boodschap en push naar `main`.
6. Wacht ongeveer een minuut en controleer met WebFetch dat
   `https://intonc.github.io/interventieoncologie/content.json` de wijziging bevat.
   Let op dat een groot bestand door WebFetch afgekapt kan worden; controleer dus
   op iets dat vooraan staat, bijvoorbeeld het veld `bijgewerkt`.
7. Draai `node bouw-stubs.js` in de kloon NA het committen van content.json, en
   commit de gewijzigde bestanden daarna mee. Dat werkt de vindbare pagina's per
   kaart, de sitemap en `wijzigingen.json` bij. Die wijzigingenlijst wordt uit de
   gitgeschiedenis afgeleid door content.json per commit te vergelijken, dus je
   hoeft er zelf niets in te schrijven en je mag hem nooit met de hand aanpassen.
8. Meld in een kort bericht wat er gepubliceerd is en wat er niet in ging.

## Bewijskracht bij nieuwe items

Elk nieuw item in `core` of `latest` krijgt een zevende element met de gegevens
voor de bewijskracht, afgeleid uit de samenvatting die je zelf hebt geschreven:

    {"d":"rct3","n":760,"mc":1,"cmp":1,"t":"A"}

`d` is de opzet: `meta_rct` (meta-analyse van gerandomiseerde trials), `rct3`
(gerandomiseerde fase III), `rct` (overige gerandomiseerde trials), `meta`
(systematische review of meta-analyse), `prosp` (prospectief cohort of
register), `retro` (retrospectief cohort), `serie` (patientenserie) of `review`
(overzichtsartikel). `n` is het aantal patienten dat in de samenvatting staat,
`mc` is 1 bij multicentrisch, `cmp` is 1 als er een vergelijkingsarm is, en `t`
is de tijdschriftklasse: A of B volgens de lijst onder `tijdschriften` in
`content.json`, anders C.

Weet je een veld niet, laat het dan weg. Is de opzet niet vast te stellen, zet
dan het hele zevende element op `null`; de site toont dan geen score in plaats
van een verzonnen score.

Het aantal patienten `n` is niet optioneel bij een uitkomst-ontwerp. Staat de
opzet op `meta_rct`, `rct3`, `rct`, `meta`, `prosp` of `retro`, dan hoort er een
`n` bij; die staat vrijwel altijd in het abstract dat je toch al ophaalt. Zonder
`n` wordt de studie te laag gescoord. `node bouw-stubs.js` meldt aan het eind
welke kernpublicaties een uitkomst-ontwerp hebben maar geen aantal; los die op
voordat je pusht.

## Tijdschriftnamen

Schrijf in het tijdschriftveld de naam voluit. De site kort hem zelf in op
plaatsen met weinig ruimte, aan de hand van de lijst `afkortingen` in
`content.json`. Staat een lang tijdschrift daar nog niet in, voeg het dan toe
met de gangbare afkorting, bijvoorbeeld "Journal of Vascular and Interventional
Radiology": "JVIR". Zet nooit de afkorting zelf in het tijdschriftveld.

## Controles voor het pushen

- `content.json` is geldige JSON.
- Elk literatuuritem is een rij van vijf of zes elementen:
  titel, "tijdschrift · jaar", url, samenvatting, sorteersleutel JJJJMM, en
  optioneel de eerste auteur als "Achternaam et al.". Vul dat zesde element
  alleen als je de auteur op het record hebt gelezen, anders laat je het weg.
- De lijsten `guides`, `core`, `latest` en `ongoing` zijn per kaart even lang in
  `nl` en in `en`, en de items staan in dezelfde volgorde.
- Er staat nergens een em-dash of en-dash in nieuwe tekst.
- Elke nieuwe samenvatting bevat in het Resultaten-deel ten minste een getal,
  tenzij het om een richtlijnstandpunt of een lopende studie gaat.
- De sorteersleutel is een geheel getal van zes cijfers.
- Geen dubbelen binnen een kaart. Vergelijk voor het toevoegen niet alleen de
  titel maar ook de link, en normaliseer daarbij: haal https, www en dx weg, en
  behandel doi.org/10.x en link.springer.com/article/10.x als dezelfde bron.
  Een publicatie hoort in core of in latest, nooit in allebei.
- Draai `python3 pipeline/controle.py`. Dat controleert de terminologie en de
  kale statements (zie hieronder). Faalt de controle, los de meldingen dan op
  of bevestig dat ze terecht zijn voordat je pusht.

## Terminologie en kale statements

`pipeline/controle.py` bewaakt twee dingen en wordt vóór het pushen gedraaid.

Terminologie: elke afkorting hoort bij de juiste term. RFA is uitsluitend
radiofrequente ablatie, MWA is microwave- of microgolfablatie, TARE en SIRT zijn
radio-embolisatie (nooit chemo-embolisatie), cTACE is conventionele TACE en
DEB-TACE is de variant met drug-eluting beads. De controle meldt het als een
afkorting tussen haakjes aan de verkeerde term wordt gekoppeld, bijvoorbeeld
"microgolfablatie (RFA)" of "TARE (chemo-embolisatie)". Een gewone opsomming als
"thermale ablatie (RFA of microwave)" is geen fout en wordt niet gemeld. Nieuw
in te voegen tekst en samenvattingen moeten deze afkortingen dus consequent en
correct gebruiken.

Kale statements: een statement op de kaart hoort op een bron te steunen. De
controle meldt een kaart waarvan de resultaten cijfers noemen terwijl er geen
kern- of recente publicatie onder staat, en een kaart zonder enige referentie.
Een cijfermatige uitspraak zonder onderbouwende publicatie hoort niet op de
kaart; voeg de bron toe of haal de claim weg.

## Verwoording: de kracht van interventieradiologie voorop

De site is er om de onderbouwing van interventieradiologie te tonen. In de
kaartteksten (bl, de drie regels van `pos`, `crit`, `results`, `lim`, `alts`)
mag de verwoording de sterke kant van IR naar voren schuiven, zolang niets wordt
weggelaten of verdraaid. Dit geldt voor de kaartteksten, niet voor de losse
publicatiesamenvattingen; die blijven trouw aan het abstract.

Concreet bij een directe vergelijking met chirurgie, resectie of radiotherapie:

- Begin met wat in het voordeel van IR is: gelijkwaardige uitkomst in de
  subgroep waar dat bewezen is (bijvoorbeeld onder een groottegrens), en de
  voordelen van IR zoals minder complicaties, lagere mortaliteit, lagere kosten,
  minder invasief of herhaalbaarheid.
- Noem daarna eerlijk waar de vergelijker beter was, met dezelfde cijfers en
  p-waarden. Laat nooit een ongunstige uitkomst weg en zwak een p-waarde niet af.
- Benoem expliciet de subgroep waarin IR bewezen is en welke grotere of
  moeilijkere groep nog in lopende studies onderzocht wordt.

Voorbeeld. Niet: "chirurgie gaf betere lokale progressievrije overleving
(p=0,021), maar ablatie had de laagste complicatiekans; onder 5 cm geen
verschil". Wel: "onder 5 cm even goede lokale controle als chirurgie en
radiotherapie (p=0,23), met de laagste complicatiekans en kosten; bij grotere
laesies bleven chirurgie en radiotherapie superieur voor lokale progressievrije
overleving (p=0,021)". Dezelfde feiten, andere volgorde.

Alle getallen, p-waarden en de referentie blijven staan. Dit is een kwestie van
volgorde en nadruk, niet van selectie.

Visueel uitlichten. De sterke kant van IR mag ook zichtbaar worden gemaakt. Er
zijn twee middelen. Het inline-accent is de huisstijl: zet op de
vergelijkingsregel de zinsnede met de gelijkwaardigheid of het IR-voordeel tussen
`<span class="ir">...</span>`, dan krijgt die een rustig groen accent. Op een
enkele vlaggenschipkaart met een echte kop-aan-kop-vergelijking mag daarnaast een
callout: vul dan op de kaart in beide talen het veld `sterk` met twee tot vier
korte punten (`"sterk":["...","..."]`), dan verschijnt boven Positie en kracht
het blok "Kracht van IR". Gebruik op zo'n kaart de callout of het inline-accent,
niet allebei, om dubbele nadruk te voorkomen. De p-waarden en de referentie
blijven in de gewone tekst staan; de punten in de callout zijn een korte
samenvatting, geen vervanging.

## Bondig verwoorden

Kort en to-the-point heeft de voorkeur. Schrijf nieuwe of gewijzigde
kernboodschappen (`bl`) meteen beknopt: elke feitelijke claim, elk getal, elke
p-waarde en elke trialnaam blijft staan, maar bindwoorden en herhaling gaan
eruit. Een kernboodschap van meer dan ongeveer honderd woorden is bijna altijd
in te korten zonder verlies; laat al compacte kaarten met rust.

De punten in de `sterk`-callout ("Kracht van IR") schrijf je in telegramstijl,
niet als volzin. Begin waar het kan met de grens of het getal en benoem de
vergelijker, bijvoorbeeld "<5 cm: lokale controle even goed als chirurgie en
radiotherapie" of "Solitair ≤5 cm: <50% van de kosten van resectie, opname 3 vs
10 dagen". Een kleiner-dan gevolgd door een cijfer (`<5 cm`, `<50%`) mag
letterlijk blijven staan; de browser leest dat als tekst, niet als een tag.

## Modaliteitsvoorkeur binnen ablatie

Ablatie is geen monoliet: RFA, microwave (MWA), cryoablatie en IRE verschillen
per indicatie. Waar de literatuur laat zien dat één modaliteit voor een
behandeling betere resultaten haalt dan de andere, benoem dat expliciet in de
kaarttekst, met dezelfde bronregels als elke andere claim (cijfers geverifieerd,
referentie erbij). En andersom: is een modaliteit voor een indicatie achterhaald
of verdrongen door een betere techniek, zeg dat dan ook, zodat de kaart niet
suggereert dat alle ablatievormen gelijkwaardig zijn.

Houd de terminologie zuiver (RFA is radiofrequente ablatie, MWA is microwave,
enzovoort) en overdrijf niet: een voorkeur staat alleen op de kaart als een
opgehaalde bron een directe of indirecte vergelijking onderbouwt. Ontbreekt die
vergelijking, dan blijft de neutrale formulering "thermale ablatie (RFA of
microwave)" staan en noteer je de openstaande vraag voor een volgende ronde.

## Tekstwijzigingen aan de kaart

Een ronde past ook de kaarttekst zelf aan waar nieuwe literatuur daarom vraagt:
bl, de drie regels van `pos`, `crit`, `results`, `lim` en `alts`. De ronde voert
zulke wijzigingen zelf door, in beide talen, per zin en niet als herschrijving
van de hele alinea, en laat elke wijziging steunen op een bron die in die ronde
is opgehaald. Volg daarbij de verwoordingsregels hierboven (kracht van IR voorop,
niets weglaten of afzwakken).

## Terugkerende actualisatie

Naast nieuwe literatuur houdt elke ronde ook het bestaande actueel:

- Lopende studies. Loop de `ongoing`-lijsten na. Is een trial afgerond en gepubliceerd, verplaats hem dan naar `core` of `latest` met een samenvatting met kerngetallen; is hij ingetrokken of gestopt, haal hem weg. Controleer de status via het trialregister (NCT-nummer) of een recente publicatie.
- Richtlijnversies. Controleer of een geciteerde richtlijn (BCLC, EASL, AASLD, ESMO, NCCN, CIRSE, Richtlijnendatabase) een nieuwere versie heeft en werk jaartal, link en zo nodig het standpunt bij.
- Kosten en resource-gebruik. Waar een kaart een directe vergelijking met chirurgie of radiotherapie heeft, is een kosten-, ligduur- of dagopname-vergelijking een sterke, onderbelichte troef van IR. Voeg zo'n studie toe als je die vindt en laat het punt in de kaarttekst of de callout terugkomen, altijd met bron.

## Wat je niet doet

- Voorstellen opnemen waarvan je de cijfers niet hebt kunnen verifiëren.
- Bestaande items of kaartteksten herschrijven zonder dat een opgehaalde bron dat steunt.
- Een ongunstige uitkomst of p-waarde weglaten of afzwakken.
- Iets publiceren dat de controles (controle.py, bouw-stubs.js) niet doorstaat.
