import config
from modules.funcs import BotUtil
from bots.forest.mongohelper import MongoHelper

bot = BotUtil(config.environ['forest'], config.creator)

from pymongo import MongoClient

db_helper = MongoHelper(MongoClient(config.environ['database']))


@bot.message_handler(commands=['fhelp'])
def help_handler(m):
    tts = """
/newgame - создать игру.
/game_info - информация о игре.
/next_turn - следующий ход.
/fme - профиль
/delgame - удалить игру.    

"""
    bot.reply_to(m, tts)


@bot.message_handler(commands=['fstart'])
def start_handler(m):
    if m.text.count(' ') == 0:
        bot.send_message(m.chat.id, 'Вы были ничем не примечательным членом вашей стаи. Все жили в мире, равенстве и '
                                    'покое. Но однажды вы проснулись, и в вашем мозгу заиграла ИДЕЯ. Вы оглянулись и '
                                    'почувствовали родство с вашей стаей. Ваша жизнь никогда не станет прежней, '
                                    'вы обрели разум. Очень скоро такая же способность пришла и к другим вашим '
                                    'собратьям. Вы произнесли речь о том, что время возвышаться, и животный век '
                                    'позади. Вашей стае понравились ваши слова, и они выбрали вас направлять '
                                    'дальнейшее движение стаи. Они пойдут куда вы им скажете, они будут выполнять все '
                                    'что вы хотите. Только от Вас зависит дальнейшая судьба Вас и Вашей стаи.')
        return


@bot.message_handler(commands=['anketa'])
def anketa_handler(m):
    bot.send_message(m.chat.id, """1. Имя вождя.
2. Имя расы (кролики, лисицы, можно сказочных).
3. Необходимо описать чем питается раса, ее время жизни, природных врагов, и т.д. (только для сказочных персонажей)
4. Предпочтительное место локации (смотрите в карту).
5. 2 характеристики на выбор:
    1) Сильные. +2 к силе.
    2) Умные. Одна выбранная технология 1-го уровня дается сразу.
    3) Находчивые. +1 СТ/ход.
    4) Сообразительные. +2Е/ход.
    5) Устрашающие (Многие NPC будут бояться вас).
    6) Удачливые (влияет на ивенты).
    7) Обладающие секретом (секрет случайно выдается в начале игры).
6. Цвет на карте.""")


@bot.message_handler(commands=['accept'])
def accept_handler(m):
    game = db_helper.find_game(m.chat.id)
    if not game['active']:
        bot.reply_to(m, 'Игра не создана.')
        return
    if not m.reply_to_message:
        bot.reply_to(m, 'Не указан получатель. Укажите его реплаем.')
        return
    if game['players'].get(str(m.reply_to_message.from_user.id)):
        bot.reply_to(m, 'Юзер уже присоединился.')
        return
    if not m.from_user.id == game['admin']:
        bot.reply_to(m, 'Может только админ.')
        return
    db_helper.join_game(m.chat.id, m.reply_to_message.from_user)
    bot.reply_to(m, 'Юзер принят!')


@bot.message_handler(commands=['flee'])
def join_handler(m):
    game = db_helper.find_game(m.chat.id)
    if not game['active']:
        bot.reply_to(m, 'Игра не создана.')
        return
    if not m.reply_to_message:
        bot.reply_to(m, 'Не указан получатель. Укажите его реплаем.')
        return
    if not m.from_user.id == game['admin']:
        bot.reply_to(m, 'Может только админ.')
        return
    if not game['players'].get(str(m.reply_to_message.from_user.id)):
        bot.reply_to(m, 'Юзера еще нет в игре.')
        return
    db_helper.leave_game(m.chat.id, m.reply_to_message.from_user)
    bot.reply_to(m, 'Юзер успешно удален из игры.')


@bot.message_handler(commands=['newgame'])
def newgame_handler(m):
    if not db_helper.find_game(m.chat.id)['active']:
        db_helper.create_game(m.chat.id, m.from_user.id)
        bot.send_message(m.chat.id, 'Игра создана!')
        return
    bot.send_message(m.chat.id, 'Игра уже и так есть.')


@bot.message_handler(commands=['game_info'])
def game_info_handler(m):
    game = db_helper.find_game(m.chat.id)
    if not game['active']:
        bot.reply_to(m, 'Игра не создана.')
        return
    tts = 'Айди игры: {}\nАдмин игры: {}\nХод: {}\nЧистота воздуха: {}\nДеревья: {}'
    tts = tts.format(game['id'], bot.get_link('Админ', game['admin']), game['year'], game['air'], game['trees'])
    bot.send_message(m.chat.id, tts, parse_mode='HTML')


@bot.message_handler(commands=['add_air'])
def set_handler(m):
    game = db_helper.find_game(m.chat.id)
    if not game['active']:
        bot.reply_to(m, 'Игра не создана.')
        return
    if not m.from_user.id == game['admin']:
        bot.reply_to(m, 'Может только админ.')
        return
    try:
        count = int(m.text.split(' ')[1])
    except ValueError:
        bot.reply_to(m, 'как я тебе {} выдам блять???!'.format(m.text.split(' ')[1]))
        return
    db_helper.set_air(game['id'], count)
    bot.reply_to(m, 'Выдано.')


@bot.message_handler(commands=['add_trees'])
def set_handler(m):
    game = db_helper.find_game(m.chat.id)
    if not game['active']:
        bot.reply_to(m, 'Игра не создана.')
        return
    if not m.from_user.id == game['admin']:
        bot.reply_to(m, 'Может только админ.')
        return
    try:
        count = int(m.text.split(' ')[1])
    except ValueError:
        bot.reply_to(m, 'как я тебе {} выдам блять???!'.format(m.text.split(' ')[1]))
        return
    db_helper.set_trees(game['id'], count)
    bot.reply_to(m, 'Выдано.')


@bot.message_handler(commands=['debug'])
def debug_handler(m):
    game = db_helper.find_game(m.chat.id)
    if not m.from_user.id == game['admin']:
        bot.reply_to(m, 'Может только админ.')
        return
    game = db_helper.find_game(m.chat.id)
    bot.send_message(m.chat.id, str(game))


@bot.message_handler(commands=['event'])
def event_handler(m):
    game = db_helper.find_game(m.chat.id)
    if not game['active']:
        bot.reply_to(m, 'Игра не создана.')
        return
    if not m.from_user.id == game['admin']:
        bot.reply_to(m, 'Может только админ.')
        return
    if not m.text.count(' '):
        bot.reply_to(m, 'Вы не указали текст ивента.')
        return
    broadcast(game, m.text.split(' ', 1)[1])


@bot.message_handler(commands=['next_turn'])
def next_turn_handler(m):
    game = db_helper.find_game(m.chat.id)
    if not game['active']:
        bot.reply_to(m, 'Игра не создана.')
        return
    if not m.from_user.id == game['admin']:
        bot.reply_to(m, 'Может только админ.')
        return
    db_helper.next_turn(m.chat.id)
    bot.send_message(m.chat.id, 'Прошел год! Ресурсы пришли!')


@bot.message_handler(commands=['delgame'])
def delgame_handler(m):
    game = db_helper.find_game(m.chat.id)
    if not game['active']:
        bot.reply_to(m, 'Игра не создана.')
        return
    if not m.from_user.id == game['admin']:
        bot.reply_to(m, 'Может только админ.')
        return
    db_helper.delete_game(m.chat.id)
    bot.reply_to(m, 'Игра удалена.')


@bot.message_handler(commands=['set_spices'])
def set_country_handler(m):
    game = db_helper.find_game(m.chat.id)
    if not game['active']:
        bot.reply_to(m, 'Игра не создана.')
        return
    if not m.reply_to_message:
        bot.reply_to(m, 'Не указан получатель. Укажите его реплаем.')
        return
    if not m.from_user.id == game['admin']:
        bot.reply_to(m, 'Может только админ.')
        return
    if not game['players'].get(str(m.reply_to_message.from_user.id)):
        bot.reply_to(m, 'Юзер не присоединился.')
        return
    if not m.text.count(' '):
        bot.reply_to(m, 'Вы не выбрали имя стаи.')
        return
    country = m.text.split(' ', 1)[1]
    db_helper.set_country(m.chat.id, m.reply_to_message.from_user, country)
    bot.reply_to(m, 'Вы успешно установили имя стаи!')


@bot.message_handler(commands=['fme'])
def me_handler(m):
    game = db_helper.find_game(m.chat.id)
    if not game['active']:
        bot.reply_to(m, 'Игра не создана.')
        return
    user = m.from_user
    if m.reply_to_message:
        if not user.id == game['admin']:
            bot.reply_to(m, 'Может только админ.')
            return
        user = m.reply_to_message.from_user
    if not game['players'].get(str(user.id)):
        bot.reply_to(m, 'Вы или юзер еще не присоединились.')
        return
    player = game['players'][(str(user.id))]
    tts = """
Имя: {}
Айди: {}
Стая: {}   
Прирост:
{}
Ресурсы:
"""
    resources = player['res']
    growers = player['growth']
    growings = ''
    for growing in growers:
        if int(growers[growing]):
            growings += '{}: {}\n'.format(rus(growing), growers[growing])
    tts = tts.format(player['name'], player['id'], rus(player['country']), growings)
    for resource in list(resources.keys()):
        if int(resources[resource]):
            tts += '{}: {}\n'.format(rus(resource), resources[resource])
    bot.reply_to(m, tts)


@bot.message_handler(commands=['give_res'])
def give_res_handler(m):
    game = db_helper.find_game(m.chat.id)
    give_all = False
    if not game['active']:
        bot.reply_to(m, 'Игра не создана.')
        return
    if not m.from_user.id == game['admin']:
        bot.reply_to(m, 'Может только админ.')
        return
    if not m.reply_to_message:
        give_all = True
    if not give_all:
        if not game['players'].get(str(m.reply_to_message.from_user.id)):
            bot.reply_to(m, 'Юзер еще не присоединился.')
            return
    if m.text.count(' ') < 2:
        bot.reply_to(m, 'Неверное количество аргументов.')
        return
    try:
        resource = m.text.split(' ')[1]
        count = int(m.text.split(' ')[2])
        if give_all:
            for player in game['players']:
                db_helper.give_res(m.chat.id, game['players'][player], resource, count)
        else:
            db_helper.give_res(m.chat.id, m.reply_to_message.from_user, resource, count)
    except ValueError:
        bot.reply_to(m, 'как я тебе {} {} выдам блять???!'.format(m.text.split(' ')[1], m.text.split(' ')[2]))
        return
    bot.reply_to(m, 'Прирост выдан')


@bot.message_handler(commands=['give_growth'])
def give_growth_handler(m):
    game = db_helper.find_game(m.chat.id)
    give_all = False
    if not game['active']:
        bot.reply_to(m, 'Игра не создана.')
        return
    if not m.from_user.id == game['admin']:
        bot.reply_to(m, 'Может только админ.')
        return
    if not m.reply_to_message:
        give_all = True
    if not give_all:
        if not game['players'].get(str(m.reply_to_message.from_user.id)):
            bot.reply_to(m, 'Юзер еще не присоединился.')
            return
    if m.text.count(' ') < 3:
        bot.reply_to(m, 'Неверное количество аргументов.')
        return
    try:
        resource = m.text.split(' ')[1]
        count = int(m.text.split(' ')[2])
        reason = m.text.split(' ', 3)[3]
        if give_all:
            for player in game['players']:
                db_helper.give_growth(m.chat.id, game['players'][player], resource, count, reason)
        else:
            db_helper.give_growth(m.chat.id, m.reply_to_message.from_user, resource, count, reason)
    except ValueError:
        bot.reply_to(m, 'как я тебе {} {} выдам блять???!'.format(resource, m.text.split(' ')[2]))
        return
    bot.reply_to(m, 'Прирост выдан')


@bot.message_handler()
def text_handler(m):
    if not db_helper.find_game(m.chat.id) and m.chat.id != 'private':
        db_helper.create_chat(m.chat.id)


def rus(text):
    rus_names = {
        'food': '🍓Еда',
        'water': '💧Вода',
        'materials': '🧱Материалы'

    }
    if not rus_names.get(text):
        return text
    return rus_names.get(text)


def broadcast(game, text):
    successful = 0
    all_users = len(game['players'])
    for player in game['players']:
        try:
            bot.send_message(game['players'][player]['id'], text)
            successful += 1
        except:
            pass
    bot.send_message(game['id'], 'Рассылка отправлено. Получили {} из {}!'.format(str(successful), str(all_users)))