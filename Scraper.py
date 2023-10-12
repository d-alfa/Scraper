
import requests
import mysql.connector
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from Pages import juodoji_arbata_pages

# Collecting data from provided Url
def collecting_data(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	items = soup.find_all(class_="products__item-link")
	all_items = []
	for item in items:
		item_data = (collecting_title(item),collecting_price(item),collecting_type(item))
		all_items.append(item_data)
		# sleep(randint(7,67))
	saving_data(all_items)
	for a in all_items:
		print(a)

# Saving data to SQL database
def saving_data(all_items):
	connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="$improver44",
        database="arbatos"
    )
	c = connection.cursor()
	# Creates table "Arbatos" inside SQL database
	# c.execute('''CREATE TABLE Arbatos 
	# 	(Title VARCHAR(255),Price FLOAT(4,2) NOT NULL,Type VARCHAR(255))''')

	# Inserts data to database
	c.executemany("INSERT INTO Arbatos VALUES (%s,%s,%s)", all_items)
	connection.commit()
	connection.close()

# Title
def collecting_title(item):
	title = item.find("h2")
	return title.string.strip()

# Price
def collecting_price(item):
	price = item.find("ins")
	price2 = price.string.replace("\xa0€","").replace(",",".")
	price_float = float(price2)
	return price_float

# Type
def collecting_type(item):
	types = []
	type = item.find("h2")
	type2 = type.string.strip()
	types.append(type2)
	for p in types:
		if "Juodoji" in p or "juodoji" in p:
			return "Juodoji Arbata"
		return None
	
# Takes pages from "Pages.py" prints them one by one and inserts them into function "collecting_data"
def pages_usage():
	j_a_pages = juodoji_arbata_pages()
	for p in j_a_pages:
		print(f"Scraping Page: {p}")
		print()
		collecting_data(p)
		print()

pages_usage()