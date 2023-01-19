import unittest
import time
from web_scrapper import WebScrapper
from selenium.webdriver.common.by import By

class WebScrapperTest(unittest.TestCase):

    def setUp(self) -> None:
        self.scraper_obj = WebScrapper()   

    def test_extract_title(self):     
        self.scraper_obj.driver.get('https://www.johnlewis.com/sony-bravia-kd32w800-2021-led-hdr-hd-ready-720p-smart-android-tv-32-inch-with-freeview-play/p5561895')
        time.sleep(10) 
        title_details = self.scraper_obj.extract_title()
        print(f"{title_details}")
        expected_title_details = ['Sony Bravia KD32W800 (2021) LED HDR HD Ready 720p Smart Android TV, 32 inch with Freeview Play']
        self.assertEqual(title_details['Title'], expected_title_details)
           

    def tearDown(self) -> None:
        self.scraper_obj.driver.quit()


if __name__ == "__main__":
    unittest.main()