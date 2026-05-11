# SOURCE FADI - commands sorted final

import os, json, re, random, time, datetime
import telebot, requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# حط التوكنات من Railway Variables أفضل:
# BOT_TOKEN = توكن البوت
# RAPID_API_KEY = مفتاح RapidAPI
TOKEN = os.getenv("BOT_TOKEN", "8516176029:AAFEAuEU93dkwAdjKva8M6M_SQjHjHxn4Uo")
RAPID_API_KEY = os.getenv("RAPID_API_KEY", "78420a7cadmsh4c0b551fb859336p128e4ajsne5d9fd86d545")

OWNER_ID = int(os.getenv("OWNER_ID", "8065884629"))
BOT_USERNAME = os.getenv("BOT_USERNAME", "fadifvambot")
DEV_USERNAME = os.getenv("DEV_USERNAME", "fvamv")
FORCE_CHANNEL = os.getenv("FORCE_CHANNEL", "@fadifva")
START_PHOTO = os.getenv("START_PHOTO", "https://i.ibb.co/1GpcX6BM/IMG-20260507-114222-327.jpg")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

def raw_send_message(chat_id, text, reply_markup=None, reply_to_message_id=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup is not None: payload["reply_markup"] = reply_markup
    if reply_to_message_id is not None: payload["reply_to_message_id"] = reply_to_message_id
    try: return requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload, timeout=20).json()
    except Exception as e: print("RAW SEND ERROR", e); return None

def raw_send_photo(chat_id, photo, caption, reply_markup=None):
    payload = {"chat_id": chat_id, "photo": photo, "caption": caption, "parse_mode": "HTML"}
    if reply_markup is not None: payload["reply_markup"] = reply_markup
    try: return requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", json=payload, timeout=20).json()
    except Exception as e: print("RAW PHOTO ERROR", e); return None

def raw_edit_message(chat_id, message_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "HTML"}
    if reply_markup is not None: payload["reply_markup"] = reply_markup
    try: return requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", json=payload, timeout=20).json()
    except Exception as e: print("RAW EDIT ERROR", e); return None

def blue_btn(text, callback_data=None, url=None):
    b = {"text": text, "style": "primary"}
    if callback_data is not None: b["callback_data"] = callback_data
    if url is not None: b["url"] = url
    return b

def red_btn(text, callback_data=None, url=None):
    b = {"text": text, "style": "danger"}
    if callback_data is not None: b["callback_data"] = callback_data
    if url is not None: b["url"] = url
    return b
DATA_FILE = "data.json"

LOCK_ALIASES = {
    "الكل": "all", "الدخول": "join", "الروابط": "links", "الرابط": "links", "المعرف": "username",
    "التاك": "tag", "الشارحه": "hashtag", "الشارحة": "hashtag", "التعديل": "edit",
    "تعديل الميديا": "edit_media", "المتحركه": "animation", "المتحركة": "animation",
    "المتحركات": "animation", "الملفات": "files", "الصور": "photos", "الفيديو": "videos",
    "الفيدوهات": "videos", "الفيديوهات": "videos", "الستوري": "story", "توجيه الستوري": "story",
    "الماركداون": "markdown", "البوتات": "bots", "التكرار": "spam", "الكلايش": "long_text",
    "السيلفي": "selfie", "الملصقات": "stickers", "الانلاين": "inline", "الدردشه": "chat",
    "الدردشة": "chat", "التوجيه": "forward", "الاغاني": "songs", "الأغاني": "songs",
    "الصوت": "voice", "الفويسات": "voice", "الجهات": "contacts", "الاشعارات": "notifications",
    "الإشعارات": "notifications", "التثبيت": "pin", "الوسائط": "media", "التفليش": "flood",
    "وسائط المميزين": "vip_media", "الفشار": "spoilers", "ارسال القناة": "send_channel",
    "القنوات": "channels", "الإنكليزيه": "english", "الانجليزي": "english", "الانكليزي": "english",
    "الفارسيه": "persian", "الفارسية": "persian", "الكفر": "bad_words", "الاباحي": "porn",
    "الإباحي": "porn"
}

SETTING_ALIASES = {
    "الرابط": "link_cmd", "الترحيب": "welcome", "الايدي": "id", "الايدي بالصورة": "id_photo",
    "الايدي بالصوره": "id_photo", "الرفع": "promote_cmd", "الحظر": "ban_cmd", "الكتم": "mute_cmd",
    "الطرد": "kick_cmd", "التقييد": "restrict_cmd", "الالعاب": "games", "الألعاب": "games",
    "اطردني": "kickme", "الردود": "replies", "تاك عام": "tagall", "التحشيش": "fun",
    "البنك": "bank", "زواج": "marriage", "ثنائي اليوم": "couple", "منشن": "mention",
    "عقاب": "punish", "اكتموه": "mutehim", "زوجني": "marriage", "بحث يوتيوب": "yt_search",
    "غنيلي": "sing", "الصيغ": "formats", "كول": "say", "الابراج": "zodiac",
    "التفاعل": "activity", "البايو": "bio", "صورتي": "myphoto", "اسمي": "myname",
    "نبذه": "bio", "النداء التلقائي": "auto_call", "تاك عام": "tagall",
    "المسح التلقائي": "auto_delete", "امسح": "delete_cmd"
}

RANK_ORDER = {
    "عضو": 0, "مميز": 1, "ادمن": 2, "أدمن": 2, "مشرف": 2,
    "مدير": 3, "منشئ": 4, "منشئ اساسي": 5, "منشئ أساسي": 5,
    "مالك": 6, "مالك اساسي": 7, "مالك أساسي": 7,
    "مطور": 8, "مطور ثانوي": 9, "مطور اساسي": 10, "مطور أساسي": 10
}
RANK_NAMES = ["مميز","ادمن","مشرف","مدير","منشئ","منشئ اساسي","مالك","مالك اساسي","مطور","مطور ثانوي","مطور اساسي"]

FUN_RANKS = {
    "تاج": "قائمه التاج", "ملك": "الملوك", "ملكه": "الملكات", "مرتي": "قائمه كلبي",
    "اثول": "الثولان", "جلب": "الجلاب", "مطي": "المطايه", "صخل": "الصخول",
    "بقره": "البقرات", "زاحف": "الزواحف", "لوكي": "اللوكيه", "غبي": "الاغبياء",
    "طلي": "الطليان", "طامس": "الطامسين", "عسل": "العسل", "كيك": "الكيك",
    "بكلبي": "قائمه كلبي", "من كلبي": "قائمه كلبي"
}

DEFAULT_LOCKS = {v: False for v in set(LOCK_ALIASES.values())}
DEFAULT_LOCK_ACTIONS = {v: "delete" for v in set(LOCK_ALIASES.values())}
DEFAULT_SETTINGS = {v: True for v in set(SETTING_ALIASES.values())}
DEFAULT_SETTINGS.update({"welcome": True, "replies": True, "id_photo": True, "games": True, "bank": True, "fun": True})

DEFAULT_DATA = {
    "locks": {}, "lock_actions": {}, "settings": {}, "ranks": {}, "muted": {}, "restricted": {},
    "banned_words": {}, "warns": {}, "users": {}, "groups": {}, "replies": {}, "multi_replies": {},
    "global_replies": {}, "media": {}, "notify": True, "bank": {}, "robbers": {}, "cooldowns": {},
    "join_info": {}, "points": {}, "messages": {}, "activity": {}, "blocked": {}, "global_ban": [],
    "global_mute": [], "marriages": {}, "birthdays": {}, "titles": {}, "custom_rank_names": {},
    "laws": {}, "welcome_text": {}, "links": {}, "scratch": {}, "fun_ranks": {},
    "bot_enabled": True, "paid_mode": False, "paid_groups": [], "force_enabled": True,
    "force2_enabled": False, "force2_channel": "", "force_group_enabled": False,
    "min_members": 0, "bot_name": "فادي", "auto_backup": False, "last_games": {}, "active_fast": {}, "game_sessions": {}, "wc_votes": {}
}

waiting_reply = {}
xo_games = {}
quiz_games = {}
roulette_games = {}

MOVIES = ["The Godfather","Inception","Interstellar","Fight Club","The Dark Knight","Gladiator","Parasite","Se7en","Joker","Titanic","Avatar","The Matrix","Forrest Gump","Spider-Man","John Wick"]
NAMES = ["سارة","نور","ملاك","زينب","حوراء","فاطمة","رقيه","شهد","مريم","اية"]
BAD_WORDS = ["كس","زب","عير","قحبة","كواد","خرا","نياكة"]
PERSIAN_RE = re.compile(r"[\u0600-\u06FF]*[پچژگ][\u0600-\u06FF]*")
EN_RE = re.compile(r"[A-Za-z]")
URL_RE = re.compile(r"(https?://|t\.me/|telegram\.me/|www\.)", re.I)

GAME_QUESTIONS = {
    "انمي": [("بطل انمي ناروتو اسمه؟", "ناروتو")],
    "المختلف": [("تفاح - موز - سيارة - برتقال: المختلف؟", "سيارة")],
    "العكس": [("عكس كلمة فوق؟", "تحت")],
    "حزوره": [("شي يمشي بلا رجلين؟", "النهر")],
    "معاني": [("ما معنى الغيث؟", "المطر")],
    "بات": [("اكتب بات", "بات")],
    "خمن": [("خمن رقم من 1 إلى 3", "2")],
    "ترتيب": [("رتب: ب ا ت ك", "كتاب")],
    "سمايلات": [("اكتب هذا السمايل 😂", "😂")],
    "اسئله": [("كم عدد الصلوات المفروضة؟", "5")],
    "لغز": [("شي كلما أخذت منه كبر؟", "الحفرة")],
    "رياضيات": [("2+2=?", "4")],
    "انكليزي": [("ترجمة book؟", "كتاب")],
    "كت": [("شنو حلمك؟", "حلمي")],
    "كت تويت": [("شنو حلمك؟", "حلمي")],
    "لو خيروك": [("لو خيروك مال أو راحة؟", "راحة")],
    "صراحه": [("اعترف بشي تحبه؟", "احب")],
    "اعلام": [("علم العراق بيه كم لون؟", "3")],
    "مقالات": [("اكتب كلمة مقال", "مقال")],
    "عواصم": [("عاصمة العراق؟", "بغداد")],
    "كلمات": [("كلمة تبدأ بحرف م؟", "ماء")],
    "الحظ": [("اكتب حظ", "حظ")],
    "حظي": [("اكتب حظي", "حظي")],
    "عربي": [("جمع كتاب؟", "كتب")],
    "دين": [("حكم الصلاة؟", "واجبة")],
    "فكك": [("فكك كلمة باب", "ب ا ب")],
    "حجره": [("حجرة ورقة مقص؟ اكتب حجرة", "حجرة")],
    "اكس او": [("اكتب X", "X")],
    "لاعب": [("لاعب أرجنتيني مشهور؟", "ميسي")],
    "سيارات": [("شركة سيارة تبدأ بت؟", "تويوتا")]
}

COMMAND_TEXTS = {}

COMMAND_TEXTS["admin"] = """✧︙اوامر ادمنية المجموعه ...
— — — — — — — — —
✧︙رفع، تنزيل ← مميز
✧︙المميزين ← مسح المميزين
✧︙رفع المالك 
✧︙تاك ، تاك للكل ، المجموعه
✧︙منع ، الغاء منع
— — — — — — — — —
✧︙حظر ، طرد ← الغاء حظر 
✧︙كتم ← الغاء كتم
✧︙تقييد ← الغاء تقييد
✧︙كشف ، رفع ← القيود
✧︙انذار ← بالرد
— — — — — — — — —
✧︙تثبيت ، الغاء تثبيت
✧︙الرابط ، الاعدادات ، الحمايه
✧︙الترحيب ، القوانين
✧︙مسح عدد / مسح بالرد"""

COMMAND_TEXTS["locks"] = """✧︙اوامر الحمايه كالاتي ...
— — — — — — — — —
✧︙قفل ، فتح ← الامر
✧︙تستطيع قفل حماية: بالتقييد ، بالطرد ، بالكتم
— — — — — — — — —
✧︙الكل ~ الدخول
✧︙الروابط ~ المعرف
✧︙التاك ~ الشارحه
✧︙التعديل ~ تعديل الميديا
✧︙المتحركه ~ الملفات
✧︙الصور ~ الفيديو
✧︙الماركداون ~ البوتات
✧︙التكرار ~ الكلايش
✧︙السيلفي ~ الملصقات
✧︙الانلاين ~ الدردشه
✧︙التوجيه ~ الاغاني
✧︙الصوت ~ الجهات
✧︙الاشعارات ~ التثبيت
✧︙الوسائط ~ التفليش
✧︙القنوات
✧︙الإنكليزيه ~ الفارسيه
✧︙الكفر ~ الاباحي"""

COMMAND_TEXTS["manager"] = """✧︙اوامر المدراء في المجموعه
— — — — — — — — —
✧︙رفع ، تنزيل ← ادمن
✧︙الادمنيه ← مسح الادمنيه
✧︙رفع الادمنيه
✧︙تنزيل الكل ← بالرد
✧︙كشف ، طرد ، قفل ← البوتات
✧︙فحص ← البوت
✧︙طرد ← المحذوفين
✧︙قفل فتح ← ارسال القناة
— — — — — — — — —
✧︙وضع/ضع: اسم، رابط، صوره، قوانين، وصف، الترحيب
✧︙اضف رد / مسح رد / الردود / مسح الردود
✧︙تاك عام ، all ، @all
✧︙الميديا ← امسح"""

COMMAND_TEXTS["owner"] = """︙اوامر مالك المجموعه
— — — — — — — — —
✧︙رفع ، تنزيل ← مالك
✧︙المالكين ، مسح المالكين
✧︙ارفعني مالك
✧︙رفع المالك
✧︙تنزيل جميع الرتب
✧︙تفعيل المالك
✧︙تعيين عدد الطرد + العدد
— — — — — — — — —
✧︙رفع ، تنزيل ← منشئ اساسي
✧︙المنشئين الاساسيين
✧︙مسح المنشئين الاساسيين"""

COMMAND_TEXTS["creator"] = """✧︙اوامر المنشئ الاساسي
— — — — — — — — —
✧︙رفع ، تنزيل ← منشئ
✧︙المنشئين ، مسح المنشئين
✧︙رفع ، تنزيل ← مشرف
✧︙ضع لقب + اللقب ← بالرد
✧︙صلاحيات المجموعه
✧︙صلاحيات المشرفين
✧︙مسح نقاطه ، رسائله ← بالرد
✧︙تفعيل/تعطيل البنك
— — — — — — — — —
✧︙اوامر المنشئ المجموعه
✧︙رفع ، تنزيل ← مدير
✧︙المدراء ، مسح المدراء
✧︙ضع التكرار ← عدد
✧︙تفعيل الكل"""

COMMAND_TEXTS["fun"] = """↫‌‌‏ اوامـــر التحشيـــش
— — — — — — — — —
✧︙تفعيل تعطيل التحشيش
✧︙رفع/تنزيل: تاج، ملك، ملكه، مرتي، اثول، جلب، مطي، صخل، بقره، زاحف، لوكي، غبي، طلي، طامس، عسل، كيك، بكلبي، من كلبي
✧︙قوائم التحشيش: الملوك، الملكات، الثولان، الجلاب، المطايه، الصخول، البقرات، الزواحف، اللوكيه، الاغبياء، العسل، الكيك
✧︙نسبه الحب/الكره/الرجوله/الانوثه/الذكاء/الغباء
✧︙شنو رايك بهذا، شنو رايك بهاي، انطي هديه، بوسه، بوسني، صيحه، رزله"""

COMMAND_TEXTS["dev"] = f"""✧︙اوامر المطور الاساسي
— — — — — — — — —
✧︙تفعيل / تعطيل
✧︙رفع/تنزيل مطور اساسي، مطور ثانوي، مطور
✧︙المطورين الاساسيين، المطورين الثانويين، المطورين
✧︙تفعيل/الغاء الوضع المدفوع
✧︙حظر عام، الغاء حظر عام
✧︙كتم عام، الغاء كتم عام
✧︙الاحصائيات
✧︙اذاعه، اذاعه خاص
✧︙جلب النسخه الاحتياطيه
✧︙تفعيل/تعطيل الاشتراك الاجباري
✧︙تغيير الاشتراك الاجباري
المطور: @{DEV_USERNAME}"""

COMMAND_TEXTS["games"] = """✧✧︙قائمــه العــاب البــوت
— — — — — — — — —
✧︙انمي، المختلف، العكس، حزوره، معاني، بات، خمن، ترتيب، سمايلات، اسئله، لغز، روليت، الروليت، رياضيات، انكليزي، كت، لو خيروك، صراحه، اعلام، مقالات، عواصم، كلمات، الحظ، حظي، عربي، دين، فكك، حجره، اكس او
— — — — — — — — —
✧︙نقاطي
✧︙بيع نقاطي + العدد"""

COMMAND_TEXTS["bank"] = """✧︙اوامر البنك كالاتي :
— — — — — — — — —
✧︙انشاء ، مسح حساب بنكي
✧︙راتب ، بخشيش
✧︙استثمار + رقم
✧︙مضاربه + رقم
✧︙حظ + رقم
✧︙حسابي ، فلوسي
✧︙حسابه ، فلوسه بالرد
✧︙سرقه بالرد
✧︙تحويل + رقم بالرد
✧︙زواج + رقم بالرد
✧︙زواجي
✧︙زوجتي ، زوجي
✧︙طالق ، خلع بالرد
✧︙توب المتزوجين
✧︙توب الحراميه
✧︙توب الفلوس
✧︙تصفير الفلوس
✧︙قائمه اكشطها
✧︙اكشط + رقم
✧︙مسح لعبه البنك
✧︙ميدالياتي
✧︙تفعيل ، تعطيل البنك
✧︙متجر البنك"""

COMMAND_TEXTS["members"] = """✧︙اوامر الاعضاء والادمنيه
— — — — — — — — —
✧︙ايدي ، ايدي بالرد ، رسائلي
✧︙تفاعلي ، بايو ، زوجني
✧︙لقبي ، لقبه بالرد
✧︙اسمي ، معرفي ، تفاعلي
✧︙جهاتي ، سحكاتي ، نقاطي
✧︙بيع نقاطي + العدد
✧︙مسح نقاطي ، التفاعل
✧︙معلوماتي ، كول + الكلمه
✧︙منشن ، نداء ، ترند
✧︙زواج ، ثنائي اليوم ، نبذه
✧︙الوقت ، الساعه ، التاريخ
✧︙زخرفه ، زخرفه + اسم
✧︙غنيلي ، اغنيه
✧︙همسه ، اسم برجك ، صورتي
✧︙صلاحياتي ، رتبتي ، نزلني"""

COMMAND_TEXTS["entertainment"] = """︙اوامر التسليه كالاتي:
— — — — — — — — —
✧︙غنيلي ، ريمكس ، اغنيه ، شعر
✧︙قصيدة ، حسينية
✧︙صوره ، متحركه ، راب
✧︙انمي ، ميمز
✧︙لاعب ، سيارات
✧︙مسلسل ، فلم
✧︙احسب + تاريخ الميلاد
✧︙معنى اسم + الاسم
✧︙ثيم
✧︙زواج ~ طلاق بالرد
✧︙ثنائي اليوم ، منشن
✧︙زوجني ، عقاب
✧︙اكتموه بالرد
✧︙الطقس + اسم المدينه
✧︙بحث يوتيوب + الفيديو"""


# ================= كلايش الأوامر الجديدة =================
COMMAND_TEXTS["locks"] = """- اوامر ( القفل والفتح ) .

- قفل / فتح + اسم القفل
- قفل + اسم القفل + بالكتم
- قفل + اسم القفل + بالطرد
- قفل + اسم القفل + بالتقييد

- التاك
- القنوات
- الصور
- الروابط
- الفشار
- التكرار
- الفيديو
- الدخول
- الاضافه
- الاغاني
- الصوت
- الملفات
- التفليش
- الدردشه
- الجهات
- السيلفي
- التثبيت
- الشارحه
- الكلايش
- البوتات
- التوجيه
- التعديل
- المعرفات
- الكيبورد
- الفارسيه
- الانكليزيه
- الملصقات
- الاشعارات
- الماركداون
- المتحركه

- تفعيل الايدي
- تعطيل الايدي
- تفعيل الايدي بالصورة
- تعطيل الايدي بالصورة
- ا  ← يعرض الايدي"""
COMMAND_TEXTS["manager"] = """- اوامر مشرفين المجموعة .

- القوائم
- الميديا
- نزلني
- انذار
- تثبيت
- ت
- الاعدادات
- التفعيلات
- صلاحياتي
- تصفير الترند
- ضبط الحمايه
- اضف رد
- اضف امر
- تاك للكل
- تاك للمشرفين
- تاك للاعضاء
- ضع رابط
- ضع تحذير
- ضع وصف
- ضع صوره
- ضع اسم
- ضع ترحيب
- ضع توحيد
- انشاء رابط
- قائمه المنع
- الغاء التثبيت
- تعيين الايدي
- تغيير الايدي
- منع • الغاء منع
- اضف رد مميز
- اضف رد متعدد
- الغاء تثبيت الكل
- كشف البوتات
- الردود المميزه
- الردود المتعدده
- الاوامر المضافه
- ضع التكرار + العدد
- تغيير المالك
- صلاحيات المجموعه
- اضف لقب + اللقب بالرد
- ضع عدد المسح + العدد
- اضف نقاط + العدد بالرد
- اضف رسائل + العدد بالرد
- ضع رتبه + اسم الرتبه بالرد
- اضف سحكات + العدد بالرد
- ضع وقت المسح + الوقت بالرد"""
COMMAND_TEXTS["delete"] = """- اوامر مسح المشرفين .

- رد
- تاك
- امر
- بالرد
- الرابط
- رد عام
- الصوره
- الايدي
- المدراء
- التحذير
- الترحيب
- رد مميز
- المنشئين
- المالكين
- الادمنيه
- المميزين
- المقيدين
- رد متعدد
- المكتومين
- قائمه المنع
- المطرودين
- المحظورين
- الثانويين
- المطورين
- كليشه المالك
- قائمه التاكات
- المميزين عام
- كليشه المطور
- مسح + العدد
- الردود المميزه
- الردود المتعدده
- قائمه المنع العام
- المنشئين الاساسيين"""
COMMAND_TEXTS["admin"] = """- اوامر الرفع والحظر .

- طرد
- تحكم
- اضف تاك
- تنزيل الكل
- رفع المالك
- رفع القيود
- رفع الادمنيه
- كشف القيود
- تقييد بالوقت
- كتم • الغاء كتم
- حظر • الغاء حظر
- تقييد • الغاء تقييد
- رفع • تنزيل ↜ منشئ
- رفع • تنزيل ↜ مدير
- رفع • تنزيل ↜ ادمن
- رفع • تنزيل ↜ مميز
- رفع • تنزيل ↜ مشرف
- رفع • تنزيل ↜ منشئ اساسي
- تغيير • مسح كليشه المالك
- تقييد ❲ رقم ❳ يوم • ساعه • دقيقه

- المدراء
- المالك
- الادمنيه
- المميزين
- المقيدين
- المكتومين
- المحظورين
- المشرفين
- المنشئين
- المنشئين الاساسيين"""
COMMAND_TEXTS["entertainment"] = """- اوامر ترفيه الاعضاء .

- نداء
- جمالي
- زوجني
- ز
- الالعاب
- ثنائي اليوم
- نسبه الحب
- نسبه الكره
- نسبه الرجوله
- نسبه الانوثه
- نسبه الجمال
- الالعاب المتطوره
- غنيلي • انمي
- صوره • اغنيه
- متحركه • ميمز
- ريمكس • افتار
- ثيم • راب
- شعر • قصيده
- فلم • مسلسل
- اقتباس • ستوري
- قران • جداريه
- هينه • هينها
- بوسه • بوسها
- تزوجني • تزوجيني
- طلقني • طلقيني
- زوجي • زوجتي
- الازواج • المتزوجين
- شنو رأيك بهذا • بهذ
- رفع • تنزيل مطي
- رفع • تنزيل ملك
- رفع • تنزيل ملكه
- رفع • تنزيل جلب
- رفع • تنزيل زاحف
- رفع • تنزيل زاحفه
- رفع • تنزيل كيك
- رفع • تنزيل كيمر
- رفع • تنزيل مرتي
- رفع • تنزيل كلبي
- رفع • تنزيل كراف
- رفع • تنزيل زنجي
- رفع • تنزيل بتك
- رفع • تنزيل كامز"""
COMMAND_TEXTS["games"] = """- اوامر الالعاب .

- لغز
- XO / اكس او
- سيارات
- اعلام
- مشاهير
- عربي
- كت
- كت تويت
- حجرة
- الاسرع
- لو خيروك
- تحدي
- رياضيات
- كلمات
- عواصم
- عقاب
- روليت
- انكليزي
- تفكيك
- بات
- امثله
- صراحة

- نقاطي
- بيع نقاطي
- بيع نقاطي + العدد"""
COMMAND_TEXTS["bank"] = """- اوامر البنك .

- انشاء حساب بنكي
- مسح حساب بنكي

- حسابي
- فلوسي
- تحويل

- راتب
- بخشيش
- زرف

- استثمار
- حظ
- مضاربه

- توب الفلوس
- توب الحراميه"""
def save_data(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA.copy())
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        d = DEFAULT_DATA.copy()
    for k, v in DEFAULT_DATA.items():
        if k not in d:
            d[k] = v
    save_data(d)
    return d

data = load_data()

def sid(x): return str(x)

def now_time(): return int(time.time())

def chat_settings(chat_id):
    cid = sid(chat_id)
    data["settings"].setdefault(cid, DEFAULT_SETTINGS.copy())
    for k, v in DEFAULT_SETTINGS.items():
        data["settings"][cid].setdefault(k, v)
    return data["settings"][cid]

def get_locks(chat_id):
    cid = sid(chat_id)
    data["locks"].setdefault(cid, DEFAULT_LOCKS.copy())
    data["lock_actions"].setdefault(cid, DEFAULT_LOCK_ACTIONS.copy())
    for k, v in DEFAULT_LOCKS.items():
        data["locks"][cid].setdefault(k, v)
    for k, v in DEFAULT_LOCK_ACTIONS.items():
        data["lock_actions"][cid].setdefault(k, v)
    return data["locks"][cid]

def get_lock_actions(chat_id):
    get_locks(chat_id)
    return data["lock_actions"][sid(chat_id)]

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
            except: pass
    if message.chat.type in ["group", "supergroup"]:
        cid = sid(message.chat.id)
        if cid not in data["groups"]:
            data["groups"][cid] = {"title": message.chat.title or "", "username": message.chat.username or ""}
            chat_settings(message.chat.id); get_locks(message.chat.id)
            save_data(data)

def update_activity(message):
    if not message.from_user: return
    uid, cid = sid(message.from_user.id), sid(message.chat.id)
    data["messages"].setdefault(cid, {})
    data["messages"][cid][uid] = data["messages"][cid].get(uid, 0) + 1
    data["activity"].setdefault(uid, 0)
    data["activity"][uid] += 1
    save_data(data)

def save_media_message(message):
    if message.chat.type not in ["group", "supergroup"]: return
    if message.content_type not in ["photo","video","sticker","animation","document","audio","voice"]:
        return
    cid = sid(message.chat.id)
    data["media"].setdefault(cid, [])
    data["media"][cid].append({"message_id": message.message_id, "type": message.content_type})
    data["media"][cid] = data["media"][cid][-1500:]
    save_data(data)

def is_subscribed(user_id):
    if not data.get("force_enabled", True): return True
    try:
        m = bot.get_chat_member(FORCE_CHANNEL, user_id)
        return m.status in ["member","administrator","creator"]
    except:
        return True

def check_sub(message):
    if message.from_user and not is_subscribed(message.from_user.id):
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("اشترك بالقناة", url="https://t.me/" + FORCE_CHANNEL.replace("@","")))
        bot.reply_to(message, "⚠️ لازم تشترك بقناة البوت أولاً", reply_markup=kb)
        return False
    return True


# ================= إضافات سورس فادي =================
def is_force_command(text):
    if not text:
        return False
    exact = {
        "الاوامر","الأوامر","اوامر","اوامري","سورس","المطور","شراء بوت مشابه",
        "ا","ايدي","ايدي بالرد","معلوماتي","صلاحياتي","رتبتي","رسائلي","نقاطي",
        "لغز","سيارات","اعلام","مشاهير","عربي","رياضيات","انكليزي","عواصم","كلمات","بات","امثله",
        "اكس او","XO","xo","اكسو","حجرة","الاسرع","كت","كت تويت","صراحة","لو خيروك",
        "تحدي","عقاب","روليت","ترند","ز","افلام","فلم","مسلسل","انمي","غنيلي","اغنيه","أغنية",
        "ريمكس","شعر","قصيدة","حسينية","راب","ميمز","ثيم","الطقس",
        "المميزين","الادمنيه","الأدمنيه","المقيدين","المشرفين","المنشئين","المكتومين",
        "ت","ر","تاك للكل","تاك للمشرفين","تاك للاعضاء"
    }
    prefixes = ("يوت ", "بحث يوتيوب ", "الطقس ", "طقس ", "بيع نقاطي", "احسب ", "معنى اسم ")
    return text in exact or text.startswith(prefixes)

def user_label(user):
    if not user:
        return "غير معروف"
    if getattr(user, "username", None):
        return f"@{user.username}"
    return f"{getattr(user, 'first_name', 'بدون اسم')} - {getattr(user, 'id', '')}"

def notify_bot_added(message):
    try:
        me = bot.get_me()
        added = any(u.id == me.id for u in getattr(message, "new_chat_members", []) or [])
        if not added:
            return
        link = "لا يوجد"
        try:
            link = bot.export_chat_invite_link(message.chat.id)
        except Exception:
            pass
        try:
            count = bot.get_chat_member_count(message.chat.id)
        except Exception:
            count = "غير معروف"
        txt = (
            "🔔 تم إضافة البوت إلى كروب جديد\n\n"
            f"• اسم الكروب: {message.chat.title}\n"
            f"• ايدي الكروب: <code>{message.chat.id}</code>\n"
            f"• رابط الكروب: {link}\n"
            f"• عدد الأعضاء: {count}\n"
            f"• بواسطة: {user_label(message.from_user)}"
        )
        bot.send_message(OWNER_ID, txt)
    except Exception as e:
        print("ADD GROUP NOTIFY ERROR", e)

def required_level_for_promote(rank):
    if rank == "مميز":
        return 2
    if rank == "ادمن":
        return 2
    if rank == "مشرف":
        return 4
    if rank == "مدير":
        return 4
    if rank == "منشئ":
        return 5
    if rank in ["منشئ اساسي", "مالك", "مالك اساسي"]:
        return 6
    if rank in ["مطور", "مطور ثانوي", "مطور اساسي"]:
        return 10
    return 2

def can_promote_to(message, rank):
    if message.from_user.id == OWNER_ID:
        return True
    try:
        cm = bot.get_chat_member(message.chat.id, message.from_user.id)
        if cm.status == "creator":
            return True
    except Exception:
        pass
    if rank in ["مطور", "مطور ثانوي", "مطور اساسي"]:
        bot.reply_to(message, "❌ رفع المطور للمطور الأساسي فقط")
        return False
    need = required_level_for_promote(rank)
    if rank_level(message.chat.id, message.from_user.id) >= need:
        return True
    bot.reply_to(message, "❌ رتبتك ما تسمح ترفع هذه الرتبة")
    return False

def tag_by_kind(message, kind):
    if not can_admin(message):
        return
    cid = sid(message.chat.id)
    ids = list(data["messages"].get(cid, {}).keys())
    if not ids:
        return bot.reply_to(message, "ماكو أعضاء مخزنين بعد")
    tags = []
    for uid in ids:
        try:
            level = rank_level(message.chat.id, int(uid))
            real_admin = False
            try:
                cm = bot.get_chat_member(message.chat.id, int(uid))
                real_admin = cm.status in ["creator", "administrator"]
            except Exception:
                pass
            if kind == "admins" and (level >= 2 or real_admin):
                tags.append(f"<a href='tg://user?id={uid}'>.</a>")
            elif kind == "members" and level < 2 and not real_admin:
                tags.append(f"<a href='tg://user?id={uid}'>.</a>")
            elif kind == "all":
                tags.append(f"<a href='tg://user?id={uid}'>.</a>")
        except Exception:
            pass
    if not tags:
        return bot.reply_to(message, "ماكو أشخاص مناسبين للتاك")
    chunk = ""
    for t in tags[:120]:
        chunk += t + " "
        if len(chunk) > 3500:
            bot.send_message(message.chat.id, chunk)
            chunk = ""
    if chunk:
        bot.send_message(message.chat.id, chunk)

def get_rank(chat_id, user_id):
    if user_id == OWNER_ID:
        return "مطور اساسي"
    return data["ranks"].get(sid(chat_id), {}).get(sid(user_id), "عضو")

def rank_level(chat_id, user_id):
    return RANK_ORDER.get(get_rank(chat_id, user_id), 0)

def set_rank(chat_id, user_id, rank):
    data["ranks"].setdefault(sid(chat_id), {})
    data["ranks"][sid(chat_id)][sid(user_id)] = rank
    save_data(data)

def del_rank(chat_id, user_id):
    cid, uid = sid(chat_id), sid(user_id)
    if cid in data["ranks"]:
        data["ranks"][cid].pop(uid, None)
        save_data(data)

def is_admin(chat_id, user_id):
    if user_id == OWNER_ID: return True
    try:
        m = bot.get_chat_member(chat_id, user_id)
        if m.status in ["creator","administrator"]: return True
    except: pass
    return rank_level(chat_id, user_id) >= 2

def can_admin(message, min_level=2):
    if message.chat.type == "private":
        bot.reply_to(message, "❌ هذا الأمر داخل الكروب فقط")
        return False
    if message.from_user.id == OWNER_ID:
        return True
    try:
        m = bot.get_chat_member(message.chat.id, message.from_user.id)
        if m.status in ["creator","administrator"]:
            return True
    except: pass
    if rank_level(message.chat.id, message.from_user.id) < min_level:
        bot.reply_to(message, "❌ ما عندك صلاحية لهذا الأمر")
        return False
    return True

def target_user(message):
    if message.reply_to_message and message.reply_to_message.from_user:
        return message.reply_to_message.from_user
    # دعم محدود للمعرف: Telegram Bot API ما يطلع id من username إذا ما عنده تفاعل سابق
    m = re.search(r"@(\w+)", message.text or "")
    if m:
        uname = m.group(1).lower()
        for uid, info in data["users"].items():
            if str(info.get("username","")).lower() == uname:
                class U: pass
                u = U(); u.id = int(uid); u.first_name = info.get("name",""); u.username = info.get("username","")
                return u
        bot.reply_to(message, "ما اعرف ايدي هذا المعرف، خليه يكتب بالبـوت أو استخدم الأمر بالرد")
        return None
    bot.reply_to(message, "❗ رد على رسالة الشخص")
    return None

def parse_amount(text):
    nums = re.findall(r"\d+", text)
    return max(1, int(nums[0])) if nums else None

def display_name(uid):
    info = data["users"].get(sid(uid), {})
    return info.get("name") or sid(uid)

def main_menu():
    return {"inline_keyboard": [
        [blue_btn("• 1 •", "help_locks"), blue_btn("• 2 •", "help_manager")],
        [blue_btn("• 3 •", "help_delete")],
        [blue_btn("• 4 •", "help_admin"), blue_btn("• 5 •", "help_entertainment")],
        [blue_btn("• 6 •", "help_games")],
        [blue_btn("البنك", "help_bank"), blue_btn("الميوزك", "help_music")],
        [red_btn("SOURCE FADI", url=f"https://t.me/{DEV_USERNAME}")]
    ]}

def owner_panel():
    return {"inline_keyboard": [
        [blue_btn("صانع الردود", "owner_add_reply"), blue_btn("الردود", "owner_replies")],
        [blue_btn("المستخدمين", "owner_users"), blue_btn("الكروبات", "owner_groups")],
        [blue_btn("إشعار الدخول", "owner_notify"), blue_btn("رجوع", "commands")]
    ]}

def start_buttons():
    return {"inline_keyboard": [
        [blue_btn("المطور", url=f"https://t.me/{DEV_USERNAME}")],
        [blue_btn("اضفني للكروب", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [blue_btn("شراء بوت مشابه", url=f"https://t.me/{DEV_USERNAME}")],
        [blue_btn("الأوامر", "commands")]
    ]}

def add_point(uid, n=1):
    uid = sid(uid)
    data["points"][uid] = data["points"].get(uid, 0) + n
    save_data(data)

def bank_user(uid):
    return data["bank"].get(sid(uid))

def create_bank(uid):
    uid = sid(uid)
    if uid in data["bank"]: return False
    data["bank"][uid] = {"account": random.randint(100000,999999), "money": 1000, "medals": [], "wife": None}
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

def make_quiz(message, game_name):
    if not chat_settings(message.chat.id).get("games", True):
        return bot.reply_to(message, "❌ الألعاب معطلة")
    if game_name in ["رياضيات", "احسب"]:
        a,b = random.randint(1,30), random.randint(1,30)
        op = random.choice(["+","-","*"])
        ans = str(eval(f"{a}{op}{b}"))
        q = f"🧮 جاوب بالرد:\n{a} {op} {b} = ؟"
    else:
        q, ans = random.choice(GAME_QUESTIONS.get(game_name, [("اكتب صح","صح")]))
        q = f"🎮 لعبة {game_name}\n\n{q}\n\nجاوب بالرد على هذه الرسالة"
    m = bot.reply_to(message, q)
    quiz_games[m.message_id] = {"answer": ans.strip().lower(), "chat": message.chat.id, "game": game_name}

def list_rank(chat_id, rank):
    cid = sid(chat_id)
    arr = [(uid,r) for uid,r in data["ranks"].get(cid, {}).items() if r == rank]
    if not arr: return f"ماكو {rank}"
    return "\n".join([f"{i+1}. {display_name(uid)} - <code>{uid}</code>" for i,(uid,_) in enumerate(arr[:100])])

def clear_rank(chat_id, rank):
    cid = sid(chat_id)
    if cid not in data["ranks"]: return
    for uid in list(data["ranks"][cid].keys()):
        if data["ranks"][cid][uid] == rank:
            del data["ranks"][cid][uid]
    save_data(data)

def punish_locked(message, lock_key):
    actions = get_lock_actions(message.chat.id)
    action = actions.get(lock_key, "delete")
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except: pass
    if action == "kick":
        try:
            bot.ban_chat_member(message.chat.id, message.from_user.id)
            bot.unban_chat_member(message.chat.id, message.from_user.id)
        except: pass
    elif action == "mute":
        try: bot.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=False)
        except: pass
    elif action == "restrict":
        try: bot.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=False)
        except: pass

def detect_lock_violation(message):
    locks = get_locks(message.chat.id)
    text = message.text or message.caption or ""
    if locks.get("all"): return "all"
    if locks.get("links") and URL_RE.search(text): return "links"
    if locks.get("username") and "@" in text: return "username"
    if locks.get("tag") and "@" in text: return "tag"
    if locks.get("hashtag") and "#" in text: return "hashtag"
    if locks.get("english") and EN_RE.search(text): return "english"
    if locks.get("persian") and PERSIAN_RE.search(text): return "persian"
    if locks.get("bad_words") and any(w in text.lower() for w in BAD_WORDS): return "bad_words"
    if locks.get("long_text") and len(text) > 400: return "long_text"
    if locks.get("photos") and message.content_type == "photo": return "photos"
    if locks.get("videos") and message.content_type == "video": return "videos"
    if locks.get("stickers") and message.content_type == "sticker": return "stickers"
    if locks.get("animation") and message.content_type == "animation": return "animation"
    if locks.get("files") and message.content_type == "document": return "files"
    if locks.get("voice") and message.content_type == "voice": return "voice"
    if locks.get("media") and message.content_type in ["photo","video","sticker","animation","document","audio","voice"]: return "media"
    if locks.get("forward") and getattr(message, "forward_date", None): return "forward"
    if locks.get("bots") and message.new_chat_members:
        for u in message.new_chat_members:
            if getattr(u, "is_bot", False): return "bots"
    return None


# ================= نظام الألعاب والنقاط والترند =================
OPTION_GAMES = {
    "لغز": [("شنو عاصمة أستراليا؟", "كانبيرا", ["سيدني", "ملبورن"]),("شي كلما أخذت منه كبر؟", "الحفرة", ["البحر", "الجبل"]),("له أسنان ولا يعض؟", "المشط", ["القلم", "الباب"]),("يمشي بلا رجلين ويبكي بلا عينين؟", "السحاب", ["النهر", "الهواء"]),("بيت بلا أبواب ولا شبابيك؟", "البيضة", ["الصندوق", "الكهف"])],
    "عربي": [("ما ضد كلمة طويل؟", "قصير", ["كبير", "بعيد"]),("جمع كتاب؟", "كتب", ["كتابات", "كاتب"]),("مرادف سريع؟", "عاجل", ["بطيء", "ثقيل"]),("ما معنى الغيث؟", "المطر", ["الشمس", "الريح"]),("ضد كلمة ليل؟", "نهار", ["قمر", "ظلام"])],
    "اعلام": [("🇮🇶", "العراق", ["سوريا", "مصر"]),("🇸🇦", "السعودية", ["قطر", "الإمارات"]),("🇪🇬", "مصر", ["العراق", "لبنان"]),("🇬🇷", "اليونان", ["إيطاليا", "إسبانيا"]),("🇹🇷", "تركيا", ["تونس", "المغرب"])],
    "سيارات": [("🚗 سيارة شعارها الحصان؟", "فيراري", ["تويوتا", "BMW"]),("🚙 شركة يابانية مشهورة؟", "تويوتا", ["مرسيدس", "فورد"]),("🏎️ سيارة ألمانية فخمة؟", "مرسيدس", ["كيا", "هيونداي"]),("🚘 شركة شعارها أربع حلقات؟", "أودي", ["نيسان", "رنج روفر"]),("🚕 سيارة كهربائية مشهورة؟", "تسلا", ["دودج", "مازدا"])],
    "مشاهير": [("لاعب أرجنتيني مشهور؟", "ميسي", ["رونالدو", "نيمار"]),("مؤسس شركة مايكروسوفت؟", "بيل غيتس", ["إيلون ماسك", "زوكربيرغ"]),("ممثل مصري مشهور قديم؟", "عادل إمام", ["كاظم الساهر", "ميسي"]),("مغني عراقي مشهور؟", "كاظم الساهر", ["فيروز", "أم كلثوم"]),("مخترع المصباح الكهربائي؟", "إديسون", ["نيوتن", "آينشتاين"])],
    "رياضيات": [("2 + 2 = ؟", "4", ["5", "3"]),("5 × 3 = ؟", "15", ["20", "10"]),("12 - 7 = ؟", "5", ["6", "4"])],
    "انكليزي": [("ترجمة Book؟", "كتاب", ["قلم", "باب"]),("ترجمة Water؟", "ماء", ["نار", "هواء"]),("ترجمة Cat؟", "قطة", ["كلب", "طير"])],
    "عواصم": [("عاصمة العراق؟", "بغداد", ["البصرة", "الموصل"]),("عاصمة مصر؟", "القاهرة", ["الإسكندرية", "طنطا"]),("عاصمة فرنسا؟", "باريس", ["لندن", "روما"])],
    "كلمات": [("كلمة تبدأ بحرف م؟", "ماء", ["باب", "قلم"]),("كلمة تبدأ بحرف ب؟", "بيت", ["شمس", "قمر"])],
    "بات": [("اكتب كلمة بات", "بات", ["تاب", "باب"])],
    "امثله": [("أكمل المثل: الصديق وقت ...", "الضيق", ["الفرح", "النوم"])],
}
CUT_QUESTIONS=["شنو أكثر موقف محرج صارلك؟","منو أقرب شخص لقلبك؟","شنو حلمك الحقيقي؟","إذا رجع بيك الزمن شتغير؟","شنو أكثر شي تخاف منه؟"]
FAST_WORDS=["تفاحة","عراق","فادي","قمر","شمس","ورد","مطر","كتاب","نهر","ذهب"]
WOULD_YOU=[("تعيش غني وحيد","تعيش فقير ويه ناس تحبك"),("تسافر للمستقبل","ترجع للماضي"),("ما تنام يومين","ما تستخدم نت أسبوع"),("تربح مليون","تعيش مرتاح طول عمرك")]
XO_WINS=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def add_messages(uid, chat_id, n):
    cid, uid = sid(chat_id), sid(uid)
    data["messages"].setdefault(cid,{})
    data["messages"][cid][uid]=data["messages"][cid].get(uid,0)+n
    save_data(data)

def pick_option_question(chat_id, game):
    pool=OPTION_GAMES.get(game, OPTION_GAMES["لغز"]); key=f"{chat_id}:{game}"
    used=data.get("last_games",{}).get(key,[]); avail=[i for i in range(len(pool)) if i not in used]
    if not avail: avail=list(range(len(pool))); used=[]
    idx=random.choice(avail); used.append(idx)
    data.setdefault("last_games",{})[key]=used[-max(3,len(pool)//2):]; save_data(data)
    return pool[idx]

def option_keyboard(gid, options):
    return {"inline_keyboard":[[blue_btn(opt, f"gans:{gid}:{i}")] for i,opt in enumerate(options)]}

def start_option_game(message, game):
    question, answer, wrongs = pick_option_question(message.chat.id, game)
    choices=[answer]+list(wrongs); random.shuffle(choices)
    gid=f"{message.chat.id}:{message.message_id}:{int(time.time())}:{random.randint(100,999)}"
    data.setdefault("game_sessions",{})[gid]={"type":"option","game":game,"answer":answer,"choices":choices}; save_data(data)
    raw_send_message(message.chat.id, f"{game}:\n❞ {question} ❝", option_keyboard(gid, choices), message.message_id)

def xo_board_keyboard(gid, board):
    rows=[]
    for r in range(3):
        row=[]
        for c in range(3):
            i=r*3+c; row.append(blue_btn(board[i] if board[i]!=" " else "•", f"xo_cell:{gid}:{i}"))
        rows.append(row)
    return {"inline_keyboard":rows}

def check_xo_winner(board):
    for a,b,c in XO_WINS:
        if board[a]!=" " and board[a]==board[b]==board[c]: return board[a]
    return "draw" if " " not in board else None

def start_xo(message):
    gid=f"xo:{message.chat.id}:{message.message_id}:{int(time.time())}"
    data.setdefault("game_sessions",{})[gid]={"type":"xo","players":[message.from_user.id,None],"names":[message.from_user.first_name,None],"board":[" "]*9,"turn":"❌","symbols":{sid(message.from_user.id):"❌"}}; save_data(data)
    raw_send_message(message.chat.id, f"لعبة XO\n\nاللاعب الأول: {message.from_user.first_name} ❌\nبانتظار اللاعب الثاني...", {"inline_keyboard":[[blue_btn("انضم كلاعب ثاني ⭕", f"xo_join:{gid}")]]}, message.message_id)

def start_rps(message):
    gid=f"rps:{message.chat.id}:{message.message_id}:{int(time.time())}"
    data.setdefault("game_sessions",{})[gid]={"type":"rps","starter":message.from_user.id}; save_data(data)
    raw_send_message(message.chat.id, "لعبة حجرة ورقة مقص\nاختار:", {"inline_keyboard":[[blue_btn("حجرة",f"rps:{gid}:rock"),blue_btn("ورقة",f"rps:{gid}:paper"),blue_btn("مقص",f"rps:{gid}:scissors")]]}, message.message_id)

def start_fast(message):
    word=random.choice(FAST_WORDS); data.setdefault("active_fast",{})[sid(message.chat.id)]={"word":word,"time":now_time()}; save_data(data)
    bot.reply_to(message, f"⚡ لعبة الاسرع\n\nاول واحد يكتب:\n{word}")

def start_would_you(message):
    a,b=random.choice(WOULD_YOU); gid=f"wc:{message.chat.id}:{message.message_id}:{int(time.time())}"
    data.setdefault("wc_votes",{})[gid]={"a":0,"b":0,"voters":[]}; save_data(data)
    raw_send_message(message.chat.id, "لو خيروك؟", {"inline_keyboard":[[blue_btn(a,f"wc:{gid}:a")],[blue_btn(b,f"wc:{gid}:b")]]}, message.message_id)

def send_commands(message, section=None):
    if section and section in COMMAND_TEXTS:
        return bot.reply_to(message, COMMAND_TEXTS[section])
    return raw_send_message(message.chat.id, "الاوامر\n\n- اليك اوامر البوت\n\n- [ 1م ] اوامر الحمايه\n- [ 2م ] اوامر المشرفين\n- [ 3م ] اوامر المسح\n- [ 4م ] اوامر الرفع والحظر\n- [ 5م ] اوامر الترفيه\n- [ 6م ] اوامر الالعاب", main_menu(), message.message_id)

@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.type != "private": return
    register_user(message)
    if not check_sub(message): return
    if message.from_user.id == OWNER_ID:
        raw_send_message(message.chat.id, "⚙️ <b>لوحة تحكم المطور</b>\n\nاختر من الأزرار:", owner_panel())
    else:
        raw_send_photo(message.chat.id, START_PHOTO, "أهلاً بك في بوت فادي المطور\nاختر من الأزرار بالأسفل", start_buttons())

@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    try: bot.answer_callback_query(call.id)
    except: pass
    if call.data.startswith("gans:"):
        _, gid, idx = call.data.split(":",2); game=data.get("game_sessions",{}).get(gid)
        if not game: return bot.answer_callback_query(call.id,"انتهت اللعبة",show_alert=True)
        choice=game["choices"][int(idx)]
        if choice==game["answer"]:
            add_point(call.from_user.id)
            return raw_edit_message(call.message.chat.id, call.message.message_id, f"✅ إجابة صحيحة\nالفائز: {call.from_user.first_name}\nربحت نقطة")
        return bot.answer_callback_query(call.id,"❌ إجابة خاطئة",show_alert=True)
    if call.data.startswith("xo_join:"):
        gid=call.data.replace("xo_join:","",1); game=data.get("game_sessions",{}).get(gid)
        if not game or game.get("type")!="xo": return bot.answer_callback_query(call.id,"اللعبة غير موجودة",show_alert=True)
        if game["players"][0]==call.from_user.id: return bot.answer_callback_query(call.id,"أنت اللاعب الأول",show_alert=True)
        if game["players"][1] is not None: return bot.answer_callback_query(call.id,"اللعبة اكتملت",show_alert=True)
        game["players"][1]=call.from_user.id; game["names"][1]=call.from_user.first_name; game["symbols"][sid(call.from_user.id)]="⭕"; data["game_sessions"][gid]=game; save_data(data)
        return raw_edit_message(call.message.chat.id, call.message.message_id, f"XO\n❌ {game['names'][0]}\n⭕ {game['names'][1]}\n\nالدور: ❌", xo_board_keyboard(gid, game["board"]))
    if call.data.startswith("xo_cell:"):
        _, gid, pos=call.data.split(":",2); pos=int(pos); game=data.get("game_sessions",{}).get(gid)
        if not game or game.get("type")!="xo": return bot.answer_callback_query(call.id,"اللعبة غير موجودة",show_alert=True)
        if call.from_user.id not in game["players"]: return bot.answer_callback_query(call.id,"هاي اللعبة مو إلك",show_alert=True)
        sym=game["symbols"].get(sid(call.from_user.id))
        if sym!=game["turn"]: return bot.answer_callback_query(call.id,"مو دورك",show_alert=True)
        if game["board"][pos]!=" ": return bot.answer_callback_query(call.id,"المكان مأخوذ",show_alert=True)
        game["board"][pos]=sym; winner=check_xo_winner(game["board"])
        if winner:
            if winner=="draw": txt="XO\nتعادل 🤝"
            else:
                uid=game["players"][0] if winner=="❌" else game["players"][1]; name=game["names"][0] if winner=="❌" else game["names"][1]; add_point(uid); txt=f"XO\nالفائز: {name} {winner}\nربح نقطة"
            data["game_sessions"].pop(gid,None); save_data(data); return raw_edit_message(call.message.chat.id, call.message.message_id, txt, xo_board_keyboard(gid, game["board"]))
        game["turn"]="⭕" if game["turn"]=="❌" else "❌"; data["game_sessions"][gid]=game; save_data(data)
        return raw_edit_message(call.message.chat.id, call.message.message_id, f"XO\n❌ {game['names'][0]}\n⭕ {game['names'][1]}\n\nالدور: {game['turn']}", xo_board_keyboard(gid, game["board"]))
    if call.data.startswith("rps:"):
        _, gid, choice=call.data.split(":",2); game=data.get("game_sessions",{}).get(gid)
        if not game or call.from_user.id!=game.get("starter"): return bot.answer_callback_query(call.id,"هاي اللعبة مو إلك",show_alert=True)
        bot_choice=random.choice(["rock","paper","scissors"]); names={"rock":"حجرة","paper":"ورقة","scissors":"مقص"}
        win=(choice=="rock" and bot_choice=="scissors") or (choice=="paper" and bot_choice=="rock") or (choice=="scissors" and bot_choice=="paper")
        result="تعادل 🤝" if choice==bot_choice else ("فزت ✅\nربحت نقطة" if win else "خسرت ❌")
        if win: add_point(call.from_user.id)
        data["game_sessions"].pop(gid,None); save_data(data)
        return raw_edit_message(call.message.chat.id, call.message.message_id, f"اختيارك: {names[choice]}\nاختيار البوت: {names[bot_choice]}\n\n{result}")
    if call.data.startswith("wc:"):
        _, gid, side=call.data.split(":",2); vote=data.get("wc_votes",{}).get(gid)
        if not vote: return
        if sid(call.from_user.id) in vote["voters"]: return bot.answer_callback_query(call.id,"مصوت قبل",show_alert=True)
        vote[side]+=1; vote["voters"].append(sid(call.from_user.id)); data["wc_votes"][gid]=vote; save_data(data)
        return bot.answer_callback_query(call.id, f"تم التصويت\nA: {vote['a']} | B: {vote['b']}", show_alert=True)
    if call.data == "commands":
        return raw_edit_message(call.message.chat.id, call.message.message_id, "الاوامر\n\n- اليك اوامر البوت\n\n- [ 1م ] اوامر الحمايه\n- [ 2م ] اوامر المشرفين\n- [ 3م ] اوامر المسح\n- [ 4م ] اوامر الرفع والحظر\n- [ 5م ] اوامر الترفيه\n- [ 6م ] اوامر الالعاب", main_menu())
    sections={"help_admin":"admin","help_locks":"locks","help_manager":"manager","help_delete":"delete","help_creator":"creator","help_owner":"owner","help_members":"members","help_bank":"bank","help_games":"games","help_entertainment":"entertainment","help_fun":"fun","help_dev":"dev"}
    if call.data=="help_music": return raw_edit_message(call.message.chat.id, call.message.message_id, "<b>❨ أوامر الميوزك ❩</b>\n\n- يوت اسم الأغنية\n- بحث يوتيوب اسم الفيديو", main_menu())
    if call.data in sections: return raw_edit_message(call.message.chat.id, call.message.message_id, COMMAND_TEXTS[sections[call.data]], main_menu())
    if call.data.startswith("owner_"):
        if call.from_user.id != OWNER_ID: return bot.answer_callback_query(call.id,"للمطور فقط",show_alert=True)
        if call.data=="owner_add_reply": waiting_reply[call.from_user.id]={"step":"add_word"}; return bot.send_message(call.message.chat.id,"اكتب الكلمة:")
        if call.data=="owner_replies": return bot.send_message(call.message.chat.id,"📜 الردود:\n"+("\n".join(data["replies"].keys()) if data["replies"] else "ماكو"))
        if call.data=="owner_users": return bot.send_message(call.message.chat.id,f"👥 عدد المستخدمين: {len(data['users'])}")
        if call.data=="owner_groups": return bot.send_message(call.message.chat.id,f"📊 عدد الكروبات: {len(data['groups'])}")
        if call.data=="owner_notify": data["notify"]=not data.get("notify",True); save_data(data); return bot.send_message(call.message.chat.id,"🔔 إشعار الدخول: "+("مفعل" if data["notify"] else "متوقف"))

@bot.message_handler(content_types=["new_chat_members", "left_chat_member"])
def delete_join_leave(message):
    try:
        notify_bot_added(message)
    except Exception:
        pass
    try: bot.delete_message(message.chat.id, message.message_id)
    except: pass
    try: register_user(message)
    except: pass

@bot.message_handler(content_types=["text","photo","video","sticker","animation","document","audio","voice","contact"])
def handler(message):
    register_user(message)
    update_activity(message)
    save_media_message(message)

    if message.from_user and sid(message.from_user.id) in data.get("global_ban", []):
        return
    if message.chat.type != "private" and message.from_user and sid(message.from_user.id) in data.get("global_mute", []):
        try: bot.delete_message(message.chat.id, message.message_id)
        except: pass
        return

    text = message.text or message.caption or ""

    # فلتر الحمايات قبل الأوامر للأعضاء فقط
    if message.chat.type != "private" and message.from_user and rank_level(message.chat.id, message.from_user.id) < 1 and not is_admin(message.chat.id, message.from_user.id):
        violation = detect_lock_violation(message)
        if violation:
            punish_locked(message, violation)
            return

    if not text: return
    text = text.strip()

    # الاشتراك الإجباري فقط عند استخدام الأوامر
    if message.chat.type != "private" and is_force_command(text) and not check_sub(message):
        return


    # اختصارات سورس فادي
    if text == "ت":
        text = "تثبيت"
    if text == "ر":
        text = "الرابط"
    if text in ["م", "اد", "من", "مط"] and message.reply_to_message:
        shortcut_rank = {"م": "مميز", "اد": "ادمن", "من": "منشئ", "مط": "مطور"}[text]
        text = "رفع " + shortcut_rank

    fast=data.get("active_fast",{}).get(sid(message.chat.id))
    if fast and text==fast.get("word"):
        add_point(message.from_user.id); data["active_fast"].pop(sid(message.chat.id),None); save_data(data)
        return bot.reply_to(message, f"⚡ الفائز: {message.from_user.first_name}\nربحت نقطة")
    if text in ["لغز","سيارات","اعلام","مشاهير","عربي","رياضيات","انكليزي","عواصم","كلمات","بات","امثله"]: return start_option_game(message,text)
    if text in ["اكس او","XO","xo","اكسو"]: return start_xo(message)
    if text=="حجرة": return start_rps(message)
    if text=="الاسرع": return start_fast(message)
    if text in ["كت","كت تويت","صراحة"]: return bot.reply_to(message, random.choice(CUT_QUESTIONS))
    if text=="لو خيروك": return start_would_you(message)
    if text in ["تحدي","عقاب","روليت"]:
        members=list(data["messages"].get(sid(message.chat.id),{}).keys())
        return bot.reply_to(message, f"🎯 الاختيار وقع على: {display_name(random.choice(members))}" if members else "ماكو أعضاء متفاعلين بعد")
    if text=="تفكيك": return bot.reply_to(message,"اكتب: فكك + الكلمة")
    if text.startswith("فكك "): return bot.reply_to(message," ".join(list(text.replace("فكك ","",1).strip())))
    if text=="نقاطي": return bot.reply_to(message, f"نقاطك: {data['points'].get(sid(message.from_user.id),0)}")
    if text.startswith("بيع نقاطي"):
        pts=data["points"].get(sid(message.from_user.id),0); amount=parse_amount(text) or pts
        if amount<=0 or pts<amount: return bot.reply_to(message,"نقاطك ما تكفي")
        data["points"][sid(message.from_user.id)]=pts-amount; add_messages(message.from_user.id,message.chat.id,amount*5); save_data(data)
        return bot.reply_to(message, f"تم بيع {amount} نقاط\nتمت إضافة {amount*5} رسالة إلى رسائلك")
    if text=="ترند":
        items=sorted(data["messages"].get(sid(message.chat.id),{}).items(), key=lambda x:x[1], reverse=True)[:10]
        if not items: return bot.reply_to(message,"ماكو ترند بعد")
        return bot.reply_to(message,"\n".join(["- ترند المجموعة .\n"]+[f"{i}- {display_name(uid)} ↢ {cnt} رسالة" for i,(uid,cnt) in enumerate(items,1)]))
    if text in ["تصفير الترند","تصفير ترند"]:
        if not can_admin(message): return
        data["messages"][sid(message.chat.id)]={}; save_data(data); return bot.reply_to(message,"تم تصفير الترند")
    if text=="ا":
        st=chat_settings(message.chat.id)
        if not st.get("id",True): return
        u=message.reply_to_message.from_user if message.reply_to_message else message.from_user
        rank=get_rank(message.chat.id,u.id) if message.chat.type!="private" else "عضو"; username=f"@{u.username}" if u.username else "لايوجد"
        pts=data["points"].get(sid(u.id),0); msgs=data["messages"].get(sid(message.chat.id),{}).get(sid(u.id),0)
        txt=f"- الاسم: {u.first_name}\n- اليوزر: {username}\n- الايدي: <code>{u.id}</code>\n- الرتبة: {rank}\n- الرسائل: {msgs}\n- النقاط: {pts}"
        if st.get("id_photo",True):
            try:
                photos=bot.get_user_profile_photos(u.id,limit=1)
                if photos.total_count>0: return bot.send_photo(message.chat.id,photos.photos[0][-1].file_id,caption=txt,reply_to_message_id=message.message_id)
            except: pass
        return bot.reply_to(message,txt)
    if text=="ز":
        members=[x for x in data["messages"].get(sid(message.chat.id),{}).keys() if x!=sid(message.from_user.id)]
        if not members: return bot.reply_to(message,"ماكو أعضاء كفاية")
        partner=random.choice(members); data["marriages"][sid(message.from_user.id)]=partner; save_data(data)
        return bot.reply_to(message, f"💍 تم زواجك من {display_name(partner)}")

    # إجابات الألعاب
    if message.reply_to_message and message.reply_to_message.message_id in quiz_games:
        q = quiz_games[message.reply_to_message.message_id]
        if text.strip().lower() == q["answer"]:
            add_point(message.from_user.id)
            quiz_games.pop(message.reply_to_message.message_id, None)
            return bot.reply_to(message, f"✅ مبروك جوابك صح\nربحت نقطة 🎉\nنقاطك: {data['points'].get(sid(message.from_user.id),0)}")
        return bot.reply_to(message, "❌ جوابك غلط")

    # انتظار الردود
    if message.from_user.id in waiting_reply:
        st = waiting_reply[message.from_user.id]
        if st["step"] == "add_word":
            waiting_reply[message.from_user.id] = {"step":"add_answer","word":text}
            return bot.reply_to(message, "اكتب الرد:")
        if st["step"] == "add_answer":
            data["replies"][st["word"]] = text; save_data(data); del waiting_reply[message.from_user.id]
            return bot.reply_to(message, "✅ تم إضافة الرد")
        if st["step"] == "del_word":
            data["replies"].pop(text, None); save_data(data); del waiting_reply[message.from_user.id]
            return bot.reply_to(message, "✅ تم حذف الرد")
        if st["step"] == "set_welcome":
            data["welcome_text"][sid(message.chat.id)] = text; save_data(data); del waiting_reply[message.from_user.id]
            return bot.reply_to(message, "✅ تم وضع الترحيب")
        if st["step"] == "set_laws":
            data["laws"][sid(message.chat.id)] = text; save_data(data); del waiting_reply[message.from_user.id]
            return bot.reply_to(message, "✅ تم وضع القوانين")

    # الردود
    if chat_settings(message.chat.id).get("replies", True) and text in data["replies"]:
        return bot.reply_to(message, data["replies"][text])
    if text in data["global_replies"]:
        return bot.reply_to(message, data["global_replies"][text])

    # القوائم

    if text == "تفع":
        if not can_admin(message): return
        chat_settings(message.chat.id)["id_photo"] = True
        save_data(data)
        return bot.reply_to(message, "✅ تم تفعيل الايدي بالصورة")
    if text == "تعط":
        if not can_admin(message): return
        chat_settings(message.chat.id)["id_photo"] = False
        save_data(data)
        return bot.reply_to(message, "✅ تم تعطيل الايدي بالصورة")

    if text in ["الاوامر","الأوامر","اوامر","اوامري"]:
        return send_commands(message)
    command_sections = {
        "اوامر الحمايه":"locks","اوامر الحماية":"locks","الحمايه":"locks","الحماية":"locks",
        "اوامر ادمنية":"admin","اوامر الادمنيه":"admin","اوامر المدراء":"manager",
        "اوامر المالك":"owner","اوامر المنشئ":"creator","اوامر الاعضاء":"members",
        "اوامر البنك":"bank","اوامر الالعاب":"games","اوامر الألعاب":"games",
        "اوامر التسليه":"entertainment","اوامر التحشيش":"fun","اوامر المطور":"dev"
    }
    if text in command_sections:
        return send_commands(message, command_sections[text])

    if text in ["لوحة","لوحه"] and message.from_user.id == OWNER_ID:
        return bot.reply_to(message, "لوحة المطور", reply_markup=owner_panel())
    if text == "سورس": return bot.reply_to(message, "أهلاً بك في سورس فادي 🔥")
    if text == "المطور": return bot.reply_to(message, f"👨‍💻 المطور: @{DEV_USERNAME}")
    if text == "شراء بوت مشابه": return bot.reply_to(message, f"للشراء راسل: @{DEV_USERNAME}")

    # تفعيل وتعطيل البوت للمطور
    if text in ["تعطيل","تفعيل"] and message.from_user.id == OWNER_ID:
        data["bot_enabled"] = text == "تفعيل"; save_data(data)
        return bot.reply_to(message, "✅ تم " + ("تفعيل البوت" if data["bot_enabled"] else "تعطيل البوت"))
    if not data.get("bot_enabled", True) and message.from_user.id != OWNER_ID:
        return

    # أوامر المطور العامة
    if text == "الاحصائيات" and message.from_user.id == OWNER_ID:
        return bot.reply_to(message, f"👥 المستخدمين: {len(data['users'])}\n📊 الكروبات: {len(data['groups'])}\n🏦 حسابات البنك: {len(data['bank'])}")
    if text.startswith("اذاعه ") and message.from_user.id == OWNER_ID:
        msg = text.replace("اذاعه ","",1)
        ok = 0
        for cid in list(data["groups"].keys()) + list(data["users"].keys()):
            try: bot.send_message(int(cid), msg); ok += 1
            except: pass
        return bot.reply_to(message, f"✅ تمت الإذاعة إلى {ok}")
    if text == "جلب النسخه الاحتياطيه" and message.from_user.id == OWNER_ID:
        try: return bot.send_document(message.chat.id, open(DATA_FILE, "rb"))
        except: return bot.reply_to(message, "ماكو نسخة")
    if text in ["تفعيل الاشتراك الاجباري","تعطيل الاشتراك الاجباري"] and message.from_user.id == OWNER_ID:
        data["force_enabled"] = text.startswith("تفعيل"); save_data(data)
        return bot.reply_to(message, "✅ تم التحديث")
    if text.startswith("تغيير الاشتراك الاجباري ") and message.from_user.id == OWNER_ID:
        global FORCE_CHANNEL
        FORCE_CHANNEL = text.split(maxsplit=2)[2].strip()
        data["force_channel_saved"] = FORCE_CHANNEL; save_data(data)
        return bot.reply_to(message, f"✅ صار الاشتراك: {FORCE_CHANNEL}")

    # ايدي ومعلومات
    if text in ["ايدي","معلوماتي","ايدي بالرد"] or text.startswith("ايدي "):
        u = message.reply_to_message.from_user if message.reply_to_message else message.from_user
        rank = get_rank(message.chat.id, u.id) if message.chat.type != "private" else "عضو"
        username = f"@{u.username}" if u.username else "لايوجد"
        pts = data["points"].get(sid(u.id), 0)
        msgs = data["messages"].get(sid(message.chat.id), {}).get(sid(u.id), 0)
        txt = f"↶ الاسم = {u.first_name}\n↶ اليوزر = {username}\n↶ الرتبه = {rank}\n↶ الايدي = <code>{u.id}</code>\n↶ الرسائل = {msgs}\n↶ النقاط = {pts}"
        if chat_settings(message.chat.id).get("id_photo", True):
            try:
                photos = bot.get_user_profile_photos(u.id, limit=1)
                if photos.total_count > 0:
                    return bot.send_photo(message.chat.id, photos.photos[0][-1].file_id, caption=txt, reply_to_message_id=message.message_id)
            except: pass
        return bot.reply_to(message, txt)

    if text in ["اسمي","معرفي","رتبتي","صلاحياتي","رسائلي","نقاطي","تفاعلي"]:
        if text == "اسمي": return bot.reply_to(message, message.from_user.first_name or "ماكو")
        if text == "معرفي": return bot.reply_to(message, f"@{message.from_user.username}" if message.from_user.username else "ما عندك معرف")
        if text == "رتبتي": return bot.reply_to(message, get_rank(message.chat.id, message.from_user.id))
        if text == "رسائلي": return bot.reply_to(message, f"رسائلك: {data['messages'].get(sid(message.chat.id),{}).get(sid(message.from_user.id),0)}")
        if text == "نقاطي": return bot.reply_to(message, f"نقاطك: {data['points'].get(sid(message.from_user.id),0)}")
        if text == "تفاعلي": return bot.reply_to(message, f"تفاعلك: {data['activity'].get(sid(message.from_user.id),0)}")
        if text == "صلاحياتي":
            try:
                cm = bot.get_chat_member(message.chat.id, message.from_user.id)
                lines = [
                    f"- الرتبة: {get_rank(message.chat.id, message.from_user.id)}",
                    f"- الحالة: {cm.status}",
                    f"- حذف الرسائل: {'✓' if getattr(cm, 'can_delete_messages', False) else '✗'}",
                    f"- حظر/تقييد: {'✓' if getattr(cm, 'can_restrict_members', False) else '✗'}",
                    f"- تثبيت: {'✓' if getattr(cm, 'can_pin_messages', False) else '✗'}",
                    f"- دعوة أعضاء: {'✓' if getattr(cm, 'can_invite_users', False) else '✗'}",
                    f"- رفع مشرفين: {'✓' if getattr(cm, 'can_promote_members', False) else '✗'}",
                ]
                return bot.reply_to(message, "صلاحياتك:\n" + "\n".join(lines))
            except Exception:
                return bot.reply_to(message, "صلاحياتك: " + ("اداري" if is_admin(message.chat.id, message.from_user.id) else "عضو"))

    if text == "منو ضافني":
        info = data["join_info"].get(sid(message.from_user.id))
        return bot.reply_to(message, f"تمت إضافتك إلى: {info.get('chat')}\nبواسطة: {info.get('by')}" if info else "ما عندي معلومات عن إضافتك.")

    # تفعيل وتعطيل إعدادات
    if text.startswith("تفعيل ") or text.startswith("تعطيل "):
        if not can_admin(message): return
        action = text.startswith("تفعيل ")
        name = text.replace("تفعيل ","",1).replace("تعطيل ","",1).strip()
        key = SETTING_ALIASES.get(name)
        if key:
            chat_settings(message.chat.id)[key] = action
            save_data(data)
            return bot.reply_to(message, f"✅ تم {'تفعيل' if action else 'تعطيل'} {name}")
        if name == "الكل":
            for k in chat_settings(message.chat.id):
                chat_settings(message.chat.id)[k] = action
            save_data(data)
            return bot.reply_to(message, f"✅ تم {'تفعيل' if action else 'تعطيل'} الكل")

    # القفل والفتح
    if text.startswith("قفل ") or text.startswith("فتح "):
        if not can_admin(message): return
        action = "قفل" if text.startswith("قفل ") else "فتح"
        rest = text.replace(action+" ","",1).strip()
        lock_action = "delete"
        for phrase, val in [("بالطرد","kick"),("بالكتم","mute"),("بالتقييد","restrict")]:
            if phrase in rest:
                lock_action = val
                rest = rest.replace(phrase,"").strip()
        key = LOCK_ALIASES.get(rest)
        if not key:
            return bot.reply_to(message, "هذا القفل غير موجود")
        get_locks(message.chat.id)[key] = action == "قفل"
        get_lock_actions(message.chat.id)[key] = lock_action
        save_data(data)
        return bot.reply_to(message, f"{'🔒 تم قفل' if action=='قفل' else '🔓 تم فتح'} {rest}")

    # مسح
    if text in ["امسح","مسح بالرد","مسح"]:
        if not can_admin(message): return
        if not message.reply_to_message: return bot.reply_to(message, "رد على رسالة")
        try:
            bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            bot.delete_message(message.chat.id, message.message_id)
        except: bot.reply_to(message, "ما اكدر أمسح")
        return
    if text.startswith("مسح ") and re.search(r"\d+", text):
        if not can_admin(message): return
        count = min(parse_amount(text), 100)
        for i in range(count + 1):
            try: bot.delete_message(message.chat.id, message.message_id - i)
            except: pass
        return
    if text in ["مسح الميديا","مسح الوسائط","مسح الصور","مسح الفيديو","مسح الفيديوهات","مسح الملصقات","مسح المتحركات","مسح الملفات","مسح الفويسات","مسح الصوتيات"]:
        if not can_admin(message): return
        cid = sid(message.chat.id)
        saved = data["media"].get(cid, [])
        type_map = {
            "مسح الصور":["photo"], "مسح الفيديو":["video"], "مسح الفيديوهات":["video"], "مسح الملصقات":["sticker"],
            "مسح المتحركات":["animation"], "مسح الملفات":["document"], "مسح الفويسات":["voice"], "مسح الصوتيات":["audio"],
            "مسح الميديا":["photo","video","sticker","animation","document","audio","voice"],
            "مسح الوسائط":["photo","video","sticker","animation","document","audio","voice"]
        }
        deleted, remain = 0, []
        for item in saved:
            if item["type"] in type_map[text]:
                try: bot.delete_message(message.chat.id, item["message_id"]); deleted += 1
                except: pass
            else: remain.append(item)
        data["media"][cid] = remain; save_data(data)
        return bot.reply_to(message, f"✅ تم تنظيف {deleted} رسالة")

    # إدارة الأشخاص
    if text in ["حظر","طرد","كتم","الغاء الكتم","الغاء حظر","الغاء الحظر","الغاء التقييد","رفع القيود","تقييد","انذار","كشف","تحكم"]:
        if text in ["حظر"] and not chat_settings(message.chat.id).get("ban_cmd", True): return
        if text in ["طرد"] and not chat_settings(message.chat.id).get("kick_cmd", True): return
        if text in ["كتم"] and not chat_settings(message.chat.id).get("mute_cmd", True): return
        if not can_admin(message): return
        u = target_user(message)
        if not u: return
        try:
            if text == "حظر":
                bot.ban_chat_member(message.chat.id, u.id); return bot.reply_to(message, "✅ تم الحظر")
            if text in ["الغاء حظر","الغاء الحظر"]:
                bot.unban_chat_member(message.chat.id, u.id); return bot.reply_to(message, "✅ تم الغاء الحظر")
            if text == "طرد":
                bot.ban_chat_member(message.chat.id, u.id); bot.unban_chat_member(message.chat.id, u.id); return bot.reply_to(message, "✅ تم الطرد")
            if text == "كتم":
                data["muted"].setdefault(sid(message.chat.id), [])
                if sid(u.id) not in data["muted"][sid(message.chat.id)]: data["muted"][sid(message.chat.id)].append(sid(u.id))
                bot.restrict_chat_member(message.chat.id, u.id, can_send_messages=False); save_data(data); return bot.reply_to(message, "✅ تم الكتم")
            if text in ["الغاء الكتم","الغاء التقييد","رفع القيود"]:
                if sid(message.chat.id) in data["muted"] and sid(u.id) in data["muted"][sid(message.chat.id)]:
                    data["muted"][sid(message.chat.id)].remove(sid(u.id))
                bot.restrict_chat_member(message.chat.id, u.id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
                save_data(data); return bot.reply_to(message, "✅ تم رفع القيود")
            if text == "تقييد":
                bot.restrict_chat_member(message.chat.id, u.id, can_send_messages=False); return bot.reply_to(message, "✅ تم تقييده")
            if text == "انذار":
                cid, uid = sid(message.chat.id), sid(u.id)
                data["warns"].setdefault(cid, {})
                data["warns"][cid][uid] = data["warns"][cid].get(uid, 0) + 1
                warns_count = data["warns"][cid][uid]
                if warns_count >= 3:
                    data["warns"][cid][uid] = 0
                    data["muted"].setdefault(cid, [])
                    if uid not in data["muted"][cid]:
                        data["muted"][cid].append(uid)
                    save_data(data)
                    bot.restrict_chat_member(message.chat.id, u.id, until_date=now_time()+86400, can_send_messages=False)
                    return bot.reply_to(message, "⚠️ وصل 3 إنذارات\nتم تقييده يوم")
                save_data(data)
                return bot.reply_to(message, f"⚠️ تم إنذاره\nعدد إنذاراته: {warns_count}")
            if text in ["كشف","تحكم"]:
                return bot.reply_to(message, f"👤 الاسم: {u.first_name}\n🆔 الايدي: <code>{u.id}</code>\n⭐ الرتبة: {get_rank(message.chat.id,u.id)}")
        except Exception:
            return bot.reply_to(message, "❌ تأكد البوت مشرف وعنده صلاحيات")

    if text.startswith("تقييد "):
        if not can_admin(message): return
        u = target_user(message)
        if not u: return
        val = text.replace("تقييد ","",1).strip()
        secs = {"5":300,"10":600,"30":1800,"60":3600,"ساعة":3600,"يوم":86400,"اسبوع":604800,"أسبوع":604800}.get(val, 600)
        try:
            bot.restrict_chat_member(message.chat.id, u.id, until_date=now_time()+secs, can_send_messages=False)
            return bot.reply_to(message, "✅ تم التقييد")
        except: return bot.reply_to(message, "❌ تأكد البوت مشرف")

    # التثبيت
    if text in ["تثبيت", "ت"]:
        if not can_admin(message): return
        if not message.reply_to_message: return bot.reply_to(message, "رد على رسالة")
        try: bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id); return bot.reply_to(message, "✅ تم التثبيت")
        except: return bot.reply_to(message, "ما اكدر اثبت")
    if text == "الغاء تثبيت":
        if not can_admin(message): return
        try: bot.unpin_chat_message(message.chat.id); return bot.reply_to(message, "✅ تم الغاء التثبيت")
        except: return bot.reply_to(message, "ما اكدر")

    # الرتب
    if text.startswith("رفع "):
        if not can_admin(message): return
        u = target_user(message)
        if not u: return
        rank = text.replace("رفع ","",1).strip()
        if rank in FUN_RANKS:
            cid = sid(message.chat.id)
            data["fun_ranks"].setdefault(cid, {})
            data["fun_ranks"][cid].setdefault(rank, [])
            if sid(u.id) not in data["fun_ranks"][cid][rank]:
                data["fun_ranks"][cid][rank].append(sid(u.id))
            save_data(data)
            return bot.reply_to(message, f"✅ تم رفعه {rank}")
        if rank not in RANK_NAMES:
            return bot.reply_to(message, "هذه الرتبة غير موجودة")
        if not can_promote_to(message, rank):
            return
        set_rank(message.chat.id, u.id, rank)
        return bot.reply_to(message, f"✅ تم رفعه {rank}")
    if text.startswith("تنزيل "):
        if not can_admin(message): return
        rank = text.replace("تنزيل ","",1).strip()
        u = target_user(message)
        if not u: return
        if rank in FUN_RANKS:
            cid = sid(message.chat.id)
            try: data["fun_ranks"][cid][rank].remove(sid(u.id))
            except: pass
            save_data(data)
            return bot.reply_to(message, f"✅ تم تنزيله من {rank}")
        del_rank(message.chat.id, u.id)
        return bot.reply_to(message, "✅ تم تنزيل رتبته")
    if text in ["تنزيل الكل","تنزيل جميع الرتب"]:
        if not can_admin(message): return
        if message.reply_to_message:
            del_rank(message.chat.id, message.reply_to_message.from_user.id)
            return bot.reply_to(message, "✅ تم تنزيل كل رتبته")
        data["ranks"][sid(message.chat.id)] = {}; save_data(data)
        return bot.reply_to(message, "✅ تم تنزيل جميع الرتب")

    lists_map = {
        "المميزين":"مميز","الادمنيه":"ادمن","الأدمنيه":"ادمن","المشرفين":"مشرف","المدراء":"مدير",
        "المنشئين":"منشئ","المنشئين الاساسيين":"منشئ اساسي","المالكين":"مالك","المالكين الاساسيين":"مالك اساسي",
        "المطورين":"مطور","المطورين الثانويين":"مطور ثانوي","المطورين الاساسيين":"مطور اساسي"
    }
    if text in lists_map:
        return bot.reply_to(message, list_rank(message.chat.id, lists_map[text]))
    if text.startswith("مسح "):
        name = text.replace("مسح ","",1).strip()
        clear_map = {"المميزين":"مميز","الادمنيه":"ادمن","المشرفين":"مشرف","المدراء":"مدير","المنشئين":"منشئ","المنشئين الاساسيين":"منشئ اساسي","المالكين":"مالك"}
        if name in clear_map:
            if not can_admin(message): return
            clear_rank(message.chat.id, clear_map[name])
            return bot.reply_to(message, "✅ تم المسح")

    # قوائم منع ومكتومين
    if text in ["المكتومين","المقيدين","قائمه المنع","قائمة المنع"]:
        cid = sid(message.chat.id)
        if text == "المكتومين":
            arr = data["muted"].get(cid, [])
            return bot.reply_to(message, "\n".join([display_name(x) for x in arr]) if arr else "ماكو مكتومين")
        if text == "المقيدين":
            arr = data["restricted"].get(cid, [])
            return bot.reply_to(message, "\n".join([display_name(x) for x in arr]) if arr else "ماكو مقيدين")
        arr = data["blocked"].get(cid, [])
        return bot.reply_to(message, "\n".join(arr) if arr else "ماكو منع")
    if text.startswith("منع "):
        if not can_admin(message): return
        word = text.replace("منع ","",1).strip()
        data["blocked"].setdefault(sid(message.chat.id), [])
        if word not in data["blocked"][sid(message.chat.id)]: data["blocked"][sid(message.chat.id)].append(word)
        save_data(data); return bot.reply_to(message, "✅ تم منع الكلمة")
    if text.startswith("الغاء منع "):
        if not can_admin(message): return
        word = text.replace("الغاء منع ","",1).strip()
        try: data["blocked"][sid(message.chat.id)].remove(word)
        except: pass
        save_data(data); return bot.reply_to(message, "✅ تم الغاء المنع")

    # الردود
    if text in ["اضف رد","اضافة رد"]:
        if not can_admin(message): return
        waiting_reply[message.from_user.id] = {"step":"add_word"}
        return bot.reply_to(message, "اكتب الكلمة:")
    if text == "مسح رد":
        if not can_admin(message): return
        waiting_reply[message.from_user.id] = {"step":"del_word"}
        return bot.reply_to(message, "اكتب الكلمة:")
    if text == "الردود":
        return bot.reply_to(message, "📜 الردود:\n" + ("\n".join(data["replies"].keys()) if data["replies"] else "ماكو ردود"))
    if text == "مسح الردود":
        if not can_admin(message): return
        data["replies"] = {}; save_data(data); return bot.reply_to(message, "✅ تم مسح الردود")


    if text == "تاك للمشرفين":
        return tag_by_kind(message, "admins")
    if text == "تاك للاعضاء":
        return tag_by_kind(message, "members")
    if text in ["تاك للكل", "تاك عام", "all", "@all"]:
        return tag_by_kind(message, "all")

    # المجموعة
    if text in ["الرابط", "ر"]:
        try:
            link = bot.export_chat_invite_link(message.chat.id)
            data["links"][sid(message.chat.id)] = link; save_data(data)
            return bot.reply_to(message, link)
        except: return bot.reply_to(message, "ما اكدر اجيب الرابط")
    if text == "القوانين":
        return bot.reply_to(message, data["laws"].get(sid(message.chat.id), "ماكو قوانين"))
    if text in ["ضع رابط","انشاء رابط"]:
        if not can_admin(message): return
        try:
            link = bot.export_chat_invite_link(message.chat.id)
            data["links"][sid(message.chat.id)] = link; save_data(data)
            return bot.reply_to(message, "✅ تم وضع الرابط\n" + link)
        except: return bot.reply_to(message, "ما اكدر انشئ رابط")
    if text.startswith("ضع قوانين") or text == "ضع القوانين":
        if not can_admin(message): return
        val = text.replace("ضع قوانين","",1).replace("ضع القوانين","",1).strip()
        if val:
            data["laws"][sid(message.chat.id)] = val; save_data(data); return bot.reply_to(message, "✅ تم وضع القوانين")
        waiting_reply[message.from_user.id] = {"step":"set_laws"}; return bot.reply_to(message, "ارسل القوانين")
    if text.startswith("ضع ترحيب") or text == "ضع الترحيب":
        if not can_admin(message): return
        val = text.replace("ضع ترحيب","",1).replace("ضع الترحيب","",1).strip()
        if val:
            data["welcome_text"][sid(message.chat.id)] = val; save_data(data); return bot.reply_to(message, "✅ تم وضع الترحيب")
        waiting_reply[message.from_user.id] = {"step":"set_welcome"}; return bot.reply_to(message, "ارسل الترحيب")
    if text.startswith("ضع اسم ") or text.startswith("اسم "):
        if not can_admin(message): return
        name = text.split(maxsplit=2)[-1]
        try: bot.set_chat_title(message.chat.id, name); return bot.reply_to(message, "✅ تم تغيير اسم المجموعة")
        except: return bot.reply_to(message, "ما اكدر اغير الاسم")
    if text == "الاعدادات" or text == "الإعدادات":
        st = chat_settings(message.chat.id); locks = get_locks(message.chat.id)
        return bot.reply_to(message, f"⚙️ الإعدادات\nالترحيب: {st.get('welcome')}\nالردود: {st.get('replies')}\nالألعاب: {st.get('games')}\nالبنك: {st.get('bank')}\n\n🔒 الأقفال المفعلة:\n" + "\n".join([k for k,v in locks.items() if v]) or "ماكو")
    if text == "الحمايه" or text == "الحماية":
        locks = get_locks(message.chat.id)
        active = [k for k,v in locks.items() if v]
        return bot.reply_to(message, "🔒 الحماية المفعلة:\n" + ("\n".join(active) if active else "ماكو"))

    # تاك
    if text in ["تاك","تاك للكل","تاك عام","all"] or "@all" in text:
        if not can_admin(message): return
        if not chat_settings(message.chat.id).get("tagall", True): return
        members = list(data["messages"].get(sid(message.chat.id), {}).keys())[:80]
        if not members: return bot.reply_to(message, "ما عندي أعضاء مخزنين بعد")
        chunks, cur = [], ""
        for uid in members:
            cur += f"<a href='tg://user?id={uid}'>.</a> "
            if len(cur) > 3500:
                chunks.append(cur); cur = ""
        if cur: chunks.append(cur)
        for ch in chunks: bot.send_message(message.chat.id, ch)
        return

    # تحشيش
    if text in FUN_RANKS.values() or text in ["الملوك","الملكات","الثولان","الجلاب","المطايه","الصخول","البقرات","الزواحف","اللوكيه","الاغبياء","العسل","الكيك","الطليان","قائمه كلبي","قائمة كلبي"]:
        cid = sid(message.chat.id)
        out = []
        for rank, listname in FUN_RANKS.items():
            if listname == text:
                arr = data["fun_ranks"].get(cid, {}).get(rank, [])
                out += [display_name(x) for x in arr]
        return bot.reply_to(message, "\n".join(out) if out else "ماكو")
    if text.startswith("نسبه ") or text in ["نسبه الحب","نسبه الكره","نسبه الرجوله","نسبه الانوثه","نسبه الذكاء","نسبه الغباء"]:
        return bot.reply_to(message, f"{text} عندك: {random.randint(1,100)}%")
    if text in ["شنو رايك بهذا","شنو رايك بهاي"]:
        return bot.reply_to(message, random.choice(["حلو/ة 😍","مو خوش 😅","أسطورة 🔥","عادي"]))
    if text in ["انطي هديه","بوسه","بوسني","صيحه","رزله"]:
        return bot.reply_to(message, random.choice(["🎁 تفضل هدية","😘 بوسة","اااااااااااااااااااااا","😂 رزلة محترمة"]))

    # بنك
    if text in ["انشاء حساب بنكي","انشاء"]:
        if not chat_settings(message.chat.id).get("bank", True): return bot.reply_to(message, "البنك معطل")
        return bot.reply_to(message, "✅ تم إنشاء حسابك البنكي ورصيدك 1000$" if create_bank(message.from_user.id) else "عندك حساب بنكي مسبقاً")
    if text == "مسح حساب بنكي":
        data["bank"].pop(sid(message.from_user.id), None); save_data(data)
        return bot.reply_to(message, "✅ تم مسح حسابك البنكي")
    if text in ["حسابي","فلوسي"]:
        acc = bank_user(message.from_user.id)
        if not acc: return bot.reply_to(message, "ما عندك حساب. اكتب: انشاء حساب بنكي")
        return bot.reply_to(message, f"🏦 حسابك: <code>{acc['account']}</code>\n💰 فلوسك: {acc['money']}$")
    if text in ["حسابه","فلوسه"]:
        if not message.reply_to_message: return bot.reply_to(message, "رد على شخص")
        acc = bank_user(message.reply_to_message.from_user.id)
        return bot.reply_to(message, f"💰 فلوسه: {acc['money']}$" if acc else "ما عنده حساب")
    if text == "راتب":
        acc = bank_user(message.from_user.id)
        if not acc: return bot.reply_to(message, "سوّي حساب بنكي أولاً")
        ok,left = cd_ok(message.from_user.id,"salary",1200)
        if not ok: return bot.reply_to(message, f"انتظر {left} ثانية")
        amount = random.randint(500,1500); acc["money"] += amount; save_data(data)
        return bot.reply_to(message, f"💵 راتبك: {amount}$")
    if text == "بخشيش":
        acc = bank_user(message.from_user.id)
        if not acc: return bot.reply_to(message, "سوّي حساب بنكي أولاً")
        ok,left = cd_ok(message.from_user.id,"tip",600)
        if not ok: return bot.reply_to(message, f"انتظر {left} ثانية")
        amount = random.randint(100,600); acc["money"] += amount; save_data(data)
        return bot.reply_to(message, f"🎁 بخشيش: {amount}$")
    if text in ["سرقه","سرقة","زرف"]:
        acc = bank_user(message.from_user.id)
        if not acc: return bot.reply_to(message, "سوّي حساب بنكي أولاً")
        if not message.reply_to_message: return bot.reply_to(message, "رد على شخص")
        victim = bank_user(message.reply_to_message.from_user.id)
        if not victim: return bot.reply_to(message, "الشخص ما عنده حساب")
        ok,left = cd_ok(message.from_user.id,"rob",600)
        if not ok: return bot.reply_to(message, f"انتظر {left} ثانية")
        amount = min(victim["money"], random.randint(50,500))
        victim["money"] -= amount; acc["money"] += amount
        data["robbers"][sid(message.from_user.id)] = data["robbers"].get(sid(message.from_user.id),0)+1
        save_data(data); return bot.reply_to(message, f"🦹 سرقت {amount}$")
    if text.startswith("تحويل "):
        acc = bank_user(message.from_user.id); amount = parse_amount(text)
        if not acc or not amount: return bot.reply_to(message, "اكتب: تحويل 100 بالرد")
        if not message.reply_to_message: return bot.reply_to(message, "رد على الشخص")
        other = bank_user(message.reply_to_message.from_user.id)
        if not other: return bot.reply_to(message, "الشخص ما عنده حساب")
        if acc["money"] < amount: return bot.reply_to(message, "فلوسك ما تكفي")
        acc["money"] -= amount; other["money"] += amount; save_data(data)
        return bot.reply_to(message, f"✅ تم تحويل {amount}$")
    if text.startswith("استثمار ") or text.startswith("حظ ") or text.startswith("مضاربه "):
        acc = bank_user(message.from_user.id); amount = parse_amount(text)
        if not acc or not amount: return bot.reply_to(message, "اكتب مبلغ صحيح")
        if acc["money"] < amount: return bot.reply_to(message, "فلوسك ما تكفي")
        if text.startswith("استثمار "):
            profit = int(amount * random.randint(1, 20) / 100); acc["money"] += profit; msg = f"📈 ربحت {profit}$"
        elif text.startswith("حظ "):
            if random.choice([True,False]): acc["money"] += amount; msg = f"🎲 فزت {amount}$"
            else: acc["money"] -= amount; msg = f"🎲 خسرت {amount}$"
        else:
            percent = random.randint(-90,90); change = int(amount*percent/100); acc["money"] += change; msg = f"📊 النسبة: {percent}%\nالنتيجة: {change}$"
        save_data(data); return bot.reply_to(message, msg)
    if text in ["توب الفلوس","توب الحراميه","توب الحرامية"]:
        if text == "توب الفلوس":
            items = sorted(data["bank"].items(), key=lambda x:x[1].get("money",0), reverse=True)[:10]
            return bot.reply_to(message, "\n".join([f"{i+1}. {display_name(uid)} — {info['money']}$" for i,(uid,info) in enumerate(items)]) or "ماكو")
        items = sorted(data["robbers"].items(), key=lambda x:x[1], reverse=True)[:10]
        return bot.reply_to(message, "\n".join([f"{i+1}. {display_name(uid)} — {c}" for i,(uid,c) in enumerate(items)]) or "ماكو")
    if text == "تصفير الفلوس":
        if not can_admin(message): return
        if message.reply_to_message:
            if sid(message.reply_to_message.from_user.id) in data["bank"]:
                data["bank"][sid(message.reply_to_message.from_user.id)]["money"] = 0; save_data(data)
                return bot.reply_to(message, "✅ تم تصفير فلوسه")
    if text.startswith("اضف فلوس "):
        if message.from_user.id != OWNER_ID: return
        amount = parse_amount(text); u = target_user(message)
        if not u or not amount: return
        create_bank(u.id); data["bank"][sid(u.id)]["money"] += amount; save_data(data)
        return bot.reply_to(message, f"✅ تم اضافة {amount}$")
    if text.startswith("زواج ") and message.reply_to_message:
        amount = parse_amount(text); acc = bank_user(message.from_user.id); other = bank_user(message.reply_to_message.from_user.id)
        if not acc or not other or not amount: return bot.reply_to(message, "لازم الاثنين عدهم حساب ومبلغ")
        if acc["money"] < amount: return bot.reply_to(message, "فلوسك ما تكفي")
        acc["money"] -= amount
        data["marriages"][sid(message.from_user.id)] = sid(message.reply_to_message.from_user.id)
        save_data(data); return bot.reply_to(message, "💍 تم الزواج")
    if text in ["زواجي","زوجتي","زوجي"]:
        partner = data["marriages"].get(sid(message.from_user.id))
        return bot.reply_to(message, f"💍 شريكك: {display_name(partner)}" if partner else "انت أعزب")
    if text in ["طالق","خلع","طلاق"]:
        data["marriages"].pop(sid(message.from_user.id), None); save_data(data)
        return bot.reply_to(message, "💔 تم الطلاق")
    if text == "توب المتزوجين":
        return bot.reply_to(message, f"عدد المتزوجين: {len(data['marriages'])}")
    if text in ["ميدالياتي","متجر البنك","قائمه اكشطها","اكشط","مسح لعبه البنك","صنع اكشطها"]:
        return bot.reply_to(message, "✅ هذا الأمر مضاف بنظام بسيط، يتم تطوير تفاصيله لاحقاً.")

    # ألعاب
    if text in GAME_QUESTIONS or text in ["رياضيات","احسب"]:
        return make_quiz(message, text)
    if text in ["روليت","الروليت"]:
        members = list(data["messages"].get(sid(message.chat.id), {}).keys())
        if len(members) < 2: return bot.reply_to(message, "لازم يتفاعلون أعضاء أكثر")
        return bot.reply_to(message, f"🎯 الروليت اختارت: {display_name(random.choice(members))}")
    if text in ["الحظ","حظي"]:
        return bot.reply_to(message, random.choice(["ربحت 🔥","خسرت 😅","حظك متوسط"]))
    if text == "بيع نقاطي" or text.startswith("بيع نقاطي "):
        pts = data["points"].get(sid(message.from_user.id),0)
        amount = parse_amount(text) or pts
        if pts < amount: return bot.reply_to(message, "نقاطك ما تكفي")
        create_bank(message.from_user.id)
        data["points"][sid(message.from_user.id)] -= amount
        data["bank"][sid(message.from_user.id)]["money"] += amount * 50
        save_data(data)
        return bot.reply_to(message, f"✅ بعت {amount} نقطة مقابل {amount*50}$")

    # تسلية وأعضاء
    if text in ["افلام","فلم","مسلسل","فلم كامل"]:
        return bot.reply_to(message, "🎬 مقترحات:\n" + "\n".join(random.sample(MOVIES, min(6,len(MOVIES)))))
    if text in ["ز","زوجني","زواج"]:
        if message.reply_to_message:
            data["marriages"][sid(message.from_user.id)] = sid(message.reply_to_message.from_user.id); save_data(data)
            return bot.reply_to(message, "💍 تم الزواج")
        return bot.reply_to(message, f"💍 تم زواجك من {random.choice(NAMES)}")
    if text == "ثنائي اليوم":
        members = list(data["messages"].get(sid(message.chat.id), {}).keys())
        if len(members) >= 2:
            a,b = random.sample(members,2)
            return bot.reply_to(message, f"💞 ثنائي اليوم:\n{display_name(a)} + {display_name(b)}")
        return bot.reply_to(message, "ماكو أعضاء كفاية")
    if text == "منشن" or text == "نداء":
        members = list(data["messages"].get(sid(message.chat.id), {}).keys())
        if members:
            uid = random.choice(members)
            return bot.reply_to(message, f"<a href='tg://user?id={uid}'>تعال هنا</a>")
    if text == "نزلني":
        del_rank(message.chat.id, message.from_user.id)
        return bot.reply_to(message, "✅ نزلتك")
    if text.startswith("كول "):
        return bot.send_message(message.chat.id, text.replace("كول ","",1))
    if text.startswith("زخرفه") or text.startswith("زخرفة"):
        name = text.replace("زخرفه","",1).replace("زخرفة","",1).strip() or message.from_user.first_name
        return bot.reply_to(message, f"𓆩 {name} 𓆪\n『{name}』\n◥ {name} ◤")
    if text in ["الوقت","الساعه","الساعة","التاريخ"]:
        now = datetime.datetime.now()
        return bot.reply_to(message, now.strftime("🕒 %H:%M\n📅 %Y-%m-%d"))
    if text.startswith("احسب "):
        date = text.replace("احسب ","",1).strip()
        try:
            y,m,d = map(int, re.split(r"[-/]", date))
            age = datetime.date.today().year - y
            return bot.reply_to(message, f"عمرك تقريباً: {age} سنة")
        except: return bot.reply_to(message, "اكتب: احسب 2008-1-7")
    if text.startswith("معنى اسم "):
        name = text.replace("معنى اسم ","",1).strip()
        return bot.reply_to(message, f"معنى اسم {name}: اسم جميل ويدل على الخير 🌷")
    if text.startswith("الطقس "):
        city = text.replace("الطقس ","",1).strip()
        return bot.reply_to(message, f"طقس {city}: ما اكدر اجيب مباشر بدون API طقس، بس الأمر شغال كرد بسيط.")
    if text in ["غنيلي","اغنيه","أغنية","ريمكس","شعر","قصيدة","حسينية","راب","ميمز","ثيم","تنظيف الصوت"]:
        replies = {
            "غنيلي":"🎵 يا ليل يا عين 🎶", "اغنيه":"🎧 اكتب: يوت اسم الاغنية", "أغنية":"🎧 اكتب: يوت اسم الاغنية",
            "شعر":"أحبك لو تكون بعيد، وأذكرك لو طال الغياب 🌷", "قصيدة":"قصيدة جميلة: سلامٌ على الطيبين",
            "حسينية":"يا حسين ❤️", "راب":"Yo Yo 🔥", "ميمز":"😂😂😂", "ثيم":"ثيمك اليوم: أسود ملكي 🖤",
            "تنظيف الصوت":"🔊 شغل صوت عالي 10 ثواني ونظف السماعة"
        }
        return bot.reply_to(message, replies.get(text, "🎶"))

    if text.startswith("بحث يوتيوب "):
        q = text.replace("بحث يوتيوب ","",1).strip()
        return bot.reply_to(message, f"https://www.youtube.com/results?search_query={q.replace(' ','+')}")

    # يوتيوب / ميوزك — محفوظ
    if text.startswith("يوت "):
        query = text.replace("يوت ", "").strip()
        if not query:
            return bot.reply_to(message, "اكتب اسم الأغنية")
        wait = bot.reply_to(message, "🔎 جاري البحث...")
        try:
            search_res = requests.get("https://www.youtube.com/results", params={"search_query": query + " اغنية audio official"}, timeout=20)
            ids = re.findall(r"watch\?v=(\S{11})", search_res.text)
            if not ids:
                return bot.reply_to(message, "ما حصلت نتيجة")
            video_url = f"https://www.youtube.com/watch?v={ids[0]}"
            headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "yt-search-and-download-mp3.p.rapidapi.com"}
            api = requests.get("https://yt-search-and-download-mp3.p.rapidapi.com/mp3", headers=headers, params={"url": video_url}, timeout=60).json()
            print("API RESPONSE:", api)
            audio_url = (api.get("link") or api.get("url") or api.get("audio") or api.get("download") or api.get("mp3") or api.get("downloadUrl") or api.get("download_url") or api.get("audioUrl") or api.get("result"))
            title = api.get("title") or query
            try: bot.delete_message(message.chat.id, wait.message_id)
            except: pass
            if not audio_url:
                return bot.reply_to(message, "ما حصلت رابط الصوت")
            kb = {"inline_keyboard": [[red_btn("SOURCE FADI", url=f"https://t.me/{DEV_USERNAME}")]]}
            return bot.send_audio(message.chat.id, audio_url, title=title, performer="Aurelius", caption=f"🎧 {title}", reply_to_message_id=message.message_id, reply_markup=kb)
        except Exception as e:
            print("MUSIC ERROR:", e)
            return bot.reply_to(message, "صار خطأ أثناء جلب الأغنية")

    # منع كلمات
    if message.chat.type != "private":
        for word in data["blocked"].get(sid(message.chat.id), []):
            if word and word in text and not is_admin(message.chat.id, message.from_user.id):
                try: bot.delete_message(message.chat.id, message.message_id)
                except: pass
                return

print("Aurelius bot is running...")
bot.infinity_polling(skip_pending=True)
