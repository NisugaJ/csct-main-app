import pathlib
import os
import json
from pprint import pprint

from dotenv import load_dotenv
from mongoengine import get_db
from mongoengine.errors import BulkWriteError

from app.db.connect import connect_to_db

from app.models.product.Product import Product

file_dir = f"{pathlib.Path.cwd()}/crawlee-scraper/storage/exports/"

def read_json_files(data_dir):
    data = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(data_dir, filename)
            with open(file_path) as json_file:
                file_data = json.load(json_file)
                data += file_data

    return data

def push_products():
    get_db()

    data = read_json_files(file_dir)

    products_dict = {}

    # Making a dictionary of products while removing duplicates
    for product in data:
        products_dict[product['product_id']] = product

    print(f"len(products_dict): {len(products_dict)}")

    # Query for products with IDs in list
    existing_products = Product.objects(product_id__in=products_dict.keys())

    # Get list of existing IDs
    existing_ids = [p.product_id for p in existing_products]
    print(f"Matched existing product id count: {len(existing_ids)}")

    # New products count
    new_products_count = len(products_dict.keys()) - len(existing_ids)

    batch_size = 100
    products = []

    for product_data in products_dict.values():
        product = Product(**product_data)
        product_id = product_data['product_id']

        if product_id not in existing_ids:
            products.append(product)

        if len(products) >= batch_size:
            try:
                Product.objects.insert(products, load_bulk=False)
                products = []
            except BulkWriteError as bwe:
                pprint(bwe.details)

    if products:
        Product.objects.insert(products, load_bulk=False)

    print(f"Inserted {new_products_count} products.")


