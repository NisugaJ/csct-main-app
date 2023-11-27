from enum import Enum


class UKSupermarkets(Enum):
    TESCO = "TESCO"
    ASDA = "ASDA"
    SAINSBURYS = "SAINSBURYS"
    MORRISONS = "MORRISONS"
    WAITROSE = "WAITROSE"
    ALDI = "ALDI"
    LIDL = "LIDL"
    CO_OP = "CO-OP"

def supermarket_prefix(supermarket_enum):
    if type(supermarket_enum) is UKSupermarkets:
        return supermarket_enum.value + "_"
    else:
        return ""