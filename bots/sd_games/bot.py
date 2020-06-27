import threading

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


@bot.message_handler(commands=['warp'])
def warp_handler(m):
    if not m.text.count(' '):
        return
    pos = m.text.split()[1]
    if pos.count('_') != 1:
        return
    player = str(m.from_user.id)
    game.players[player]['pos'] = pos
    kb = get_kb(player)
    bot.send_message(player, 'Карта', reply_markup=kb)


@bot.message_handler()
def emoji_handler(m):
    if m.text not in UNICODE_EMOJI:
        return
    game.players[str(m.from_user.id)]['icon'] = m.text
    bot.reply_to(m, 'Иконка обновлена.')


@bot.callback_query_handler(func=lambda c: c.data == 'place')
def call(c: types.CallbackQuery):
    player_id = str(c.from_user.id)
    pos = game.players[player_id]['pos']
    if game.players[player_id]['bricks'] <= 0:
        bot.answer_callback_query(c.id, 'У вас нет кирпичей!')
    game.map[pos] = 'wall'
    game.players[player_id]['bricks'] -= 1
    bot.answer_callback_query(c.id, 'Вы построили стену!')


@bot.callback_query_handler(func=lambda c: '_' in c.data)
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
    if game.map[c.data] == 'brick':
        game.map[c.data] = 'nothing'
        game.players[player_id]['bricks'] += 1
        bot.answer_callback_query(c.id,
                                  f'Вы получили кирпич! Теперь у вас {game.players[player_id]["bricks"]} кирпичей.')
    if game.map[c.data] == 'wall':
        threading.Timer(60, game.map.update, args=[{c.data: 'nothing'}]).start()
        bot.answer_callback_query(c.id, f'Вы уебали стену. Она разрушится через минуту.')
        return
    game.players[player_id]['pos'] = c.data
    game.down_data()
    kb = get_kb(player_id)
    bot.edit_message_text(f'Карта. '
                          f'\nКозы: {game.players[player_id]["goats"]}'
                          f'\n Координаты: {pos}'
                          f'\nКирпичи: {game.players[player_id]["bricks"]}',
                          c.message.chat.id, c.message.message_id, reply_markup=kb)


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
    kb.add(types.InlineKeyboardButton(text='Положить кирпич (спавнит стену)', callback_data='place'))
    return kb
