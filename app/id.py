def get_id_text(user):

    text = f"""
<blockquote>

<tg-emoji emoji-id="5368324170671202286">👑</tg-emoji>
<b>USER INFO</b>

<tg-emoji emoji-id="5368324170671202287">🔥</tg-emoji>
NaMe ⇴ {user.first_name}

<tg-emoji emoji-id="5368324170671202288">💎</tg-emoji>
uSeR ⇴ @{user.username}

<tg-emoji emoji-id="5368324170671202289">✨</tg-emoji>
iD ⇴ {user.id}

</blockquote>
"""

    return text
