from fastapi import APIRouter
from langchain.tools import json
import json

from app.models.product.Product import Product

products_router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@products_router.get("/all")
def get_all_products():
    products = Product.objects().aggregate([
        {
            "$project": {
                "product_name": 1,
                "product_id": 1
            }
        }
    ])

    response = []
    for product in products:
        response.append({
            "product_id": product['product_id'],
            "product_name": product['product_name']
        })

    return response
