import random
import threading

from modules.funcs import BotUtil
from .. import config
from ..config import environ
from ..mongohelper import MongoHelper

bot = BotUtil(environ['lena'])
db = MongoHelper()


class Lena:
    def __init__(self):
        self.bot = bot
        self.id = self.bot.get_me().id
        self.name = 'Lena'
        self.prefix = 'len'
        self.chat_id = config.chat_id
        self.cache = {}
        self.common_help_text = '{}, привет. Ты можешь мне помочь?'
        self.respective_help_text = '{}, привет! Ты мне часто помогаешь, поэтому хотелось бы попросить тебя о помощи ' \
                                    'еще раз... Не откажешь?'

        self.help_texts = ['Спасибо! Тогда пошли, мне нужно отсортировать лекарства в медпункте.',
                           'Спасибо! Пойдём, надо разобрать склад и принести несколько'
                           ' комплектов пионерской формы для Слави.']
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
        bot.send_sticker(config.chat_id, 'CAADAgADaQADgi0zD9ZBO-mNcLuBAg')

    def help_timeout(self):
        db.increase_value(self.cache['help'], {f'respects.{self.name}': -1})
        del self.cache['help']


lena = Lena()


@bot.message_handler(commands=['control'])
def start_control(m):
    if m.from_user.id not in db.get_bot_admins(lena.prefix):
        return
    if lena.cache.get('controller'):
        bot.reply_to(m, 'Мной уже управляют!')
        return
    lena.cache.update({'controller': m.from_user.id})
    bot.reply_to(m, 'Ты теперь управляешь мной!')


@bot.message_handler(commands=['stopcontrol'])
def stop_control(m):
    if m.from_user.id not in db.get_bot_admins(lena.prefix):
        return
    if not lena.cache.get('controller'):
        bot.reply_to(m, 'Мной еще не управляют!')
        return
    lena.cache.update({'controller': None})
    bot.reply_to(m, 'Ты больше не управляешь мной!')


@bot.message_handler(commands=[f'{lena.prefix}'])
def control(m):
    if not m.text.count(' '):
        return
    if m.from_user.id not in db.get_bot_admins(lena.prefix):
        return
    bot.delete_message(m.chat.id, m.message_id)
    bot.send_message(m.chat.id, m.text.split(' ', 1)[1])


@bot.message_handler()
def text_handler(m):
    if m.text[0] == '/':
        return
    if lena.cache.get('controller') == m.from_user.id:
        bot.send_message(m.chat.id, m.text)
        bot.delete_message(m.chat.id, m.message_id)
    if not m.reply_to_message:
        return
    if m.reply_to_message.from_user.id != bot.get_me().id:
        return
    if m.from_user.id != lena.cache.get('help'):
        return
    bot.reply_to(m, random.choice(lena.help_texts))
    db.increase_value(m.from_user.id, {f'respects.{lena.name}': 4})
    lena.help_timer.cancel()
    del lena.cache['help']
