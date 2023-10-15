from dataclasses import dataclass, field
from models.Nutrient import Nutrient
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Nutrients:
    main_nutrients: list[Nutrient] = field(default_factory=list)
    minerals:  list[Nutrient] = field(default_factory=list)
    vitamins:  list[Nutrient] = field(default_factory=list)