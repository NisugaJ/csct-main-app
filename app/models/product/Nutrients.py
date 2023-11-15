from mongoengine import ListField,  EmbeddedDocument, EmbeddedDocumentField

from app.models.product.Nutrient import Nutrient


class Nutrients(EmbeddedDocument):
    main_nutrients = ListField(EmbeddedDocumentField(Nutrient))
    minerals = ListField(EmbeddedDocumentField(Nutrient))
    vitamins = ListField(EmbeddedDocumentField(Nutrient))