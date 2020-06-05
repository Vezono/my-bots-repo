import random
import threading

from modules.funcs import BotUtil
from .. import config
from ..config import environ
from ..mongohelper import MongoHelper

bot = BotUtil(environ['alisa'])
db = MongoHelper()


class Alisa:
    def __init__(self):
        self.bot = bot
        self.id = self.bot.get_me().id
        self.name = 'Alisa'
        self.prefix = 'ali'
        self.chat_id = config.chat_id
        self.cache = {}
        self.common_help_text = '{}, смотри, куда идёшь! Должен будешь, и долг отработаешь прямо сейчас.' \
                                ' Мне тут помощь нужна в одном деле...'
        self.respective_help_text = '{}, привет, я же знаю, что ты любишь повеселиться! Готов на этот раз?'
        self.help_texts = ['Отлично! Значит так, нам с Ульяной нужен отвлекающий на кухню...',
                           'Ну пошли, там нужно один прикол с Электроником намутить...']
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
        bot.send_sticker(config.chat_id, 'CAADAgADOQADgi0zDztSbkeWq3BEAg')

    def help_timeout(self):
        db.increase_value(self.cache['help'], {f'respects.{self.name}': -1})
        del self.cache['help']


alisa = Alisa()


@bot.message_handler(commands=['control'])
def alisa_start_control(m):
    if m.from_user.id not in db.get_bot_admins(alisa.prefix):
        return
    if alisa.cache.get('controller'):
        bot.reply_to(m, 'Мной уже управляют!')
        return
    alisa.cache.update({'controller': m.from_user.id})
    bot.reply_to(m, 'Ты теперь управляешь мной!')


@bot.message_handler(commands=['stopcontrol'])
def alisa_start_control(m):
    if m.from_user.id not in db.get_bot_admins(alisa.prefix):
        return
    if not alisa.cache.get('controller'):
        bot.reply_to(m, 'Мной еще не управляют!')
        return
    alisa.cache.update({'controller': None})
    bot.reply_to(m, 'Ты больше не управляешь мной!')


@bot.message_handler(commands=[f'{alisa.prefix}'])
def control(m):
    if not m.text.count(' '):
        return
    if m.from_user.id not in db.get_bot_admins(alisa.prefix):
        return
    bot.delete_message(m.chat.id, m.message_id)
    bot.send_message(m.chat.id, m.text.split(' ', 1)[1])


@bot.message_handler()
def text_handler(m):
    if m.text[0] == '/':
        return
    if alisa.cache.get('controller') == m.from_user.id:
        bot.send_message(m.chat.id, m.text)
        bot.delete_message(m.chat.id, m.message_id)
    if not m.reply_to_message:
        return
    if m.reply_to_message.from_user.id != bot.get_me().id:
        return
    if m.from_user.id != alisa.cache.get('help'):
        return
    bot.reply_to(m, random.choice(alisa.help_texts))
    db.increase_value(m.from_user.id, {f'respects.{alisa.name}': 4})
    alisa.help_timer.cancel()
    del alisa.cache['help']
