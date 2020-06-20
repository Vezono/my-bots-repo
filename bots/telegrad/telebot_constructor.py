from telebot import types


class TConstructor:
    def __init__(self):
        pass

    @staticmethod
    def reply_kb(user):
        kb = types.ReplyKeyboardMarkup()
        emoji = '🚶'
        if user['human']['gender'] == 'female':
            emoji = '🚶‍♀️'
        kb.add(types.KeyboardButton(emoji + 'Передвижение'))
        h = user['human']
        if h['position']['flat']:
            kb.add(types.KeyboardButton('🗄' + 'Холодильник'), types.KeyboardButton('🍗' + 'Еда'))
            kb.add(types.KeyboardButton('📱' + 'Искать подработку'), types.KeyboardButton('🛏' + 'Сон'))
            kb.add(types.KeyboardButton('🔐Закрыть/открыть квартиру'))
        kb.add(types.KeyboardButton('👤Профиль'))
        return kb
