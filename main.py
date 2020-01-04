from bots import britbot
from bots import sender
from bots import randomer
from bots import george_bd
from bots import pasuk

import config

from modules.manybotslib import BotsRunner

from modules.funcs import BotUtil

bot = BotUtil('1006055451:AAGta5Mx9nIH6CTal0pirJp-n3wvsq2QKRk')

bots = {
    'Брит': britbot.bot,
    'НейроЮля': sender.bot,
    'Mr. Random': randomer.bot,
    'DB Checker': george_bd.bot,
    'Пасюк': pasuk.bot,
    'Bot Ruler': bot
}

runner = BotsRunner(admins=(config.creator), retries=3, show_traceback=True)
runner.add_bots(bots)
runner.set_main_bot(bot, 'status')

runner.run()
