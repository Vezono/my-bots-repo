import os
import random

import cv2
import requests

import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['bpl'], config.creator)
from pymongo import MongoClient

db = MongoClient(config.environ['database'])
stats = db.bpl.stats
bpl_chat = -1001405019571
checking = False
laguhs = ['CAACAgIAAx0CU77lswABAURBXpnKMeC0YVdPq31zvXmeFN7H0xYAAgkAA_0jtDKK2a659YfNGBgE',
          'CAACAgIAAx0CU77lswABAUR_XpnM9Cob3c5JN9_OZUvvxmCIDsEAAiAAAw1KOy-DS40doZsPVBgE',
          'CAACAgIAAx0CU77lswABAUSKXpnNlWHVVSGctSY75-C7T7RGHtMAAk0AA7w4Txr_NCxY2aZ6DxgE']
goats_mid = ['не смог дернуть писю {}😭', 'дернул писю {}', 'оторвал писю {}', 'пощекотал писю {}', 'подрочил писю {}']
goats_end = ['Гоше', 'козе', 'Бриту', 'Пасюку', 'Полунину', 'МНЕ', 'ослу', 'Шмэку']


@bot.message_handler(commands=['help'])
def help_handler(m):
    bot.send_message(m.chat.id, """Я типичный бплщик, привет!
/laguh - кинуть лягушку
/pisya - дернуть писю козе
/cheking - переключить чекер
/top_laguh - посмотреть топ лягушатников
/help - показать это сообщение (ебать логика уровня Аскольда)""")


@bot.message_handler(commands=['cheking'])
def cheking_handler(m):
    global checking
    checking = not checking
    bot.reply_to(m, f'чекинг теперь {checking}')


@bot.message_handler(commands=['laguh'])
def laguh_handler(m):
    reply_to = None
    if m.reply_to_message:
        reply_to = m.reply_to_message.message_id
    bot.send_sticker(m.chat.id, laguhs[0], reply_to_message_id=reply_to)


@bot.message_handler(commands=['pisya'])
def pisya_handler(m):
    goat = random.choice(goats_mid).format(random.choice(goats_end))
    tts = f'{m.from_user.first_name} {goat}!'
    bot.send_message(m.chat.id, tts)


@bot.message_handler(content_types=['sticker'])
def lagushka_handler(m):
    if m.chat.id != bpl_chat:
        return
    file_url = bot.get_file_url(m.sticker.thumb.file_id)
    r = requests.get(file_url)
    with open('res/jaba_compare.jpg', 'wb') as fd:
        for chunk in r.iter_content():
            fd.write(chunk)
    hash1 = CalcImageHash("res/jaba.jpg")
    hash2 = CalcImageHash("res/jaba_compare.jpg")
    os.remove('res/jaba_compare.jpg')
    diff = CompareHash(hash1, hash2)
    if diff == 0:
        try:
            x = stats.find_one({})[str(m.from_user.id)]
            stats.update_one({}, {'$inc': {str(m.from_user.id): 1}})
        except:
            stats.update_one({}, {'$set': {str(m.from_user.id): 1}})
    if checking:
        bot.reply_to(m, f'Расхождение стикера с лягушкой - {diff}')


@bot.message_handler(commands=['top_laguh'])
def top_laguh_handler(m):
    top = stats.find_one({})
    tts = 'Топ лягушатников:\n'
    for user in top:
        if user == '_id':
            continue
        name = 'Брит'
        if user != '512006137':
            name = bot.get_chat_member(bpl_chat, str(user)).user.first_name
        tts += f'{name} - {top[user]} лягушек\n'
    bot.reply_to(m, tts)


# Функция вычисления хэша
def CalcImageHash(FileName):
    image = cv2.imread(FileName)  # Прочитаем картинку
    resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
    avg = gray_image.mean()  # Среднее значение пикселя
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу

    # Рассчитаем хэш
    _hash = ""
    for x in range(8):
        for y in range(8):
            val = threshold_image[x, y]
            if val == 255:
                _hash = _hash + "1"
            else:
                _hash = _hash + "0"

    return _hash


def CompareHash(hash1, hash2):
    l = len(hash1)
    i = 0
    count = 0
    while i < l:
        if hash1[i] != hash2[i]:
            count = count + 1
        i = i + 1
    return count
