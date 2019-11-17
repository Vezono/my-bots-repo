import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import traceback
from manybotslib import BotsRunner
n=0
token = os.environ['lifegame']
bot = telebot.TeleBot(token)

em_alive='🦠'
em_dead='⬛️'

games={}

@bot.message_handler(commands=['life'])
def life(m):
    game=creategame(m.chat.id)
    for ids in game:
        c=ids
    x=m.text.split(' ')
    i=1
    while i<len(x):
        try:
            game[c]['world'][x[i]]='alive'
            i+=1
        except:
            pass
    
    games.update(game)
    startgame(game[c])

    
@bot.message_handler(commands=['clear'])
def clearr(m):
    dl=[]
    try:
        for ids in games:
            if games[ids]['id']==m.chat.id:
                dl.append(ids)
        for ids in dl:
            games[ids]['del']=1
            del games[ids]
        bot.send_message(m.chat.id, 'Удалил все игры в чате')
    except:
        bot.send_message(441399484, traceback.format_exc())

def startgame(game, no=0):
    text=''
    x=0
    y=0
    global em_alive
    global em_dead
    while y<int(game['size'][0]):
        x=0
        while x<int(game['size'][1]):
            cpoint=str(x)+str(y)
            if game['world'][cpoint]=='alive':
                text+=em_alive
            else:
                text+=em_dead
            x+=1
        y+=1
        text+='\n'
    if game['msg']==None:
        game['msg']=bot.send_message(game['id'], text)
    else:
        try:
            medit(text, game['msg'].chat.id, game['msg'].message_id)
        except:
            pass
    if no==0:
        mapedit(game)
    else:
        del games[game['code']]
    
    
def mapedit(game):
    alive=[]
    dead=[]
    for ids in game['world']:
        x=int(ids[0])
        y=int(ids[1])
        nearalive=0
        i1=-1
        i2=-1
        while i1<=1:
            i2=-1
            while i2<=1:
                point=str(x+i1)+str(y+i2)
                try:
                    if game['world'][point]=='alive' and point!=ids:
                        nearalive+=1
                except:
                    #bot.send_message(441399484, traceback.format_exc())
                    pass
                i2+=1
            i1+=1
        if game['world'][ids]=='alive':
            if nearalive>=2 and nearalive<=3:
                alive.append(ids)
            else:
                dead.append(ids)
                
        elif game['world'][ids]=='dead':
            if nearalive==3:
                alive.append(ids)
            else:
                dead.append(ids)
    for ids in dead:
        game['world'][ids]='dead'
    for ids in alive:
        game['world'][ids]='alive'
    d=0
    if game['last']==game['world']:
        game['count']+=1
        if game['count']>=3:
            del games[game['code']]  
            bot.send_message(441399484, 'deleted')
            d=1
    else:
        game['count']=0
    game['last']=game['world'].copy()
    if game['del']==1:
        d=1
    if len(alive)!=0 and d!=1:
        t=threading.Timer(game['speed'], startgame, args=[game])
        t.start()
       
    elif d!=1:
        t=threading.Timer(game['speed'], startgame, args=[game, 1])
        t.start()
    

    
def creategame(chatid, size='99', speed=1.2):   # x = size[0];  y = size[1];   speed в секундах.
    global n
    n+=1
    world={}
    x=0
    y=0
    while x<int(size[0]):
        y=0
        world.update({str(x)+str(y):'dead'})
        while y<int(size[1]):
            world.update({str(x)+str(y):'dead'})
            y+=1
        x+=1
    return {n:{
        'id':chatid,
        'world':world,
        'size':size,
        'speed':speed,
        'msg':None,
        'code':n,
        'last':{},
        'count':0,
        'xod':0,
        'del':0
    }
           }

    
def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)    
                                 
runner = BotsRunner([792414733]) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Lifegame", bot)
runner.set_main_bot(bot)
runner.run()
