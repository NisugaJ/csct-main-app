from datetime import datetime

import scrapy
from mongoengine import Document,\
    StringField,\
    FloatField,\
    BooleanField,\
    ListField,\
    ReferenceField,\
    EmbeddedDocumentField,\
    DateTimeField,\
    signals,\
    EmbeddedDocumentListField

from app.models.product.Nutrient import Nutrient
from app.models.product.Price import PriceAndWeight


class Product(Document):
    product_id = StringField(required=True, unique=True)
    product_name = StringField(required=True)
    price = EmbeddedDocumentField(document_type=PriceAndWeight)
    ingredients = StringField()
    nutrients = EmbeddedDocumentListField(document_type=Nutrient)
    customer_rating = FloatField()
    product_link = StringField(required=True, unique=True)
    meat_alternative = BooleanField()
    meat_taste = BooleanField()
    meat_look = BooleanField()
    counterpart_products = ListField(ReferenceField('self'))
    plant_based = BooleanField()
    dairy = BooleanField()

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField()

    @signals.pre_save.connect
    def update_updated_at(sender, document, **kwargs):
        document.updated_at = datetime.utcnow()

