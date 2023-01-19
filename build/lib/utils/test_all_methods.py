import unittest
import time
from web_scrapper import WebScrapper
from selenium.webdriver.common.by import By

class WebScrapperTest(unittest.TestCase):


    def setUp(self) -> None:
        self.scraper_obj = WebScrapper()
        self.scraper_obj.dict = {
                            'Product Id':[], 
                            'Image URL':[],
                            'Unique Id':[],
                            'Title':[],
                            'Price':[]
                            } 

    def test_extract_all_product_url(self):
        product_url_list = self.scraper_obj.extract_all_product_url("https://www.johnlewis.com/search/view-all-tvs/_/N-474p?search-term=sony+television&chunk=2")
        for i in range(3):
            print(f"{product_url_list[i]}")
        expected_product_url_list_length = 34
        self.assertEqual(len(product_url_list), expected_product_url_list_length)

    def test_get_product_id(self):    
        self.scraper_obj.driver.get('https://www.johnlewis.com/sony-bravia-xr-xr55a80k-2022-oled-hdr-4k-ultra-hd-smart-google-tv-55-inch-with-youview-freesat-hd-dolby-atmos-acoustic-surface-audio-black/p6243821')
        time.sleep(10) 
        self.scraper_obj.dict = self.scraper_obj.get_product_id()
        print(f"{self.scraper_obj.dict}")
        expected_product_id = ['6243821']
        self.assertEqual(self.scraper_obj.dict['Product Id'], expected_product_id)
    
    def test_generate_uuid_id(self):     
        self.scraper_obj.driver.get('https://www.johnlewis.com/sony-bravia-kd32w800-2021-led-hdr-hd-ready-720p-smart-android-tv-32-inch-with-freeview-play/p5561895')
        time.sleep(10) 
        self.scraper_obj.dict = self.scraper_obj.generate_uuid_id()
        print(f"{self.scraper_obj.dict}")

    def test_extract_title(self):     
        self.scraper_obj.driver.get('https://www.johnlewis.com/sony-bravia-kd32w800-2021-led-hdr-hd-ready-720p-smart-android-tv-32-inch-with-freeview-play/p5561895')
        time.sleep(10) 
        self.scraper_obj.dict = self.scraper_obj.extract_title()
        print(f"{self.scraper_obj.dict}")
        expected_title_details = ['Sony Bravia KD32W800 (2021) LED HDR HD Ready 720p Smart Android TV, 32 inch with Freeview Play']
        self.assertEqual(self.scraper_obj.dict['Title'], expected_title_details)

    
    def test_extract_price(self):
        self.scraper_obj.driver.get('https://www.johnlewis.com/sony-bravia-xr-xr55a80k-2022-oled-hdr-4k-ultra-hd-smart-google-tv-55-inch-with-youview-freesat-hd-dolby-atmos-acoustic-surface-audio-black/p6243821')
        time.sleep(10) 
        self.scraper_obj.dict = self.scraper_obj.extract_price()
        print(f"{self.scraper_obj.dict}")
        expected_price = ['£1599.00']
        self.assertEqual(self.scraper_obj.dict['Price'], expected_price)
    
    def test_extract_image_url(self):
        self.scraper_obj.driver.get('https://www.johnlewis.com/sony-bravia-xr-xr55a80k-2022-oled-hdr-4k-ultra-hd-smart-google-tv-55-inch-with-youview-freesat-hd-dolby-atmos-acoustic-surface-audio-black/p6243821')
        time.sleep(10) 
        self.scraper_obj.dict = self.scraper_obj.extract_image_url(1)
        print(f"{self.scraper_obj.dict}")
        expected_img_details = ['https://johnlewis.scene7.com/is/image/JohnLewis/241005876?$rsp-pdp-port-640$']
        self.assertEqual(self.scraper_obj.dict['Image URL'], expected_img_details)
    
    def test_save_dict_to_json(self):
        self.scraper_obj.save_dict_to_json(self.scraper_obj.dict)

    def test_download_img(self):
        self.scraper_obj.download_img(self.scraper_obj.dict)

    def tearDown(self) -> None:
        self.scraper_obj.driver.quit()


if __name__ == "__main__":
    unittest.main()