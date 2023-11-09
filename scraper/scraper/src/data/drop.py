from scraper.src.db.connect import connect_to_db
from scraper.src.models.scraping.ListPageMeta import ListPageMeta
from scraper.src.models.scraping.SupermarketMeta import SuperMarketMeta
from dotenv import load_dotenv

load_dotenv()

def drop_initial_data():
    # Connect to the database first
    connect_to_db()

    # Drop the initial data
    SuperMarketMeta.drop_collection()

    print(f"Number of SuperMarketMeta objects: {SuperMarketMeta.objects.count()}")


drop_initial_data()