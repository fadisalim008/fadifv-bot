from pyrogram import filters

async def register(app):

    @app.on_message(filters.text)
    async def replies(client, message):
        text = message.text

        if text == "سورس":
            await message.reply_text("أهلاً بك في سورس فادي")

        elif text == "المطور":
            await message.reply_text("fvamv")
