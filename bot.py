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
    "locks": {}, "ranks": {}, "muted": {}, "users": {}, "groups": {},
    "replies": {}, "media": {}, "notify": True,
    "bank": {}, "robbers": {}, "cooldowns": {},
    "settings": {"welcome": True, "replies": True, "id_photo": True, "games": True},
    "join_info": {}, "points": {}
}

waiting_reply = {}
xo_games = {}
quiz_games = {}

MEANINGS = [
    ("ما معنى كلمة الغيث؟", "المطر"),
    ("ما معنى كلمة الفؤاد؟", "القلب"),
    ("ما معنى كلمة الثرى؟", "التراب")
]

ARABIC_Q = [
    ("جمع كلمة كتاب؟", "كتب"),
    ("ضد كلمة طويل؟", "قصير"),
    ("مرادف كلمة جميل؟", "حسن")
]

RIDDLES = [
    ("له أسنان ولا يعض؟", "المشط"),
    ("يمشي بلا رجلين؟", "الوقت"),
    ("بيت بلا أبواب ولا شبابيك؟", "البيضة")
]

CUT_TWEET = [
    "شنو حلمك؟",
    "شنو أكثر شي تحبه؟",
    "منو أقرب شخص إلك؟",
    "شنو بلد تتمنى تزوره؟"
]

MOVIES = [
    "The Godfather",
    "Inception",
    "Interstellar",
    "Fight Club",
    "The Dark Knight",
    "Gladiator",
    "Parasite",
    "Se7en"
]

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

def sid(x):
    return str(x)

def register_user(message):
    if not message.from_user:
        return

    uid = sid(message.from_user.id)

    if uid not in data["users"]:
        data["users"][uid] = {
            "name": message.from_user.first_name or "",
            "username": message.from_user.username or "ماكو"
        }
        save_data(data)

        if data.get("notify", True):
            try:
                bot.send_message(
                    OWNER_ID,
                    f"🔔 دخول مستخدم جديد\n\n"
                    f"👤 الاسم: {message.from_user.first_name}\n"
                    f"🔗 اليوزر: @{message.from_user.username or 'ماكو'}\n"
                    f"🆔 الايدي: {message.from_user.id}"
                )
            except:
                pass

    if message.chat.type in ["group", "supergroup"]:
        cid = sid(message.chat.id)
        if cid not in data["groups"]:
            data["groups"][cid] = {
                "title": message.chat.title or "",
                "username": message.chat.username or ""
            }
            save_data(data)

def save_media_message(message):
    if message.chat.type not in ["group", "supergroup"]:
        return

    if message.content_type not in ["photo", "video", "sticker", "animation", "document"]:
        return

    cid = sid(message.chat.id)
    data["media"].setdefault(cid, [])
    data["media"][cid].append({
        "message_id": message.message_id,
        "type": message.content_type
    })
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
        data["locks"][cid] = {
            "links": False,
            "photos": False,
            "stickers": False,
            "videos": False,
            "forward": False,
            "bots": False,
            "all": False,
            "voice": False,
            "files": False,
            "animation": False,
            "channels": False
        }
        save_data(data)

    return data["locks"][cid]

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
        return get_rank(chat_id, user_id) in [
            "مالك اساسي", "مالك", "منشئ", "مدير", "ادمن", "مشرف"
        ]
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
    kb.add(
        InlineKeyboardButton("🔵📜 الردود", callback_data="owner_replies"),
        InlineKeyboardButton("🔵👥 المستخدمين", callback_data="owner_users")
    )
    kb.add(
        InlineKeyboardButton("🔴🗑 حذف رد", callback_data="owner_del_reply"),
        InlineKeyboardButton("🔵📊 الكروبات", callback_data="owner_groups")
    )
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
• تقييد 5 / 10 / 30 / 60 / يوم / اسبوع بالرد
• الغاء الحظر بالرد
• الغاء الكتم بالرد
• الغاء التقييد بالرد
• صلاحياته بالرد
"""

HELP_LOCKS = """
<b>❨ أوامر القفل والفتح ❩</b>

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
• افلام
• ز / زوجني
• طلاق
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
• تفعيل الايدي
• تعطيل الايدي
• منو ضافني

المطور: @{DEV_USERNAME}
القناة: {FORCE_CHANNEL}
"""

def bank_user(uid):
    return data["bank"].get(sid(uid))

def create_bank(uid):
    uid = sid(uid)

    if uid in data["bank"]:
        return False

    acc = random.randint(100000, 999999)
    data["bank"][uid] = {
        "account": acc,
        "money": 1000
    }
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

def add_point(uid):
    uid = sid(uid)
    data["points"][uid] = data["points"].get(uid, 0) + 1
    save_data(data)

@bot.message_handler(commands=["start"])
def start(message):
    register_user(message)

    if not check_sub(message):
        return

    # فقط بالبريفات تظهر ازرار المطور
    if message.chat.type == "private":
        bot.send_message(
            message.chat.id,
            "أهلاً بك 🌷\nاختر من الأزرار:",
            reply_markup=start_buttons()
        )
    else:
        bot.reply_to(message, "اهلاً 👋 اكتب الاوامر")

@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    try:
        bot.answer_callback_query(call.id)
    except:
        pass

    if call.data == "commands":
        bot.edit_message_text(
            "📚 اختر قسم:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu()
        )

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


@bot.message_handler(content_types=["text","photo","video","sticker","animation","document"])
def handler(message):
    register_user(message)
    save_media_message(message)

    if message.chat.type != "private":
        if not check_sub(message):
            return

    text = message.text or ""

    # ================= ID =================
    if text == "ايدي":
        if data["settings"].get("id_photo", True):
            bot.send_photo(
                message.chat.id,
                "https://i.imgur.com/8z1Z6hR.jpg",
                caption=f"""⇜ USE = @{message.from_user.username or "ماكو"}
⇜ ID = {message.from_user.id}""",
                reply_to_message_id=message.message_id
            )
        else:
            bot.reply_to(message, f"🆔 ايديك: {message.from_user.id}")

    elif text == "تعطيل الايدي":
        data["settings"]["id_photo"] = False
        save_data(data)
        bot.reply_to(message, "❌ تم تعطيل صورة الايدي")

    elif text == "تفعيل الايدي":
        data["settings"]["id_photo"] = True
        save_data(data)
        bot.reply_to(message, "✅ تم تفعيل صورة الايدي")

    # ================= مسح ميديا =================
    elif text == "مسح الميديا":
        if not can_admin(message): return
        cid = sid(message.chat.id)
        for m in data["media"].get(cid, []):
            try:
                bot.delete_message(message.chat.id, m["message_id"])
            except:
                pass
        data["media"][cid] = []
        save_data(data)
        bot.reply_to(message, "🗑 تم تنظيف الميديا")

    elif text in ["امسح","مسح"] and message.reply_to_message:
        if not can_admin(message): return
        try:
            bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

    # ================= زواج =================
    elif text in ["ز","زوجني"]:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
            bot.reply_to(message, f"💍 تم زواجك من @{user.username or user.first_name}")
        else:
            bot.reply_to(message, "رد على شخص")

    elif text == "طلاق":
        bot.reply_to(message, "💔 تم الطلاق")

    # ================= تقييد =================
    elif text.startswith("تقييد"):
        if not can_admin(message): return
        user = target_user(message)
        if not user: return

        times = {
            "5":300, "10":600, "30":1800, "60":3600,
            "يوم":86400, "اسبوع":604800
        }

        t = text.split()[1] if len(text.split()) > 1 else "5"
        sec = times.get(t,300)

        bot.restrict_chat_member(
            message.chat.id, user.id,
            can_send_messages=False,
            until_date=int(time.time()) + sec
        )
        bot.reply_to(message, f"⛔ تم تقييده {t}")

    # ================= صلاحيات =================
    elif text == "صلاحياته" and message.reply_to_message:
        m = bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)

        txt = f"""⇜ {m.status}
⇜ الصلاحيات ↓

حذف الرسائل {'ꪜ' if m.can_delete_messages else '✘'}
دعوة {'ꪜ' if m.can_invite_users else '✘'}
حظر {'ꪜ' if m.can_restrict_members else '✘'}
تثبيت {'ꪜ' if m.can_pin_messages else '✘'}
"""
        bot.reply_to(message, txt)

    # ================= بنك =================
    elif text == "انشاء حساب بنكي":
        if create_bank(message.from_user.id):
            bot.reply_to(message, "🏦 تم انشاء حساب")
        else:
            bot.reply_to(message, "عندك حساب")

    elif text == "فلوسي":
        acc = bank_user(message.from_user.id)
        if not acc:
            return bot.reply_to(message, "ما عندك حساب")
        bot.reply_to(message, f"💰 فلوسك: {acc['money']}")

    elif text == "راتب":
        ok, t = cd_ok(message.from_user.id,"salary",1200)
        if not ok:
            return bot.reply_to(message, f"⏳ بعد {t} ثانية")

        acc = bank_user(message.from_user.id)
        if not acc:
            return bot.reply_to(message, "ما عندك حساب")

        acc["money"] += 500
        save_data(data)
        bot.reply_to(message, "💵 استلمت راتب")

    # ================= العاب =================
    elif text == "رياضيات":
        a,b = random.randint(1,10), random.randint(1,10)
        quiz_games[message.chat.id] = a+b
        bot.reply_to(message, f"{a}+{b}=?")

    elif message.chat.id in quiz_games:
        if text.isdigit() and int(text) == quiz_games[message.chat.id]:
            add_point(message.from_user.id)
            bot.reply_to(message, "✅ صح +1 نقطة")
            del quiz_games[message.chat.id]

    elif text == "افلام":
        bot.reply_to(message, "\n".join(random.sample(MOVIES,5)))

    # ================= يوت =================
    elif text.startswith("يوت "):
        query = text.replace("يوت ","").strip()

        wait = bot.reply_to(message,"🔎 جاري البحث...")

        try:
            r = requests.get("https://www.youtube.com/results", params={"search_query":query})
            vids = re.findall(r"watch\\?v=(\\S{11})", r.text)

            url = f"https://www.youtube.com/watch?v={vids[0]}"

            res = requests.get(
                "https://yt-search-and-download-mp3.p.rapidapi.com/mp3",
                headers={
                    "X-RapidAPI-Key": RAPID_API_KEY,
                    "X-RapidAPI-Host": "yt-search-and-download-mp3.p.rapidapi.com"
                },
                params={"url":url}
            ).json()

            audio = res.get("link")
            title = res.get("title") or query

            bot.delete_message(message.chat.id, wait.message_id)

            if not audio:
                return bot.reply_to(message,"❌ ما حصلت صوت")

            bot.send_audio(
                message.chat.id,
                audio,
                caption=f"🎧 {title}",
                reply_to_message_id=message.message_id
            )

        except Exception as e:
            bot.reply_to(message,"❌ خطأ")

print("RUNNING...")
bot.infinity_polling(skip_pending=True)
