import time

import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['attorney'], config.creator)

from pymongo import MongoClient

db = MongoClient(config.environ['database'])
rooms = db.attorney.rooms
users = db.attorney.users

from telebot import types

jobs = ['attorney', 'prosecutor', 'judge', 'witness', 'attorney helper', 'prosecutor helper']


@bot.message_handler(commands=['start'])
def start_handler(m):
    get_user(m.from_user.id)
    bot.reply_to(m, 'Привет. Выбери себе имя командой /name и иди в суд командой /rooms.')


@bot.message_handler(commands=['name'])
def name_handler(m):
    if not m.text.count(' '):
        return
    name = m.text.split(' ', 1)[1]
    if not name.isalpha():
        bot.reply_to(m, 'Имя должно состоять из букв!')
        return
    user = get_user(m.from_user.id)
    users.update_one(user, {'$set': {'name': name}})
    bot.reply_to(m, 'Имя успешно изменено. Теперь вы можете идти с ним в зал суда!')


@bot.message_handler(commands=['rooms'])
def rooms_handler(m):
    user = get_user(m.from_user.id)
    free_rooms = [room for room in rooms.find({'active': False})]
    if not free_rooms:
        add_room()
        free_rooms = [room for room in rooms.find({'active': False})]
    kb = types.InlineKeyboardMarkup()
    for room in free_rooms:
        kb.add(types.InlineKeyboardButton(text=room['name'], callback_data=f'join_room?{room["id"]}'))
    bot.send_message(m.from_user.id, 'Выберите комнату для присоединения.', reply_markup=kb)


@bot.message_handler(commands=['profile'])
def profile_handler(m):
    user = get_user(m.from_user.id)
    stats = user["stats"]
    tts = f'Ваш профиль, {m.from_user.first_name}:\n' \
          f'\n' \
          f'Имя в суде: {user["name"]}\n' \
          f'\n' \
          f'🥇Статистика:\n' \
          f'🛡Побед за адвоката: {stats["attorney"]}\n' \
          f'🛡+За его помощника: {stats["attorney helper"]}\n' \
          f'🗡Побед за прокурора: {stats["prosecutor"]}\n' \
          f'🗡+За его помощника: {stats["prosecutor helper"]}\n' \
          f'👨🏻‍⚖️Вынесено вердиктов за судью: {stats["judge"]}\n' \
          f'👨🏻‍⚕️Свидетельств: {stats["witness"]}\n'
    bot.reply_to(m, tts)


@bot.callback_query_handler(func=lambda c: c.data.split('?')[0] == 'join_room')
def join_room(c):
    user = get_user(c.from_user.id)
    room_id = int(c.data.split('?')[1])
    room = rooms.find_one({'id': room_id})
    users.update_one(user, {'$set': {'room': room_id}})
    if room['name'] == 'Пустая комната!':
        users.update_one({'id': user['id']}, {'$set': {'status': 'naming_room'}})
        bot.reply_to(c.message, 'Возможно, вы первый присоединившийся в комнату! Пожалуйста, дайте ей имя.')
        return
    users.update_one(user, {'$set': {'status': 'job_selecting'}})
    kb = types.InlineKeyboardMarkup()
    available_jobs = [job for job in rooms.find_one({'id': room_id}) if job in jobs]
    buttons = [types.InlineKeyboardButton(text=job, callback_data=f'set_job?{job}') for job in available_jobs]
    kb.add(*buttons)
    bot.reply_to(c.message, 'Хорошо! Теперь выберите работу, которую вы будете выполнять в суде!', reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.split('?')[0] == 'set_job')
def set_job(c):
    user = get_user(c.from_user.id)
    job = c.data.split('?')[1]
    room = rooms.find_one({'id': user['room']})
    rooms.update_one(room, {'$set': {job: user['id']}})
    users.update_one(user, {'$set': {'status': 'typing'}})
    bot.reply_to(c.message, f'Отлично! Вы теперь {job}! Можете писать в чат, вас услышат другие участники суда.')


@bot.message_handler()
def handler(m):
    user = get_user(m.from_user.id)
    if user['status'] == 'naming_room':
        if not m.text.isalpha():
            bot.reply_to(m, 'Имя комнаты должно состоять из букв!')
            return
        rooms.update_one({'id': user['room']}, {'$set': {'name': m.text}})
        users.update_one(user, {'$set': {'status': 'job_selecting'}})
        kb = types.InlineKeyboardMarkup()
        available_jobs = [job for job in rooms.find_one({'id': user['room']}) if job in jobs]
        buttons = [types.InlineKeyboardButton(text=job, callback_data=job) for job in available_jobs]
        kb.add(*buttons)
        bot.reply_to(m, 'Хорошо! Теперь выберите работу, которую вы будете выполнять в суде!', reply_markup=kb)
    if user['status'] == 'typing':
        if not user['room']:
            return
        room = rooms.find_one({'id': user['room']})
        members = [member for member in [room[job] for job in room if job in jobs] if member != user['id']]
        user_job = [member for member in [room[job] for job in room if job in jobs] if member == user['id']][0]
        tts = f'{user["name"]}[{user_job}]: {m.text}'
        [bot.send_message(member_id, tts) for member_id in members]


def get_user(user_id):
    user = users.find_one({'id': user_id})
    if not user:
        user = {
            'id': user_id,
            'name': None,
            'stats': {job: 0 for job in jobs},
            'room': None,
            'status': None
        }
        users.insert(user)
    return user


def add_room():
    room = {
        'name': 'Пустая комната!',
        'active': False,
        'id': int(time.time())
    }
    room.update({job: None for job in jobs})
    rooms.insert_one(room)
