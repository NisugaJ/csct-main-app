import unittest

from dotenv import load_dotenv

from app.db.connect import connect_to_db
from app.models.product.Product import Product


class ProductInsertionTest(
    unittest.TestCase
    ):
    product_item = {
        "product_url": "https://groceries.asda.com/product/vegan-cheese-spreads/cathedral-city-our-plant-based-dairy-free-cheese-alternative-280-g/1000383164817",
        "product_type": "MEAT_ALTERNATIVE", "product_id": "9864684987258_TEST_PRODUCT",
        "product_name": "Cathedral City Our Plant Based Dairy Free Cheese Alternative 280g",
        "price": {"raw_selling_price": "now \u00a33.00", "raw_weight": "280g", "raw_uom": "(\u00a323.08/kg)"},
        "ingredients": "Water, Coconut Oil, Modified Starch, Potato Starch, Bamboo Fibre, Flavourings, Salt, Fructose, Calcium, Acid (Lactic Acid), Gelling Agent (Agar), Colour (Carotenes)",
        "nutrients": [{"name_raw": "Energy", "portion_raw": "1476kJ / 356kcal"},
                      {"name_raw": "Fat", "portion_raw": "29.5g"},
                      {"name_raw": "(of which saturates)", "portion_raw": "25.5g"},
                      {"name_raw": "Carbohydrate", "portion_raw": "22.4g"},
                      {"name_raw": "(of which sugars)", "portion_raw": "0.6g"},
                      {"name_raw": "Protein", "portion_raw": "0.2g"}, {"name_raw": "Salt", "portion_raw": "2.2g"},
                      {"name_raw": "Calcium", "portion_raw": "160mg (20% RI)"},
                      {"name_raw": "RI = Reference Intake", "portion_raw": ""},
                      {"name_raw": "Approx. 9 servings per pack", "portion_raw": ""}], "customer_rating": 4.37}

    def setUp(self):
        load_dotenv()
        connect_to_db()

    def test_pre_save_callback(self):
        product = Product(**self.product_item)
        product.save()

        fetched_product = Product.objects.get(
            product_id=self.product_item["product_id"]
            )

        fetched_product.delete()

        print(
            f"product_id: {fetched_product.product_id}"
            )
        print(
            f"created_at: {fetched_product.created_at}"
            )
        print(
            f"updated_at: {fetched_product.updated_at}"
            )
        print(
            f"selling_price: {fetched_product.price.selling_price}"
            )

        self.assertIsNotNone(
            fetched_product.updated_at
            )
        self.assertIsNotNone(
            fetched_product.price.selling_price
            )

    def test_product_type_detection(self):
        product = Product(**self.product_item)

        print(f"Previous product_type: {product.product_type}")
        Product.detect_product_type(product)
        print(f"New product_type: {product.product_type}")


if __name__ == '__main__':
    unittest.main()
