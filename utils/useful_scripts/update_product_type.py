import re

from dotenv import load_dotenv
from mongoengine import get_db

from app.db.connect import connect_to_db
from app.models.product.Product import Product

def update_product_category():
    # Use a pipeline as a high-level helper
    from transformers import pipeline

    pipe = pipeline(
        "text-classification",
        model="nisuga/food_type_classification_model"
        )


    db = get_db()

    collection = db['product']

    # Define the pattern for the regex
    regex_pattern = re.compile(r'^\/.*')

    # Define the prefix to be added
    # prefix_to_add = 'https://groceries.asda.com'

    # Filter documents with the specified regex pattern
    # filter_criteria = {'product_link': {'$regex': regex_pattern}}

    updated_count = 0

    stop_words = ["ASDA", "ASDA Succulent", "Oak Smoked"]

    for product in Product.objects():
        # Split product name into words
        words = product.product_name.split()

        # Filter out stop words
        filtered_words = [word for word in words if word not in stop_words]

        # Join words back into string
        input = " ".join(
            filtered_words
        )

        result = pipe(input)
        label = result[0]['label']
        print(f"{product.product_name}:: {label}")

        # Update documents by adding a prefix
        update_operation = {'$set': {'product_type': label}}

        # Use update_many to apply the update to multiple documents
        collection.update_one({'product_id': product['product_id']}, update_operation)

        updated_count += updated_count + 0

    print('Documents updated:', updated_count)

