from ast import arguments
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import json
import urllib.request
import uuid
import os
import json
import time



class WebScrapper:
    '''
    A Class that is used to scrape a desired website, and contains therein all the methods used to achieve the set objective.

    
    Parameters:
    ----------
    Url: str
        the url of the website to be scrapped
    
        
    Attributes:
    ----------
    tv_urls: list
        A list of the Tv Urls scrapped from the website.
    tv_data_dictionary: dict
        Of the form {field : list}
        A dictionary that holds a list of all feature scrapped for each Tv, such as its unique id, product id, price, description, and image url
    

    Methods:
    -------
    allow_all_cookies()
        Finds and clicks the "Allow-all cookies" button on the website.
    extract_tv_urls()
        Extracts all Tv Urls of each Sony TV that is being scrapped.
    save_tv_url()
        Saves all the extracted tv urls in a list.
    save_product_id()
        Extracts product ID from the tv url and saves it in a dictionary
    extract_tv_image_source()
        Extracts Tv Image source from each tv url
    extract_tv_text_details()
        Extracts all Tv text details from each tv url presented
    generate_uuid_id()
        Generates a V4 UUID for each entry in the dictionary
    retrieve_all_tv_data()
        Retrieves all Tv data(Images and Text data) from each Tv Url
    save_dictionary()
        Creates 'raw_data' folder to contain Product id folders for each tv and saves the dictionary in it
    download_and_save_tv_image()
        Downloads and saves each tv Image from each tv image source


    '''  
    def __init__(self, Url: str = "https://www.johnlewis.com/search/view-all-tvs/_/N-474p?search-term=sony+television&chunk=2" ):
        self.driver = webdriver.Chrome()
        self.driver.get(Url)
        self.Url = Url
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
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
        print("Scroll_web method works!")

    # Navigates to the next required webpage
    def go_to_nextwebpage(self):
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable--extensions")
        while True:
            try:
                self.driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(self.driver,20).until(EC.element_to_be_clickable((By.XPATH,"//li[@class='arrow__right']/a"))))
                self.driver.find_element_by_xpath("//li[@class='arrow__right']/a").click()
                print("Navigating to the next page")
            except (TimeoutException, WebDriverException) as e:
                print("Last page reached")
                break
        self.driver.quit()

    def allow_all_cookies(self):
        '''
        Finds and clicks the "Allow-all cookies" button

        '''
        
        try :
            allow_all_button = self.driver.find_element(by=By.XPATH, value =  '//button[@data-test="allow-all"]')
            allow_all_button.click()
            print("Allow all Button clicked!")
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")
        return self.driver

 
    def extract_tv_urls(self) -> None:
        '''
        Obtains from the HTML of the website, a list of all the xpath that houses the Urls to all the Sony Television to be scrapped.
        For each xpath in the list, it does two things:
        1. It calls the save_tv_url method and also
        2. Calls the save_product_id method

        '''

        time.sleep(10)
        tv_container = self.driver.find_element(by = By.XPATH, value ='//div[@class="ProductGrid_product-grid__Ph0C3"]')
        tv_list = tv_container.find_elements(by = By.XPATH, value ='.//div[@data-grid-checked="min"]')
        for tv in tv_list:
            self.save_tv_url(tv)
            self.save_product_id(tv)
        print(f" No of Sony TV URLs scrapped = {len(self.tv_urls)}")
        print(f" No of Product Ids scrapped = {len(self.tv_data_dictionary['Product Id'])}")
   
    
    def save_tv_url(self,tv):
        '''
        Receives an xpath (tv) as an input and extracts the tv url from it and saves the url in a list called tv_urls. 
        
        '''
        a_tag = tv.find_element(by = By.XPATH, value = './/a')
        tv_href = a_tag.get_attribute('href')
        self.tv_urls.append(tv_href)
            

    def save_product_id(self, tv):
        '''
        Receives an xpath (tv) as an input and extracts the Product id of the television from it and saves it in the dictionary. 
        
        '''
        article_tag = tv.find_element(by = By.XPATH, value = './/article')
        product_id = article_tag.get_attribute('data-product-id')
        self.tv_data_dictionary['Product Id'].append(product_id)
        


    def extract_tv_image_source(self, i, tv_url:str) -> None: 
        '''
        From the presented tv url(tv_url), this method extracts the tv image source and saves the resulting Image Url in the dictionary. 
        
        '''

        self.driver.get(tv_url)
        time.sleep(10) 
        img_tag = self.driver.find_element(by=By.XPATH, value ='//img[@data-index="0"]')
        self.image_src =img_tag.get_attribute('src')
        self.tv_data_dictionary['Image URL'].append(self.image_src)
        print(f" Image URL {i+1} saved successfully!")
        print(" ====================================")

           
    def extract_tv_text_details(self, tv_url:str):
        '''
        This method extracts the text details (price, description) of the tv url presented and saves each detail in the dictionary. 
        
        '''

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

        

    def generate_uuid_id(self):
        '''
        Generates a V4 UUID (unique id) for each entry in the dictionary, and saves the generated id in the dictionary.
        
        '''
        self.unique_id = str(uuid.uuid4())
        self.tv_data_dictionary['Unique Id'].append(self.unique_id)
        print(f" Unique Id  = {self.unique_id}")


    
    def retrieve_all_tv_data(self):
        '''
        First calls method to extract all tv urls and for each extracted Url, does 3 things sequentially:
        1. Calls method that generates a unique id for that url,
        2. Calls method that extracts Text data from the Tv URL presented, and
        3. Calls method that extracts the the image source.
        
        '''

        self.extract_tv_urls()                               
        for i, tv_url in enumerate(self.tv_urls):
            print(f" Sony TV {i+1} scrapped details: ")
            print(f" Product Id = {(self.tv_data_dictionary['Product Id'][i])}")
            self.generate_uuid_id()                                                
            self.extract_tv_text_details(tv_url)
            self.extract_tv_image_source(i,tv_url)
        self.driver.quit()
        
   
    def save_dictionary(self):
        '''
        Creates a folder called 'raw_data' in the root folder of the project
        Within the newly created folder, the method creates a folder with the Product id of each tv as its name,
        Inside each Product id folder, the method saves the dictionary in a file called data.json
        
        '''
        project_root_folder = 'C:\Users\chick\OneDrive\Desktop\AiCore\Projects\DataCollection' 
        directory = "raw_data"
        raw_data_folder = os.path.join(project_root_folder,directory)
        os.makedirs(raw_data_folder)
        print("'raw_data' folder created succesfully")
        for product_id in self.tv_data_dictionary['Product Id']:
            new_parent_dir ='C:/Users/chick/OneDrive/Desktop/Aicore/Projects/DataCollection/raw_data'
            new_directory = product_id
            prod_id_folder = os.path.join(new_parent_dir, new_directory)
            os.makedirs(prod_id_folder)
            print(f"{product_id} folder created")
            # create a json file called 'data.json' from dictionary
            with open (f"C:/Users/chick/OneDrive/Desktop/Aicore/Projects/DataCollection/raw_data/{product_id}/data.json", "w") as fp:                 
                json.dump(self.tv_data_dictionary, fp) 


    def download_and_save_tv_image(self):
        '''
        Creates a folder called 'Images' inside the previously created 'raw_data' folder
        Pulls from the dictionary the list of all Image Url earlier saved.
        For each Image url, download each tv image and name it as <product id of each tv image >.jpg inside the newly created 'Images' folder 
    
        '''
        raw_data_dir = 'C:/Users/chick/OneDrive/Desktop/Aicore/Projects/DataCollection/raw_data'
        images_dir = "Images"
        images_folder = os.path.join(raw_data_dir, images_dir)
        os.makedirs(images_folder)
        print("'Images' folder created succesfully")
        for i, image_url in enumerate(self.tv_data_dictionary['Image URL']):
            urllib.request.urlretrieve(image_url, f"C:/Users/chick/OneDrive/Desktop/Aicore/Projects/DataCollection/raw_data/Images/{self.tv_data_dictionary['Product Id'][i]}.jpg")
            
    

if __name__ == "__main__" :
    bot = WebScrapper()    # Creates an instance of the Class             
    #bot.allow_all_cookies()              # method works
    time.sleep(10)
    #bot.scroll_up_and_down()          # method works
    bot.retrieve_all_tv_data()         # method works 
    bot.save_dictionary()                      
    bot.download_and_save_tv_image()
   
                                             
# %%
        
    

    

       





