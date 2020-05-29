import os
import traceback

import telebot

from .constants import *

world = telebot.TeleBot(os.environ['worldtoken'])


@world.message_handler(commands=['rp'])
def rp_handler(m):
    if m.from_user.id == creator:
        global nowrp
        nowrp = not nowrp
        world.send_message(m.chat.id, 'now ' + str(nowrp))


@world.message_handler(commands=['switch'])
def switch_handler(m):
    if m.from_user.id == creator:
        global rds
        rds = not rds
        world.reply_to(m, f'now {rds}')


@world.message_handler(commands=['do'])
def do_handler(m):
    if not m.text.count(' '):
        return
    if m.from_user.id != creator:
        return
    cmd = m.text.split(' ', 1)[1]
    try:
        eval(cmd)
        world.send_message(m.chat.id, 'Success')
    except:
        world.send_message(creator, traceback.format_exc())
