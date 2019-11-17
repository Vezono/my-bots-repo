import os
import telebot
import time
import random
import threading
from telebot import types
from pymongo import MongoClient
import traceback
import apiai, json
from api.ai import Agent
from manybotslib import BotsRunner

token = os.environ['god']
bot = telebot.TeleBot(token)

neiro = apiai.ApiAI(os.environ['neirogod'])
parent='projects/small-talk-rshahq/Small-Talk'

agent = Agent(
'cipraded',
os.environ['neirogod'],
os.environ['neirogoduser'],
)

training = False
teachers = [268486177, 792414733, 441399484]
@bot.message_handler(commands=['status'])
def status(m):
    bot.reply_to(m, runner.get_status())
@bot.message_handler()
def txt(m):
    response = react(m)
    if response:
        bot.reply_to(m, response)
def react(m):
    request = neiro.text_request()
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'cipraded' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = m.text.lower() # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    return response
print('God works!')
runner = BotsRunner(teachers) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("God", bot)
runner.set_main_bot(bot)
runner.run()
