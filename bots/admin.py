import os
import traceback

import telebot
from telebot import types
from manybotslib import BotsRunner

import datetime
import calendar
import time
import threading

import random

from pymongo import MongoClient



token = os.environ['admin']
bot = telebot.TeleBot(token)


global_admins = [268486177, 792414733, 441399484]
group_admins = ['administrator', 'creator']

@bot.message_handler(commands=['status'])
def status(m):
    bot.reply_to(m, runner.get_status())
@bot.message_handler(commands=['mute'])
def mute(m):
    if m.chat.type == 'private':
        return    
    if is_admin(m.chat.id, m.from_user.id) and not is_admin(m.chat.id, m.reply_to_message.from_user.id):
        text=m.text.split(' ')
        try:
            timee=text[1]
            i=int(timee[:-1])
            number=timee[len(timee)-1]
        except:
            i=0
            number='m'
            untildate=int(time.time())
            if number=='m':
                untildate+=i*60
                datetext='минут'
            if number=='h':
                untildate+=i*3600
                datetext='часов'
            if number=='d':
                untildate+=i*3600*24
                datetext='дней'           
            if m.reply_to_message:
                ahref = '[' +m.reply_to_message.from_user.first_name + ']' + '(tg://user?id=' +  str(m.reply_to_message.from_user.id) + ')'
                bot.restrict_chat_member(can_send_messages=False, user_id=m.reply_to_message.from_user.id, chat_id=m.chat.id, until_date=untildate)
                if i==0:
                    text='Кинул ' + ahref + ' в мут навсегда.'
                else:
                    text='Кинул ' + ahref + ' в мут на '+str(i)+' '+datetext+'.'
                bot.send_message(m.chat.id, text, parse_mode='Markdown')
    else:
        bot.send_message(m.chat.id, 'Ты кто такой чтобы это делать?')
        
        
@bot.message_handler(commands=['ban'])
def ban(m):
    if m.chat.type == 'private':
        return    
    if is_admin(m.chat.id, m.from_user.id) and not is_admin(m.chat.id, m.reply_to_message.from_user.id):
        text=m.text.split(' ')
        try:
            timee=text[1]
            i=int(timee[:-1])
            number=timee[len(timee)-1]
        except:
            i=0
            number='m'
            untildate=int(time.time())
            if number=='m':
                untildate+=i*60
                datetext='минут'
            if number=='h':
                untildate+=i*3600
                datetext='часов'
            if number=='d':
                untildate+=i*3600*24
                datetext='дней'           
            if m.reply_to_message:
                ahref = '[' +m.reply_to_message.from_user.first_name + ']' + '(tg://user?id=' +  str(m.reply_to_message.from_user.id) + ')'
                bot.kick_chat_member(user_id=m.reply_to_message.from_user.id, chat_id=m.chat.id, until_date=untildate)
                if i==0:
                    text='Кинул ' + ahref + ' в мут навсегда.'
                else:
                    text='Кинул ' + ahref + ' в мут на '+str(i)+' '+datetext+'.'
                bot.send_message(m.chat.id, text, parse_mode='Markdown')
    else:
        bot.send_message(m.chat.id, 'Ты кто такой чтобы это делать?')
@bot.message_handler(commands=['unmute'])
def unmutee(m): 
    if m.chat.type == 'private':
        return
    if is_admin(m.chat.id, m.from_user.id):
       ahref = '[' +m.reply_to_message.from_user.first_name + ']' + '(tg://user?id=' +  str(m.reply_to_message.from_user.id) + ')'
       bot.restrict_chat_member(can_send_messages=True, can_send_other_messages=True, user_id=m.reply_to_message.from_user.id, chat_id=m.chat.id)
       bot.send_message(m.chat.id, 'Анмутил '+ahref+'.', parse_mode='Markdown')
    else:
       bot.send_message(m.chat.id, 'Ты кто такой чтобы это делать?')
       pass
    pass
@bot.message_handler(commands=['unban'])
def unban(m): 
    if m.chat.type == 'private':
        return
    if is_admin(m.chat.id, m.from_user.id):
       ahref = '[' +m.reply_to_message.from_user.first_name + ']' + '(tg://user?id=' +  str(m.reply_to_message.from_user.id) + ')'
       bot.unban_chat_member(user_id=m.reply_to_message.from_user.id, chat_id=m.chat.id)
       bot.send_message(m.chat.id, 'Разбанил '+ahref+'.', parse_mode='Markdown')
    else:
       bot.send_message(m.chat.id, 'Ты кто такой чтобы это делать?')
@bot.message_handler(commands=['kick'])
def kick(m): 
    if m.chat.type == 'private':
        return
    if is_admin(m.chat.id, m.from_user.id):
       ahref = '[' +m.reply_to_message.from_user.first_name + ']' + '(tg://user?id=' +  str(m.reply_to_message.from_user.id) + ')'
       bot.unban_chat_member(user_id=m.reply_to_message.from_user.id, chat_id=m.chat.id)
       bot.send_message(m.chat.id, 'Кикнул '+ahref+'.', parse_mode='Markdown')
    else:
       bot.send_message(m.chat.id, 'Ты кто такой чтобы это делать?')    
    
    
@bot.message_handler(commands=['info'])
def ping(m):
    tts = '*Информация о чате*:\nЧат айди: `{}`\nТип чата: `{}`\n\n*Информация о юзере*: \nИмя юзера: `{}`\nАйди юзера: `{}`' # Text To Send
    if m.reply_to_message:
        tts = tts.format(str(m.chat.id), m.chat.type, m.reply_to_message.from_user.first_name, str(m.reply_to_message.from_user.id))
    else:
        tts = tts.format(str(m.chat.id), m.chat.type, m.from_user.first_name, str(m.from_user.id))
    bot.send_message(m.chat.id, tts)
@bot.message_handler()
def txt(m):
    pass

def is_admin(chat, user):
    chat_member = bot.get_chat_member(chat, user)
    if chat_member.status in group_admins:
        return True
    else:
        return False  
print('Admin works!')
runner = BotsRunner(global_admins) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Admin", bot)
runner.set_main_bot(bot)
runner.run()

