from dataclasses import dataclass


@dataclass
class Book:
    id: int
    readed_by: list
    pushed_by: int = 0
    title: str = 'Unknown'
    author: str = 'Unknown'
    genre: str = 'Unknown'
    difficulty: str = '0'
    desc: str = 'Unknown'
