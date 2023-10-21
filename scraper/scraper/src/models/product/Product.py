from mongoengine import Document, StringField, FloatField, BooleanField, ListField, ReferenceField,\
    EmbeddedDocumentField
from scraper.src.models.product.Nutrients import Nutrients
from scraper.src.models.product.Price import Price

class Product(Document):
    product_id = StringField(required=True, unique=True)
    product_name = StringField(required=True)
    price = EmbeddedDocumentField(Price)
    ingredients = StringField()
    nutrients = EmbeddedDocumentField(Nutrients)
    customer_reviews = ListField(StringField(null=False))
    customer_rating = FloatField()
    product_link = StringField(required=True, unique=True)
    meat_alternative = BooleanField()
    meat_taste = BooleanField()
    meat_look = BooleanField()
    counterpart_products = ListField(ReferenceField('self'))
    plant_based = BooleanField()
    dairy = BooleanField()
