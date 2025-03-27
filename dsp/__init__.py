import os

import json
with open(
        os.path.join(
            os.path.dirname(__file__), 
            r"resources/FractionateEverything.json"
        ), 
        "r"
    ) as f: 
    factory = json.load(f)

from .items import Item, ItemType, dsp_items
from .recipe import Recipe, RecipeType, dsp_recipes