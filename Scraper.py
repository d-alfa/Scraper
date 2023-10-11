
import requests
import mysql.connector
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from Puslapiai import juodoji_arbata_puslapiai,j_a_puslapiai

# Informacijos rinkimas pagal Url
def duomenu_rinkimas(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	items = soup.find_all(class_="products__item-link")
	all_items = []
	for item in items:
		item_data = (pavadinimo_gavimas(item),kainos_gavimas(item),tipo_gavimas(item))
		all_items.append(item_data)
		# sleep(randint(7,67))
	duomenu_išsaugojimas(all_items)
	print(all_items)

# Duomenų išsaugojimas
def duomenu_išsaugojimas(all_items):
	connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="$improver44",
        database="arbatos"
    )
	c = connection.cursor()

	# Sukuria table "Arbatos" tarp nurodytos duomenų bazės
	# c.execute('''CREATE TABLE Arbatos 
	# 	(Pavadinimas VARCHAR(255),Kaina FLOAT(4,2) NOT NULL,Tipas VARCHAR(255))''')

	# Perkelia duomenis į duomenų baze
	c.executemany("INSERT INTO Arbatos VALUES (%s,%s,%s)", all_items)
	connection.commit()
	connection.close()

# Pavadinimas
def pavadinimo_gavimas(item):
	pavadinimas = item.find("h2")
	return pavadinimas.string.strip()

# Kaina
def kainos_gavimas(item):
	kaina = item.find("ins")
	kaina2 = kaina.string.replace("\xa0€","").replace(",",".")
	kaina_float = float(kaina2)
	return kaina_float

# Tipas
def tipo_gavimas(item):
	pavadinimai = []
	tipas = item.find("h2")
	tipas2 = tipas.string.strip()
	pavadinimai.append(tipas2)
	for p in pavadinimai:
		if "Juodoji" in p or "juodoji" in p:
			return "Juodoji Arbata"
		return None
	
# Paima kiekviena elementa atskirai, ir panaudoja jį tarp funckijos "duomenu_rinkimas"
juodoji_arbata_puslapiai()
for p in j_a_puslapiai:
	print(f"Scraping Puslapis: {p}")
	print()
	duomenu_rinkimas(p)
	print()