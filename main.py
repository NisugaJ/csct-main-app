from dotenv import load_dotenv
load_dotenv()
from app.db.connect import connect_to_db
# Connect to the Mongo database
connect_to_db()

import uvicorn
import multiprocessing
import os

from starlette.middleware.cors import CORSMiddleware

from app.api.index import app_router

from fastapi import FastAPI


from app.helpers.initialize import initialize
from product_analyzer.utils.vector_store import prepare_vector_stores
# from scraper_script import start_scraper


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(app_router, prefix="/v1")

@app.get("/")
def read_root():
    """
    Handler function for the root endpoint.

    Returns:
        dict: The response containing the app name.
    """
    return {"app": "Scraper Application"}


if __name__ == '__main__':

    # Publish the schema
    # initialize()

    # if os.getenv("RUN_SUPERMARKET_SCRAPER") == "True":
    #     multiprocessing.set_start_method("spawn")
    #     multiprocessing.Process(target=start_scraper).start()
    #     print("Started supermarket scraper as a daemon process...")

    if os.getenv("ADD_DATA_TO_VECTOR_STORE") == "True":
        prepare_vector_stores()

    # Run the app
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=5842, log_level="info")

