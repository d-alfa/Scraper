
import unittest
from unittest.mock import Mock, patch
import mysql.connector
from bs4 import BeautifulSoup
import sys
sys.path.insert(1, "C:/Users/Alfonsas/OneDrive/Desktop/Python/Projektai/Scraper")
from Scraper import collecting_pages, using_pages, collecting_data, collecting_title, collecting_price, collecting_type, saving_data, passing_data_into_saving_data, collecting_url_and_data, printing_data

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

class Test_Saving_Data(unittest.TestCase):

    # Tests saving_data functionality using "unittest.mock"
    @patch('Scraper.mysql.connector.connect')
    def test_saving_data(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_connection = mock_connect.return_value
        item = [("Green Tea", 5.99, "Green")]
        saving_data(item)

        # Checks if "mock object" was called with specific arguments
        mock_connect.assert_called_with(
            host="localhost",
            user="root",
            password="$improver44",
            database="arbatos"
        )
    
        # Checks if "executemany" method of the "mock_cursor" was called with specific arguments
        mock_cursor.executemany.assert_called_with("INSERT INTO arbatos VALUES (%s,%s,%s)", item)

        # Checks if "commit" and "close" methods of the "mock_connection" were called
        mock_connection.commit.assert_called()
        mock_connection.close.assert_called()

class Test_Passing_Data_Into_Saving_data(unittest.TestCase):

    # Tests "passing_data_into_saving_data" functionality using "unittest.mock"
    @patch('Scraper.using_pages')
    @patch('Scraper.saving_data')
    def test_passing_data_into_saving_data(self, mock_saving_data, mock_using_pages):
        data = [
            ('Item1', 10.0, 'Type1'),
            ('Item2', 15.0, 'Type2'),
            ('Item3', 8.0, 'Type3')
        ]
        mock_using_pages.return_value = data
        passing_data_into_saving_data()

        # Records the expected calls with each "item" from "data"  
        calls = [unittest.mock.call(item) for item in data]

        # Checks if "mock_saving_data" has been called with the list of "calls"
        mock_saving_data.assert_has_calls(calls)

class Test_Collecting_Url_And_Data(unittest.TestCase):

    # Data from collecting_url_and_data can't be None
    def test_collecting_url_and_data_is_not_None(self):
        self.assertIsNotNone(collecting_url_and_data)

    # Returned data must contain 3 different Url
    def test_collecting_url_and_data_url_check(self):
        url = collecting_pages()
        data = collecting_url_and_data()
        self.assertIn(url[0], data[0])
        self.assertIn(url[1], data[2])
        self.assertIn(url[2], data[4])

    # Returned data must contain same data as using_pages function
    def test_collecting_url_and_data_data_check(self):
        expected_data = using_pages()
        current_data = collecting_url_and_data()
        self.assertListEqual(expected_data[0], current_data[1])
        self.assertListEqual(expected_data[1], current_data[3])
        self.assertListEqual(expected_data[2], current_data[5])

class Test_Printing_Data(unittest.TestCase):

    # Tests "printing_data" functionality using "unittest.mock"
    @patch('Scraper.collecting_url_and_data')
    @patch('builtins.print')
    def test_printing_data(self, mock_print, mock_collecting_url_and_data):
        url_and_data = [
            ['https://example.com/1'], [('Item1', 10.0, 'Type1'),('Item2', 15.0, 'Type2')],
            ['https://example.com/2'], [('Item3', 9.0, 'Type3'),('Item4', 14.0, 'Type4')],
        ]
        mock_collecting_url_and_data.return_value = url_and_data
        printing_data()

        # List of expected_calls
        expected_calls = [unittest.mock.call(item) for item in mock_collecting_url_and_data]
        
        # Checks if mock_print kas been called with arguments from expected_calls
        mock_print.assert_has_calls(expected_calls, any_order=True)

if __name__== '__main__':
    unittest.main()