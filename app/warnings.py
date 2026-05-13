import json
import os

FILE = "data/warnings.json"

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

def add_warning(chat_id, user_id):

    data = load()

    cid = str(chat_id)
    uid = str(user_id)

    if cid not in data:
        data[cid] = {}

    data[cid][uid] = data[cid].get(uid, 0) + 1

    save(data)

    return data[cid][uid]

def get_warnings(chat_id, user_id):

    data = load()

    return data.get(str(chat_id), {}).get(str(user_id), 0)

def reset_warnings(chat_id, user_id):

    data = load()

    cid = str(chat_id)
    uid = str(user_id)

    if cid in data and uid in data[cid]:
        data[cid][uid] = 0

    save(data)
