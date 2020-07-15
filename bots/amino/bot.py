import time

from amino import SubClient
from pymongo import MongoClient

from .config import *

chat_methods = {
    "0:0": 'text_message',
    "0:100": 'image_message',
    "0:103": 'youtube_message',
    "2:110": 'voice_message',
    "3:113": 'sticker_message',
    "101:0": 'group_member_join',
    "102:0": 'group_member_leave',
    "103:0": 'chat_invite'
}


class Bot:
    def __init__(self):
        self.db = MongoClient(mongo_token).amino.readed
        self.client = SubClient(comId=com_id, profile='')
        self.client.login(email=email, password=password)
        self.client.activity_status(1)
        self.client.check_in()

        self.text_handlers = {}
        self.method_handlers = {}

    def handle_messages(self):
        readed = self.readed
        result = []
        for m in self.get_messages():
            if m['messageId'] not in readed and m["uid"] != self.client.userId:
                result.append(m)
                readed.append(m['messageId'])
        self.update_readed(readed)
        return result

    @property
    def readed(self):
        return self.db.find_one({})['readed']

    def get_messages(self):
        result = []
        # for thread in self.client.get_chat_threads().json:
        # result += self.client.get_chat_messages(thread['threadId'], 5).json
        result += self.client.get_chat_messages(cn_id, 5).json
        return result

    def update_readed(self, readed):
        self.db.update_one({}, {'$set': {'readed': readed}})

    def message_handler(self, command=None, content_type=None):
        def decorator(handler):
            if content_type:
                message_type = [method for method in chat_methods
                                if content_type == chat_methods[method]][0]
                self.method_handlers.update({message_type: handler})
                return handler
            self.text_handlers.update({command: handler})
            return handler

        return decorator

    def polling(self, speed=1, none_stop=True):
        while none_stop:
            try:
                self.operate()
                time.sleep(speed)
            except:
                pass

    def operate(self):
        for m in self.handle_messages():
            print(m)
            message_type = f'{m["type"]}:{m["mediaType"]}'
            if message_type in self.method_handlers:
                self.method_handlers[message_type](m)
            if message_type == '0:0':
                for handler in self.text_handlers:
                    if m['content'].startswith(handler):
                        self.text_handlers[handler](m)
