import telebot

import config
from .db import db
from .views import Views

views = Views()

token = config.environ['telegrad']
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_handler(m):
    if db.user_ever_been(m.from_user.id):
        return
    user = db.form_user_dict(m.from_user)
    kb = views.form_register_keyboard(user)
    bot.reply_to(m, 'Приветствуем тебя здесь. Создай персонажа.', reply_markup=kb)


@bot.callback_query_handler(func=lambda c: db.user_ever_been(c.from_user.id))
def callback_handler():
    pass
