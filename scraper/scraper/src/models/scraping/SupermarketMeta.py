from mongoengine import Document, ListField, StringField, ReferenceField, EmbeddedDocumentField, ObjectIdField
from scraper.src.models.scraping.ListPageMeta import ListPageMeta

class SuperMarketMeta(Document):
    _id = ObjectIdField(required=True, primary_key=True)

    # e.g: ASDA
    name = StringField(required=True, unique=True)

    # e.g: www.asda.com
    main_link = StringField(required=True)

    pages = ListField(EmbeddedDocumentField(ListPageMeta))





