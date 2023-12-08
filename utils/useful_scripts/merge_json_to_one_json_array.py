import datetime
import pathlib
import os
import json
from pprint import pprint
import random

from dotenv import load_dotenv
from mongoengine import get_db
from mongoengine.errors import BulkWriteError

from app.db.connect import connect_to_db

from app.models.product.Product import Product

file_dir = f"{pathlib.Path.cwd()}/crawlee-scraper/storage/exports/singles"
dest_dir = f"{pathlib.Path.cwd()}/crawlee-scraper/storage/exports/merged-singles/"

def merge_json_files():
    data = []
    for filename in os.listdir(file_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(file_dir, filename)
            with open(file_path, encoding='utf-8') as json_file:
                file_data = json.load(json_file)
                data.append(file_data)
    print(data)
    with open(f"{dest_dir}{random.randint(1000, 10000)}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)




