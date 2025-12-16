import json
from pathlib import Path

def load_recipes():
    data_path = Path(__file__).parent / "recipes.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)
