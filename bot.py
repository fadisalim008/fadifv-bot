
import os, json, re, random, time, datetime
import telebot, requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# حط التوكنات من Railway Variables أفضل:
# BOT_TOKEN = توكن البوت
# RAPID_API_KEY = مفتاح RapidAPI
TOKEN = os.getenv("BOT_TOKEN", "8516176029:AAFEAuEU93dkwAdjKva8M6M_SQjHjHxn4Uo")
RAPID_API_KEY = os.getenv("RAPID_API_KEY", "f590d18da9mshd55fe58cee3c77cp141b8ajsn63f68639be0f")

OWNER_ID = int(os.getenv("OWNER_ID", "8065884629"))
BOT_USERNAME = os.getenv("BOT_USERNAME", "fadifvambot")
DEV_USERNAME = os.getenv("DEV_USERNAME", "fvamv")
FORCE_CHANNEL = os.getenv("FORCE_CHANNEL", "@fadifva")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
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
    "min_members": 0, "bot_name": "فادي", "auto_backup": False
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
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("الحماية", callback_data="help_locks"), InlineKeyboardButton("الأدمنية", callback_data="help_admin"))
    kb.add(InlineKeyboardButton("المدراء", callback_data="help_manager"), InlineKeyboardButton("المنشئ", callback_data="help_creator"))
    kb.add(InlineKeyboardButton("المالك", callback_data="help_owner"), InlineKeyboardButton("الأعضاء", callback_data="help_members"))
    kb.add(InlineKeyboardButton("البنك", callback_data="help_bank"), InlineKeyboardButton("الألعاب", callback_data="help_games"))
    kb.add(InlineKeyboardButton("التسلية", callback_data="help_entertainment"), InlineKeyboardButton("التحشيش", callback_data="help_fun"))
    kb.add(InlineKeyboardButton("المطور", callback_data="help_dev"), InlineKeyboardButton("الميوزك", callback_data="help_music"))
    return kb

def owner_panel():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("صانع الردود", callback_data="owner_add_reply"), InlineKeyboardButton("الردود", callback_data="owner_replies"))
    kb.add(InlineKeyboardButton("المستخدمين", callback_data="owner_users"), InlineKeyboardButton("الكروبات", callback_data="owner_groups"))
    kb.add(InlineKeyboardButton("إشعار الدخول", callback_data="owner_notify"), InlineKeyboardButton("رجوع", callback_data="commands"))
    return kb

def start_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("👨‍💻 المطور", url=f"https://t.me/{DEV_USERNAME}"))
    kb.add(InlineKeyboardButton("➕ اضفني للكروب", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"))
    kb.add(InlineKeyboardButton("💰 شراء بوت مشابه", url=f"https://t.me/{DEV_USERNAME}"))
    kb.add(InlineKeyboardButton("📚 الأوامر", callback_data="commands"))
    return kb

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

def send_commands(message, section=None):
    if section and section in COMMAND_TEXTS:
        return bot.reply_to(message, COMMAND_TEXTS[section])
    return bot.reply_to(message, "📚 اختر قسم الأوامر:", reply_markup=main_menu())

@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.type != "private": return
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
    sections = {"help_admin":"admin","help_locks":"locks","help_manager":"manager","help_creator":"creator","help_owner":"owner","help_members":"members","help_bank":"bank","help_games":"games","help_entertainment":"entertainment","help_fun":"fun","help_dev":"dev"}
    if call.data == "help_music":
        return bot.edit_message_text("<b>❨ أوامر الميوزك ❩</b>\n\n• يوت اسم الأغنية\n• بحث يوتيوب اسم الفيديو", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    if call.data in sections:
        return bot.edit_message_text(COMMAND_TEXTS[sections[call.data]], call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    if call.data.startswith("owner_"):
        if call.from_user.id != OWNER_ID:
            return bot.answer_callback_query(call.id, "للمطور فقط", show_alert=True)
        if call.data == "owner_add_reply":
            waiting_reply[call.from_user.id] = {"step":"add_word"}
            return bot.send_message(call.message.chat.id, "اكتب الكلمة:")
        if call.data == "owner_replies":
            return bot.send_message(call.message.chat.id, "📜 الردود:\n" + ("\n".join(data["replies"].keys()) if data["replies"] else "ماكو"))
        if call.data == "owner_users":
            return bot.send_message(call.message.chat.id, f"👥 عدد المستخدمين: {len(data['users'])}")
        if call.data == "owner_groups":
            return bot.send_message(call.message.chat.id, f"📊 عدد الكروبات: {len(data['groups'])}")
        if call.data == "owner_notify":
            data["notify"] = not data.get("notify", True); save_data(data)
            return bot.send_message(call.message.chat.id, "🔔 إشعار الدخول: " + ("مفعل" if data["notify"] else "متوقف"))

@bot.message_handler(content_types=["new_chat_members"])
def welcome(message):
    register_user(message)
    if message.chat.type in ["group","supergroup"]:
        locks = get_locks(message.chat.id)
        for u in message.new_chat_members:
            if u.is_bot and locks.get("bots") and not is_admin(message.chat.id, message.from_user.id):
                try: bot.kick_chat_member(message.chat.id, u.id)
                except: pass
                continue
            data["join_info"][sid(u.id)] = {"chat": message.chat.title or "", "by": message.from_user.first_name if message.from_user else "رابط", "time": now_time()}
            save_data(data)
            if chat_settings(message.chat.id).get("welcome", True):
                txt = data["welcome_text"].get(sid(message.chat.id), f"هلا {u.first_name} 🌷\nنورت الكروب")
                bot.send_message(message.chat.id, txt.replace("{name}", u.first_name or ""))

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

    if message.chat.type != "private" and not check_sub(message): return

    text = message.text or message.caption or ""

    # فلتر الحمايات قبل الأوامر للأعضاء فقط
    if message.chat.type != "private" and message.from_user and not is_admin(message.chat.id, message.from_user.id):
        violation = detect_lock_violation(message)
        if violation:
            punish_locked(message, violation)
            return

    if not text: return
    text = text.strip()

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
        if text == "صلاحياتي": return bot.reply_to(message, "صلاحياتك: " + ("اداري" if is_admin(message.chat.id, message.from_user.id) else "عضو"))

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
                data["warns"][cid][uid] = data["warns"][cid].get(uid, 0) + 1; save_data(data)
                return bot.reply_to(message, f"⚠️ تم إنذاره\nعدد إنذاراته: {data['warns'][cid][uid]}")
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
    if text == "تثبيت":
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
    if text in ["المكتومين","قائمه المنع","قائمة المنع"]:
        cid = sid(message.chat.id)
        if text == "المكتومين":
            arr = data["muted"].get(cid, [])
            return bot.reply_to(message, "\n".join([display_name(x) for x in arr]) if arr else "ماكو مكتومين")
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

    # المجموعة
    if text == "الرابط":
        try:
            link = bot.export_chat_invite_link(message.chat.id)
            data["links"][sid(message.chat.id)] = link; save_data(data)
            return bot.reply_to(message, link)
        except: return bot.reply_to(message, "ما اكدر اجيب الرابط")
    if text == "القوانين":
        return bot.reply_to(message, data["laws"].get(sid(message.chat.id), "ماكو قوانين"))
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
            search_res = requests.get("https://www.youtube.com/results", params={"search_query": query}, timeout=20)
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
            return bot.send_audio(message.chat.id, audio_url, title=title, performer="Aurelius", caption=f"🎧 {title}", reply_to_message_id=message.message_id)
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
