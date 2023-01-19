import unittest
import time
from web_scrapper import WebScrapper
from selenium.webdriver.common.by import By

class WebScrapperTest(unittest.TestCase):

    def setUp(self) -> None:
        self.scraper_obj = WebScrapper()   

    def test_extract_image_url(self):
        self.scraper_obj.driver.get('https://www.johnlewis.com/sony-bravia-xr-xr55a80k-2022-oled-hdr-4k-ultra-hd-smart-google-tv-55-inch-with-youview-freesat-hd-dolby-atmos-acoustic-surface-audio-black/p6243821')
        time.sleep(10) 
        img_details = self.scraper_obj.extract_image_url(1)
        print(f"{img_details}")
        expected_img_details = ['https://johnlewis.scene7.com/is/image/JohnLewis/241005876?$rsp-pdp-port-640$']
        self.assertEqual(img_details['Image URL'], expected_img_details)
           

    def tearDown(self) -> None:
        self.scraper_obj.driver.quit()


if __name__ == "__main__":
    unittest.main()