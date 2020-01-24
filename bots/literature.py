from telebot import types

from pymongo import MongoClient

from config import *
from modules.eatable import Cooker
from modules.funcs import BotUtil

client = MongoClient(environ['database'])
db = client.litbot
users = db.users
books = db.books

bot = BotUtil(environ['litbot'], creator=creator)
cooker = Cooker(bot)


@bot.message_handler(commands=['start'])
def start(m):
    if not m.text.count(' '):
        return
    book_id = int(m.text.split(' ')[1])
    book = books.find_one({'id': book_id})
    tts = '📖Книга {}\n\n👤Автор: {}\n📄Кол-во страниц: {}\n🏷Категория: {}'
    tts = tts.format(book['title'], book['author'], str(book['pages']), book['category'])
    bot.reply_to(m, tts)


@bot.message_handler(commands=['profile'])
def profile(m):
    user = users.find_one({'id': m.from_user.id})
    if not user:
        user = create_user(m.from_user)
    tts = '👤Профиль {}:\n\n📄Кол-во страниц: {}\n📖Кол-во книг: {}\n🏅Репутация: {}'
    tts = tts.format(user['name'], str(user['pages']), str(len(user['books'])), str(user['reputation']))
    bot.reply_to(m, tts)


@bot.message_handler(commands=['search'])
def search(m):
    mongo_shelve = books.find()
    shelve = []
    for book in mongo_shelve:
        shelve.append(book)
    if not m.text.count(' '):
        bot.reply_to(m, 'Вы не указали книгу!')
        return
    tts = 'Найдено книг:\n'
    for book in shelve:
        if m.text.split(' ')[1].lower() in book['title'].lower():
            tts += '\n<a href="t.me/g_literature_bot?start={}">'.format(str(book['id'])) + book['title'].capitalize() + '</a>'
    bot.reply_to(m, tts, parse_mode='HTML')


@bot.message_handler(commands=['books'])
def biblioteca(m):
    mongo_shelve = books.find()
    shelve = []
    for book in mongo_shelve:
        shelve.append(book)
    if not shelve:
        bot.reply_to(m, 'В библиотеке пусто!')
        return
    bot.reply_to(m, 'Книг в библиотеке: '+str(len(shelve)))


@bot.message_handler(commands=['add_book'])
def add_book(m):
    if m.from_user.id != creator:
        return
    if m.text.count('\\') < 3:
        bot.reply_to(m, 'Недостаточно аргументов!')
        return
    book = dict()
    query = m.text.split(' ', 1)[1].split('\\')
    book['title'] = query[1].capitalize()
    book['author'] = query[2]
    book['pages'] = int(query[3])
    book['category'] = query[4]
    create_book(book)
    bot.report(str(book))
    bot.reply_to(m, 'Книга успешно добавлена!')


@bot.message_handler(commands=['devbooks'])
def dev_biblioteca(m):
    if m.from_user.id != creator:
        return
    mongo_shelve = books.find()
    shelve = []
    for book in mongo_shelve:
        shelve.append(book)
    if not shelve:
        bot.reply_to(m, 'В библиотеке пусто!')
        return
    bot.reply_to(m, str(shelve))


def create_user(user):
    commit = {
        'name': user.first_name,
        'id': user.id,
        'pages': 0,
        'coins': 0,
        'reputation': 0,
        'books': []
    }
    return users.insert_one(commit)


def create_book(book):
    mongo_shelve = books.find()
    shelve = []
    for book in mongo_shelve:
        shelve.append(book)
    commit = {
        'title': book['title'],
        'id': len(shelve) + 1,
        'author': book['author'],
        'pages': book['pages'],
        'category': book['category'],
        'readers': []
    }
    return books.insert_one(commit)
