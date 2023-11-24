# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging

import mongoengine
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from mongoengine import NotUniqueError

from app.models.product.Product import Product


class SupermarketscraperPipeline:

    def __init__(self):
        self.db = mongoengine.get_db()
        self.collection_name = "products"

    def process_item(self, item, spider):
        logging.info("Item processing")

        item_dict = ItemAdapter(item).asdict()

        product = Product(**item_dict)

        try:
            product.update(validate=True, upsert=True)
            logging.info(f"Item {product.product_id} saved")
        except NotUniqueError as e:
            # Handle the duplicate key error
            logging.error(
                "Duplicate key error: " + str(
                    e
                    )
                )

        return item
