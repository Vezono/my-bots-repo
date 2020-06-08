import random
import threading

from bots.everlastingsummer.pioner import Pioner
from modules.funcs import BotUtil
from .. import config
from ..config import environ
from ..mongohelper import MongoHelper

bot = BotUtil(environ['electronic'])
db = MongoHelper()


class Electronic:
    def __init__(self):
        self.bot = bot
        self.id = self.bot.get_me().id
        self.name = 'Electronic'
        self.prefix = 'ele'
        self.chat_id = config.chat_id
        self.cache = {}

    def game(self, players=None):
        new_players = []
        if players is None:
            players = self.cache['players']
            new_players = ['Ульяна', 'Алиса', 'Лена', 'Мику', 'Славя', 'Женя']
        self.cache['game'] = False
        if not players:
            self.bot.send_message(self.chat_id, 'Недостаточно игроков для начала турнира! '
                                                'Придется играть в следующий раз.')
            return
        if len(players + new_players) == 1:
            name = players[0]
            if isinstance(name, Pioner):
                name = name.name
            self.bot.send_message(self.chat_id, f'Встречайте победителя: {name}')
            return
        if not len(players + new_players) % 2:
            if new_players:
                new_players.remove(random.choice(new_players))
            else:
                player = random.choice(players)
                players.remove(player)
                if isinstance(player, Pioner):
                    player = player.name
                bot.send_message(self.chat_id, f'Игроку {player} стало нехорошо и он вышел.')
        tts = 'Вот вам турнирная сетка на данный этап:\n\n'
        grid = [[] for i in range(len(new_players + players) // 2)]
        all_players = new_players + players
        for pair in grid:
            for i in range(2):
                player = random.choice(all_players)
                pair.append(player)
                all_players.remove(player)
            tts += ' VS '.join([player for player in pair if not isinstance(player, Pioner)]
                               +
                               [player.name for player in pair if isinstance(player, Pioner)])
            tts += '\n'
        self.bot.send_message(self.chat_id, tts)
        players = []
        for pair in grid:
            pair.remove(random.choice(pair))
            players.append(pair[0])
        threading.Timer(30, self.game, args=[players]).start()


electronic = Electronic()


@bot.message_handler(commands=['control'])
def start_control(m):
    if m.from_user.id not in db.get_bot_admins(electronic.prefix):
        return
    if electronic.cache.get('controller'):
        bot.reply_to(m, 'Мной уже управляют!')
        return
    electronic.cache.update({'controller': m.from_user.id})
    bot.reply_to(m, 'Ты теперь управляешь мной!')


@bot.message_handler(commands=['stopcontrol'])
def stop_control(m):
    if m.from_user.id not in db.get_bot_admins(electronic.prefix):
        return
    if not electronic.cache.get('controller'):
        bot.reply_to(m, 'Мной еще не управляют!')
        return
    electronic.cache.update({'controller': None})
    bot.reply_to(m, 'Ты больше не управляешь мной!')


@bot.message_handler(commands=[f'{electronic.prefix}'])
def control(m):
    if not m.text.count(' '):
        return
    if m.from_user.id not in db.get_bot_admins(electronic.prefix):
        return
    bot.delete_message(m.chat.id, m.message_id)
    bot.send_message(m.chat.id, m.text.split(' ', 1)[1])


@bot.message_handler()
def text_handler(m):
    if m.text[0] == '/':
        return
    if m.reply_to_message and m.text == 'Хочу принять участие в турнире!' and electronic.cache.get('cards'):
        if m.reply_to_message.from_user.id == bot.get_me().id:
            pioner = db.get_pioner(m.from_user.id)
            if pioner in electronic.cache['players']:
                bot.reply_to(m, 'Я уже тебя записал!')
                return
            electronic.cache['players'].append(pioner)
            bot.reply_to(m, 'Хорошо, записал тебя.')
    if electronic.cache.get('controller') != m.from_user.id:
        return
    bot.send_message(m.chat.id, m.text)
    bot.delete_message(m.chat.id, m.message_id)
