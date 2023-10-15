from dataclasses import dataclass, fields, field
from dataclasses_json import dataclass_json
from typing import List, Any
from models.Price import Price
from models.Nutrients import  Nutrients


@dataclass_json
@dataclass
class Product:
    product_id: str
    product_name: str
    price: Price
    ingredients: str
    nutrients: Nutrients
    customer_reviews: List[str]
    customer_rating: float
    product_link: str
    meat_alternative: bool
    meat_taste: bool
    meat_look: bool
    counterpart_products: List[str]
    plant_based: bool = False
    dairy: bool = False
