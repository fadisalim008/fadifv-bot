import json
import os

DATA_FILE = "data.json"

DEFAULT_DATA = {
    "groups": {},
    "users": {},
    "warns": {},
    "mutes": {},
    "bans": {},
    "restrictions": {},
    "points": {},
    "messages": {},
    "games": {},
    "bank": {},
    "replies": {}
}

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()
