
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
	html_data = soup.find_all(class_="products__item-link")

	all_data = []
	for data in html_data:
		item_data = (collecting_title(data),collecting_price(data),collecting_type(data))
		all_data.append(item_data)
		# sleep(randint(7,67))

	saving_data(all_data)
	for a in all_data:
		print(a)

# Title
def collecting_title(data):
	title = data.find("h2")
	return title.string.strip()

# Price
def collecting_price(data):
	price = data.find("ins")
	price2 = price.string.replace("\xa0€","").replace(",",".")
	price_float = float(price2)
	return price_float

# Type
def collecting_type(data):
	types = []
	type = data.find("h2")
	type2 = type.string.strip()
	types.append(type2)
	for p in types:
		if "Juodoji" in p or "juodoji" in p:
			return "Juodoji Arbata"
		return None

# Takes pages from "Pages.py" prints them one by one and inserts them into function "collecting_data"
def page_usage():
	j_a_pages = juodoji_arbata_pages()
	for p in j_a_pages:
		print()
		print(f"Scraping Page: {p}")
		print()
		collecting_data(p)
		print()

# Saving data to SQL database
def saving_data(all_data):
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
	c.executemany("INSERT INTO Arbatos VALUES (%s,%s,%s)", all_data)
	connection.commit()
	connection.close()

page_usage()