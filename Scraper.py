
import requests
import mysql.connector
from bs4 import BeautifulSoup
import json

# Request URl
# def scrape_items(url):
# 	response = requests.get(url)
# 	soup = BeautifulSoup(response.text, "html.parser")
# 	items = soup.find_all("arbata")
	# all_items = []
	# for item in items:
		# item_data = (get_title(item),get_price(item),get_type(item))
		# all_items.append(item_data)
	# save_items(all_items)

j_a = open("juodoji-arbata.html", encoding="utf-8")
soup = BeautifulSoup(j_a, "html.parser")

# # title
# title = soup.find_all("h2")
# parent = title[0].parent
# h2 = parent.find("h2")
# print(h2.string.strip())

# # kaina
# kaina = soup.find_all("ins")
# parent = kaina[0].parent
# ins = parent.find("ins")
# print(ins.string.strip())

# tipas
tipas = json.loads(soup.find("script", type="text/javascript").text)
print(tipas["articleBody"])



# def save_items(all_items):
# 	connection = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="$improver44",
#         database="arbatos"
#     )
# 	c = connection.cursor()
# 	c.execute('''CREATE TABLE Arbatos 
# 		(Pavadinimas TEXT,Kaina REAL,Tipas Text)''')
# 	c.executemany("INSERT INTO Arbatos VALUES (%s,%s,%s)", all_items)
# 	connection.commit()
# 	connection.close()
	
# def get_title(item):
# 	return item.find("h2").find("products_item-title")["title"]

# <h2 class="products__item-title">
#                 Juodoji arbata SKONIS IR KVAPAS DARJEELING FTGFOP1
#             </h2>

# def get_price(item):
# 	price = item.select(".price_color")[0].get_text()
# 	return price

# def get_type(item):
# 	ratings = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
# 	paragraph = book.select(".star-rating")[0]
# 	word = paragraph.get_attribute_list("class")[-1]
# 	return ratings[word]

# scrape_items("https://www.skonis-kvapas.lt/arbata/juodoji-arbata")