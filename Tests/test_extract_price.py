import unittest
import time
from web_scrapper import WebScrapper
from selenium.webdriver.common.by import By

class WebScrapperTest(unittest.TestCase):

    def setUp(self) -> None:
        self.scraper_obj = WebScrapper()   

    def test_extract_price(self):
        self.scraper_obj.driver.get('https://www.johnlewis.com/sony-bravia-xr-xr55a80k-2022-oled-hdr-4k-ultra-hd-smart-google-tv-55-inch-with-youview-freesat-hd-dolby-atmos-acoustic-surface-audio-black/p6243821')
        time.sleep(10) 
        price_details = self.scraper_obj.extract_price()
        print(f"{price_details}")
        expected_price = ['£1599.00']
        self.assertEqual(price_details['Price'], expected_price)
           

    def tearDown(self) -> None:
        self.scraper_obj.driver.quit()


if __name__ == "__main__":
    unittest.main()