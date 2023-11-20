# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SupermarketscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    product_id = scrapy.Field()
    product_name = scrapy.Field()
    # price = EmbeddedDocumentField(
    #     PriceAndWeight
    #     )
    ingredients = scrapy.Field()
    # nutrients = EmbeddedDocumentField(
    #     Nutrients
    #     )
    # customer_reviews = ListField(
    #     StringField(
    #         null=False
    #         )
    #     )
    customer_rating = scrapy.Field()
    product_link = scrapy.Field()
    meat_alternative = scrapy.Field()
    meat_taste = scrapy.Field()
    meat_look = scrapy.Field()
    # counterpart_products = ListField(
    #     ReferenceField(
    #         'self'
    #         )
    #     )
    plant_based = scrapy.Field()
    dairy = scrapy.Field()