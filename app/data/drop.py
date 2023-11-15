
from dotenv import load_dotenv

from app.db.connect import connect_to_db
from app.models.scraping.SupermarketMeta import SuperMarketMeta

load_dotenv()

def drop_initial_data():
    # Connect to the database first
    connect_to_db()

    # Drop the initial data
    SuperMarketMeta.drop_collection()

    print(f"Number of SuperMarketMeta objects: {SuperMarketMeta.objects.count()}")


drop_initial_data()