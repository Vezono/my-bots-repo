# -*- coding: utf-8 -*-

import json
import random
import re
import threading
import time

import apiai
from pymongo import MongoClient

from .olga_dmitrievna import *
from .world import *

alisa = telebot.TeleBot(os.environ['alisa'])
miku = telebot.TeleBot(os.environ['miku'])
lena = telebot.TeleBot(os.environ['lena'])
slavya = telebot.TeleBot(os.environ['slavya'])
uliana = telebot.TeleBot(os.environ['uliana'])
electronic = telebot.TeleBot(os.environ['electronic'])
zhenya = telebot.TeleBot(os.environ['zhenya'])
tolik = telebot.TeleBot(os.environ['tolik'])
shurik = telebot.TeleBot(os.environ['shurik'])
semen = telebot.TeleBot(os.environ['semen'])
pioneer = telebot.TeleBot(os.environ['pioneer'])
yuriy = telebot.TeleBot(os.environ['yuriy'])
alexandr = telebot.TeleBot(os.environ['alexandr'])
vladislav = telebot.TeleBot(os.environ['vladislav'])
samanta = telebot.TeleBot(os.environ['samanta'])
vasiliyhait = telebot.TeleBot(os.environ['vasiliyhait'])
viola = telebot.TeleBot(os.environ['viola'])
yuliya = telebot.TeleBot(os.environ['yuliya'])
evillena = telebot.TeleBot(os.environ['evillena'])
monster = telebot.TeleBot(os.environ['monster'])
sayori = telebot.TeleBot(os.environ['sayori'])
yuri = telebot.TeleBot(os.environ['yuri'])
monika = telebot.TeleBot(os.environ['monika'])
natsuki = telebot.TeleBot(os.environ['natsuki'])

pioner_prefixes = {
    'жен': zhenya,
    'мик': miku,
    'али': alisa,
    'од': olga,
    'лен': lena,
    'сла': slavya,
    'уль': uliana,
    'эле': electronic,
    'тол': tolik,
    'шур': shurik,
    'сем': semen,
    'пио': pioneer,
    'але': miku,
    'вла': vladislav,
    'сам': samanta,
    'евл': evillena,
    'улм': monster
}

client = MongoClient(os.environ['database'])
db = client.everlastingsummer
users = db.users
thunder = db.thunder
thunder_variables = db.thunder_variables
ban = db.ban
cday = db.cday
ctime_rp = db.ctime
admins = db.admins

if not ctime_rp.find_one({}):
    ctime_rp.insert_one({'ctime_rp': times[0]})

if not cday.find_one({}):
    cday.insert_one({'cday': 1})


def neiro(m, pioner):
    if not neiro_on:
        return
    if pioner != alisa:
        return
    if not m.reply_to_message or 'алиса' not in m.text.lower():
        return
    if m.reply_to_message.from_user.id != alisa.get_me().id:
        return
    if m.from_user.id != m.chat.id:
        return
    req = apiai.ApiAI(os.environ['apiai_alisa']).text_request()
    req.lang = 'ru'
    req.session_id = 'Alisa_id'
    req.query = m.text
    responseJson = json.loads(req.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    if 'paren' in responseJson['result']['parameters']:
        if 'парень' in responseJson['result']['parameters']['paren']:
            response = 'Ну... У меня нет парня.'
        elif 'парнем' in responseJson['result']['parameters']['paren']:
            response = 'Мило... Я подумаю.'
    if not response:
        txt = random.choice(['Я тебя не понимаю! Говори понятнее!', 'Прости, не понимаю тебя.', 'Я тебя не поняла!'])
        pioner.send_message(m.chat.id, txt, reply_to_message_id=m.message_id)
        return
    pioner.send_message(m.chat.id, response)


def createadmin(pioner, user_id=creator):
    return {
        pioner: [user_id],
        'name': pioner,
        'controller': None
    }


if not admins.find_one({'name': 'evl_admins'}):
    admins.insert_one(createadmin('evl_admins', 496583701))

if not admins.find_one({'name': 'mns_admins'}):
    admins.insert_one(createadmin('mns_admins', 496583701))

if not admins.find_one({'name': 'sayori_admins'}):
    admins.insert_one(createadmin('sayori_admins'))

if not admins.find_one({'name': 'yuri_admins'}):
    admins.insert_one(createadmin('yuri_admins'))

if not admins.find_one({'name': 'natsuki_admins'}):
    admins.insert_one(createadmin('natsuki_admins'))

if not admins.find_one({'name': 'monika_admins'}):
    admins.insert_one(createadmin('monika_admins'))


def createban(id):
    return {
        'id': id
    }


if ban.find_one({'id': 617640951}) == None:
    ban.insert_one(createban(617640951))


def worktoquest(work_code):
    work_descs = {
        'concertready': 'Подготовиться к вечернему концерту',
        'sortmedicaments': 'Отсортировать лекарства в медпункте',
        'checkpionerssleeping': 'На вечер - проследить за тем, чтобы в 10 часов все были в домиках',
        'pickberrys': 'Собрать ягоды для торта',
        'bringfoodtokitchen': 'Принести на кухню нужные ингридиенты',
        'helpinmedpunkt': 'Последить за медпунктом, пока медсестры не будет',
        'helpinkitchen': 'Помочь с приготовлением еды на кухне',
        'cleanterritory': 'Подмести территорию лагеря',
        'washgenda': 'Помыть памятник на главной площади'

    }
    return work_descs.get(work_code)


def lvlsort(x):
    return [ids['name'] for ids in works if ids['lvl'] == x and not ids['value']]


def statfind(pioner):
    stats = None
    if pioner == uliana:
        stats = 'ul_admins'
    if pioner == lena:
        stats = 'le_admins'
    if pioner == tolik:
        stats = 'to_admins'
    if pioner == alisa:
        stats = 'al_admins'
    if pioner == olga:
        stats = 'od_admins'
    if pioner == zhenya:
        stats = 'zh_admins'
    if pioner == shurik:
        stats = 'sh_admins'
    if pioner == electronic:
        stats = 'el_admins'
    if pioner == slavya:
        stats = 'sl_admins'
    if pioner == miku:
        stats = 'mi_admins'
    if pioner == pioneer:
        stats = 'pi_admins'
    if pioner == semen:
        stats = 'se_admins'
    if pioner == yuriy:
        stats = 'yu_admins'
    if pioner == alexandr:
        stats = 'ale_admins'
    if pioner == vladislav:
        stats = 'vl_admins'
    if pioner == samanta:
        stats = 'sa_admins'
    if pioner == vasiliyhait:
        stats = 'va_admins'
    if pioner == viola:
        stats = 'vi_admins'
    if pioner == yuliya:
        stats = 'yul_admins'
    if pioner == monster:
        stats = 'mns_admins'
    if pioner == evillena:
        stats = 'evl_admins'
    if pioner == sayori:
        stats = 'sayori_admins'
    if pioner == monika:
        stats = 'monika_admins'
    if pioner == natsuki:
        stats = 'natsuki_admins'
    if pioner == yuri:
        stats = 'yuri_admins'
    return stats


def stickhandler(m, pioner):
    if ban.find_one({'id': m.from_user.id}):
        return
    stats = statfind(pioner)

    adm = admins.find_one({'name': stats})
    if not adm['controller']:
        return
    controller = adm['controller']
    if m.from_user.id != controller['id']:
        return
    if not m.reply_to_message:
        try:
            olga.delete_message(m.chat.id, m.message_id)
        except:
            try:
                monika.delete_message(m.chat.id, m.message_id)
            except:
                pass
        pioner.send_sticker(m.chat.id, m.sticker.file_id)
    else:
        try:
            olga.delete_message(m.chat.id, m.message_id)
        except:
            try:
                monika.delete_message(m.chat.id, m.message_id)
            except:
                pass
        pioner.send_sticker(m.chat.id, m.sticker.file_id, reply_to_message_id=m.reply_to_message.message_id)


def pichandler(m, pioner):
    if ban.find_one({'id': m.from_user.id}):
        return
    stats = statfind(pioner)

    adm = admins.find_one({'name': stats})
    if not adm['controller']:
        return
    controller = adm['controller']
    if m.from_user.id != controller['id']:
        return
    if not m.reply_to_message:
        try:
            olga.delete_message(m.chat.id, m.message_id)
        except:
            try:
                monika.delete_message(m.chat.id, m.message_id)
            except:
                pass
        if m.caption:
            pioner.send_photo(m.chat.id, m.photo[0].file_id, caption=m.caption)
        else:
            pioner.send_photo(m.chat.id, m.photo[0].file_id)
    else:
        try:
            olga.delete_message(m.chat.id, m.message_id)
        except:
            try:
                monika.delete_message(m.chat.id, m.message_id)
            except:
                pass
        if m.caption:
            pioner.send_photo(m.chat.id, m.photo[0].file_id, caption=m.caption,
                              reply_to_message_id=m.reply_to_message.message_id)
        else:
            pioner.send_photo(m.chat.id, m.photo[0].file_id,
                              reply_to_message_id=m.reply_to_message.message_id)


def audiohandler(m, pioner):
    if ban.find_one({'id': m.from_user.id}) == None:
        olga.send_message(creator, 'audeo')
        stats = statfind(pioner)

        adm = admins.find_one({'name': stats})
        if adm['controller'] != None:
            controller = adm['controller']
            if m.from_user.id == controller['id']:
                if m.reply_to_message == None:
                    try:
                        olga.delete_message(m.chat.id, m.message_id)
                    except:
                        try:
                            monika.delete_message(m.chat.id, m.message_id)
                        except:
                            pass
                    try:
                        pioner.send_audio(m.chat.id, m.audio.file_id)
                    except:
                        pioner.send_voice(m.chat.id, m.voice.file_id)
                else:
                    try:
                        olga.delete_message(m.chat.id, m.message_id)
                    except:
                        try:
                            monika.delete_message(m.chat.id, m.message_id)
                        except:
                            pass
                    try:
                        pioner.send_audio(m.chat.id, m.audio.file_id, reply_to_message_id=m.reply_to_message.message_id)
                    except:
                        pioner.send_voice(m.chat.id, m.voice.file_id, reply_to_message_id=m.reply_to_message.message_id)


def msghandler(m, pioner):
    if ban.find_one({'id': m.from_user.id}):
        return
    stats = statfind(pioner)
    text = None
    if m.text[0] == '/':
        pioner2 = None
        for prefix in pioner_prefixes:
            if m.text.startswith(f'/{prefix}'):
                pioner2 = pioner_prefixes[prefix]
                break
        if not pioner2 or pioner != pioner2:
            return
        else:
            text = m.text.split(' ', 1)[1]
    adm = admins.find_one({'name': stats})
    if not adm['controller']:
        # neiro(m, pioner)
        return
    controller = adm['controller']
    if m.from_user.id != controller['id']:
        return
    if not m.reply_to_message:
        try:
            olga.delete_message(chat_id=m.chat.id, message_id=m.message_id)
        except:
            try:
                monika.delete_message(m.chat.id, m.message_id)
            except:
                pass
        if text != None:
            tosend = text
        else:
            tosend = m.text
        msg = pioner.send_message(m.chat.id, tosend)
    else:
        try:
            try:
                olga.delete_message(m.chat.id, m.message_id)
            except:
                try:
                    monika.delete_message(m.chat.id, m.message_id)
                except:
                    pass
            pioner.send_message(m.chat.id, m.text, reply_to_message_id=m.reply_to_message.message_id)

        except:
            olga.send_message(creator, traceback.format_exc())


@olga.message_handler(commands=['allinfo'])
def allinfoaboutp(m):
    try:
        x = users.find({})
        text = ''
        text2 = ''
        text3 = ''
        for ids in x:
            if len(text) <= 1000:
                try:
                    text += ids['pionername'] + ' ' + '(' + ids['name'] + ')' + ' `' + str(ids['id']) + '`\n'
                except:
                    text += '(' + ids['name'] + ')' + ' `' + str(ids['id']) + '`\n'
            elif len(text2) <= 1000:
                try:
                    text2 += ids['pionername'] + ' ' + '(' + ids['name'] + ')' + ' `' + str(ids['id']) + '`\n'
                except:
                    text2 += '(' + ids['name'] + ')' + ' `' + str(ids['id']) + '`\n'
        olga.send_message(creator, text, parse_mode='markdown')
        if text2 != '':
            olga.send_message(creator, text2, parse_mode='markdown')
    except:
        olga.send_message(creator, traceback.format_exc())


@olga.message_handler(commands=['start'])
def start(m):
    if m.chat.id == m.from_user.id and ban.find_one({'id': m.from_user.id}) == None:
        x = users.find_one({'id': m.from_user.id})
        if x == None:
            users.insert_one(createuser(m.from_user.id, m.from_user.first_name, m.from_user.username))
            olga.send_chat_action(mainchat, 'typing')
            time.sleep(4)
            olga.send_message(m.chat.id,
                              'Здраствуй, пионер! Меня зовут Ольга Дмитриевна, я буду твоей вожатой. Впереди тебя ждёт интересная жизнь в лагере "Совёнок"! ' +
                              'А сейчас скажи нам, как тебя зовут (следующим сообщением).')
        else:
            if x['setgender'] == 0 and x['setname'] == 0:
                x = users.find_one({'id': m.from_user.id})
                olga.send_chat_action(m.chat.id, 'typing')
                time.sleep(4)
                if x['working'] == 1:
                    olga.send_message(m.chat.id, 'Здраствуй, пионер! Вижу, ты занят. Молодец! Не буду отвлекать.')
                else:
                    olga.send_message(m.chat.id, 'Здраствуй, пионер! Отдыхаешь? Могу найти для тебя занятие!')


@olga.message_handler(commands=['pioner'])
def pinfo(m):
    if m.from_user.id == creator:
        try:
            x = users.find_one({'id': m.reply_to_message.from_user.id})
            if x != None:
                text = ''
                for ids in x:
                    text += ids + ': ' + str(x[ids]) + '\n'
                olga.send_message(creator, text)
        except:
            olga.send_message(creator, traceback.format_exc())


@olga.message_handler(commands=['work'])
def work(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        global rds
        x = users.find_one({'id': m.from_user.id})
        if x != None and rds == True:
            if x['setgender'] == 0 and x['setname'] == 0:
                if x['working'] == 0:
                    if x['waitforwork'] == 0:
                        if x['relaxing'] == 0:
                            users.update_one({'id': m.from_user.id}, {'$set': {'waitforwork': 1}})
                            olga.send_chat_action(m.chat.id, 'typing')
                            time.sleep(4)
                            olga.send_message(m.chat.id, random.choice(worktexts), reply_to_message_id=m.message_id)
                            t = threading.Timer(random.randint(60, 120), givework, args=[m.from_user.id])
                            t.start()
                        else:
                            olga.send_chat_action(m.chat.id, 'typing')
                            time.sleep(4)
                            olga.send_message(m.chat.id,
                                              'Нельзя так часто работать! Хвалю, конечно, за трудолюбивость, но сначала отдохни.',
                                              reply_to_message_id=m.message_id)


def givework(id):
    nosend = 0
    x = users.find_one({'id': id})
    if x != None:
        try:
            text = ''
            if x['gender'] == 'male':
                gndr = ''
            if x['gender'] == 'female':
                gndr = 'а'
            quests = lvlsort(1)
            sendto = types.ForceReply(selective=False)

            quest = None
            olga.send_chat_action(id, 'typing')
            time.sleep(4)
            if x['OlgaDmitrievna_respect'] >= 75:
                lvl1quests = lvlsort(1)
                text += 'Так как ты у нас ответственный пионер, [' + x['pionername'] + '](tg://user?id=' + str(
                    id) + '), у меня для тебя есть важное задание!\n'
                if len(lvl1quests) > 0:
                    quest = random.choice(lvl1quests)
                    users.update_one({'id': id}, {'$set': {'prepareto': quest}})
                    print('Юзер готовится к квесту: ' + quest)
                    users.update_one({'id': id}, {'$set': {'answering': 1}})
                    t = threading.Timer(60, cancelquest, args=[id])
                    t.start()
                else:
                    text = 'Важных заданий на данный момент нет, [' + x['pionername'] + '](tg://user?id=' + str(
                        id) + ')... Но ничего, обычная работа почти всегда найдётся!\n'
                    questt = []
                    quest2 = lvlsort(2)
                    quest3 = lvlsort(3)
                    for ids in quest2:
                        questt.append(ids)
                    for ids in quest3:
                        questt.append(ids)
                    if len(questt) > 0:
                        quest = random.choice(questt)
                        print('Юзер готовится к квесту: ' + quest)
                        users.update_one({'id': id}, {'$set': {'prepareto': quest}})
                        users.update_one({'id': id}, {'$set': {'answering': 1}})
                    else:
                        nosend = 1
                        olga.send_message(mainchat, 'К сожалению, заданий для тебя сейчас нет, [' + x[
                            'pionername'] + '](tg://user?id=' + str(id) + '). Но за желание помочь лагерю хвалю!',
                                          parse_mode='markdown')
                        users.update_one({'id': id}, {'$set': {'waitforwork': 0}})
            elif x['OlgaDmitrievna_respect'] >= 40:
                text += 'Нашла для тебя занятие, [' + x['pionername'] + '](tg://user?id=' + str(id) + ')!\n'
                lvl2quests = lvlsort(2)
                if len(lvl2quests) > 0:
                    quest = random.choice(lvl2quests)
                    sendto = types.ForceReply(selective=False)
                    users.update_one({'id': id}, {'$set': {'prepareto': quest}})
                    users.update_one({'id': id}, {'$set': {'answering': 1}})
                    print('Юзер готовится к квесту: ' + quest)
                    t = threading.Timer(60, cancelquest, args=[id])
                    t.start()
                else:
                    lvl3quests = lvlsort(3)
                    if len(lvl3quests) > 0:
                        quest = random.choice(lvl3quests)
                        sendto = types.ForceReply(selective=False)
                        print('Юзер готовится к квесту: ' + quest)
                        users.update_one({'id': id}, {'$set': {'prepareto': quest}})
                        users.update_one({'id': id}, {'$set': {'answering': 1}})
                        t = threading.Timer(60, cancelquest, args=[id])
                        t.start()
                    else:
                        nosend = 1
                        olga.send_message(mainchat, 'К сожалению, заданий для тебя сейчас нет, [' + x[
                            'pionername'] + '](tg://user?id=' + str(id) + '). Но за желание помочь лагерю хвалю!',
                                          parse_mode='markdown')
                        users.update_one({'id': id}, {'$set': {'waitforwork': 0}})

            else:
                text += 'Ответственные задания я тебе пока что доверить не могу, [' + x[
                    'pionername'] + '](tg://user?id=' + str(
                    id) + '). Чтобы вырастить из тебя образцового пионера, начнем с малого.\n'
                lvl3quests = lvlsort(3)
                if len(lvl3quests) > 0:
                    quest = random.choice(lvl3quests)
                    sendto = types.ForceReply(selective=False)
                    users.update_one({'id': id}, {'$set': {'prepareto': quest}})
                    print('Юзер готовится к квесту: ' + quest)
                    users.update_one({'id': id}, {'$set': {'answering': 1}})
                    t = threading.Timer(60, cancelquest, args=[id])
                    t.start()
                else:
                    nosend = 1
                    olga.send_message(mainchat, 'К сожалению, заданий для тебя сейчас нет, [' + x[
                        'pionername'] + '](tg://user?id=' + str(id) + '). Но за желание помочь лагерю хвалю!',
                                      parse_mode='markdown')
            if quest == 'pickberrys':
                text += 'Собери-ка ягоды для вечернего торта! Ты готов, пионер?'
            if quest == 'bringfoodtokitchen':
                text += 'На кухне не хватает продуктов. Посети библиотеку, кружок кибернетиков и медпункт, там должны быть некоторые ингридиенты. Справишься?'
            if quest == 'washgenda':
                if x['gender'] == 'female':
                    gndr = 'ла'
                text += f'Наш памятник на главной площади совсем запылился. Не мог{gndr} бы ты помыть его?'
            if quest == 'cleanterritory':
                text += 'Территория лагеря всегда должна быть в чистоте! Возьми веник и совок, и подмети здесь всё. Справишься?'
            if quest == 'concertready':
                text += 'Тебе нужно подготовить сцену для сегодняшнего выступления: принести декорации и аппаратуру, которые нужны выступающим пионерам, выровнять стулья. Приступишь?'
            if quest == 'sortmedicaments':
                text += 'Тебе нужно помочь медсестре: отсортировать привезённые недавно лекарства по ящикам и полкам. Возьмёшься?'
            if quest == 'checkpionerssleeping':
                text += 'Уже вечер, и все пионеры должны в это время ложиться спать. Пройдись по лагерю и поторопи гуляющих. Готов' + gndr + '?'
            if quest == 'helpinmedpunkt':
                text += 'Медсестре нужна твоя помощь: ей срочно нужно в райцентр. Посидишь в медпункте за неё?'
            if quest == 'helpinkitchen':
                gndr2 = ''
                if x['gender'] == 'female':
                    gndr = 'а'
                    gndr2 = 'ла'
                text += 'На кухне не хватает людей! Было бы хорошо, если бы ты помог' + gndr2 + ' им с приготовлением. Готов' + gndr + '?'
            if nosend == 0:
                users.update_one({'id': id}, {'$set': {'answering': 1}})
                olga.send_message(mainchat, text, parse_mode='markdown')
        except:
            olga.send_message(creator, traceback.format_exc())


def cancelquest(id):
    x = users.find_one({'id': id})
    if not x:
        return
    if x['answering'] != 1:
        return
    users.update_one({'id': id}, {'$set': {'prepareto': None}})
    users.update_one({'id': id}, {'$set': {'answering': 0}})
    users.update_one({'id': id}, {'$set': {'waitforwork': 0}})
    olga.send_message(mainchat,
                      f'[{x["pionername"]}](tg://user?id={id})! '
                      f'Почему не отвечаешь? Неприлично, знаешь ли. '
                      f'Ну, раз не хочешь, найду другого пионера для этой работы.',
                      parse_mode='markdown')
    users.update_one({'id': id}, {'$inc': {'OlgaDmitrievna_respect': -4}})


@olga.message_handler(commands=['cards'])
def gamestestdsdfsdgd(m):
    if rds and electronicstats['waitingplayers'] != 1:
        eveninggames()


####################################### OLGA ##############################################
@olga.message_handler(commands=['control'])
def odcontrol(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        adm = admins.find_one({'name': 'od_admins'})
        if m.from_user.id in adm['od_admins']:
            if adm['controller'] == None:
                admins.update_one({'name': 'od_admins'}, {'$set': {'controller': {'id': m.from_user.id,
                                                                                  'name': m.from_user.first_name}}})
                olga.send_message(m.from_user.id,
                                  'Здравствуй, пионер. Быть вожатым - большая ответственность! Не опозорь меня!')
            else:
                olga.send_message(m.from_user.id, 'Мной уже управляют!')


@olga.message_handler(commands=['stopcontrol'])
def odstopcontrol(m):
    x = 'od_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            olga.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@olga.message_handler(content_types=['sticker'])
def stickercatchod(m):
    if m.from_user.id == creator:
        olga.send_message(creator, m.sticker.file_id)
    stickhandler(m, olga)


@olga.message_handler(content_types=['photo'])
def photocatchod(m):
    pichandler(m, olga)


@olga.message_handler(content_types=['audio'])
@olga.message_handler(content_types=['voice'])
def photocatchod(m):
    audiohandler(m, olga)


@olga.message_handler()
def messag(m):
    if ban.find_one({'id': m.from_user.id}):
        return
    if m.chat.type == 'private':
        user = users.find_one({'id': m.from_user.id})
        if user:
            if user['setname'] == 1:
                correct_name = re.search('^[a-z,A-Z,а-я,А-Я]*$', m.text)
                if correct_name:
                    users.update_one({'id': m.from_user.id}, {'$set': {'pionername': m.text}})
                    users.update_one({'id': m.from_user.id}, {'$set': {'setname': 0}})
                    olga.send_message(m.chat.id,
                                      'Отлично! И еще одна просьба... Прости конечно, но это нужно для документа, в котором ' +
                                      'хранится информация обо всех пионерах. Я, конечно, сама вижу, но это надо сделать твоей рукой. ' +
                                      'Напиши вот тут свой пол (М или Д).')
                else:
                    olga.send_message(m.chat.id,
                                      'Нет-нет! Имя может содержать только буквы русского и английского алфавита!')
            else:
                if user['setgender'] == 1:
                    if m.text.lower() in ['м', 'д']:
                        users.update_one({'id': m.from_user.id}, {'$set': {'setgender': 0}})
                        users.update_one({'id': m.from_user.id},
                                         {'$set': {'gender': {'м': 'male', 'д': 'female'}[m.text.lower()]}})
                        olga.send_message(m.chat.id,
                                          f'Добро пожаловать в лагерь, {user["pionername"]}! Заходи в '
                                          f'@everlastingsummerchat, и знакомься с остальными пионерами!')
    else:
        user = users.find_one({'id': m.from_user.id})
        if not user:
            return
        if user['setgender']:
            return
        if m.reply_to_message != None:
            if m.reply_to_message.from_user.id == 636658457:
                if user['answering'] == 1:
                    if m.text.lower() in yestexts:
                        users.update_one({'id': m.from_user.id}, {'$set': {'answering': 0}})
                        users.update_one({'id': m.from_user.id}, {'$set': {'working': 1}})
                        users.update_one({'id': m.from_user.id}, {'$set': {'waitforwork': 0}})
                        dowork(m.from_user.id)
                        users.update_one({'id': m.from_user.id}, {'$set': {'prepareto': None}})
                        olga.send_message(m.chat.id, 'Молодец, пионер! Как закончишь - сообщи мне.',
                                          reply_to_message_id=m.message_id)
        lineykatexts = ['я здесь', 'я тута', 'я пришёл', 'я пришла', 'я пришел']
        if odstats['waitforlineyka'] == 1:
            for lineykatext in lineykatexts:
                if lineykatext in m.text.lower():
                    if user['gender'] == 'male':
                        g = 'шёл'
                    else:
                        g = 'шла'
                    pioner_link = f'[{user["pionername"]}](tg://user?id={user["id"]})'
                    odstats['lineyka'].append(pioner_link)
                    olga.send_message(m.chat.id, f'А вот и {pioner_link} при{g} на линейку!')
                    break
    msghandler(m, olga)


def reloadquest(index):
    works[index]['value'] = 0
    print('Квест ' + works[index]['name'] + ' обновлён!')


def dowork(user_id):
    user = users.find_one({'id': user_id})
    i = 0
    index = None
    for ids in works:
        if user['prepareto'] == ids['name']:
            index = i
        i += 1
    if index != None:
        works[index]['value'] = 1
        z = None
        if works[index]['name'] == 'sortmedicaments':
            z = random.randint(3600, 7200)
        if works[index]['name'] == 'pickberrys':
            z = random.randint(7200, 9200)
        if works[index]['name'] == 'bringfoodtokitchen':
            z = random.randint(2200, 3600)
        if works[index]['name'] == 'helpmedpunkt':
            z = random.randint(7200, 10200)
        if works[index]['name'] == 'cleanterritory' or works[index]['name'] == 'washgenda':
            z = random.randint(900, 2700)
        if z:
            threading.Timer(z, reloadquest, args=[index]).start()
        threading.Timer(300, endwork, args=[user_id, works[index]['name']]).start()


def endwork(id, work):
    t = threading.Timer(180, relax, args=[id])
    t.start()
    x = users.find_one({'id': id})
    users.update_one({'id': id}, {'$set': {'working': 0}})
    users.update_one({'id': id}, {'$set': {'relaxing': 1}})
    strenght = 0
    agility = 0
    intelligence = 0
    if x['gender'] == 'female':
        gndr = 'а'
    else:
        gndr = ''
    text = 'Ты хорошо поработал' + gndr + '! Улучшенные характеристики:\n'
    if work == 'sortmedicaments':
        agility = random.randint(0, 2)
        strenght = random.randint(1, 100)
        if strenght <= 15:
            strenght = 1
        else:
            strenght = 0
        intelligence = random.randint(1, 100)
        if intelligence <= 10:
            intelligence = 1
        else:
            intelligence = 0
    if work == 'pickberrys':
        strenght = random.randint(0, 2)
        agility = random.randint(1, 100)
        if agility <= 50:
            agility = random.randint(0, 2)
        else:
            agility = 0
    if work == 'bringfoodtokitchen':
        strenght = random.randint(1, 2)
        agility = random.randint(1, 100)
        if agility <= 30:
            agility = random.randint(1, 2)
        else:
            agility = 0
    if work == 'helpmedpunkt':
        intelligence = random.randint(2, 3)
        strenght = random.randint(1, 100)
        if strenght <= 35:
            strenght = random.randint(1, 2)
        else:
            strenght = 0
        agility = random.randint(1, 100)
        if agility <= 5:
            agility = 1
        else:
            agility = 0
    if work == 'cleanterritory' or work == 'washgenda':
        strenght = random.randint(0, 2)
        agility = random.randint(0, 1)
    if work == 'checkpionerssleeping':
        agility = random.randint(1, 2)
        intelligence = random.randint(1, 100)
        if intelligence <= 40:
            intelligence = random.randint(0, 2)
        else:
            intelligence = 0
    if work == 'concertready' or work == 'checkpionerssleeping' or work == 'helpinmedpunkt':
        agility = 3
        intelligence = 4
        strenght = 3
    if work == 'helpinkitchen':
        agility = random.randint(1, 2)
        intelligence = 1
        strenght = random.randint(0, 1)
    if agility > 0:
        text += '*Ловкость*\n'
    if strenght > 0:
        text += '*Сила*\n'
    if intelligence > 0:
        text += '*Интеллект*\n'
    if text == 'Ты хорошо поработал' + gndr + '! Улучшенные характеристики:\n':
        text = 'Физических улучшений не заметно, но ты заслужил' + gndr + ' уважение вожатой!'
    users.update_one({'id': id}, {'$inc': {'strenght': strenght}})
    users.update_one({'id': id}, {'$inc': {'agility': agility}})
    users.update_one({'id': id}, {'$inc': {'intelligence': intelligence}})
    olga.send_message(mainchat, 'Отличная работа, [' + x['pionername'] + '](tg://user?id=' + str(
        id) + ')! Теперь можешь отдохнуть.', parse_mode='markdown')
    users.update_one({'id': id}, {'$inc': {'OlgaDmitrievna_respect': 1}})
    try:
        world.send_message(id, text, parse_mode='markdown')
    except:
        world.send_message(mainchat,
                           '[' + x['pionername'] + '](tg://user?id=' + str(id) + ')' + random.choice(worldtexts) + text,
                           parse_mode='markdown')


def relax(id):
    users.update_one({'id': id}, {'$set': {'relaxing': 0}})


def createuser(id, name, username):
    return {'id': id,
            'name': name,
            'username': username,
            'pionername': None,
            'gender': None,
            'popularity': 1,
            'strenght': 3,
            'agility': 3,
            'intelligence': 3,
            'prepareto': None,
            'setname': 1,
            'setgender': 1,
            'waitforwork': 0,
            'respect': 50,
            'working': 0,
            'relaxing': 0,
            'answering': 0,
            'busy': [],
            'OlgaDmitrievna_respect': 50,
            'Slavya_respect': 50,
            'Uliana_respect': 50,
            'Alisa_respect': 50,
            'Lena_respect': 50,
            'Electronic_respect': 50,
            'Miku_respect': 50,
            'Zhenya_respect': 50,
            'helping': 0

            }


def gettime(t):
    x = time.ctime()
    x = x.split(" ")
    for ids in x:
        for idss in ids:
            if idss == ':':
                tru = ids
    x = tru
    x = x.split(":")
    minute = int(x[1])
    hour = int(x[0]) + 3
    if t == 'h':
        return hour
    elif t == 'm':
        return minute


def checktime():
    t = threading.Timer(60, checktime)
    t.start()
    hour = gettime('h')
    minute = gettime('m')
    if hour == 17 and minute == 0:
        x = findindex('concertready')
        works[x]['value'] = 0
    if hour == 21 and minute == 30:
        x = findindex('checkpionerssleeping')
        works[x]['value'] = 0
    if (hour == 8 and minute == 10) or (hour == 13 and minute == 0) or (hour == 20 and minute == 30):
        x = findindex('helpinkitchen')
        works[x]['value'] = 0
    if (hour == 19 and minute == 0):
        cardplayers = []
        eveninggames()
    if (hour == 7 and minute == 0):
        odstats['waitforlineyka'] = 1
        olga.send_chat_action(mainchat, 'typing')
        time.sleep(3)
        olga.send_message(mainchat, 'Доброе утро, пионеры! В 7:30 жду всех на линейке!')
    if (hour == 7 and minute == 30):
        odstats['waitforlineyka'] = 0
        olga.send_chat_action(mainchat, 'typing')
        time.sleep(3)
        olga.send_message(mainchat, 'Здраствуйте, пионеры! Сейчас проведём перекличку...')
        olga.send_chat_action(mainchat, 'typing')
        time.sleep(4)
        text = ''
        for ids in odstats['lineyka']:
            text += ids + '\n'
        olga.send_message(mainchat, text + '\nВот все, кто сегодня пришёл. Молодцы, пионеры! Так держать!' + \
                          'Сейчас расскажу о планах на день.', parse_mode='markdown')
    global nowrp
    if nowrp:
        if (hour == 9 and minute == 0):
            for ids in rpchats:
                try:
                    world.send_message(ids, '*Сигнал, оповещающий о начале завтрака*', parse_mode='markdown')
                except:
                    pass
        if (hour == 14 and minute == 0):
            for ids in rpchats:
                try:
                    world.send_message(ids, '*Сигнал, оповещающий о начале обеда*', parse_mode='markdown')
                except:
                    pass
        if (hour == 21 and minute == 0):
            for ids in rpchats:
                try:
                    world.send_message(ids, '*Сигнал, оповещающий о начале ужина*', parse_mode='markdown')
                except:
                    pass


zavtrak = '9:00'
obed = '14:00'
uzhin = '21:00'


def eveninggames():
    global rds
    if rds:
        egames = ['cards']  # ,'ropepulling']
        x = random.choice(egames)
        if x == 'cards':
            electronicstats['waitingplayers'] = 1
            leader = 'electronic'
            olga.send_chat_action(mainchat, 'typing')
            t = threading.Timer(3.5, sendmes, args=[olga,
                                                    'Уже 7 вечера, а это значит, что пора начинать наши вечерние игры! На сегодня ' + \
                                                    'у нас по плану придуманная Электроником карточная игра. [Электроник](https://t.me/ES_ElectronicBot), ' + \
                                                    'дальше расскажешь ты.', 'markdown'])
            t.start()
            time.sleep(4.5)
            electronic.send_chat_action(mainchat, 'typing')
            t = threading.Timer(2, sendmes, args=[electronic, 'Есть, Ольга Дмитриевна!', None])
            t.start()
            t = threading.Timer(2.1, sendstick, args=[electronic, 'CAADAgAD1QADgi0zDyFh2eUTYDzzAg'])
            t.start()
            time.sleep(4)
            electronic.send_chat_action(mainchat, 'typing')
            t = threading.Timer(10, sendmes, args=[electronic,
                                                   'Итак. Правила игры просты: надо выиграть, собрав на руке более сильную ' + \
                                                   'комбинацию, чем у соперника. Процесс игры заключается в том, что соперники поочереди ' + \
                                                   'забирают друг у друга карты. Делается это так: в свой ход вы выбираете одну из карт соперника, ' + \
                                                   'а он после этого может поменять любые 2 карты в своей руке местами. Вы эту перестановку ' + \
                                                   'видите, и после его действия можете изменить свой выбор. А можете не менять. ' + \
                                                   'Так повторяется 3 раза, и вы забираете последнюю карту, которую выберите. Затем ' + \
                                                   'такой же ход повторяется со стороны соперника. Всего каждый участник делает 3 хода, ' + \
                                                   'и после этого оба игрока вскрываются...', None])
            t.start()
            time.sleep(4)
            electronic.send_chat_action(mainchat, 'typing')
            time.sleep(4)
            electronic.send_chat_action(mainchat, 'typing')
            time.sleep(4)
            electronic.send_chat_action(mainchat, 'typing')
            t = threading.Timer(5, sendmes,
                                args=[electronic, 'Что смешного? Ладно, неважно. Все поняли правила? Отлично! Для ' + \
                                      'регистрации в турнире нужно подойти ко мне, и сказать: "`Хочу принять участие в турнире!`". ' + \
                                      'Регистрация заканчивается через 20 минут!', 'markdown'])
            t.start()
            t = threading.Timer(300, starttournier, args=['cards'])
            t.start()

        elif x == 'football':
            leader = 'uliana'
            olga.send_chat_action(mainchat, 'typing')
            t = threading.Timer(3.5, sendmes, args=[olga,
                                                    'Уже 7 вечера, а это значит, что пора начинать наши вечерние игры! На сегодня ' + \
                                                    'у нас по плану футбол! [Ульяна](https://t.me/ES_UlianaBot), ' + \
                                                    'расскажет вам про правила проведения турнира.', 'markdown'])
            t.start()
            time.sleep(4.5)
            uliana.send_chat_action(mainchat, 'typing')
            t = threading.Timer(2, sendmes, args=[uliana, 'Так точно, Ольга Дмитриевна!', None])
            t.start()
            t = threading.Timer(2.1, sendstick, args=[uliana, 'CAADAgADKQADgi0zD_inNy0pZyh0Ag'])
            t.start()
            time.sleep(4)
            uliana.send_chat_action(mainchat, 'typing')
            t = threading.Timer(5, sendmes, args=[uliana, 'Правила просты - не жульничать! Для записи на турнир ' + \
                                                  'подойдите ко мне и скажите "`Хочу участвовать!`". Вроде бы всё... Жду всех!',
                                                  'markdown'])
            t.start()
        elif x == 'ropepulling':
            leader = 'alisa'


setka = []


def starttournier(game):
    try:
        if game == 'cards':
            global cardplayers
            global setka
            newplayers = ['miku', 'slavya', 'zhenya', 'alisa', 'lena', 'uliana']
            specialrules = 0
            i = 0
            for ids in cardplayers:
                i += 1
            if i % 2 == 0:
                if i >= 10:
                    prm = 16
                elif i > 0:
                    prm = 8
                else:
                    prm = 0
            else:
                if i == 1:
                    prm = 4
                elif i == 3 or i == 5 or i == 7:
                    prm = 8
                elif i == 9:
                    prm = 12
                    specialrules = 1
            g = 0
            if prm > 0:
                while g < (prm - i):
                    randomplayer = random.choice(newplayers)
                    cardplayers.append(randomplayer)
                    newplayers.remove(randomplayer)
                    g += 1
                text = ''
                i = 0
                h = len(cardplayers)
                while i < (h / 2):
                    player1 = random.choice(cardplayers)
                    cardplayers.remove(player1)
                    player2 = random.choice(cardplayers)
                    cardplayers.remove(player2)
                    setka.append([player1, player2])
                    i += 1
                for ids in setka:
                    text += '\n\n'
                    vs = ' VS '
                    for idss in ids:
                        try:
                            int(idss)
                            x = users.find_one({'id': idss})
                            text += '[' + x['pionername'] + '](tg://user?id=' + str(x['id']) + ')' + vs
                        except:
                            text += nametopioner(idss) + vs
                        vs = ''
                electronic.send_chat_action(mainchat, 'typing')
                time.sleep(5)
                electronic.send_message(mainchat,
                                        'Ну что, все в сборе? Тогда вот вам турнирная сетка на первый этап:\n' + text,
                                        parse_mode='markdown')
                time.sleep(1.5)
                electronic.send_chat_action(mainchat, 'typing')
                time.sleep(3)
                electronic.send_message(mainchat,
                                        'А теперь прошу к столам! Каждый садится со своим соперником. Через 2 минуты начинается ' +
                                        'первый этап!')
                electronicstats['cardsturn'] = 1
                t = threading.Timer(120, cards_nextturn)
                t.start()
                for ids in setka:
                    i = 0
                    for idss in ids:
                        try:
                            int(idss)
                            i += 1
                        except:
                            if i == 0:
                                index = 1
                            elif i == 1:
                                index = 0
                            try:
                                int(ids[index])
                                talkwithplayer(ids[index], idss)
                            except:
                                pass
            else:
                electronic.send_message(mainchat,
                                        'К сожалению, игроков для турнира сегодня не набралось. Ну ничего, в следующий раз попробуем!')
    except:
        setka = []
        cardplayers = []
        electronicstats['waitingplayers'] = 0
        electronicstats['playingcards'] = 0
        electronicstats['cardsturn'] = 0
        electronic.send_message(mainchat, 'Непредвиденные обстоятельства! Турнир придётся отменить!')


def cards_nextturn():
    try:
        global setka
        global cardplayers
        for ab in setka:
            cardplayers.append(ab[0])
            cardplayers.append(ab[1])
        if len(cardplayers) > 0:
            print(setka)
            print(cardplayers)
            for ids in setka:
                i = -1
                print(ids)
                for idss in ids:
                    print(idss)
                    i += 1
                    if i < 2:
                        try:
                            print('try1')
                            int(ids[0])
                            if i == 0:
                                index = 1
                            else:
                                index = 0
                            try:
                                print('try2')
                                int(ids[index])
                                player1 = users.find_one({'id': ids[0]})
                                player2 = users.find_one({'id': ids[1]})
                                r = player1['intelligence'] - player2['intelligence']
                                r = r / 2
                                x = random.randint(1, 100)
                                if x <= (50 + r):
                                    cardplayers.remove(player2['id'])
                                else:
                                    cardplayers.remove(player1['id'])
                                i = 10
                                print('try2complete')

                            except:
                                coef = 0
                                user = users.find_one({'id': ids[1]})
                                if user != None:
                                    coef += user['intelligence']
                                if ids[index] == 'miku':
                                    intelligence = mikustats['intelligence']
                                if ids[index] == 'alisa':
                                    intelligence = alisastats['intelligence']
                                if ids[index] == 'lena':
                                    intelligence = lenastats['intelligence']
                                if ids[index] == 'slavya':
                                    intelligence = slavyastats['intelligence']
                                if ids[index] == 'zhenya':
                                    intelligence = zhenyastats['intelligence']
                                if ids[index] == 'uliana':
                                    intelligence = ulianastats['intelligence']
                                if intelligence == 1:
                                    x = 80 + coef
                                if intelligence == 2:
                                    x = 60 + coef
                                if intelligence == 3:
                                    x = 40 + coef
                                if intelligence == 4:
                                    x = 20 + coef
                                if x >= 90:
                                    x = 90
                                if random.randint(1, 100) <= x:
                                    cardplayers.remove(ids[1])
                                else:
                                    cardplayers.remove(ids[0])
                                i = 10

                        except:
                            try:
                                print('try3')
                                int(ids[1])
                                index = 0
                                coef = 0
                                user = users.find_one({'id': ids[1]})
                                if user != None:
                                    coef += user['intelligence']
                                if ids[index] == 'miku':
                                    intelligence = mikustats['intelligence']
                                if ids[index] == 'alisa':
                                    intelligence = alisastats['intelligence']
                                if ids[index] == 'lena':
                                    intelligence = lenastats['intelligence']
                                if ids[index] == 'slavya':
                                    intelligence = slavyastats['intelligence']
                                if ids[index] == 'zhenya':
                                    intelligence = zhenyastats['intelligence']
                                if ids[index] == 'uliana':
                                    intelligence = ulianastats['intelligence']
                                if intelligence == 1:
                                    x = 75 + coef
                                if intelligence == 2:
                                    x = 60 + coef
                                if intelligence == 3:
                                    x = 40 + coef
                                if intelligence == 4:
                                    x = 20 + coef
                                if x >= 90:
                                    x = 90
                                if random.randint(1, 100) <= x:
                                    cardplayers.remove(ids[0])
                                else:
                                    cardplayers.remove(ids[1])
                                i = 10

                            except:
                                print('try4')
                                if ids[0] == 'miku':
                                    intelligence1 = mikustats['intelligence']
                                if ids[0] == 'alisa':
                                    intelligence1 = alisastats['intelligence']
                                if ids[0] == 'lena':
                                    intelligence1 = lenastats['intelligence']
                                if ids[0] == 'slavya':
                                    intelligence1 = slavyastats['intelligence']
                                if ids[0] == 'zhenya':
                                    intelligence1 = zhenyastats['intelligence']
                                if ids[0] == 'uliana':
                                    intelligence1 = ulianastats['intelligence']
                                if ids[1] == 'miku':
                                    intelligence2 = mikustats['intelligence']
                                if ids[1] == 'alisa':
                                    intelligence2 = alisastats['intelligence']
                                if ids[1] == 'lena':
                                    intelligence2 = lenastats['intelligence']
                                if ids[1] == 'slavya':
                                    intelligence2 = slavyastats['intelligence']
                                if ids[1] == 'zhenya':
                                    intelligence2 = zhenyastats['intelligence']
                                if ids[1] == 'uliana':
                                    intelligence2 = ulianastats['intelligence']
                                z = intelligence1 - intelligence2
                                if z == 0:
                                    x = 50
                                elif z == 1:
                                    x = 60
                                elif z == 2:
                                    x = 75
                                elif z == 3:
                                    x = 85
                                elif z == -1:
                                    x = 40
                                elif z == -2:
                                    x = 25
                                elif z == -3:
                                    x = 15
                                if random.randint(1, 100) <= x:
                                    cardplayers.remove(ids[1])
                                else:
                                    cardplayers.remove(ids[0])
                                i = 10
            text = ''
            x = 0
            for dd in cardplayers:
                x += 1
                try:
                    int(dd)
                    text += users.find_one({'id': dd})['pionername'] + '\n'
                except:
                    text += nametopioner(dd) + '\n'
            text1 = ''
            text3 = ''
            if electronicstats['cardsturn'] == 1:
                text1 = 'Завершился первый этап турнира! А вот и наши победители:\n\n'
            elif electronicstats['cardsturn'] == 2:
                if x > 1:
                    text1 = 'Второй этап турнира подошёл к концу! Встречайте победителей:\n\n'
                else:
                    text1 = 'Финал подошёл к концу! И наш победитель:\n\n'
            elif electronicstats['cardsturn'] == 3:
                if x == 2:
                    text1 = 'Полуфинал завершён! В финале встретятся:\n\n'
                else:
                    text1 = 'Встречайте победителя турнира:\n\n'
            elif electronicstats['cardsturn'] == 4:
                text1 = 'Турнир завершён! И наш победитель:\n\n'
            if x == 2:
                text3 = 'Настало время для финала! Кто же станет победителем на этот раз?'
            elif x == 4:
                text3 = 'На очереди у нас полуфинал. Кто же из четырёх оставшихся игроков попадёт в финал?'
            elif x == 8:
                text3 = 'Скоро начнётся раунд 2. Игроки, приготовьтесь!'
            electronicstats['cardsturn'] += 1
            electronic.send_message(mainchat, text1 + text + '\n' + text3, parse_mode='markdown')
            setka = []
            i = 0
            if len(cardplayers) > 1:
                x = len(cardplayers) / 2
                while i < x:
                    player1 = random.choice(cardplayers)
                    cardplayers.remove(player1)
                    player2 = random.choice(cardplayers)
                    cardplayers.remove(player2)
                    lst = [player1, player2]
                    setka.append(lst)
                    i += 1
                t = threading.Timer(120, cards_nextturn)
                t.start()
            else:
                time.sleep(2)
                olga.send_chat_action(mainchat, 'typing')
                time.sleep(5)
                try:
                    name = users.find_one({'id': cardplayers[0]})['pionername']
                except:
                    name = nametopioner(cardplayers[0])
                olga.send_message(mainchat,
                                  'Отлично! Поздравляю, ' + name + '! А теперь приберитесь тут, скоро ужин.',
                                  parse_mode='markdown')
                olga.send_sticker(mainchat, 'CAADAgADqwADgi0zDzm_zSmMbMmiAg')
                setka = []
                cardplayers = []
                electronicstats['waitingplayers'] = 0
                electronicstats['playingcards'] = 0
                electronicstats['cardsturn'] = 0
        else:
            electronic.send_message(mainchat,
                                    'К сожалению, игроков для турнира сегодня не набралось. Ну ничего, в следующий раз попробуем!')
            setka = []
            cardplayers = []
            electronicstats['waitingplayers'] = 0
            electronicstats['playingcards'] = 0
            electronicstats['cardsturn'] = 0

    except:
        setka = []
        cardplayers = []
        electronicstats['waitingplayers'] = 0
        electronicstats['playingcards'] = 0
        electronicstats['cardsturn'] = 0
        electronic.send_message(mainchat, 'Непредвиденные обстоятельства! Турнир придётся отменить!')


def talkwithplayer(player, pioner):
    if pioner == 'miku':
        t = threading.Timer(random.randint(10, 90), sayto, args=[miku, 'miku', player, cards_startround_mikutexts])
        t.start()
    if pioner == 'alisa':
        t = threading.Timer(random.randint(10, 90), sayto, args=[alisa, 'alisa', player, cards_startround_alisatexts])
        t.start()
    if pioner == 'zhenya':
        t = threading.Timer(random.randint(10, 90), sayto,
                            args=[zhenya, 'zhenya', player, cards_startround_zhenyatexts])
        t.start()
    if pioner == 'uliana':
        t = threading.Timer(random.randint(10, 90), sayto,
                            args=[uliana, 'uliana', player, cards_startround_ulianatexts])
        t.start()
    if pioner == 'slavya':
        t = threading.Timer(random.randint(10, 90), sayto,
                            args=[slavya, 'slavya', player, cards_startround_slavyatexts])
        t.start()
    if pioner == 'lena':
        t = threading.Timer(random.randint(10, 90), sayto, args=[lena, 'lena', player, cards_startround_lenatexts])
        t.start()


cards_startround_mikutexts = ['Ой, Привет! Если не помнишь, то меня Мику зовут. Мы сейчас с тобой ' + \
                              'играем! Ты хорошо играешь? Я не очень...',
                              'Привет! Мы с тобой уже знакомы, если помнишь... ' + \
                              'Удачи на турнире!']
cards_startround_alisatexts = ['Ну привет. Готовься проиграть!']
cards_startround_slavyatexts = ['Привет! Интересно, кто победит в турнире в этот раз...']
cards_startround_ulianatexts = ['Привет-привет! Я сегодня настроена на победу, так что советую сразу сдаться!']
cards_startround_lenatexts = ['Привет. Удачи на сегодняшнем турнире!']
cards_startround_zhenyatexts = ['Выходит, мы с тобой сегодня играем. Давай сразу к игре, без лишних разговоров!']


def sayto(pioner, pionername, id, texts):
    x = users.find_one({'id': id})
    if x['gender'] == 'female':
        gndr = 'а'
    else:
        gndr = ''
    if pionername == 'miku':
        textstochat = ['Привет, ' + x['pionername'] + '! Меня Мику зовут! Мы ещё не знакомы, можем ' + \
                       '[поговорить](https://t.me/ES_MikuBot) после турнира... А сейчас - удачи!']
    elif pionername == 'alisa':
        textstochat = ['Ну привет, ' + x['pionername'] + '! Думаешь победить в турнире? Даже не надейся! Меня тебе ' + \
                       'точно не обыграть!']
    elif pionername == 'slavya':
        textstochat = ['Привет, ' + x['pionername'] + '! Чего-то я тебя не видела раньше... Меня Славя зовут! Можем ' + \
                       '[познакомиться](https://t.me/SlavyaBot) на досуге. Ну а сейчас готовься к игре!']
    elif pionername == 'uliana':
        textstochat = ['Привет! Тебя ведь ' + x['pionername'] + ' зовут? Я Ульяна! Готов' + gndr + ' проиграть?']

    elif pionername == 'lena':
        textstochat = ['Привет, ' + x[
            'pionername'] + '. Меня Лена зовут... Хотя ты наверняка уже знаешь, ведь в турнирной сетке написано. ' + \
                       'Удачи!']

    elif pionername == 'zhenya':
        textstochat = ['Ну привет, ' + x['pionername'] + '. Не знаю, зачем я вообще играю, но уже поздно передумывать.']

    try:
        pioner.send_chat_action(id, 'typing')
        time.sleep(5)
        pioner.send_message(id, random.choice(texts))
    except:
        pioner.send_chat_action(mainchat, 'typing')
        time.sleep(5)
        pioner.send_message(mainchat, random.choice(textstochat), parse_mode='markdown')


def nametopioner(pioner):
    if pioner == 'miku':
        return '[Мику](https://t.me/ES_MikuBot)'
    if pioner == 'alisa':
        return '[Алиса](https://t.me/ES_AlisaBot)'
    if pioner == 'zhenya':
        return '[Женя](https://t.me/ES_ZhenyaBot)'
    if pioner == 'uliana':
        return '[Ульяна](https://t.me/ES_UlianaBot)'
    if pioner == 'slavya':
        return '[Славя](https://t.me/SlavyaBot)'
    if pioner == 'lena':
        return '[Лена](https://t.me/ES_LenaBot)'
    if pioner == 'electronic':
        return '[Электроник](https://t.me/ES_ElectronicBot)'
    if pioner == 'shurik':
        return '[Шурик](https://t.me/ES_Shurikbot)'


def addtogame(name, game):
    game.append(name)


def sendmes(sender, text, parse_mode):
    sender.send_message(mainchat, text, parse_mode=parse_mode)


def sendstick(sender, stick):
    sender.send_sticker(mainchat, stick)


####################################### ELECTRONIC ##############################################
@electronic.message_handler(commands=['control'])
def electroniccontrol(m):
    adm = admins.find_one({'name': 'el_admins'})
    if m.from_user.id in adm['el_admins']:
        if adm['controller'] == None:
            admins.update_one({'name': 'el_admins'}, {'$set': {'controller': {'id': m.from_user.id,
                                                                              'name': m.from_user.first_name}}})
            electronic.send_message(m.from_user.id, 'Привет! надеюсь ты знаешь, как управлять мной.')


@electronic.message_handler(commands=['stopcontrol'])
def electronicstopcontrol(m):
    x = 'el_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            electronic.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@electronic.message_handler(content_types=['sticker'])
def stickercatchelectronic(m):
    stickhandler(m, electronic)


@electronic.message_handler(content_types=['audio'])
@electronic.message_handler(content_types=['voice'])
def stickercatchelectronic(m):
    audiohandler(m, electronic)


@electronic.message_handler(content_types=['photo'])
def photocatchel(m):
    pichandler(m, electronic)


@electronic.message_handler()
def electronichandler(m):
    try:
        if ban.find_one({'id': m.from_user.id}) == None:
            if electronicstats['waitingplayers'] == 1:
                if m.text.lower() == 'хочу принять участие в турнире!':
                    x = users.find_one({'id': m.from_user.id})
                    if x['gender'] == 'female':
                        gndr = 'а'
                    else:
                        gndr = ''
                    if x['id'] not in cardplayers:
                        if m.from_user.id == m.chat.id:
                            texts = ['Привет! Записал тебя в список участников. Жди начала турнира!',
                                     'Хорошо. Записал тебя!',
                                     'Рад, что тебя заинтересовала моя игра. Теперь ты тоже в списке участников!']
                            text = random.choice(texts)
                            electronic.send_message(m.chat.id, text)
                            cardplayers.append(x['id'])
                        else:
                            if m.reply_to_message != None:
                                if m.reply_to_message.from_user.id == 609648686:
                                    texts = ['Привет, [' + x['pionername'] + '](tg://user?id=' + str(
                                        x['id']) + ')! Записал тебя в список участников. Жди начала турнира!',
                                             'Хорошо, [' + x['pionername'] + '](tg://user?id=' + str(
                                                 x['id']) + '). Записал тебя!',
                                             'Рад, что тебя заинтересовала моя игра. Теперь ты тоже в списке участников!']
                                    text = random.choice(texts)
                                    electronic.send_message(m.chat.id, text, parse_mode='markdown',
                                                            reply_to_message_id=m.message_id)
                                    cardplayers.append(x['id'])
                    else:
                        if m.from_user.id == m.chat.id:
                            reply_to_message_id = None
                        else:
                            reply_to_message_id = m.message_id
                        electronic.send_message(m.chat.id, '[' + x['pionername'] + '](tg://user?id=' + str(x['id']) + \
                                                '), ты уже записан' + gndr + ' на турнир!', parse_mode='markdown',
                                                reply_to_message_id=reply_to_message_id)
                else:
                    pass

            msghandler(m, electronic)

    except:
        electronic.send_message(creator, traceback.format_exc())


######################## LENA ###################################################


@lena.message_handler(commands=['control'])
def lenacontrol(m):
    x = 'le_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            lena.send_message(m.from_user.id,
                              'Теперь ты управляешь мной! Я буду присылать тебе все сообщения, которые вижу!')


@lena.message_handler(commands=['stopcontrol'])
def lenastopcontrol(m):
    x = 'le_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            lena.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@lena.message_handler()
def lenamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        print('1')
        yes = ['да!', 'конечно!', 'да', 'да, могу.', 'могу', 'могу.', 'конечно могу!', 'да']
        if lenastats['whohelps'] != None:
            print('2')
            y = 0
            if m.from_user.id == lenastats['whohelps']:
                print('3')
                for ids in yes:
                    if ids in m.text.lower():
                        y = 1
                if y == 1:
                    pioner = users.find_one({'id': m.from_user.id})
                    print('4')
                    try:
                        lenastats['timer'].cancel()
                    except:
                        pass
                    allhelps = ['Спасибо! Тогда пошли, мне нужно отсортировать лекарства в медпункте.',
                                'Спасибо! Пойдём, надо разобрать склад и принести несколько комплектов пионерской формы для Слави.']
                    lenastats['whohelps'] = None
                    helpp = random.choice(allhelps)
                    lena.send_chat_action(m.chat.id, 'typing')
                    time.sleep(4)
                    lena.send_message(m.chat.id, helpp)
                    sendstick(lena, 'CAADAgADZwADgi0zD-vRcG90IHeAAg')
                    t = threading.Timer(300, helpend, args=[m.from_user.id, 'lena'])
                    t.start()
                    users.update_one({'id': m.from_user.id}, {'$set': {'helping': 1}})
        msghandler(m, lena)


@lena.message_handler(content_types=['sticker'])
def stickercatchlena(m):
    stickhandler(m, lena)


@lena.message_handler(content_types=['photo'])
def photocatchlena(m):
    pichandler(m, lena)


@lena.message_handler(content_types=['audio'])
@lena.message_handler(content_types=['voice'])
def photocatchlena(m):
    audiohandler(m, lena)


####################################### ALICE ##############################################
@alisa.message_handler(commands=['control'])
def alisacontrol(m):
    x = 'al_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            alisa.send_message(m.from_user.id,
                               'Ну ты вроде теперь мной управляешь. Я буду присылать тебе все сообщения, которые вижу, но если мне что-то не понравится - буду злиться!')


@alisa.message_handler(commands=['stopcontrol'])
def alisastopcontrol(m):
    x = 'al_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            alisa.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@alisa.message_handler()
def alisamessages(m):
    try:
        if ban.find_one({'id': m.from_user.id}) == None:
            yes = ['да', 'я готов', 'го', 'ну го', 'я в деле']
            if alisastats['whohelps'] != None:
                y = 0
                try:
                    olga.send_message(creator, str(alisastats['whohelps']))
                except:
                    olga.send_message(creator, traceback.format_exc())
                if m.from_user.id == alisastats['whohelps']:
                    for ids in yes:
                        if ids in m.text.lower():
                            y = 1
                    if y == 1:
                        olga.send_message(creator, '1')
                        pioner = users.find_one({'id': m.from_user.id})
                        try:
                            alisastats['timer'].cancel()
                        except:
                            pass
                        allhelps = ['Ну пошли, там нужно один прикол с Электроником намутить...',
                                    'Отлично! Значит так, нам с Ульяной нужен отвлекающий на кухню...']
                        alisastats['whohelps'] = None
                        helpp = random.choice(allhelps)
                        alisa.send_chat_action(m.chat.id, 'typing')
                        time.sleep(4)
                        alisa.send_message(m.chat.id, helpp)
                        sendstick(alisa, 'CAADAgADOwADgi0zDzD8ZNZXu5LHAg')
                        t = threading.Timer(300, helpend, args=[m.from_user.id, 'alisa'])
                        t.start()
                        users.update_one({'id': m.from_user.id}, {'$set': {'helping': 1}})

            msghandler(m, alisa)
            if m.chat.id == mainchat:
                if m.reply_to_message != None:
                    if m.reply_to_message.from_user.id == 634115873:
                        pioner = users.find_one({'id': m.from_user.id})
                        if pioner != None:
                            text = m.text.lower()
                            if 'пошли' in text:
                                if 'ко мне' in text:
                                    texts2 = ['Ну... Я подумаю.', 'Даже не знаю...']
                                    texts1 = ['Совсем офигел?', 'Страх потерял?']
                                    texts3 = ['Лучше ко мне', 'Ну пошли!']
                                    stick2 = 'CAADAgAD4QIAAnHMfRgPhIdIfUrCGAI'
                                    stick1 = 'CAADAgAD4wIAAnHMfRjkcHoZL5eAgwI'
                                    stick3 = 'CAADAgAD7AIAAnHMfRgXuTTXBIbwWgI'
                                    if pioner['Alisa_respect'] < 40:
                                        txt = texts1
                                        stick = stick1
                                    elif pioner['Alisa_respect'] <= 50:
                                        txt = texts2
                                        stick = stick2
                                    elif pioner['Alisa_respect'] <= 75:
                                        txt = texts3
                                        stick = stick3
                                    alisa.send_chat_action(mainchat, 'typing')
                                    t = threading.Timer(3, sendmes, args=[alisa, random.choice(txt), None])
                                    t.start()
                                    t = threading.Timer(3, sendstick, args=[alisa, stick])
                                    t.start()

    except:
        alisa.send_message(creator, traceback.format_exc())


@alisa.message_handler(content_types=['sticker'])
def stickercatchalisa(m):
    stickhandler(m, alisa)


@alisa.message_handler(content_types=['photo'])
def photocatchalisa(m):
    pichandler(m, alisa)


@alisa.message_handler(content_types=['audio'])
@alisa.message_handler(content_types=['voice'])
def photocatchalisa(m):
    audiohandler(m, alisa)


####################################### ULIANA ##############################################
@uliana.message_handler(commands=['control'])
def ulianaacontrol(m):
    x = 'ul_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            uliana.send_message(m.from_user.id, 'Привет! Теперь ты мной управляешь, прикольно!')


@uliana.message_handler(commands=['stopcontrol'])
def ulianastopcontrol(m):
    x = 'ul_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            uliana.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@uliana.message_handler()
def ulianamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        yes = ['да', 'давай', 'я в деле', 'рассказывай']
        if ulianastats['whohelps'] != None:
            y = 0
            if m.from_user.id == ulianastats['whohelps']:
                for ids in yes:
                    if ids in m.text.lower():
                        y = 1
                if y == 1:
                    pioner = users.find_one({'id': m.from_user.id})
                    try:
                        ulianastats['timer'].cancel()
                    except:
                        pass
                    allhelps = [
                        'Я тут хочу заняться одним безобидным делом, и в этом мне потребуются спички... Если что, тебя не сдам!',
                        'О, круто! Мне тут нужно раздобыть немного глицерина...']
                    ulianastats['whohelps'] = None
                    helpp = random.choice(allhelps)
                    uliana.send_chat_action(m.chat.id, 'typing')
                    time.sleep(4)
                    uliana.send_message(m.chat.id, helpp)
                    sendstick(uliana, 'CAADAgADKQADgi0zD_inNy0pZyh0Ag')
                    t = threading.Timer(300, helpend, args=[m.from_user.id, 'uliana'])
                    t.start()
                    users.update_one({'id': m.from_user.id}, {'$set': {'helping': 1}})
        msghandler(m, uliana)


@uliana.message_handler(content_types=['sticker'])
def stickercatchalisa(m):
    stickhandler(m, uliana)


@uliana.message_handler(content_types=['audio'])
@uliana.message_handler(content_types=['voice'])
def stickercatchalisa(m):
    audiohandler(m, uliana)


@uliana.message_handler(content_types=['photo'])
def photocatchuliana(m):
    pichandler(m, uliana)


####################################### SLAVYA ##############################################
@slavya.message_handler(commands=['control'])
def slavyacontrol(m):
    x = 'sl_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            slavya.send_message(m.from_user.id, 'Привет! Теперь ты мной управляешь! Только аккуратнее!')


@slavya.message_handler(commands=['stopcontrol'])
def slavyastopcontrol(m):
    x = 'sl_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            slavya.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@slavya.message_handler()
def slavyamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        yes = ['да', 'я готов', 'давай', 'я в деле']
        if slavyastats['whohelps'] != None:
            y = 0
            if m.from_user.id == slavyastats['whohelps']:
                for ids in yes:
                    if ids in m.text.lower():
                        y = 1
                if y == 1:
                    pioner = users.find_one({'id': m.from_user.id})
                    try:
                        slavyastats['timer'].cancel()
                    except:
                        pass
                    allhelps = [
                        'Отлично! А теперь само задание: надо развесить на деревьях гирлянды, а то завтра вечером будут танцы! Нужна соответствующая атмосфера.',
                        'Спасибо! Тогда наполни вот это ведро водой и принеси сюда, мне надо помыть памятник.']
                    slavyastats['whohelps'] = None
                    helpp = random.choice(allhelps)
                    slavya.send_chat_action(m.chat.id, 'typing')
                    time.sleep(4)
                    slavya.send_message(m.chat.id, helpp)
                    sendstick(slavya, 'CAADAgADUgADgi0zD4hu1wGvwGllAg')
                    t = threading.Timer(300, helpend, args=[m.from_user.id, 'slavya'])
                    t.start()
                    users.update_one({'id': m.from_user.id}, {'$set': {'helping': 1}})
        msghandler(m, slavya)


@slavya.message_handler(content_types=['sticker'])
def stickercatchslavya(m):
    stickhandler(m, slavya)


@slavya.message_handler(content_types=['audio'])
@slavya.message_handler(content_types=['voice'])
def stickercatchslavya(m):
    audiohandler(m, slavya)


@slavya.message_handler(content_types=['photo'])
def photocatchslavya(m):
    pichandler(m, slavya)


####################################### MIKU ##############################################
@miku.message_handler(commands=['control'])
def mikucontrol(m):
    x = 'mi_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            miku.send_message(m.from_user.id,
                              'Привет! Теперь ты управляешь мной, как здорово! Ой, а я однажды в школе пыталась управлять музыкальным клубом, но ничего не вышло... Надеюсь, у тебя получится лучше!')


@miku.message_handler(commands=['stopcontrol'])
def mikustopcontrol(m):
    x = 'mi_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            miku.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@miku.message_handler()
def mikumessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, miku)


@miku.message_handler(content_types=['photo'])
def photocatchmiku(m):
    pichandler(m, miku)


@miku.message_handler(content_types=['sticker'])
def stickercatchmiku(m):
    stickhandler(m, miku)


@miku.message_handler(content_types=['audio'])
@miku.message_handler(content_types=['voice'])
def stickercatchmiku(m):
    audiohandler(m, miku)


####################################### ZHENYA ##############################################
@zhenya.message_handler(commands=['control'])
def zhenyacontrol(m):
    x = 'zh_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            zhenya.send_message(m.from_user.id, 'Привет, ты теперь управляешь мной... А я пока пойду почитаю.')


@zhenya.message_handler(commands=['stopcontrol'])
def zhenyastopcontrol(m):
    x = 'zh_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            zhenya.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@zhenya.message_handler()
def zhenyamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, zhenya)


@zhenya.message_handler(content_types=['sticker'])
def stickercatchzhenya(m):
    stickhandler(m, zhenya)


@zhenya.message_handler(content_types=['photo'])
def photocatchzhenya(m):
    pichandler(m, zhenya)


@zhenya.message_handler(content_types=['audio'])
@zhenya.message_handler(content_types=['voice'])
def photocatchzhenya(m):
    audiohandler(m, zhenya)


####################################### TOLIK ##############################################
@tolik.message_handler(commands=['control'])
def tolikcontrol(m):
    x = 'to_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            tolik.send_message(m.from_user.id, 'Я - Толик.')


@tolik.message_handler(commands=['stopcontrol'])
def tolikstopcontrol(m):
    x = 'to_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            tolik.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@tolik.message_handler()
def tolikmessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, tolik)


@tolik.message_handler(content_types=['sticker'])
def stickercatchtolik(m):
    stickhandler(m, tolik)


@tolik.message_handler(content_types=['audio'])
@tolik.message_handler(content_types=['voice'])
def stickercatchtolik(m):
    audiohandler(m, tolik)


@tolik.message_handler(content_types=['photo'])
def photocatchtolik(m):
    pichandler(m, tolik)


####################################### SHURIK ##############################################
@shurik.message_handler(commands=['control'])
def shurikcontrol(m):
    x = 'sh_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            shurik.send_message(m.from_user.id, 'Привет, ну ты теперь управляешь мной. Думаю, что умеешь.')


@shurik.message_handler(commands=['stopcontrol'])
def shuriktopcontrol(m):
    x = 'sh_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            shurik.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@shurik.message_handler()
def shurikmessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, shurik)


@shurik.message_handler(content_types=['sticker'])
def stickercatchzshurik(m):
    stickhandler(m, shurik)


@shurik.message_handler(content_types=['audio'])
@shurik.message_handler(content_types=['voice'])
def stickercatchzshurik(m):
    audiohandler(m, shurik)


@shurik.message_handler(content_types=['photo'])
def photocatchshurik(m):
    pichandler(m, shurik)


###################################### SEMEN ###############################################


@semen.message_handler(commands=['control'])
def semencontrol(m):
    x = 'se_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            semen.send_message(m.from_user.id, 'Ну ты типо мной управляешь.')


@semen.message_handler(commands=['stopcontrol'])
def semenstopcontrol(m):
    x = 'se_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            semen.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@semen.message_handler()
def semenmessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, semen)


@semen.message_handler(content_types=['sticker'])
def stickercatchsemen(m):
    stickhandler(m, semen)


@semen.message_handler(content_types=['audio'])
@semen.message_handler(content_types=['voice'])
def stickercatchsemen(m):
    audiohandler(m, semen)


@semen.message_handler(content_types=['photo'])
def photocatchsemen(m):
    pichandler(m, semen)


###################################### PIONEER ###############################################


@pioneer.message_handler(commands=['control'])
def pioneercontrol(m):
    x = 'pi_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            pioneer.send_message(m.from_user.id, 'Хех, посмотрим, что ты придумал.')


@pioneer.message_handler(commands=['stopcontrol'])
def pioneerstopcontrol(m):
    x = 'pi_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            pioneer.send_message(m.from_user.id, 'Ты больше не управляешь мной.')


@pioneer.message_handler()
def pioneermessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, pioneer)


@pioneer.message_handler(content_types=['sticker'])
def stickercatchpioneer(m):
    stickhandler(m, pioneer)


@pioneer.message_handler(content_types=['audio'])
@pioneer.message_handler(content_types=['voice'])
def stickercatchpioneer(m):
    audiohandler(m, pioneer)


@pioneer.message_handler(content_types=['photo'])
def photocatchpioneer(m):
    pichandler(m, pioneer)


###################################### YURIY ###############################################


@yuriy.message_handler(commands=['control'])
def yuriyercontrol(m):
    x = 'yu_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            yuriy.send_message(m.from_user.id, 'Теперь ты управляешь мной!')


@yuriy.message_handler(commands=['stopcontrol'])
def pioneerstopcontrol(m):
    x = 'yu_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            yuriy.send_message(m.from_user.id, 'Ты больше не управляешь мной.')


@yuriy.message_handler()
def yuriyrmessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, yuriy)


@yuriy.message_handler(content_types=['sticker'])
def stickercatchpioneer(m):
    stickhandler(m, yuriy)


@yuriy.message_handler(content_types=['audio'])
@yuriy.message_handler(content_types=['voice'])
def stickercatchpioneer(m):
    audiohandler(m, yuriy)


@yuriy.message_handler(content_types=['photo'])
def photocatchyuriy(m):
    pichandler(m, yuriy)


###################################### ALEXANDR ###############################################


@alexandr.message_handler(commands=['control'])
def alexandrercontrol(m):
    x = 'ale_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            alexandr.send_message(m.from_user.id, 'Теперь ты управляешь мной!')


@alexandr.message_handler(commands=['stopcontrol'])
def alexandrstopcontrol(m):
    x = 'ale_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            alexandr.send_message(m.from_user.id, 'Ты больше не управляешь мной.')


@alexandr.message_handler()
def alexrmessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, alexandr)


@alexandr.message_handler(content_types=['sticker'])
def stickercatchpialexr(m):
    stickhandler(m, alexandr)


@alexandr.message_handler(content_types=['audio'])
@alexandr.message_handler(content_types=['voice'])
def stickercatchpialexr(m):
    audiohandler(m, alexandr)


@alexandr.message_handler(content_types=['photo'])
def photocatchalex(m):
    pichandler(m, alexandr)


###################################### VLADISLAV ###############################################


@vladislav.message_handler(commands=['control'])
def vladislavrercontrol(m):
    x = 'vl_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            vladislav.send_message(m.from_user.id, 'Теперь ты управляешь мной!')


@vladislav.message_handler(commands=['stopcontrol'])
def alexandrstopcontrol(m):
    x = 'vl_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            vladislav.send_message(m.from_user.id, 'Ты больше не управляешь мной.')


@vladislav.message_handler()
def yuriyrmessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, vladislav)


@vladislav.message_handler(content_types=['sticker'])
def stickercatchpioneer(m):
    stickhandler(m, vladislav)


@vladislav.message_handler(content_types=['audio'])
@vladislav.message_handler(content_types=['voice'])
def stickercatchpioneer(m):
    audiohandler(m, vladislav)


@vladislav.message_handler(content_types=['photo'])
def photocatchvlad(m):
    pichandler(m, vladislav)


####################################### SAMANTA ##############################################
@samanta.message_handler(commands=['control'])
def samantacontrol(m):
    x = 'sa_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            samanta.send_message(m.from_user.id,
                                 'Привет! Теперь ты управляешь мной!')


@samanta.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x = 'sa_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            samanta.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@samanta.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, samanta)


@samanta.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, samanta)


@samanta.message_handler(content_types=['audio'])
@samanta.message_handler(content_types=['voice'])
def stickercatchsamantau(m):
    audiohandler(m, samanta)


@samanta.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, samanta)


####################################### VASILIYHAIT ##############################################
@vasiliyhait.message_handler(commands=['control'])
def samantacontrol(m):
    x = 'va_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            samanta.send_message(m.from_user.id,
                                 'Привет! Теперь ты управляешь мной!')


@vasiliyhait.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x = 'va_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            samanta.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@vasiliyhait.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, vasiliyhait)


@vasiliyhait.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, vasiliyhait)


@vasiliyhait.message_handler(content_types=['audio'])
@vasiliyhait.message_handler(content_types=['voice'])
def stickercatchsamantau(m):
    audiohandler(m, vasiliyhait)


@vasiliyhait.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, vasiliyhait)


####################################### VIOLA ##############################################
@viola.message_handler(commands=['control'])
def samantacontrol(m):
    x = 'vi_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            viola.send_message(m.from_user.id,
                               'Ну привет, пионер. Теперь ты управляешь мной.')
        else:
            viola.send_message(m.from_user.id, 'Мной уже управляют!')


@viola.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x = 'vi_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            viola.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@viola.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, viola)


@viola.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, viola)


@viola.message_handler(content_types=['audio'])
@viola.message_handler(content_types=['voice'])
def stickercatchsamantau(m):
    audiohandler(m, viola)


@viola.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, viola)


####################################### Sayori ##############################################
@sayori.message_handler(commands=['control'])
def samantaacontrol(m):
    x = 'sayori_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            sayori.send_message(m.from_user.id,
                                'Ура, теперь ты управляешь мной!')
        else:
            sayori.send_message(m.from_user.id, 'Мной уже управляют!')


@sayori.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x = 'sayori_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            sayori.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@sayori.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, sayori)


@sayori.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, sayori)


@sayori.message_handler(content_types=['audio'])
@sayori.message_handler(content_types=['voice'])
def stickercatchsamantau(m):
    audiohandler(m, sayori)


@sayori.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, sayori)


####################################### Yuri ##############################################
@yuri.message_handler(commands=['control'])
def samantaacontrol(m):
    x = 'yuri_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            yuri.send_message(m.from_user.id,
                              'Теперь ты управляешь мной! Только аккуратнее...')
        else:
            yuri.send_message(m.from_user.id, 'Мной уже управляют!')


@yuri.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x = 'yuri_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            yuri.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@yuri.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, yuri)


@yuri.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, yuri)


@yuri.message_handler(content_types=['audio'])
@yuri.message_handler(content_types=['voice'])
def stickercatchsamantau(m):
    audiohandler(m, yuri)


@yuri.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, yuri)


####################################### Monika ##############################################
@monika.message_handler(commands=['control'])
def samantaacontrol(m):
    x = 'monika_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            monika.send_message(m.from_user.id,
                                'Привет, теперь ты управляешь мной!')
        else:
            monika.send_message(m.from_user.id, 'Мной уже управляют!')


@monika.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x = 'monika_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            monika.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@monika.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, monika)


@monika.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, monika)


@monika.message_handler(content_types=['audio'])
@monika.message_handler(content_types=['voice'])
def stickercatchsamantau(m):
    audiohandler(m, monika)


@monika.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, monika)


####################################### Natsuki ##############################################
@natsuki.message_handler(commands=['control'])
def samantaacontrol(m):
    x = 'natsuki_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            natsuki.send_message(m.from_user.id,
                                 'Теперь ты управляешь мной! Но запомни - это не мило!')
        else:
            natsuki.send_message(m.from_user.id, 'Мной уже управляют!')


@natsuki.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x = 'natsuki_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            natsuki.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@natsuki.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, natsuki)


@natsuki.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, natsuki)


@natsuki.message_handler(content_types=['audio'])
@natsuki.message_handler(content_types=['voice'])
def stickercatchsamantau(m):
    audiohandler(m, natsuki)


@natsuki.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, natsuki)


####################################### YULIYA ##############################################
@yuliya.message_handler(commands=['control'])
def samantacontrolyu(m):
    yuliya.send_message(creator, '1')
    x = 'yul_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            yuliya.send_message(m.from_user.id,
                                'Привет! Теперь ты управляешь мной!')
        else:
            yuliya.send_message(m.from_user.id, 'Мной уже управляют!')


@yuliya.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x = 'yul_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            yuliya.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@yuliya.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, yuliya)


@yuliya.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, yuliya)


@yuliya.message_handler(content_types=['audio'])
@yuliya.message_handler(content_types=['voice'])
def stickercatchsamantau(m):
    audiohandler(m, yuliya)


@yuliya.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, yuliya)


####################################### EVILLENA ##############################################
@evillena.message_handler(commands=['control'])
def samantacontrol(m):
    x = 'evl_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            evillena.send_message(m.from_user.id,
                                  'Теперь ты управляешь мной!')
        else:
            evillena.send_message(m.from_user.id, 'Мной уже управляют!')


@evillena.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x = 'evl_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            evillena.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@evillena.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, evillena)


@evillena.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, evillena)


@evillena.message_handler(content_types=['audio'])
@evillena.message_handler(content_types=['voice'])
def stickercatchsamantau(m):
    audiohandler(m, evillena)


@evillena.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, evillena)


####################################### MONSTER ##############################################
@monster.message_handler(commands=['control'])
def samantacontrol(m):
    x = 'mns_admins'
    adm = admins.find_one({'name': x})
    if m.from_user.id in adm[x]:
        if adm['controller'] == None:
            admins.update_one({'name': x}, {'$set': {'controller': {'id': m.from_user.id,
                                                                    'name': m.from_user.first_name}}})
            yuliya.send_message(m.from_user.id,
                                'Теперь ты управляешь мной!')
        else:
            yuliya.send_message(m.from_user.id, 'Мной уже управляют!')


@monster.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x = 'mns_admins'
    adm = admins.find_one({'name': x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name': x}, {'$set': {'controller': None}})
            yuliya.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@monster.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, monster)


@monster.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, monster)


@monster.message_handler(content_types=['audio'])
@monster.message_handler(content_types=['voice'])
def stickercatchsamantau(m):
    audiohandler(m, monster)


@monster.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, monster)


def helpend(id, pioner):
    x = users.find_one({'id': id})
    users.update_one({'id': id}, {'$set': {'helping': 0}})
    if pioner == 'lena':
        lena.send_chat_action(id, 'typing')
        time.sleep(4)
        lena.send_message(mainchat,
                          'Спасибо за помощь, [' + x['pionername'] + '](tg://user?id=' + str(x['id']) + ')! ' + \
                          'Без тебя ушло бы гораздо больше времени. Ну, я пойду...', parse_mode='markdown')
        users.update_one({'id': x['id']}, {'$inc': {'Lena_respect': random.randint(4, 5)}})
    if pioner == 'alisa':
        alisa.send_chat_action(id, 'typing')
        time.sleep(4)
        alisa.send_message(mainchat,
                           'Ну спасибо за помощь, [' + x['pionername'] + '](tg://user?id=' + str(x['id']) + ')! ' + \
                           'Неплохо получилось!', parse_mode='markdown')
        users.update_one({'id': x['id']}, {'$inc': {'Alisa_respect': random.randint(4, 5)}})

    if pioner == 'slavya':
        slavya.send_chat_action(id, 'typing')
        time.sleep(4)
        slavya.send_message(mainchat,
                            'Спасибо за помощь, [' + x['pionername'] + '](tg://user?id=' + str(x['id']) + ')! ' + \
                            'Теперь можешь отдыхать.', parse_mode='markdown')
        users.update_one({'id': x['id']}, {'$inc': {'Slavya_respect': random.randint(4, 5)}})

    if pioner == 'uliana':
        uliana.send_chat_action(id, 'typing')
        time.sleep(4)
        uliana.send_message(mainchat,
                            'Как здорово! Спасибо за помощь, [' + x['pionername'] + '](tg://user?id=' + str(
                                x['id']) + ')!' + \
                            '', parse_mode='markdown')
        users.update_one({'id': x['id']}, {'$inc': {'Uliana_respect': random.randint(4, 5)}})


cardplayers = []

alisastats = {
    'strenght': 1,
    'agility': 2,
    'intelligence': 3,
    'controller': None,
    'bot': alisa,
    'whohelps': None
}
lenastats = {
    'strenght': 2,
    'agility': 2,
    'intelligence': 2,
    'whohelps': None,
    'timer': None,
    'controller': None,
    'bot': lena
}
mikustats = {
    'strenght': 2,
    'agility': 2,
    'intelligence': 2,
    'controller': None,
    'bot': miku
}
ulianastats = {
    'strenght': 1,
    'agility': 4,
    'intelligence': 1,
    'controller': None,
    'bot': uliana,
    'whohelps': None,
    'timer': None
}
slavyastats = {
    'strenght': 1,
    'agility': 1,
    'whohelps': None,
    'timer': None,
    'intelligence': 4,
    'controller': None,
    'bot': slavya
}
electronicstats = {
    'strenght': 3,
    'agility': 1,
    'intelligence': 4,
    'waitingplayers': 0,
    'playingcards': 0,
    'cardsturn': 0,
    'controller': None,
    'bot': electronic

}
zhenyastats = {
    'strenght': 2,
    'agility': 1,
    'intelligence': 3,
    'controller': None,
    'bot': zhenya

}

tolikstats = {
    'strenght': 2,
    'agility': 2,
    'intelligence': 2,
    'controller': None,
    'bot': tolik

}

shurikstats = {
    'strenght': 2,
    'agility': 1,
    'intelligence': 4,
    'controller': None,
    'bot': shurik

}

odstats = {
    'lineyka': [],
    'waitforlineyka': 0,
    'controller': None,
    'bot': olga
}

semenstats = {
    'controller': None,
    'bot': semen
}

pioneerstats = {
    'controller': None,
    'bot': pioneer
}

ctrls = []
ctrls.append(odstats)
ctrls.append(electronicstats)
ctrls.append(slavyastats)
ctrls.append(zhenyastats)
ctrls.append(ulianastats)
ctrls.append(mikustats)
ctrls.append(lenastats)
ctrls.append(alisastats)
ctrls.append(shurikstats)
ctrls.append(tolikstats)

zavtrak = '9:00'
obed = '14:00'
uzhin = '21:00'


def findindex(x):
    i = 0
    for ids in works:
        if ids['name'] == x:
            index = i
        i += 1
    return index


def randomhelp():
    t = threading.Timer(random.randint(420, 1000), randomhelp)
    t.start()
    global rds
    if rds == True:
        spisok = []
        pioners = ['lena', 'alisa', 'slavya', 'uliana']
        x = users.find({})
        for ids in x:
            if ids['pionername'] != None:
                spisok.append(ids)
        if len(spisok) > 0:
            hour = gettime('h')
            if hour >= 7 and hour <= 23:
                pioner = random.choice(spisok)
                z = random.choice(pioners)
                helpto(pioner, z)


def helpto(pioner, x):
    if pioner['gender'] == 'male':
        g = ''
    else:
        g = 'ла'
    if x == 'lena':
        try:
            if pioner['Lena_respect'] >= 85:
                text = '[' + pioner['pionername'] + '](tg://user?id=' + str(pioner[
                                                                                'id']) + '), привет! Ты мне часто помогаешь, поэтому хотелось бы попросить тебя о помощи еще раз... Не откажешь?'
            else:
                text = '[' + pioner['pionername'] + '](tg://user?id=' + str(
                    pioner['id']) + '), привет. Не мог' + g + ' бы ты мне помочь?'
            lena.send_chat_action(mainchat, 'typing')
            time.sleep(4)
            m = lena.send_message(mainchat, text, parse_mode='markdown')
            lenastats['whohelps'] = pioner['id']
            t = threading.Timer(300, helpcancel, args=['lena', m, pioner['id']])
            t.start()
            lenastats['timer'] = t
            sendstick(lena, 'CAADAgADaQADgi0zD9ZBO-mNcLuBAg')
        except:
            pass

    if x == 'alisa':
        try:
            if pioner['Alisa_respect'] >= 85:
                text = '[' + pioner['pionername'] + '](tg://user?id=' + str(
                    pioner['id']) + '), привет, я же знаю, что ты любишь повеселиться! Готов на этот раз?'
            else:
                text = '[' + pioner['pionername'] + '](tg://user?id=' + str(pioner[
                                                                                'id']) + '), смотри, куда идёшь! Должен будешь, и долг отработаешь прямо сейчас. Мне тут помощь нужна в одном деле...'
            alisa.send_chat_action(mainchat, 'typing')
            time.sleep(4)
            m = alisa.send_message(mainchat, text, parse_mode='markdown')
            alisastats['whohelps'] = pioner['id']
            t = threading.Timer(300, helpcancel, args=['alisa', m, pioner['id']])
            t.start()
            alisastats['timer'] = t
            sendstick(alisa, 'CAADAgADOQADgi0zDztSbkeWq3BEAg')
        except:
            olga.send_message(creator, traceback.format_exc())

    if x == 'slavya':
        try:
            if pioner['Slavya_respect'] >= 85:
                text = 'Привет, ' + '[' + pioner['pionername'] + '](tg://user?id=' + str(pioner[
                                                                                             'id']) + ')! Ты не раз выручал меня, поэтому я знаю, что тебе можно довериться. Поможешь мне с одним важным заданием?'
            else:
                text = 'Привет, [' + pioner['pionername'] + '](tg://user?id=' + str(
                    pioner['id']) + ')! Поможешь мне с одним важным заданием?'
            slavya.send_chat_action(mainchat, 'typing')
            time.sleep(4)
            m = slavya.send_message(mainchat, text, parse_mode='markdown')
            slavyastats['whohelps'] = pioner['id']
            t = threading.Timer(300, helpcancel, args=['slavya', m, pioner['id']])
            t.start()
            slavyastats['timer'] = t
            sendstick(slavya, 'CAADAgADTAADgi0zD6PLpc722Bz3Ag')
        except:
            olga.send_message(creator, traceback.format_exc())

    if x == 'uliana':
        try:
            if pioner['Uliana_respect'] >= 85:
                text = 'Привет, ' + '[' + pioner['pionername'] + '](tg://user?id=' + str(
                    pioner['id']) + ')! Мне не помешала бы помощь в одном деле... Я знаю, что ты согласишься!'
            else:
                text = 'Эй, [' + pioner['pionername'] + '](tg://user?id=' + str(
                    pioner['id']) + ')! Поможешь мне с одним делом?'
            uliana.send_chat_action(mainchat, 'typing')
            time.sleep(4)
            m = uliana.send_message(mainchat, text, parse_mode='markdown')
            ulianastats['whohelps'] = pioner['id']
            t = threading.Timer(300, helpcancel, args=['uliana', m, pioner['id']])
            t.start()
            ulianastats['timer'] = t
            sendstick(uliana, 'CAADAgADLwADgi0zD7_x8Aph94DmAg')
        except:
            olga.send_message(creator, traceback.format_exc())


def helpcancel(pioner, m, userid):
    user = users.find_one({'id': userid})
    if pioner == 'lena':
        lenastats['whohelps'] = None
        lena.send_chat_action(mainchat, 'typing')
        time.sleep(4)
        lena.send_message(mainchat, 'Ты, наверное, сейчас занят... Прости, что побеспокоила.',
                          reply_to_message_id=m.message_id)
        if user['Lena_respect'] > 0:
            users.update_one({'id': user['id']}, {'$inc': {'Lena_respect': -1}})
    if pioner == 'alisa':
        alisastats['whohelps'] = None
        alisa.send_chat_action(mainchat, 'typing')
        time.sleep(4)
        if user['Alisa_respect'] < 85:
            alisa.send_message(mainchat, 'Ну и пожалуйста!', reply_to_message_id=m.message_id)
        else:
            alisa.send_message(mainchat, 'Ну как хочешь! Сама справлюсь.', reply_to_message_id=m.message_id)
        if user['Alisa_respect'] > 0:
            users.update_one({'id': user['id']}, {'$inc': {'Alisa_respect': -1}})
    if pioner == 'slavya':
        slavyastats['whohelps'] = None
        slavya.send_chat_action(mainchat, 'typing')
        time.sleep(4)
        if user['Slavya_respect'] < 85:
            slavya.send_message(mainchat, 'Ладно, спрошу кого-нибудь другого.', reply_to_message_id=m.message_id)
        else:
            slavya.send_message(mainchat, 'Ладно, ничего страшного - спрошу кого-нибудь другого.',
                                reply_to_message_id=m.message_id)
        if user['Slavya_respect'] > 0:
            users.update_one({'id': user['id']}, {'$inc': {'Slavya_respect': -1}})

    if pioner == 'uliana':
        ulianastats['whohelps'] = None
        uliana.send_chat_action(mainchat, 'typing')
        time.sleep(4)
        if user['Uliana_respect'] < 85:
            uliana.send_message(mainchat, 'Ой, ну и ладно! Найду того, кому интересно!',
                                reply_to_message_id=m.message_id)
        else:
            uliana.send_message(mainchat, 'Ладно, как хочешь. Но если появится желание - говори!',
                                reply_to_message_id=m.message_id)
        if user['Uliana_respect'] > 0:
            users.update_one({'id': user['id']}, {'$inc': {'Uliana_respect': -1}})


def randomact():
    t = threading.Timer(random.randint(4900, 18000), randomact)
    t.start()
    global rds
    if rds == True:
        lisst = ['talk_uliana+olgadmitrievna', 'talk_uliana+alisa', 'talk_el+shurik']
        x = random.choice(lisst)
        if x == 'talk_uliana+olgadmitrievna':
            olga.send_chat_action(mainchat, 'typing')
            time.sleep(4)
            olga.send_message(mainchat, nametopioner('uliana') + ', а ну стой! Ты эти конфеты где взяла?',
                              parse_mode='markdown')
            sendstick(olga, 'CAADAgADtwADgi0zD-9trZ_s35yQAg')
            time.sleep(1)
            uliana.send_chat_action(mainchat, 'typing')
            time.sleep(2)
            uliana.send_message(mainchat, 'Какие конфеты?')
            sendstick(uliana, 'CAADAgADHQADgi0zD1aFI93sTseZAg')
            time.sleep(2)
            olga.send_chat_action(mainchat, 'typing')
            time.sleep(3)
            olga.send_message(mainchat, 'Те, что ты за спиной держишь! Быстро верни их в столовую!')
            time.sleep(1)
            uliana.send_chat_action(mainchat, 'typing')
            time.sleep(2)
            uliana.send_message(mainchat, 'Хорошо, Ольга Дмитриевна...')
            sendstick(uliana, 'CAADAgADJQADgi0zD1PW7dDuU5hCAg')
        if x == 'talk_uliana+alisa':
            alisa.send_chat_action(mainchat, 'typing')
            time.sleep(3)
            alisa.send_message(mainchat, nametopioner('uliana') + ', не боишься, что Ольга Дмитриевна спалит?',
                               parse_mode='markdown')
            time.sleep(1)
            uliana.send_chat_action(mainchat, 'typing')
            time.sleep(2)
            uliana.send_message(mainchat, 'Ты о чём?')
            time.sleep(2)
            alisa.send_chat_action(mainchat, 'typing')
            time.sleep(2)
            alisa.send_message(mainchat, 'О конфетах, которые ты украла!')
            sendstick(alisa, 'CAADAgADOwADgi0zDzD8ZNZXu5LHAg')
            time.sleep(1)
            uliana.send_chat_action(mainchat, 'typing')
            time.sleep(2)
            uliana.send_message(mainchat, 'Да не, не спалит! Я так уже много раз делала!')
            sendstick(uliana, 'CAADAgADKQADgi0zD_inNy0pZyh0Ag')
            time.sleep(2)
            alisa.send_chat_action(mainchat, 'typing')
            time.sleep(2)
            alisa.send_message(mainchat, 'Тогда делись!')
            time.sleep(1)
            uliana.send_chat_action(mainchat, 'typing')
            time.sleep(2)
            uliana.send_message(mainchat, 'Тогда пошли в домик!')
        if x == 'talk_el+shurik':
            electronic.send_chat_action(mainchat, 'typing')
            time.sleep(3)
            electronic.send_message(mainchat,
                                    nametopioner('shurik') + ', как думаешь, возможно ли перемещение во времени?',
                                    parse_mode='markdown')
            sendstick(electronic, 'CAADAgAD0wADgi0zD1LBx9yoFTBiAg')
            time.sleep(1)
            shurik.send_chat_action(mainchat, 'typing')
            time.sleep(2)
            shurik.send_message(mainchat, 'В теории... Хотя нет, это антинаучно.')
            sendstick(shurik, 'CAADAgAD5QADgi0zDwyDLbq7ZQ4vAg')
            time.sleep(2)
            electronic.send_chat_action(mainchat, 'typing')
            time.sleep(2)
            electronic.send_message(mainchat,
                                    'А мне вот кажется, что когда-нибудь прогресс дойдёт и до такого...')


checktime()

t = threading.Timer(120, randomhelp)
t.start()


def polling(pollingbot):
    pollingbot.polling(none_stop=True, timeout=600)


t = threading.Timer(120, randomact)
t.start()

if True:
    print('7777')
    users.update_many({}, {'$set': {'working': 0}})
    users.update_many({}, {'$set': {'waitforwork': 0}})
    users.update_many({}, {'$set': {'relaxing': 0}})
    users.update_many({}, {'$set': {'answering': 0}})
    t = threading.Timer(1, polling, args=[uliana])
    t.start()
    uliana.send_message(creator, 'Я могу принимать сообщения!')
    t = threading.Timer(1, polling, args=[olga])
    t.start()
    t = threading.Timer(1, polling, args=[lena])
    t.start()
    t = threading.Timer(1, polling, args=[electronic])
    t.start()
    t = threading.Timer(1, polling, args=[zhenya])
    t.start()
    t = threading.Timer(1, polling, args=[alisa])
    t.start()
    t = threading.Timer(1, polling, args=[slavya])
    t.start()
    t = threading.Timer(1, polling, args=[miku])
    t.start()
    t = threading.Timer(1, polling, args=[tolik])
    t.start()
    t = threading.Timer(1, polling, args=[shurik])
    t.start()
    t = threading.Timer(1, polling, args=[semen])
    t.start()
    t = threading.Timer(1, polling, args=[pioneer])
    t.start()
    t = threading.Timer(1, polling, args=[world])
    t.start()
    t = threading.Timer(1, polling, args=[yuriy])
    t.start()
    t = threading.Timer(1, polling, args=[alexandr])
    t.start()
    t = threading.Timer(1, polling, args=[vladislav])
    t.start()
    t = threading.Timer(1, polling, args=[samanta])
    t.start()
    t = threading.Timer(1, polling, args=[vasiliyhait])
    t.start()
    t = threading.Timer(1, polling, args=[viola])
    t.start()
    t = threading.Timer(1, polling, args=[yuliya])
    t.start()
    t = threading.Timer(1, polling, args=[evillena])
    t.start()
    t = threading.Timer(1, polling, args=[monster])
    t.start()
    t = threading.Timer(1, polling, args=[natsuki])
    t.start()
    t = threading.Timer(1, polling, args=[monika])
    t.start()
    t = threading.Timer(1, polling, args=[sayori])
    t.start()
    t = threading.Timer(1, polling, args=[yuri])
    t.start()


@world.message_handler(commands=['addplayer'])
def addplayer(m):
    if m.from_user.id == creator:
        pioner = m.text.split(' ')[2]
        user = int(m.text.split(' ')[1])
        thunder.insert_one(createeventuser(user, pioner))
        world.send_message(m.chat.id, 'Юзер добавлен!')


def createeventuser(user, pioner):
    return {
        'id': user,
        'pioner': pioner,
        'choicing': 0,
        'ready': 0,
        'nextfunc': None
    }


@world.message_handler(content_types=['photo'])
def imgg(m):
    world.send_photo(creator, m.photo[0].file_id, caption=str(m.photo[0].file_id))


@world.message_handler(content_types=['audio'])
def audiohandlerrrrr(m):
    world.send_audio(creator, m.audio.file_id)
    world.send_message(creator, m.audio.file_id)


############################################### ПИОНЕР: НАЧАЛО ##############################################

def pi_sends(user):
    if user != None:
        slt = 3
        long = 5
        pi_user = thunder.find_one({'pioner': 'pioner'})
        se_user = thunder.find_one({'pioner': 'semen'})
        world.send_photo(user['id'], 'AgADAgADhqoxGx3TaEs2RjkBAr60m95HhA8ABLaEkJAkRZsEQy8BAAEC')
        world.send_message(user['id'], 'Меня разбудило громкое завывание сработавшей сигнализации.')
        time.sleep(slt)
        world.send_message(user['id'], '~Чёрт, надо будет убавить громкость рупоров.~')
        time.sleep(slt)
        world.send_message(user['id'], 'Я поднялся с кровати и накинул лежавшую рядом кожаную куртку.')
        time.sleep(slt)
        world.send_message(user['id'], 'Я кинул короткий взгляд на часы.')
        time.sleep(slt)
        world.send_message(user['id'], '~7:30~')
        time.sleep(slt)
        world.send_message(user['id'], '~Кого это принесло с утра пораньше?!~')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Нацепив ботинки, я подошел к столу с пультом управления и нажал на небольшую красную кнопку.')
        time.sleep(slt)
        world.send_message(user['id'], 'Звук сирены тут же прекратился.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Я на ходу подхватил с пола фонарь и направился в черноту тоннеля, захлопнув за собой массивную дверь бомбоубежища.')
        time.sleep(slt)
        world.send_message(user['id'], 'Не прошло и пяти минут, как я уже был на месте.')
        world.send_photo(user['id'], 'AgADAgAD_qsxG9QTYUuEsMnVDPodCSNTOQ8ABFoAASsafFfUD_AiBgABAg')
        time.sleep(slt)
        world.send_message(user['id'],
                           'На первый взгляд это был ничем не примечательный свод тоннеля недалеко от входа в катакомбы, однако, ' +
                           'если приглядеться чуть внимательнее, то можно заметить слабо мигающую красную лампочку в самой верхней точки каменного свода.')
        time.sleep(long)
        world.send_message(user['id'],
                           'Именно от этой красной лампочки, вниз, тянулась едва ли заметная леска. В черноте тоннеля заметить её было практически невозможно.')
        time.sleep(slt)
        world.send_message(user['id'], 'Я медленно провёл светом фонаря от потолка до пола тоннеля.')
        time.sleep(slt)
        world.send_message(user['id'], 'Ничего. Леска пропала.')
        time.sleep(slt)
        world.send_message(user['id'], 'Механизм был устоен так, чтобы порвать леску смог только человек.')
        time.sleep(slt)
        world.send_message(user['id'], 'От массы менее пятнадцати килограмм леска бы не порвалась.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Это сразу ликвидировало вариант с лесной живностью. Белка или кролик не смогли бы порвать леску, а сигнализация бы не сработала.')
        time.sleep(long)
        world.send_message(user['id'], 'А это значит, что...')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nДавно не виделись.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Раздался за спиной знакомый голос.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я медленно развернулся и посветил фонарём на источник звука.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Мда. Я ошибся. Лесная живность все-таки смогла порвать леску.~',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Передо мной стояла Юля.', parse_mode='markdown')
        world.send_sticker(user['id'], 'CAADAgADkwADgi0zD6BnrLMAAVO12AI')
        time.sleep(slt)
        world.send_message(user['id'],
                           '_Пионер_:\nВот так встреча. Кажется, последний раз мы не очень весело расстались.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Юля нервно дёрнула ушами.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '_Юля_:\nТы сам в этом виноват. Если бы ты сделал правильный выбор, то уехал бы вместе с ним.',
                           parse_mode='markdown')
        world.send_sticker(user['id'], 'CAADAgADkwADgi0zD6BnrLMAAVO12AI')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nДа брось, я уже смирился. Давай не будем давить на старые раны.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nЯ пришла сюда не за этим.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '_Пионер_:\nТак я и знал. Глупо было надеяться, что ты зашла на чай. Которого, кстати, у меня нет...',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Юля переменилась в лице.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nЧай? Что за чай? Никогда о нем не слышала.', parse_mode='markdown')
        world.send_sticker(user['id'], 'CAADAgADowADgi0zDw_IFESsbO6uAg')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nЭто заваренные запасы.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Коротко обьяснил я ей.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nФу! Какая гадость!', parse_mode='markdown')
        world.send_sticker(user['id'], 'CAADAgADkwADgi0zD6BnrLMAAVO12AI')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nМы отошли от темы. Зачем ты пришла?', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Лицо Юли вновь обрело прежнюю серьёзность.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nЧтобы предупредить тебя.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nПредупредить? О чём?', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nНо для начала мне нужно рассказать тебе все, что знаю сама.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'По моей спине пробежал холодок.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nЧто? Что ты имеешь ввиду?', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Юля раздраженно качнула хвостом.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nНе прикидывайся идиотом. Ты прекрасно меня понял.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я стоял открыв рот, не в силах произнести ни слова.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Все секреты лагеря станут моими!~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Юля тем временем медленными шагами начинала приближаться ко мне.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Подойдя совсем близко, она начала обходить меня вокруг.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nИтак, начнём с самого простого. Кто я такая? Ты знаешь?',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nДевочка-кошка.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Выдавил я.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nНет, не все так просто. Я...', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Её слова прервал оглушительный взрыв где-то на поверхности.',
                           parse_mode='markdown')
        world.send_photo(user['id'], 'AgADAgADh6oxGx3TaEtrkrCzsJYzIotbOQ8ABO6maOEKrBrV7hkGAAEC')
        world.send_audio(user['id'], 'CQADAgADkgMAApS8aEtZQAEN-2XZgwI')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Юля отпрыгнула от меня и оскалилась, посмотрев вверх. Её зрачки превратились в две узкие щелки.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nО нет, я опоздала!', parse_mode='markdown')
        world.send_sticker(user['id'], 'CAADAgADpwADgi0zD3TCQLMRiwEvAg')
        time.sleep(slt)
        world.send_message(user['id'], 'Она резко перевела взгляд на меня.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nУ нас мало времени! Слушай меня, и запоминай!', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '_Юля_:\nЧерез несколько минут тебя закинет на новую смену. В ней будет много других твоих двойников. Но лишь один из них настоящий. Все остальные не больше чем клоны.',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], '_Юля_:\nГоворю сразу, в лагере будут происходить необьяснимые вещи.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nИ я хочу, чтобы ты был готов, когда встретишься с ними. Ты...',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Очередной взрыв вновь приглушил её слова...', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Я отошел на шаг назад и прислонился спиной к стене. Юля крепче прижала уши к затылку.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Нас стало разделять всё большее расстояние.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nТы должен найти настоящего Семёна!', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я опешил от её слов.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Настоящего?!~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nНастоящего?! Неужели ты намекаешь на...', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Юля с горечью посмотрела мне в глаза.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nСожалею, но это так.', parse_mode='markdown')
        world.send_sticker(user['id'], 'CAADAgADoQADgi0zD07z3mQumb44Ag')
        time.sleep(slt)
        world.send_message(user['id'], '~НЕ МОЖЕТ БЫТЬ!~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Я не могу быть клоном! Я настоящий! Это *я* настоящий Семён!~',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nТы должен спасти его. Только один из вас выберется.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nЗапомни!', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '_Юля_:\n_Восход окрасит бесконечно темное небо багряной краской, как знак того, сколько крови было пролито ради свободы._',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], 'Чужим голосом произнесла Юля.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '~Спасти его?! Ну уж нет. Я не стану жертвовать своей жизнью ради очередного сопливого Семенчика.~',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], 'В груди начала закипать бешеная злоба.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nСпасти его?! Спасти его?!', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nДа пошла ты! Это я настоящий Семен! Это я живой!',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Юля округлила глаза.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '_Юля_:\nНет, нет, нет... Даже не думай об этом! Ты не представляешь, что тогда произойдет!',
                           parse_mode='markdown')
        world.send_sticker(user['id'], 'CAADAgADnQADgi0zD35x6NCuNd5VAg')
        time.sleep(slt)
        world.send_message(user['id'], 'Я безумно улыбнулся.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nНеужели ты не понимаешь?! Мне нечего терять!', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '_Пионер_:\nТы совершила ошибку, придя сюда. Но я не могу не выразить благодарность тебе за информацию. К сожалению, теперь я буду обладать ей один.',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'],
                           'В этот момент рука уже находилась за спиной. Холодное лезвие упиралось в ремень шорт.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я резко сорвался с места и кинулся на Юлю.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Она вскрикнула.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я рывком вынул нож из тела, кинул девушку на пол и направился к выходу наружу.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nСемен, ты... Совершаешь... Ошибку...', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Прохрипела за спиной Юля.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nНет, ошибку совершили вы, когда отправили меня в этот лагерь.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nНо я выберусь отсюда.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nИ никто меня не остановит...', parse_mode='markdown')
        time.sleep(slt)
        t = threading.Thread(target=se_sends, args=[se_user])
        t.start()
        t = threading.Timer(10, pioner_awaking, args=[pi_user])
        t.start()


############################################### СЕМЁН: НАЧАЛО ##############################################
def se_sends(user):
    if user != None:
        slt = 3
        long = 5
        pi_user = thunder.find_one({'pioner': 'pioner'})
        se_user = thunder.find_one({'pioner': 'semen'})
        world.send_photo(user['id'], '')
        world.send_message(user['id'], 'В глаза ударил яркий свет.')
        time.sleep(slt)
        world.send_message(user['id'], '~Да здраствует новая смена.~')
        time.sleep(slt)
        world.send_message(user['id'], 'Запах бензина и пыли. Вот с чего начинается очередной цикл.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Я машинально встал, и вышел из Икаруса, не забыв захватить пачку "Космоса" из бардачка.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Вокруг все цвело и пахло, как всегда. Прекрасные пейзажи этого мира уже давно перестали удивлять.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Первые смены, бывало даже резали глаза, но человек быстро адаптируется к окружающей среде.')
        time.sleep(long)
        world.send_message(user['id'], 'Я сел на бордюр, подкурил сигарету и принялся ждать.')
        time.sleep(slt)
        world.send_message(user['id'], 'Каждую смену ровно через 15 минут после приезда приходила она.')
        time.sleep(slt)
        world.send_message(user['id'], 'Славя.')
        time.sleep(slt)
        world.send_message(user['id'], 'За время пока я в лагере, я успел неплохо покопаться в себе.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Славя была, пожалуй, единственная, кто ни разу за все циклы не смог мне надоесть.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Она одна кое-как понимала меня, когда я рассказывал ей о моей нелегкой судьбе в этом лагере.')
        time.sleep(slt)
        world.send_message(user['id'], 'Или делала вид?')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Впрочем, неважно, ведь тогда мне было просто необходимо, чтобы меня кто-то выслушал. И она прекрасно исполняла мое желание.')
        time.sleep(long)
        world.send_message(user['id'], 'Я докурил, затушил об асфальт сигарету, и глянул на время.')
        time.sleep(slt)
        world.send_message(user['id'], '10:34.')
        time.sleep(slt)
        world.send_message(user['id'], 'Ну всё, пора идти.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Подойдя к воротам, я прислушался, приготовясь услышать разговоры двух кибернетиков, как обычно стоявших около клубов.')
        time.sleep(long)
        world.send_message(user['id'], 'Тишина.')
        time.sleep(slt)
        world.send_message(user['id'],
                           '~Странно. Ну ладно. Может при переходе на новый цикл у меня было повреждение слуха.~')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Иногда случались небольшие инциденты при попадании на новую смену. Особенно часто после суицида. Проблемы незначительные, но заметные сразу.')
        time.sleep(long)
        world.send_message(user['id'],
                           'Допустим, я однажды пробовал выпить все таблетки в медпункте, так после пробуждения в автобусе у меня всю смену без причины болел живот.',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], 'Посмотрев еще раз на часы, я обнаружил, что время уже...',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '10:36', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Сердце упало в пятки.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Не может быть!~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я забежал за лагерные ворота.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Насколько же я был удивлен, когда не увидел за воротами НИКОГО!',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Что тут мать твою происходит?!~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Ни одной смены с похожим сюжетом на моей памяти не было.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Всегда в 10:35 Славя приходила меня встречать. Всегда около клубов стояли и разговаривали кибернетики.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Сейчас же меня никто не встретил и около клубов было пусто.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '~Так. Надо собраться. Может быть стоит пройтись по лагерю? Или стоит пойти умыться и придти в себя?~',
                           parse_mode='markdown')
        time.sleep(slt)
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Обойти лагерь', callback_data='semen_check_all'))
        kb.add(types.InlineKeyboardButton(text='Пойти к умывальникам', callback_data='semen_goto_wash'))
        world.send_message(user['id'], 'Как поступить?', reply_markup=kb)
        thunder.update_one({'id': user['id']}, {'$set': {'choicing': 1}})


############################################### ПИОНЕР: ПРОБУЖДЕНИЕ ##############################################

def pioner_awaking(user):
    if user != None:
        slt = 3
        long = 5
        pi_user = thunder.find_one({'pioner': 'pioner'})
        world.send_photo(user['id'], '')
        world.send_message(user['id'], 'Я очнулся в бункере, на холодном полу.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Не в автобусе?~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Мне это показалось странным, но потом я вспомнил, что сказала мне Юля в прошлой смене.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '~В лагере будут происходить странные вещи. Эта смена будет последней для всех. И выберется только один...~',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '~Не зря я столько времени готовился к этому! Моё тело значительно сильнее и выносливее всех остальных Семёнов.~',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], 'Я оглядел себя, и злобно ухмыльнулся.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Настало время выбраться отсюда. И я сделаю это, чего бы мне это не стоило.~',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я встал с пола, покопался в ящиках и достал оттуда кухонный нож.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Да начнётся игра... *На выживание!*', parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], '...', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я решил выйти наружу через старый корпус.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'По пути я встретил одного из Семенов, о которых мне говорила Юля. Не составило труда избавиться от конкурента, учитывая тот факт, что у меня было оружие.',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'],
                           'Я ещё много раз встречал их копии, и всегда исход был одним. Они физически не способны противостоять мне. Некоторые из них даже первми пытались кидаться на меня.',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], '~Видимо, не одному мне известно о том, что эта смена последняя.~',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Интересно, был ли среди них "настоящий", как назвала его Юля?~',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'От этой мысли злоба ещё сильнее разгоралась во мне. Мне не хотелось верить в её слова, но подсознательно я понимал, что она права. Ей не было смысла врать мне тогда.',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], '~Плевать. Выберусь отсюда только я.~', parse_mode='markdown')
        time.sleep(slt)
        thunder.update_one({'pioner': 'pioner'}, {'$set': {'nextfunc': 'pioner_gooutbunker', 'ready': 1}})


############################################### СЛАВЯ: ПРОБУЖДЕНИЕ ##############################################

def slavya_awaking(user):
    if user != None:
        slt = 3
        long = 5
        sl_user = thunder.find_one({'pioner': 'slavya'})
        world.send_photo(user['id'], '')
        world.send_message(user['id'], 'Я как обычно проснулась у себя в домике.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Но Жени тут почему-то не было.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Странно... Обычно я просыпаюсь раньше неё.~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Ладно. Наверное, она пошла в библиотеку.~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Я встала с кровати, оделась, и взяв умывальные принадлежности, отправилась приводить себя в порядок.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Пока я шла к умывальникам, я не встретила ни одного человека.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Где все? Неужели сегодня абсолютно весь лагерь решил проспать линейку?~',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Хотя до линейки было еще где-то пол часа, в это время обычно многие просыпаются и идут по своим делам.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я закончила умываться, но обстановка в лагере не давала покоя.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Очень странно. Может, стоит спросить Ольгу Дмитриевну? Или пойти в библиотеку и поговорить с Женей?',
                           parse_mode='markdown')
        time.sleep(slt)
        thunder.update_one({'pioner': 'slavya'}, {'$set': {'choicing': 1}})
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Пойти к Ольге Дмитриевне в домик', callback_data='slavya_check_olga'))
        kb.add(types.InlineKeyboardButton(text='Пойти в библиотеку', callback_data='slavya_check_library'))
        world.send_message(user['id'], 'Как поступить?', reply_markup=kb)


def semen_checkall(user):
    pass


@world.callback_query_handler(func=lambda call: True)
def inline(call):
    user = thunder.find_one({'id': call.from_user.id})
    if call.data == 'semen_check_all':
        if user['choicing'] == 1:
            thunder.update_one({'id': call.from_user.id},
                               {'$set': {'choicing': 0, 'nextfunc': 'semen_checkall', 'ready': 1}})
            thunder_variables.update_one({'name': 'semen_checkall'}, {'$set': {'value': 1}})
            checkall()


def checkall():
    no = 0
    for ids in thunder.find({}):
        if ids['ready'] == 0:
            no = 1
    if no == 0:
        for ids in thunder.find({}):
            dofunc(ids)
        thunder.update_many({}, {'$set': {'nextfunc': None, 'ready': 0}})


def dofunc(user):
    if user['nextfunc'] == 'semen_checkall':
        semen_checkall(user)


@world.message_handler(commands=['remove_event_users'])
def delusersevent(m):
    for ids in thunder.find({}):
        thunder.remove({'id': ids['id']})
    world.send_message(m.chat.id, 'success')

# @world.message_handler(commands=['start_event'])
# def starteventt(m):
#    if m.from_user.id == creator:
#        for ids in thunder_variables.find({}):
#            thunder_variables.remove({'name': ids['name']})
#        thunder_variables.insert_one(createvar('semen_1choice', None))
#        event_thunder_in_paradise()
#        if len(m.text.split()) == 2:
#            try:
#                event_thunder_in_paradise(polunin_pidor=True)
#            except:
#                bot.send_message(mainchat, 'Полунин облажался')
#                world.send_message(mainchat, traceback.format_exc())
#

# def createvar(name, value):
#    return {
#        'name': name,
#        'value': value
#    }
#

# from events import Event  # этот импорт должен быть тут, чтобы избежать ошибок
# from events.scenaries import grom  # как и этот


# def event_thunder_in_paradise(polunin_pidor=False):
#    actives = ['semen', 'pioner', '']
#    pi_user = thunder.find_one({'pioner': 'pioner'})
#    se_user = thunder.find_one({'pioner': 'semen'})
#    if polunin_pidor:
#        event = Event(mainchat, grom)
#        event.add_user(pi_user['id'], 'pioner')
#        event.add_user(se_user['id'], 'semen')
#        return
#    t = threading.Thread(target=pi_sends, args=[pi_user])
#    t.start()
#    for ids in thunder.find({}):
#        if ids['pioner'] != 'pioner':
#            world.send_message(ids['id'], 'Ваш временной промежуток ещё не настал. Ожидайте, история началась...')
#
