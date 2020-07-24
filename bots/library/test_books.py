from .books import Books


class TestBooks(Books):
    def __init__(self):
        super().__init__()
        self.books = self.db.test_books
