import telebot
import time
import random
import threading
from telebot import types
from pymongo import MongoClient
import traceback

def hostloshod(test):
    token = '587282753:AAHHyjXezDjRy7osT_JmR9raPay0CwbXRRY'
    bot = telebot.TeleBot(token)
    print('Launching "loshadkin.py"...')
    exec(open("loshadkin.py").read())
    
def hostgbball(test):
    token = '765563788:AAFnkelmaKJkalYOAJsU0fTrexErKOnl5No'
    bot = telebot.TeleBot(token)
    print('Launching "gbball.py"...')
    exec(open("gbball.py").read())    
threading.Timer(1,hostloshod,args=['test']).start()
threading.Timer(1,hostgbball,args=['test']).start()
threading.Timer(2,print,args=['All apps launched!']).start() 
