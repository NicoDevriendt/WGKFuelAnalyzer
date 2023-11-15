import os, csv, json
import configparser
import shutil

from Repositories import WGKFualCardAnalyzerRepo as repo
from Utils import configer 
from Models.transactie import Transactie

# Archiveren van een file naar de archive folder bepaald volgens de .config file.
# Params: folder: String Locatie van de file die men wenst te archiveren.
#         file: String Bestandnaam van de file die men wenst te archiveren.
def archiveerFile(folder,file):
    fullPathOfFile = os.path.join(folder,file)

    # Bepalen archive folder volgens de .config file.
    archiveFolder = os.path.join(os.getcwd(),configer.getConfig().get('TRANSACTION', 'ARCHIVE_FOLDER'))
    fullpathOfArchiveFile = os.path.join(archiveFolder,file)

    # Indien de file reeds bestaat in de archive folder, verwijder deze file.
    if os.path.isfile(fullpathOfArchiveFile) == True:
        try:
            os.remove(fullpathOfArchiveFile)
        except FileNotFoundError:
            # File is ondertussen verwijderd.
            pass
        except Exception as e:
            raise e
    try:
        # Verplaatsen van de verwerkte file naar de archive folder.
        shutil.move(fullPathOfFile, archiveFolder)
    except Exception as e:
        raise Exception(f"Fout bij het archiveren van een file {fullPathOfFile} \n {e}")

# Deze functie verwerkt een bestand.
# Dit betekent de tankkaart file inlezen en data wegschrijven in de Sqlite database.
# De nodige info verzamelen en omzetten in een JSON structuur die aangeboden wordt
# aan de software applicatie FleetWave die instaat voor het verdere beheer van het wagenpark.
# Params: folder: String Locatie van de file die men wenst te verwerken.
#         file: String Bestandnaam van de file die men wenst te verwerken.
def verwerkTransactieFile(folder,file):
    # Opmaken full path van de file die moet verwerkt worden.
    fullPathOfFile = os.path.join(folder,file)
    try:
        # Open de csv file
        with open(fullPathOfFile,'r',encoding="utf-8") as myTransactionFile:
            # Maak een csv reader.
            csvReader = csv.reader(myTransactionFile, delimiter=';')
            try:
                # Eerste lijn is een header die niet moet verwerkt worden
                header = str(next(csvReader))
                transactieDict = [];

                # Verwerk elke rij uit de CSV file
                for row in csvReader:
                    # Datum, tijd & kaartnummer wordt gebruikt om na te gaan of deze 
                    # registratie reeds aanwezig is in de database. Dubbele registraties moet
                    # vermeden worden.
                    datum_transactie = row[0]
                    tijd_transactie = row[1]
                    kaartnummer = int(row[2])
                    # Haal de transactie op met bijhorende datum, tijd & kaartnummer
                    transactie = repo.fetchOneTransactionByCardId(datum_transactie,tijd_transactie,kaartnummer)
                    # Indien transactie niet is gevonden, mag deze weggeschreven worden in de database en toegevoegd worden
                    # aan de lijst met transactie dictionary (die later wordt gebruikt om JSON file aan te maken)
                    if transactie == None:
                        objTransactie = __createTransactionObject(row)
                        repo.InsertCsvRecordToDB(objTransactie)
                        transactieDict.append(__convertDataRowToDictItem(row))
            except ValueError as err:
                raise Exception(f"Fout bij het verwerken van {fullPathOfFile}.\n Controleer de kolommen in het aanwezige bestand.\n Foutmelding: {err}")
            except Exception as e:
                raise Exception(f"Fout bij het verwerken van {fullPathOfFile}.\n Controleer de data in het aanwezige bestand. {e}")

    except FileNotFoundError as err:
        raise Exception(f"Kan bestand {fullPathOfFile} niet vinden tijdens het verwerkingsproces")
    except Exception as e:
        raise e

    # Maak een JSON string aan met de data die uit de file werd verwerkt in de database.
    jsonDataString = json.dumps(transactieDict, indent=4)

    # Bepaal de locatie voor de JSON files adhv de settings in de .config file.
    jsonFolder = os.path.join(os.getcwd(),configer.getConfig().get('TRANSACTION', 'JSON_FOLDER'))
    # De naam van de JSON file is hetzelfde bestandsnaam als het CSV bestand, maar dan met de extensie .JSON.
    fullpathOfJSONFile = os.path.join(jsonFolder,file.replace('.csv','.json'))
    try:
        # Schrijf de JSON file weg in de JSON folder.
        with open(fullpathOfJSONFile,'w') as myJsonFile:
            myJsonFile.write(jsonDataString)
    except Exception as e:
        raise e

# Data uit de database converten naar een dictionary item.
def __convertDataRowToDictItem(data):
        datum_transactie = data[0]
        tijd_transactie = data[1]
        autoId = data[11]
        kilometerstand = int(data[16])
        
        return { "autoId": autoId, "datum": datum_transactie, "tijd": tijd_transactie, "kilometerstand": kilometerstand}

# Creer a.d.h.v de doorgegeven data uit de csv file een Tankkaart object
def __createTransactionObject(data):
    datum_transactie = data[0]
    tijd_transactie = data[1]
    kaartnummer = int(data[2])
    adres = data[4]
    landcode = data[5]
    afdeling = data[9]
    autoId = data[14]
    kilometerstand = int(data[16])
    product = data[19]
    aantal_liter = abs(0.00 if data[20] == "" else float(data[20].replace(',','.')))
    off_prijs_l = 0.00 if data[24] == "" else float(data[24].replace(',','.'))
    korting_l = 0.00 if data[25] == "" else float(data[25].replace(',','.'))
    btwTarief = 0.00 if data[31] == "" else float(data[31].replace(',','.'))

    return Transactie(datum_transactie, tijd_transactie, kaartnummer, adres, landcode, afdeling, autoId, kilometerstand, product, aantal_liter, off_prijs_l, korting_l, btwTarief)
    
if __name__ == '__main__':
    pass