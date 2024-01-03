import concurrent
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
import utils

class ProductType(
    Enum
):
    ANIMAL_BASED = "ANIMAL_BASED"
    PLANT_BASED = "PLANT_BASED"


class Product(
    Document
):
    product_id = StringField(
        required=True,
        unique=True
    )
    product_name = StringField(
        required=True
    )
    price = EmbeddedDocumentField(
        document_type=PriceAndWeight
    )
    ingredients = StringField()
    nutrients = EmbeddedDocumentListField(
        document_type=Nutrient
    )
    customer_rating = FloatField()
    product_url = StringField(
        required=True,
        unique=True
    )
    product_image_url = StringField()
    product_type = EnumField(
        ProductType
    )
    counterpart_products = ListField(
        ReferenceField(
            'self'
        )
    )

    created_at = DateTimeField(
        default=datetime.now
    )
    updated_at = DateTimeField()

#
#     @classmethod
#     def pre_save(cls, sender, document, **kwargs):
#         document.detect_product_type(document)
#
#         if document.price.selling_price is None:
#             document.price.selling_price = Price.fromstring(document.price.raw_selling_price).amount_float
#
#         document.updated_at = datetime.now()
#
#     @classmethod
#     def detect_product_type(self, document):
#         product_context = document.product_name.lower()
#
#         dairy_keywords = {'milk', 'butter', 'cream', 'cheese', 'yogurt', 'curd', 'whey', 'butter', 'buttermilk',
#                           'sour cream', 'cottage cheese', 'whipped cream', 'evaporated milk', 'condensed milk', 'ghee',
#                           'mozzarella', 'cheddar', 'parmesan', 'ricotta', 'feta', 'cream cheese', 'provolone',
#                           'goat cheese', 'blue cheese', 'brie', 'camembert', 'colby', 'swiss cheese', 'monterey jack',
#                           'havarti', 'mascarpone', 'neufchâtel', 'queso fresco', 'queso blanco', 'paneer',
#                           'mexican crema', 'crème fraîche', 'malted milk', 'powdered milk', 'skim milk', 'whole milk',
#                           'low-fat milk', 'fat-free milk', '2% milk', '1% milk', 'heavy cream', 'half-and-half',
#                           'whole-milk yogurt', 'low-fat yogurt', 'fat-free yogurt', 'milk powder', 'milk solids',
#                           'casein', 'lactose', 'whey protein', 'curds', 'milkfat'}
#
#         plant_based_keywords = {"vegan", "plant-based", "plant based", "vegetarian", "cruelty-free", "animal-free",
#                                 "plant-powered", "no animal ingredients", "vegetable-based", "herbivore-friendly",
#                                 "free from animal by-products", "ethical eating", "whole foods", "non-gmo",
#                                 "plant-derived", "plant-forward", "plant-centric", "cruelty-free", "no animal testing",
#                                 "plant extracts", "non-animal sourced additives"}
#
#         dairy_alternative_keywords = plant_based_keywords.union({'soy milk', 'almond milk', 'coconut milk', 'vegan cheese', "Plant-Based","Dairy-Free", "Vegan", "Vegetarian", "Alternative", "Substitute", "Non-Dairy", "Milk Alternative", "Cheese Alternative", "Butter Substitute", "Yogurt Alternative", "Cream Substitute", "Ice Cream Alternative", "Non-Dairy Milk", "Non-Dairy Cheese", "Non-Dairy Butter", "Non-Dairy Yogurt", "Non-Dairy Cream", "Non-Dairy Ice Cream", "Vegan Milk", "Vegan Cheese", "Vegan Butter", "Vegan Yogurt", "Vegan Cream", "Vegan Ice Cream", "Plant Milk", "Nut Milk", "Soy Milk", "Almond Milk", "Coconut Milk", "Rice Milk", "Oat Milk", "Cashew Milk", "Hemp Milk", "Flax Milk", "Pea Milk", "Quinoa Milk", "Sunflower Milk", "Dairy Alternative", "Non-Dairy Option", "Vegan Option", "Plant-Based Option"})
#
#         meat_keywords = {'beef', 'chicken', 'pork', 'lamb', 'seafood', 'carmine', 'salmon', 'royal jelly', 'ostrich',
#                          'tallow', 'Faggots', 'potted meat', 'organ meat', 'broth', 'sausages', 'smoked haddock', 'cod',
#                          'bangers', 'animal fat', 'beef', 'suet', 'stock', 'roe', 'lobster', 'plaice', 'elk', 'veal',
#                          'haggis', 'wild boar', 'smoked mackerel', 'clams', 'intestines', 'cochineal', 'sole',
#                          'Scotch egg', 'alligator', 'kidney', 'pies', 'cured meat', 'catfish', 'Bury black pudding',
#                          'goose', 'liver', 'smoked salmon', 'lamb', 'black pudding', 'meat extract', 'haddock',
#                          'bone marrow', 'bison', 'collagen', 'gelatin', 'mussels', 'fish roe', 'pork', 'honey',
#                          'kippers', 'kangaroo', 'tripe', 'game bird', 'swordfish', 'duck', 'pheasant', 'jerky', 'offal',
#                          'caviar', 'rennet', 'goat', 'white pudding', 'trout', 'bacon', 'chicken', 'partridge',
#                          'biltong', 'pepperoni', 'whey', 'ham', 'cumberland sausage', 'meat by-products', 'grouse',
#                          'shrimp', 'fish', 'tilapia', 'turkey', 'shellfish', 'raccoon', 'corned beef', 'venison',
#                          'rabbit', 'isinglass', 'albumen', 'pasties', 'beef dripping', 'crab', 'sausage',
#                          'Lincolnshire sausage', 'salami', 'heart', 'quail', 'hare', 'mutton', 'smoked meat',
#                          'smoked trout', 'game meat', 'wild game', 'meatballs', 'sardines', 'tuna', 'anchovies', 'lard'}
#
#         meat_alternative_keywords = plant_based_keywords.union({'tofu', 'plant-based protein', 'vegan sausage', 'meat substitute', "non-dairy", "meatless", "dairy-free", "egg-free", "nut-based", "legume-based", "tofu", "seitan", "tempeh", "plant proteins", "plant-derived", "meat alternative", "egg alternative", "meat-free", "soy-based", "gluten-free", "grain-based", "non-animal", "no animal-derived ingredients", "chickpea-based", "nutritional yeast", "fruit-based", "whole grain", "chia seeds", "flax seeds", "algae-based", "no animal by-products"})
#
#         if document.product_type is not None:
#             prev_type = ProductType(document.product_type)
#         else:
#             return
#
#
#         if any(keyword in product_context for keyword in dairy_keywords):
#             document.product_type = ProductType.DAIRY
#         elif any(keyword in product_context for keyword in meat_keywords):
#             document.product_type = ProductType.MEAT
#         else:
#             if any(keyword in product_context for keyword in dairy_alternative_keywords):
#                 document.product_type = ProductType.DAIRY_ALTERNATIVE
#             if any(keyword in product_context for keyword in meat_alternative_keywords):
#                 document.product_type = ProductType.MEAT_ALTERNATIVE
#
#         Product.print_type_transition(document.product_name, prev_type.value, document.product_type.value)
#
#
#     @classmethod
#     def print_type_transition(self, product_name, previous_type, new_type):
#         print(f"\"{product_name}\",{previous_type},{new_type}")
#
#
#     @classmethod
#     def pre_bulk_insert(cls, sender, documents, **kwargs):
#         for document in documents:
#             document.pre_save(sender, document)
#
#
# # Attaching signals to Product document class
#
# signals.pre_save.connect(
#     Product.pre_save,
#     sender=Product
# )
#
# signals.pre_bulk_insert.connect(
#     Product.pre_bulk_insert,
#     sender=Product
# )