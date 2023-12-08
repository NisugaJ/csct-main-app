import decimal
import secrets
import os
from pathlib import Path
from types import NoneType


def get_a_unique_image_name():
    while True:
        random_string = secrets.token_hex(8) + ".png"
        file_path = os.path.join(f"{Path.cwd()}/app/public/images/", random_string)

        if not os.path.exists(file_path):
            break

    return random_string

def val(value, default_value="#not-found#"):
    invalid_data_types = [
        NoneType,
    ]

    if type(value) in invalid_data_types or value == "":
        return default_value
    elif type(value) in (int, float, type(decimal.Decimal)):
        return -99
    return value

def readable_product_type(product_type):
    if product_type is not None and product_type != "":
        return product_type.replace("_", " ").capitalize()