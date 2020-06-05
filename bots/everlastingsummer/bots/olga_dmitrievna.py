import time

from modules.funcs import BotUtil
from tokens import environ
from .. import config
from ..mongohelper import MongoHelper

bot = BotUtil(environ['TELEGRAM_TOKEN'])
db = MongoHelper()


class OlgaDmitrievna:
    def __init__(self):
        self.bot = bot
        self.prefix = 'olg'
        self.chache = {}
        self.id = self.bot.get_me().id


olga = OlgaDmitrievna()


@bot.message_handler(commands=['control'])
def olga_start_control(m):
    if m.from_user.id not in db.get_bot_admins(olga.prefix):
        return
    if olga.chache.get('controller'):
        bot.reply_to(m, 'Мной уже управляют!')
        return
    olga.chache.update({'controller': m.from_user.id})
    bot.reply_to(m, 'Ты теперь управляешь мной!')


@bot.message_handler(commands=['stopcontrol'])
def lena_stop_control(m):
    if m.from_user.id not in db.get_bot_admins(olga.prefix):
        return
    if not olga.chache.get('controller'):
        bot.reply_to(m, 'Мной еще не управляют!')
        return
    olga.chache.update({'controller': None})
    bot.reply_to(m, 'Ты больше не управляешь мной!')


@bot.message_handler(commands=['give_control'])
def give_control(m):
    if not m.text.count(' '):
        return
    if m.from_user.id not in config.admins:
        return
    if not m.reply_to_message:
        return
    db.add_bot_admin(m.text.split(" ")[1], m.reply_to_message.from_user.id)
    bot.reply_to(m, f'Я выдала контроль для него на {m.text.split(" ")[1]}')


@bot.message_handler(commands=[f'{olga.prefix}'])
def alisa_control(m):
    if not m.text.count(' '):
        return
    if m.from_user.id not in db.get_bot_admins(olga.prefix):
        return
    bot.delete_message(m.chat.id, m.message_id)
    bot.send_message(m.chat.id, m.text.split(' ', 1)[1], parse_mode='HTML')


@bot.message_handler(commands=['start'])
def start_handler(m):
    if m.chat.type != 'private':
        return
    if db.user_banned(m.from_user.id) or db.get_pioner(m.from_user.id):
        return
    if m.from_user.id not in olga.chache:
        olga.chache.update({m.from_user.id: {
            'name': None,
            'gender': None
        }})
        bot.send_chat_action(m.from_user.id, 'typing')
        time.sleep(4)
        bot.send_message(m.chat.id,
                         'Здраствуй, пионер! Меня зовут Ольга Дмитриевна, я буду твоей вожатой. '
                         'Впереди тебя ждёт интересная жизнь в лагере "Совёнок"! '
                         'А сейчас скажи нам, как тебя зовут (следующим сообщением).')
        return


@bot.message_handler()
def text_handler(m):
    if m.text[0] == '/':
        return
    if olga.chache.get('controller') == m.from_user.id:
        bot.send_message(m.chat.id, m.text)
        bot.delete_message(m.chat.id, m.message_id)
    if m.chat.type != 'private':
        return
    if db.user_banned(m.from_user.id) or db.get_pioner(m.from_user.id):
        return
    if m.from_user.id not in olga.chache:
        bot.reply_to(m, 'Вы не зарегестрированы. Нажмите /start')
    if len(m.text) > 12:
        return
    if not olga.chache[m.from_user.id]['name']:
        if not m.text.isalpha():
            bot.reply_to(m, 'Нет нет! Таких имен не бывает!')
            return
        olga.chache[m.from_user.id]['name'] = m.text
        bot.send_message(m.chat.id,
                         'Отлично! И еще одна просьба... Прости конечно, но это нужно для документа, в котором '
                         'хранится информация обо всех пионерах. Я, конечно, сама вижу, но это надо сделать твоей '
                         'рукой. Напиши вот тут свой пол (М или Д).')
        return
    if not olga.chache[m.from_user.id]['gender']:
        if m.text.lower() not in ['м', 'д']:
            bot.reply_to(m, 'Нет нет! Таких полов не бывает!')
            return
        olga.chache[m.from_user.id]['gender'] = m.text
        bot.send_message(m.chat.id,
                         f'Добро пожаловать в лагерь, {olga.chache[m.from_user.id]["name"]}! Заходи в '
                         f'@everlastingsummerchat, и знакомься с остальными пионерами! Через пять минут я запишу тебя '
                         f'во все документы.')
        db.create_pioner(m.from_user, olga.chache[m.from_user.id]['name'], olga.chache[m.from_user.id]['gender'])
