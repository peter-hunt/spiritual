from .ability import *
from .smartdata import SmartData

__all__ = ['Piece']


class Piece(SmartData):
    kind: str
    abilities: list[Ability]
