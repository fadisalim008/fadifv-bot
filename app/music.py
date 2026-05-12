import requests
from app.buttons import source_button

def search_song(query):
    try:
        url = "https://itunes.apple.com/search"

        params = {
            "term": query,
            "limit": 1
        }

        r = requests.get(url, params=params).json()

        if not r["results"]:
            return None

        song = r["results"][0]

        return {
            "name": song["trackName"],
            "audio": song["previewUrl"]
        }

    except:
        return None

def send_music(bot, message, query):
    song = search_song(query)

    if not song:
        return bot.reply_to(
            message,
            "صار خطأ أثناء جلب الأغنية"
        )

    bot.send_audio(
        message.chat.id,
        song["audio"],
        title=song["name"],
        reply_markup=source_button(),
        reply_to_message_id=message.message_id
    )
