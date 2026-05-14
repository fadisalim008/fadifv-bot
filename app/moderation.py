from app.ranks import get_rank
from app.warnings import add_warning, get_warnings, reset_warnings

OWNER_ID = 8065884629

muted_users = {}
banned_users = {}
restricted_users = {}

def is_owner(user_id):
    return int(user_id) == OWNER_ID

def is_basic_dev(chat_id, user_id):
    return is_owner(user_id) or get_rank(chat_id, user_id) == "مطور اساسي"

def get_target(message):
    if not message.reply_to_message:
        return None
    return message.reply_to_message.from_user

def mute(bot, message):

    target = get_target(message)

    if not target:
        return bot.reply_to(message, "رد على الشخص")

    muted_users.setdefault(str(message.chat.id), set())
    muted_users[str(message.chat.id)].add(target.id)

    try:

        bot.restrict_chat_member(
            message.chat.id,
            target.id,
            can_send_messages=False
        )

    except:
        pass

    bot.reply_to(message, "تم كتم العضو")

def unmute(bot, message):

    target = get_target(message)

    if not target:
        return bot.reply_to(message, "رد على الشخص")

    muted_users.get(str(message.chat.id), set()).discard(target.id)

    try:

        bot.restrict_chat_member(
            message.chat.id,
            target.id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )

    except:
        pass

    bot.reply_to(message, "تم الغاء الكتم")

def ban(bot, message):

    if not is_basic_dev(message.chat.id, message.from_user.id):

        return bot.reply_to(
            message,
            "الحظر للمطور الاساسي فقط"
        )

    target = get_target(message)

    if not target:
        return bot.reply_to(message, "رد على الشخص")

    try:

        bot.ban_chat_member(
            message.chat.id,
            target.id
        )

        bot.reply_to(message, "تم حظر العضو")

    except:

        bot.reply_to(message, "ماكدرت احظر العضو")

def unban(bot, message):

    if not is_basic_dev(message.chat.id, message.from_user.id):

        return bot.reply_to(
            message,
            "الغاء الحظر للمطور الاساسي فقط"
        )

    target = get_target(message)

    if not target:
        return bot.reply_to(message, "رد على الشخص")

    try:

        bot.unban_chat_member(
            message.chat.id,
            target.id
        )

        bot.reply_to(message, "تم الغاء الحظر")

    except:

        bot.reply_to(message, "ماكدرت الغي الحظر")

def kick(bot, message):

    if not is_basic_dev(message.chat.id, message.from_user.id):

        return bot.reply_to(
            message,
            "الطرد للمطور الاساسي فقط"
        )

    target = get_target(message)

    if not target:
        return bot.reply_to(message, "رد على الشخص")

    try:

        bot.ban_chat_member(
            message.chat.id,
            target.id
        )

        bot.unban_chat_member(
            message.chat.id,
            target.id
        )

        bot.reply_to(message, "تم طرد العضو")

    except:

        bot.reply_to(message, "ماكدرت اطرد العضو")

def restrict(bot, message):

    target = get_target(message)

    if not target:
        return bot.reply_to(message, "رد على الشخص")

    restricted_users.setdefault(str(message.chat.id), set())
    restricted_users[str(message.chat.id)].add(target.id)

    try:

        bot.restrict_chat_member(
            message.chat.id,
            target.id,
            can_send_messages=False
        )

    except:
        pass

    bot.reply_to(message, "تم تقييد العضو")

def lift_restrictions(bot, message):

    target = get_target(message)

    if not target:
        return bot.reply_to(message, "رد على الشخص")

    muted_users.get(str(message.chat.id), set()).discard(target.id)
    restricted_users.get(str(message.chat.id), set()).discard(target.id)

    try:

        bot.restrict_chat_member(
            message.chat.id,
            target.id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )

    except:
        pass

    bot.reply_to(message, "تم رفع القيود")

def warn(bot, message):

    target = get_target(message)

    if not target:
        return bot.reply_to(message, "رد على الشخص")

    count = add_warning(
        message.chat.id,
        target.id
    )

    if count >= 3:

        return bot.reply_to(
            message,
            f"هذا العضو عبر جميع الانذارات\nعدد انذاراته: {count}"
        )

    bot.reply_to(
        message,
        f"تم انذاره\nعدد انذاراته: {count}"
    )

def warnings_count(bot, message):

    target = get_target(message)

    if not target:
        return bot.reply_to(message, "رد على الشخص")

    count = get_warnings(
        message.chat.id,
        target.id
    )

    bot.reply_to(message, f"انذاراته: {count}")

def clear_warnings(bot, message):

    target = get_target(message)

    if not target:
        return bot.reply_to(message, "رد على الشخص")

    reset_warnings(
        message.chat.id,
        target.id
    )

    bot.reply_to(message, "تم مسح انذاراته")

def clear_muted(bot, message):

    muted_users[str(message.chat.id)] = set()

    bot.reply_to(
        message,
        "تم مسح المكتومين"
    )

def clear_restricted(bot, message):

    restricted_users[str(message.chat.id)] = set()

    bot.reply_to(
        message,
        "تم مسح المقيدين"
    )

def clear_banned(bot, message):

    banned_users[str(message.chat.id)] = set()

    bot.reply_to(
        message,
        "تم مسح المحظورين"
    )
