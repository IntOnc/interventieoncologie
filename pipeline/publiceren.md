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
7. Meld in een kort bericht wat er gepubliceerd is en wat er niet in ging.

## Controles voor het pushen

- `content.json` is geldige JSON.
- Elk literatuuritem is een rij van precies vijf elementen:
  titel, "tijdschrift · jaar", url, samenvatting, sorteersleutel JJJJMM.
- De lijsten `guides`, `core`, `latest` en `ongoing` zijn per kaart even lang in
  `nl` en in `en`, en de items staan in dezelfde volgorde.
- Er staat nergens een em-dash of en-dash in nieuwe tekst.
- Elke nieuwe samenvatting bevat in het Resultaten-deel ten minste een getal,
  tenzij het om een richtlijnstandpunt of een lopende studie gaat.
- De sorteersleutel is een geheel getal van zes cijfers.

## Wat je niet doet

- Voorstellen opnemen die Kenneth niet heeft genoemd.
- Bestaande items herschrijven zonder dat daar akkoord voor is.
- Iets publiceren waarvan de cijfers niet geverifieerd zijn.
