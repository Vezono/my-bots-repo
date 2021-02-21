import random

from pymongo import MongoClient

import config


class Database:
    def __init__(self):
        self.phrases = MongoClient(config.environ['database_clear']).bots.phrases

    def answer(self, text):
        answers = []
        for word in text.split():
            answers += self.phrases.aggregate([{'$match': {'question': {'$regex': word}}}, {'$sample': {'size': 1}}])
        if not answers:
            return 'Не понимаю тебя'
        return random.choice(list(answers))['message']

    @staticmethod
    def is_triggered(text):
        if random.randint(1, 100) == 1:
            return True
        for name in {'loshadkin', 'пасюк', 'лошадкин'}:
            if name in text.lower():
                return True
        return False

    def process_message(self, m):
        try:
            _id = self.phrases.find({}).sort({'_id': -1}).limit(1)['_id'] + 1
            question = m.reply_to_message.text if m.reply_to_message else m.text
            doc = {
                '_class': 'Phrase',
                '_id': _id,
                'question': question,
                'message': m.text
            }
            self.phrases.insert_one(doc)
        except:
            pass
