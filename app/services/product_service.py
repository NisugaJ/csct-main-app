from app.models.product.Product import Product, ProductType
from utils.utils import readable_product_type

def make_passage(product: Product):
    nutrients = [f"{nutrient.name_raw}: {nutrient.portion_raw}" for nutrient in product.nutrients]

    passage = (f"The product {product.product_name} is a {ProductType(product.product_type).value.replace('_', '-').lower()} product and "
               f"ingredients are {product.ingredients}. "
               f"product. View the product at {product.product_url}. It has a customer rating of "
               f"{product.customer_rating}. "
               f"The selling price is £{product.price.selling_price}. "
               f"The selling weight is {product.price.raw_weight}. "
               f"It has below nutrients.\n "
               )

    for nutri in nutrients:
        passage += f"{nutri} \n"

    print(passage)

    return passage