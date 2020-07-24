import typing
from pymongo import MongoClient
import config
import dataclass_factory
from .book import Book


class Books:
    def __init__(self):
        self.db = MongoClient(config.environ['database']).library
        self.books = self.db.books
        self.factory = dataclass_factory.Factory()
        self.sync_all_books()

    def drop_books(self):
        self.books.drop()

    @property
    def max_book_id(self) -> int:
        ids = {book.id for book in self.all_books}
        ids.add(0)
        return max(ids)

    @property
    def all_books(self) -> typing.List[Book]:
        books = self.books.find({})
        return [self.deserialize_book(book) for book in books]

    @property
    def all_book_dicts(self) -> typing.List[dict]:
        return self.books.find({})

    def sync_book(self, book: Book):
        sample_book_dict = self.form_book_dict()
        book_dict = self.serialize_book(book)
        for line in sample_book_dict:
            if line not in book_dict:
                book_dict.update({line: sample_book_dict[line]})
        self.update_book(book.id, book_dict)

    def sync_all_books(self):
        for book in self.all_books:
            self.sync_book(book)

    def get_book(self, book_id):
        book = self.books.find_one({'id': book_id})
        if not book:
            return None
        return self.deserialize_book(book)

    def get_book_dict(self, book_id):
        book = self.get_book(book_id)
        if not book:
            return None
        return self.serialize_book(book)

    def deserialize_book(self, book) -> Book:
        return self.factory.load(book, Book)

    def serialize_book(self, book: Book) -> dict:
        return self.factory.dump(book)

    def update_book(self, book_id, param, method='$set'):
        self.books.update_one({'id': book_id}, {method: param})

    def form_book_dict(self, **kwargs):
        book = {
            'id': self.max_book_id + 1,
            'readed_by': [],
            'pushed_by': 0,
            'title': 'Unknown',
            'author': 'Unknown',
            'genre': 'Unknown',
            'difficulty': '0',
            'desc': 'Unknown'
        }
        book.update(kwargs)
        return book

    def form_book(self, **kwargs) -> Book:
        book_dict = self.form_book_dict(**kwargs)
        return self.deserialize_book(book_dict)

    def create_book(self, **kwargs) -> Book:
        book_dict = self.form_book_dict(**kwargs)
        self.books.insert_one(book_dict)
        return self.deserialize_book(book_dict)

    def get_user_books(self, user_id):
        return self.filter_books({'pushed_by': user_id})

    def filter_books(self, query):
        books = self.books.find(query)
        return self.deserialize_books(books)

    def deserialize_books(self, books: list) -> typing.List[Book]:
        return [self.deserialize_book(book) for book in books]

    def serialize_books(self, books: typing.List[Book]) -> typing.List[dict]:
        return [self.serialize_book(book) for book in books]
