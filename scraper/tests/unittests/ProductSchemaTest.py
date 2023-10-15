import json
import unittest

from models.Nutrient import Nutrient
from models.Nutrients import Nutrients
from models.Price import Price
from models.Product import Product


class ProductSchemaTest(unittest.TestCase):
    def test_json_to_object_conversion(self):

        product_data = json.dumps({
            "product_id": "sdW76wqygd",
            "product_name": "Test name",
            "price": {
                "currency": "£",
                "retail_price": 2.34,
                "selling_price": 2.45
            },
            "ingredients": "lorem lorem ipsum lorem lorem lorem",
            "nutrients": {
                "main_nutrients": [
                    {
                        "name": "carbohydrate",
                        "value": 4,
                        "value_unit": "mg",
                        "portion": 100,
                        "portion_unit": "g"
                    }
                ]
            },
            "customer_reviews": [],
            "customer_rating": 4.8,
            "product_link": "http://...........",
            "plant_based": True,
            "meat_alternative": True,
            "meat_taste": False,
            "meat_look": True,
            "counterpart_products": ["w3r@eqa", "asd2rqe3"]
        })

        self.assertEqual(Product.schema().loads(product_data),
                         Product(product_id='sdW76wqygd', product_name='Test name', price=Price(currency='£', retail_price=2.34, selling_price=2.45), ingredients='lorem lorem ipsum lorem lorem lorem', nutrients=Nutrients(main_nutrients=[Nutrient(name='carbohydrate', value=4.0, value_unit='mg', portion=100.0, portion_unit='g')], minerals=[], vitamins=[]), customer_reviews=[], customer_rating=4.8, product_link='http://...........', plant_based=True, meat_alternative=True, meat_taste=False, meat_look=True, counterpart_products=['w3r@eqa', 'asd2rqe3']))  # add assertion here


if __name__ == '__main__':
    unittest.main()