from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Price:
    currency: str
    retail_price: float
    selling_price: float