# Redactiegids — Interventie Oncologie

Dit is de enige bron voor de huisstijl van de kaartteksten. Lees hem vóór je een
kaarttekst schrijft of wijzigt. Hij geldt voor de redactionele velden in beide
talen: `bl` (kernboodschap), de drie regels van `pos` (g/l/v), `crit`, `results`,
`lim`, `alts` en de `sterk`-callout.

Uitzondering: de losse publicatiesamenvatting (het vierde element van een
literatuurrij) blijft trouw aan het abstract en volgt deze stijlregels alleen
voor zover ze de feiten niet raken. De verwoordingsvrijheid hieronder geldt voor
de kaartteksten, niet voor die samenvattingen.

De machinaal te controleren regels worden afgedwongen door `pipeline/controle.py`
en de checklist in `pipeline/publiceren.md`. Draai die controle vóór het pushen.
De controle faalt hard op een em- of en-dash, een dubbele spatie en een
niet-compacte p-notatie (hoofdletter-P of spaties rond de operator), en
waarschuwt zacht (zonder te falen) bij een kwalitatief uitkomstwoord zonder getal
in de buurt en bij een zin van meer dan 45 woorden in de kernboodschap. Loop die
zachte punten na; ze zijn een uitnodiging om te kwantificeren of te splitsen,
geen verbod.

## 1. Toon en doel

De site toont de onderbouwing van interventieradiologie (IR). De verwoording mag
de sterke kant van IR vooropzetten, zolang er niets wordt weggelaten, verdraaid
of afgezwakt. Eerlijk en pro-IR sluiten elkaar niet uit: het is een kwestie van
volgorde en nadruk, nooit van selectie.

## 2. Opbouw van de kernboodschap (`bl`)

Vaste openingszin. Begin elke kernboodschap met hetzelfde patroon: "[techniek]
is [wat] voor [indicatie met maat]." Zo krijgt de lezer kaart na kaart meteen
houvast.

Bondig. Kort en to-the-point heeft de voorkeur. Elke feitelijke claim, elk getal,
elke p-waarde en elke trialnaam blijft staan, maar bindwoorden en herhaling gaan
eruit. Een kernboodschap van meer dan ongeveer honderd woorden is bijna altijd in
te korten zonder verlies; laat al compacte kaarten met rust.

Witregels tegen lappen tekst. Verdeel een kernboodschap van meer dan twee, drie
zinnen in alinea's. Zet in `bl` een lege regel (twee newlines, `\n\n`) op een
natuurlijk breekpunt, bijvoorbeeld tussen "wat het is" en "het bewijs", of vóór
een losse risico- of nuancezin. De front-end rendert elk door een lege regel
gescheiden blok als een eigen alinea. Houd het aantal alinea's in `nl` en `en`
gelijk en breek nooit midden in een citaat of een getal.

Geen opsomming van primaire-tumortypes. Laat bij een metastase-indicatie de
opsomming van welke primaire tumoren het kan betreffen (long, niercel,
colorectaal, melanoom, enzovoort) weg; die voegt niets toe aan de kernboodschap.

## 3. Getallen, eenheden en vergelijkingen

Kwantificeer vage woorden. Schrijf "hoog", "laag", "klein", "vaak" of "zeldzaam"
nooit zonder het getal uit de bron ernaast, waar de bron dat geeft: "technisch
succes rond 90%", niet "hoog technisch succes"; "zeldzaam (<1%)"; "kleine tumoren
(<5 cm)". De grens of het percentage moet steunen op de literatuur van de kaart;
verzin geen getal. De maat bij "klein" is kaartspecifiek: "(<5 cm)" bij
bijnierablatie, "(tot ongeveer 3 cm)" bij HCC, "(cT1a, ≤4 cm)" bij
niercelcarcinoom. Staat de maat al eerder in dezelfde zin, dan hoef je haar niet
te herhalen.

Vast vergelijkingspatroon. Schrijf een directe vergelijking als "A tegen B:
X% versus Y% (p=…)", met de IR-kant eerst. Gebruik consequent "versus" tussen de
twee cijfers en "tegen" (of "tegenover") om de twee behandelingen te introduceren;
wissel niet af met "vergeleken met" en "ten opzichte van" binnen dezelfde functie.

p-waarden. Schrijf "p=0,005" en "p<0,001" (in het Engels met punt: "p=0.005").
Een kleiner-dan-teken gevolgd door een cijfer (`<5 cm`, `<50%`, `p<0,001`) mag
letterlijk blijven staan; de browser leest dat als tekst, niet als een tag. Zwak
een p-waarde nooit af en laat er nooit een weg.

Decimalen en eenheden. In het Nederlands een komma als decimaalteken (2,7 cm), in
het Engels een punt (2.7 cm). Zet een spatie tussen getal en eenheid (10 mm,
44 maanden). Houd binnen een kaart dezelfde eenheid aan voor dezelfde grootheid.

## 4. Bewijskracht in de verwoording

Laat het werkwoord de opzet verraden. Een gerandomiseerde trial of meta-analyse
"toont", "geeft" of "bevestigt"; een prospectief of retrospectief cohort "wijst
op" of "suggereert". Zo signaleert de zin zelf hoe hard het bewijs is.

Zwak onderbouwd hoort niet in de kernboodschap. Rust een claim op één
retrospectieve studie of een enkel cohort, dan is dat te zwak voor `bl`; laat de
studie in de literatuurlijst staan en zet de nuance hooguit in `results`, met de
opzet expliciet benoemd ("in een retrospectieve studie"). Alleen een RCT of
meta-analyse is sterk genoeg voor een uitspraak in de kernboodschap.

Weeg de klinische context mee. Een techniek die in de richtlijnen en de praktijk
geen gangbare optie is voor een indicatie (bijvoorbeeld cryoablatie bij HCC, dat
op één RCT uit 2015 rust) hoort niet als voorkeur in de kernboodschap, ook niet
als er een positieve trial bestaat.

## 5. Vergelijking met chirurgie, resectie of radiotherapie

Bij een directe vergelijking, in deze volgorde:

- Begin met wat in het voordeel van IR is: gelijkwaardige uitkomst in de subgroep
  waar dat bewezen is (bijvoorbeeld onder een groottegrens), en de voordelen van
  IR zoals minder complicaties, lagere mortaliteit, lagere kosten, minder invasief
  of herhaalbaarheid.
- Noem daarna eerlijk waar de vergelijker beter was, met dezelfde cijfers en
  p-waarden.
- Benoem expliciet de subgroep waarin IR bewezen is en welke grotere of
  moeilijkere groep nog in lopende studies onderzocht wordt.

Voorbeeld. Niet: "chirurgie gaf betere lokale progressievrije overleving
(p=0,021), maar ablatie had de laagste complicatiekans; onder 5 cm geen verschil".
Wel: "onder 5 cm even goede lokale controle als chirurgie en radiotherapie
(p=0,23), met de laagste complicatiekans en kosten; bij grotere laesies bleven
chirurgie en radiotherapie superieur voor lokale progressievrije overleving
(p=0,021)". Dezelfde feiten, andere volgorde.

## 6. Modaliteitsvoorkeur binnen ablatie

Ablatie is geen monoliet: RFA, microwave (MWA), cryoablatie en IRE verschillen
per indicatie. Waar de literatuur laat zien dat één modaliteit voor een
behandeling betere resultaten haalt, benoem dat expliciet, met dezelfde bronregels
als elke andere claim. Is een modaliteit voor een indicatie achterhaald of
verdrongen, zeg dat dan ook, zodat de kaart niet suggereert dat alle
ablatievormen gelijkwaardig zijn.

Een voorkeur staat alleen op de kaart als een opgehaalde bron een vergelijking
onderbouwt, en alleen in de kernboodschap als die bron een RCT of meta-analyse is
(zie sectie 4). Ontbreekt de vergelijking, dan blijft de neutrale formulering
"thermale ablatie (RFA of microwave)" staan.

## 7. Terminologie

Afkortingen exact. RFA is uitsluitend radiofrequente ablatie, MWA is microwave-
of microgolfablatie, TARE en SIRT zijn radio-embolisatie (nooit
chemo-embolisatie), cTACE is conventionele TACE en DEB-TACE de variant met
drug-eluting beads. Koppel een afkorting nooit aan de verkeerde term;
`controle.py` meldt "microgolfablatie (RFA)" en dergelijke.

Eén term per begrip. Gebruik voor hetzelfde begrip steeds dezelfde term en wissel
niet tussen synoniemen. De vaste keuzes: "opnameduur" (niet "ligduur"),
"complicatiekans" (niet "complicatierisico"), "lokale controle" (niet "lokale
tumorcontrole"), "majeure complicaties", "technisch succes".

Bewaar wél de echte verschillen tussen eindpunten. "Lokale controle", "lokaal
recidiefvrije overleving", "progressievrije overleving" en "totale overleving"
zijn geen synoniemen en mogen niet door elkaar worden gebruikt; volg wat de bron
meet. Let ook op het verschil tussen "technisch succes" (de procedure is volgens
plan uitgevoerd) en "technische effectiviteit" (volledige ablatie op de eerste
controle-beeldvorming) — dat zijn twee verschillende eindpunten, geen synoniemen.

Tijdschriftnaam voluit. Zet in het tijdschriftveld de naam voluit; de site kort
hem zelf in via de lijst `afkortingen`. Nooit de afkorting zelf in het veld.

## 8. Visuele middelen

Inline-accent. Zet op de vergelijkingsregel de zinsnede met de gelijkwaardigheid
of het IR-voordeel tussen `<span class="ir">...</span>` voor een rustig groen
accent. Dit is de standaard.

Kracht-van-IR-callout. Op een vlaggenschipkaart met een echte
kop-aan-kop-vergelijking mag daarnaast het veld `sterk` (twee tot vier punten in
beide talen); dan verschijnt boven Positie en kracht het blok "Kracht van IR".
Schrijf die punten in telegramstijl, niet als volzin, begin waar het kan met de
grens of het getal en benoem de vergelijker: "<5 cm: lokale controle even goed als
chirurgie en radiotherapie", "Solitair ≤5 cm: <50% van de kosten van resectie,
opname 3 vs 10 dagen". Gebruik op één kaart de callout óf het inline-accent, niet
allebei. De p-waarden en de referentie blijven in de gewone tekst; de callout is
een samenvatting, geen vervanging.

Bold alleen het uitkomstcijfer. Zet in de `results`-regels alleen het
uitkomstgetal tussen `<b>...</b>`, niet halve zinnen. Dat houdt de sectie
scanbaar.

## 9. Typografie

Geen em-dash of en-dash. Gebruik een komma, een dubbele punt of het woord "tot"
voor een bereik ("3 tot 5 cm", niet "3–5 cm"). Geen dubbele spaties.

## 10. Tweetaligheid

Nederlands is primair, Engels loopt parallel. De lijsten `guides`, `core`,
`latest` en `ongoing` zijn per kaart even lang in `nl` en `en` en staan in
dezelfde volgorde; de kernboodschap heeft in beide talen hetzelfde aantal
alinea's. Een wijziging in de ene taal krijgt altijd meteen zijn tegenhanger in
de andere.
