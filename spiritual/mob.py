from .piece import Piece
from .smartdata import SmartData

__all__ = ['Mob']


class Mob(SmartData):
    name: str
    pieces: list[Piece]
    abilities: list[str]
    drops: list[str]
