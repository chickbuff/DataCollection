import unittest
import time
from web_scrapper import WebScrapper
from selenium.webdriver.common.by import By

class WebScrapperTest(unittest.TestCase):

    def setUp(self) -> None:
        self.scraper_obj = WebScrapper()   

    def test_get_product_id(self):    
        self.scraper_obj.driver.get('https://www.johnlewis.com/sony-bravia-xr-xr55a80k-2022-oled-hdr-4k-ultra-hd-smart-google-tv-55-inch-with-youview-freesat-hd-dolby-atmos-acoustic-surface-audio-black/p6243821')
        time.sleep(10) 
        product_id = self.scraper_obj.get_product_id()
        print(f"{product_id}")
        expected_product_id = ['6243821']
        self.assertEqual(product_id['Product Id'], expected_product_id)

           

    def tearDown(self) -> None:
        self.scraper_obj.driver.quit()


if __name__ == "__main__":
    unittest.main()