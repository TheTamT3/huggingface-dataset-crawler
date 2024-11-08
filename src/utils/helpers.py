import json


def read_json(path):
    with open(path, encoding="utf-8") as json_file:
        return json.load(json_file)


def save_to_json(data, filename="output.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
