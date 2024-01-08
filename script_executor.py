from dotenv import load_dotenv

from utils.useful_scripts.extract_nutrient_raw_names import extract_nutrient_raw_names

load_dotenv()

from utils.useful_scripts.embeddings import find_embeddings_by_product_id, delete_all_collections

from app.db.connect import connect_to_db
connect_to_db()


from utils.useful_scripts.chroma import chroma_run


### Files related scripts

# Merge all json files in /crawlee-scraper/storage/exports/ to one json file
# merge_json_files()

### Products monog collection related scripts

# Push extracted products in /crawlee-scraper/storage/exports/ to MongoDB
# push_products()

# make_passages()
# embed_products()
# update_products()
# get_item_name_and_type()
# update_product_category()


### LLM related scripts

# chroma_run()

# find_embeddings_by_product_id("ASDA_910002551988")

# delete_all_collections()

extract_nutrient_raw_names()