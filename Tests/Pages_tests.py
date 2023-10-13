
import unittest
import sys
sys.path.insert(1, "C:/Users/Alfonsas/OneDrive/Desktop/Python/Projektai/Scraper")
from Pages import juodoji_arbata_pages

class juodoji_arbata_pages_Tests(unittest.TestCase):
    ''' Must be total 3 pages total '''
    def test_pages_count(self):
        self.assertEqual(len(juodoji_arbata_pages()), 3)

    ''' Must be certain url'''
    def test_pages_structure(self):
        present_pages = juodoji_arbata_pages()
        for p in present_pages:
            self.assertTrue(p.startswith("https://www.skonis-kvapas.lt/arbata/juodoji-arbata?page="))

    ''' Present pages must be equal to expected pages '''
    def test_juodoji_arbata_pages(self):
        expected_pages = [
            "https://www.skonis-kvapas.lt/arbata/juodoji-arbata?page=1",
            "https://www.skonis-kvapas.lt/arbata/juodoji-arbata?page=2",
            "https://www.skonis-kvapas.lt/arbata/juodoji-arbata?page=3"
        ]
        present_pages = juodoji_arbata_pages()
        self.assertEqual(present_pages,expected_pages)

if __name__== '__main__':
    unittest.main()