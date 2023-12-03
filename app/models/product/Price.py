from mongoengine import StringField, FloatField, EmbeddedDocument


class PriceAndWeight(EmbeddedDocument):
    selling_price = FloatField()
    weight = StringField()

    raw_selling_price = StringField(
        required=True
    )
    raw_weight = StringField( required=True)
    raw_uom = StringField( required=True)
