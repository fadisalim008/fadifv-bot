import json
import os

FILE = "data/smart_ban.json"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(FILE):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

TYPE_MAP = {
    "photo": "الصور",
    "video": "الفيديوهات",
    "sticker": "الملصقات",
    "animation": "المتحركات",
    "document": "الملفات",
    "voice": "الصوت",
    "audio": "الصوتيات"
}

def load():
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_smart_ban(chat_id, user_id, content_type):
    data = load()
    cid = str(chat_id)
    uid = str(user_id)

    data.setdefault(cid, {})
    data[cid].setdefault(uid, [])

    if content_type not in data[cid][uid]:
        data[cid][uid].append(content_type)

    save(data)

def clear_smart_ban(chat_id, user_id):
    data = load()
    cid = str(chat_id)
    uid = str(user_id)

    if cid in data and uid in data[cid]:
        del data[cid][uid]

    save(data)

def is_smart_banned(chat_id, user_id, content_type):
    data = load()
    return content_type in data.get(str(chat_id), {}).get(str(user_id), [])

def smart_ban_name(content_type):
    return TYPE_MAP.get(content_type, content_type)
