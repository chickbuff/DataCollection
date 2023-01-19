import unittest
import time
from web_scrapper import WebScrapper
from selenium.webdriver.common.by import By

class WebScrapperTest(unittest.TestCase):

    def setUp(self) -> None:
        self.scraper_obj = WebScrapper()   

    def test_extract_all_product_url(self):
        product_url_list = self.scraper_obj.extract_all_product_url("https://www.johnlewis.com/search/view-all-tvs/_/N-474p?search-term=sony+television&chunk=2")
        for i in range(3):
            print(f"{product_url_list[i]}")
        expected_product_url_list_length = 34
        self.assertEqual(len(product_url_list), expected_product_url_list_length)
           

    def tearDown(self) -> None:
        self.scraper_obj.driver.quit()


if __name__ == "__main__":
    unittest.main()