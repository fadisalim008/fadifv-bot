import os
import requests
import yt_dlp
from app.buttons import source_button
from app.config import RAPID_API_KEY

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def send_music(bot, message, query):
    try:
        # 1) RapidAPI
        if RAPID_API_KEY:
            headers = {
                "X-RapidAPI-Key": RAPID_API_KEY,
                "X-RapidAPI-Host": "yt-search-and-download-mp3.p.rapidapi.com"
            }

            search = requests.get(
                "https://yt-search-and-download-mp3.p.rapidapi.com/search",
                headers=headers,
                params={"q": query},
                timeout=15
            ).json()

            items = search.get("videos") or search.get("result") or []
            if items:
                video = items[0]
                url = video.get("url") or f"https://www.youtube.com/watch?v={video.get('id')}"
                title = video.get("title", query)

                mp3 = requests.get(
                    "https://yt-search-and-download-mp3.p.rapidapi.com/mp3",
                    headers=headers,
                    params={"url": url},
                    timeout=30
                ).json()

                audio = (
                    mp3.get("link") or mp3.get("url") or mp3.get("audio")
                    or mp3.get("download") or mp3.get("downloadUrl")
                )

                if audio:
                    return bot.send_audio(
                        message.chat.id,
                        audio,
                        title=title,
                        caption=f"🎧 {title}",
                        reply_markup=source_button(),
                        reply_to_message_id=message.message_id
                    )

        # 2) yt-dlp YouTube + Android/iPhone + cookies
        sources = [
            (f"ytsearch20:{query}", ["android"]),
            (f"ytsearch20:{query} اغنية", ["ios"]),
            (f"ytsearch20:{query} audio", ["android"]),
            (f"ytsearch20:{query} official", ["ios"]),
            (f"scsearch10:{query}", None),
        ]

        for search_url, client in sources:
            try:
                opts = {
                    "format": "bestaudio/best",
                    "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
                    "noplaylist": True,
                    "quiet": True,
                    "no_warnings": True,
                    "socket_timeout": 12,
                    "retries": 2,
                }

                if os.path.exists("cookies.txt"):
                    opts["cookiefile"] = "cookies.txt"

                if client:
                    opts["extractor_args"] = {
                        "youtube": {"player_client": client}
                    }

                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(search_url, download=True)

                    if "entries" in info:
                        info = next((x for x in info["entries"] if x), None)

                    if not info:
                        continue

                    title = info.get("title", query)
                    path = ydl.prepare_filename(info)

                    with open(path, "rb") as audio:
                        bot.send_audio(
                            message.chat.id,
                            audio,
                            title=title,
                            caption=f"🎧 {title}",
                            reply_markup=source_button(),
                            reply_to_message_id=message.message_id
                        )

                    try:
                        os.remove(path)
                    except:
                        pass

                    return

            except:
                continue

        return bot.reply_to(message, "صار خطأ أثناء جلب الأغنية")

    except:
        return bot.reply_to(message, "صار خطأ أثناء جلب الأغنية")
