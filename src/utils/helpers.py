import json
from typing import Any


def read_json(path: str) -> Any:
    with open(path, encoding="utf-8") as json_file:
        return json.load(json_file)


def save_to_json(data: list[dict[str, Any]], filename: str = "output.json") -> Any:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
