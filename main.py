import config
from modules.funcs import BotUtil

bot = BotUtil('1006055451:AAGta5Mx9nIH6CTal0pirJp-n3wvsq2QKRk', config.creator)
bot.report('Инициализация...')
bot.report(config.environ)

from bots import britbot
from bots import sender
from bots import randomer
from bots import george_bd
from bots import pasuk

from modules.manybotslib import BotsRunner

bots = {
    'Брит': britbot.bot,
    'НейроЮля': sender.bot,
    'Mr. Random': randomer.bot,
    'DB Checker': george_bd.bot,
    'Пасюк': pasuk.bot,
    'Bot Ruler': bot
}

runner = BotsRunner(admins=[config.creator], retries=3, show_traceback=True)
runner.add_bots(bots)
runner.set_main_bot(bot, 'status')
bot.report('Готово! Боты запущены и готовы к работе.')
runner.run()
