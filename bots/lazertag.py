import os
import telebot
import random
import threading
from telebot import types
from pymongo import MongoClient
import traceback
from modules.manybotslib import BotsRunner

token = os.environ['lazertag']
bot = telebot.TeleBot(token)


client=MongoClient(os.environ['database'])
db=client.lazertag
users=db.users
admin = 792414733
games=[]

@bot.message_handler(commands=['help'])
def help(m):
    bot.send_message(m.chat.id, '''Правила игры: 
Игроки делятся на команды. У каждого игрока есть три варианта хода - атака, защита, и перезарядка лазера
Максимальное значение атаки - 20
Каждый раз, когда вы атакуете, вы тратите заряд лазера.
Каждый раз, когда вы защищаетесь, вы тратите заряд щита.
Чтобы восстановить заряд лазера, нажмите перезарядка лазера (восстановит 25%).
Чтобы восстановить заряд щита, выберите меню щита, и выставьте защиту в минус. Нельзя выставить защиту меньше, чем 40%. Если в этот ход по вам попали, то вы получите урон = урон из лазеров + заряд щита, так что не стоит восстанавливать слишком большие значения.
Побеждает команда, которая выживет.''')

@bot.message_handler(commands=['start'])
def start(m):
   x=users.find_one({'id':m.from_user.id})
   if x==None:
      users.insert_one(createuser(m.from_user.id,m.from_user.first_name,m.from_user.username))
      bot.send_message(m.chat.id, m.from_user.first_name+', приветствую в игре "Лазертаг"! Цель этой игры - остаться единственной '+
                       'живой командой в игре! Подробности по команде /help.')
     

@bot.message_handler(commands=['preparegame'])
def preparegame(m):
    no=0
    for ids in games:
        if ids['id']==m.chat.id:
            no=1
            game=ids
    if no==0:
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Сменить команду', callback_data='teamchoice'))
        msg=bot.send_message(m.chat.id, 'Начинаем сбор игроков! Жмите /tagjoin для вступления в игру.',reply_markup=kb)
        games.append(creategame(m.chat.id,msg))
        for ids in games:
            if ids['id']==m.chat.id:
                yes=1
                game=ids
        t=threading.Timer(300,cancelgame,args=[game])
        t.start()
        game['canceltimer']=t
    else:
        try:
            medit('Список игроков ниже.',game['message'].chat.id,game['message'].message_id)
        except:
            pass
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Сменить команду', callback_data='teamchoice'))
        msg=bot.send_message(m.chat.id, editmessage(game),reply_markup=kb)
        game['message']=msg
        

@bot.message_handler(commands=['tagjoin'])
def tagjoin(m):
    game=None
    yes=0
    for ids in games:
        if ids['id']==m.chat.id:
            yes=1
            game=ids
    if game!=None:
        if game['started']==0:
            if yes==1:
                allplayers=[]
                no=0
                for ids in game['teams']:
                    for idss in ids['players']:
                        if idss['id']==m.from_user.id:
                            no=1
                if no==0:
                    try:
                        x=createplayer(m.from_user.id)
                        bot.send_message(m.from_user.id, 'Вы успешно присоединились!')
                        bot.send_message(m.chat.id, m.from_user.first_name+' присоединился к игре!')
                        game['teams'].append(createteam(game))
                        game['teams'][len(game['teams'])-1]['players'].append(x)
                        kb=types.InlineKeyboardMarkup()
                        kb.add(types.InlineKeyboardButton(text='Сменить команду', callback_data='teamchoice'))
                        medit(editmessage(game),game['message'].chat.id,game['message'].message_id,reply_markup=kb)
                    except:
                        bot.send_message(m.chat.id, 'Сначала напишите /start боту @Lazertagg_bot в личку!')
                else:
                    bot.send_message(m.chat.id, m.from_user.first_name+', вы уже в игре!')
        else:
            bot.send_message(m.chat.id, 'Игра уже началась!')
        
     
@bot.message_handler(commands=['tagstart'])
def tagstart(m):
    yes=0
    for ids in games:
        if ids['id']==m.chat.id:
            yes=1
            game=ids
    if yes==1:
        if len(game['teams'])>1:
            if game['started']==0:
                game['canceltimer'].cancel()
                game['started']=1
                t=threading.Timer(60,endturn,args=[game])
                t.start()
                game['timer']=t
                startgame(game)
        else:
            bot.send_message(m.chat.id, 'Недостаточно команд!')
    else:
        bot.send_message(m.chat.id, 'Нет запущенной игры! Нажмите /preparegame для сбора игроков.')
            
            
@bot.callback_query_handler(func=lambda call:True)
def inline(call): 
    if 'fight' in call.data:
        kb=types.InlineKeyboardMarkup()
        game=None
        player=None
        chat=call.data.split(' ')[2]
        for ids in games:
            if ids['id']==int(chat):
                game=ids
        if game!=None:
            for ids in game['teams']:
                for idss in ids['players']:
                    if idss['id']==call.from_user.id and 'ready' not in idss['effects']:
                        player=idss
        if player!=None:
            if 'shoot' in call.data:
                for ids in game['teams']:
                    if ids['id']!=player['team']:
                        for idss in ids['players']:
                            if idss['dead']!=1:
                                kb.add(types.InlineKeyboardButton(text='💢'+idss['name'],callback_data='fight target '+chat+' '+str(idss['id'])))
                kb.add(types.InlineKeyboardButton(text='Назад',callback_data='fight back1 '+chat))
                medit('Выберите цель.',player['message'].chat.id,player['message'].message_id,reply_markup=kb)
            
            if 'back1' in call.data:
                sendmenu(player,game,player['team'])
                
            if 'def' in call.data:
                s=[1,5,10]
                s2=[20,30,40]
                m=[-1,-5,-10]
                m2=[-20,-30,-40]
                d=[]
                d2=[]
                b=[]
                b2=[]
                for ids in s:
                    b.append(types.InlineKeyboardButton(text='🔵+'+str(ids)+'%',callback_data='fight def1 '+chat+' '+str(ids)))
                for ids in s2:
                    b2.append(types.InlineKeyboardButton(text='🔵+'+str(ids)+'%',callback_data='fight def1 '+chat+' '+str(ids)))
                for ids in m:
                    d.append(types.InlineKeyboardButton(text='🔵'+str(ids)+'%',callback_data='fight def1 '+chat+' '+str(ids)))
                for ids in m2:
                    d2.append(types.InlineKeyboardButton(text='🔵'+str(ids)+'%',callback_data='fight def1 '+chat+' '+str(ids)))
                kb.add(b[0],b[1],b[2])
                kb.add(b2[0],b2[1],b2[2])
                kb.add(d[0],d[1],d[2])
                kb.add(d2[0],d2[1],d2[2])
                if 'def1' in call.data:
                    x=int(call.data.split(' ')[3])
                    player['currentdef']+=x
                    if player['currentdef']>player['shield']:
                        player['currentdef']=player['shield']
                        bot.answer_callback_query(call.id, 'У вас не хватает мощности щита!')
                    if player['currentdef']<-40:
                        player['currentdef']=-40
                        bot.answer_callback_query(call.id, 'Нельзя зарядить более 40% щита за ход!')
                if player['currentdef']<0:
                    txt='⚡️Зарядить щит'
                else:
                    txt='🔵Защита!'
                kb.add(types.InlineKeyboardButton(text=txt,callback_data='fight shield '+chat))
                kb.add(types.InlineKeyboardButton(text='Отмена.',callback_data='fight back1 '+chat))
                medit('Выберите мощность щита. Текущая мощность: '+str(player['currentdef'])+'%',player['message'].chat.id,player['message'].message_id,reply_markup=kb)
                
            if 'shield' in call.data:
                player['ready']=1
                if player['currentdef']<0:
                    txt='Вы заряжаете свой щит.'
                else:
                    txt='Вы приготовились защищаться от лазеров.'
                player['action']='def'
                medit(txt+' Ждите окончания хода.',player['message'].chat.id,player['message'].message_id)
                player['message']=None
                check(game)
                
                
            if 'target' in call.data:
                target=call.data.split(' ')[3]
                s=[1,5,10]
                s2=[20,30,40]
                m=[-1,-5,-10]
                m2=[-20,-30,-40]
                d=[]
                d2=[]
                b=[]
                b2=[]
                for ids in s:
                    b.append(types.InlineKeyboardButton(text='🔴+'+str(ids)+'%',callback_data='fight target1 '+chat+' '+str(target)+' '+str(ids)))
                for ids in s2:
                    b2.append(types.InlineKeyboardButton(text='🔴+'+str(ids)+'%',callback_data='fight target1 '+chat+' '+str(target)+' '+str(ids)))
                for ids in m:
                    d.append(types.InlineKeyboardButton(text='🔴'+str(ids)+'%',callback_data='fight target1 '+chat+' '+str(target)+' '+str(ids)))
                for ids in m2:
                    d2.append(types.InlineKeyboardButton(text='🔴'+str(ids)+'%',callback_data='fight target1 '+chat+' '+str(target)+' '+str(ids)))
                kb.add(b[0],b[1],b[2])
                kb.add(b2[0],b2[1],b2[2])
                kb.add(d[0],d[1],d[2])
                kb.add(d2[0],d2[1],d2[2])
                kb.add(types.InlineKeyboardButton(text='Огонь!',callback_data='fight fire '+chat+' '+target))
                kb.add(types.InlineKeyboardButton(text='Отмена.',callback_data='fight back1 '+chat))
                if 'target1' in call.data:
                    x=int(call.data.split(' ')[4])
                    player['currentcharge']+=x
                    if player['currentcharge']>40:
                        player['currentcharge']=40
                        bot.answer_callback_query(call.id, 'Нельзя выставить мощности больше, чем 40%!')
                    if player['currentcharge']<0:
                        player['currentcharge']=0
                        bot.answer_callback_query(call.id, 'Нельзя выставить мощности меньше, чем 0%!')
                    if player['currentcharge']>player['lazer']:
                        player['currentcharge']=player['lazer']
                        bot.answer_callback_query(call.id, 'Не хватает мощности лазера!')
                medit('Выберите силу заряда. Текущая сила: '+str(player['currentcharge'])+'%',player['message'].chat.id,player['message'].message_id,reply_markup=kb)
                
            if 'fire' in call.data:
                enemy=None
                target=call.data.split(' ')[3]
                for ids in game['teams']:
                    for idss in ids['players']:
                        if idss['id']==int(target):
                            enemy=idss
                if enemy!=None:
                    player['ready']=1
                    player['target']=enemy
                    player['action']='attack'
                    medit('Вы направляете свой лазер на '+enemy['name']+'... Ждите окончания хода.',player['message'].chat.id,player['message'].message_id)
                    player['message']=None
                    check(game)
                else:
                    bot.answer_callback_query(call.id, 'В этой игре нет такого игрока!')
             
            if 'reloadgun' in call.data:
                player['ready']=1
                player['action']='reload'
                medit('Вы заряжаете лазер! Ждите окончания хода.',player['message'].chat.id,player['message'].message_id)
                player['message']=None
                check(game)
                    
                
def check(game):
    no=0
    for ids in game['teams']:
        for idss in ids['players']:
            if idss['dead']==0 and idss['ready']==0:
                no=1
    if no==0:
        endturn(game)

                
def endturn(game):
  try:
    try:
        game['timer'].cancel()
    except:
        pass
    for ids in game['teams']:
        for idss in ids['players']:
            if idss['message']!=None:
                if 'afk' in idss['effects']:
                    idss['dead']=1
                    game['res']+=idss['name']+' умер от АФК!\n'
                idss['effects'].append('afk')
                medit('Время вышло!',idss['message'].chat.id,idss['message'].message_id)
                idss['message']=None
            else:
                try:
                    idss['effects'].remove('afk')
                except:
                    pass
            if idss['ready']==1:
                action(idss)
    for ids in game['teams']:
        for idss in ids['players']:
            if idss['action']=='attack':
                if idss['takendmg']<=0:
                    game['res']+='🔴|'+idss['name']+' заряжает лазер на '+str(idss['currentcharge'])+'% и стреляет в '+idss['target']['name']+'!\n'
                else:
                    idss['hp']-=idss['takendmg']
                    game['res']+='🔴💔|'+idss['name']+' заряжает лазер на '+str(idss['currentcharge'])+'% и стреляет в '+idss['target']['name']+', '+\
                    'но тоже попадает под огонь! Потеряно '+str(idss['takendmg'])+'% хп.\n'
                
    for ids in game['teams']:
        for idss in ids['players']:
            if idss['action']=='def' and 'dead' not in idss['effects']:
                if idss['currentdef']<0:
                    if idss['takendmg']>0:
                        idss['takendmg']-=idss['currentdef']
                        idss['hp']-=idss['takendmg']
                        game['res']+='🔋💔|'+idss['name']+' зарядил '+str(idss['currentdef']-(2*idss['currentdef']))+'% щита и потерял '+str(idss['takendmg'])+'% хп!\n'
                    else:
                        game['res']+='🔋|'+idss['name']+' зарядил '+str(idss['currentdef']-(2*idss['currentdef']))+'% щита!\n'
                else:
                    if idss['currentdef']>=idss['takendmg']:
                        l=int(idss['takendmg']/2)
                        idss['lazer']+=l
                        idss['shield']-=idss['currentdef']
                        game['res']+='🔵|'+idss['name']+' блокирует весь входящий урон ('+str(idss['takendmg'])+')! Потеряно '+str(idss['currentdef'])+'% заряда щита; '+\
                        'восстановлено '+str(l)+'% энергии лазера!\n'
                    else:
                        l=int(idss['currentdef']/3)
                        idss['lazer']+=l
                        idss['shield']-=idss['currentdef']
                        idss['takendmg']-=idss['currentdef']
                        idss['hp']-=idss['takendmg']
                        game['res']+='🔵💔|'+idss['name']+' тратит '+str(idss['currentdef'])+'% щита, но блокирует не весь входящий урон! Потеряно '+str(idss['takendmg'])+'% хп; '+\
                        'восстановлено '+str(l)+'% энергии лазера!\n'
    for ids in game['teams']:
        for idss in ids['players']:
            if idss['action']=='reload' and 'dead' not in idss['effects']:
                if idss['takendmg']>0:
                    idss['hp']-=idss['takendmg']
                    game['res']+='🔋💔|'+idss['name']+' восстанавливает 25% лазера, но попадает под огонь! Потеряно '+str(idss['takendmg'])+'% хп.\n'
                else:
                    game['res']+='🔋|'+idss['name']+' восстанавливает 25% лазера!\n'
                    
    for ids in game['teams']:
        for idss in ids['players']:
            if idss['action']==None and 'dead' not in idss['effects']:
                if idss['takendmg']>0:
                    idss['hp']-=idss['takendmg']
                    game['res']+='😴💔|'+idss['name']+' пропускает ход и подставляется под лазер! Потеряно '+str(idss['takendmg'])+'% хп.\n'
                else:
                    game['res']+='😴|'+idss['name']+' пропускает ход, и не теряет ни одного хп!\n'
                    
    for ids in game['teams']:
        for idss in ids['players']:
            idss['ready']=0
            idss['currentdef']=0
            idss['currentcharge']=0
            idss['action']=None
            idss['target']=None
            idss['takendmg']=0
            if idss['lazer']>idss['maxlazer']:
                idss['lazer']=idss['maxlazer']
                game['res2']+='⚡️🔴|'+idss['name']+' теряет лишний заряд лазера.\n'
            if idss['shield']>idss['maxshield']:
                idss['shield']=idss['maxshield']
                game['res2']+='⚡️🔵|'+idss['name']+' теряет лишний заряд щита.\n'
    for ids in game['teams']:
        for idss in ids['players']:
            if idss['hp']<=0 or (idss['lazer']<=0 and idss['shield']<=0):
              if 'dead' not in idss['effects']:
                idss['dead']=1
                game['res2']+='☠️|'+idss['name']+' погибает.\n'
                idss['effects'].append('dead')
    aliveteams=[]
    for ids in game['teams']:
        for idss in ids['players']:
            if idss['dead']==0 and idss['team'] not in aliveteams:
                aliveteams.append(idss['team'])
    bot.send_message(game['id'],game['res'])
    bot.send_message(game['id'],game['res2'])
    for ids in game['teams']:
        for idss in ids['players']:
            if idss['dead']!=1:
                bot.send_message(idss['id'],game['res'])
                bot.send_message(idss['id'],game['res2'])
    if len(aliveteams)>1:
        for ids in game['teams']:
            for idss in ids['players']:
                if idss['dead']!=1:
                    sendmenu(idss,game,idss['team'])
        game['turn']+=1
        game['res']='Результаты хода '+str(game['turn'])+':\n'
        game['res2']='Итоги хода:\n'
        t=threading.Timer(60,endturn,args=[game])
        t.start()
        game['timer']=t
    elif len(aliveteams)==1:
        tm=None
        for ids in game['teams']:
            if ids['id']==aliveteams[0]:
                tm=ids
        txt=''
        for ids in tm['players']:
            if ids['dead']==0:
                txt+=ids['name']+'\n'
        bot.send_message(game['id'],'Команда '+aliveteams[0]+' победила! Выжившие участники команды:\n'+txt)
        games.remove(game)
    else:
        bot.send_message(game['id'],'Все команды проиграли!')
        games.remove(game)
        
  except Exception as e:
    print('Ошибка:\n', traceback.format_exc())
    bot.send_message(admin, traceback.format_exc())
    games.remove(game)
    bot.send_message(game['id'],'Произошла ошибка! Игра была удалена.')


def action(player):
    if player['action']=='attack':
        target=player['target']
        target['takendmg']+=player['currentcharge']
        player['lazer']-=player['currentcharge']
    elif player['action']=='def':
        if player['currentdef']<0:
            player['shield']-=player['currentdef']
    elif player['action']=='reload':
        player['lazer']+=25
    
                
def startgame(game):
    for ids in game['teams']:
        team=ids['id']
        for idss in ids['players']:
            idss['team']=team
    for ids in game['teams']:
        for idss in ids['players']:
            sendmenu(idss,game,idss['team'])
    bot.send_message(game['id'],'Начинаем перестрелку! Приготовьте свои лазер-пушки и энергетические щиты и переключайтесь в личку бота!')
            
    
def sendmenu(player,game,team):
    text='Ваша команда:\n\n'
    for ids in game['teams']:
        if ids['id']==team:
            team=ids
    for ids in team['players']:
        text+=ids['name']+':\n'+'♥️:'+str(ids['hp'])+'%, 🔵:'+str(ids['shield'])+'%, 🔴:'+str(ids['lazer'])+'%\n\n'
    kb=types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='🔴Стрельба', callback_data='fight shoot '+str(game['id'])),types.InlineKeyboardButton(text='🔵Защита', callback_data='fight def '+str(game['id'])))
    kb.add(types.InlineKeyboardButton(text='🔋Зарядить лазер',callback_data='fight reloadgun '+str(game['id'])))
    if player['message']==None:
        msg=bot.send_message(player['id'],text+'Выберите действие.',reply_markup=kb)
        player['message']=msg
    else:
        medit(text+'Выберите действие.',player['message'].chat.id,player['message'].message_id,reply_markup=kb)
    
    
    
def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)  


def editmessage(game):
    text='Начинаем сбор игроков! Жмите /tagjoin для вступления в игру.\n\n'
    if game['started']==1:
        text='Игра уже идёт!\n\n'
    for ids in game['teams']:
        t=ids
        text+='Команда '+t['name']+':\n'
        i=0
        for idss in t['players']:
            player=idss
            if i!=len(t['players'])-1:
                symbol='┞'
            else:
                symbol='┕'
            text+=symbol+player['name']+'\n'
            i+=1
        text+='\n'
    return text
        

def randomgen(teams):
    allids=[]
    for ids in teams:
        allids.append(ids['id'])
    i=0
    x=''
    while i<3:
        i=random.randint(0,9)
        x+=str(i)
        i+=1
    while x in allids:
        x=''
        i=0
        while i<3:
            i=random.randint(0,9)
            x+=str(i)
            i+=1
    return x
    
def cancelgame(game):
    try:
        games.remove(game)
        bot.send_message(game['id'],'Игра была отменена!')
    except:
        pass
    

def createplayer(id):
    x=users.find_one({'id':id})
    if x!=None:
        return x
        
def createteam(game):
    id=randomgen(game['teams'])
    return {
        'id':id,            #id тут str, не int!
        'players':[],
        'name':id
    }
        
def creategame(id,message):
   return {
      'id':id,
      'teams':[],
      'turn':1,
      'started':0,
      'message':message,
      'res':'Результаты хода 1:\n',
      'res2':'Итоги хода:\n',
      'timer':None,
      'canceltimer':None
   }

def createdamager(player,damage):
    return {
        'id':player['id'],
        'damage':damage
    }

def createuser(id,name,username):
   return {
      'id':id,
      'name':name,
      'username':username,
      'dead':0,
      'shield':100,
      'maxshield':100,
      'lazer':100,
      'maxlazer':100,
      'maxcharge':20,
      'currentdef':0,
      'hp':100,
      'maxhp':100,
      'takendmg':0,
      'restturns':0,
      'effects':[],
      'ready':0,
      'team':None,
      'action':None,
      'target':None,
      'message':None,
      'damagers':[],
      'currentcharge':0
   }
print('Lazertag works!')
runner = BotsRunner() # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Lazertag", bot)
runner.set_main_bot(bot)
runner.run()
