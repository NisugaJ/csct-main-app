from mongoengine import StringField, ListField, ReferenceField, EmbeddedDocument, ObjectIdField

from app.models.product.Product import Product


class ListPageMeta(EmbeddedDocument):

    _id = ObjectIdField(required=True, primary_key=True)

    # e.g:
    link = StringField(required=True, unique=True)

    #  html blocks of each product in the current page
    blocks = ListField(StringField(null=False))
    products = ListField(ReferenceField(Product))

    # Product Type
    product_type = StringField(required=True, choices=["meat", "dairy", "plant_based"])





