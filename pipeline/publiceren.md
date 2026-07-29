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
- Draai `python3 pipeline/controle.py`. Dat controleert de terminologie, de
  kale statements en de stijl (harde checks: em/en-dash, dubbele spatie,
  niet-compacte p-notatie; zachte waarschuwingen: vaag woord zonder getal, zin
  van meer dan 45 woorden). Faalt de controle op een harde check, los die dan op
  of bevestig dat ze terecht is voordat je pusht. De zachte waarschuwingen laten
  de controle slagen, maar loop ze na en kwantificeer of splits waar dat kan.

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

## Verwoording en huisstijl

De volledige huisstijl staat in `pipeline/redactiegids.md`. Lees die gids vóór je
een kaarttekst schrijft of wijzigt; hij is de enige bron voor toon, opbouw,
getallen, terminologie en de visuele middelen. De kern in het kort:

- Kracht van IR voorop, maar niets weglaten, verdraaien of afzwakken; alle
  getallen, p-waarden en referenties blijven staan. Dit is volgorde en nadruk,
  geen selectie.
- Kernboodschap bondig, met een vaste openingszin en witregels tussen de
  alinea's (nl en en gelijk aantal).
- Kwantificeer vage woorden (klein, hoog, vaak, zeldzaam) met het getal uit de
  bron; verzin niets.
- Wat zwak is onderbouwd (één retrospectieve studie of cohort) hoort niet in de
  kernboodschap, hooguit in `results` met de opzet benoemd. Alleen een RCT of
  meta-analyse is sterk genoeg voor `bl`.
- Modaliteitsvoorkeur binnen ablatie alleen met een onderbouwende bron; anders
  de neutrale formulering "thermale ablatie (RFA of microwave)".
- Terminologie zuiver (RFA, MWA, TARE, cTACE, DEB-TACE) en één term per begrip.
- Visueel: inline `.ir`-accent of de `sterk`-callout in telegramstijl, niet
  allebei op één kaart.

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
- Wachtrij. `pipeline/wachtrij.json` is de gedeelde lijst van eerder gevonden maar nog niet verifieerbare items. Loop die aan het begin van je ronde langs: is een item nu wel indexeerbaar, voeg het dan toe en haal het uit de wachtrij; laat items ouder dan 60 dagen vallen. Wat je zelf vindt maar niet kunt verifieren, zet je erin met datum.

## Verhouding tot de dagelijkse scan

Naast deze diepe rondes (maandag, woensdag, vrijdag) draait op de tussenliggende dagen een lichte dagelijkse scan, beschreven in `pipeline/dagelijkse-scan.md`. Die ontdekt alleen of er nieuwe, geindexeerde literatuur of een gewijzigde trialstatus is en verwerkt dat gericht; het volledige tijdschrift- en per-kaart-werk blijft aan de diepe rondes. Beide delen dezelfde `wachtrij.json`.

## Wat je niet doet

- Voorstellen opnemen waarvan je de cijfers niet hebt kunnen verifiëren.
- Bestaande items of kaartteksten herschrijven zonder dat een opgehaalde bron dat steunt.
- Een ongunstige uitkomst of p-waarde weglaten of afzwakken.
- Iets publiceren dat de controles (controle.py, bouw-stubs.js) niet doorstaat.
