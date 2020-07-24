from modules.coach import Coach

coach = Coach()

import telebot
import config

token = config.environ['TOKEN']
bot = telebot.TeleBot(token)


@bot.message_handler()
def text_handler(m):
    pass


from modules.bot_keeper import keeper
keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
