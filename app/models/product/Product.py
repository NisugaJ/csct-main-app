from datetime import datetime
from enum import Enum

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
    EmbeddedDocumentListField,\
    EnumField

from app.models.product.Nutrient import Nutrient
from app.models.product.Price import PriceAndWeight

class ProductType(Enum):
    MEAT = "MEAT"
    DAIRY = "DAIRY"
    VEGETARIAN = "VEGETARIAN"
    VEGAN = "VEGAN"
    MEAT_ALTERNATIVE = "MEAT_ALTERNATIVE"
    DAIRY_ALTERNATIVE = "DAIRY_ALTERNATIVE"

class Product(Document):
    product_id = StringField(required=True, unique=True)
    product_name = StringField(required=True)
    price = EmbeddedDocumentField(document_type=PriceAndWeight)
    ingredients = StringField()
    nutrients = EmbeddedDocumentListField(document_type=Nutrient)
    customer_rating = FloatField()
    product_link = StringField(required=True, unique=True)
    product_type = EnumField(ProductType)
    counterpart_products = ListField(ReferenceField('self'))

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField()

    @signals.pre_save.connect
    def update_updated_at(sender, document, **kwargs):
        document.updated_at = datetime.utcnow()

    @signals.pre_save_post_validation.connect
    def update_product_type(sender, document, **kwargs):
        product_context = document.product_name.lower().join(document.ingredients.lower())

        # Todo: Identify appropriate product type based on semantic search using the product document



