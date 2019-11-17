
import os
import telebot
import time
import random
import threading
from manybotslib import BotsRunner
from telebot import types
from pymongo import MongoClient
import traceback

token = os.environ['hawkeye']
bot = telebot.TeleBot(token)
admins = [792414733]
fighters=[]
btimer=10

names=['Волк', 'Осёл', 'Кроль', 'Пажилая чимчима', 'Сосааать']

@bot.message_handler(commands=['start'])
def start(m):
    no=0
    for ids in fighters:
        if ids['id']==m.from_user.id:
            no=1
    if no==0:
        fighters.append(createplayer(user=m.from_user))
        bot.send_message(m.chat.id, 'Вы успешно зашли в игру! Теперь ждите, пока ваш боец прострелит кому-нибудь яйцо.\nСоветую кинуть бота в мут!')
 
@bot.message_handler(commands=['add'])
def add(m):
    if m.from_user.id in admins:
        name=m.text.split(' ')[1]
        fighters.append(createplayer(name=name))
        bot.send_message(m.chat.id, 'Добавлен игрок "'+name+'"!')

    
@bot.message_handler(commands=['settimer'])
def settimer(m):
    if m.from_user.id in admins:
        try:
            global btimer
            btimer=int(m.text.split(' ')[1])
        except:
            pass
        
@bot.message_handler(commands=['stats'])
def stats(m):
    me=None
    for ids in fighters:
        if ids['id']==m.from_user.id:
            me=ids
    if me!=None:
        text=''
        text+='ХП: '+str(me['hp'])+'\n'
        text+='В вас попали: '+str(me['hitted'])+' раз(а)\n'
        text+='Вы убили: '+str(me['killed'])+' дурачков\n'
        bot.send_message(m.chat.id, text)


def createplayer(user=None, name=None):
    if user!=None:
        name=user.first_name
        idd=user.id
    else:
        name=name
        idd='npc'
    return {
            'hp':1000,
            'damage':10,
            'killchance':5,
            'name':name,
            'id':idd,
            'hitted':0,  # сколько раз попали
            'killed':0,   # сколько уебал
            'killer':''
               }
        
           
   
    
def fight():
    for ids in fighters:
        alive=[]
        for idss in fighters:
            if idss['hp']>0 and idss['id']!=ids['id']:
                alive.append(idss)
        if len(alive)>0:
            text=''
            target=random.choice(alive)
            dmg=ids['damage']+ids['damage']*(random.randint(-20, 20)/100)
            target['hp']-=dmg
            target['hitted']+=1
            text+='Вы попали в '+target['name']+'! Нанесено '+str(dmg)+' урона.\n'
            if target['hp']<=0:
                ids['killed']+=1
                target['killer']=ids['name']
                text+='Вы убили цель!\n'
            else:
                if random.randint(1,100)<=ids['killchance']:
                    target['hp']=0
                    ids['killed']+=1
                    target['killer']=ids['name']
                    text+='Вы прострелили яйцо цели! Та погибает.\n'
            try:
                bot.send_message(ids['id'], text)
            except:
                pass
    dellist=[]
    for ids in fighters:
        if ids['hp']<=0:
            dellist.append(ids)
    for ids in dellist:
        try:
            bot.send_message(ids['id'], 'Вы сдохли. Вас убил '+ids['killer'])
        except:
            pass
        me=ids
        text='Итоговые статы:\n\n'
        text+='ХП: '+str(me['hp'])+'\n'
        text+='В вас попали: '+str(me['hitted'])+' раз(а)\n'
        text+='Вы убили: '+str(me['killed'])+' дурачков\n'
        try:
            bot.send_message(ids['id'], text)
        except:
            pass
        fighters.remove(ids)
    if len(fighters)<=2:
        name=random.choice(names)
        fighters.append(createplayer(name=name))
    global btimer
    t=threading.Timer(btimer, fight)
    t.start()
    
fight() 

def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)   
runner = BotsRunner(admins) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Hawkeye", bot)
runner.set_main_bot(bot)
print('Hawkeye works!')
runner.run()
