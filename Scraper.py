
import requests
import mysql.connector
from bs4 import BeautifulSoup
from time import sleep
from random import randint

# Request URl
def scrape_items(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	items = soup.find_all(class_="products__item-link")
	all_items = []
	for item in items:
		item_data = (pavadinimo_gavimas(item),kainos_gavimas(item),tipo_gavimas(item))
		all_items.append(item_data)
		# sleep(randint(7,67))
	save_items(all_items)
	print(all_items)

# Duomenų išsaugojimas
def save_items(all_items):
	connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="$improver44",
        database="arbatos"
    )
	c = connection.cursor()
	# Sukuria table "Arbatos" tarp nurodytos duomenų bazės
	c.execute('''CREATE TABLE Arbatos 
		(Pavadinimas VARCHAR(255),Kaina FLOAT(4,2) NOT NULL,Tipas VARCHAR(255))''')
	c.executemany("INSERT INTO Arbatos VALUES (%s,%s,%s)", all_items)
	connection.commit()
	connection.close()

# pavadinimas
def pavadinimo_gavimas(item):
	pavadinimas = item.find("h2")
	return pavadinimas.string.strip()

# kaina
def kainos_gavimas(item):
	kaina = item.find("ins")
	kaina2 = kaina.string.replace("\xa0€","").replace(",",".")
	kaina_float = float(kaina2)
	return kaina_float

# tipas
def tipo_gavimas(item):
	pavadinimai = []
	tipas = item.find("h2")
	tipas2 = tipas.string.strip()
	pavadinimai.append(tipas2)
	for p in pavadinimai:
		if "Juodoji" in p or "juodoji" in p:
			return "Juodoji Arbata"
	return None

scrape_items("https://www.skonis-kvapas.lt/arbata/juodoji-arbata")