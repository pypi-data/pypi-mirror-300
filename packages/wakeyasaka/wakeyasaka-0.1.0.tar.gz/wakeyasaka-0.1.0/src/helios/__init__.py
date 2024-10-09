import telebot
import os
import json

from dotenv import load_dotenv
from wakeonlan import send_magic_packet

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
USER_ID = os.getenv('USER_ID')

bot = telebot.TeleBot(token=BOT_TOKEN)

with open('members.json', 'r') as file:
    members = json.load(file)


@bot.message_handler(commands=['start'], func=lambda m: str(m.from_user.id) == USER_ID)
def on_start(message):
    bot.send_message(message.chat.id, 'Praise the sun!')


@bot.message_handler(content_types=['text'], regexp='^[Ww]ake .+', func=lambda m: str(m.from_user.id == USER_ID))
def arise(message):
    for item in members:
        if item['name'] == message.text.split(' ')[1]:
            send_magic_packet(item['address'])
            bot.send_message(message.chat.id, 'Sent magic package!')
            return
    bot.send_message(message.chat.id, 'Who?')


bot.infinity_polling()
