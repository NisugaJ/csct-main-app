from dotenv import load_dotenv
load_dotenv()

from app.db.connect import connect_to_db
connect_to_db()


from utils.useful_scripts.chroma import chroma_run



# Push extracted products in /crawlee-scraper/storage/exports/ to MongoDB
# push_products()

# Merge all json files in /crawlee-scraper/storage/exports/ to one json file
# merge_json_files()



# make_passages()


# embed_products()


# update_products()

# get_item_name_and_type()

# update_product_category()


chroma_run()