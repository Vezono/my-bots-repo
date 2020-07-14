import telebot

import config
from .db import db

token = config.environ['TOKEN']
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_handler(m):
    if db.user_ever_been(m.from_user.id):
        return
    db.form_user_dict(m.from_user)
