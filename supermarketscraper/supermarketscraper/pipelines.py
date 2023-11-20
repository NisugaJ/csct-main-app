# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging

import mongoengine
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from app.models.product.Product import Product


class SupermarketscraperPipeline:

    def __init__(self):
        self.db = mongoengine.get_db()
        self.collection_name = "products"

    def process_item(self, item, spider):
        logging.info("Item processing")

        item_dict = ItemAdapter(item).asdict()

        line = json.dumps(item_dict)
        logging.info(line)

        product = Product(**item_dict)
        product.save(validate=True)

        return item
