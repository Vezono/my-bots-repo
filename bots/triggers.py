import telebot
from pymongo import MongoClient
from modules.coach import Coach
coach = Coach()
import config

teachers = [792414733]

token = config.environ['god']
bot = telebot.TeleBot(token)

client = MongoClient(config.environ['database'])
db = client.triggerbot
triggs = db.triggs


@bot.message_handler(commands=['gettriggers'])
def gettriggers(m):
    triggers = triggs.find_one({'chat': m.chat.id})
    chat_triggers = {}
    for trigger in triggers.keys():
        chat_triggers.update({trigger: triggers[trigger]})
    tts = 'Ваши триггеры:\n\n'
    t = 0
    for trigger in chat_triggers.keys():
        tts += '{} : {}\n\n'.format(trigger, chat_triggers[trigger])
    bot.reply_to(m, tts)


@bot.message_handler(commands=['addtrigger'])
def addtrigger(m):
    if m.text.count(' ') and m.text.count('/') == 2:
        text = m.text.split(' ', 1)
        args = text[1].split('/')
        triggs.update_one({'chat': m.chat.id}, {'$set': {args[0]: args[1]}})
        bot.reply_to(m, 'Триггер успешно добавлен!')


@bot.message_handler()
def texthandler(m):
    if not triggs.find_one({'chat': m.chat.id}):
        triggs.insert_one({'chat': m.chat.id})
    else:
        pass
    chat_triggers = {}
    triggers = triggs.find_one({'chat': m.chat.id})
    del triggers['_id']
    del triggers['chat']
    for trigger in triggers:
        chat_triggers.update({trigger: triggers[trigger]})
    for i in chat_triggers.keys():
        if i in m.text.lower():
            bot.reply_to(m, chat_triggers[i])


from modules.bot_keeper import keeper
keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')