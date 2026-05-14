from telebot import TeleBot from telebot.types import Message

from app.config import BOT_TOKEN, START_PHOTO from app.buttons import start_buttons, raw_send_photo from app.help import help_menu, get_help_text from app.music import send_music from app.weather import get_weather from app.ai import ask_ai from app.whisper import create_whisper, handle_whisper from app.id import get_id_text

from app.games import ( GAME_NAMES, make_game, handle_game_answer, start_fast, check_fast, random_cut, random_would )

from app.entertainment import ( random_theme, random_poem, random_anime, random_movie, random_series, marry_user, call_user )

from app.moderation import ( mute, unmute, ban, unban, kick, restrict, lift_restrictions, warn, warnings_count, clear_warnings, clear_muted, clear_restricted, clear_banned )

bot = TeleBot(BOT_TOKEN, parse_mode="HTML")

members_cache = {}

def add_member(chat_id, user_id): cid = str(chat_id)

if cid not in members_cache:
    members_cache[cid] = set()

members_cache[cid].add(user_id)

def get_members(chat_id): return list(members_cache.get(str(chat_id), []))

@bot.message_handler(commands=["start"]) def start(message: Message):

add_member(message.chat.id, message.from_user.id)

raw_send_photo(
    message.chat.id,
    START_PHOTO,
    "هلا بك في بوت فادي",
    start_buttons()
)

@bot.callback_query_handler(func=lambda call: True) def callbacks(call):

if call.data.startswith("game:"):
    return handle_game_answer(bot, call)

if call.data.startswith("whisper_"):
    return handle_whisper(bot, call)

if call.data == "help" or call.data.startswith("help") or call.data == "bank":

    return bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=get_help_text(call.data),
        reply_markup=help_menu()
    )

@bot.message_handler(func=lambda m: True) def handler(message: Message):

add_member(message.chat.id, message.from_user.id)

if not message.text:
    return

text = message.text.strip()

if text in ["الاوامر", "الأوامر", "اوامر"]:

    return raw_send_photo(
        message.chat.id,
        START_PHOTO,
        "قائمة الاوامر",
        help_menu()
    )

if text in ["ايدي", "ا"]:

    return bot.reply_to(
        message,
        get_id_text(message.from_user),
        parse_mode="HTML"
    )

if text.startswith("يوت "):

    return send_music(
        bot,
        message,
        text.replace("يوت ", "", 1)
    )

if text.startswith("طقس "):

    return bot.reply_to(
        message,
        get_weather(
            text.replace("طقس ", "", 1)
        )
    )

if text.startswith("زنجي "):

    return bot.reply_to(
        message,
        ask_ai(
            text.replace("زنجي ", "", 1)
        )
    )

if (
    text.startswith("همسة ")
    or text.startswith("همسه ")
    or text.startswith("هم ")
):

    return create_whisper(bot, message)

if text in GAME_NAMES:

    q, kb = make_game(text)

    return bot.send_message(
        message.chat.id,
        q,
        reply_markup=kb
    )

if text == "الاسرع":

    word = start_fast(message.chat.id)

    return bot.send_message(
        message.chat.id,
        f"اول واحد يكتب:\n{word}"
    )

if check_fast(message.chat.id, text):
    return bot.reply_to(message, "فزت")

if text in ["كت", "كت تويت", "صراحة"]:
    return bot.reply_to(message, random_cut())

if text == "لو خيروك":
    return bot.reply_to(message, random_would())

if text == "ثيم":
    return bot.reply_to(message, random_theme())

if text == "شعر":
    return bot.reply_to(message, random_poem())

if text == "انمي":
    return bot.reply_to(message, random_anime())

if text in ["فلم", "افلام"]:
    return bot.reply_to(message, random_movie())

if text == "مسلسل":
    return bot.reply_to(message, random_series())

if text in ["زوجني", "ز"]:

    partner = marry_user(
        message.chat.id,
        message.from_user.id,
        get_members(message.chat.id)
    )

    if not partner:
        return bot.reply_to(message, "ماكو اعضاء كفاية")

    return bot.reply_to(
        message,
        f"تم زواجك من:\n{partner}"
    )

if text in ["نداء", "نن"]:

    user = call_user(
        message.chat.id,
        get_members(message.chat.id)
    )

    if not user:
        return bot.reply_to(message, "ماكو اعضاء")

    return bot.reply_to(
        message,
        f"نداء للعضو:\n{user}"
    )

if text == "كتم":
    return mute(bot, message)

if text == "الغاء الكتم":
    return unmute(bot, message)

if text == "حظر":
    return ban(bot, message)

if text == "الغاء حظر":
    return unban(bot, message)

if text == "طرد":
    return kick(bot, message)

if text == "تقييد":
    return restrict(bot, message)

if text in ["رفع القيود", "رف"]:
    return lift_restrictions(bot, message)

if text == "مسح المكتومين":
    return clear_muted(bot, message)

if text == "مسح المقيدين":
    return clear_restricted(bot, message)

if text == "مسح المحظورين":
    return clear_banned(bot, message)

if text == "انذار":
    return warn(bot, message)

if text == "انذاراته":
    return warnings_count(bot, message)

if text == "مسح انذاراته":
    return clear_warnings(bot, message)

print("BOT READY") bot.infinity_polling(skip_pending=True)
