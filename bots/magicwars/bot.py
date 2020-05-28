import bots.magicwars.battle as game
import bots.magicwars.constants as constants
import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['magic_wars'], config.creator)
games = {}


@bot.message_handler(commands=['help'])
def help_handler(m):
    tts = '/elements - доступные элементы\n' \
          '/battle - начать игру'
    bot.reply_to(m, tts)


@bot.message_handler(commands=['elements'])
def elements_handler(m):
    tts = ", ".join([constants.rus(element) for element in constants.elements])
    bot.reply_to(m, f'Доступные элементы: {tts}')


@bot.message_handler(commands=['battle'])
def battle_handler(m):
    games.update({m.chat.id: game.Game(m.chat.id)})
    bot.send_message(m.chat.id, 'Начинаю набор колдунов!\n/join для присоединения.')


@bot.message_handler(commands=['join'])
def join_handler(m):
    battle = get_game(m.chat.id)
    if not battle:
        bot.reply_to(m, 'Игра не создана. Создайте с помощью /battle.')
        return
    if battle.turn:
        return
    magician = game.Magician(m.from_user.id, m.from_user.first_name)
    joined_users = [user.user_id for user in battle.magicians]
    if m.from_user.id in joined_users:
        bot.reply_to(m, 'Вы уже присоединились.')
        return
    battle.magicians.append(magician)
    bot.reply_to(m, 'Вы присоединились. /start_game для начала игры.')


@bot.message_handler(commands=['start_game'])
def start_game_handler(m):
    battle = get_game(m.chat.id)
    if not battle:
        bot.reply_to(m, 'Игра не создана. Создайте с помощью /battle.')
        return
    if battle.turn:
        return
    if not battle.magicians:
        bot.reply_to(m, 'Слишком мало игроков.')
        return
    elif len(battle.magicians) < 2:
        battle.magicians.append(game.Magician())
    battle.next_turn()


@bot.message_handler()
def cast_handler(m):
    battle = get_game(m.chat.id)
    if not battle:
        return
    if not m.reply_to_message:
        return
    if m.reply_to_message.from_user.id not in [user.user_id for user in battle.magicians]:
        return
    magician = None
    enemy = None

    for user in battle.magicians:
        if user.user_id == m.reply_to_message.from_user.id:
            enemy = user
        if user.user_id == m.from_user.id:
            magician = user

    if magician.casted:
        return

    cast = [m.text.lower()]
    if m.text.count(' '):
        cast = m.text.lower().split(' ')
    bot.reply_to(m, magician.cast(enemy, cast))


def get_game(chat_id):
    battle = games.get(chat_id)
    if not battle:
        return
    if not battle.exists:
        return
    return battle
