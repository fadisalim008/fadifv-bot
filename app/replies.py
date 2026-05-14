import json
import os
import random

FILE = "data/replies.json"

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

def add_reply(chat_id, trigger, reply_text):

    data = load()

    cid = str(chat_id)

    data.setdefault(cid, {})
    data[cid].setdefault("normal", {})

    data[cid]["normal"][trigger] = reply_text

    save(data)

def delete_reply(chat_id, trigger):

    data = load()

    cid = str(chat_id)

    try:
        del data[cid]["normal"][trigger]
        save(data)
        return True
    except:
        return False

def get_reply(chat_id, text):

    data = load()

    cid = str(chat_id)

    return data.get(cid, {}).get("normal", {}).get(text)

def list_replies(chat_id):

    data = load()

    cid = str(chat_id)

    replies = data.get(cid, {}).get("normal", {})

    if not replies:
        return "لا توجد ردود"

    return "\n".join([f"- {x}" for x in replies])

# ===== الردود المميزة =====

def add_vip_reply(chat_id, trigger, reply_text):

    data = load()

    cid = str(chat_id)

    data.setdefault(cid, {})
    data[cid].setdefault("vip", {})

    data[cid]["vip"][trigger] = reply_text

    save(data)

def delete_vip_reply(chat_id, trigger):

    data = load()

    cid = str(chat_id)

    try:
        del data[cid]["vip"][trigger]
        save(data)
        return True
    except:
        return False

def get_vip_reply(chat_id, text):

    data = load()

    cid = str(chat_id)

    return data.get(cid, {}).get("vip", {}).get(text)

def list_vip_replies(chat_id):

    data = load()

    cid = str(chat_id)

    replies = data.get(cid, {}).get("vip", {})

    if not replies:
        return "لا توجد ردود مميزة"

    return "\n".join([f"- {x}" for x in replies])

# ===== الردود المتعددة =====

def add_multi_reply(chat_id, trigger, reply_text):

    data = load()

    cid = str(chat_id)

    data.setdefault(cid, {})
    data[cid].setdefault("multi", {})
    data[cid]["multi"].setdefault(trigger, [])

    data[cid]["multi"][trigger].append(reply_text)

    save(data)

def get_multi_reply(chat_id, text):

    data = load()

    cid = str(chat_id)

    replies = data.get(cid, {}).get("multi", {}).get(text)

    if not replies:
        return None

    return random.choice(replies)

def list_multi_replies(chat_id):

    data = load()

    cid = str(chat_id)

    replies = data.get(cid, {}).get("multi", {})

    if not replies:
        return "لا توجد ردود متعددة"

    return "\n".join([f"- {x}" for x in replies])

def clear_replies(chat_id):

    data = load()

    cid = str(chat_id)

    if cid in data:
        data[cid]["normal"] = {}

    save(data)

def clear_vip_replies(chat_id):

    data = load()

    cid = str(chat_id)

    if cid in data:
        data[cid]["vip"] = {}

    save(data)

def clear_multi_replies(chat_id):

    data = load()

    cid = str(chat_id)

    if cid in data:
        data[cid]["multi"] = {}

    save(data)
