from telebot import types
import config
from telebot import types

import config


class Cooker:

    def __init__(self, bot):
        self.__bot = bot

    def tea(self, tea, to_user, from_user, chat):
        from_user_link = self.__bot.get_link(to_user.first_name, to_user.id)
        to_user_link = self.__bot.get_link(from_user.first_name, from_user.id)
        kb = types.InlineKeyboardMarkup()
        row1 = list()
        row2 = list()
        for i in ['drink', 'reject']:
            row1.append(types.InlineKeyboardButton(self.__rus(i), callback_data='{} {}'.format(i, str(to_user.id))))
        for i in ['throw']:
            row2.append(types.InlineKeyboardButton(self.__rus(i), callback_data='{} {}'.format(i, str(to_user.id))))
        kb.add(*row1)
        kb.add(*row2)
        if to_user.id == self.__bot.get_me().id:
            tts = 'Не хочу я чай твой, ' + from_user + '!'
            kb = None
        else:
            tts = '{} приготовил чай "{}" для вас, {}!'.format(from_user_link, tea, to_user_link)
        self.__bot.send_message(chat.id, tts, reply_markup=kb, parse_mode='HTML')

    def cook(self, message, from_user, to_user, chat, meal):
        from_user_link = self.__bot.get_link(to_user.first_name, to_user.id)
        to_user_link = self.__bot.get_link(from_user.first_name, from_user.id)
        tts = '{} приготовил(а) пользователю {} {}!'.format(to_user_link, from_user_link, meal)
        kb = types.InlineKeyboardMarkup(3)
        buttons1 = [types.InlineKeyboardButton(text='Съесть', callback_data='eat ' + meal),
                    types.InlineKeyboardButton(text='Оставить', callback_data='stay ' + meal),
                    types.InlineKeyboardButton(text='Выбросить', callback_data='trash ' + meal)]
        kb.add(*buttons1)
        self.__bot.reply(chat.id, tts, message, reply_markup=kb, parse_mode='HTML')

    def __rus(self, text):
        try:
            return config.r[text]
        except:
            return text