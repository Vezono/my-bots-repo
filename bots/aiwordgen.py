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
@bot.message_handler(commands=['reload'])
def adddict(m):
    if m.from_user.id==admin:
        reload()

@bot.message_handler(commands=['adddict'])
def adddict(m):
    if m.from_user.id==admin:
        words.insert_one({'words':{}})
        words.update_one({},{'$set':{'words2':{}}})
        words.update_one({},{'$set':{'words':{}}})
        bot.send_message(admin, 'yes')
def generate(sentences):
    global allw
    allwords = allw
    ctext = ''
    csent = 0
    dic = 'words'
    for i in range(sentences):
        cword = 0
        current_word = ''
        while '&end' not in current_word:
            start = None
            if not cword:
                start = allwords[dic]['&start']
                items = []
                for ids in start:
                    for a in range(start[ids]):
                        items.append(ids)
                start = random.choice(items)
                i = 0
                cwd = ''
                current_word = start.capitalize()
                ctext += start + ' '
            else:
                next_words = []
                for ids in allwords[dic][current_word]:
                    for count_of_word in range(allwords[dic][current_word][ids]):
                        next_words.append(ids)
                next_word = random.choice(next_words)
                endsent = 0
                if current_word[-1] in endsymbols:
                    endsent = 1
                current_word = next_word
                if '&end' not in next_word:
                    i = 0
                    cwd = ''
                    for a in next_word:
                        if a != '@':
                            cwd += a
                    ctext += cwd + ' '
                else:
                    if endsent == 0:
                        ctext = ctext[:len(ctext) - 1]
                        ctext += '.'
            cword += 1
        csent += 1
        ctext += ' '
    return ctext        
@bot.message_handler(commands=['story'])
def story(m):
    try:
        bot.send_message(admin, generate(random.randint(1, 3)))      
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
