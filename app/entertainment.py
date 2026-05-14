import random

THEMES = [
    "https://t.me/addtheme/ClassicBlue",
    "https://t.me/addtheme/DarkSpace",
    "https://t.me/addtheme/OceanBlue",
    "https://t.me/addtheme/BlackRed",
    "https://t.me/addtheme/PurpleNight",
    "https://t.me/addtheme/GreenLife",
    "https://t.me/addtheme/GoldenDark",
    "https://t.me/addtheme/NeonBlue",
    "https://t.me/addtheme/DeepBlack",
    "https://t.me/addtheme/CoffeeDark",
    "https://t.me/addtheme/SkyLight",
    "https://t.me/addtheme/GrayMinimal",
    "https://t.me/addtheme/RedMoon",
    "https://t.me/addtheme/AnimePink",
    "https://t.me/addtheme/IraqDark",
    "https://t.me/addtheme/NightWolf",
    "https://t.me/addtheme/BlueFire",
    "https://t.me/addtheme/WhiteClean",
    "https://t.me/addtheme/CyberDark",
    "https://t.me/addtheme/SoftPurple",
    "https://t.me/addtheme/OrangeSun",
]

POEMS = [
    "https://www.youtube.com/results?search_query=مظفر+النواب+قصيدة",
    "https://www.youtube.com/results?search_query=احمد+مطر+قصيدة",
    "https://www.youtube.com/results?search_query=نزار+قباني+قصيدة+صوت",
    "https://www.youtube.com/results?search_query=محمود+درويش+قصيدة+صوت",
    "https://www.youtube.com/results?search_query=الجواهري+قصيدة+صوت",
]

ANIME = [
    ("Attack on Titan", "صراع البشر ضد العمالقة، أحداث قوية وغموض وحروب."),
    ("Death Note", "طالب يحصل على دفتر يقتل من يكتب اسمه، صراع ذكاء رهيب."),
    ("Naruto", "نينجا يحاول يصير الأقوى ويحمي قريته."),
    ("One Piece", "قراصنة يبحثون عن الكنز الأعظم ومغامرات طويلة."),
    ("Demon Slayer", "شاب يحارب الشياطين حتى ينقذ أخته."),
    ("Jujutsu Kaisen", "لعنات وسحرة وقتالات قوية."),
    ("Tokyo Ghoul", "شاب يتحول لنصف غول ويعيش صراع داخلي."),
    ("Hunter x Hunter", "مغامرات وقتالات وذكاء عالي."),
    ("Vinland Saga", "فايكنغ وانتقام وحروب وتطور شخصية."),
    ("Monster", "طبيب يلاحق قاتل عبقري في قصة نفسية عميقة."),
]

MOVIES = [
    ("Inception", "فلم عن الأحلام داخل الأحلام وسرقة الأفكار."),
    ("Interstellar", "رحلة فضائية لإنقاذ البشرية وقصة مؤثرة."),
    ("The Dark Knight", "باتمان ضد الجوكر، جريمة وفلسفة وفوضى."),
    ("Fight Club", "فلم نفسي عن التمرد والهوية."),
    ("Se7en", "تحقيق مظلم بجرائم غريبة."),
    ("The Godfather", "مافيا وعائلة وسلطة."),
    ("Joker", "قصة تحول رجل محطم إلى الجوكر."),
    ("Parasite", "فلم كوري عن الطبقات والفقر والدهاء."),
    ("Gladiator", "محارب روماني ينتقم بكرامة."),
    ("The Matrix", "عالم وهمي وحقيقة مخفية."),
]

SERIES = [
    ("Breaking Bad", "مدرس كيمياء يدخل عالم المخدرات ويتحول لشخص خطير."),
    ("Game of Thrones", "صراع عروش وممالك وخيانة وحروب."),
    ("Vikings", "حياة الفايكنغ وغزواتهم وصراعاتهم."),
    ("Dark", "سفر عبر الزمن وغموض عائلي معقد."),
    ("Peaky Blinders", "عصابة بريطانية وصعود نفوذها."),
    ("Prison Break", "هروب ذكي من السجن وخطط معقدة."),
    ("The Last of Us", "عالم بعد الوباء ورحلة نجاة."),
    ("Sherlock", "تحقيقات ذكية وغموض."),
]

last_marriage = {}
last_call = {}

def random_theme():
    return "ثيم تليجرام عشوائي:\n" + random.choice(THEMES)

def random_poem():
    return "شعر عشوائي:\n" + random.choice(POEMS)

def random_anime():
    name, desc = random.choice(ANIME)
    return f"انمي مقترح:\n{name}\n\n{desc}"

def random_movie():
    name, desc = random.choice(MOVIES)
    return f"فلم مقترح:\n{name}\n\n{desc}"

def random_series():
    name, desc = random.choice(SERIES)
    return f"مسلسل مقترح:\n{name}\n\n{desc}"

def get_random_member(chat_id, members, avoid=None):
    if not members:
        return None

    avoid = avoid or []
    choices = [m for m in members if str(m) not in avoid]

    if not choices:
        choices = members

    return random.choice(choices)

def marry_user(chat_id, user_id, members):
    key = str(chat_id)

    avoid = last_marriage.get(key, [])
    partner = get_random_member(chat_id, members, avoid=[str(user_id)] + avoid[-5:])

    if not partner:
        return None

    last_marriage.setdefault(key, [])
    last_marriage[key].append(str(partner))
    last_marriage[key] = last_marriage[key][-10:]

    return partner

def call_user(chat_id, members):
    key = str(chat_id)

    avoid = last_call.get(key, [])
    target = get_random_member(chat_id, members, avoid=avoid[-5:])

    if not target:
        return None

    last_call.setdefault(key, [])
    last_call[key].append(str(target))
    last_call[key] = last_call[key][-10:]

    return target
