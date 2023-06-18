from pathlib import Path

__all__ = ['init']


def init_dir():
    paths = (
        Path().home().joinpath('spiritual'),
        Path().home().joinpath('spiritual', 'profiles'),
    )
    for path in paths:
        path.mkdir(exist_ok=True)


def init():
    init_dir()
