from typing import Union

from fastapi import APIRouter
from langchain.tools import json
import json

from app.models.product.Product import Product

products_router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@products_router.get("/all")
def get_all_products(type: Union[str, None] = None):

    if type == "PLANT_BASED":
        filter_ = {
            "product_type": "PLANT_BASED"
        }
    elif type == "ANIMAL_BASED":
        filter_ = {
            "product_type": "ANIMAL_BASED"
        }
    else:
        filter_ = {}

    products = Product.objects().aggregate([
        {
            "$project": {
                "product_id": 1,
                "product_name": 1,
                "product_type": 1,
            },
        },
        {
            "$match": filter_
        }
    ])

    response = []
    for product in products:
        response.append({
            "product_id": product['product_id'],
            "product_name": product['product_name'],
            "product_type": product['product_type']
        })

    return response
