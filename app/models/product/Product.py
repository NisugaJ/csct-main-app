import scrapy
from mongoengine import Document, StringField, FloatField, BooleanField, ListField, ReferenceField,\
    EmbeddedDocumentField

from app.models.product.Nutrient import Nutrient
from app.models.product.Price import  PriceAndWeight


class Product(Document):
    product_id = StringField(required=True, unique=True)
    product_name = StringField(required=True)
    price = EmbeddedDocumentField(PriceAndWeight)
    ingredients = StringField()
    nutrients = ListField(ReferenceField(Nutrient))
    customer_rating = FloatField()
    product_link = StringField(required=True, unique=True)
    meat_alternative = BooleanField()
    meat_taste = BooleanField()
    meat_look = BooleanField()
    counterpart_products = ListField(ReferenceField('self'))
    plant_based = BooleanField()
    dairy = BooleanField()
