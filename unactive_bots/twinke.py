from pymongo import MongoClient

import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['twinkle'], config.creator)

client = MongoClient(config.environ['database'])
db = client.twinkle
users = db.users


@bot.message_handler()
def text_handler(m):
    if not users.find_one({'id': m.from_user.id}):
        users.insert_one(createtwink(m.from_user))
        return
    users.update_one({'id': m.from_user.id}, {})


de
