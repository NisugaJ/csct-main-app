from app.models.product.Product import Product
from utils.utils import readable_product_type

def make_passages():
    products = Product.objects()

    passages = []

    for product in products:
        passages.append(
            f"The price of {product.product_name} is {product.price.raw_selling_price} and ingredients are {product.ingredients}.It is a {readable_product_type(product.product_type.value)} product. View the product at {product.product_url}. It has a customer rating of {product.customer_rating}.\n"
        )

    return passages