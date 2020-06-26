import telebot
from pymongo import MongoClient
from telebot import types

import config

token = config.environ['spamer_base']
bot = telebot.TeleBot(token)

db = MongoClient(config.environ['database'])
users = db.spamer_base.users
admins = db.spamer_base.admins


@bot.message_handler(commands=['admin'])
def admin_handler(m):
    if m.from_user.id != config.creator:
        return
    if not m.reply_to_message:
        return
    admins.insert_one({
        'id': m.reply_to_message.from_user.id
    })


@bot.message_handler(commands=['high'])
def high_handler(m):
    if not admins.find_one({'id': m.from_user.id}):
        return
    if not m.text.count(' '):
        bot.reply_to(m, 'Вы забыли указать айдишники.')
    spamers = [user_id for user_id in m.text.split(' ') if user_id.isdigit()]
    for spamer in spamers:
        spamer = users.find_one({'id': spamer})
        if not spamer:
            users.insert_one({'id': spamer})
        users.update_one({'id': spamer}, {'risk': 'high'})
    bot.reply_to(m, f'Сделал спамерами следующих юзеров: {", ".join(spamers)}')


@bot.message_handler(commands=['middle'])
def middle_handler(m):
    if not admins.find_one({'id': m.from_user.id}):
        return
    if not m.text.count(' '):
        bot.reply_to(m, 'Вы забыли указать айдишники.')
    spamers = [user_id for user_id in m.text.split(' ') if user_id.isdigit()]
    for spamer in spamers:
        spamer = users.find_one({'id': spamer})
        if not spamer:
            users.insert_one({'id': spamer})
        users.update_one({'id': spamer}, {'risk': 'middle'})
    bot.reply_to(m, f'Сделал возможно-спамерами следующих юзеров: {", ".join(spamers)}')


@bot.message_handler(commands=['low'])
def low_handler(m):
    if not admins.find_one({'id': m.from_user.id}):
        return
    if not m.text.count(' '):
        bot.reply_to(m, 'Вы забыли указать айдишники.')
    spamers = [user_id for user_id in m.text.split(' ') if user_id.isdigit()]
    for spamer in spamers:
        spamer = users.find_one({'id': spamer})
        if not spamer:
            users.insert_one({'id': spamer})
        users.update_one({'id': spamer}, {'risk': 'low'})
    bot.reply_to(m, f'Простил следующих юзеров: {", ".join(spamers)}')


@bot.message_handler(content_types=['new_chat_members'])
def new_member_handler(m):
    if bot.get_chat_member(m.chat.id, bot.get_me().id).status != 'administrator':
        bot.reply_to(m, 'Я не админ и не могу проверить, спамер ли это. Дайте права админа. Желательно фулл.')
    user = users.find_one({'id': m.new_chat_members[0].id})
    kick = types.InlineKeyboardButton(text='Кикнуть', callback_data=f'kick {user["id"]}')
    ban = types.InlineKeyboardButton(text='Забанить', callback_data=f'ban {user["id"]}')
    stay = types.InlineKeyboardButton(text='Оставить', callback_data=f'stay {user["id"]}')
    if user['risk'] == 'middle':
        kb = types.InlineKeyboardMarkup()
        kb.add(ban, kick, stay)
        bot.reply_to(m, 'У этого пользователя средний уровень риска спамера. Что делаем?', reply_markup=kb)
    elif user['risk'] == 'high':
        bot.unban_chat_member(m.chat.id, user['id'])
        bot.reply_to(m, 'Спамер. Кикнул его нахуй. Нехуй было добавлять в группы ебаные.')


@bot.callback_query_handler(func=lambda c: c.data.split()[0] == 'ban')
def ban(c):
    target = int(c.data.split()[1])
    bot.kick_chat_member(c.message.chat.id, target)
    bot.edit_message_text('Забанил его.', c.message.chat.id, c.message.id)


@bot.callback_query_handler(func=lambda c: c.data.split()[0] == 'kick')
def kick(c):
    target = int(c.data.split()[1])
    bot.unban_chat_member(c.message.chat.id, target)
    bot.edit_message_text('Кикнул его.', c.message.chat.id, c.message.id)


@bot.callback_query_handler(func=lambda c: c.data.split()[0] == 'stay')
def stay(c):
    bot.edit_message_text('Оставил его.', c.message.chat.id, c.message.id)
