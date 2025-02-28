import time, threading, schedule
from telebot import TeleBot

API_TOKEN = '7294624873:AAEA6i-U03rMzCpVmgEtAeR6gagQLmaE0ew'
bot = TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Hi! Use /set <seconds> <message> to set a timer, and Use /unset to unset all timers")


def beep(chat_id, user_text) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text=user_text)


@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    user_text = message.text.split()[2:]
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        schedule.every(sec).seconds.do(beep, message.chat.id, user_text).tag(message.chat.id)
        bot.reply_to(message, "timer has been set successfully on")
    else:
        bot.reply_to(message, 'Usage: /set <seconds> <message>')


@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)
    bot.reply_to(message, "the timer was successfully stopped")


if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
