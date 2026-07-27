# Publiceren na akkoord

Dit is de werkwijze voor een onderhoudsronde die van Kenneth te horen krijgt welke
voorstellen erin mogen. De ronde publiceert zelf; hij uploadt niets.

## Wat je nodig hebt

Het publicatietoken staat in de opdracht van de geplande taak. Het geeft alleen
schrijfrechten op dit ene repo. Zet het nooit in een bestand dat je commit, en
herhaal het niet in je antwoord of in het overzicht.

## Belangrijk over de omgeving

`api.github.com` is in deze omgeving afgeschermd en antwoordt met een foutmelding
over `add_repo`. Git over https werkt wel. Gebruik dus git, nooit de GitHub API.
Ook `curl` naar willekeurige hosts is meestal geblokkeerd; gebruik WebFetch om te
controleren of een wijziging live staat.

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
7. Draai `node bouw-stubs.js` in de kloon en commit de gewijzigde bestanden mee.
   Dat werkt de vindbare pagina's per kaart, de sitemap en de wijzigingenlijst bij.
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

## Tekstwijzigingen aan de kaart

Een ronde mag ook de kaarttekst zelf voorstellen aan te passen: bl, de drie
regels van `pos`, `crit`, `results`, `lim` en `alts`. Dat gebeurt alleen als
Kenneth het nummer van dat tekstvoorstel heeft genoemd, en dan letterlijk zoals
voorgesteld, in beide talen. Pas de zin aan, herschrijf niet de hele alinea, en
laat elke wijziging steunen op een bron die in die ronde is opgehaald.

## Wat je niet doet

- Voorstellen opnemen die Kenneth niet heeft genoemd.
- Bestaande items of kaartteksten herschrijven zonder dat daar akkoord voor is.
- Iets publiceren waarvan de cijfers niet geverifieerd zijn.
