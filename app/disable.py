import json
import os

FILE = "data/disable.json"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(FILE):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

def load():
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_disabled(chat_id, feature):
    data = load()
    return data.get(str(chat_id), {}).get(feature, False)

def disable_feature(chat_id, feature):
    data = load()

    if str(chat_id) not in data:
        data[str(chat_id)] = {}

    data[str(chat_id)][feature] = True
    save(data)

def enable_feature(chat_id, feature):
    data = load()

    if str(chat_id) not in data:
        data[str(chat_id)] = {}

    data[str(chat_id)][feature] = False
    save(data)

FEATURES = {
    "الالعاب": "games",
    "يوتيوب": "youtube",
    "الذكاء": "ai",
    "البنك": "bank",
    "الترفيه": "fun"
}
