import random
import threading

from modules.funcs import BotUtil
from .. import config
from ..config import environ
from ..mongohelper import MongoHelper

bot = BotUtil(environ['miku'])
db = MongoHelper()


class Miku:
    def __init__(self):
        self.bot = bot
        self.id = self.bot.get_me().id
        self.name = 'Miku'
        self.prefix = 'mik'
        self.chat_id = config.chat_id
        self.cache = {}
        self.common_help_text = '{}, привет. Ты можешь мне помочь? '
        self.respective_help_text = '{}, привет! Ты мне часто помогаешь, поэтому хотелось бы попросить тебя о помощи ' \
                                    'еще раз... Не откажешь?'

        self.help_texts = ['У меня просто писька болит, можешь пососа...'
                           ' Ой, извини, загооврилась немного. Поможешь с гитарой? Она просто растроилась '
                           'а сама починить ее не могу. Я конечно могла попроси...']
        self.help_timer = None

    def help_request(self):
        pioner = random.choice(db.get_pioners())
        user_link = bot.get_link(pioner.name, pioner.id)
        tts = self.common_help_text.format(user_link)
        if pioner.respects[self.name] > 85:
            tts = self.respective_help_text.format(user_link)
        self.cache.update({'help': pioner.id})
        self.help_timer = threading.Timer(150, self.help_timeout)
        self.help_timer.start()
        bot.send_message(config.chat_id, tts, parse_mode='HTML')
        bot.send_sticker(config.chat_id, 'CAACAgIAAxkBAAEIBExe2m0xX_DDQZzvPXtYf73DPJM7BAACewADgi0zD0LrKNP7bYCXGgQ')

    def help_timeout(self):
        db.increase_value(self.cache['help'], {f'respects.{self.name}': -1})
        del self.cache['help']


miku = Miku()


@bot.message_handler(commands=['control'])
def start_control(m):
    if m.from_user.id not in db.get_bot_admins(miku.prefix):
        return
    if miku.cache.get('controller'):
        bot.reply_to(m, 'Мной уже управляют!')
        return
    miku.cache.update({'controller': m.from_user.id})
    bot.reply_to(m, 'Ты теперь управляешь мной!')


@bot.message_handler(commands=['stopcontrol'])
def stop_control(m):
    if m.from_user.id not in db.get_bot_admins(miku.prefix):
        return
    if not miku.cache.get('controller'):
        bot.reply_to(m, 'Мной еще не управляют!')
        return
    miku.cache.update({'controller': None})
    bot.reply_to(m, 'Ты больше не управляешь мной!')


@bot.message_handler(commands=[f'{miku.prefix}'])
def control(m):
    if not m.text.count(' '):
        return
    if m.from_user.id not in db.get_bot_admins(miku.prefix):
        return
    bot.delete_message(m.chat.id, m.message_id)
    bot.send_message(m.chat.id, m.text.split(' ', 1)[1])


@bot.message_handler()
def text_handler(m):
    if m.text[0] == '/':
        return
    if miku.cache.get('controller') == m.from_user.id:
        bot.send_message(m.chat.id, m.text)
        bot.delete_message(m.chat.id, m.message_id)
    if not m.reply_to_message:
        return
    if m.reply_to_message.from_user.id != bot.get_me().id:
        return
    if m.from_user.id != miku.cache.get('help'):
        return
    bot.reply_to(m, random.choice(miku.help_texts))
    db.increase_value(m.from_user.id, {f'respects.{miku.name}': 4})
    miku.help_timer.cancel()
    del miku.cache['help']
