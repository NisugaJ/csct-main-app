from mongoengine import FloatField, StringField, EmbeddedDocument


class Nutrient(EmbeddedDocument):

    # e.g: carbohydrate
    name = StringField(required=True)

    # e.g:  contains 40 mg
    value = FloatField(required=True)  # e.g: 40
    value_unit = StringField(required=True)  # e.g: mg

    # e.g: per 100 grams
    portion = FloatField(required=True)  # e.g: 100
    portion_unit = StringField(required=True)  # e.g: g
