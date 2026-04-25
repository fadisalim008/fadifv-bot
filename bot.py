import os, json, re, random, time
import telebot, requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8516176029:AAH-s3Y0nLAdmQN_LyeR3aS-tbK1XInMINY"
RAPID_API_KEY = "8d1aaa7799mshaeb22e8130d13c2p169c25jsnf375a4b0af2b"

OWNER_ID = 8065884629
BOT_USERNAME = "fadifvambot"
DEV_USERNAME = "fvamv"
FORCE_CHANNEL = "@fadifva"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DATA_FILE = "data.json"

DEFAULT_DATA = {
    "locks": {}, "ranks": {}, "muted": {}, "users": {}, "groups": {},
    "replies": {}, "media": {}, "notify": True,
    "bank": {}, "robbers": {}, "cooldowns": {}
}

waiting_reply = {}
xo_games = {}
quiz_games = {}

MEANINGS = [("ما معنى كلمة الغيث؟", "المطر"), ("ما معنى كلمة الفؤاد؟", "القلب"), ("ما معنى كلمة الثرى؟", "التراب")]
ARABIC_Q = [("جمع كلمة كتاب؟", "كتب"), ("ضد كلمة طويل؟", "قصير"), ("مرادف كلمة جميل؟", "حسن")]
RIDDLES = [("له أسنان ولا يعض؟", "المشط"), ("يمشي بلا رجلين؟", "الوقت"), ("بيت بلا أبواب ولا شبابيك؟", "البيضة")]
CUT_TWEET = ["شنو حلمك؟", "شنو أكثر شي تحبه؟", "منو أقرب شخص إلك؟", "شنو بلد تتمنى تزوره؟"]

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

def save_data(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

data = load_data()

def sid(x): return str(x)

def register_user(message):
    if not message.from_user:
        return
    uid = sid(message.from_user.id)
    if uid not in data["users"]:
        data["users"][uid] = {"name": message.from_user.first_name or "", "username": message.from_user.username or "ماكو"}
        save_data(data)
        if data.get("notify", True):
            try:
                bot.send_message(OWNER_ID, f"🔔 دخول مستخدم جديد\n\n👤 الاسم: {message.from_user.first_name}\n🔗 اليوزر: @{message.from_user.username or 'ماكو'}\n🆔 الايدي: {message.from_user.id}")
            except:
                pass
    if message.chat.type in ["group", "supergroup"]:
        cid = sid(message.chat.id)
        if cid not in data["groups"]:
            data["groups"][cid] = {"title": message.chat.title or "", "username": message.chat.username or ""}
            save_data(data)

def save_media_message(message):
    if message.chat.type not in ["group", "supergroup"]:
        return
    if message.content_type not in ["photo", "video", "sticker", "animation", "document"]:
        return
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

def get_locks(chat_id):
    cid = sid(chat_id)
    if cid not in data["locks"]:
        data["locks"][cid] = {"links": False, "photos": False, "stickers": False, "videos": False, "forward": False, "bots": False, "all": False}
        save_data(data)
    return data["locks"][cid]

def get_rank(chat_id, user_id):
    return data["ranks"].get(sid(chat_id), {}).get(sid(user_id))

def set_rank(chat_id, user_id, rank):
    cid, uid = sid(chat_id), sid(user_id)
    data["ranks"].setdefault(cid, {})
    data["ranks"][cid][uid] = rank
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

def owner_panel():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("🟢➕ صانع الردود", callback_data="owner_add_reply"))
    kb.add(InlineKeyboardButton("🔵📜 الردود", callback_data="owner_replies"), InlineKeyboardButton("🔵👥 المستخدمين", callback_data="owner_users"))
    kb.add(InlineKeyboardButton("🔴🗑 حذف رد", callback_data="owner_del_reply"), InlineKeyboardButton("🔵📊 الكروبات", callback_data="owner_groups"))
    kb.add(InlineKeyboardButton("🟡🔔 إشعار الدخول", callback_data="owner_notify"))
    kb.add(InlineKeyboardButton("🔴 رجوع", callback_data="commands"))
    return kb

def start_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("👨‍💻 المطور", url=f"https://t.me/{DEV_USERNAME}"))
    kb.add(InlineKeyboardButton("➕ اضفني للكروب", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"))
    kb.add(InlineKeyboardButton("💰 شراء بوت مشابه", url=f"https://t.me/{DEV_USERNAME}"))
    kb.add(InlineKeyboardButton("📚 الأوامر", callback_data="commands"))
    return kb

HELP_ADMIN = """
<b>❨ أوامر الرفع والتنزيل ❩</b>

• رفع مشرف / تنزيل مشرف
• رفع مالك اساسي / تنزيل مالك اساسي
• رفع مالك / تنزيل مالك
• رفع مدير / تنزيل مدير
• رفع ادمن / تنزيل ادمن
• رفع مميز / تنزيل مميز
• تنزيل الكل بالرد
• تنزيل الكل بدون رد

<b>❨ أوامر المسح ❩</b>

• امسح بالرد
• مسح بالرد
• مسح + العدد
• مسح الميديا
• مسح الصور
• مسح الملصقات
• مسح الردود

<b>❨ أوامر الطرد الحظر الكتم ❩</b>

• حظر بالرد
• طرد بالرد
• كتم بالرد
• الغاء الحظر بالرد
• الغاء الكتم بالرد
"""

HELP_LOCKS = """
<b>❨ أوامر القفل والفتح ❩</b>

• قفل الروابط / فتح الروابط
• قفل الصور / فتح الصور
• قفل الفيديو / فتح الفيديو
• قفل الملصقات / فتح الملصقات
• قفل التوجيه / فتح التوجيه
• قفل البوتات / فتح البوتات
• قفل الكل / فتح الكل
"""

HELP_REPLIES = """
<b>❨ أوامر الردود ❩</b>

• الردود
• اضف رد
• مسح رد
• مسح الردود
• الرد + كلمة الرد
"""

HELP_BANK = """
<b>✜ أوامر البنك</b>

• انشاء حساب بنكي
• مسح حساب بنكي
• حسابي
• فلوسي
• تحويل
• راتب
• بخشيش
• زرف
• استثمار + المبلغ
• حظ + المبلغ
• مضاربه + المبلغ
• توب الفلوس
• توب الحراميه
"""

HELP_GAMES = """
<b>❖ أوامر الألعاب</b>

• تفعيل الالعاب
• تعطيل الالعاب
• xo
• رياضيات
• احسب
• معاني
• عربي
• لغز
• حجره
• كت تويت
• روليت
• ايموجي
• ارقام
• تخمين
"""

HELP_MUSIC = """
<b>❨ أوامر الميوزك ❩</b>

• يوت اسم الاغنية

مثال:
• يوت سيف عامر شجرة
"""

HELP_DEV = f"""
<b>❨ أوامر Dev ❩</b>

• سورس
• المطور
• شراء بوت مشابه
• الاوامر
• لوحة

المطور: @{DEV_USERNAME}
القناة: {FORCE_CHANNEL}
"""

def bank_user(uid):
    uid = sid(uid)
    if uid not in data["bank"]:
        return None
    return data["bank"][uid]

def create_bank(uid):
    uid = sid(uid)
    if uid in data["bank"]:
        return False
    acc = random.randint(100000, 999999)
    while any(v.get("account") == acc for v in data["bank"].values()):
        acc = random.randint(100000, 999999)
    data["bank"][uid] = {"account": acc, "money": 1000}
    save_data(data)
    return True

def cd_ok(uid, key, seconds):
    uid = sid(uid)
    now = int(time.time())
    data["cooldowns"].setdefault(uid, {})
    last = data["cooldowns"][uid].get(key, 0)
    if now - last < seconds:
        return False, seconds - (now - last)
    data["cooldowns"][uid][key] = now
    save_data(data)
    return True, 0

def parse_amount(text):
    try:
        return max(1, int(text.split()[1]))
    except:
        return None

def top_money():
    items = sorted(data["bank"].items(), key=lambda x: x[1].get("money", 0), reverse=True)[:10]
    if not items:
        return "ماكو حسابات بنكية."
    txt = "🏦 <b>توب الفلوس</b>\n\n"
    for i, (uid, info) in enumerate(items, 1):
        name = data["users"].get(uid, {}).get("name", uid)
        txt += f"{i}. {name} — {info.get('money', 0)}$\n"
    return txt

def top_robbers():
    items = sorted(data["robbers"].items(), key=lambda x: x[1], reverse=True)[:10]
    if not items:
        return "ماكو حرامية بعد."
    txt = "🦹 <b>توب الحراميه</b>\n\n"
    for i, (uid, count) in enumerate(items, 1):
        name = data["users"].get(uid, {}).get("name", uid)
        txt += f"{i}. {name} — {count} زرفه\n"
    return txt

def xo_keyboard(chat_id):
    game = xo_games[chat_id]
    kb = InlineKeyboardMarkup(row_width=3)
    b = game["board"]
    btns = [InlineKeyboardButton(b[i] if b[i] != " " else "⬜", callback_data=f"xo_{chat_id}_{i}") for i in range(9)]
    kb.add(btns[0], btns[1], btns[2])
    kb.add(btns[3], btns[4], btns[5])
    kb.add(btns[6], btns[7], btns[8])
    kb.add(InlineKeyboardButton("❌ إنهاء", callback_data=f"xo_end_{chat_id}"))
    return kb

def xo_winner(b):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,c,d in wins:
        if b[a] != " " and b[a] == b[c] == b[d]:
            return b[a]
    return "draw" if " " not in b else None

def ask_quiz(chat_id, qtype):
    if qtype == "math":
        a, b = random.randint(1, 20), random.randint(1, 20)
        op = random.choice(["+", "-", "*"])
        ans = str(eval(f"{a}{op}{b}"))
        q = f"🧮 جاوب:\n{a} {op} {b} = ؟"
    elif qtype == "meaning":
        q, ans = random.choice(MEANINGS)
        q = "📚 " + q
    elif qtype == "arabic":
        q, ans = random.choice(ARABIC_Q)
        q = "📝 " + q
    else:
        q, ans = random.choice(RIDDLES)
        q = "🧩 " + q
    quiz_games[chat_id] = ans.strip().lower()
    bot.send_message(chat_id, q)

@bot.message_handler(commands=["start"])
def start(message):
    register_user(message)
    if not check_sub(message): return
    if message.from_user.id == OWNER_ID:
        bot.send_message(message.chat.id, "⚙️ <b>لوحة تحكم المطور</b>\n\nاختر من الأزرار:", reply_markup=owner_panel())
    else:
        bot.send_message(message.chat.id, "أهلاً بك في بوت فادي المطور 🌷\nاختر من الأزرار بالأسفل 👇", reply_markup=start_buttons())

@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    try: bot.answer_callback_query(call.id)
    except: pass

    if call.data == "commands":
        return bot.edit_message_text("📚 قائمة أوامر بوت فادي\nاختر القسم:", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    if call.data == "help_admin":
        return bot.edit_message_text(HELP_ADMIN, call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    if call.data == "help_locks":
        return bot.edit_message_text(HELP_LOCKS, call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    if call.data == "help_replies":
        return bot.edit_message_text(HELP_REPLIES, call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    if call.data == "help_bank":
        return bot.edit_message_text(HELP_BANK, call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    if call.data == "help_games":
        return bot.edit_message_text(HELP_GAMES, call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    if call.data == "help_music":
        return bot.edit_message_text(HELP_MUSIC, call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    if call.data == "help_dev":
        return bot.edit_message_text(HELP_DEV, call.message.chat.id, call.message.message_id, reply_markup=main_menu())

    if call.data.startswith("owner_"):
        if call.from_user.id != OWNER_ID:
            return bot.answer_callback_query(call.id, "للمطور فقط", show_alert=True)
        if call.data == "owner_add_reply":
            waiting_reply[call.from_user.id] = {"step": "add_word"}
            return bot.send_message(call.message.chat.id, "اكتب الكلمة:")
        if call.data == "owner_del_reply":
            waiting_reply[call.from_user.id] = {"step": "del_word"}
            return bot.send_message(call.message.chat.id, "اكتب الكلمة التي تريد حذفها:")
        if call.data == "owner_replies":
            txt = "📜 الردود:\n\n" + "\n".join([f"• {k}" for k in data["replies"]]) if data["replies"] else "لا توجد ردود."
            return bot.send_message(call.message.chat.id, txt)
        if call.data == "owner_users":
            return bot.send_message(call.message.chat.id, f"👥 عدد المستخدمين: {len(data['users'])}")
        if call.data == "owner_groups":
            return bot.send_message(call.message.chat.id, f"📊 عدد الكروبات: {len(data['groups'])}")
        if call.data == "owner_notify":
            data["notify"] = not data.get("notify", True); save_data(data)
            return bot.send_message(call.message.chat.id, "🔔 إشعار الدخول: " + ("مفعل" if data["notify"] else "متوقف"))

    if call.data.startswith("xo_end_"):
        chat_id = int(call.data.replace("xo_end_", ""))
        xo_games.pop(chat_id, None)
        return bot.edit_message_text("تم إنهاء XO", call.message.chat.id, call.message.message_id)

    if call.data.startswith("xo_"):
        _, chat_id, pos = call.data.split("_")
        chat_id, pos = int(chat_id), int(pos)
        if chat_id not in xo_games: return
        game = xo_games[chat_id]
        if call.from_user.id != game["turn"]:
            return bot.answer_callback_query(call.id, "مو دورك", show_alert=True)
        if game["board"][pos] != " ":
            return bot.answer_callback_query(call.id, "المكان مأخوذ", show_alert=True)
        game["board"][pos] = game["symbols"][call.from_user.id]
        res = xo_winner(game["board"])
        if res:
            xo_games.pop(chat_id, None)
            return bot.edit_message_text("🤝 تعادل" if res == "draw" else f"🏆 فاز {call.from_user.first_name}", call.message.chat.id, call.message.message_id)
        p1, p2 = game["players"]
        game["turn"] = p2 if call.from_user.id == p1 else p1
        bot.edit_message_text("🎮 لعبة XO", call.message.chat.id, call.message.message_id, reply_markup=xo_keyboard(chat_id))

@bot.message_handler(content_types=["new_chat_members"])
def welcome(message):
    register_user(message)
    for u in message.new_chat_members:
        bot.send_message(message.chat.id, f"هلا {u.first_name} 🌷\nنورت الكروب", reply_markup=start_buttons())

@bot.message_handler(content_types=["text", "photo", "video", "sticker", "animation", "document", "audio", "voice"])
def handler(message):
    register_user(message)
    save_media_message(message)
    if message.chat.type != "private" and not check_sub(message): return

    locks = get_locks(message.chat.id)
    text = message.text or ""

    if message.chat.type != "private":
        if locks.get("all") and not is_admin(message.chat.id, message.from_user.id):
            try: bot.delete_message(message.chat.id, message.message_id)
            except: pass
            return
        if locks.get("links") and text and ("http://" in text or "https://" in text or "t.me/" in text) and not is_admin(message.chat.id, message.from_user.id):
            try: bot.delete_message(message.chat.id, message.message_id)
            except: pass
            return
        if locks.get("photos") and message.content_type == "photo" and not is_admin(message.chat.id, message.from_user.id):
            try: bot.delete_message(message.chat.id, message.message_id)
            except: pass
            return
        if locks.get("videos") and message.content_type == "video" and not is_admin(message.chat.id, message.from_user.id):
            try: bot.delete_message(message.chat.id, message.message_id)
            except: pass
            return
        if locks.get("stickers") and message.content_type == "sticker" and not is_admin(message.chat.id, message.from_user.id):
            try: bot.delete_message(message.chat.id, message.message_id)
            except: pass
            return

    if not text: return

    if message.chat.id in quiz_games and text.strip().lower() == quiz_games[message.chat.id]:
        quiz_games.pop(message.chat.id, None)
        return bot.reply_to(message, f"✅ صح عليك {message.from_user.first_name}")

    if message.from_user.id in waiting_reply:
        st = waiting_reply[message.from_user.id]
        if st["step"] == "add_word":
            waiting_reply[message.from_user.id] = {"step": "add_answer", "word": text}
            return bot.reply_to(message, "اكتب الرد:")
        if st["step"] == "add_answer":
            data["replies"][st["word"]] = text; save_data(data); del waiting_reply[message.from_user.id]
            return bot.reply_to(message, "✅ تم إضافة الرد")
        if st["step"] == "del_word":
            data["replies"].pop(text, None); save_data(data); del waiting_reply[message.from_user.id]
            return bot.reply_to(message, "✅ تم حذف الرد")

    if text in data["replies"]:
        return bot.reply_to(message, data["replies"][text])

    if text in ["الاوامر", "الأوامر", "اوامر"]:
        return bot.reply_to(message, "📚 اختر قسم الأوامر:", reply_markup=main_menu())
    if text in ["لوحة", "لوحه"] and message.from_user.id == OWNER_ID:
        return bot.reply_to(message, "لوحة المطور", reply_markup=owner_panel())
    if text == "سورس": return bot.reply_to(message, "أهلاً بك في سورس فادي 🔥")
    if text == "المطور": return bot.reply_to(message, f"👨‍💻 المطور: @{DEV_USERNAME}")
    if text == "شراء بوت مشابه": return bot.reply_to(message, f"للشراء راسل: @{DEV_USERNAME}")

    if text in ["اضف رد", "اضافة رد"]:
        waiting_reply[message.from_user.id] = {"step": "add_word"}
        return bot.reply_to(message, "اكتب الكلمة:")
    if text == "مسح رد":
        waiting_reply[message.from_user.id] = {"step": "del_word"}
        return bot.reply_to(message, "اكتب الكلمة:")
    if text == "الردود":
        return bot.reply_to(message, "📜 الردود:\n" + "\n".join(data["replies"].keys()) if data["replies"] else "ماكو ردود")
    if text == "مسح الردود":
        if not can_admin(message): return
        data["replies"] = {}; save_data(data)
        return bot.reply_to(message, "✅ تم مسح الردود")

    if text == "انشاء حساب بنكي":
        return bot.reply_to(message, "✅ تم إنشاء حسابك البنكي ورصيدك 1000$" if create_bank(message.from_user.id) else "عندك حساب بنكي مسبقاً")
    if text == "مسح حساب بنكي":
        data["bank"].pop(sid(message.from_user.id), None); save_data(data)
        return bot.reply_to(message, "✅ تم مسح حسابك البنكي")
    if text == "حسابي":
        acc = bank_user(message.from_user.id)
        return bot.reply_to(message, f"🏦 رقم حسابك: <code>{acc['account']}</code>" if acc else "ما عندك حساب. اكتب: انشاء حساب بنكي")
    if text == "فلوسي":
        acc = bank_user(message.from_user.id)
        return bot.reply_to(message, f"💰 فلوسك: {acc['money']}$" if acc else "ما عندك حساب.")
    if text == "راتب":
        acc = bank_user(message.from_user.id)
        if not acc: return bot.reply_to(message, "سوّي حساب بنكي أولاً")
        ok, left = cd_ok(message.from_user.id, "salary", 1200)
        if not ok: return bot.reply_to(message, f"انتظر {left} ثانية")
        amount = random.randint(500, 1500); acc["money"] += amount; save_data(data)
        return bot.reply_to(message, f"💵 راتبك: {amount}$")
    if text == "بخشيش":
        acc = bank_user(message.from_user.id)
        if not acc: return bot.reply_to(message, "سوّي حساب بنكي أولاً")
        ok, left = cd_ok(message.from_user.id, "tip", 600)
        if not ok: return bot.reply_to(message, f"انتظر {left} ثانية")
        amount = random.randint(100, 600); acc["money"] += amount; save_data(data)
        return bot.reply_to(message, f"🎁 بخشيش: {amount}$")
    if text == "زرف":
        acc = bank_user(message.from_user.id)
        if not acc: return bot.reply_to(message, "سوّي حساب بنكي أولاً")
        if not message.reply_to_message: return bot.reply_to(message, "رد على شخص حتى تزرفه")
        victim = bank_user(message.reply_to_message.from_user.id)
        if not victim: return bot.reply_to(message, "الشخص ما عنده حساب")
        ok, left = cd_ok(message.from_user.id, "rob", 600)
        if not ok: return bot.reply_to(message, f"انتظر {left} ثانية")
        amount = min(victim["money"], random.randint(50, 500))
        victim["money"] -= amount; acc["money"] += amount
        data["robbers"][sid(message.from_user.id)] = data["robbers"].get(sid(message.from_user.id), 0) + 1
        save_data(data)
        return bot.reply_to(message, f"🦹 زرفت {amount}$")
    if text.startswith("تحويل "):
        acc = bank_user(message.from_user.id)
        if not acc: return bot.reply_to(message, "ما عندك حساب")
        amount = parse_amount(text)
        if not amount: return bot.reply_to(message, "اكتب: تحويل 100 بالرد")
        if not message.reply_to_message: return bot.reply_to(message, "رد على الشخص")
        other = bank_user(message.reply_to_message.from_user.id)
        if not other: return bot.reply_to(message, "الشخص ما عنده حساب")
        if acc["money"] < amount: return bot.reply_to(message, "فلوسك ما تكفي")
        acc["money"] -= amount; other["money"] += amount; save_data(data)
        return bot.reply_to(message, f"✅ تم تحويل {amount}$")
    if text.startswith("استثمار "):
        acc = bank_user(message.from_user.id); amount = parse_amount(text)
        if not acc or not amount: return bot.reply_to(message, "اكتب: استثمار 100")
        if acc["money"] < amount: return bot.reply_to(message, "فلوسك ما تكفي")
        profit = int(amount * random.randint(1, 15) / 100)
        acc["money"] += profit; save_data(data)
        return bot.reply_to(message, f"📈 ربحت {profit}$")
    if text.startswith("حظ "):
        acc = bank_user(message.from_user.id); amount = parse_amount(text)
        if not acc or not amount: return bot.reply_to(message, "اكتب: حظ 100")
        if acc["money"] < amount: return bot.reply_to(message, "فلوسك ما تكفي")
        if random.choice([True, False]):
            acc["money"] += amount; msg = f"🎲 فزت وربحت {amount}$"
        else:
            acc["money"] -= amount; msg = f"🎲 خسرت {amount}$"
        save_data(data); return bot.reply_to(message, msg)
    if text.startswith("مضاربه "):
        acc = bank_user(message.from_user.id); amount = parse_amount(text)
        if not acc or not amount: return bot.reply_to(message, "اكتب: مضاربه 100")
        if acc["money"] < amount: return bot.reply_to(message, "فلوسك ما تكفي")
        percent = random.randint(-90, 90); change = int(amount * percent / 100)
        acc["money"] += change; save_data(data)
        return bot.reply_to(message, f"📊 النسبة: {percent}%\nالنتيجة: {change}$")
    if text == "توب الفلوس": return bot.reply_to(message, top_money())
    if text == "توب الحراميه": return bot.reply_to(message, top_robbers())

    if text in ["امسح", "مسح بالرد"]:
        if not can_admin(message): return
        if not message.reply_to_message: return bot.reply_to(message, "رد على رسالة")
        try:
            bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            bot.delete_message(message.chat.id, message.message_id)
        except: bot.reply_to(message, "ما اكدر أمسح")
        return

    if text in ["مسح الميديا", "مسح الصور", "مسح الملصقات"]:
        if not can_admin(message): return
        cid = sid(message.chat.id); saved = data["media"].get(cid, [])
        allowed = ["photo"] if text == "مسح الصور" else ["sticker", "animation"] if text == "مسح الملصقات" else ["photo", "video", "sticker", "animation", "document"]
        deleted, remaining = 0, []
        for item in saved:
            if item["type"] in allowed:
                try: bot.delete_message(message.chat.id, item["message_id"]); deleted += 1
                except: pass
            else:
                remaining.append(item)
        data["media"][cid] = remaining; save_data(data)
        return bot.reply_to(message, f"✅ تم مسح {deleted} من الميديا")

    if text.startswith("مسح "):
        if not can_admin(message): return
        try:
            count = min(int(text.split()[1]), 100)
            for i in range(count + 1):
                try: bot.delete_message(message.chat.id, message.message_id - i)
                except: pass
        except: bot.reply_to(message, "اكتب: مسح 10")
        return

    if text in ["حظر", "طرد", "كتم", "الغاء الكتم", "الغاء الحظر"]:
        if not can_admin(message): return
        u = target_user(message)
        if not u: return
        try:
            if text == "حظر": bot.ban_chat_member(message.chat.id, u.id); bot.reply_to(message, "تم الحظر")
            elif text == "الغاء الحظر": bot.unban_chat_member(message.chat.id, u.id); bot.reply_to(message, "تم إلغاء الحظر")
            elif text == "طرد": bot.ban_chat_member(message.chat.id, u.id); bot.unban_chat_member(message.chat.id, u.id); bot.reply_to(message, "تم الطرد")
            elif text == "كتم": bot.restrict_chat_member(message.chat.id, u.id, can_send_messages=False); bot.reply_to(message, "تم الكتم")
            elif text == "الغاء الكتم": bot.restrict_chat_member(message.chat.id, u.id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True); bot.reply_to(message, "تم إلغاء الكتم")
        except: bot.reply_to(message, "تأكد البوت مشرف")
        return

    if text.startswith("رفع "):
        if not can_admin(message): return
        u = target_user(message)
        if not u: return
        rank = text.replace("رفع ", "").strip()
        allowed = ["مالك اساسي", "مالك", "منشئ", "مدير", "ادمن", "مشرف", "مميز", "هطف", "حمار", "كلب", "خروف", "بقلبي"]
        if rank not in allowed: return bot.reply_to(message, "هذه الرتبة غير موجودة")
        set_rank(message.chat.id, u.id, rank)
        return bot.reply_to(message, f"تم رفعه {rank}")
    if text.startswith("تنزيل "):
        if not can_admin(message): return
        if text == "تنزيل الكل":
            data["ranks"][sid(message.chat.id)] = {}; save_data(data)
            return bot.reply_to(message, "تم تنزيل كل الرتب")
        u = target_user(message)
        if not u: return
        del_rank(message.chat.id, u.id)
        return bot.reply_to(message, "تم تنزيل رتبته")

    if text.startswith("قفل ") or text.startswith("فتح "):
        if not can_admin(message): return
        action = "قفل" if text.startswith("قفل ") else "فتح"
        name = text.replace(action + " ", "").strip()
        mapping = {"الروابط":"links","الصور":"photos","الفيديو":"videos","الملصقات":"stickers","التوجيه":"forward","البوتات":"bots","الكل":"all"}
        if name not in mapping: return bot.reply_to(message, "هذا الأمر غير موجود")
        locks[mapping[name]] = action == "قفل"; save_data(data)
        return bot.reply_to(message, f"{'🔒 تم قفل' if action=='قفل' else '🔓 تم فتح'} {name}")

    if text == "xo":
        if not message.reply_to_message: return bot.reply_to(message, "رد على شخص")
        p1, p2 = message.from_user.id, message.reply_to_message.from_user.id
        if p1 == p2: return bot.reply_to(message, "ما تكدر تلعب ويا نفسك")
        xo_games[message.chat.id] = {"board":[" "]*9, "players":[p1,p2], "symbols":{p1:"❌",p2:"⭕"}, "turn":p1}
        return bot.reply_to(message, "🎮 بدأت لعبة XO", reply_markup=xo_keyboard(message.chat.id))
    if text in ["رياضيات", "احسب"]: return ask_quiz(message.chat.id, "math")
    if text == "معاني": return ask_quiz(message.chat.id, "meaning")
    if text == "عربي": return ask_quiz(message.chat.id, "arabic")
    if text == "لغز": return ask_quiz(message.chat.id, "riddle")
    if text == "حجره": return bot.reply_to(message, f"أنا اخترت: {random.choice(['حجرة','ورقة','مقص'])}")
    if text == "كت تويت": return bot.reply_to(message, random.choice(CUT_TWEET))
    if text in ["ارقام", "تخمين"]:
        n = random.randint(1, 10); quiz_games[message.chat.id] = str(n)
        return bot.reply_to(message, "خمن رقم من 1 إلى 10")
    if text == "ايموجي":
        em = random.choice(["😂", "❤️", "🔥", "😎", "😭"]); quiz_games[message.chat.id] = em
        return bot.reply_to(message, f"اكتب هذا الإيموجي: {em}")
    if text == "روليت":
        names = ["الأحمر", "الأسود"]
        return bot.reply_to(message, f"🎰 النتيجة: {random.choice(names)}")

    if text in ["زواج", "طلاق"]:
        if not message.reply_to_message: return bot.reply_to(message, "رد على شخص")
        return bot.reply_to(message, "💍 تم الزواج" if text == "زواج" else "💔 تم الطلاق")

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
            audio_url = api.get("link") or api.get("url") or api.get("audio") or api.get("download") or api.get("mp3")
            if not audio_url: return bot.reply_to(message, "ما حصلت رابط الصوت")
            try: bot.delete_message(message.chat.id, wait.message_id)
            except: pass
            return bot.send_audio(message.chat.id, audio_url, title=query, performer="Aurelius", reply_to_message_id=message.message_id)
        except Exception as e:
            print("MUSIC ERROR:", e)
            return bot.reply_to(message, "صار خطأ أثناء جلب الأغنية")

print("Aurelius bot is running...")
bot.infinity_polling(skip_pending=True)
