import json
import os

FILE = "data/ranks.json"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(FILE):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

RANK_LEVELS = {
    "عضو": 0,
    "مميز": 1,
    "ادمن": 2,
    "مشرف": 3,
    "مدير": 4,
    "منشئ": 5,
    "منشئ اساسي": 6,
    "مطور": 7,
    "مطور اساسي": 8
}

SHORT_RANKS = {
    "م": "مميز",
    "اد": "ادمن",
    "من": "منشئ",
    "مننن": "منشئ اساسي",
    "مط": "مطور",
    "مططط": "مطور اساسي"
}

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

def get_level(chat_id, user_id):
    return RANK_LEVELS.get(get_rank(chat_id, user_id), 0)

def has_rank(chat_id, user_id, min_rank="مميز"):
    return get_level(chat_id, user_id) >= RANK_LEVELS.get(min_rank, 1)

def remove_rank(chat_id, user_id):
    data = load()
    cid = str(chat_id)
    uid = str(user_id)

    if cid in data and uid in data[cid]:
        del data[cid][uid]

    save(data)

def promote_by_short(chat_id, user_id, short):
    rank = SHORT_RANKS.get(short)

    if not rank:
        return None

    set_rank(chat_id, user_id, rank)
    return rank
