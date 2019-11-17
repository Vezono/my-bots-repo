import telebot
from manybotslib import BotsRunner
from telebot import types

import os

import time
import random
import threading

import traceback

global_admins = [792414733]
bot_token = os.environ['cooker']
bot = telebot.TeleBot(bot_token)
bot_id = bot.get_me().id
eatable = ['суп', 'картофель', 'торт', 'вода', 'кока кола', 'сок из апельсинов', 'клубника', 'отрава', 'пицца']
cookers={}
def medit(message_text, chat_id, message_id, reply_markup=None, parse_mode='Markdown'):
    return bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text, reply_markup=reply_markup,
                                 parse_mode=parse_mode)
@bot.message_handler(commands=['cook'])
def eat(m):
    try:
        meal = m.text.lower().split(' ', 1)[1]
    except:
        bot.send_message(m.chat.id, 'Вы забыли указать, что именно вы хотите приготовить!')
    if m.reply_to_message is None:
        try:
            cookself(m, meal)
        except:
            bot.send_message(m.chat.id, traceback.format_exc())
    else:
        try:
            cookto(m, meal)
        except:
            bot.send_message(m.chat.id, traceback.format_exc())
@bot.message_handler(commands=['status'])
def status(m):
    bot.reply_to(m, runner.get_status())
@bot.message_handler(commands=['append'])
def appendix(m):
    try:
        meal = m.text.lower().split(' ', 1)[1]
        eatable.append(meal)
        bot.send_message(m.chat.id, 'Я научился готовить '+ meal + '!')
        bot.send_message(main_admin_id, str(eatable))
    except:
        bot.send_message(m.chat.id, 'Вы забыли указать, что именно готовить!')
@bot.message_handler(commands=['remove'])
def appendix(m):
    if m.from_user.id != main_admin_id:
        return
    meal = m.text.lower().split(' ', 1)[1]
    eatable.remove(meal)
    bot.send_message(m.chat.id, 'Я разучился готовить '+ meal + '!')
    print(eatable)
          
def cookto(m, meal):
    tts = m.from_user.first_name + ' приготовил(а) пользователю ' + m.reply_to_message.from_user.first_name + ' ' + meal + '!'
    if meal in eatable:
        kb=types.InlineKeyboardMarkup(3) 
        artrits = meal
        buttons1=[types.InlineKeyboardButton(text='Съесть', callback_data='eat '+artrits), 
                  types.InlineKeyboardButton(text='Оставить', callback_data='stay '+artrits), 
                  types.InlineKeyboardButton(text='Выбросить', callback_data='trash '+artrits)]
        kb.add(*buttons1)
        oldm = m
        m = bot.reply_to(m, tts, reply_markup=kb)
    else:
        bot.send_message(m.chat.id, 'Он(а) не может съесть ' + meal + ', потому что я неумею это готовить. Чтобы научить меня - /append еда.')
def cookself(m, meal):
    if meal in eatable:
        bot.send_message(m.chat.id, m.from_user.first_name + ' сьел(а) ' + meal + '!')
    else:
        bot.send_message(m.chat.id, 'Вы не можете съесть ' + meal + ', потому что я неумею это готовить. Чтобы научить меня - /append еда.')
        
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
    calldata = call.data
    attribut = calldata.split()[0]
    userid = call.message.reply_to_message.from_user.id
    meal = calldata.split()[1]
    user_name = call.message.reply_to_message.from_user.first_name
    mid = call.message.message_id
    if userid == call.from_user.id:
        if attribut == 'eat':
            tts = call.from_user.first_name + ' с апетитом сьел(а) блюдо "' + meal + '" от пользователя ' + user_name + '!'
            medit(call.message.chat.id, mid, tts, reply_markup=None)
        elif attribut == 'stay':
            tts = call.from_user.first_name + ' решил(а) не есть блюдо "' + meal + '" от пользователя ' + user_name + '!'
            medit(call.message.chat.id, mid,  tts, reply_markup=None)
        elif attribut == 'trash':
            tts = call.from_user.first_name + ' выбросил(а) блюдо "' + meal + '" от пользователя ' + user_name + '!'
            medit(call.message.chat.id, mid,  tts, reply_markup=None)     
    else:
        bot.answer_callback_query(call.id, 'Это не ваше меню!')
runner = BotsRunner(global_admins) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Cooker", bot)
runner.set_main_bot(controller)
print('Cooker works!')
runner.run()
