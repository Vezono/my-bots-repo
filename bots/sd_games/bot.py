import telebot
from emoji import UNICODE_EMOJI
from telebot import types

import config

token = config.environ['walker']
bot = telebot.TeleBot(token)
from .game import Game

game = Game()


@bot.message_handler(commands=['start'])
def join_handler(m):
    if str(m.from_user.id) in game.players:
        return
    game.create_player(m.from_user)
    player = str(m.from_user.id)
    kb = get_kb(player)
    bot.send_message(player, 'Карта', reply_markup=kb)


@bot.message_handler()
def emoji_handler(m):
    if m.text not in UNICODE_EMOJI:
        return
    game.players[str(m.from_user.id)]['icon'] = m.text
    bot.reply_to(m, 'Иконка обновлена.')


@bot.callback_query_handler(func=lambda c: c)
def call(c: types.CallbackQuery):
    player_id = str(c.from_user.id)
    pos = game.players[player_id]['pos']
    near = game.get_near(pos)
    if c.data not in near:
        bot.answer_callback_query(c.id, 'Сюда нельзя.')
        return
    if game.map[c.data] == 'goat':
        game.map[c.data] = 'nothing'
        game.players[player_id]['goats'] += 1
        bot.answer_callback_query(c.id, f'Вы получили казу! Теперь у вас {game.players[player_id]["goats"]} коз.')
    game.players[player_id]['pos'] = c.data
    game.down_data()
    kb = get_kb(player_id)
    bot.edit_message_text(f'Карта. Козы: {game.players[player_id]["goats"]} Координаты: {pos}', c.message.chat.id,
                          c.message.message_id, reply_markup=kb)


def get_kb(user_id: str) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(5)
    pos = game.players[user_id]['pos']
    visible = game.get_map(pos)
    encounter = 1
    row = []
    for tile in visible:
        row.append(types.InlineKeyboardButton(text=game.get_icon(tile), callback_data=tile))
        if encounter == 5:
            kb.add(*row)
            encounter = 0
            row = []
        encounter += 1
    return kb
