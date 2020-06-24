import random
import threading
import time

from pymongo import MongoClient
from telebot import types, TeleBot

from .bot import Bot
from .config import *

db = MongoClient(mongo_token)
users = db.amino.users
bar_db = db.amino.bar
potions_db = db.amino.potions
calendar_db = db.amino.calendar

calendar = calendar_db.find_one({})
del calendar['_id']

bot = Bot()
t_bot = TeleBot(t_token)


@t_bot.message_handler(commands=['potions'])
def potions_handler(m):
    reload_bar()
    kb = types.InlineKeyboardMarkup()
    for name in potions:
        kb.add(types.InlineKeyboardButton(text=name, callback_data=name))
    t_bot.reply_to(m, 'Что хотите посмотреть?', reply_markup=kb)


@t_bot.message_handler(commands=['weapons'])
def weapons_handler(m):
    t_bot.reply_to(m, weapons, parse_mode='HTML')


@t_bot.message_handler(commands=['map'])
def map_handler(m):
    t_bot.reply_to(m, map_text, parse_mode='HTML')


@t_bot.message_handler(commands=['employers'])
def employers_handler(m):
    t_bot.reply_to(m, employers, parse_mode='HTML')


@t_bot.message_handler(commands=['rules'])
def rules_handler(m):
    t_bot.reply_to(m, rules, parse_mode='HTML')


@t_bot.message_handler(commands=['museum'])
def museum_handler(m):
    tts = '<b>Национальный музей клубничной культуры:</b>'
    for shelf in museum:
        item = museum[shelf]
        tts += f'\n{shelf}. {item["name"]}, {item["count"]} шт.'
    t_bot.reply_to(m, tts, parse_mode='HTML')


@t_bot.message_handler(commands=['bar'])
def bar_handler(m):
    reload_bar()
    kb = types.InlineKeyboardMarkup()
    for name in bar:
        kb.add(types.InlineKeyboardButton(text=name, callback_data=name))
    t_bot.reply_to(m, 'Что хотите посмотреть?', reply_markup=kb)


@t_bot.message_handler(commands=['calendar'])
def calendar_handler(m):
    mon, day = str(time.localtime()[1]), str(time.localtime()[2])
    if len(mon) == 1:
        mon = f'0{mon}'
    if len(day) == 1:
        day = f'0{day}'
    tts = '<b>Календарь</b>:\n'
    today = f'{day} {mon}'
    for date in calendar:
        if date == today:
            tts += f'<b>[{date}]</b> - {calendar[date]}\n'
        else:
            tts += f'{date} - {calendar[date]}\n'
    t_bot.send_message(m.chat.id, tts, parse_mode='HTML')


@t_bot.message_handler(commands=['potion'])
def add_handler(m):
    if m.from_user.id != tg_brit_id:
        return
    text = m.text.split(' ', 1)[1]
    count = int(text.split("/", 3)[0])
    name = text.split('/', 3)[1]
    drink = text.split('/', 3)[2]
    desc = text.split('/', 3)[3]
    potions_db.update_one({}, {'$set': {
        f'{name}.{drink}':
            {'count': count,
             'desc': desc}
    }})
    reload_bar()
    t_bot.reply_to(m, f'Добавила зелье "{drink}" в категорию {name} с количеством {count} и описанием "{desc}" '
                      f'и обновила зелья.')


@t_bot.message_handler(commands=['add'])
def add_handler(m):
    if m.from_user.id != tg_brit_id:
        return
    text = m.text.split(' ', 1)[1]
    count = int(text.split("/", 3)[0])
    name = text.split('/', 3)[1]
    drink = text.split('/', 3)[2]
    desc = text.split('/', 3)[3]
    bar_db.update_one({}, {'$set': {
        f'{name}.{drink}':
            {'count': count,
             'desc': desc}
    }})
    reload_bar()
    t_bot.reply_to(m, f'Добавила напиток "{drink}" в категорию {name} с количеством {count} и описанием "{desc}" '
                      f'и обновила бар.')


@t_bot.message_handler(commands=['today'])
def today_handler(m):
    if m.from_user.id != tg_brit_id:
        return
    date = f'{m.text.split(" ", 3)[1]} {m.text.split(" ", 3)[2]}'
    holiday = m.text.split(' ', 3)[3]
    calendar_db.update_one({}, {'$set': {
        date: holiday
    }})
    global calendar
    calendar = calendar_db.find_one({})
    del calendar['_id']
    t_bot.reply_to(m, f'Добавила праздник "{holiday}" с датой {date} и обновила календарь.')


@t_bot.message_handler()
def txt_handler(m):
    if m.chat.id != tg_cn_id:
        return
    tts = f'[tg][{m.from_user.first_name}]: {m.text}'
    bot.client.send_message(cn_id, tts)


@t_bot.message_handler(content_types=['new_chat_members'])
def txt_handler(m):
    tts = f'[tg]{m.new_chat_members[0].first_name} присоединился к чату'
    bot.client.send_message(cn_id, tts)


@t_bot.callback_query_handler(func=lambda c: c.data in potions)
def call_handler(c):
    if c.from_user.id != c.message.reply_to_message.from_user.id:
        return
    tts = f'<b>{c.data}:</b>\n'
    kb = types.InlineKeyboardMarkup()
    for drink in potions[c.data]:
        if potions[c.data][drink]["count"] <= 0:
            return
        kb.add(types.InlineKeyboardButton(text=f'{drink}: {potions[c.data][drink]["count"]} шт.',
                                          callback_data=f'{c.data}?{drink}'))
    kb.add(types.InlineKeyboardButton(text=f'Назад.', callback_data=f'back'))
    t_bot.edit_message_text(tts, c.message.chat.id, c.message.message_id, reply_markup=kb, parse_mode='HTML')


@t_bot.callback_query_handler(func=lambda c: c.data in bar)
def call_handler(c):
    if c.from_user.id != c.message.reply_to_message.from_user.id:
        return
    tts = f'<b>{c.data}:</b>\n'
    kb = types.InlineKeyboardMarkup()
    for drink in bar[c.data]:
        if bar[c.data][drink]["count"] <= 0:
            return
        kb.add(types.InlineKeyboardButton(text=f'{drink}: {bar[c.data][drink]["count"]} шт.',
                                          callback_data=f'{c.data}?{drink}'))
    kb.add(types.InlineKeyboardButton(text=f'Назад.', callback_data=f'back'))
    t_bot.edit_message_text(tts, c.message.chat.id, c.message.message_id, reply_markup=kb, parse_mode='HTML')


@t_bot.callback_query_handler(func=lambda c: c.data == 'back')
def back_handler(c):
    if c.from_user.id != c.message.reply_to_message.from_user.id:
        return
    kb = types.InlineKeyboardMarkup()
    for name in bar:
        kb.add(types.InlineKeyboardButton(text=name, callback_data=name))
    t_bot.edit_message_text('Что хотите посмотреть?', c.message.chat.id, c.message.message_id, reply_markup=kb)


@t_bot.callback_query_handler(func=lambda c: c.data.split(' ', 1)[0] == 'accept')
def accept_handler(c):
    if c.from_user.id != tg_brit_id:
        return
    name = c.data.split(' ', 1)[1].split('?')[0]
    drink = c.data.split(' ', 1)[1].split('?')[1]
    bar_db.update_one({}, {'$inc': {f'{name}.{drink}.count': -0.2}})
    tts = f'{c.message.reply_to_message.from_user.first_name} выпил(а) {drink}!'
    reload_bar()
    t_bot.edit_message_text(tts, c.message.chat.id, c.message.message_id)


@t_bot.callback_query_handler(func=lambda c: c.data.split(' ')[0] == 'request')
def request_handler(c):
    if c.from_user.id != c.message.reply_to_message.from_user.id:
        return
    name = c.data.split(' ', 1)[1].split('?')[0]
    drink = c.data.split(' ', 1)[1].split('?')[1]
    tts = f'Ожидайте, пока Брит одобрит выдачу напитка.'
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Одобрить.', callback_data=f'accept {name}?{drink}'))
    t_bot.edit_message_text(tts, c.message.chat.id, c.message.message_id, reply_markup=kb)


@t_bot.callback_query_handler(func=lambda c: '?' in c.data and c.data.split('?')[0] in bar)
def drink_handler(c):
    if c.from_user.id != c.message.reply_to_message.from_user.id:
        return
    name = c.data.split('?')[0]
    drink = c.data.split('?')[1]
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Выпить.', callback_data=f'prequest {c.data}'))
    kb.add(types.InlineKeyboardButton(text='Назад.', callback_data=name))
    tts = f'Название: {drink}\nКоличество: {bar[name][drink]["count"]}\nОписание: {bar[name][drink]["desc"]}'
    t_bot.edit_message_text(tts, c.message.chat.id, c.message.message_id, reply_markup=kb)


@t_bot.callback_query_handler(func=lambda c: '?' in c.data and c.data.split('?')[0] in potions)
def drink_handler(c):
    if c.from_user.id != c.message.reply_to_message.from_user.id:
        return
    name = c.data.split('?')[0]
    drink = c.data.split('?')[1]
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Выпить.', callback_data=f'request {c.data}'))
    kb.add(types.InlineKeyboardButton(text='Назад.', callback_data=name))
    tts = f'Название: {drink}\nКоличество: {potions[name][drink]["count"]}\nОписание: {potions[name][drink]["desc"]}'
    t_bot.edit_message_text(tts, c.message.chat.id, c.message.message_id, reply_markup=kb)


@bot.message_handler(command='/online')
def online_handler(m):
    bot.client.activity_status(1)
    bot.client.send_message(m['threadId'], 'Теперь онлайн!', replyTo=m['messageId'])


@bot.message_handler(command='/offline')
def offline_handler(m):
    bot.client.activity_status(1)
    bot.client.send_message(m['threadId'], 'Теперь оффлайн!', replyTo=m['messageId'])


@bot.message_handler(command='/ping')
def ping_handler(m):
    bot.client.activity_status(1)
    bot.client.send_message(m['threadId'], 'Понг!', replyTo=m['messageId'])


@bot.message_handler(command='/random')
def random_handler(m):
    if m['content'].count(' ') < 2:
        bot.client.send_message(m['threadId'], 'Вы забыли указать аргументы!')
        return

    args = m['content'].split(' ')
    args.remove('/random')
    for arg in args:
        if not arg.isdigit():
            return
    bot.client.send_message(m['threadId'], f'Результат: {random.randint(int(args[0]), int(args[1]))}')


@bot.message_handler(command='/watch_ad')
def ad_handler(m):
    response = bot.client.watch_ad
    money = bot.client.get_wallet_info.totalCoinsFloat
    bot.client.send_message(m['threadId'], f'Успешно посмотрел рекламу с кодом {response}. На счету сейчас: {money}',
                            replyTo=m['messageId'])


@bot.message_handler(content_type='text_message')
def text_handler(m):
    if m["threadId"] != cn_id:
        return
    tts = f'[amino][{m["author"]["nickname"]}]: {m["content"]}'
    t_bot.send_message(tg_cn_id, tts)


@bot.message_handler(content_type='voice_message')
def voice_handler(m):
    pass
    # bot.client.send_message(m['threadId'], 'Твои голосовые тут никому не нужны иди нахуй')


@bot.message_handler(content_type='group_member_join')
def join_handler(m):
    bot.client.send_message(m['threadId'], f'Добро пожаловать к нашему шалашу, {m["author"]["nickname"]}')
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Забанить', callback_data=f'ban {m["uid"]}'),
           types.InlineKeyboardButton(text='Оставить', callback_data=f'stay'))
    t_bot.send_message(tg_cn_id, f'К амино чату джойнулся  {m["author"]["nickname"]}. Что будем делать?',
                       reply_markup=kb)


@bot.message_handler(content_type='group_member_leave')
def join_handler(m):
    bot.client.send_message(m['threadId'], f'Пока, {m["author"]["nickname"]}')
    t_bot.send_message(tg_cn_id, f'Из амино чата ливнул  {m["author"]["nickname"]}.')


@t_bot.callback_query_handler(func=lambda c: c.data.split(' ')[0] == 'ban')
def c_ban_handler(c):
    if c.from_user.id != tg_brit_id:
        return
    user_id = c.data.split(' ')[1]
    bot.client.kick(user_id, cn_id)
    tts = c.message.text.split(' Что будем делать?')[0] + ' Он успешно заблокирован.'
    t_bot.edit_message_text(tts, tg_cn_id, c.message_id)


@t_bot.callback_query_handler(func=lambda c: c.data.split(' ')[0] == 'stay')
def c_ban_handler(c):
    if c.from_user.id != tg_brit_id:
        return
    tts = c.message.text.split(' Что будем делать?')[0]
    t_bot.edit_message_text(tts, tg_cn_id, c.message_id)


def get_user(user_id):
    user = users.find_one({'id': user_id})
    if not user:
        commit = {
            'id': user_id,
            'inventory': {}
        }
        users.insert_one(commit)
        return commit
    return user


def reload_bar():
    global potions
    potions = potions_db.find_one({})
    del potions['_id']
    try:
        global bar
        bar = bar_db.find_one({})
        del bar['_id']
    except:
        pass
    return bar


potions = {}
bar = reload_bar()


def boot():
    threading.Thread(target=bot.polling, args=[0]).start()
    threading.Thread(target=t_bot.polling, args=[True]).start()
