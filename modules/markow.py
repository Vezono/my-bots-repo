import random

class MarkowChains:
    def __init__(self, db):
        self.__db = db
        self.__allwords = dict()
        self.__end_symbols = ['!', '.', '?', ')']
    def generate(self, sentences=3):
        ctext = ''
        csent = 0
        dic = 'words'
        for i in range(sentences):
            cword = 0
            current_word = ''
            while '&end' not in current_word:
                start = None
                if not cword:
                    start = self.__allwords[dic]['&start']
                    items = []
                    for ids in start:
                        for a in range(start[ids]):
                            items.append(ids)
                    start = random.choice(items)
                    i = 0
                    cwd = ''
                    current_word = start.capitalize()
                    ctext += start + ' '
                else:
                    next_words = []
                    for ids in self.__allwords[dic][current_word]:
                        for count_of_word in range(self.__allwords[dic][current_word][ids]):
                            next_words.append(ids)
                    next_word = random.choice(next_words)
                    endsent = 0
                    if current_word[-1] in endsymbols:
                        endsent = 1
                    current_word = next_word
                    if '&end' not in next_word:
                        i = 0
                        cwd = ''
                        for a in next_word:
                            if a != '@':
                                cwd += a
                        ctext += cwd + ' '
                    else:
                        if endsent == 0:
                            ctext = ctext[:len(ctext) - 1]
                            ctext += '.'
                cword += 1
            csent += 1
            ctext += ' '
        return ctext       
