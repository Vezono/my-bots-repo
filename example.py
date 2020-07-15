from modules.coach import Coach

coach = Coach()

import telebot
import config

token = config.environ['TOKEN']
bot = telebot.TeleBot(token)


@bot.message_handler()
def text_handler(m):
    pass


print(f'Booted in {coach.time()}.')
