import os, sys

from UI import WGKFuelCardAnalyzeViewer as view
from Utils import configer 

try:
    config = configer.getConfig()
except Exception as err:
    print(err)
    sys.exit(1)

# Controleren van de configuratie file
# De Sqlite databank moet aanwezig zijn die geconfigureerd is in de .config file.
# Maak de nodige folder aan IN, ARCHIVE, JSON om brandstof transactie files te 
# verwerken
# Maak de nodige EXPORT folder aan die gebruikt wordt om data te exporteren (naar Excel) 
def __checkConfigSettings():
    # Controle of de file WGKFuelAnalyzer.config bestaat
    if os.path.isfile('WGKFuelAnalyzer.config'):
        config.read(r'WGKFuelAnalyzer.config')
    else:
        print("Fout Kan config bestand WGKFuelAnalyzer.config niet vinden")
        sys.exit(1)
    
    # Haal de naam van de database op & controleer of deze aanwezig is op de aangegeven locatie.
    db_file = config.get('global', 'DATABASE')
    if os.path.isfile(db_file) == False:
        print(f"FOUT: Database file bestaat niet : {db_file}")
        sys.exit(1)

    # Samenstellen van de locatie van de IN, ARCHIVE, JSON & EXPORT folder
    # Indien nodig worden deze folders aangemaakt.
    inFolder = __composeFolder('IN_FOLDER')
    __makeTransactionFolder(inFolder)

    archiveFolder = __composeFolder('ARCHIVE_FOLDER')
    __makeTransactionFolder(archiveFolder)

    jsonFolder = __composeFolder('JSON_FOLDER')
    __makeTransactionFolder(jsonFolder)

    exportFolder = __composeFolder('EXPORT_FOLDER')
    __makeTransactionFolder(exportFolder)

# Haal de corresponderende folder key uit de TRANSACTION setting uit de config file.
# Indien enkel een foldernaam is gespecificeerd zonder pad, wordt de huidige directory gebruikt
# als pad.
def __composeFolder(folderNameKey):
    try:
        folder = config.get('TRANSACTION', folderNameKey)
        return os.path.join(os.getcwd(),config.get('TRANSACTION', folderNameKey))
    except configparser.NoOptionError: 
        print(f"Fout: Key {folderNameKey} bestaat niet in de configuratiefile")
        sys.exit(1)

# Maak de folder aan indien deze nog niet bestaat.
def __makeTransactionFolder(folder):
    if os.path.isdir(folder) == False:
        try:
            os.mkdir(folder)
        except FileNotFoundError as err:
            parentDir= os.path.abspath(os.path.join(folder, os.pardir))
            print(f"FOUT ! Transaction folder kan niet aangemaakt worden. Controleer of de folder {parentDir} bestaat")
            sys.exit(1)

if __name__ == '__main__':
    # Vooraleer de applicatie wordt opgesteld, wordt de nodige configuratie settings gecontroleerd.
    __checkConfigSettings()
    view.startup()
