
import unittest
import mysql.connector
from bs4 import BeautifulSoup
import sys
sys.path.insert(1, "C:/Users/Alfonsas/OneDrive/Desktop/Python/Projektai/Scraper")
from Scraper import collecting_data, collecting_title, collecting_price, collecting_type, collecting_pages, using_pages, printing_data, saving_data

class Test_Collecting_Pages(unittest.TestCase):

    # Function must return certain url's
    def test_collecting_pages_j_a_pages(self):
        current_pages = collecting_pages()
        expected_pages = [
            "https://www.skonis-kvapas.lt/arbata/juodoji-arbata?page=1",
            "https://www.skonis-kvapas.lt/arbata/juodoji-arbata?page=2",
            "https://www.skonis-kvapas.lt/arbata/juodoji-arbata?page=3",
        ]
        self.assertEqual(current_pages,expected_pages)

    # Function must return 3 different url
    def test_collecting_pages_j_a_pages_len(self):
        current_pages = collecting_pages()
        self.assertEqual(len(current_pages),3)

class Test_Using_Pages(unittest.TestCase):

    # Data from using_pages can't be None
    def test_using_pages_data_is_not_None(self):
        collected_data = using_pages()
        self.assertIsNotNone(collected_data)

    # Function must return 3 seperate lists inside a list
    def test_using_pages_data_types(self):
        collected_data = using_pages()
        self.assertEqual(len(collected_data),3)

class Test_Collecting_Data(unittest.TestCase):

    # Ensure that data is not None
    def test_colecting_data_is_not_none(self):
        data = collecting_data("https://www.skonis-kvapas.lt/arbata/juodoji-arbata")
        self.assertIsNotNone(data)

    # Each item must have 3 elements
    def test_collecting_data_count(self):
        data = collecting_data("https://www.skonis-kvapas.lt/arbata/juodoji-arbata")
        for d in data:
            self.assertEqual(len(d),3)

    # Each item must have a specific type
    def test_collecting_data_type(self):
        data = collecting_data("https://www.skonis-kvapas.lt/arbata/juodoji-arbata")
        for d in data:
            self.assertIsInstance(d[0],str)
            self.assertIsInstance(d[1],float)
            self.assertIsInstance(d[2],str)

class Test_Collecting_Title(unittest.TestCase):

    # Returns ValueError if there is no data inside <h2></h2>
    def test_collecting_title_no_data(self):
        html_data ='<div class="products__item-link"><h2></h2></div>'
        soup = BeautifulSoup(html_data, "html.parser")
        with self.assertRaises(ValueError):
            collecting_title(soup)

    # Returned data must be "str"
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

class Test_Collecting_Type(unittest.TestCase):

    # Returns ValueError if there is no <h2></h2> brackets
    def test_collecting_type_no_h2(self):
        html_data = '<div class="products__item-link"></div>'
        soup = BeautifulSoup(html_data, "html.parser")
        with self.assertRaises(ValueError):
            collecting_type(soup)

    # Returns ValueError if there is no data inside <h2></h2>
    def test_collecting_type_no_data(self):
        html_data = '<div class="products__item-link"><h2></h2></div>'
        soup = BeautifulSoup(html_data, "html.parser")
        with self.assertRaises(ValueError) as error:
            collecting_type(soup)
        self.assertEqual(str(error.exception), "No Data inside <h2></h2>")

    # Function must return "str"
    def test_collecting_type_str(self):
        html_data = '<div class="products__item-link"><h2>juodoji</h2></div>'
        soup = BeautifulSoup(html_data, "html.parser")
        p_type = collecting_type(soup)
        self.assertIsInstance(p_type,str)

class Test_Printing_Data(unittest.TestCase):

    # Data from printing_data can't be None
    def test_printing_data_is_not_None(self):
        self.assertIsNotNone(printing_data())

    # Returned data must contain 3 different Url
    def test_printing_data_url_check(self):
        url = collecting_pages()
        data = printing_data()
        self.assertIn(url[0], data[0])
        self.assertIn(url[1], data[2])
        self.assertIn(url[2], data[4])

    # Returned data must contain same data as using_pages function
    def test_printing_data_data_check(self):
        expected_data = using_pages()
        current_data = printing_data()
        self.assertIn(expected_data[0], current_data[1])
        self.assertIn(expected_data[1], current_data[3])
        self.assertIn(expected_data[2], current_data[5])

class Test_Saving_Data(unittest.TestCase):

    # SetUp for database 
    def setUp(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="$improver44",
            # insert test database
            database="arbatos"
    )
        self.cursor = self.connection.cursor()
        # self.cur.execute('''CREATE TABLE Arbatos
        #     (Title VARCHAR(255), Price FLOAT(4,2) NOT NULL, Type VARCHAR(255))''')
        self.connection.commit()
    def tearDown(self):
        self.connection.close()

    # Checks if saved data is inside database
    def test_saving_data(self):
        sample_data = [
            ('Juodoji arbata SKONIS IR KVAPAS DARJEELING FTGFOP1', 4.48, 'Juodoji Arbata'),
            ('Juodoji arbata SKONIS IR KVAPAS EARL GREY', 1.79, 'Juodoji Arbata'),
            ('Juodoji arbata Darjeeling ORANGE VALLEY SFTGFOP1 FF 2023', 6.87, 'Juodoji Arbata'),
        ]
        saving_data(sample_data)
        self.cursor.execute("SELECT * FROM Arbatos")
        data_from_database = self.cursor.fetchmany(3)
        self.assertEqual(data_from_database, sample_data)

if __name__== '__main__':
    unittest.main()