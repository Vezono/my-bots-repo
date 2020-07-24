from modules.coach import Coach

coach = Coach()

from telebot import TeleBot, types
import config

token = config.environ['library']
bot = TeleBot(token)

from .users import Users
from .books import Books
from .test_books import TestBooks

users = Users()
books = Books()
test_books = TestBooks()
book_repo = test_books

temp = dict()


@bot.message_handler(commands=['library'])
def library_handler(m):
    kb = types.InlineKeyboardMarkup(2)
    kb.add(
        types.InlineKeyboardButton(text='По автору', callback_data='search author'),
        types.InlineKeyboardButton(text='По названию', callback_data='search title'),
        types.InlineKeyboardButton(text='По жанру', callback_data=f'search genre'),
    )
    bot.reply_to(m, 'Поиск по:', reply_markup=kb)


@bot.message_handler(commands=['add_book'])
def add_book(m):
    if m.chat.type != 'private':
        bot.reply_to(m, 'Работает только в лс.')
        return
    book = book_repo.create_book(pushed_by=m.from_user.id)
    bot.reply_to(m,
                 f'Вы создали книгу.\n\n{form_book_msg(book)}\n\nЧто хотите поменять?\n\n',
                 reply_markup=form_book_kb(book))


@bot.message_handler(commands=['profile'])
def profile_handler(m):
    users.sync_tg_user(m.from_user)
    user = users.get_user(m.from_user.id)
    tts = f'Имя: {user.name}\n\n' \
          f'Статистика:\n' \
          f'Прочитано книг: {len(user.readed)}\n' \
          f'Добавлено книг: {len(book_repo.get_user_books(m.from_user.id))}'
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Мои книги', callback_data='my_books 0'))
    bot.reply_to(m, tts, reply_markup=kb)


@bot.message_handler(commands=['drop'])
def drop_handler(m):
    book_repo.drop_books()
    bot.reply_to(m, 'Dropped.')


@bot.message_handler()
def text_handler(m):
    users.sync_tg_user(m.from_user)
    if m.chat.type != 'private':
        return
    if m.from_user.id not in temp:
        return
    user_data = temp[m.from_user.id]
    if user_data['type'] == 'edit':
        book_repo.update_book(user_data['book_id'], {user_data['line']: m.text})
        book = book_repo.get_book(user_data['book_id'])
        kb = form_book_kb(book)
        kb.add(types.InlineKeyboardButton(text='В список книг', callback_data='my_books 0'))
        bot.edit_message_text(form_book_msg(book),
                              m.from_user.id,
                              user_data['msg'].message_id,
                              reply_markup=kb)
    elif user_data['type'] == 'search':
        book_list = []
        for book in book_repo.all_books:
            for word in m.text.lower().split(' '):
                if word in book.title.lower():
                    if book not in book_list:
                        book_list.append(book)
        kb = book_list_kb(book_list)
        bot.edit_message_text(
            'Книги по вашему запросу: ',
            m.from_user.id,
            user_data['msg'].message_id,
            reply_markup=kb
        )
    bot.delete_message(m.from_user.id, m.message_id)
    del temp[m.from_user.id]


@bot.callback_query_handler(func=lambda c: c.data.startswith('my_books'))
def callback_handler(c):
    if c.from_user.id != c.message.reply_to_message.from_user.id:
        return
    page = int(c.data.split(' ')[1])
    book_list = book_repo.get_user_books(c.from_user.id)
    kb = book_list_kb(book_list, page)
    bot.edit_message_text('Ваши книги.', c.message.chat.id, c.message.message_id, reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith('search '))
def callback_handler(c):
    if c.from_user.id != c.message.reply_to_message.from_user.id:
        return
    line = c.data.split(' ')[1]
    temp.update({
        c.from_user.id: {
            'line': line,
            'msg': c.message,
            'type': 'search'
        }
    })
    bot.edit_message_text('Введите текст запроса: ', c.message.chat.id, c.message.message_id)


@bot.callback_query_handler(func=lambda c: c.data.startswith('v '))
def callback_handler(c):
    if c.from_user.id != c.message.reply_to_message.from_user.id:
        return
    book_id = int(c.data.split(' ')[1])
    book = book_repo.get_book(book_id)
    kb = form_book_kb(book)
    kb.add(types.InlineKeyboardButton(text='Назад в список книг', callback_data='my_books 0'))
    bot.edit_message_text(form_book_msg(book),
                          c.message.chat.id, c.message.message_id,
                          reply_markup=kb)


@bot.callback_query_handler(func=lambda c: '?' in c.data)
def callback_handler(c):
    line = c.data.split('?')[0]
    book_id = int(c.data.split('?')[1])
    temp.update({
        c.from_user.id: {
            'book_id': book_id,
            'line': line,
            'msg': c.message,
            'type': 'edit'
        }
    })
    bot.edit_message_text(f'Вы хотите изменить поле {line}. Отправьте его значение следующим значением.',
                          c.from_user.id, c.message.message_id)


def form_book_kb(book):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Название', callback_data=f'title?{book.id}'))
    kb.add(types.InlineKeyboardButton(text='Автор', callback_data=f'author?{book.id}'))
    kb.add(types.InlineKeyboardButton(text='Жанр', callback_data=f'genre?{book.id}'))
    kb.add(types.InlineKeyboardButton(text='Сложность', callback_data=f'difficulty?{book.id}'))
    kb.add(types.InlineKeyboardButton(text='Описание', callback_data=f'desc?{book.id}'))
    return kb


def form_book_msg(book):
    tts = f'Айди книги: #{book.id}#\n'
    tts += f'Название: {book.title}\n'
    tts += f'Автор: {book.author}\n'
    tts += f'Жанр: {book.genre}\n'
    tts += f'Сложность: {book.difficulty}\n'
    tts += f'Описание: {book.desc}'
    return tts


def book_list_kb(book_list, number=0):
    kb = types.InlineKeyboardMarkup()
    pages = []
    page = []
    for index in range(len(book_list)):
        if index % 5 == 0 and index != 0:
            pages.append(page.copy())
            page = []
        book = book_list[index]
        page.append(types.InlineKeyboardButton(text=book.title, callback_data=f'v {book.id}'))
        if index == len(book_list) - 1:
            pages.append(page.copy())
    if number in range(len(pages)) or -number in range(len(pages)):
        page = pages[number]
    else:
        page = []
    for button in page:
        kb.add(button)
    kb.add(
        types.InlineKeyboardButton(text='<', callback_data=f'my_books {number - 1}'),
        types.InlineKeyboardButton(text='>', callback_data=f'my_books {number + 1}')
    )
    kb.add(types.InlineKeyboardButton(text=f'Страница: {number + 1}', callback_data=f'my_books {number}'))
    return kb


from modules.bot_keeper import keeper
keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
