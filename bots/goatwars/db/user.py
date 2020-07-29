from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    milk: int = 0
    exp: int = 0
