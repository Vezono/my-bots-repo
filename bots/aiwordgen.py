import os
import telebot
import time
import random
import threading
from manybotslib import BotsRunner
from telebot import types
from pymongo import MongoClient
import traceback
admin = 792414733

token = os.environ['aiwordgen']
bot = telebot.TeleBot(token)


client=MongoClient(os.environ['database'])
db=client.aiwordgen
words=db.words
twowords=0
allw={}

endsymbols=['!', '.', '?', ')']


@bot.message_handler(commands=['adddict'])
def adddict(m):
    if m.from_user.id==admin:
        words.update_one({},{'$set':{'words2':{}}})
        bot.send_message(admin, 'yes')
    
@bot.message_handler(commands=['story'])
def story(m):
    if True:
        try:
            sentences=random.randint(1,3)
            try:
                sentences=int(m.text.split(' ')[1])
            except:
                pass
            csent=0
            ctext=''
            global allw
            allwords=allw
            global twowords
            if twowords==1:
                dic='words2'
            else:
                dic='words'
            while csent<sentences:
                cword=0
                currentword=''
                while '&end' not in currentword:
                    start=None
                    if cword==0:
                        if twowords==0:
                            start=allwords[dic]['&start']
                        else:
                            for idss in allwords[dic]:
                                if '&start' in idss:
                                    start=allwords[dic][idss]
                        items=[]
                        for ids in start:
                            i=0
                            try:
                                while i<start[ids]: 
                                    items.append(ids)
                                    i+=1
                            except:
                                pass
                        start=random.choice(items)
                        i=0
                        cwd=''
                        currentword=start
                        
                        st=0
                        for a in start:
                            if i==0 and a.isupper()==False and st==0:
                                if a!='@':
                                    cwd+=a.upper()
                            else:
                                if a!='@':
                                    cwd+=a
                            st+=1
                        start=cwd
                        ctext+=start+' '
                    else:
                        nextwords=[]
                        for ids in allwords[dic][currentword]:
                            i=0
                           
                             
                            while i<allwords[dic][currentword][ids]:
                                    nextwords.append(ids)
                                    i+=1
                            
                        nextword=random.choice(nextwords)
                        if currentword[len(currentword)-1] in endsymbols:
                            endsent=1
                        else:
                            endsent=0
                        currentword=nextword
                        
                        if '&end' not in nextword:
                            i=0
                            cwd=''
                            for a in nextword:
                                if a!='@':
                                    cwd+=a
                            ctext+=cwd+' '
                        else:
                            if endsent==0:
                                if twowords==1:
                                    ctext=ctext[:len(ctext)-5]
                                else: 
                                    ctext=ctext[:len(ctext)-1]
                                ctext+='.'
                        
                    cword+=1
                csent+=1
                ctext+=' '
            bot.send_message(m.chat.id, ctext)
        except Exception as e:
            bot.send_message(admin, traceback.format_exc())
            


@bot.message_handler()
def addword(m):
    global twowords
    if m.from_user.id!=m.chat.id:
        try:
            if m.text[0]!='/' and m.text[0]!="@":
                toupdate={}
                allword=words.find_one({})
                textwords=m.text.split(' ')
                i=0
                for ids in textwords:
                  if ids not in endsymbols:
                    currentword=ids
                    if twowords==1:
                        try:
                            currentword=ids+' '+textwords[i+1]
                        except:
                            currentword+=ids+' '+'&end'
                    if currentword=='&start':
                        currentword='start'
                    if i==0:
                        fixids=currentword
                        while fixids[len(fixids)-1]==".":
                            fixids=fixids[:len(fixids)-1]
                        if "." not in fixids:
                            toupdate.update({'&start':{fixids:1}})
                    end=False
                    try:
                        nextword=textwords[i+1]
                        if twowords==1:
                            try:
                                nextword=textwords[i+2]+' '+textwords[i+3]
                            except:
                                nextword=textwords[i+2]+' '+'&end'
                                end=True
                    except:
                        nextword='&end'
                        end=True
                    if '&end' in nextword and end==False:
                        nextword='end'
                    try:
                        if currentword[len(currentword)-1] in endsymbols:
                            nextword='&end'
                    except Exception as e:
                        bot.send_message(admin, traceback.format_exc())
                    try:
                        while currentword[len(currentword)-1] == '.':
                            currentword=currentword[:len(currentword)-1]
                    except Exception as e:
                        bot.send_message(admin, traceback.format_exc())
                    try:
                        while nextword[len(nextword)-1]==".":
                            nextword=nextword[:len(nextword)-1]
                    except Exception as e:
                        bot.send_message(admin, traceback.format_exc())
                    if currentword not in toupdate:     
                        if "." not in currentword and "." not in nextword:
                            toupdate.update({currentword:{nextword:1}})
                    else:
                        if nextword not in toupdate[currentword]:
                            if "." not in currentword and "." not in nextword:
                                toupdate[currentword].update({nextword:1})
                        else:
                            
                            toupdate[currentword][nextword]+=1
                    i+=1
                
                if twowords==1:
                    dic='words2'
                else:
                    dic='words'
                for ids in toupdate:
                    if ids not in allword[dic]:
                        for idss in toupdate[ids]:
                            if isinstance(toupdate[ids][idss], int):
                                words.update_one({},{'$set':{dic+'.'+str(ids)+'.'+str(idss):toupdate[ids][idss]}})
                    else:
                        for idss in toupdate[ids]:
                            if idss not in allword['words'][ids]:
                                if isinstance(toupdate[ids][idss], int):
                                    words.update_one({},{'$set':{dic+'.'+str(ids)+'.'+str(idss):toupdate[ids][idss]}})
                            else:
                                if isinstance(toupdate[ids][idss], int):
                                    words.update_one({},{'$inc':{dic+'.'+str(ids)+'.'+str(idss):toupdate[ids][idss]}})
                     
        except Exception as e:
            bot.send_message(admin, traceback.format_exc())
            
        
def reload():
    t=threading.Timer(3600, reload)
    t.start()
    global allw
    allw=words.find_one({})
    
reload() 
   

print('Aiwordgen works!')
runner = BotsRunner([admin]) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Aiwordgen", bot)
runner.set_main_bot(bot)
runner.run()
