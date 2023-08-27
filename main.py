from scraper import Scraper

def main(url):
    my_scrapper=Scraper(url=url)
    my_scrapper.main()
    
if __name__== "__main__":
    url= "https://www.premierleague.com/stats/top/players/goals"
    main(url=url)