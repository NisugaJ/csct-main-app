from enum import Enum

from mongoengine import FloatField, StringField, EnumField, EmbeddedDocument

class NutrientType(Enum):
    MAIN = "MAIN"
    VITAMIN = "VITAMIN"
    MINERAL = "MINERAL"
    OTHER = "OTHER"


class Nutrient(EmbeddedDocument):

    # e.g: carbohydrate
    name = StringField(required=False)
    name_raw = StringField(required=True)

    # e.g:  contains 40 mg
    value = FloatField(required=False)  # e.g: 40
    value_unit = StringField(required=False)  # e.g: mg

    # one portion = 100g or 100ml
    portion = FloatField(required=False)  # e.g: 100
    portion_raw = StringField(required=True)  # e.g: '100g'
    portion_unit = StringField(required=False)  # e.g: g

    category = EnumField(NutrientType, default=NutrientType.MAIN)
