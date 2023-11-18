from mongoengine import StringField, FloatField, EmbeddedDocument


class PriceAndWeight(EmbeddedDocument):
    selling_price = FloatField(required=True)
    weight = StringField(required=True)
