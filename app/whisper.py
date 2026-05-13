import uuid

from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

WHISPERS = {}

def create_whisper(bot, message):

    if not message.reply_to_message:
        bot.reply_to(message, "استعمل الامر بالرد")
        return

    text = message.text.split(maxsplit=1)

    if len(text) < 2:
        bot.reply_to(message, "اكتب الهمسة")
        return

    whisper_text = text[1]

    target = message.reply_to_message.from_user

    whisper_id = str(uuid.uuid4())[:8]

    WHISPERS[whisper_id] = {
        "text": whisper_text,
        "target": target.id,
        "sender": message.from_user.id,
        "sender_name": message.from_user.first_name
    }

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton(
            "همسة",
            callback_data=f"whisper_{whisper_id}"
        )
    )

    bot.reply_to(
        message,
        f"تم ارسال همسة لـ {target.first_name}",
        reply_markup=kb
    )


def handle_whisper(bot, call):

    whisper_id = call.data.split("_")[1]

    data = WHISPERS.get(whisper_id)

    if not data:
        bot.answer_callback_query(
            call.id,
            "الهمسة محذوفة",
            show_alert=True
        )
        return

    if call.from_user.id != data["target"]:

        bot.answer_callback_query(
            call.id,
            "هذه الهمسة ليست لك",
            show_alert=True
        )

        try:

            bot.send_message(
                data["sender"],
                f"""
شخص حاول يفتح همستك

الاسم:
{call.from_user.first_name}

الايدي:
{call.from_user.id}
"""
            )

        except:
            pass

        return

    bot.answer_callback_query(
        call.id,
        data["text"],
        show_alert=True
            )
