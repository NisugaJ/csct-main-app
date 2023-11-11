from dotenv import load_dotenv

from scraper.db.connect import connect_to_db
from scraper.helpers.initialize import initialize

load_dotenv()

if __name__ == '__main__':
    # Connect to the database
    connect_to_db()

    initialize()

    print("after initialize")


