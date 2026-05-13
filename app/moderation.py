import telebot

def ban_user(bot, message, user_id):

    try:
        bot.ban_chat_member(
            message.chat.id,
            user_id
        )

        bot.reply_to(
            message,
            "تم حظر العضو"
        )

    except:
        bot.reply_to(
            message,
            "ماكدرت احظر العضو"
        )

def unban_user(bot, message, user_id):

    try:
        bot.unban_chat_member(
            message.chat.id,
            user_id
        )

        bot.reply_to(
            message,
            "تم الغاء حظر العضو"
        )

    except:
        bot.reply_to(
            message,
            "ماكدرت الغي الحظر"
        )

def mute_user(bot, message, user_id):

    try:

        bot.restrict_chat_member(
            message.chat.id,
            user_id,
            can_send_messages=False
        )

        bot.reply_to(
            message,
            "تم كتم العضو"
        )

    except:

        bot.reply_to(
            message,
            "ماكدرت اكتم العضو"
        )

def unmute_user(bot, message, user_id):

    try:

        bot.restrict_chat_member(
            message.chat.id,
            user_id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True
        )

        bot.reply_to(
            message,
            "تم الغاء الكتم"
        )

    except:

        bot.reply_to(
            message,
            "ماكدرت الغي الكتم"
        )

def kick_user(bot, message, user_id):

    try:

        bot.ban_chat_member(
            message.chat.id,
            user_id
        )

        bot.unban_chat_member(
            message.chat.id,
            user_id
        )

        bot.reply_to(
            message,
            "تم طرد العضو"
        )

    except:

        bot.reply_to(
            message,
            "ماكدرت اطرد العضو"
        )
