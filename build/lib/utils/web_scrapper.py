from ast import arguments
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import boto3
import json
import os
import pandas as pd
import time
import urllib.request
import uuid




class WebScrapper:
    '''
    A Class that is used to scrape a desired website, and contains therein all the methods used to achieve the set objective.

    
    Parameters:
    ----------
    website_to_scrape: str
        the url of the website to be scrapped
    
        
    Attributes:
    ----------
    prod_xpath_list: list
        A list of Xpaths scrapped from given website
    product_url_list: list
        A list of the product Urls scrapped from the website.
    product_data_dictionary: dict
        Of the form {field : list}
        A dictionary that holds a list of all feature scrapped for each Tv, such as its unique id, product id, price, description, and image url
    

    Methods:
    -------
    allow_all_cookies()
        Finds and clicks the "Allow-all cookies" button on the website.
    extract_all_product_url()
        Returns a list of saved product url extracted from the xpath of all products listed on the desired website.
    save_product_url()
        Saves all the extracted product urls in a list.
    get_product_id()
        Extracts product ID from the product url presented and saves it in a dictionary.
    generate_uuid_id()
        Generates a V4 UUID for each entry in the dictionary and saves in the dictionary.
    extract_price()    
        This method extracts product price details from the product url presented and saves each detail in the dictionary.
    extract_title()
        This method extracts product title from the url presented and saves each detail in the dictionary.
    extract_image_url() 
        Extracts from the each product url, the list of associated image url and saves the list in the dictionary.
    save_dict_to_json()
        Creates a folder in the root directory to contain mutiple product id folders(to be created) and saves the dictionary in a JSON format into each product id folder. 
    download_img()
        Locally downloads each product Image and saves it a new folder called 'images'
    create_folder
        creates folder from the parent and child directories supplied
    scrape_website()
        Calls several methods to scrape/retrieves all product data(product id, Text data, and Images) from each product Url extracted from the website.



    '''  
    def __init__(self, website_to_scrape: str):
        options = Options()
        options.add_argument("--headless")
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
        options.add_argument("window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(chrome_options=options)
        self.website_to_scrape = website_to_scrape
        self.prod_xpath_list = []
        self.product_url_list = []
        self.product_data_dictionary = {
            'Product Id':[], 
            'Unique Id':[], 
            'Title':[], 
            'Price':[], 
            'Image URL':[]
            } 
    
        
    # Navigates the webpage by scrolling through the webpage 
    def scroll_up_and_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
        print(" Page Scrolling done!")

    def allow_all_cookies(self):
        '''
        Finds and clicks the "Allow-all cookies" button

        '''
        try :
            allow_all_button = self.driver.find_element(by = By.XPATH, value ='//button[@data-test="allow-all"]')
            allow_all_button.click()
            print(" Allow all Button clicked!")
            time.sleep(1)
        except TimeoutException:
            print(" Loading took too much time!")
        return self.driver
 
    def extract_all_product_url(self, given_webpage:str) -> None:
        '''
        i.  The webpage scrolls up and down,
        ii. Allow button is clicked,
        iii.The program obtains from the given webpage, a list of all the xpath that houses the Product Urls (of all the Sony Television) to be scrapped.
        iv. It saves the product url for each xpath in the list.

        '''
        self.driver.get(given_webpage)
        print(" Given WebPage Opened!")
        time.sleep(1)
        self.scroll_up_and_down()
        time.sleep(1)
        self.allow_all_cookies()
        prod_container = self.driver.find_element(by = By.XPATH, value ='//div[@class="ProductGrid_product-grid__Ph0C3"]')
        #prod_container = self.driver.find_element(by = By.XPATH, value ='//div[@data-test-id="product-grid"]')
        prod_xpath_list = prod_container.find_elements(by = By.XPATH, value ='.//div[@data-grid-checked="min"]')
        print (f" Xpath length = {len(prod_xpath_list)}")
        for each_xpath in prod_xpath_list:
            self.save_product_url(each_xpath)
        print(f" No of Product URLs scrapped = {len(self.product_url_list)}")
        print(" ============================")
        return self.product_url_list
        
    def save_product_url(self,presented_xpath:str):
        '''
        Receives an xpath as an input and extracts the product url from it and saves the url in a list called product_url_list. 
        
        '''
        a_tag = presented_xpath.find_element(by = By.XPATH, value = './/a')
        prod_href = a_tag.get_attribute('href')
        self.product_url_list.append(prod_href)
        
    def get_product_id(self):
        '''
        Receives the url of product and extracts the Product id from it and saves it in the dictionary. 
        
        '''
        article_tag = self.driver.find_element(by = By.XPATH, value = './/jl-user-content')
        product_id_tag = article_tag.get_attribute('productid')
        self.product_data_dictionary['Product Id'].append(product_id_tag)
        print(f" Product Id = {product_id_tag}")
        return self.product_data_dictionary

    def generate_uuid_id(self):
        '''
        Generates a V4 UUID (unique id) for each entry in the dictionary, and saves the generated id in the dictionary.
        
        '''
        unique_id = str(uuid.uuid4())
        self.product_data_dictionary['Unique Id'].append(unique_id)
        print(f" Product Unique Id = {unique_id}")
        return self.product_data_dictionary
        
    def extract_title(self):
        '''
        This method extracts product title from the url presented and saves it in the dictionary. 
        
        '''
        title_locator = self.driver.find_element(by = By.XPATH, value ='//img[@data-index="image-0"]')
        title = title_locator.get_attribute('alt')
        self.product_data_dictionary['Title'].append(title)
        print(f" Product Title = {title}")
        return self.product_data_dictionary

    def extract_price(self):
        '''
        This method extracts product price from the url presented and saves it in the dictionary. 
        
        '''
        price_tag = self.driver.find_element(by = By.XPATH, value ='//dd[@data-testid="product:basket:price"]')
        price = price_tag.text
        self.product_data_dictionary['Price'].append(price)
        print(f" Product Price =  {price}")
        return self.product_data_dictionary

    def extract_image_url(self, i:int) -> None: 
        '''
        From the presented url, this method extracts the product image source and saves the resulting Image Url in the dictionary. 
        
        ''' 
        img_tag = self.driver.find_element(by = By.XPATH, value ='//img[@data-index="image-0"]')
        self.image_src =img_tag.get_attribute('src')
        self.product_data_dictionary['Image URL'].append(self.image_src)
        print(f" Image URL {i+1} saved successfully!")
        return self.product_data_dictionary
           
    def save_dict_to_json(self, dict_to_save:dict) -> None:
        '''
        Creates a folder called 'raw_data' in the root folder of the project
        Within the newly created folder, the method creates a folder with the Product id of each tv as its name,
        Inside each Product id folder, the method saves the dictionary in a file called data.json
        
        '''
        
        try:
            dir_to_create = 'raw_data'
            self._create_folder('C:/Users/chick/OneDrive/Desktop/Aicore/Projects/DataCollection',dir_to_create)
        except:
            print(f" {dir_to_create} folder already exists")
        #Loop to create multiple product id folders inside 'raw_data' folder
        for  product_id in dict_to_save['Product Id']:
            try:
                dir_to_create2 = product_id
                self._create_folder('C:/Users/chick/OneDrive/Desktop/Aicore/Projects/DataCollection/raw_data',dir_to_create2)
                #create a json file called 'data.json' from dictionary
                with open (f"C:/Users/chick/OneDrive/Desktop/Aicore/Projects/DataCollection/raw_data/{product_id}/data.json", "w") as fp:                 
                    json.dump(dict_to_save, fp)
            except:
                print(f"{product_id} folder already exist")
             
    def _create_folder(self, parent_dir:str, child_dir:str):
        '''
        Method used to create a folder from the parent and child directories supplied
    
        '''
        folder_to_create = os.path.join(parent_dir,child_dir)
        os.makedirs(folder_to_create)
        print(f"'{child_dir}' folder created")

    def download_img(self, dict_to_download_from:dict) -> None:
        '''
        Creates a folder called 'Images' inside the previously created 'raw_data' folder
        Pulls from the dictionary the list of all Image Urls earlier saved, and
        For each Image url, download each product image and name it as <product id of each tv image >.jpg and save it inside the newly created 'Images' folder 
    
        '''
        try:
            child_dir = 'Images'
            self._create_folder('C:/Users/chick/OneDrive/Desktop/Aicore/Projects/DataCollection/raw_data', child_dir)
        except:
            print(f"{child_dir} folder already exist")
        for i, image_url in enumerate(dict_to_download_from['Image URL']):
                urllib.request.urlretrieve(image_url, f"C:/Users/chick/OneDrive/Desktop/Aicore/Projects/DataCollection/raw_data/Images/{dict_to_download_from['Product Id'][i]}.jpg")
        

    def scrape_website(self):
        '''
        First calls method to extract all product xpath from the given webpage and saves the product url associated with each xpath extracted.
        For each product Url, it calls the methods below and saves the result in the dictionary. 
             i. Gets the Product id for each product,
            ii. Generates the unique id for each product,
           iii. Extracts title of each product,
            iv. Extract price of each product, and
             v. Extract the image url.
        It then saves data dictionary into a Json format before finally
        Downloading and saving locally the raw Product Images from Image Url  in the Dictionary.
        '''
        self.extract_all_product_url(self.website_to_scrape)
        for i, prod_url in enumerate(self.product_url_list):
            self.driver.get(prod_url)
            time.sleep(1) 
            print(f" Sony TV {i+1} scrapped details:")                                             
            self.get_product_id()
            self.generate_uuid_id()
            self.extract_title()
            self.extract_price()
            self.extract_image_url(i)
            print(" ====================================")
        self.driver.quit()
        self.save_dict_to_json(self.product_data_dictionary)
        self.download_img(self.product_data_dictionary)
    
    

if __name__ == "__main__" :
    bot = WebScrapper("https://www.johnlewis.com/search/view-all-tvs/_/N-474p?search-term=sony+television&chunk=2")           # Creates an instance of the Class             
    bot.scrape_website() 
    
   
                                             
# %%
        
    

    

       





