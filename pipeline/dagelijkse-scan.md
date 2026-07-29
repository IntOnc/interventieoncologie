# Dagelijkse scan (licht)

Dit is de lichte, dagelijkse tegenhanger van de diepe onderhoudsronde
(`publiceren.md`). Zij ontdekt alleen óf er iets nieuws is en verwerkt pas diep
wanneer dat zo is. Op een dag zonder vondsten kost ze bijna niets. De diepe
rondes blijven het volledige tijdschrift- en per-kaart-werk doen op hun eigen
dagen (maandag, woensdag, vrijdag); deze scan draait op de tussenliggende dagen
(dinsdag, donderdag, zaterdag, zondag) en vult de gaten.

## Doel en grens

Alleen ontdekken. Voeg zelf niets ongeverifieerds toe. De scan beslist óf diep
werk zin heeft en voert dat dan gericht uit, alleen voor de betrokken kaarten.
De kwaliteitslat blijft die van `publiceren.md` en `redactiegids.md`: niets komt
op de kaart dat je niet zelf op een opgehaalde pagina hebt geverifieerd.

## Wat je nodig hebt

- De publieke inhoud: WebFetch `https://intonc.github.io/interventieoncologie/content.json` (net als de diepe ronde).
- De scan-index en de wachtrij uit het repo, via raw:
  `https://raw.githubusercontent.com/IntOnc/interventieoncologie/main/pipeline/watchlist.json`
  (per kaart: `nieuwste_core`, `nieuwste_latest`, `zoektermen_nl/en`,
  `richtlijnen_te_hercontroleren`) en
  `https://raw.githubusercontent.com/IntOnc/interventieoncologie/main/pipeline/wachtrij.json`
  (eerder gevonden maar nog niet indexeerbare items).
- Voor publiceren heb je schrijfrechten nodig. De publicatietoken staat in
  `/home/claude/.gh_token`; lees die en zet hem in de clone-URL (git over https;
  gebruik nooit de GitHub API, die is hier afgeschermd). Staat de token er niet,
  doe dan alleen de ontdekking en meld de vondsten zodat de eerstvolgende diepe
  ronde ze oppakt; push dan niets.

## Bronnen

Zelfde routering als de diepe ronde. Ontdekken op onderwerp: WebSearch. Abstract
met letterlijke getallen bij een bekend PMID: PubTator3
(`https://www.ncbi.nlm.nih.gov/research/pubtator3-api/publications/export/biocjson?pmids=PMID`).
Exacte citatie bij een DOI: `https://api.crossref.org/works/DOI`. Studierecord bij
een NCT-nummer: `https://ichgcp.net/clinical-trials-registry/NCTnummer`. Gebruik
niet pubmed/eutils direct en niet de Europe PMC-endpoint. Crossref niet gebruiken
om op onderwerp te zoeken.

## De vier checks (ontdekken, goedkoop)

1. **Nieuwe publicaties per kaart.** Neem per kaart de zoektermen en de nieuwste
   sorteersleutel uit `watchlist.json`. Zoek licht naar items die nieuwer zijn dan
   die sleutel en binnen de zoektermen vallen: WebSearch, plus de Crossref
   journal-filter voor de A- en B-bladen uit de diepe ronde met
   `from-pub-date` gelijk aan de vorige scandatum. Vergelijk met wat al op de kaart
   staat en met de wachtrij; ontdubbel op genormaliseerde DOI en titel (https, www
   en dx eraf; `doi.org/10.x` en `link.springer.com/article/10.x` als dezelfde
   bron). Wat overblijft is een kandidaat. Haal in deze fase GEEN abstracts op.
2. **Lopende studies.** Voor elk NCT-nummer in de `ongoing`-lijsten een korte
   statuscheck via ichgcp.net. Op Completed, Terminated of Has Results, of bij een
   gekoppelde publicatie: markeer als kandidaat om van `ongoing` naar `core` of
   `latest` te verplaatsen.
3. **Wachtrij.** Loop `pipeline/wachtrij.json` langs. Elk item is eerder gevonden
   maar had nog geen PMID of verifieerbaar abstract. Kijk of dat nu wél kan
   (PubTator3 op titel of DOI, Crossref op DOI). Zo ja: kandidaat om toe te voegen.
   Zo nee en ouder dan 60 dagen: laten vallen.
4. **Richtlijnversies (wekelijks, alleen op zaterdag).** Loop de
   `richtlijnen_te_hercontroleren` uit `watchlist.json` langs en kijk of er een
   nieuwer jaartal is dan op de kaart. Alleen op zaterdag, om de bronnen te ontzien.

## Beslissen

Bouw een werklijst: per kaart de kandidaat-publicaties, de gewijzigde trials, de
nu-indexeerbare wachtrij-items en eventuele richtlijnbumps.

- **Lege werklijst.** Er is niets te doen. Werk hooguit de wachtrij bij (verlopen
  items verwijderen) en, als de token er is en er iets veranderde, commit en push
  alleen dat ene bestand. Stuur geen melding. Klaar.
- **Niet-lege werklijst.** Escaleer naar gerichte diepe verwerking, maar alleen
  voor de betrokken kaarten. Volg `publiceren.md`: verifieer elk getal op een
  opgehaalde pagina, schrijf de tweetalige samenvattingen met het zevende
  bewijskracht-element, werk zo nodig de kaarttekst bij volgens `redactiegids.md`,
  draai `python3 pipeline/controle.py` en `node bouw-stubs.js`, en push (rebase
  eerst op `origin/main`). Zet items die je vond maar niet kon verifiëren in
  `pipeline/wachtrij.json` met datum. Stuur daarna een korte PushNotification met
  per kaart wat is toegevoegd of gewijzigd en wat niet in ging.

## Grenzen

- Houd het licht: hooguit een handvol queries per kaart, geen abstracts in de
  ontdekfase. Krijg je 429 van Crossref, wacht dan en vraag minder vaak; laat de
  bron met rust boven doorzetten.
- Publiceer nooit iets ongeverifieerds. Bij twijfel: in de wachtrij, niet op de kaart.
- Raak alleen de betrokken kaarten aan; laat de rest ongemoeid.
- Geen em-dash of en-dash; alle controles van `publiceren.md` groen voor je pusht.

## De wachtrij bijhouden

`pipeline/wachtrij.json` is de gedeelde lijst van gevonden-maar-nog-niet-
verifieerbare items; ook de diepe rondes lezen en schrijven die. Per item:
`kaart`, `titel`, `doi` of `url`, `reden` (bijvoorbeeld "geen PMID/abstract"),
`sinds` (JJJJ-MM-DD). Verwijder een item zodra het is toegevoegd of ouder dan 60
dagen en nog steeds niet indexeerbaar.
