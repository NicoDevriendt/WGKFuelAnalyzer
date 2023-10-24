import os, csv, sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from Repositories import WGKFualCardAnalyzerRepo as repo
from Controllers import WGKFuelAnalyzerController as controller
from Utils import configer 

# Bij opstart van de applicatie wordt een menu item weergegeven aan de gebruiker
# Na uitvoeren van een menu item, komt men steeds terug naar dit menu
# Via de menu keuze 99 kan men het menu verlaten, en stopt het programma.
def startup():
    answer = ""
    while (answer != "99"):
        try:
            # clear de output van de terminal, zodat we de informatie in de terminal overzichtelijk
            # houden.
            os.system('cls')
            answer = input("""Welke optie wenst je uit te voeren \n
                1. Import tankkaart files \n
                2. Kostprijs per afdeling \n
                3. Niet toegelaten product \n
                4. Niet toegelaten producten (export Excel) \n
                5. Kostprijsevolutie \n
                6. Km stand opvragen \n
                7. Km stand wijzigen \n
                99. Stoppen \n 
                Uw keuze: """)
            if answer == "1":
                importNewFiles()
            elif answer == "2":
                kostprijsPerAfdeling()
            elif answer == "3":
                nietToegelatenProduct()
            elif answer == "4":
                exportNietToegelatenProductenToExcel()
            elif answer == "5":
                kostprijsEvolutie()
            elif answer == "6":
                getKilometerstand()
            elif answer == "7":
                updateKilometerstand()
            elif answer == "99":
                pass
            else:
                print("Foutieve keuze !!")
        except Exception as e:
            print(f"Er is een fout gebeurt tijdens de verwerking \n {e}")
            __pressKeyToContinue()

# Importeren van de files die in de IN folder staan.
# Enkel CSV files worden verwerkt.
def importNewFiles():
    # Bepaal de locatie van de IN folder
    inFolder = os.path.join(os.getcwd(),configer.getConfig().get('TRANSACTION', 'IN_FOLDER'))
    try:
        with os.scandir(inFolder) as entries:
            for entry in entries:
                if (entry.name.endswith('csv')):
                    # Verwerken van de file in de database en aanmaak JSON file voor integratie met externe software.
                    print(f"Bezig met file {entry.name} aan het verwerken")
                    controller.verwerkTransactieFile(inFolder,entry.name)
                    # Na het verwerken van de file, wordt de file gearchiveerd naar de EXPORT folder.
                    print(f"Bezig met archiveren {entry.name}")
                    controller.archiveerFile(inFolder, entry.name)
                else:
                    print(f"{entry.name} is niet in een CSV formaat")
            print("Verwerking voltooid")
            __pressKeyToContinue()
    except Exception as err:
        raise Exception(f"Fout bij het lezen van de foler { inFolder } \n {err}")

# Deze functie geeft een overzicht van de kosten per afdeling voor een opgegeven periode.
# Het maakt een vergelijk mogelijk tussen de totale kosten per afdeling en wordt naast 
# een tabel, alsook weergegeven in een staafdiagram en taartdiagram.
def kostprijsPerAfdeling():
    # Opvragen van de begin & einddatum.
    start, einde = __askDateRange()

    # Ophalen van de uitgaven gegroepeerd per afdeling uit de database tussen de opgegeven begin en einddatum.
    kostenPerAfdeling = repo.fetchKostprijsPerAfdeling(start, einde)

    # Indien er geen transacties zijn, wordt een melding weergegeven aan de gebruiker.
    if len(kostenPerAfdeling) == 0:
        raise Exception(f"Geen transacties gevonden binnen de periode " + __convertDateRangeToString(start,einde))
    
    # Voor elke afdeling wordt de overeenkomstige uitgave vermeld     
    for afdeling in kostenPerAfdeling:
        col1 = "{:<20}".format(afdeling[0]) if afdeling[0] != "" else "Niet toegewezen"
        col2 = "{:>10}".format(afdeling[1])
        print(f"{col1} \t {col2}")

    npArray = __convertDbResultToTransposedNpArray(kostenPerAfdeling)
    if npArray.size != 0:
        afdelingen = npArray[0]
        afdelingen = np.where(afdelingen == "", "Niet\ntoegewezen", afdelingen)
        uitgaven = np.asarray(npArray[1], dtype=float)
        plotTitle = f"Brandstof uitgaven per afdeling " +  __convertDateRangeToString(start,einde)

        # Aanmaak van de staafdiagram
        plt.subplot(2,1,1)
        plt.bar(afdelingen, uitgaven)
        plt.title(plotTitle)
        plt.xlabel("Afdelingen")
        plt.ylabel("Uitgave")
        plt.grid()
        
        # Aanmaak van de taardiagram
        plt.subplot(2,1,2)
        plt.pie(uitgaven, labels=afdelingen)
        plt.legend(bbox_to_anchor=(1.55,1.025),loc="upper left")
        plt.show()
    else:
        print(f"Geen transacties gevonden binnen de periode " + __convertDateRangeToString(start,einde))

# De organisatie wenst niet langer dat medewerkers andere brandstof tanken met de tankkaart dan Euro 95
# Met deze functie wordt een overzicht gegeven van datum, tijd, kaarnummer, id van de auto & welk product
# er werd getankt buiten Euro 95 voor de gevraagde periode.        
def nietToegelatenProduct():
    # Opvragen van de begin & einddatum.
    start, einde = __askDateRange()

    # Ophalen van alle transacties binnen de opgegeven begin & einddatum, waarvan het product 
    # verschillend is van Euro 95
    transacties = repo.fetchNotAllowedTransactions(start,einde)
    headerCol1 = "{:<10}".format("Datum")
    headerCol2 = "{:<5}".format("Tijd")
    headerCol3 = "{:<20}".format("kaartnummer")
    headerCol4 = "{:<10}".format("autoId")
    headerCol5 = "{:<30}".format("product")
    print(f"{headerCol1} \t {headerCol2} \t {headerCol3} \t {headerCol4} \t {headerCol5} \t")
    for transactie in transacties:
        col1 = "{:<10}".format(transactie[0])
        col2 = "{:<5}".format(transactie[1])
        col3 = "{:<20}".format(transactie[2])
        col4 = "{:<10}".format(transactie[3])
        col5 = "{:<30}".format(transactie[4])
        print(f"{col1} \t {col2} \t {col3} \t {col4} \t {col5} \t")
    print(f"Totaal aantal transacties: { len(transacties) }")
    __pressKeyToContinue()

# Export naar Excel van producten die niet langer toegelaten zijn bij gebruik van de tank kaart door 
# de organisatie. Enkel Euro 95 is nog toegelaten.
# De excel file komt terecht in de EXPORT folder die terug te vinden is in de .config file
# De naam is vrij te kiezen door de gebruiker, maar moet wel eindigen extensie .xlsx
def exportNietToegelatenProductenToExcel():
    # Naam van de excel export file.
    file_name = input("Naam van de export file (eindigen met extensie .xlsx) : ")

    # Controle of de naam bestaand uit een bestandsnaam & eindigt met de extensie .xlsx
    file_parts = file_name.split('.')
    if (len(file_parts) != 2 or (len(file_parts) == 2 and file_parts[-1].lower() != 'xlsx')):
        raise Exception("Fout: Benaming export file niet correct !")
    
    # Opvragen van de begin & einddatum.
    start, einde = __askDateRange()

    # Via pandas wordt een dataframe opgehaald die alle transacties bevat waarvan het aangekochte product
    # niet toegelaten is, binnen de opgegeven periode. 
    transacties = repo.fetchDfWithNotAllowedTransactions(start,einde)

    # Export file wordt samen gesteld volgens de ingegeven locatie en de EXPORT locatie volgens de settings file.
    exportFile = os.path.join(os.getcwd(),configer.getConfig().get('TRANSACTION', 'EXPORT_FOLDER'),file_name)
    try:
        # Dataframe wordt omgezet naar een excel file.
        transacties.to_excel(exportFile, sheet_name="transacties", index=False)
    except Exception as err:
        raise Exception(f"Er is een fout gebeurd tijdens het exporteren \n {err}")

    print(f"Export is uitgevoerd naar { exportFile }")
    __pressKeyToContinue()

# Functie geeft een grafisch overzicht van de maandelijkse evolutie van de algemene uitgaven met de tankaarten 
# binnen een opgegeven kalenderjaar.
def kostprijsEvolutie():
    jaar = input("Geef het jaar in:")
    # Ophalen van de totale uitgaven gegroepeerd op maand van het opgegeven kalenderjaar.
    evolutie = repo.fetchKostprijsEvolutie(jaar)

    npArray = __convertDbResultToTransposedNpArray(evolutie)
    if npArray.size != 0 :
        maanden = npArray[0]
        kostprijsAfdelingen = np.asarray(npArray[1], dtype=float)
        
        plt.plot(maanden,kostprijsAfdelingen,color="red", linewidth='2')
        plt.xlabel(f"maanden voor {jaar}")
        plt.ylabel("uitgave")
        plt.title("evolutie brandstof uitgaven")
        plt.show()
    else:
        print(f"Geen transacties gevonden voor het jaar {jaar}")
        __pressKeyToContinue()

# Opvragen van de kilometerstand die door een medewerker werd ingevoerd op een bepaalde datum, tijdstip &
# gebruikte kaart.
def getKilometerstand():
    # Opvragen van datum,tijd & id van de gebruikte kaart.
    datum = input("Geef het datum in (DD/MM/YYYY):")
    tijd = input("Geef het tijdstip in (HH:MI):")
    cardId = input("Geef het kaartnummer van de tank kaart:")

    # Transactie opvragen in de database
    transaction = repo.fetchOneTransactionByCardId(datum,tijd,cardId)
    if transaction != None:
        print(f"Op datum {transaction[0]} {transaction[1]} werd met kaartnummer {transaction[2]} : {transaction[3]} km geregistreerd")
    else:
        print("Transactie werd niet gevonden !")
    
    __pressKeyToContinue()
    return transaction

# Deze functie maakt het mogelijk om een kilometerstand te wijzigen van een geregistreerde transactie.
# vb Bij input foutieve km stand tijdens de tankbeurt
# Na het opvragen van de datum , tijd & id van de kaart wordt de huidige kilometerstand opgevraagd en 
# indien de transactie gevonden wordt, kan deze aangepast worden door de gebruiker.
def updateKilometerstand():
    # Opgevragen huidige kilometerstand
    transaction = getKilometerstand() 

    if transaction != None:
        # Indien er een transactie gevonden is, bevraag de nieuwe km stand en voer de gewijzigde stand door in de database.
        nieuwe_km = input("Wat is de nieuwe km stand ? :")
        transaction = repo.updateOneTransactionByCardId(transaction[0] ,transaction[1],transaction[2],int(nieuwe_km))
        print("Kilometerstand werd gewijzigd")
        __pressKeyToContinue()

# Helper functie om array om te zetten naar een numpy array & dimensies omkeren
# Params: List
# Return: Numpy array object
def __convertDbResultToTransposedNpArray(array):
    npArray = np.array(array)
    return npArray.transpose()

# Helper functie om date range op te vragen bij de gebruiker en verifiëren of de datum werd ingevoerd
# in het formaat DD/MM/YYYY
# Return: tuple (DateTime,DateTime) 
def __askDateRange():
    begindatum = input("Vanaf welke datum formaat DD/MM/YYYY:")
    try:
        start = datetime.strptime(begindatum,"%d/%m/%Y")
    except ValueError as err:
        raise Exception(f"Ongeldige startdatum: {err}")

    einddatum = input("Tot welke datum formaat DD/MM/YYYY:")
    try:
        einde = datetime.strptime(einddatum,"%d/%m/%Y")
    except ValueError as err:
        raise Exception(f"Ongeldige startdatum: {err}")
        
    return(start,einde)

# Helper functie om gebruiker toets te laten indrukken om programma verder te laten lopen
def __pressKeyToContinue():
    input("Druk op een toets om verder te gaan...")

# Helper functie die een date range terug geeft in een string.
# Params: start: DateTime
#         einde: DateTime
# Return: string
def __convertDateRangeToString(start,einde):
    return f"{start.strftime('%d/%m/%Y')} - {einde.strftime('%d/%m/%Y')}"

if __name__ == '__main__':
    pass