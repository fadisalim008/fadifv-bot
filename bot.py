from telebot import TeleBot

TOKEN = "8667177884:AAFiV6hCpSX2AMyqi9apiiXo0UavZDNan74"

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "هلا بيك 👋\nبوتك شغال بنجاح ✅")

print("Bot running...")
bot.infinity_polling()
