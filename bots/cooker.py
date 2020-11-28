from config import environ, creator
from modules.coach import Coach

coach = Coach()
from modules.eatable import Cooker
from modules.funcs import BotUtil

bot = BotUtil(environ['cooker'])
cooker = Cooker(bot)


def log(m):
    try:
        bot.send_message(creator, f'{m.chat.title}({m.chat_id}):\n\n{m.from_user.first_name}'
                                  f'({m.from_user.id}): {m.text}')
    except:
        pass
    return False


@bot.message_handler(func=lambda m: log(m))
def log(m):
    pass


@bot.message_handler(commands=['help'])
def help_handler(m):
    bot.reply_to(m, '/tea - завари чай.\n/cook - приготовь еды.')


@bot.message_handler(commands=['cook'])
def cook_handler(m):
    if not m.text.count(' '):
        bot.send_message(m.chat.id, 'Вы забыли указать, что именно вы хотите приготовить!')
        return
    meal = m.text.lower().split(' ', 1)[1]
    if m.reply_to_message:
        cooker.cook(m.reply_to_message.message_id, m.from_user, m.reply_to_message.from_user, m.chat, meal)
    else:
        bot.send_message(m.chat.id, m.from_user.first_name + ' сьел(а) ' + meal + '!')


@bot.message_handler(commands=['tea'])
def tea_handler(m):
    if not m.reply_to_message:
        if not m.text.count(' '):
            tea = 'обычный'
        else:
            tea = m.text.split(' ', 1)[1]
        tts = '{} заварил себе чай "{}"!'.format(m.from_user.first_name, tea)
        bot.send_message(m.chat.id, tts)
        return

    from_user = m.from_user
    to_user = m.reply_to_message.from_user
    if m.text.count(' ') == 0:
        tea = 'обычный'
    else:
        tea = m.text.split(' ', 1)[1].replace("<", "&lt;")
    cooker.tea(tea, from_user, to_user, m.chat)


@bot.callback_query_handler(lambda c: True)
def callback_handler(c):
    tts = ''
    action = c.data.split()[0]
    to_user = c.message.entities[1].user
    from_user = c.message.entities[0].user
    to_link = bot.get_link(to_user.first_name, to_user.id)
    from_link = bot.get_link(from_user.first_name, from_user.id)
    if 'eat' in c.data or 'trash' in c.data or 'stay' in c.data:
        meal = c.data.split()[1]
        m_id = c.message.message_id
        if to_user.id == c.from_user.id:
            if action == 'eat':
                tts = f'{to_link} с апетитом сьел(а) блюдо "{meal}" от пользователя {from_link}!'
            elif action == 'stay':
                tts = f'{to_link} решил(а) не есть блюдо "{meal}" от пользователя {from_link}!'
            elif action == 'trash':
                tts = f'{to_link} выбросил(а) блюдо "{meal}" от пользователя {from_link}!'
            bot.edit_message(tts, c.message.chat.id, m_id, reply_markup=None, parse_mode='HTML')
        else:
            bot.answer_callback_query(c.id, 'Это не ваше меню!')
        return
    tea = c.message.text.split('"')[1]
    if to_user.id == c.from_user.id:
        if action == 'drink':
            tts = f'Вы выпили чай "{tea}", {to_link}!'
        elif action == 'reject':
            tts = f'Вы отказались от чая "{tea}", {to_link}!'
        elif action == 'throw':
            tts = f'Вы вылили в унитаз чай "{tea}", {to_link}!!'
        elif action == 'Да':
            tts = f'Вы выпили чай "{tea}", {to_link}!! Спасибо!!!'
        elif action == 'Нет':
            tts = f'Простите, {to_link}.'
    else:
        bot.answer_callback_query(c.id, 'Это не ваш чай!')
        return
    bot.edit_message_text(tts, c.message.chat.id, c.message.message_id, parse_mode='HTML')


from modules.bot_keeper import keeper
keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')