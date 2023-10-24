class Transactie:
	def __init__(self, datum, tijd, cardId, adres, landcode, afdeling, autoId, kilometerstand, product, aantalLiter, offPrijsL, kortingL, btwTarief):
		self.__datum = datum
		self.__tijd = tijd
		self.__cardId = cardId
		self.__adres = adres
		self.__landcode = landcode
		self.__afdeling = afdeling
		self.__autoId = autoId
		self.__kilometerstand = kilometerstand
		self.__product = product
		self.__aantalLiter = aantalLiter
		self.__offPrijsL = offPrijsL
		self.__kortingL = kortingL
		self.__btwTarief = btwTarief
	def get_Datum(self):
		return self.__datum

	def get_Tijd(self):
		return self.__tijd

	def get_CardId(self):
		return self.__cardId

	def get_Adres(self):
		return self.__adres

	def get_Landcode(self):
		return self.__landcode

	def get_Afdeling(self):
		return self.__afdeling

	def get_AutoId(self):
		return self.__autoId

	def get_Kilometerstand(self):
		return self.__kilometerstand

	def get_Product(self):
		return self.__product

	def get_AantalLiter(self):
		return self.__aantalLiter

	def get_OffPrijsL(self):
		return self.__offPrijsL

	def get_KortingL(self):
		return self.__kortingL

	def get_btwTarief(self):
		return self.__btwTarief
