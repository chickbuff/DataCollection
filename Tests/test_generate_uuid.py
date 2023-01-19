import unittest
import time
from web_scrapper import WebScrapper
from selenium.webdriver.common.by import By

class WebScrapperTest(unittest.TestCase):

    def setUp(self) -> None:
        self.scraper_obj = WebScrapper()   

    def test_generate_uuid_id(self):     
        self.scraper_obj.driver.get('https://www.johnlewis.com/sony-bravia-kd32w800-2021-led-hdr-hd-ready-720p-smart-android-tv-32-inch-with-freeview-play/p5561895')
        time.sleep(10) 
        unique_id = self.scraper_obj.generate_uuid_id()
        print(f"{unique_id}")

           

    def tearDown(self) -> None:
        self.scraper_obj.driver.quit()


if __name__ == "__main__":
    unittest.main()