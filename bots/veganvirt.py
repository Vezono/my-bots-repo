'''
from manybotslib import BotsRunner
import os
import telebot
import math
import random
import threading
import calendar
import time
import traceback
from telebot import types
token = os.environ['veganvirt']
bot = telebot.TeleBot(token)
randlist=['Возбужденный Самец', 'Веган', 'Большой Банан', 'Гей Воробей', 'Большая Залупа Коня', 'Малая Залупа Коня', 'Осёл', 'Трахер', 
         'Сыч ебаный', 'Пидорас', 'Дрочила', 'Дрочемыш', 'Анальный Зонд', 'Волосатая Феминистка', 'Гей', 'Еблет', 'Исма', 'Еблак', 'Минетный монстр',
         'Анальный зверь']
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
    if call.data=='join':        
      try:
        if call.from_user.id not in info.lobby.game[call.message.chat.id]['players']:
              z=0
              for ids in info.lobby.game:
                  if call.from_user.id in info.lobby.game[ids]['players']:
                    z+=1    
              if z==0:
               if len(info.lobby.game[call.message.chat.id]['players'])<len(randlist):
                  info.lobby.game[call.message.chat.id]['players'].update(createuser(call.from_user.id, call.message.chat.id))
                  bot.send_message(call.message.chat.id, 'Аноним вошел!')
                  info.lobby.alreadyplay.append(call.from_user.id)
               else:
                   try:
                       bot.send_message(call.from_user.id, 'Достигнуто максимальное число пидоров!')
                   except:
                       pass
                    
               #if len(info.lobby.game[call.message.chat.id]['players'])>len(randlist):
               # bot.send_message(call.message.chat.id, 'Набор окончен!')
               # begin(call.message.chat.id)
      except:
        pass
                                  


def del2(id):
    try:
      del info.lobby.game[id]
      bot.send_message(id, '25 минут прошло! Вирт остановлен!')
    except:
      pass

def delplayer(id, id2):
    try:
        del info.lobby.game[id]['players'][id2]
    except:
        pass
            
def deleter(id):
  try:
    del info.lobby.game[id]
  except:
    pass
    
@bot.message_handler(commands=['stop'])
def s(m):
  for ids in info.lobby.game:
    if m.from_user.id in info.lobby.game[ids]['players']:
        bot.send_message(ids, 'Аноним вышел!')
        t=threading.Timer(0.1, delplayer, args=[ids, m.from_user.id])
        t.start()

@bot.message_handler(commands=['lobby'])
def m(m):
    if m.chat.id not in info.lobby.game:
        info.lobby.game.update(createroom(m.chat.id))
        t=threading.Timer(1500, del2, args=[m.chat.id])
        t.start()
        info.lobby.game[m.chat.id]['timer']=t
        bot.send_message(441399484, 'Вирт начался где-то!')
        Keyboard=types.InlineKeyboardMarkup()          
        Keyboard.add(types.InlineKeyboardButton(text='Писька', callback_data='join'))
        info.lobby.game[m.chat.id]['startm']=bot.send_message(m.chat.id, 'Начинаем! жмите на кнопку, чтобы присоединиться', reply_markup=Keyboard)
    else:
      try:
        bot.reply_to(info.lobby.game[m.chat.id]['startm'], 'Вирт уже идёт!')
      except:
        pass

def namechoice(id):
    x=random.choice(randlist)
    while x in info.lobby.game[id]['nicks']:
        x=random.choice(randlist)
    info.lobby.game[id]['nicks'].append(x)
    return x
        

         


@bot.message_handler(content_types=['text'])
def h(m):
    for ids in info.lobby.game:
        if m.from_user.id in info.lobby.game[ids]['players']:
          if m.chat.id>0:
            try:
              bot.send_message(ids, '_'+info.lobby.game[ids]['players'][m.from_user.id]['name']+'_:\n'+m.text, parse_mode='markdown')
              info.lobby.game[ids]['timer'].cancel()
              t=threading.Timer(1500, del2, args=[ids])
              t.start()
              info.lobby.game[ids]['timer'].stop()
              info.lobby.game[ids]['timer']=t
            except:
                pass
            try:
                for idd in info.lobby.game[ids]['players']:
                    if m.from_user.id!=idd:
                      bot.send_message(idd, '_'+info.lobby.game[ids]['players'][m.from_user.id]['name']+'_:\n'+m.text, parse_mode='markdown')
            except:
                pass

    
def createroom(id):
  return{id:{
      'nicks':[],
      'startm':None,
      'timer':None,
    'players':{
    }
     }
      }   
        
def createuser(id, chatid):
    return{id:{
           'name':namechoice(chatid)
          }
          }
       
       
       


runner = BotsRunner() # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Veganvirt", bot)
runner.set_main_bot(bot)
runner.run()
'''
