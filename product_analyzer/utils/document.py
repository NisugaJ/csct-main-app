from langchain.schema import Document
import re

from app.models.product.Product import Product
from app.services.product_service import make_passage


def extract_number_from_str(string: str = None):
    number = 0
    if string:
        match = re.search(r'(\d+(?:\.\d+)?)', string)
        if match:
            number = float(match.group(1))

    return number

def get_doc_from_raw(raw_product: Product, use_case: "search" or "chat"):

    metadata = raw_product.to_mongo().to_dict()
    metadata.pop("nutrients")
    metadata.pop("price")
    metadata.pop("counterpart_products")

    for nutrient in raw_product.nutrients:
        if nutrient.name_raw and nutrient.portion_raw:
            nutri_name = nutrient.name_raw.lower().replace(" ", "_")
            val_per_100g = extract_number_from_str(nutrient.portion_raw)

            if val_per_100g > 0:
                metadata[f"nutrient_{nutri_name}"] = val_per_100g

    metadata[f"price_selling_price"] = raw_product.price.selling_price
    metadata[f"price_raw_uom"] = raw_product.price.raw_uom
    metadata[f"price_raw_weight"] = raw_product.price.raw_weight

    source_content = make_passage(product=raw_product)
    metadata[f"source"] = source_content

    if use_case == "search":
        page_content = raw_product.product_name
    elif use_case == "chat":
        page_content = source_content
    else:
        raise ValueError("use_case must be 'search' or 'chat'")

    doc = Document(
        page_content=page_content,
        metadata=metadata
    )

    return doc
