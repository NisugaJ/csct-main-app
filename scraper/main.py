import json

from models.Product import Product


if __name__ == '__main__':

    # Example usage:
    product_data = {
        "product_id": "sdW76wqygd",
        "product_name": "",
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
    }

    product_instance = Product.schema().loads(json.dumps(product_data))
    print(product_instance)


