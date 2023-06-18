from numbers import Number
from pathlib import Path

from .smartdata import SmartData

__all__ = ['Profile']


class Profile(SmartData):
    player_name: str

    achievements: dict[str, bool] = {}
    skills: dict[str, Number] = {}
    items: list = []

    last_update: int = 0

    @classmethod
    def new(cls, player_name: str) -> 'Profile':
        return cls(player_name=player_name)

    def save(self):
        with open(Path.home().joinpath('spiritual', 'profiles',
                                       f'{self.player_name}.json'), 'w') as file:
            self.dump(file)
