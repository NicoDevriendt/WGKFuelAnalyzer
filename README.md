# WGKFuelAnalyzer
Analyseren van het gebruik van tankkaarten
Binnen het Wit Gele Kruis heeft elke medewerker met een dienstwagen / bedrijfswagen
een tankkaart ter beschikking.
Periodiek krijgt de organisatie een overzicht van de uitgevoerde tankbeurten.
Dit zijn lijsten in een CSV bestand die verwerkt moeten worden & waarop men enkele overzichten
wenst te maken.

Het opstarten van de applicatie gebeurt via het commando
python WGKFuelCardAnalyzer.py

Vervolgens komt men in een menu structuur terecht waaraan de gebruiker wordt
gevraagd welke actie men wenst uit te voeren

1. Import tankkaart files: 
   Via deze menu worden de CSV files ingelezen in de database
   en vervolgens gearchiveerd.
   Het Wit Gele Kruis gebruikt FleetWave voor het beheer van het wagenpark
   Via een JSON file wenst men de kilometerstand door te geven aan FleetWave
   Via de WGKFuelAnalyzer.config file worden de correcte folders uitgelezen alsook
   de locatie van de database.
2. Kostprijs per afdeling:
   Het Wit Gele Kruis bestaat uit verschillende afdelingen
   Men wenst een uitgave overzicht te hebben voor elke afdeling.
   Naast een oplijsting in een tabel, worden ook de gegevens visueel via een staafdiagram 
   en taartdiagram weergegeven
3. Niet toegelaten product:
   De organisatie wenst dat elke medewerker Euro 95 tankt.
   Via deze lijst wenst men een overzicht te krijgen welke tankbeurten een ander 
   product hebben getankt.
4. Niet toegelaten product (export Excel):
   Idem als optie 3, maar de gegevens worden geexporteerd naar Excel
5. Kostprijsevolutie:
   Per maand in een opgegeven kalenderjaar: de evolutie zien van de brandstof uitgaven
6. Km stand opvragen:
   Kilomterstand opvragen uit de database van een transactie op een bepaalde datum, tijd & kaartnummer
7. Km stand wijzigen:
   Tijdens elke tankbeurt moet een medewerker de kilometers opgeven op de terminal in het tankstation.
   De medewerker kan een fout maken.
   Via deze optie kan men deze fout corrigeren


Notitie:

In de databank is er slechts één bestand aanwezig nl bestand met de transacties
Omwille van de GDPR wetgeving heb ik het bestand die de koppeling met de medewerkers
via cardId & bestand die de koppeling met de wagen via autoId niet kunnen gebruiken
voor deze opdracht.

