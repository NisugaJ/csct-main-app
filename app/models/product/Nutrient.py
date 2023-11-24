from mongoengine import FloatField, StringField, EnumField, EmbeddedDocument


class Nutrient(EmbeddedDocument):

    # e.g: carbohydrate
    name = StringField(required=False)
    name_raw = StringField(required=True)

    # e.g:  contains 40 mg
    value = FloatField(required=False)  # e.g: 40
    value_unit = StringField(required=False)  # e.g: mg

    # e.g: per 100 grams
    portion = FloatField(required=False)  # e.g: 100
    portion_raw = StringField(required=True)  # e.g: '100g'
    portion_unit = StringField(required=False)  # e.g: g

    category = EnumField(enum=['main', 'minerals', 'vitamins'], default='main')
