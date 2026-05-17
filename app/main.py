from telebot import TeleBot
from telebot.types import Message

from app.config import BOT_TOKEN

bot = TeleBot(BOT_TOKEN, parse_mode="HTML")


@bot.message_handler(commands=["start"])
def start(message):

    bot.reply_to(
        message,
        "هلا بك في بوت فادي"
    )


@bot.message_handler(func=lambda m: True)
def all_messages(message):

    text = message.text if message.text else ""

    # ايدي
    if text in ["ايدي", "ا"]:

        msg = f"""
<blockquote>

👑 <b>OWNER INFO</b>

🔥 Name ⇴ {message.from_user.first_name}

💎 User ⇴ @{message.from_user.username}

✨ ID ⇴ {message.from_user.id}

</blockquote>
"""

        return bot.reply_to(
            message,
            msg,
            parse_mode="HTML"
        )

    # الاوامر
    if text in ["الاوامر", "اوامر"]:

        return bot.reply_to(
            message,
            """
1 - القفل والفتح
2 - الادمنية
3 - المسح
4 - الحظر والطرد
5 - الترفيه
6 - الالعاب
"""
        )

    # همسة
    if text.startswith("همسة") or text.startswith("همسه"):

        return bot.reply_to(
            message,
            "تم ارسال الهمسة"
        )

    # ثيم
    if text == "ثيم":

        return bot.reply_to(
            message,
            "https://t.me/addtheme/ClassicBlue"
        )

    # شعر
    if text == "شعر":

        return bot.reply_to(
            message,
            "https://www.youtube.com/results?search_query=قصيدة"
        )

    # انمي
    if text == "انمي":

        return bot.reply_to(
            message,
            "Attack on Titan\nصراع البشر ضد العمالقة"
        )

    # فلم
    if text == "فلم":

        return bot.reply_to(
            message,
            "Interstellar\nرحلة فضائية لانقاذ البشرية"
        )

    # مسلسل
    if text == "مسلسل":

        return bot.reply_to(
            message,
            "Breaking Bad\nمدرس يدخل عالم المخدرات"
        )

    # زوجني
    if text in ["زوجني", "ز"]:

        return bot.reply_to(
            message,
            "تم زواجك عشوائياً 😂"
        )

    # نداء
    if text in ["نداء", "نن"]:

        return bot.reply_to(
            message,
            "تم نداء عضو عشوائي"
        )

    # كتم
    if text == "كتم":

        if not message.reply_to_message:
            return bot.reply_to(message, "رد على الشخص")

        try:

            bot.restrict_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id,
                can_send_messages=False
            )

            bot.reply_to(message, "تم كتم العضو")

        except:

            bot.reply_to(message, "ماكدرت اكتمه")

    # الغاء الكتم
    if text == "الغاء الكتم":

        if not message.reply_to_message:
            return bot.reply_to(message, "رد على الشخص")

        try:

            bot.restrict_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id,
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )

            bot.reply_to(message, "تم الغاء الكتم")

        except:

            bot.reply_to(message, "ماكدرت الغي الكتم")

    # حظر
    if text == "حظر":

        if not message.reply_to_message:
            return bot.reply_to(message, "رد على الشخص")

        try:

            bot.ban_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id
            )

            bot.reply_to(message, "تم حظر العضو")

        except:

            bot.reply_to(message, "ماكدرت احظره")

    # طرد
    if text == "طرد":

        if not message.reply_to_message:
            return bot.reply_to(message, "رد على الشخص")

        try:

            uid = message.reply_to_message.from_user.id

            bot.ban_chat_member(
                message.chat.id,
                uid
            )

            bot.unban_chat_member(
                message.chat.id,
                uid
            )

            bot.reply_to(message, "تم طرد العضو")

        except:

            bot.reply_to(message, "ماكدرت اطرده")


print("BOT READY")

bot.infinity_polling(skip_pending=True)
