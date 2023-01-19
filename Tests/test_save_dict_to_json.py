import unittest
import time
from web_scrapper import WebScrapper
from selenium.webdriver.common.by import By

class WebScrapperTest(unittest.TestCase):


    def setUp(self) -> None:
        self.scraper_obj = WebScrapper()
        self.scraper_obj.dict = {
            'Product Id':["prodidtest1", "prodidtest2", "prodidtest3"], 
            'Image URL':["https://johnlewis.scene7.com/is/image/JohnLewis/238145395?$rsp-pdp-port-640$", "https://johnlewis.scene7.com/is/image/JohnLewis/006274514?$fashion-ui$", "https://johnlewis.scene7.com/is/image/JohnLewis/006146464?$fashion-ui$"]
            } 

    def test_save_dict_to_json(self):
        self.scraper_obj.save_dict_to_json(self.scraper_obj.dict)
       
    
    def tearDown(self) -> None:
        self.scraper_obj.driver.quit()


if __name__ == "__main__":
    unittest.main()