import os
import re
import json
import requests
import yt_dlp

from app.config import BOT_TOKEN, RAPID_API_KEY
from app.buttons import source_button

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def clean_name(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)[:80]

def send_music(bot, message, query):
    wait = bot.reply_to(message, "🎧 جاري البحث...")

    try:
        safe_title = clean_name(query)
        file_name = f"{DOWNLOAD_DIR}/{safe_title}.mp3"

        # RapidAPI
        if RAPID_API_KEY:
            try:
                headers = {
                    "X-RapidAPI-Key": RAPID_API_KEY,
                    "X-RapidAPI-Host": "yt-search-and-download-mp3.p.rapidapi.com"
                }

                search = requests.get(
                    "https://yt-search-and-download-mp3.p.rapidapi.com/search",
                    headers=headers,
                    params={"q": query},
                    timeout=20
                ).json()

                items = search.get("videos") or search.get("result") or []

                if items:
                    video = items[0]

                    url = video.get("url") or f"https://youtube.com/watch?v={video.get('id')}"
                    title = video.get("title", query)

                    mp3 = requests.get(
                        "https://yt-search-and-download-mp3.p.rapidapi.com/mp3",
                        headers=headers,
                        params={"url": url},
                        timeout=30
                    ).json()

                    audio_url = (
                        mp3.get("link")
                        or mp3.get("url")
                        or mp3.get("audio")
                        or mp3.get("download")
                        or mp3.get("downloadUrl")
                    )

                    if audio_url:
                        audio_data = requests.get(audio_url, timeout=40).content

                        safe_title = clean_name(title)
                        file_name = f"{DOWNLOAD_DIR}/{safe_title}.mp3"

                        with open(file_name, "wb") as f:
                            f.write(audio_data)

                        with open(file_name, "rb") as audio:
                            requests.post(
                                f"https://api.telegram.org/bot{BOT_TOKEN}/sendAudio",
                                data={
                                    "chat_id": message.chat.id,
                                    "title": safe_title,
                                    "performer": "SOURCE FADI",
                                    "caption": f"{safe_title} 🎧",
                                    "reply_to_message_id": message.message_id,
                                    "reply_markup": json.dumps(source_button())
                                },
                                files={
                                    "audio": audio
                                },
                                timeout=60
                            )

                        try:
                            os.remove(file_name)
                        except:
                            pass

                        try:
                            bot.delete_message(message.chat.id, wait.message_id)
                        except:
                            pass

                        return

            except:
                pass

        # yt-dlp fallback
        opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            "noplaylist": True,
            "quiet": True,
            "cookiefile": "cookies.txt" if os.path.exists("cookies.txt") else None,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "ios"]
                }
            }
        }

        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)

            if "entries" in info:
                info = info["entries"][0]

            path = ydl.prepare_filename(info)
            title = clean_name(info.get("title", query))

            with open(path, "rb") as audio:
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendAudio",
                    data={
                        "chat_id": message.chat.id,
                        "title": title,
                        "performer": "SOURCE FADI",
                        "caption": f"{title} 🎧",
                        "reply_to_message_id": message.message_id,
                        "reply_markup": json.dumps(source_button())
                    },
                    files={
                        "audio": audio
                    },
                    timeout=60
                )

            try:
                os.remove(path)
            except:
                pass

        try:
            bot.delete_message(message.chat.id, wait.message_id)
        except:
            pass

    except:
        try:
            bot.delete_message(message.chat.id, wait.message_id)
        except:
            pass

        bot.reply_to(
            message,
            "❌ صار خطأ أثناء جلب الأغنية"
                    )
