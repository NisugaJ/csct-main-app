import json
import unittest


from scraper.src.models.product.Nutrient import Nutrient
from scraper.src.models.product.Nutrients import Nutrients
from scraper.src.models.product.Price import Price
from scraper.src.models.product.Product import Product


class ProductSchemaTest(unittest.TestCase):
    def test_json_to_object_conversion(self):
        product_data = json.loads(
            '{"product_id": "sdW76wqygd", "product_name": "Test name", "price": {"currency": "\u00a3", '
            '"retail_price": 2.34, "selling_price": 2.45}, "ingredients": "lorem lorem ipsum lorem lorem lorem", '
            '"nutrients": {"main_nutrients": [{"name": "carbohydrate", "value": 4.0, "value_unit": "mg", "portion": '
            '100.0, "portion_unit": "g"}], "minerals": [], "vitamins": []}, "customer_reviews": [], '
            '"customer_rating": 4.8, "product_link": "http://...........", "plant_based": true, "meat_alternative": '
            'true, "meat_taste": false, "meat_look": true, "counterpart_products": ["w3r@eqa", "asd2rqe3"]}')

        product_obj = Product(
                product_id='sdW76wqygd',
                product_name='Test name',
                price=Price(currency='£', retail_price=2.34, selling_price=2.45),
                ingredients='lorem lorem ipsum lorem lorem lorem',
                nutrients=Nutrients(
                    main_nutrients=[
                        Nutrient(name="carbohydrate", value=4.0, value_unit="mg", portion=100.0, portion_unit="g")
                    ],
                ),
                customer_rating=4.8,
                product_link='http://...........',
                plant_based=True,
                meat_alternative=True,
                meat_taste=False,
                meat_look=True,
                counterpart_products=['w3r@eqa', 'asd2rqe3']
                )

        self.assertEqual(
            product_data,
            product_obj.to_mongo().to_dict()
        )


if __name__ == '__main__':
    unittest.main()