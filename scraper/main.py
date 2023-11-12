import uvicorn
from dotenv import load_dotenv
from scraper.db.connect import connect_to_db
from scraper.helpers.crawler import start_crawler_process
from scraper.helpers.initialize import initialize
from typing import Union
from fastapi import FastAPI

load_dotenv()

# Create the FastAPI app
app = FastAPI()


from fastapi import FastAPI

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

    start_crawler_process()

    # Run the app
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=5842, log_level="info")


