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
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)


games={}

def effect(target='all', amount=0):
      return {
          'target':target,
          'amount':amount
      }
    

coldunstva={
    'start':{},
    'mid':{},
    'end':{}
}
cstart={'Ебанутый':{
    'effects':{'damage':effect(target='all', amount=2)
              },
    'cost':47,
    'name':'Ебанутый'
                },
         
        'Ебущий':{
    'effects':{'damage':effect(target='allenemy', amount=1),
               'damage':effect(target='1random', amount=2)
              },
    'cost':47,
     'name':'Ебущий'

                 },
        'Дохлый':{
    'effects':{'damage':effect(target='allenemy', amount=2),
               'heal':effect(target='1random', amount=1)
              },
    'cost':47,
     'name':'Дохлый'

                 },
          
       }

cmid={'Осёл':{
    'effects':{'damage':effect(target='allenemy', amount=3)
              },
    'cost':47,
    'name':'Осёл'
                },
         
        'Пидорас':{
    'effects':{'heal':effect(target='self', amount=2),
               'stun':effect(target='1random', amount=2)
              },
    'cost':47,
    'name':'Пидорас'

                 },
      'Спермоед':{
    'effects':{'heal':effect(target='allenemy', amount=1),
               'damage':effect(target='self', amount=1)
              },
    'cost':47,
    'name':'Спермоед'

                 }
          
       }

cend={'С нижнего Тагила':{
    'effects':{'heal':effect(target='all', amount=1)
              },
    'cost':47,
    'name':'С нижнего Тагила'
                },
         
        'Дряхлой бабки':{
    'effects':{'stun':effect(target='self', amount=2)
              },
    'cost':47,
    'name':'Дряхлой бабки'

                 },
      'Спидозного мамонта':{
    'effects':{'dagame':effect(target='1randomenemy', amount=3),
               'heal':effect(target='self', amount=3),
              },
    'cost':47,
    'name':'Спидозного мамонта'

                 }
          
       }

for ids in cstart:
    coldunstva['start'].update({ids:cstart[ids]})
for ids in cmid:
    coldunstva['mid'].update({ids:cmid[ids]})
for ids in cend:
    coldunstva['end'].update({ids:cend[ids]})
    

    
@bot.message_handler(commands=['coldunstvo'])
def coldovatt(m):
    if m.chat.id not in games:
        games.update(creategame(m.chat.id))
        bot.send_message(m.chat.id, 'Го колдовать, я создал\n/joen для присоединения.')
    
@bot.message_handler(commands=['joen'])
def coldovattjoen(m):
    try:
        if m.from_user.id not in games[m.chat.id]['players'] and games[m.chat.id]['started']==False:
            games[m.chat.id]['players'].update(createplayer(m.from_user))
            bot.send_message(m.chat.id, m.from_user.first_name+' присоединился!')
    except:
        bot.send_message(m.chat.id, 'Тут еще нет игры ебать.')
        bot.send_message(441399484, traceback.format_exc())
        
        
@bot.message_handler(commands=['gogogo'])
def coldovattstart(m):
    try:
        if games[m.chat.id]['started']==False and len(games[m.chat.id]['players'])>1:
            games[m.chat.id]['started']=True
            bot.send_message(m.chat.id, 'ПОИХАЛИ КОЛДОВАТЬ!')
            begincoldun(m.chat.id)
        else:
            bot.send_message(m.chat.id, 'Недостаточно игроков ебланище!')
    except:
        bot.send_message(m.chat.id, 'Здесь нет игры ебать!')
        bot.send_message(441399484, traceback.format_exc())
            
    
    
def begincoldun(id):
    game=games[id]
    for ids in game['players']:
        player=game['players'][ids]
        if player['stunned']==False and player['hp']>0:
            turn(game, player)
    try:
        bot.send_message(id, game['endturntext'], parse_mode='markdown')
    except:
        bot.send_message(id, 'Нихуя не произошло!')
    for ids in game['players']:
        player=game['players'][ids]
        if player['stun']>0:
            player['stunned']=True
    game['endturntext']=''
    for ids in game['players']:
        player=game['players'][ids]
        try:
            if player['stun']>0:
                player['stun']-=1
                if player['stun']==0:
                    player['stunned']=False
        except:
            pass
    alive=0
    for ids in game['players']:
        player=game['players'][ids]
        if player['hp']>0:
            alive+=1
    if alive<=1:
        endgame(game)
    else:
        t=threading.Timer(20, begincoldun, args=[id])
        t.start()
    
def endgame(game):
    text='Игра окончена! Выжившие:\n'
    for ids in game['players']:
        player=game['players'][ids]
        if player['hp']>0:
            text+=player['name']+'\n'
    if text=='Игра окончена! Выжившие:\n':
        text+='Выживших нет! ВСЕ СДОХЛИ НАХУУУЙ!'
    bot.send_message(game['id'], text)
    del games[game['id']]
    
    
def turn(game, player):
    allcs=[]
    allcm=[]
    allce=[]
    for i in coldunstva['start']:
        print('i=')
        print(i)
        print(coldunstva['start'][i])
        allcs.append(coldunstva['start'][i])
    for i in coldunstva['mid']:
        allcm.append(coldunstva['mid'][i])
    for i in coldunstva['end']:
        allce.append(coldunstva['end'][i])
    start=random.choice(allcs)
    mid=random.choice(allcm)
    end=random.choice(allce)
    zaklinanie={
        'start':start,
        'mid':mid,
        'end':end
    }
    effecttext=''
    zakltext=''
    for ids in zaklinanie:
        print(zaklinanie)
        effecttext+=cast(zaklinanie[ids], game, player)
        zakltext+=zaklinanie[ids]['name']+' '
    game['endturntext']+='Ход игрока '+player['name']+'! Он кастует: *'+zakltext+'*! Вот, что он сделал:\n'+effecttext+'\n'
    
    
def cast(zaklinanie, game, player):
    text=''
    print(zaklinanie)
    for ids in zaklinanie:
        name=ids
    for ids in zaklinanie['effects']:
        effect=zaklinanie['effects'][ids]
        if ids=='damage':
            if effect['target']=='all':
                text+='Нанёс всем '+str(effect['amount'])+' урона!\n'
                for idss in game['players']:
                    target=game['players'][idss]
                    target['hp']-=effect['amount']
            elif effect['target']=='allenemy':
                text+='Нанёс всем своим врагам '+str(effect['amount'])+' урона!\n'
                for idss in game['players']:
                    target=game['players'][idss]
                    if target['id']!=player['id']:
                        target['hp']-=effect['amount']
                        
            elif effect['target']=='self':
                text+='Нанёс себе '+str(effect['amount'])+' урона! Точно ебланище.\n'
                player['hp']-=effect['amount']
                        
            elif 'random' in effect['target']:
                if 'enemy' not in effect['target']:
                    amount=int(effect['target'].split('random')[0])
                    i=0
                    text+='Нанес '+str(effect['amount'])+' урона колдунам:\n'
                    while i<amount:
                        ii=[]
                        for idss in game['players']:
                            ii.append(idss)
                        ii=random.choice(ii)
                        target=game['players'][ii]
                        target['hp']-=effect['amount']
                        text+=target['name']+'\n'
                        i+=1
                else:
                    amount=int(effect['target'].split('random')[0])
                    i=0
                    text+='Нанес '+str(effect['amount'])+' урона соперникам:\n'
                    while i<amount:
                        ii=[]
                        for idss in game['players']:
                            ii.append(idss)
                        ii=random.choice(ii)
                        target=game['players'][ii]
                        while target['id']==player['id']:
                            ii=[]
                            for idss in game['players']:
                                ii.append(idss)
                            ii=random.choice(ii)
                            target=game['players'][ii]
                        target['hp']-=effect['amount']
                        text+=target['name']+'\n'
                        i+=1
        if ids=='heal':
            if effect['target']=='all':
                text+='Восстановил '+str(effect['amount'])+' хп всем участникам боя!\n'
                for idss in game['players']:
                    target=game['players'][idss]
                    target['hp']+=effect['amount']
                    
            elif effect['target']=='allenemy':
                text+='Восстановил '+str(effect['amount'])+' хп всем своим врагам (непонятно, для чего. Возможно, он еблан)!\n'
                for idss in game['players']:
                    target=game['players'][idss]
                    if target['id']!=player['id']:
                        target['hp']-=effect['amount']
            
            elif effect['target']=='self':
                text+='Восстановил себе '+str(effect['amount'])+' хп!\n'
                player['hp']+=effect['amount']
                
            elif 'random' in effect['target']:
                if 'enemy' not in effect['target']:
                    amount=int(effect['target'].split('random')[0])
                    i=0
                    text+='Восстановил '+str(effect['amount'])+' хп колдунам:\n'
                    while i<amount:
                        ii=[]
                        for idss in game['players']:
                            ii.append(idss)
                        ii=random.choice(ii)
                        target=game['players'][ii]
                        target['hp']+=effect['amount']
                        text+=target['name']+'\n'
                        i+=1
                else:
                    amount=int(effect['target'].split('random')[0])
                    i=0
                    text+='Восстановил '+str(effect['amount'])+' хп соперникам:\n'
                    while i<amount:
                        ii=[]
                        for idss in game['players']:
                            ii.append(idss)
                        ii=random.choice(ii)
                        target=game['players'][ii]
                        while target['id']==player['id']:
                            ii=[]
                            for idss in game['players']:
                                ii.append(idss)
                            ii=random.choice(ii)
                            target=game['players'][ii]
                        target['hp']-=effect['amount']
                        text+=target['name']+'\n'
                        i+=1
                
        if ids=='stun':
            if effect['target']=='all':
                text+='Застанил всех игроков на '+str(effect['amount']-1)+' ходов!\n'
                for idss in game['players']:
                    target=game['players'][idss]
                    i=0
                    while i<effect['amount']:
                        target['stun']+=1
                        i+=1
                                
            elif effect['target']=='allenemy':
                text+='Застанил всех своих врагов на '+str(effect['amount']-1)+' ходов!\n'
                for idss in game['players']:
                    target=game['players'][idss]
                    if target['id']!=player['id']:
                        i=0
                        while i<effect['amount']:
                            target['stun']+=1
                            i+=1
            
            elif effect['target']=='self':
                text+='Застанил себя на '+str(effect['amount']-1)+' ходов! Ебланище.\n'
                i=0
                while i<effect['amount']:
                    player['stun']+=1
                    i+=1
                
            elif 'random' in effect['target']:
                if 'enemy' not in effect['target']:
                    amount=int(effect['target'].split('random')[0])
                    i=0
                    text+='Застанил '+str(amount)+' колдунов на '+str(effect['amount']-1)+' ходов. Пострадавшие:\n'
                    while i<amount:
                        ii=[]
                        for idss in game['players']:
                            ii.append(idss)
                        ii=random.choice(ii)
                        target=game['players'][ii]
                        target['stun']+=effect['amount']
                        text+=target['name']+'\n'
                        i+=1
                else:
                    amount=int(effect['target'].split('random')[0])
                    i=0
                    text+='Застанил '+str(amount)+' соперников на '+str(effect['amount']-1)+' ходов. Пострадавшие:\n'
                    while i<amount:
                        ii=[]
                        for idss in game['players']:
                            ii.append(idss)
                        ii=random.choice(ii)
                        target=game['players'][ii]
                        while target['id']==player['id']:
                            ii=[]
                            for idss in game['players']:
                                ii.append(idss)
                            ii=random.choice(ii)
                            target=game['players'][ii]
                        target['stun']+=effect['amount']
                        text+=target['name']+'\n'
                        i+=1
                
    return text
    
    
def creategame(chatid):
    return {chatid:{
        'id':chatid,
        'players':{},
        'started':False,
        'endturntext':''
    }}

def createplayer(user):
    return {user.id:{
        'id':user.id,
        'hp':20,
        'effects':[],
        'name':user.first_name,
        'stun':0,
        'stunned':False
    }
           }


runner = BotsRunner([792414733]) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Coldunstvo", bot)
runner.set_main_bot(bot)
print('Coldustvo works!')
runner.run()
