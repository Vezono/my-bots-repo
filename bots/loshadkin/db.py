import random

from pymongo import MongoClient

import config


class Database:
    def __init__(self):
        self.db = MongoClient(config.environ['database']).loshadkin
        self.two_g = self.db.converted
        self.three_g = self.db.third_gen

        self.pairs = dict()
        self.message_list = set()

        self.alpha = False

        self.sync()

    def init_pairs(self):
        paired_array = self.three_g.find_one({})['pairs']
        for pair in paired_array:
            q = pair['q']
            a = pair['a']
            self.pairs.update({q: a})

    def init_messages(self):
        messages_doc = self.two_g.find_one({})
        for index in messages_doc:
            message = messages_doc[index]
            if not message:
                continue
            if index == '_id':
                continue
            self.message_list.add(message)

    def sync(self):
        self.init_pairs()
        self.init_messages()

    def two_g_answer(self, text):
        text = text.lower()
        text = text.replace('ты', 'я')
        answers = set()
        for message in self.message_list:
            for word in message.split():
                if word.lower() in text.split():
                    answers.add(message)
        if not answers:
            return 'Не понимаю тебя'
        return random.choice(list(answers))

    def three_g_answer(self, text):
        text = text.lower()
        text = text.replace('ты', 'я')
        answers = set()
        for q in self.pairs:
            a = self.pairs[q]
            for word in text.split():
                if word.lower() in text.split():
                    answers.add(a)
        if not answers:
            return 'Не понимаю тебя'
        return random.choice(list(answers))

    def insert_message(self, text):
        self.two_g.update_one({}, {text.replace('.', ''): text})
        self.sync()

    def insert_pair(self, q, a):
        packet = {
            'q': q,
            'a': a
        }
        self.three_g.update_one({}, {'$push': {'pairs': packet}})
        self.sync()

    def is_triggered(self, text):
        if random.randint(1, 100) == 1:
            return True
        for name in {'loshadkin', 'пасюк', 'лошадкин'}:
            if name in text.lower():
                return True
        return False

    def process_message(self, m):
        if m.reply_to_message:
            if m.reply_to_message.text:
                self.insert_pair(m.reply_to_message.text, m.text)
        else:
            self.insert_message(m.text)
