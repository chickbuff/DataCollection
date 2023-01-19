import unittest
import time
from web_scrapper import WebScrapper
from selenium.webdriver.common.by import By

class WebScrapperTest(unittest.TestCase):


    def setUp(self) -> None:
        self.scraper_obj = WebScrapper()
        self.scraper_obj.dict = {
            'Product Id':['test12345'], 
            'Image URL':['https://johnlewis.scene7.com/is/image/JohnLewis/238145395?$rsp-pdp-port-640$']
            } 

    def test_download_img(self):
        self.scraper_obj.download_img(self.scraper_obj.dict)
       
    
    def tearDown(self) -> None:
        self.scraper_obj.driver.quit()


if __name__ == "__main__":
    unittest.main()