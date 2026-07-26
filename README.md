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

Een literatuurverwijzing is steeds een rij van vijf:

    [titel, "tijdschrift · jaar", url, samenvatting, sorteersleutel JJJJMM]

De samenvatting gebruikt `<b>Opzet:</b>`, `<b>Resultaten:</b>` en
`<b>Conclusie:</b>` in het Nederlands, en `Design`, `Results` en `Conclusion`
in het Engels. Het ⚠-signaal kijkt naar het Resultaten-segment: staat daar geen
getal in, dan wordt het item gemarkeerd als "cijfers te verifiëren".

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
