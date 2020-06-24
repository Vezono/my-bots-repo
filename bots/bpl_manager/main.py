from pymongo import MongoClient

import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['bpl_manager'], config.creator)
db = MongoClient(config.environ['database'])

chats = db.bpl_manager.chats


@bot.message_handler(content_types=['new_chat_members'])
def new_chat_handler(m):
    if m.new_chat_members[0].id != bot.get_me().id:
        return
    chat = get_chat(m.chat.id)


def get_chat(chat_id):
    chat = chats.find_one({'id': chat_id})
    if not chat:
        chat = {
            'id': chat_id,
            'init_progress': 0,
            'blocked': False,
        }
        chats.insert_one(chat)
    return chat
