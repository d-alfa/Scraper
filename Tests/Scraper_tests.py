
import unittest
from bs4 import BeautifulSoup
import sys
sys.path.insert(1, "C:/Users/Alfonsas/OneDrive/Desktop/Python/Projektai/Scraper")
from Scraper import collecting_data, collecting_title, collecting_price#, collecting_type, page_usage

class Test_Collecting_Data(unittest.TestCase):

    # "Ensure that data is not None"
    def test_colecting_data_is_not_none(self):
        data = collecting_data("https://www.skonis-kvapas.lt/arbata/juodoji-arbata")
        self.assertIsNotNone(data)

    # "Each item must have 3 elements"
    def test_collecting_data_count(self):
        data = collecting_data("https://www.skonis-kvapas.lt/arbata/juodoji-arbata")
        for d in data:
            self.assertEqual(len(d),3)

    # "Each item must have a specific type"
    def test_collecting_data_type(self):
        data = collecting_data("https://www.skonis-kvapas.lt/arbata/juodoji-arbata")
        for d in data:
            self.assertIsInstance(d[0],str)
            self.assertIsInstance(d[1],float)
            self.assertIsInstance(d[2],str)

class Test_Collecting_Title(unittest.TestCase):

    # "Returns ValueError if there is no data inside <h2></h2>"
    def test_collecting_title_no_data(self):
        html_data ='<div class="products__item-link"><h2></h2></div>'
        soup = BeautifulSoup(html_data, "html.parser")
        with self.assertRaises(ValueError):
            collecting_title(soup)

    # "Returned data must be str"
    def test_collecting_title_str(self):
        html_data ='<div class="products__item-link"><h2>Title</h2></div>'
        soup = BeautifulSoup(html_data, "html.parser")
        title = collecting_title(soup)
        self.assertIsInstance(title,str)

class Test_Collecting_Price(unittest.TestCase):

    # Returns ValueError if there is no <ins></ins> brackets
    def test_collecting_price_no_ins(self):
        html_data = '<div class="products__item-link"></div>'
        soup = BeautifulSoup(html_data, "html.parser")
        with self.assertRaises(ValueError):
            collecting_price(soup)

    # Returns ValueError if there is no data inside <ins></ins>
    def test_collecting_price_no_data(self):
        html_data = '<div class="products__item-link"><ins></ins></div>'
        soup = BeautifulSoup(html_data, "html.parser")
        with self.assertRaises(ValueError) as error:
            collecting_price(soup)
        self.assertEqual(str(error.exception), "No Data inside <ins></ins>")

    # Function must return "float"
    def test_collecting_price_float(self):
        html_data = '<div class="products__item-link"><ins>3.99</ins></div>'
        soup = BeautifulSoup(html_data, "html.parser")
        price = collecting_price(soup)
        self.assertIsInstance(price,float)

if __name__== '__main__':
    unittest.main()