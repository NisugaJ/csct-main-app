from dotenv import load_dotenv

from app.db.connect import connect_to_db
from app.models.product.Product import Product
from utils.useful_scripts.merge_json_to_one_json_array import merge_json_files
from utils.useful_scripts.push_products import push_products
from utils.utils import readable_product_type

load_dotenv()
connect_to_db()

# Push extracted products in /crawlee-scraper/storage/exports/ to MongoDB
# push_products()

# Merge all json files in /crawlee-scraper/storage/exports/ to one json file
# merge_json_files()

# Generate passages from a product items
def make_passages():
    products = Product.objects()

    passages = []

    for product in products:
        passages.append(
            f"The price of {product.product_name} is {product.price.raw_selling_price} and ingredients are {product.ingredients}.It is a {readable_product_type(product.product_type.value)} product. View the product at {product.product_url}. It has a customer rating of {product.customer_rating}.\n"
        )

    print(passages)

    open("data/passages.txt", "w").write("".join(passages))


make_passages()



