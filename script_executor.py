from dotenv import load_dotenv

from app.db.connect import connect_to_db
from app.models.product.Product import Product
from app.services.product_service import make_passages
from product_analyzer.product_embedding import embed_products
from utils.useful_scripts.csv import get_item_name_and_type

from utils.useful_scripts.merge_json_to_one_json_array import merge_json_files
from utils.useful_scripts.push_products import push_products
from utils.useful_scripts.update_product_type import update_product_category
from utils.useful_scripts.update_products import update_products
from utils.utils import readable_product_type

load_dotenv()
connect_to_db()

# Push extracted products in /crawlee-scraper/storage/exports/ to MongoDB
# push_products()

# Merge all json files in /crawlee-scraper/storage/exports/ to one json file
# merge_json_files()

# Generate passages from a product items
def save_passages():
    passages = make_passages()
    open("data/passages.txt", "w").writelines("".join(passages))


# make_passages()


# embed_products()


# update_products()

# get_item_name_and_type()

# update_product_category()