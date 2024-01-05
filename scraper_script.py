import os

from dotenv import load_dotenv

from app.db.connect import connect_to_db
from supermarketscraper.SuperMarketScraper import SuperMarketScraper


def start_scraper():
    scraper = SuperMarketScraper()
    scraper.run_spiders()


if os.getenv("RUN_SUPERMARKET_SCRAPER") == "True":
    load_dotenv()
    connect_to_db()

    start_scraper()
