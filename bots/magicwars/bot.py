from modules.coach import Coach

coach = Coach()

from telebot import types

import bots.magicwars.battle as game
import bots.magicwars.constants as constants
import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['magic_wars'], config.creator)
games = {}


@bot.message_handler(commands=['help'])
def help_handler(m):
    tts = '/elements - доступные элементы\n' \
          '/battle - начать битву волшебников\n' \
          '/hell - открыть врата в ад\n' \
          '/dungeon - открыть подземелье\n\n'
    tts += """Кастуешь реплаем на бота - кастуешь на мобов
Кастуешь реплаем на юзера - кастуешь на мага
В касте юзаешь до четырех элементов (можно больше но будет выбрано рандомно)
Можно прописать любому мобу или магу защиту от элемента (блокировка жизни, защита от огня)
Если будет защита от жизни, юзер не сможет хилится"""
    bot.reply_to(m, tts)


@bot.message_handler(commands=['elements'])
def elements_handler(m):
    tts = ", ".join([constants.rus(element) for element in constants.elements])
    bot.reply_to(m, f'Доступные элементы: {tts}')


@bot.message_handler(commands=['hell'])
def hell_handler(m):
    games.update({m.chat.id: game.Hell(m.chat.id)})
    bot.send_message(m.chat.id, 'Вы открыли врата в ад!\n/join для присоединения.')


@bot.message_handler(commands=['dungeon'])
def dungeon_handler(m):
    games.update({m.chat.id: game.Dungeon(m.chat.id)})
    bot.send_message(m.chat.id, 'Подземелье открыто!\n/join для присоединения.')


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
    magician = game.Magician(battle, m.from_user.id, m.from_user.first_name)
    joined_users = [user.user_id for user in battle.magicians]
    if m.from_user.id in joined_users:
        bot.reply_to(m, 'Вы уже присоединились.')
        return
    battle.magicians.append(magician)
    bot.reply_to(m, 'Вы присоединились. /start_game для начала игры.')


@bot.message_handler(commands=['pause'])
def pause_handler(m):
    battle = get_game(m.chat.id)
    if not battle:
        bot.reply_to(m, 'Игра не создана. Создайте с помощью /battle.')
        return
    if battle.pause:
        bot.reply_to(m, 'Игра и так на паузе. Нажмите /resume для продолжения.')
        return
    battle.timer.cancel()
    battle.pause = True
    bot.reply_to(m, 'Игра приостановлена.')


@bot.message_handler(commands=['resume'])
def resume_handler(m):
    battle = get_game(m.chat.id)
    if not battle:
        bot.reply_to(m, 'Игра не создана. Создайте с помощью /battle.')
        return
    if not battle.pause:
        bot.reply_to(m, 'Игра и не так на паузе. Нажмите /pause чтобы приостановить.')
        return
    battle.pause = False

    battle.next_turn()


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
    elif len(battle.magicians) < 2 and battle.type == 'battle':
        battle.magicians.append(game.Magician(game))
    battle.next_turn()


@bot.message_handler()
def cast_handler(m):
    battle = get_game(m.chat.id)
    if not battle:
        return
    if not battle.timer:
        return
    if not m.reply_to_message:
        return
    if m.from_user.id not in [user.user_id for user in battle.magicians]:
        return

    magician = [user for user in battle.magicians if user.user_id == m.from_user.id][0]
    if magician.casted:
        return
    target = game.Magician
    if battle.type == 'battle':
        if m.reply_to_message.from_user.id not in [user.user_id for user in battle.magicians]:
            return
        target = [user for user in battle.magicians if user.user_id == m.reply_to_message.from_user.id][0]
    elif battle.type == 'dungeon':
        if m.reply_to_message.from_user.id == bot.get_me().id:
            kb = types.InlineKeyboardMarkup()
            for mob in battle.mobs:
                kb.add(types.InlineKeyboardButton(f'{mob.name} - 🖤️{mob.xp}ХП', callback_data=f'attack?{mob.id}'))
            bot.reply_to(m, 'По ком вы хотите кастануть?', reply_markup=kb)
            return
        else:
            if m.reply_to_message.from_user.id not in [user.user_id for user in battle.magicians]:
                return
            target = [user for user in battle.magicians if user.user_id == m.reply_to_message.from_user.id][0]

    cast = [m.text.lower()]
    if m.text.count(' '):
        cast = m.text.lower().split(' ')
        for element in cast:
            if not magician.init_element(element) == 'defence':
                continue
            if len(cast) < 2:
                break
            cast.remove(element)
            bot.reply_to(m, magician.defend(target, cast))
            return
    bot.reply_to(m, magician.cast(target, cast))


@bot.callback_query_handler(func=lambda c: c.data.split('?')[0] == 'attack')
def attack_callhadler(c):
    battle = get_game(c.message.chat.id)
    if not battle:
        return
    magician = [user for user in battle.magicians if user.user_id == c.from_user.id][0]
    mob_id = int(c.data.split('?')[1])
    target = [mob for mob in battle.mobs if mob.id == mob_id][0]
    cast_text = c.message.reply_to_message.text
    cast = [cast_text.lower()]
    if cast_text.count(' '):
        cast = cast_text.lower().split(' ')
        for element in cast:
            if not magician.init_element(element) == 'defence':
                continue
            if len(cast) < 2:
                break
            cast.remove(element)
            bot.edit_message(magician.defend(target, cast), c.message.chat.id, c.message.message_id)
            return
    bot.edit_message(magician.cast(target, cast), c.message.chat.id, c.message.message_id)


def get_game(chat_id):
    battle = games.get(chat_id)
    if not battle:
        return
    if not battle.exists:
        return
    return battle


from modules.bot_keeper import keeper

keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
