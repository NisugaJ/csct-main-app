from mongoengine import StringField, FloatField, EmbeddedDocument


class PriceAndWeight(EmbeddedDocument):
    selling_price = FloatField()
    selling_size = StringField()
    selling_size_type = StringField()

    # 1 unit = 100g or 100ml
    unit_price = FloatField()
    unit_size_type = StringField()  # g,kg,ml,l

    raw_selling_price = StringField(
        required=True
    )
    raw_weight = StringField(required=True)
    raw_uom = StringField(required=True)
