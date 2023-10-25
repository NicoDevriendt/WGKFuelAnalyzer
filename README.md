# WGKFuelAnalyzer
Algemeen:
Onderwerp:Analyseren van het gebruik van tankkaarten
Beschrijving onderwerp:
Binnen het Wit Gele Kruis heeft elke medewerker met een dienstwagen / bedrijfswagen &
een tankkaart ter beschikking.
Periodiek krijgt de organisatie een overzicht van de uitgevoerde tankbeurten.
Deze lijsten worden in een CSV bestand aangeleverd, die verwerkt moeten worden 
& waarop men enkele overzichten wenst te maken.

Installation Requirements:
Python versie >= 3.8

Startup commando:
python WGKFuelCardAnalyzer.py

Configuration file:
Het bestand met de instellingen moet in de root folder komen van de applicatie 
en moet volgende naam hebben: WGKFuelAnalyzer.config

Binnen deze config file zijn twee sections aanwezig nl global & TRANSACTION
In de sectie global moet er een keyword DATABASE aanwezig zijn met het volledige
pad (inclusief bestandsnaam) van de Sqlite db file.

In de sectie TRANSACTION zijn er 4 parameters:
 
IN_FOLDER = Locatie waar de files terecht komen die moeten verwerkt worden door het programma.
ARCHIVE_FOLDER = Locatie waar de files terecht komen die reeds verwerkt zijn, en gearchiveerd worden.
JSON_FOLDER = Na verwerking van een file uit de IN_FOLDER worden bepaalde data omgezet naar JSON structuur
              voor verdere verwerking in extern pakket omtrent wagenpark beheer.
              Deze files komen terecht in de folder die hier gespecificeerd wordt.
EXPORT_FOLDER = Folder waarin de gevraagde exports van overzichten (Excel) in terecht komen.

Belangrijk: Geef je enkel een naam van een folder, worden deze folders aangemaakt in je huidige directory.

Handleiding:

Vervolgens komt men in een menu structuur terecht waaraan de gebruiker wordt
gevraagd welke actie men wenst uit te voeren
Stoppen van het programma gebeurt met de optie 99

1. Import tankkaart files: 
   Via deze menu worden de CSV files ingelezen in de database
   en vervolgens gearchiveerd.
   Het Wit Gele Kruis gebruikt FleetWave voor het beheer van het wagenpark.
   Via een JSON file wenst men de kilometerstand door te geven aan FleetWave.
   Via de WGKFuelAnalyzer.config file worden de correcte folders uitgelezen alsook
   de locatie van de database.
2. Kostprijs per afdeling:
   Het Wit Gele Kruis bestaat uit verschillende afdelingen.
   Men wenst een uitgave overzicht te hebben voor elke afdeling.
   Naast een oplijsting in een tabel, worden ook de gegevens visueel via een staafdiagram 
   en taartdiagram weergegeven.
3. Niet toegelaten product:
   De organisatie wenst dat elke medewerker Euro 95 tankt.
   Via deze lijst wenst men een overzicht te krijgen welke tankbeurten een ander 
   product hebben getankt.
4. Niet toegelaten product (export Excel):
   Idem als optie 3, maar de gegevens worden geexporteerd naar Excel.
5. Kostprijsevolutie:
   Per maand in een opgegeven kalenderjaar: de evolutie zien van de brandstof uitgaven.
6. Km stand opvragen:
   Kilomterstand opvragen uit de database van een transactie op een bepaalde datum, tijd & kaartnummer.
7. Km stand wijzigen:
   Tijdens elke tankbeurt moet een medewerker de kilometers opgeven aan de terminal in het tankstation.
   De medewerker kan een fout maken.
   Via deze optie kan men deze fout corrigeren
8. Statistische gegevens:
   Levert statistische gegevens omtrent Officiële prijzen, Verkregen koringen, liters brandstof, totaal bedrag
   voor een opgegeven kalenderjaar 



Opmerking:

In de databank is er slechts één bestand aanwezig nl bestand met de transacties
Omwille van de GDPR wetgeving heb ik het bestand die de koppeling met de medewerkers
via cardId & bestand die de koppeling met de wagens via autoId niet kunnen gebruiken
voor deze opdracht.


