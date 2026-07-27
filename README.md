# interventieoncologie.nl

Tweetalige evidence-site over interventieoncologie.

## Structuur

    index.html      de schil: opmaak en weergavecode, ongeveer 30 kB
    content.json    alle inhoud: kaarten, literatuur, techniekpagina's
    bouw-offline.js maakt een enkel bestand voor lokaal bekijken
    interventieoncologie-offline.html  het resultaat daarvan

De site laadt `content.json` op bij het openen. Inhoud en vormgeving staan
daarmee los van elkaar, en dat is met opzet: de onderhoudspipeline bewerkt
uitsluitend `content.json` en komt nooit aan `index.html`.

## Wat er waar staat in content.json

    site        de vaste teksten van de site, per taal
    organs      de organen voor het filter
    diseases    de ziektebeelden voor het filter
    techs       de technieken voor het filter
    index       per kaart de facetten, ondertitel en zoektermen
    cards       de inhoud van elke kaart, in het Nederlands en Engels
    pos         de drie regels van "Positie en kracht" per kaart
    techpages   de techniekoverzichtspagina's
    editorial   de vaste voettekst over auteurschap en herziening

Een literatuurverwijzing is een rij van vijf, met een optioneel zesde element:

    [titel, "tijdschrift · jaar", url, samenvatting, sorteersleutel JJJJMM, auteur]

Het zesde element is de eerste auteur zoals die getoond wordt, bijvoorbeeld
"Meijerink et al." of, bij een enkele auteur, alleen de achternaam. Het mag
ontbreken of leeg zijn; de weergave laat het veld dan gewoon weg. Vul het
alleen met een naam die je op het registratie- of uitgeversrecord hebt gelezen.

Een zevende element bevat de gegevens voor de bewijskracht:

    {"d":"rct3","n":760,"mc":1,"cmp":1,"t":"A"}

`d` is de studieopzet (`meta_rct`, `rct3`, `rct`, `meta`, `prosp`, `retro`,
`serie` of `review`), `n` het aantal patienten, `mc` 1 bij multicentrisch,
`cmp` 1 bij een vergelijkende opzet en `t` de tijdschriftklasse A, B of C.
Ontbreekt het veld of is `d` leeg, dan toont de site geen score in plaats van
een gegokte. De klassenlijst met tijdschriften staat in `content.json` onder
`tijdschriften` en mag daar worden uitgebreid.

De score loopt van 0 tot 100 en is opgebouwd uit opzet (maximaal 50), aantal
patienten (maximaal 18), vergelijkend (10), multicentrisch (10) en tijdschrift
(maximaal 12). Opzet weegt bewust het zwaarst: een gerandomiseerde fase
III-trial in een gemiddeld blad hoort hoger uit te komen dan een kleine
retrospectieve serie in een goed blad. De opbouw staat bij elk item uitgeklapt,
zodat een lezer kan zien waar het cijfer vandaan komt en het desgewenst kan
negeren.

De lijsten `core`, `latest` en `ongoing` worden op de kaart als een lijst
getoond, gesorteerd op sorteersleutel met de nieuwste bovenaan, met knoppen om
op soort te filteren. De richtlijnen staan daarboven in een eigen blok.

De samenvatting gebruikt `<b>Opzet:</b>`, `<b>Resultaten:</b>` en
`<b>Conclusie:</b>` in het Nederlands, en `Design`, `Results` en `Conclusion`
in het Engels. Het ⚠-signaal kijkt naar het Resultaten-segment: staat daar geen
getal in, dan wordt het item gemarkeerd als "cijfers te verifiëren".

## Adressen

Elke kaart en elke techniekpagina heeft een eigen adres. In de applicatie is dat
een hash-route, bijvoorbeeld `#/nl/kaart/rcc-ablatie` of `#/en/techniek/abl`.
Daarnaast staat er per kaart een vindbare pagina op schijf, bijvoorbeeld
`kaart/rcc-ablatie/`, met een eigen titel, omschrijving en Open Graph-gegevens,
zodat zoekmachines en linkvoorbeelden iets zinnigs te pakken hebben. Die pagina
stuurt een bezoeker met JavaScript door naar de interactieve versie.

`node bouw-stubs.js` genereert die pagina's, plus `sitemap.xml`, `robots.txt` en
`wijzigingen.json`. Draai dat na elke inhoudelijke wijziging. Staat de site
later op het eigen domein, pas dan de constante `BASIS` bovenin dat bestand aan.

## Lokaal bekijken

`index.html` rechtstreeks vanaf de schijf openen werkt niet, omdat de browser
dan geen `content.json` mag ophalen. Twee manieren die wel werken:

    python -m http.server 8000

en dan http://localhost:8000 openen, of gebruik
`interventieoncologie-offline.html`, waarin de inhoud is ingebakken.

Na een wijziging in `content.json` de offline-versie opnieuw maken met:

    node bouw-offline.js

## Onderhoud

De maandelijkse ronde leest deze repository, zoekt per kaart naar nieuwe
evidentie, verifieert de cijfers en levert voorstellen aan. Goedgekeurde
voorstellen worden in `content.json` verwerkt. Zie de map `pipeline` voor het
ontwerp en de watchlist.

## Herkomst en aansprakelijkheid

De inhoud is een samenvatting van gepubliceerde evidentie en vervangt geen
klinisch oordeel. Bij elke verwijzing staat de directe link naar de bron, zodat
elk getal terug te voeren is op de publicatie waar het uit komt.
