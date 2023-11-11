from scraper.db.connect import connect_to_db
from scraper.models.scraping.SupermarketMeta import SuperMarketMeta
from dotenv import load_dotenv

load_dotenv()

def drop_initial_data():
    # Connect to the database first
    connect_to_db()

    # Drop the initial data
    SuperMarketMeta.drop_collection()

    print(f"Number of SuperMarketMeta objects: {SuperMarketMeta.objects.count()}")


drop_initial_data()