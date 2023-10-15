from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Nutrient:

    # e.g: carbohydrate
    name: str

    # e.g:  contains 40 mg
    value: float  # e.g: 40
    value_unit: str  # e.g: mg

    # e.g: per 100 grams
    portion: float  # e.g: 100
    portion_unit: str  # e.g: g
