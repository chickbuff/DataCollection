from utils.web_scrapper import WebScrapper
import time

if __name__ == "__main__" :
    bot = WebScrapper()    # Creates an instance of the Class             
    #bot.allow_all_cookies()              # method works
    time.sleep(10)
    #bot.scroll_up_and_down()          # method works
    bot.retrieve_all_tv_data()         # method works 
    bot.save_dictionary()                      
    bot.download_and_save_tv_image()