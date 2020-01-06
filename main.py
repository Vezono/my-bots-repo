from timeit import default_timer as timer
start_time = timer()

import config
from modules.funcs import BotUtil
from telebot import types

bot = BotUtil('1006055451:AAGta5Mx9nIH6CTal0pirJp-n3wvsq2QKRk', config.creator)
bot.report('Инициализация...')

from bots import britbot
from bots import sender
from bots import randomer
from bots import george_bd
from bots import pasuk

from modules.manybotslib import BotsRunner

bots = {
    'Брит': britbot.bot,
    'НейроЮля': sender.bot,
    'Mr.Random': randomer.bot,
    'DB_Checker': george_bd.bot,
    'Пасюк': pasuk.bot,
    'Bot_Ruler': bot
}


@bot.message_handler(commands=['os'])
def ret_os(m):
    if m.from_user.id == config.creator:
        bot.report(str(config.environ).replace(', ', ',\n\n'))


@bot.message_handler(commands=['bots'])
def setup_bots(m):
    if not m.from_user.id == config.creator:
        return
    buttons = []
    kb = types.InlineKeyboardMarkup()
    for botrun in list(bots.keys()):
        kb.add(types.InlineKeyboardButton(text=botrun, callback_data=botrun))
    bot.send_message(m.chat.id, 'Ваши боты:', reply_markup=kb)


@bot.callback_query_handler(func=lambda call:True)
def inline(c):
    botname = c.data.split(' ')[0]
    if not c.data.count(' '):
        tts = 'Настройка бота {}.'.format(botname)
        kb = types.InlineKeyboardMarkup()
        for func in ['status']:
            kb.add(types.InlineKeyboardButton(text=func, callback_data=botname+' '+func))
        bot.edit_message(chat_id=c.from_user.id, message_id=c.message.message_id, message_text=tts, reply_markup=kb)
        return
    task = c.data.split(' ')[1]
    if task == 'status':
        bot.report(runner.get_status()[botname])

runner = BotsRunner(admins=[config.creator], retries=3, show_traceback=True)
runner.add_bots(bots)
runner.set_main_bot(bot, 'status')
bot.report('Готово! Боты запущены и готовы к работе.\nВремени использовано: '+str(int(timer() - start_time)) + ' секунд.')
runner.run()

