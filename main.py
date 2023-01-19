from utils.web_scrapper import WebScrapper

if __name__ == "__main__" :
    bot = WebScrapper("https://www.johnlewis.com/search?search-term=sony%20television&suggestion=true")  # Creates an instance of the Class             
    bot.scrape_website()
                       