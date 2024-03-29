import re

from dotenv import load_dotenv
from mongoengine import get_db

from app.db.connect import connect_to_db
from app.models.product.Product import Product

def update_products():

    db = get_db()

    collection = db['product']

    # Define the pattern for the regex
    regex_pattern = re.compile(r'^\/.*')

    # Define the prefix to be added
    prefix_to_add = 'https://groceries.asda.com'

    # Filter documents with the specified regex pattern
    filter_criteria = {'product_link': {'$regex': regex_pattern}}

    updated_count = 0

    for product in Product.objects().aggregate([{"$filter": filter_criteria}]):
        print(product)

        product['product_link'] = prefix_to_add + product['product_link']

        # Update documents by adding a prefix
        update_operation = {'$set': {'product_link': product["product_link"]}}

        # Use update_many to apply the update to multiple documents
        result = collection.update_one( {'product_id': product['product_id']}, update_operation)

    print('Documents updated:', updated_count)