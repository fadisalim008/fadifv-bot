import json
import os

FILE = "data/ranks.json"

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

def set_rank(chat_id, user_id, rank):

    data = load()

    cid = str(chat_id)
    uid = str(user_id)

    if cid not in data:
        data[cid] = {}

    data[cid][uid] = rank

    save(data)

def get_rank(chat_id, user_id):

    data = load()

    return data.get(str(chat_id), {}).get(str(user_id), "عضو")

def remove_rank(chat_id, user_id):

    data = load()

    cid = str(chat_id)
    uid = str(user_id)

    if cid in data and uid in data[cid]:
        del data[cid][uid]

    save(data)

RANKS = [
    "مميز",
    "ادمن",
    "مشرف",
    "مدير",
    "منشئ",
    "منشئ اساسي",
    "مالك"
]
