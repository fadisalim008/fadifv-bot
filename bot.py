import telebot
import json
import os
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

TOKEN = "8667177884:AAFiV6hCpSX2AMyqi9apiiXo0UavZDNan74"
CHANNEL = "@fadifva"

bot = telebot.TeleBot(TOKEN)

os.makedirs("data", exist_ok=True)

USERS = "data/users.json"
GROUPS = "data/groups.json"


def load(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def save_user(message):
    users = load(USERS)
    uid = str(message.from_user.id)
    if uid not in users:
        users[uid] = {
            "name": message.from_user.first_name or "",
            "username": message.from_user.username or ""
        }
        save(USERS, users)


def save_group(message):
    if message.chat.type in ["group", "supergroup"]:
        groups = load(GROUPS)
        gid = str(message.chat.id)
        if gid not in groups:
            groups[gid] = {
                "title": message.chat.title or ""
            }
            save(GROUPS, groups)


def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


def require_sub(message):
    if message.chat.type == "private":
        if not check_sub(message.from_user.id):
            bot.reply_to(message, f"اشترك بالقناة أولاً:\n{CHANNEL}")
            return False
    return True


def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("① اوامر الادمنيه", callback_data="admin"),
        InlineKeyboardButton("② اوامر الاعدادات", callback_data="settings"),
        InlineKeyboardButton("③ اوامر القفل - الفتح", callback_data="locks"),
        InlineKeyboardButton("④ اوامر التسليه", callback_data="fun"),
        InlineKeyboardButton("⑤ اوامر Dev", callback_data="dev"),
        InlineKeyboardButton("⑥ الاوامر الخدميه", callback_data="service")
    )
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    save_user(message)
    save_group(message)

    if not require_sub(message):
        return

    bot.reply_to(message, f"هلا {message.from_user.first_name} 🌷")


@bot.message_handler(func=lambda m: m.text in ["الاوامر", "اوامر", "الأوامر"])
def commands_menu(message):
    save_user(message)
    save_group(message)

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
    bot.send_message(message.chat.id, text, reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: CallbackQuery):
    data = call.data

    if data == "admin":
        text = """
👮‍♂️ أهلاً بك عزيزي
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

    elif data == "settings":
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

    elif data == "locks":
        text = """
🔒 أهلاً بك عزيزي
- اوامر القفل - الفتح
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
        bot.answer_callback_query(call.id, "تم فتح أوامر القفل - الفتح")
        bot.send_message(call.message.chat.id, text)

    elif data == "fun":
        text = """
🎮 أهلاً بك عزيزي
- اوامر التسليه
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

• رفع عام + اسم اختياري
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
- اوامر تسليه شغاله :

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

    elif data == "dev":
        text = """
🛠 أهلاً بك عزيزي
- اوامر Dev
━━━━━━━━━━━━

• هذه القائمة مخصصة لتطوير البوت
• لاحقاً نضيف بيها اوامر المطور
• مثل اذاعة
• احصائيات
• تفعيل وتعطيل ميزات عامة
• صيانة السورس
"""
        bot.answer_callback_query(call.id, "تم فتح أوامر Dev")
        bot.send_message(call.message.chat.id, text)

    elif data == "service":
        text = """
📡 أهلاً بك عزيزي
- الاوامر الخدميه
━━━━━━━━━━━━

• /start
• الاوامر
• /id
• /testdata
• عرض عدد المستخدمين
• عرض عدد الكروبات
• فحص البيانات
"""
        bot.answer_callback_query(call.id, "تم فتح الاوامر الخدميه")
        bot.send_message(call.message.chat.id, text)


@bot.message_handler(commands=['حظي'])
def luck(message):
    bot.reply_to(message, f"نسبة حظك اليوم: {random.randint(0,100)}% 😎")


@bot.message_handler(commands=['صراحة'])
def truth(message):
    bot.reply_to(message, random.choice([
        "شنو اكثر شي ندمت عليه؟",
        "تحب من طرف واحد؟ 😏",
        "آخر مرة بكيت ليش؟",
        "شنو سرك الي محد يعرفه؟"
    ]))


@bot.message_handler(commands=['سؤال'])
def question(message):
    bot.reply_to(message, random.choice([
        "تحب السهر لو النوم؟",
        "تفضل حب لو صداقة؟",
        "شنو افضل يوم بحياتك؟",
        "تؤمن بالحظ؟"
    ]))


@bot.message_handler(commands=['نكتة'])
def joke(message):
    bot.reply_to(message, random.choice([
        "واحد بخيل وقع من الدرج قال الحمدلله جت على قدمي 😂",
        "واحد غبي راح يشتري شمسية فتحها داخل المحل وطردوه 🤣",
        "واحد سألوه ليش تضحك؟ قال تذكرت نكتة نسيتها 😂"
    ]))


@bot.message_handler(commands=['اهانة'])
def insult(message):
    bot.reply_to(message, random.choice([
        "ولك انت شكو هيج 😂",
        "روح نام احسن لك 😴",
        "عقلك دا يسوي تحديث لو شنو؟ 🤣",
        "انت وضعك يحتاج اعادة تشغيل 😂"
    ]))


@bot.message_handler(commands=['تحشيش'])
def tahsheesh(message):
    bot.reply_to(message, random.choice([
        "واحد شاف نفسه بالحلم صحى اعتذر 😂",
        "واحد غبي راح يدرس اونلاين ضيع الواي فاي 🤣",
        "واحد راح يشتري عقل قال خلص الكمية 😂"
    ]))


@bot.message_handler(commands=['جلد'])
def roast(message):
    bot.reply_to(message, random.choice([
        "انت لو تجي مسابقة غباء تاخذ مركز اول بدون منافس 😂",
        "انت لو ذكاء جان هسه صرت عالم 🤣",
        "والله وضعك يحتاج صيانة عامة 😭"
    ]))


@bot.message_handler(commands=['id'])
def my_id(message):
    bot.reply_to(message, f"ايديك: `{message.from_user.id}`", parse_mode="Markdown")


@bot.message_handler(commands=['testdata'])
def testdata(message):
    users = load(USERS)
    groups = load(GROUPS)
    bot.reply_to(
        message,
        f"عدد المستخدمين: {len(users)}\nعدد الكروبات: {len(groups)}"
    )


@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
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
def all_messages(message):
    save_user(message)
    save_group(message)


print("Bot running...")
bot.infinity_polling()
