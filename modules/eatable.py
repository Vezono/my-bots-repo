from modules.funcs import BotUtil
from telebot import types
import config

class Cooker:

    def __init__(self, bot):
        self.__bot = bot
        self.__bot_helper = BotUtil(self.__bot)

    def tea(self, tea, to_user, from_user, chat, message):
        from_user_link = self.__bot_helper.get_link(to_user.first_name, to_user.id)
        to_user_link = self.__bot_helper.get_link(from_user.first_name, from_user.id)
        kb = types.InlineKeyboardMarkup()
        row1 = list()
        row2 = list()
        for i in ['drink', 'reject']:
            row1.append(types.InlineKeyboardButton(self.__rus(i), callback_data='{} {}'.format(i, to_user.first_name)))
        for i in ['throw']:
            row2.append(types.InlineKeyboardButton(self.__rus(i), callback_data='{} {}'.format(i, to_user.first_name)))
        kb.add(*row1)
        kb.add(*row2)
        if to_user.id == self.__bot.get_me().id:
            tts = 'Не хочу я чай твой, ' + from_user + '!'
            kb = None
        else:
            tts = '{} приготовил чай "{}" для вас, {}!'.format(from_user_link, tea, to_user_link)
        self.__bot_helper.reply(chat.id, tts, message, reply_markup=kb, parse_mode='HTML')

    def cook(self, message, from_user, to_user, chat, meal):
        tts = from_user.first_name + ' приготовил(а) пользователю ' + to_user.first_name + ' ' + meal + '!'
        kb = types.InlineKeyboardMarkup(3)
        buttons1 = [types.InlineKeyboardButton(text='Съесть', callback_data='eat ' + meal),
                    types.InlineKeyboardButton(text='Оставить', callback_data='stay ' + meal),
                    types.InlineKeyboardButton(text='Выбросить', callback_data='trash ' + meal)]
        kb.add(*buttons1)
        self.__bot_helper.reply(chat.id, tts, message, reply_markup=kb)

    def __rus(self, text):
        try:
            return config.r[text]
        except:
            return text