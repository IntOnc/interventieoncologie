# Onderhoudspipeline voor interventieoncologie.nl

Ontwerp van 26 juli 2026, op basis van de werkelijke onderhoudslast van de site op dat moment.

## Waar het over gaat

De site telt 34 kaarten met 333 literatuurverwijzingen, en omdat alles tweetalig is
staan er 666 samenvattingen in die kunnen verouderen. Een derde van de verwijzingen
komt uit 2024 of later, 94 verwijzingen zijn uit 2019 of eerder. De oudste richtlijn
die op een kaart staat is dertien jaar oud. Zonder pipeline verschuift de vraag
binnen een jaar van "wat voegen we toe" naar "wat klopt er nog".

De schaarse hulpbron is niet zoekwerk en niet schrijfwerk. Het is het oordeel van
de interventieradioloog: hoort dit erbij, en verandert het wat we doen. Alles wat
geen oordeel vraagt hoort geautomatiseerd, en alles wat wel oordeel vraagt hoort
zo aangeleverd dat het in minuten te beslissen is.

## Het uitgangspunt

Drie regels waar het ontwerp op rust.

De eerste is dat de inhoud losstaat van de vormgeving. Zolang alle tekst in het
HTML-bestand zit kan alleen iemand die dat bestand durft te bewerken er iets aan
veranderen. Daarom staat de inhoud nu ook als `content.json` naast de site.

De tweede is dat de pipeline nooit rechtstreeks publiceert. Hij levert voorstellen
aan, en publiceren gebeurt pas na akkoord. Bij een evidence-site is een fout in een
getal erger dan een maand vertraging.

De derde is dat elk voorstel al af moet zijn. Een melding dat er iets nieuws is
kost meer tijd dan hij oplevert. Een kant-en-klaar item in het format van de kaart,
inclusief geverifieerde cijfers en de plek waar het hoort, is in twintig seconden
te beoordelen.

## De vier stappen

### 1. Signaleren, automatisch

Per kaart staat in `watchlist.json` wat er gevolgd moet worden: de zoektermen in
beide talen, de richtlijnen met hun URL en datum, en de lopende-onderzoeksqueries.
Dat bestand wordt uit de site zelf afgeleid, dus een nieuwe kaart komt er vanzelf in.

Er wordt op drie dingen gelet. Nieuwe publicaties die binnen de zoektermen van een
kaart vallen. Richtlijnen waarvan de versie of de datum is veranderd, want een
gewijzigde aanbeveling raakt de kaart harder dan een nieuwe cohortstudie. En
studies die van wervend naar afgerond zijn gegaan, want dat is het moment waarop
er resultaten aankomen.

### 2. Filteren, automatisch

Het merendeel van wat een zoekopdracht oplevert hoort er niet in. Er wordt
weggefilterd op vier gronden: case reports en kleine series zonder uitkomstmaten,
overzichtsartikelen die niets toevoegen aan wat er al staat, publicaties die al op
de kaart staan, en publicaties waarvan de cijfers niet te verifiëren zijn omdat de
uitgever niet toegankelijk is.

Wat overblijft wordt gerangschikt op wat het met de kaart doet. Een richtlijnwijziging
komt bovenaan, daarna iets dat een bestaand cijfer tegenspreekt, daarna een
gerandomiseerde trial, daarna een meta-analyse, en pas daarna een cohortstudie die
het beeld bevestigt.

### 3. Opstellen, automatisch

Elk voorstel wordt geleverd als een compleet item in het format van de kaart:
de exacte titel, tijdschrift en jaar, de directe link, een samenvatting met Opzet,
Resultaten en Conclusie inclusief de getallen, en de sorteersleutel. In beide talen.
Daarbij staat waar het heen moet (welke kaart, welke lijst) en wat het met de
bestaande tekst doet, dus of het iets aanvult of iets tegenspreekt.

Cijfers die niet op een opgehaalde pagina te lezen waren gaan er niet in. Die
komen op de verifieerlijst.

### 4. Beoordelen, met de hand

Wat er maandelijks binnenkomt is een overzicht met per voorstel drie mogelijke
antwoorden: opnemen, niet opnemen, of eerst zelf lezen. Daarbij twee vaste lijsten:
de kaarten waar in twaalf maanden niets nieuws bij is gekomen, en de items met een
⚠-vlag waar nog cijfers ontbreken.

Dit is het enige deel dat tijd kost. De schatting is twintig tot dertig minuten per
maand bij de huidige omvang.

## Hoe het draait

Er is geen server, geen abonnement en geen software om te installeren. Eens per
maand start een geplande taak een sessie die de watchlist afloopt, de zoekopdrachten
doet, de vondsten verifieert en het overzicht als bestand aflevert. Bij akkoord
worden de goedgekeurde items in een werksessie op de site toegepast, waarna de
gewijzigde versie teruggeleverd wordt.

Dat is bewust de eenvoudigste vorm die werkt. Als de site later echt online komt te
staan hoort daar een repository bij waarin de inhoud als data leeft en waarin elke
wijziging als voorstel binnenkomt dat met één klik wordt goedgekeurd. Dat is dezelfde
pipeline met een nettere administratie eromheen, en het is een verplaatsing waarvoor
het huidige `content.json` al klaarligt.

## Wat er nu al ligt

`content.json` bevat de volledige inhoud van de site als data, los van de
vormgeving. Dat is het bestand waar een toekomstige website, een app of een
exportfunctie op kan draaien.

`watchlist.json` bevat per kaart wat er gevolgd moet worden, afgeleid uit de site
zelf, inclusief de items waar nog cijfers ontbreken.

`staleness.json` rangschikt de kaarten op veroudering, gemeten aan de nieuwste
publicatie erop, de oudste richtlijn erop en het aantal dunne items. Dat is de
volgorde waarin een maandelijkse ronde de kaarten aan zou moeten pakken.

## De eerste proefronde

Op de meest verouderde kaart, IRE bij perivasculaire colorectale levermetastasen,
waar de nieuwste publicatie ruim zeven jaar oud was, leverde één zoekopdracht een
systematische review uit 2023 op met 8 studies en 180 patiënten. Die is geverifieerd
en toegevoegd, en levert precies wat de kaart miste: een compleet complicatieprofiel
met procedure-gerelateerde mortaliteit van 1,1%, ritmestoornissen bij 5%, bloeding
bij 3,8% en galwegstricturen bij 2,8%.

Tijd voor de beoordeling: één publicatie, één beslissing.

## Wat er nog beslist moet worden

Het ⚠-signaal staat nu te ruim afgesteld. Het markeert elk item in Core evidence
of Latest publications zonder cijfer in de samenvatting, en dat zijn er 77. Een
deel daarvan is terecht, maar bij overzichtsartikelen en richtlijnstandpunten is
een getal ook niet te verwachten. Het signaal moet onderscheid gaan maken tussen
een studie die uitkomsten hoort te rapporteren en een publicatie die dat van
nature niet doet, anders is de lijst te lang om iets mee te doen.

De frequentie is een tweede keuze. Maandelijks past bij de huidige groei. Per
kwartaal is verdedigbaar zodra de site stabiel is, met als uitzondering dat
richtlijnwijzigingen altijd direct worden gemeld.
