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
    load_dotenv()
    connect_to_db()
    get_db()

    data = read_json_files(
        file_dir
        )

    batch_size = 100
    products = []
    pushed_product_id_list = []

    for product_data in data:
        product = Product(**product_data)
        product_id = product_data['product_id']
        new_product = False if Product.objects(product_id=product_id).first() else True

        if product_id not in pushed_product_id_list and new_product:
            products.append(product)
            pushed_product_id_list.append(product_id)

        if len(products) >= batch_size:
            try:
                Product.objects.insert(products, load_bulk=False)
                products = []
            except BulkWriteError as bwe:
                pprint(bwe.details)

    if products:
        Product.objects.insert(products, load_bulk=False)


