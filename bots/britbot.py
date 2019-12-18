import os
import telebot
import time
import random
import threading
from telebot import types
from pymongo import MongoClient
import traceback
from manybotslib import BotsRunner

client = MongoClient(os.environ['database'])
db = client.gbball
users = db.users
chats = db.chats

token = os.environ['britbot']
bot = telebot.TeleBot(token)
creator = 792414733

@bot.message_handler(commands=['announce'])
def announce(m):
    if m.from_user.id != creator:
        return
    if not m.text.count(' '):
        bot.reply_to(m, 'Недостаточно аргументов.')
    tts = '📣Сообщение разработчика:\n\n' + m.text.split(' ', 1)[1]
    not_announced = ''
    count = 0
    all_users = 0
    for user in users.find({}):
        all_users += 1
        try:
            bot.send_message(user['id'], tts)
            count += 1
        except:
            not_announced += '\n{}'.format(user['id'])
    tts = 'Сообщение отправлено {}/{} юзерам.\nСообщение не получили:\n{}'.format(str(count),
                                                                                  str(all_users),
                                                                                  not_announced)        
    bot.send_message(m.chat.id, tts)       
    

@bot.message_handler(commands=['update'])
def cupdate(m):
    if m.from_user.id != creator:
        return
    if not m.text.count(' '):
        bot.reply_to(m, 'Недостаточно аргументов.')
    tts = '📣Обновление:\n\n' + m.text.split(' ', 1)[1]
    not_announced = ''
    count = 0
    all_chats = 0
    for chat in chats.find({}):
        all_chat += 1
        try:
            bot.send_message(chat['id'], tts)
            count += 1
        except:
            not_announced += '\n{}'.format(chat['id'])
    tts = 'Сообщение отправлено в {}/{} чатов.\nСообщение не получили:\n{}'.format(str(count),
                                                                                   str(all_chats),
                                                                                   not_announced)        
    bot.send_message(m.chat.id, tts) 
    
@bot.message_handler(commands=['start'])
def start(m):            
    if m.chat.type == 'private':
        if not users.find_one({'id':m.from_user.id}):
            users.insert_one(createuser(m.from_user.first_name, m.from_user.id))
    else:
        if not chats.find_one({'id':m.chat.id}):
            chats.insert_one(createchat(m.chat.title, m.chat.id, m))
    bot.send_message(m.chat.id, 'Привет. Добро пожаловать. Снова.')        
        

        
def createuser(name, id):
    return {'id':id,
            'name':name,
            'coins':0
    }
def createchat(name, id, m):
    return {'id':id,
            'name':name,
            'invitor':getlink(m.from_user.first_name, m.from_user.id)
    }
def getlink(name, id):
    return '<a href="tg://user?id={}">{}</a>'.format(id, name)

runner = BotsRunner([creator]) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Brit", bot)
runner.set_main_bot(bot)
print('Brit works!')
runner.run()
