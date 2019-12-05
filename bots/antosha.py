import telebot
from manybotslib import BotsRunner
from telebot import types

import os

import time
import random
import threading

import traceback

bot_token = os.environ['antosha']
bot = telebot.TeleBot(bot_token)

client=MongoClient(os.environ['database'])
db=client.antosha
phrases=db.phrases

creator = 792414733

timings = '''
1. Персонажи, все, включая закадровых - 11-12 декабря.
Нужна характеристика.
2. Сюжет - с 12 по 18-19 декабря. Важно каждое предложение.
3. Изображения локаций, персонажей - с 19 по 24-25 декабря.
На изображении требуются: персонаж в полнорост, без сложной позы, палитра, краткое описание персонажа, макет.
4. Оформление - с 25 по 31 декабря.

ДЕДЛАЙН РЕЛИЗА ФАНФИКА - 3 ЯНВАРЯ.
'''
@bot.message_handler()
def texthandler(m):
    if 'бот' in m.text.lower() or 'антон' in m.text.lower():
        bot.reply_to(m, random.choice(['Бляха', 'I`ll be back']))
@bot.message_handler(commands=['status'])
def status(m):
    bot.reply_to(m, runner.get_status())
@bot.message_handler(commands=['getm'])
def status(m):
    if m.from_user.id == creator:
        bot.reply_to(m, str(m))
@bot.message_handler(commands=['timings'])
def status(m):
    bot.reply_to(m, timings)        
@bot.message_handler(commands=['joke'])
def joke(m):     
    pass
@bot.message_handler(commands=['addjoke'])
def addjoke(m):
    pass
@bot.message_handler(commands=['tea'])
def ftea(m):
    if m.reply_to_message:
        from_user = m.from_user.first_name
        if m.text.count(' ') == 0:
            tea = 'обычный'
        else:
            tea = m.text.split(' ', 1)[1]
        touser = m.reply_to_message.from_user.first_name
        ahref = '<a href="tg://user?id={}">{}</a>'.format(m.reply_to_message.from_user.id, touser)
        kb = types.InlineKeyboardMarkup()
        btns = []
        btns2 = []
        for i in ['drink', 'reject']:
            btns.append(types.InlineKeyboardButton(rus(i), callback_data='{} {}'.format(i, touser)))
        for i in ['throw']:
            btns2.append(types.InlineKeyboardButton(rus(i), callback_data='{} {}'.format(i, touser)))
        kb.add(*btns)
        kb.add(*btns2)
        if touser == bot.get_me().first_name:
            tts = 'Н-но это я должен готовить чай вам, ' + from_user + '!!'
            kb = None
        else:
            tts = '{} приготовил чай "{}" для вас, {}!'.format(from_user, tea, ahref)
        bot.delete_message(m.chat.id, m.message_id)
        bot.send_message(m.chat.id, tts, reply_markup=kb, parse_mode='HTML')
    else:
        if m.text.count(' ') == 0:
            tea = 'обычный'
        else:
            tea = m.text.split(' ', 1)[1]
        tts = '{} заварил себе чай "{}"!'.format(m.from_user.first_name, tea)
        bot.delete_message(m.chat.id, m.message_id)
        bot.send_message(m.chat.id, tts)

r = {'drink': 'Выпить',
     'reject': 'Отказаться',
     'throw': 'Вылить'}

def rus(name):
    try:
        return r[name]
    except:
        return name
runner = BotsRunner([792414733]) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Antosha", bot)
runner.set_main_bot(bot)
print('Antosha works!')
runner.run()
