import telebot
import json
import os
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8667177884:AAFiV6hCpSX2AMyqi9apiiXo0UavZDNan74"
CHANNEL = "@fadifva"              # قناة الاشتراك
BOT_USERNAME = "Fadifvbot"     # يوزر البوت بدون @
DEV_USERNAME = "fvamv"     # يوزرك بدون @

bot = telebot.TeleBot(TOKEN)

os.makedirs("data", exist_ok=True)

USERS_FILE = "data/users.json"
GROUPS_FILE = "data/groups.json"


def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def save_user(message):
    users = load_data(USERS_FILE)
    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = {
            "name": message.from_user.first_name or "",
            "username": message.from_user.username or ""
        }
        save_data(USERS_FILE, users)


def save_group(message):
    if message.chat.type in ["group", "supergroup"]:
        groups = load_data(GROUPS_FILE)
        group_id = str(message.chat.id)

        if group_id not in groups:
            groups[group_id] = {
                "title": message.chat.title or ""
            }
            save_data(GROUPS_FILE, groups)


def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


def require_subscription(message):
    if message.chat.type == "private":
        if not is_subscribed(message.from_user.id):
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("اشترك بالقناة", url=f"https://t.me/{CHANNEL.replace('@', '')}")
            )
            bot.reply_to(
                message,
                f"لازم تشترك بالقناة أولاً:\n{CHANNEL}",
                reply_markup=markup
            )
            return False
    return True


def private_start_buttons():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("المطور", url=f"https://t.me/{DEV_USERNAME}"),
        InlineKeyboardButton("اضفني +", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
    )
    markup.add(
        InlineKeyboardButton("شراء بوت مشابه", url=f"https://t.me/{DEV_USERNAME}")
    )
    return markup


def commands_menu_buttons():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("1 اوامر الادمنيه", callback_data="admin"),
        InlineKeyboardButton("2 اوامر الاعدادات", callback_data="settings")
    )
    markup.add(
        InlineKeyboardButton("3 اوامر القفل - الفتح", callback_data="locks"),
        InlineKeyboardButton("4 اوامر التسليه", callback_data="fun")
    )
    markup.add(
        InlineKeyboardButton("5 اوامر Dev", callback_data="dev"),
        InlineKeyboardButton("6 الاوامر الخدميه", callback_data="service")
    )
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    save_user(message)
    save_group(message)

    if message.chat.type == "private":
        if not require_subscription(message):
            return

        text = """
🗽
- أهلاً بك في بوت الحماية.
- وظيفتي حماية المجموعات من التفليش والتخريب.
- لتفعيل البوت أرسل كلمة: تفعيل
"""
        photo_url = "https://picsum.photos/700/500"

        try:
            bot.send_photo(
                message.chat.id,
                photo_url,
                caption=text,
                reply_markup=private_start_buttons()
            )
        except:
            bot.send_message(
                message.chat.id,
                text,
                reply_markup=private_start_buttons()
            )
        return

    bot.reply_to(message, f"هلا {message.from_user.first_name} 🌷")


@bot.message_handler(func=lambda message: message.text == "تفعيل")
def activate_bot(message):
    if message.chat.type in ["group", "supergroup"]:
        save_group(message)
        bot.reply_to(
            message,
            "تم تفعيل البوت في هذا الكروب ✅\nارسل (الاوامر) حتى تظهر لك قائمة الأوامر."
        )


@bot.message_handler(func=lambda message: message.text in ["مطور", "المطور"])
def developer_info(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("حساب المطور", url=f"https://t.me/{DEV_USERNAME}"))
    bot.reply_to(
        message,
        f"هذا حساب المطور:\n@{DEV_USERNAME}",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text in ["الاوامر", "اوامر", "الأوامر"])
def show_commands_menu(message):
    text = """
- أهلاً بك عزيزي في قائمة الأوامر :

━━━━━━━━━━━━
◂ 1 : أوامر الادمنيه
◂ 2 : أوامر الاعدادات
◂ 3 : أوامر القفل - الفتح
◂ 4 : أوامر التسليه
◂ 5 : أوامر Dev
◂ 6 : الأوامر الخدميه
━━━━━━━━━━━━
"""
    bot.send_message(message.chat.id, text, reply_markup=commands_menu_buttons())


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "admin":
        text = """
• أهلاً بك في عزيزي
- قائمة اوامر الادمنيه
━━━━━━━━━━━━

- اوامر الرفع والتنزيل :

• رفع - تنزيل مالك اساسي
• رفع - تنزيل مالك
• رفع - تنزيل مشرف
• رفع - تنزيل منشئ
• رفع - تنزيل مدير
• رفع - تنزيل ادمن
• رفع - تنزيل مميز
• تنزيل الكل - لازاله جميع الرتب اعلاه

━━━━━━━━━━━━
- اوامر المسح :

• مسح الكل
• مسح المنشئين
• مسح المدراء
• مسح المالكين
• مسح الادمنيه
• مسح المميزين
• مسح المحظورين
• مسح المكتومين
• مسح قائمه المنع
• مسح الردود
• مسح الاوامر المضافه
• مسح + عدد
• مسح بالرد
• مسح الايدي
• مسح الترحيب
• مسح الرابط

━━━━━━━━━━━━
- اوامر الطرد والحظر :

• تقييد + الوقت
• حظر
• طرد
• كتم
• تقييد
• الغاء الحظر
• الغاء الكتم
• فك التقييد
• رفع القيود
• منع بالرد
• الغاء منع بالرد
• طرد البوتات
• طرد المحذوفين
• كشف البوتات
"""
        bot.answer_callback_query(call.id, "تم فتح أوامر الادمنيه")
        bot.send_message(call.message.chat.id, text)

    elif call.data == "settings":
        text = """
⚙️ أهلاً بك عزيزي
- اوامر الاعدادات
━━━━━━━━━━━━

• تفعيل - تعطيل ضافني
• تفعيل - تعطيل الاذكار
• تفعيل - تعطيل الثنائي
• تفعيل - تعطيل افتاري
• تفعيل - تعطيل التسليه
• تفعيل - تعطيل الكت
• تفعيل - تعطيل الترحيب
• تفعيل - تعطيل الردود
• تفعيل - تعطيل الانذار
• تفعيل - تعطيل التحذير
• تفعيل - تعطيل الايدي
• تفعيل - تعطيل الرابط
• تفعيل - تعطيل اطردني
• تفعيل - تعطيل الحظر
• تفعيل - تعطيل الرفع
• تفعيل - تعطيل التنزيل
• تفعيل - تعطيل التحويل
• تفعيل - تعطيل الحمايه
• تفعيل - تعطيل المنشن
• تفعيل - تعطيل وضع الاقتباسات
• تفعيل - تعطيل الخدميه
• تفعيل - تعطيل اليوتيوب
• تفعيل - تعطيل الايدي بالصوره
• تفعيل - تعطيل التحقق
• تفعيل - تعطيل ردود السورس
"""
        bot.answer_callback_query(call.id, "تم فتح أوامر الاعدادات")
        bot.send_message(call.message.chat.id, text)

    elif call.data == "locks":
        text = """
🔒 اوامر القفل - الفتح
━━━━━━━━━━━━

• قفل - فتح السب
• قفل - فتح الايرانيه
• قفل - فتح الكتابه
• قفل - فتح الاباحي
• قفل - فتح تعديل الميديا
• قفل - فتح التعديل
• قفل - فتح الفيديو
• قفل - فتح الصور
• قفل - فتح الملصقات
• قفل - فتح المتحركه
• قفل - فتح الدردشه
• قفل - فتح الروابط
• قفل - فتح التاك
• قفل - فتح البوتات
• قفل - فتح المعرفات
• قفل البوتات بالطرد
• قفل - فتح الكلايش
• قفل - فتح التكرار
• قفل - فتح التوجيه
• قفل - فتح الانلاين
• قفل - فتح الجهات
• قفل - فتح الكل
• قفل - فتح الدخول
• قفل - فتح الصوت

━━━━━━━━━━━━
- اوامر التقييد :

• قفل - فتح التوجيه بالتقييد
• قفل - فتح الروابط بالتقييد
• قفل - فتح المتحركه بالتقييد
• قفل - فتح الصور بالتقييد
• قفل - فتح الفيديو بالتقييد
"""
        bot.answer_callback_query(call.id, "تم فتح أوامر القفل والفتح")
        bot.send_message(call.message.chat.id, text)

    elif call.data == "fun":
        text = """
• اهلا بك عزيزي
- اوامر التسليه :
━━━━━━━━━━━━
- اوامر تسلية تظهر بالايدي :

• رفع - تنزيل : هطف : الهطوف
• رفع - تنزيل : بثر : البثرين
• رفع - تنزيل : حمار : الحمير
• رفع - تنزيل : كلب : الكلاب
• رفع - تنزيل : كلبه : الكلبات
• رفع - تنزيل : عتوي : العتوين
• رفع - تنزيل : عتويه : العتويات
• رفع - تنزيل : لحجي : اللحوج
• رفع - تنزيل : لحجيه : اللحجيات
• رفع - تنزيل : خروف : الخرفان
• رفع - تنزيل : خفيفه : الخفيفات
• رفع - تنزيل : خفيف : الخفيفين
• رفع بقلبي : تنزيل من قلبي
━━━━━━━━━━━━
للقروب:
• رفع + اسم اختياري
• مسح رتب التسليه
• رتب التسليه
• تعطيل التسليه
━━━━━━━━━━━━
للعام:
• رفع عام +اسم اختياري
• رتب التسليه عام
• مسح رتب التسليه
━━━━━━━━━━━━
• طلاق - زواج
• زوجي - زوجتي
• تتزوجني
━━━━━━━━━━━━
• اكتموه (تصويت)
• تعطيل - تفعيل : اكتموه
• تعطيل - تفعيل : زوجني
━━━━━━━━━━━━
• /حظي
• /صراحة
• /سؤال
• /نكتة
• /اهانة
• /تحشيش
• /جلد
"""
        bot.answer_callback_query(call.id, "تم فتح أوامر التسليه")
        bot.send_message(call.message.chat.id, text)

    elif call.data == "dev":
        text = f"""
🛠 اوامر Dev
━━━━━━━━━━━━
• المطور : @{DEV_USERNAME}
• شراء بوت مشابه
• دعم فني
• تطوير سورس
"""
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("حساب المطور", url=f"https://t.me/{DEV_USERNAME}"))
        bot.answer_callback_query(call.id, "تم فتح أوامر Dev")
        bot.send_message(call.message.chat.id, text, reply_markup=markup)

    elif call.data == "service":
        users = load_data(USERS_FILE)
        groups = load_data(GROUPS_FILE)
        text = f"""
📡 الاوامر الخدميه
━━━━━━━━━━━━
• /start
• الاوامر
• مطور
• تفعيل
• /id
• /testdata

━━━━━━━━━━━━
عدد المستخدمين: {len(users)}
عدد الكروبات: {len(groups)}
"""
        bot.answer_callback_query(call.id, "تم فتح الاوامر الخدميه")
        bot.send_message(call.message.chat.id, text)


@bot.message_handler(commands=['حظي'])
def luck(message):
    bot.reply_to(message, f"نسبة حظك اليوم: {random.randint(0, 100)}% 😎")


@bot.message_handler(commands=['صراحة'])
def truth(message):
    questions = [
        "شنو اكثر شي ندمت عليه؟",
        "تحب من طرف واحد؟ 😏",
        "آخر مرة بكيت ليش؟",
        "شنو سرك الي محد يعرفه؟"
    ]
    bot.reply_to(message, random.choice(questions))


@bot.message_handler(commands=['سؤال'])
def question(message):
    questions = [
        "تحب السهر لو النوم؟",
        "تفضل حب لو صداقة؟",
        "شنو افضل يوم بحياتك؟",
        "تؤمن بالحظ؟"
    ]
    bot.reply_to(message, random.choice(questions))


@bot.message_handler(commands=['نكتة'])
def joke(message):
    jokes = [
        "واحد بخيل وقع من الدرج قال الحمدلله جت على قدمي 😂",
        "واحد غبي راح يشتري شمسية فتحها داخل المحل وطردوه 🤣",
        "واحد سألوه ليش تضحك؟ قال تذكرت نكتة نسيتها 😂"
    ]
    bot.reply_to(message, random.choice(jokes))


@bot.message_handler(commands=['اهانة'])
def insult(message):
    texts = [
        "ولك انت شكو هيج 😂",
        "روح نام احسن لك 😴",
        "عقلك دا يسوي تحديث لو شنو؟ 🤣",
        "انت وضعك يحتاج اعادة تشغيل 😂"
    ]
    bot.reply_to(message, random.choice(texts))


@bot.message_handler(commands=['تحشيش'])
def tahsheesh(message):
    texts = [
        "واحد شاف نفسه بالحلم صحى اعتذر 😂",
        "واحد غبي راح يدرس اونلاين ضيع الواي فاي 🤣",
        "واحد راح يشتري عقل قال خلص الكمية 😂"
    ]
    bot.reply_to(message, random.choice(texts))


@bot.message_handler(commands=['جلد'])
def roast(message):
    texts = [
        "انت لو تجي مسابقة غباء تاخذ مركز اول بدون منافس 😂",
        "انت لو ذكاء جان هسه صرت عالم 🤣",
        "والله وضعك يحتاج صيانة عامة 😭"
    ]
    bot.reply_to(message, random.choice(texts))


@bot.message_handler(commands=['id'])
def my_id(message):
    bot.reply_to(message, f"ايديك: {message.from_user.id}")


@bot.message_handler(commands=['testdata'])
def testdata(message):
    users = load_data(USERS_FILE)
    groups = load_data(GROUPS_FILE)
    bot.reply_to(
        message,
        f"عدد المستخدمين: {len(users)}\nعدد الكروبات: {len(groups)}"
    )


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_members(message):
    save_group(message)
    for user in message.new_chat_members:
        try:
            bot.send_message(
                message.chat.id,
                f"هلا {user.first_name} 🌷\nنورت الكروب: {message.chat.title}\nالتزم بالقوانين وتكدر تشارك برأيك بكل احترام."
            )
        except:
            pass


@bot.message_handler(func=lambda message: True)
def save_everything(message):
    save_user(message)
    save_group(message)


print("Bot is running...")
bot.infinity_polling()
