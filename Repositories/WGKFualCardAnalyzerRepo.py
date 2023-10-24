import sqlite3
import pandas as pd

from Utils import configer 

# Deze functie bepaalt de database file via de .config file
# en maakt vervolgens een connectie met de database.
def __createDBConnection():
    try:
        db_name = configer.getConfig().get('global', 'DATABASE')
        return sqlite3.connect(db_name)
    except Exception as err:
        raise Exception(f"Fout bij het maken van een connectie naar de database \n {err}")

# Ophalen van een totale uitgave gegroepeerd op afdeling, binnen de opgegeven begindatum en einddatum
# Params begindatum: DateTime
#        einddatum: DateTime
# Return tuple list
def fetchKostprijsPerAfdeling(begindatum, einddatum):
    with __createDBConnection() as dbconnectie:
        myCursor = dbconnectie.cursor()
        query = """
            select afdeling, round(sum((officiële_prijs_liter - korting_liter) * aantal_liter),2)
            from transacties
            where date(substr(datum,7,4) ||  '-'  || substr(datum,4,2) ||  '-' || substr(datum,1,2))  between date(?) and date(?) 
            group by afdeling
             """
        convertedStartDate = f"{begindatum.year}-{__convert2Leading0(begindatum.month)}-{__convert2Leading0(begindatum.day)}"
        convertedEndDate = f"{einddatum.year}-{__convert2Leading0(einddatum.month)}-{__convert2Leading0(einddatum.day)}"

        parameters = (convertedStartDate, convertedEndDate)
        myCursor.execute(query,parameters)
        
        transacties = myCursor.fetchall()
    return transacties

# Ophalen van een totale kostprijs per maand binnen een opgegeven kalenderjaar.
# Params jaar: Integer
# Return tuple list
def fetchKostprijsEvolutie(jaar):
	with __createDBConnection() as dbconnectie:
		myCursor = dbconnectie.cursor()
		query = """
		select substr(datum,4,2) as maand, round(sum((officiële_prijs_liter - korting_liter) * aantal_liter),2) 
		from transacties where substr(datum,7,4) 
		LIKE ? group by substr(datum,4,2)
		"""
		myCursor.execute(query,[jaar])
		transacties = myCursor.fetchall()
	return transacties

# Ophalen van alle transacties die brandstof hebben getankt die niet toegelaten is door de organisatie.
# Params begindatum: DateTime
#        einddatum: DateTime
# Return tuple list
def fetchNotAllowedTransactions(begindatum, einddatum):
	with __createDBConnection() as dbconnectie:
		myCursor = dbconnectie.cursor()
        # Query & parameters worden samengesteld via een private function
		query, parameters = __getSQLNotAllowedTransactions(begindatum,einddatum)
		myCursor.execute(query,parameters)
        
		transacties = myCursor.fetchall()
	return transacties

# Ophalen van alle transacties in een dataframe die brandstof hebben getankt die niet toegelaten is door de organisatie.
# Params begindatum: DateTime
#        einddatum: DateTime
# Return dataframe
def fetchDfWithNotAllowedTransactions(begindatum,einddatum):
    with __createDBConnection() as dbconnectie:
        # Query & parameters worden samengesteld via een private function
        query, parameters = __getSQLNotAllowedTransactions(begindatum,einddatum)
        transacties = pd.read_sql_query(query,dbconnectie, params=parameters)
    return transacties

# Ophalen van een transactie volgens een gegeven datum, tijd & kaartnummer
# Params datum: String
#        tijd: String
#        cardId: String
# Return tuple
def fetchOneTransactionByCardId(datum,tijd,cardId):
    with __createDBConnection() as dbconnectie:
        myCursor = dbconnectie.cursor()
        query = """
            select datum,tijd, kaartnummer, kilometerstand
            from transacties
            where datum = ? and tijd= ? and kaartnummer = ?
            """
        parameters = (datum, tijd,cardId)
        myCursor.execute(query,parameters)
        
        transactie = myCursor.fetchone()
        
    return transactie

# Kilometerstand wijzigen van een transactie op een bepaalde datum, tijdstip, cardid
# Params datum: String
#        tijd: String
#        cardId: String
#        kilometerstand: Integer
# Return tuple
def updateOneTransactionByCardId(datum,tijd,cardId,kilometerstand):
    with __createDBConnection() as dbconnectie:
        myCursor = dbconnectie.cursor()
        query = """
            update transacties
            set kilometerstand = ?
            where datum = ? and tijd= ? and kaartnummer = ?
            """
        parameters = (kilometerstand,datum, tijd,cardId)

        myCursor.execute(query,parameters)
        
    dbconnectie.commit;

# CSV data wegschrijven in de database
# Params: data: List
def InsertCsvRecordToDB(objTankKaart):
    with __createDBConnection() as dbconnectie:
        datum_transactie = objTankKaart.get_Datum()
        tijd_transactie = objTankKaart.get_Tijd()
        kaartnummer = objTankKaart.get_CardId()
        adres = objTankKaart.get_Adres()
        landcode = objTankKaart.get_Landcode()
        afdeling = objTankKaart.get_Afdeling()
        autoId = objTankKaart.get_AutoId()
        kilometerstand = objTankKaart.get_Kilometerstand()
        product = objTankKaart.get_Product()
        aantal_liter = objTankKaart.get_AantalLiter()
        off_prijs_l = objTankKaart.get_OffPrijsL()
        korting_l = objTankKaart.get_KortingL()
        btwTarief = objTankKaart.get_btwTarief()
        
        myCursor = dbconnectie.cursor()
        query = """
             INSERT INTO transacties(datum, tijd, kaartnummer, adres, landcode, afdeling, autoId, kilometerstand,product, aantal_liter, officiële_prijs_liter, korting_liter, btw_tarief)
             values (?,?,?,?,?,?,?,?,?,?,?,?,?)
             """
        parameters = (datum_transactie,tijd_transactie,kaartnummer,adres,landcode,afdeling,autoId,kilometerstand,product,aantal_liter,off_prijs_l,korting_l,btwTarief)
       
        myCursor.execute(query,parameters)
        dbconnectie.commit()

# Query & parameters samenstellen voor transacties op te halen waarbij producten zijn getankt die niet toegelaten zijn door
# de organisatie
# Params begindatum: DateTime
#        einddatum: DateTime
# Return tuple
def __getSQLNotAllowedTransactions(begindatum, einddatum):
    query = """
            select datum,tijd, kaartnummer,autoid,product
            from transacties
            where product <> 'EURO 95' and date(substr(datum,7,4) ||  '-'  || substr(datum,4,2) ||  '-' || substr(datum,1,2))  between date(?) and date(?) 
            order by date(substr(datum,7,4) ||  '-'  || substr(datum,4,2) ||  '-' || substr(datum,1,2))
            """
    convertedStartDate = f"{begindatum.year}-{__convert2Leading0(begindatum.month)}-{__convert2Leading0(begindatum.day)}"
    convertedEndDate = f"{einddatum.year}-{__convert2Leading0(einddatum.month)}-{__convert2Leading0(einddatum.day)}"

    parameters = (convertedStartDate, convertedEndDate)

    return (query,parameters)

# Conversie van een getal waarde zodat deze uit twee posities bestaat
# wordt gebruikt om dag en maand te converteren naar 01,02,...
# Params: waarde: String
# Return String
def __convert2Leading0(waarde):
    return f"{'{:02d}'.format(waarde)}"

if __name__ == '__main__':
	pass