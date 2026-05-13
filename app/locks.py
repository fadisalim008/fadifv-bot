import json
import os

FILE = "data/locks.json"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(FILE):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

LOCKS = {
    "الروابط": "links",
    "الرابط": "links",
    "الصور": "photos",
    "الفيديو": "video",
    "الفيدوهات": "video",
    "الفيديوهات": "video",
    "الملصقات": "stickers",
    "المتحركه": "animation",
    "المتحركات": "animation",
    "الملفات": "files",
    "الصوت": "voice",
    "التاك": "tag",
    "القنوات": "channels",
    "المعرفات": "username",
    "الانكليزيه": "english",
    "الفارسيه": "persian",
    "الدردشه": "chat",
    "البوتات": "bots",
    "التوجيه": "forward"
}

def load():
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def lock(chat_id, name):
    key = LOCKS.get(name)
    if not key:
        return False

    data = load()
    cid = str(chat_id)

    if cid not in data:
        data[cid] = {}

    data[cid][key] = True
    save(data)
    return True

def unlock(chat_id, name):
    key = LOCKS.get(name)
    if not key:
        return False

    data = load()
    cid = str(chat_id)

    if cid not in data:
        data[cid] = {}

    data[cid][key] = False
    save(data)
    return True

def is_locked(chat_id, key):
    data = load()
    return data.get(str(chat_id), {}).get(key, False)
