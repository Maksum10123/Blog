import telebot
from api import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    args = message.text.split()
    if len(args) > 1:
        token = args[1]
        chat_id = message.chat.id
        backlink = f"http://127.0.0.1:8000/accounts/connect-telegram/done/{token}/{chat_id}/"
        text = (
            f"Привет {message.from_user.first_name}\n\n"
            f"Для завершение привязки нажми на кнопку"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton(text='Пожтвердить привязку', url=backlink)
        markup.add(btn)
        bot.send_message(chat_id, text, reply_markup=markup)
    else:
        bot.send_animation(message.chat.id, "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcW5hMGFwOWVyMmZnZjhtbXVmbmdpN29mODNhYjdyNmIwZXRraDJteCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/A363LZlQaX0ZO/giphy.gif")
print("Бот запущен")
bot.polling()