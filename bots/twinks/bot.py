from modules.coach import Coach

coach = Coach()

from config import environ
from .manager import Manager

manager = Manager(5, api_id=int(environ['api_id']), api_hash=environ['api_hash'])

from telebot import TeleBot

bot = TeleBot(environ['twink_bot'])

institut = -1001217288970
prince_message = 1580


@bot.message_handler(commands=['earn'])
def earn_h(m):
    bot.send_message(m.from_user.id, f'{manager.earn_yuliacoins(institut, prince_message)}')


from modules.bot_keeper import keeper

keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
