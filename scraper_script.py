from app.db.connect import connect_to_db
from supermarketscraper.SuperMarketScraper import SuperMarketScraper

def start_scraper():
    connect_to_db()
    scraper = SuperMarketScraper()
    scraper.run_spiders()