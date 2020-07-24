from dataclasses import dataclass


@dataclass
class User:
    id: int
    readed: list
    pushed: list
    points: int = 0
    name: str = 'Unknown'
