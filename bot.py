import os, json, re, random, time
import telebot, requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8516176029:AAH-s3Y0nLAdmQN_LyeR3aS-tbK1XInMINY"
RAPID_API_KEY = "8d1aa779mshaeb22e8130d13c2p169c25jsnf375a4b0af2b"

OWNER_ID = 8065884629
BOT_USERNAME = "fadifvambot"
DEV_USERNAME = "fvamv"
FORCE_CHANNEL = "@fadifva"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DATA_FILE = "data.json"

DEFAULT_DATA = {
    "locks": {}, "ranks": {}, "users": {}, "groups": {},
    "replies": {}, "media": {}, "bank": {}, "robbers": {},
    "cooldowns": {}, "points": {}, "notify": True,
    "settings": {"welcome": True, "replies": True, "id_photo": True, "games": True}
}

waiting_reply = {}
quiz_games = {}

def save_data(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
        for k, v in DEFAULT_DATA.items():
            if k not in d:
                d[k] = v
        save_data(d)
        return d
    except:
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()

data = load_data()
def sid(x): return str(x)

def register_user(message):
    if not message.from_user: return
    uid = sid(message.from_user.id)
    if uid not in data["users"]:
        data["users"][uid] = {"name": message.from_user.first_name or "", "username": message.from_user.username or "ماكو"}
        save_data(data)
    if message.chat.type in ["group", "supergroup"]:
        data["groups"][sid(message.chat.id)] = {"title": message.chat.title or "", "username": message.chat.username or ""}
        save_data(data)

def get_locks(chat_id):
    cid = sid(chat_id)
    if cid not in data["locks"]:
        data["locks"][cid] = {
            "links": False, "photos": False, "videos": False, "stickers": False,
            "voice": False, "files": False, "animation": False,
            "forward": False, "bots": False, "all": False
        }
        save_data(data)
    return data["locks"][cid]

def save_media_message(message):
    if message.chat.type not in ["group", "supergroup"]: return
    if message.content_type not in ["photo", "video", "sticker", "animation", "document"]: return
    cid = sid(message.chat.id)
    data["media"].setdefault(cid, [])
    data["media"][cid].append({"message_id": message.message_id, "type": message.content_type})
    data["media"][cid] = data["media"][cid][-500:]
    save_data(data)

def is_subscribed(user_id):
    try:
        m = bot.get_chat_member(FORCE_CHANNEL, user_id)
        return m.status in ["member", "administrator", "creator"]
    except:
        return True

def check_sub(message):
    if message.from_user and not is_subscribed(message.from_user.id):
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("اشترك بالقناة", url="https://t.me/fadifva"))
        bot.reply_to(message, "⚠️ لازم تشترك بقناة البوت أولاً", reply_markup=kb)
        return False
    return True

def get_rank(chat_id, user_id):
    return data["ranks"].get(sid(chat_id), {}).get(sid(user_id))

def set_rank(chat_id, user_id, rank):
    data["ranks"].setdefault(sid(chat_id), {})
    data["ranks"][sid(chat_id)][sid(user_id)] = rank
    save_data(data)

def del_rank(chat_id, user_id):
    cid, uid = sid(chat_id), sid(user_id)
    if cid in data["ranks"] and uid in data["ranks"][cid]:
        del data["ranks"][cid][uid]
        save_data(data)

def is_admin(chat_id, user_id):
    try:
        m = bot.get_chat_member(chat_id, user_id)
        if m.status in ["creator", "administrator"]:
            return True
        return get_rank(chat_id, user_id) in ["مالك اساسي", "مالك", "منشئ", "مدير", "ادمن", "مشرف"]
    except:
        return False

def can_admin(message):
    if message.chat.type == "private":
        return False
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ هذا الأمر للمشرفين فقط")
        return False
    return True

def target_user(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❗ رد على رسالة الشخص")
        return None
    return message.reply_to_message.from_user

def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("1️⃣ أوامر الإدارة", callback_data="help_admin"))
    kb.add(InlineKeyboardButton("2️⃣ أوامر القفل والفتح", callback_data="help_locks"))
    kb.add(InlineKeyboardButton("3️⃣ أوامر الردود", callback_data="help_replies"))
    kb.add(InlineKeyboardButton("4️⃣ أوامر البنك", callback_data="help_bank"))
    kb.add(InlineKeyboardButton("5️⃣ أوامر الألعاب", callback_data="help_games"))
    kb.add(InlineKeyboardButton("6️⃣ أوامر الميوزك", callback_data="help_music"))
    kb.add(InlineKeyboardButton("⚙️ أوامر Dev", callback_data="help_dev"))
    return kb

def start_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("👨‍💻 المطور", url=f"https://t.me/{DEV_USERNAME}"))
    kb.add(InlineKeyboardButton("➕ اضفني للكروب", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"))
    kb.add(InlineKeyboardButton("💰 شراء بوت مشابه", url=f"https://t.me/{DEV_USERNAME}"))
    kb.add(InlineKeyboardButton("📚 الأوامر", callback_data="commands"))
    return kb

def owner_panel():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("➕ اضف رد", callback_data="owner_add_reply"))
    kb.add(InlineKeyboardButton("📜 الردود", callback_data="owner_replies"), InlineKeyboardButton("👥 المستخدمين", callback_data="owner_users"))
    kb.add(InlineKeyboardButton("🗑 حذف رد", callback_data="owner_del_reply"), InlineKeyboardButton("📊 الكروبات", callback_data="owner_groups"))
    kb.add(InlineKeyboardButton("📚 الأوامر", callback_data="commands"))
    return kb

HELP_ADMIN = """<b>❨ أوامر الإدارة ❩</b>

• حظر بالرد
• طرد بالرد
• كتم بالرد
• الغاء الحظر بالرد
• الغاء الكتم بالرد
• تقييد 5 / 10 / 30 / 60 / يوم / اسبوع بالرد
• رفع مشرف / تنزيل مشرف بالرد
• رفع ادمن / تنزيل ادمن بالرد
• رفع مميز / تنزيل مميز بالرد
• تنزيل الكل
• امسح بالرد
• مسح + العدد
• مسح الميديا
• مسح الصور
• مسح الملصقات
• صلاحياته بالرد
"""

HELP_LOCKS = """<b>❨ أوامر القفل والفتح ❩</b>

• قفل الروابط / فتح الروابط
• قفل الصور / فتح الصور
• قفل الفيديو / فتح الفيديو
• قفل الملصقات / فتح الملصقات
• قفل الفويسات / فتح الفويسات
• قفل الملفات / فتح الملفات
• قفل المتحركات / فتح المتحركات
• قفل التوجيه / فتح التوجيه
• قفل البوتات / فتح البوتات
• قفل الكل / فتح الكل
"""

HELP_REPLIES = """<b>❨ أوامر الردود ❩</b>

• الردود
• اضف رد
• مسح رد
• مسح الردود
"""

HELP_BANK = """<b>✜ أوامر البنك</b>

• انشاء حساب بنكي
• مسح حساب بنكي
• حسابي
• فلوسي
• تحويل + المبلغ بالرد
• راتب
• بخشيش
• زرف بالرد
• استثمار + المبلغ
• حظ + المبلغ
• مضاربه + المبلغ
• توب الفلوس
• توب الحراميه
"""

HELP_GAMES = """<b>❖ أوامر الألعاب</b>

• رياضيات
• احسب
• معاني
• عربي
• لغز
• حجره
• كت تويت
• افلام
• ز / زوجني
• طلاق
"""

HELP_MUSIC = """<b>❨ أوامر الميوزك ❩</b>

• يوت اسم الاغنية
"""

HELP_DEV = f"""<b>❨ أوامر Dev ❩</b>

• سورس
• المطور
• شراء بوت مشابه
• الاوامر
• لوحة
• ايدي
• تفعيل الايدي
• تعطيل الايدي

المطور: @{DEV_USERNAME}
القناة: {FORCE_CHANNEL}
"""

def bank_user(uid):
    return data["bank"].get(sid(uid))

def create_bank(uid):
    uid = sid(uid)
    if uid in data["bank"]: return False
    data["bank"][uid] = {"account": random.randint(100000, 999999), "money": 1000}
    save_data(data)
    return True

def cd_ok(uid, key, seconds):
    uid, now = sid(uid), int(time.time())
    data["cooldowns"].setdefault(uid, {})
    last = data["cooldowns"][uid].get(key, 0)
    if now - last < seconds:
        return False, seconds - (now - last)
    data["cooldowns"][uid][key] = now
    save_data(data)
    return True, 0

def parse_amount(text):
    try: return max(1, int(text.split()[1]))
    except: return None

@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.type != "private":
        return
    register_user(message)
    if not check_sub(message): return
    if message.from_user.id == OWNER_ID:
        bot.send_message(message.chat.id, "⚙️ لوحة تحكم المطور", reply_markup=owner_panel())
    else:
        bot.send_message(message.chat.id, "أهلاً بك في بوت فادي 🌷", reply_markup=start_buttons())

@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    try: bot.answer_callback_query(call.id)
    except: pass

    if call.data == "commands":
        bot.edit_message_text("📚 اختر قسم:", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    elif call.data == "help_admin":
        bot.edit_message_text(HELP_ADMIN, call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    elif call.data == "help_locks":
        bot.edit_message_text(HELP_LOCKS, call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    elif call.data == "help_replies":
        bot.edit_message_text(HELP_REPLIES, call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    elif call.data == "help_bank":
        bot.edit_message_text(HELP_BANK, call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    elif call.data == "help_games":
        bot.edit_message_text(HELP_GAMES, call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    elif call.data == "help_music":
        bot.edit_message_text(HELP_MUSIC, call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    elif call.data == "help_dev":
        bot.edit_message_text(HELP_DEV, call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    elif call.from_user.id == OWNER_ID and call.data == "owner_add_reply":
        waiting_reply[call.from_user.id] = {"step": "add_word"}
        bot.send_message(call.message.chat.id, "اكتب الكلمة:")
    elif call.from_user.id == OWNER_ID and call.data == "owner_del_reply":
        waiting_reply[call.from_user.id] = {"step": "del_word"}
        bot.send_message(call.message.chat.id, "اكتب الكلمة:")
    elif call.from_user.id == OWNER_ID and call.data == "owner_replies":
        bot.send_message(call.message.chat.id, "\n".join(data["replies"].keys()) or "ماكو ردود")
    elif call.from_user.id == OWNER_ID and call.data == "owner_users":
        bot.send_message(call.message.chat.id, f"عدد المستخدمين: {len(data['users'])}")
    elif call.from_user.id == OWNER_ID and call.data == "owner_groups":
        bot.send_message(call.message.chat.id, f"عدد الكروبات: {len(data['groups'])}")

@bot.message_handler(content_types=["new_chat_members"])
def welcome(message):
    register_user(message)
    for u in message.new_chat_members:
        if data["settings"].get("welcome", True):
            bot.send_message(message.chat.id, f"هلا {u.first_name} 🌷\nنورت الكروب")

@bot.message_handler(content_types=["text", "photo", "video", "sticker", "animation", "document", "audio", "voice"])
def handler(message):
    register_user(message)
    save_media_message(message)

    if message.chat.type != "private":
        if not check_sub(message): return

    text = message.text or ""
    locks = get_locks(message.chat.id)

    # تطبيق القفل فعلياً
    if message.chat.type != "private" and not is_admin(message.chat.id, message.from_user.id):
        should_delete = False
        if locks.get("all"): should_delete = True
        if locks.get("links") and text and ("http://" in text or "https://" in text or "t.me/" in text): should_delete = True
        if locks.get("photos") and message.content_type == "photo": should_delete = True
        if locks.get("videos") and message.content_type == "video": should_delete = True
        if locks.get("stickers") and message.content_type == "sticker": should_delete = True
        if locks.get("voice") and message.content_type == "voice": should_delete = True
        if locks.get("files") and message.content_type == "document": should_delete = True
        if locks.get("animation") and message.content_type == "animation": should_delete = True
        if locks.get("forward") and message.forward_date: should_delete = True

        if should_delete:
            try: bot.delete_message(message.chat.id, message.message_id)
            except: pass
            return

    if not text: return

    # ردود مضافة
    if message.from_user.id in waiting_reply:
        st = waiting_reply[message.from_user.id]
        if st["step"] == "add_word":
            waiting_reply[message.from_user.id] = {"step": "add_answer", "word": text}
            return bot.reply_to(message, "اكتب الرد:")
        if st["step"] == "add_answer":
            data["replies"][st["word"]] = text
            save_data(data)
            del waiting_reply[message.from_user.id]
            return bot.reply_to(message, "تم إضافة الرد")
        if st["step"] == "del_word":
            data["replies"].pop(text, None)
            save_data(data)
            del waiting_reply[message.from_user.id]
            return bot.reply_to(message, "تم حذف الرد")

    if data["settings"].get("replies", True) and text in data["replies"]:
        return bot.reply_to(message, data["replies"][text])

    # أوامر عامة
    if text in ["الاوامر", "الأوامر", "اوامر"]:
        return bot.reply_to(message, "📚 اختر قسم:", reply_markup=main_menu())
    if text == "سورس": return bot.reply_to(message, "أهلاً بك في سورس فادي 🔥")
    if text == "المطور": return bot.reply_to(message, f"👨‍💻 المطور: @{DEV_USERNAME}")
    if text == "شراء بوت مشابه": return bot.reply_to(message, f"للشراء راسل: @{DEV_USERNAME}")
    if text in ["لوحة", "لوحه"] and message.from_user.id == OWNER_ID:
        return bot.reply_to(message, "لوحة المطور", reply_markup=owner_panel())

    # القفل والفتح
    if text.startswith("قفل ") or text.startswith("فتح "):
        if not can_admin(message): return
        action = "قفل" if text.startswith("قفل ") else "فتح"
        name = text.replace(action + " ", "").strip()
        mapping = {
            "الروابط": "links", "الصور": "photos", "الفيديو": "videos",
            "الملصقات": "stickers", "الفويسات": "voice",
            "الملفات": "files", "المتحركات": "animation",
            "التوجيه": "forward", "البوتات": "bots", "الكل": "all"
        }
        if name not in mapping:
            return bot.reply_to(message, "❌ هذا القفل غير موجود")
        locks[mapping[name]] = action == "قفل"
        save_data(data)
        return bot.reply_to(message, f"{'🔒 تم قفل' if action == 'قفل' else '🔓 تم فتح'} {name}")

    # ايدي
    if text == "ايدي":
        username = f"@{message.from_user.username}" if message.from_user.username else "ماكو"
        txt = f"↶ USE = {username}\n↶ ID = <code>{message.from_user.id}</code>"
        if data["settings"].get("id_photo", True):
            try:
                photos = bot.get_user_profile_photos(message.from_user.id, limit=1)
                if photos.total_count > 0:
                    return bot.send_photo(message.chat.id, photos.photos[0][-1].file_id, caption=txt, reply_to_message_id=message.message_id)
            except: pass
        return bot.reply_to(message, txt)

    if text == "تفعيل الايدي":
        data["settings"]["id_photo"] = True; save_data(data)
        return bot.reply_to(message, "تم تفعيل الايدي بالصورة")
    if text == "تعطيل الايدي":
        data["settings"]["id_photo"] = False; save_data(data)
        return bot.reply_to(message, "تم تعطيل صورة الايدي")

    # الردود
    if text in ["اضف رد", "اضافة رد"]:
        waiting_reply[message.from_user.id] = {"step": "add_word"}
        return bot.reply_to(message, "اكتب الكلمة:")
    if text == "مسح رد":
        waiting_reply[message.from_user.id] = {"step": "del_word"}
        return bot.reply_to(message, "اكتب الكلمة:")
    if text == "الردود":
        return bot.reply_to(message, "\n".join(data["replies"].keys()) or "ماكو ردود")
    if text == "مسح الردود":
        if not can_admin(message): return
        data["replies"] = {}; save_data(data)
        return bot.reply_to(message, "تم مسح الردود")

    # إدارة
    if text in ["حظر", "طرد", "كتم", "الغاء الكتم", "الغاء الحظر"]:
        if not can_admin(message): return
        u = target_user(message)
        if not u: return
        try:
            if text == "حظر":
                bot.ban_chat_member(message.chat.id, u.id); bot.reply_to(message, "تم الحظر")
            elif text == "الغاء الحظر":
                bot.unban_chat_member(message.chat.id, u.id); bot.reply_to(message, "تم إلغاء الحظر")
            elif text == "طرد":
                bot.ban_chat_member(message.chat.id, u.id); bot.unban_chat_member(message.chat.id, u.id); bot.reply_to(message, "تم الطرد")
            elif text == "كتم":
                bot.restrict_chat_member(message.chat.id, u.id, can_send_messages=False); bot.reply_to(message, "تم الكتم")
            else:
                bot.restrict_chat_member(message.chat.id, u.id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
                bot.reply_to(message, "تم إلغاء الكتم")
        except:
            bot.reply_to(message, "تأكد البوت مشرف")
        return

    if text.startswith("تقييد "):
        if not can_admin(message): return
        u = target_user(message)
        if not u: return
        val = text.replace("تقييد ", "").strip()
        secs = {"5":300, "10":600, "30":1800, "60":3600, "ساعة":3600, "يوم":86400, "اسبوع":604800}.get(val, 300)
        try:
            bot.restrict_chat_member(message.chat.id, u.id, can_send_messages=False, until_date=int(time.time()) + secs)
            bot.reply_to(message, "تم التقييد")
        except:
            bot.reply_to(message, "تأكد البوت مشرف")
        return

    if text in ["امسح", "مسح بالرد"]:
        if not can_admin(message): return
        if not message.reply_to_message: return bot.reply_to(message, "رد على رسالة")
        try:
            bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            bot.delete_message(message.chat.id, message.message_id)
        except: bot.reply_to(message, "ما اكدر أمسح")
        return

    if text.startswith("مسح "):
        if not can_admin(message): return
        try:
            count = min(int(text.split()[1]), 100)
            for i in range(count + 1):
                try: bot.delete_message(message.chat.id, message.message_id - i)
                except: pass
        except:
            bot.reply_to(message, "اكتب: مسح 10")
        return

    if text in ["مسح الميديا", "مسح الصور", "مسح الملصقات"]:
        if not can_admin(message): return
        cid = sid(message.chat.id)
        saved = data["media"].get(cid, [])
        allowed = ["photo"] if text == "مسح الصور" else ["sticker", "animation"] if text == "مسح الملصقات" else ["photo", "video", "sticker", "animation", "document"]
        deleted, remain = 0, []
        for item in saved:
            if item["type"] in allowed:
                try: bot.delete_message(message.chat.id, item["message_id"]); deleted += 1
                except: pass
            else:
                remain.append(item)
        data["media"][cid] = remain; save_data(data)
        return bot.reply_to(message, f"تم مسح {deleted}")

    # بنك
    if text == "انشاء حساب بنكي":
        return bot.reply_to(message, "تم إنشاء حسابك ورصيدك 1000" if create_bank(message.from_user.id) else "عندك حساب")
    if text == "فلوسي":
        acc = bank_user(message.from_user.id)
        return bot.reply_to(message, f"فلوسك: {acc['money']}$" if acc else "ما عندك حساب")
    if text == "حسابي":
        acc = bank_user(message.from_user.id)
        return bot.reply_to(message, f"رقم حسابك: {acc['account']}" if acc else "ما عندك حساب")
    if text == "راتب":
        acc = bank_user(message.from_user.id)
        if not acc: return bot.reply_to(message, "سوّي حساب")
        ok, left = cd_ok(message.from_user.id, "salary", 1200)
        if not ok: return bot.reply_to(message, f"انتظر {left} ثانية")
        amount = random.randint(500, 1500); acc["money"] += amount; save_data(data)
        return bot.reply_to(message, f"راتبك: {amount}$")
    if text == "بخشيش":
        acc = bank_user(message.from_user.id)
        if not acc: return bot.reply_to(message, "سوّي حساب")
        ok, left = cd_ok(message.from_user.id, "tip", 600)
        if not ok: return bot.reply_to(message, f"انتظر {left} ثانية")
        amount = random.randint(100, 600); acc["money"] += amount; save_data(data)
        return bot.reply_to(message, f"بخشيش: {amount}$")

    # ألعاب
    if text in ["رياضيات", "احسب"]:
        a, b = random.randint(1, 20), random.randint(1, 20)
        quiz_games[message.chat.id] = str(a + b)
        return bot.reply_to(message, f"{a}+{b}=?")
    if message.chat.id in quiz_games and text.strip() == quiz_games[message.chat.id]:
        data["points"][sid(message.from_user.id)] = data["points"].get(sid(message.from_user.id), 0) + 1
        save_data(data); del quiz_games[message.chat.id]
        return bot.reply_to(message, "صح +1 نقطة")
    if text == "افلام":
        return bot.reply_to(message, random.choice(["Inception", "Interstellar", "The Dark Knight", "Fight Club", "Se7en"]))
    if text in ["ز", "زوجني"]:
        return bot.reply_to(message, "💍 تم زواجك")
    if text == "طلاق":
        return bot.reply_to(message, "💔 تم الطلاق")

    # يوتيوب
    if text.startswith("يوت "):
        query = text.replace("يوت ", "").strip()
        if not query: return bot.reply_to(message, "اكتب اسم الأغنية")
        wait = bot.reply_to(message, "🔎 جاري البحث...")
        try:
            search_res = requests.get("https://www.youtube.com/results", params={"search_query": query}, timeout=20)
            ids = re.findall(r"watch\?v=(\S{11})", search_res.text)
            if not ids: return bot.reply_to(message, "ما حصلت نتيجة")
            video_url = f"https://www.youtube.com/watch?v={ids[0]}"
            headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "yt-search-and-download-mp3.p.rapidapi.com"}
            api = requests.get("https://yt-search-and-download-mp3.p.rapidapi.com/mp3", headers=headers, params={"url": video_url}, timeout=60).json()
            print("API RESPONSE:", api)
            audio_url = api.get("link") or api.get("url") or api.get("audio") or api.get("download") or api.get("mp3") or api.get("downloadUrl") or api.get("download_url") or api.get("audioUrl")
            title = api.get("title") or query
            try: bot.delete_message(message.chat.id, wait.message_id)
            except: pass
            if not audio_url: return bot.reply_to(message, "ما حصلت رابط الصوت")
            return bot.send_audio(message.chat.id, audio_url, title=title, performer="Aurelius", caption=f"🎧 {title}", reply_to_message_id=message.message_id)
        except Exception as e:
            print("MUSIC ERROR:", e)
            return bot.reply_to(message, "صار خطأ أثناء جلب الأغنية")

print("Aurelius bot is running...")
bot.infinity_polling(skip_pending=True)
