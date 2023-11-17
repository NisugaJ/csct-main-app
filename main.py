import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from app.db.connect import connect_to_db
from app.helpers.initialize import initialize
from supermarketscraper.scraper import Scraper

# import api
from app.api import index

load_dotenv()

# Create the FastAPI app
app = FastAPI()


@app.get("/")
def read_root():
    """
    Handler function for the root endpoint.

    Returns:
        dict: The response containing the app name.
    """
    return {"app": "Scraper Application"}


if __name__ == '__main__':
    # Connect to the database
    connect_to_db()

    # Publish the schema
    initialize()

    # Run the supermarket scraper
    if os.getenv("RUN_SUPERMARKET_SCRAPER") == "True":
        scraper = Scraper()
        scraper.run_spiders()

    # Run the app
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=5842, log_level="info")


