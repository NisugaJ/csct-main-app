from datetime import datetime
from enum import Enum
from price_parser import Price

from mongoengine import Document,\
    StringField,\
    FloatField,\
    BooleanField,\
    ListField,\
    ReferenceField,\
    EmbeddedDocumentField,\
    DateTimeField,\
    signals,\
    EmbeddedDocumentListField,\
    EnumField

from app.models.product.Nutrient import Nutrient
from app.models.product.Price import PriceAndWeight

class ProductType(Enum):
    MEAT = "MEAT"
    DAIRY = "DAIRY"
    VEGETARIAN = "VEGETARIAN"
    VEGAN = "VEGAN"
    MEAT_ALTERNATIVE = "MEAT_ALTERNATIVE"
    DAIRY_ALTERNATIVE = "DAIRY_ALTERNATIVE"

class Product(Document):
    product_id = StringField(required=True, unique=True)
    product_name = StringField(required=True)
    price = EmbeddedDocumentField(document_type=PriceAndWeight)
    ingredients = StringField()
    nutrients = EmbeddedDocumentListField(document_type=Nutrient)
    customer_rating = FloatField()
    product_url = StringField(required=True, unique=True)
    product_type = EnumField(ProductType)
    counterpart_products = ListField(ReferenceField('self'))

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField()

    @signals.pre_save.connect
    def update_updated_at(sender, document, **kwargs):
        document.updated_at = datetime.utcnow()

    @signals.pre_save_post_validation.connect
    def update_product_type(self, sender, document, **kwargs):
        document.detect_product_type(document)

        document.price.selling_price = Price.fromstring(document.price.raw_selling_price).amount_float

    def detect_product_type(self, document):
        product_context = document.product_name.lower().join(document.ingredients.lower().split())

        meat_keywords = set(['seafood', 'carmine', 'salmon', 'royal jelly', 'ostrich', 'tallow', 'Faggots', 'potted meat', 'organ meat', 'broth', 'sausages', 'smoked haddock', 'cod', 'bangers', 'animal fat', 'beef', 'suet', 'stock', 'roe', 'lobster', 'plaice', 'elk', 'veal', 'haggis', 'wild boar', 'smoked mackerel', 'clams', 'intestines', 'cochineal', 'sole', 'Scotch egg', 'alligator', 'kidney', 'pies', 'cured meat', 'catfish', 'Bury black pudding', 'goose', 'liver', 'smoked salmon', 'lamb', 'black pudding', 'meat extract', 'haddock', 'bone marrow', 'bison', 'collagen', 'gelatin', 'mussels', 'fish roe', 'pork', 'honey', 'kippers', 'kangaroo', 'tripe', 'game bird', 'swordfish', 'duck', 'pheasant', 'jerky', 'offal', 'caviar', 'rennet', 'goat', 'white pudding', 'trout', 'bacon', 'chicken', 'partridge', 'biltong', 'pepperoni', 'whey', 'ham', 'cumberland sausage', 'meat by-products', 'grouse', 'shrimp', 'fish', 'tilapia', 'turkey', 'shellfish', 'raccoon', 'corned beef', 'venison', 'rabbit', 'isinglass', 'albumen', 'pasties', 'beef dripping', 'crab', 'sausage', 'Lincolnshire sausage', 'salami', 'heart', 'quail', 'hare', 'mutton', 'smoked meat', 'smoked trout', 'game meat', 'wild game', 'meatballs', 'sardines', 'tuna', 'anchovies', 'lard'])

        for keyword in meat_keywords:
            if keyword in product_context:
                document.product_type = ProductType.MEAT
                print("Changed product type to MEAT")

        plant_based_keywords = set(["vegan", "plant-based", "plant based", "vegetarian", "cruelty-free", "animal-free", "non-dairy", "meatless",
            "dairy-free", "egg-free", "plant-powered", "no animal ingredients", "vegetable-based", "herbivore-friendly",
            "free from animal by-products", "ethical eating", "whole foods", "non-gmo", "nut-based", "legume-based",
            "tofu", "seitan", "tempeh", "plant proteins", "plant-derived", "meat alternatives", "dairy alternatives",
            "egg alternatives", "plant-forward", "meat-free", "plant-centric", "cruelty-free", "no animal testing",
            "soy-based", "gluten-free", "grain-based", "non-animal", "environmentally friendly",
            "conscious consumption", "sustainable food", "no animal-derived ingredients", "chickpea-based",
            "nutritional yeast", "mycroprotein", "plant extracts", "fruit-based", "whole grain", "no added hormones",
            "non-animal sourced additives", "chia seeds", "flax seeds", "algae-based", "no animal by-products"])

        for keyword in plant_based_keywords:
            if keyword in product_context:
                document.product_type = ProductType.MEAT_ALTERNATIVE
                print("Changed product type to MEAT_ALTERNATIVE")
