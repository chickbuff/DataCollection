from ast import arguments
import json
from lib2to3.pgen2 import driver
from turtle import delay
import urllib.request
import uuid
import os
import json
from bs4 import BeautifulSoup  
from selenium  import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time

class WebScrapper:
    
    def __init__(self, URL ):
        self.URL = URL
        self.driver = webdriver.Chrome()
        self.tv_urls = []
        self.tv_data_dictionary = {
            'Product Id':[], 
            'Unique Id':[], 
            'Description':[], 
            'Price':[], 
            'Image URL':[]
            } 
    
        
    # Navigates the webpage by scrolling through the webpage 
    def scroll_up_and_down(self):
        self.driver.get(self.URL)
        time.sleep(10)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)
        self.driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
        print("Scroll_web method works!")

    # Navigates to the next required webpage
    def go_to_nextwebpage(self):
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable--extensions")
        self.driver.get(self.URL)
        while True:
            try:
                self.driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(self.driver,20).until(EC.element_to_be_clickable((By.XPATH,"//li[@class='arrow__right']/a"))))
                self.driver.find_element_by_xpath("//li[@class='arrow__right']/a").click()
                print("Navigating to the next page")
            except (TimeoutException, WebDriverException) as e:
                print("Last page reached")
                break
        self.driver.quit()

    # Allows cookies 
    def bypass_cookies(self):
        self.driver.get(self.URL)
        time.sleep(3)
        try :
            allow_all_button = self.driver.find_element(by=By.XPATH, value =  '//button[@data-test="allow-all"]')
            allow_all_button.click()
            print("Allow all Button clicked!")
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")
        return self.driver

    # Gets all TV URLs/Product ID of each TV
    def extract_tv_urls(self) -> None:
        self.driver.get(self.URL)
        time.sleep(10)
        tv_container = self.driver.find_element(by = By.XPATH, value ='//div[@class="ProductGrid_product-grid__Ph0C3"]')
        tv_list = tv_container.find_elements(by = By.XPATH, value ='.//div[@data-grid-checked="min"]')
        for tv in tv_list:
            self.save_tv_url(tv)
            self.save_product_id(tv)
        print(f" No of Sony TV URLs scrapped = {len(self.tv_urls)}")
        print(f" No of Product Ids scrapped = {len(self.tv_data_dictionary['Product Id'])}")
   
    #Saves tv urls in a list
    def save_tv_url(self,tv):
        a_tag = tv.find_element(by = By.XPATH, value = './/a')
        details_link = a_tag.get_attribute('href')
        self.tv_urls.append(details_link)
            
    #extracts product ID from tv url and saves it in a dictionary
    def save_product_id(self, tv):
        article_tag = tv.find_element(by = By.XPATH, value = './/article')
        product_id = article_tag.get_attribute('data-product-id')
        self.tv_data_dictionary['Product Id'].append(product_id)
        


    # Extracts TV Image url from each tv page presented
    def extract_tv_image_source(self, i, tv_url:str) -> None: 
        self.driver.get(tv_url)
        time.sleep(10) 
        img_tag = self.driver.find_element(by=By.XPATH, value ='//img[@data-index="0"]')
        self.image_src =img_tag.get_attribute('src')
        self.tv_data_dictionary['Image URL'].append(self.image_src)
        print(f" Image URL {i+1} saved successfully!")
        print(" ====================================")

        
    # Extracts all Tv text details from each url presented    
    def extract_tv_text_details(self, tv_url:str):
        self.driver.get(tv_url)
        time.sleep(10)
        price_span_tag = self.driver.find_element(by = By.XPATH, value ='//span[@data-testid="product:price"]')
        price = price_span_tag.text
        self.tv_data_dictionary['Price'].append(price)
        print(f" Price =  {price}")
        description_locator = self.driver.find_element(by = By.XPATH, value ='//h1[@data-testid="product:title"]')
        description = description_locator.text
        self.tv_data_dictionary['Description'].append(description)
        print(f" Description = {description}")

        
    # Generates a V4 UUID for each entry
    def generate_uuid_id(self):
        self.unique_id = str(uuid.uuid4())
        self.tv_data_dictionary['Unique Id'].append(self.unique_id)
        print(f" Unique Id  = {self.unique_id}")


    # Retrieves all Tv data(Images and Text data) from each Tv URL
    def retrieve_all_tv_data(self):                           
        self.extract_tv_urls()                               
        for i, tv_url in enumerate(self.tv_urls):
            print(f" Sony TV {i+1} scrapped details: ")
            print(f" Product Id = {(self.tv_data_dictionary['Product Id'][i])}")
            self.generate_uuid_id()                                                
            self.extract_tv_text_details(tv_url)
            self.extract_tv_image_source(i,tv_url)
        self.driver.quit()
        

    #Creates folders and saves  the dictionary in it    
    def save_dictionary(self):
        project_root_folder = 'C:/Users/chick/miniconda3/envs/data_env/DataCollection/' 
        directory = "raw_data"
        raw_data_folder = os.path.join(project_root_folder,directory)
        os.makedirs(raw_data_folder)
        print("'raw_data' folder created succesfully")
        for product_id in self.tv_data_dictionary['Product Id']:
            new_parent_dir ='C:/Users/chick/miniconda3/envs/data_env/DataCollection/raw_data'
            new_directory = product_id
            prod_id_folder = os.path.join(new_parent_dir, new_directory)
            os.makedirs(prod_id_folder)
            print(f"{product_id} folder created")
            # create a json file called 'data.json' from dictionary
            with open (f"C:/Users/chick/miniconda3/envs/data_env/DataCollection/raw_data/{product_id}/data.json", "w") as fp:                 
                json.dump(self.tv_data_dictionary, fp) 

    #Downloads and save each TV Image extracted from source
    def download_and_save_tv_image(self):
        raw_data_dir = 'C:/Users/chick/miniconda3/envs/data_env/DataCollection/raw_data'
        images_dir = "Images"
        images_folder = os.path.join(raw_data_dir, images_dir)
        os.makedirs(images_folder)
        print("'Images' folder created succesfully")
        for i, image_url in enumerate(self.tv_data_dictionary['Image URL']):
            urllib.request.urlretrieve(image_url, f"C:/Users/chick/miniconda3/envs/data_env/DataCollection/raw_data/Images/{self.tv_data_dictionary['Product Id'][i]}.jpg")
            
    
            
            


if __name__ == "__main__" :
    sony_tv_Page = "https://www.johnlewis.com/search/view-all-tvs/_/N-474p?search-term=sony+television&chunk=2"
    bot = WebScrapper(sony_tv_Page)    # Creates an instance of the Class             
    #startscrape.bypass_cookies()              # method works
    #startscrape.scroll_up_and_down()          # method works
    bot.retrieve_all_tv_data()         # method works 
    bot.save_dictionary()                      
    bot.download_and_save_tv_image()
   
                                             
# %%
        
    

    

       





