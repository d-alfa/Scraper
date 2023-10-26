
import requests
import mysql.connector
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from Pages import juodoji_arbata_pages

# Collecting pages from Pages.py
def collecting_pages():
	collected_url = []
	j_a_pages = juodoji_arbata_pages()
	for url in j_a_pages:
		collected_url.append(url)
	return collected_url

# Uses pages from "collecting_pages" function and passes them to "collecting_data" function
def using_pages():
	collected_data = []
	collected_url = collecting_pages()
	for url in collected_url:
		collected_data.append(collecting_data(url))
	return collected_data

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
	return all_data

# Title
def collecting_title(data):
	title = data.find("h2")
	h2 = title.string
	if h2 == None:
		raise ValueError("No Data inside <h2></h2>")
	else:
		return h2.strip()

# Price
def collecting_price(data):
	price = data.find("ins")
	if price == None:
		raise ValueError("There is no <ins></ins> brackets")
	ins = price.string
	if ins == None:
		raise ValueError("No Data inside <ins></ins>")
	else:
		final_price = ins.replace("\xa0€","").replace(",",".").replace("€","")
		return float(final_price)

# Type
def collecting_type(data):
	p_type = data.find("h2")
	if p_type == None:
		raise ValueError("There is no <h2></h2> brackets")
	h2 = p_type.string
	if h2 == None:
		raise ValueError("No Data inside <h2></h2>")
	if "juodoji" in h2.strip().lower():
		return "Juodoji Arbata"

# Saving data to SQL database
def saving_data(item):
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

	# Inserts data into database
	c.executemany("INSERT INTO Arbatos VALUES (%s,%s,%s)", item)
	connection.commit()
	connection.close()

# Takes data from "using_pages" and passes it into "saving_data" function
def passing_data_into_saving_data():
	data = using_pages()
	for item in data:
		saving_data(item)

# Prints out collected Url and Data 
def printing_data():
	url_and_data = []
	pages = collecting_pages()
	data = using_pages()

	for url in pages:
		url_and_data.append([url])

	for i, item in enumerate(data):
		url_and_data.insert(i * 2 + 1, item)

	for item in url_and_data:
		for i in item:
			print(i)

	return url_and_data

passing_data_into_saving_data()
printing_data()