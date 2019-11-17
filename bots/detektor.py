import os

import telebot
from telebot import types
from manybotslib import BotsRunner

import time
import random
import threading
import traceback

from telebot import types
from pymongo import MongoClient

token = os.environ['detektor']
bot = telebot.TeleBot(token)

admin = 792414733

@bot.message_handler(commands=['start'])
def start(m):   
    bot.send_message(m.chat.id, 'Здравствуйте! Я подключен к датабазе бога! Задавайте вопросы. /help для помощи')
@bot.message_handler(commands=['help'])
def help(m):
    bot.send_message(m.chat.id, '/yesno Вопрос?\n/question "Вопрос?" ответ1/ответ2')
@bot.message_handler(commands=['yesno'])
def yesno(m):
    random.seed(m.text.split(' ', 1)[1])
    so = random.choice(['Да.', 'Нет.'])
    bot.send_message(m.chat.id, so)
    
@bot.message_handler(commands=['question'])
def question(m):
    try:
        txt = m.text.split(' ', 1)[1].split('"')
        quest = txt[1]
        argss = txt[2][1:].split('/')
        random.seed(quest)
        so = random.choice(argss)
        print(argss)
        print(so)
        so = "Вопрос: " + quest + '\n' + 'Ответ: ' + so
        bot.send_message(m.chat.id, so)
    except:
        bot.send_message(792414733, traceback.format_exc())
    
@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    try:
        message = query.query
        txt = message.split('"')
        print(txt)
        quest = txt[1]
        argss = txt[2][1:].split('/')
        if False:
            argss=['Да.', 'Нет.']
        else:
            pass
        random.seed(quest)
        so = random.choice(argss)
        print(argss)
        print(so)
        pso = "Вопрос: " + quest + '\n' + 'Ответ: ' + so   
        tts = types.InlineQueryResultArticle(
                id='1', title=quest,
                description=so,
                input_message_content=types.InputTextMessageContent(
                message_text=pso))
        bot.answer_inline_query(query.id, [tts])
    except:
        bot.send_message(admin, traceback.format_exc())      
print('Detektor works!')
runner = BotsRunner([admin])
runner.add_bot("Detektor", bot)
runner.set_main_bot(bot)
runner.run()
