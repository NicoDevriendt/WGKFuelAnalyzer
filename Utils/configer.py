import configparser
import os

# Config file ophalen
def getConfig():
    # Controle alvorens de config file wordt gelezen, of de file aanwezig bestaat
    configFile = "WGKFuelAnalyzer.config"
    if os.path.isfile(configFile):
        config = configparser.ConfigParser()
        config.read(rf'{configFile}')  
        return config
    else:
        raise Exception("Fout: Kan config bestand WGKFuelAnalyzer.config niet vinden")

if __name__ == '__main__':
    pass