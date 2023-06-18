from .__init__ import *
from .init import init


def main():
    window = SpiritualWindow()
    window.run()


def test():
    from .profile import Profile
    from pathlib import Path
    from json import load as json_load
    with open(Path.home().joinpath('spiritual', 'profiles', 'e.json')) as file:
        data = json_load(file)
    print(data)
    print(Profile.is_valid(data))


if __name__ == '__main__':
    init()
    main()
    # test()
