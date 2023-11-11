from mongoengine import StringField, FloatField, EmbeddedDocument


class Price(EmbeddedDocument):
    currency = StringField(required=True)
    retail_price = FloatField(required=True)
    selling_price = FloatField(required=True)
