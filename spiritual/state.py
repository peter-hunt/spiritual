from pygame.constants import (
    KEYDOWN, K_a, K_d, K_s, K_w,
    SRCALPHA,
)
from pygame.key import get_pressed
from pygame.surface import Surface

from json import JSONDecodeError, load as json_load
from math import ceil, floor
from pathlib import Path

from .assets import PLAYER_DIRECTIONS
from .constant import DEFAULT_VELOCITY, DEFAULT_ACCELERATION
from .element import Button, Sprite, TextPrompt, Title
from .profile import Profile
from .tilemap import TILEMAPS, TILES, COLLISSION_TILES
from .util import frange, pf_ceil, pf_floor

__all__ = [
    'State',
    'MenuState',
    'ProfilesState', 'NewProfileState',
    'SettingsState',
    'GameState',
    'STATES',
]


class State:
    def __init__(self):
        self.elements = []
        self.priorities = []

    def on_resize(self, size: tuple[int, int], window):
        for element in self.elements:
            element.on_resize(size, window)

    def on_event(self, event, window):
        for element in self.elements:
            element.on_event(event, window)

    def update(self, window, dt):
        for element in self.elements:
            element.update(window, dt)

    def init(self, window):
        pass


class MenuState(State):
    def __init__(self):
        self.elements = [
            Title('Spiritual', 200, 60, 400, 100, font_size=64),
            Button('Profiles', 200, 210, 400, 80, (255, 255, 255),
                   None, 32, (0, 0, 0), self.button_profiles),
            Button('Settings', 200, 310, 400, 80, (255, 255, 255),
                   None, 32, (0, 0, 0), self.button_settings),
            Button('Exit', 200, 410, 400, 80, (255, 255, 255),
                   None, 32, (0, 0, 0), self.button_exit),
        ]
        self.priorities = [0, 0, 0, 0]

    def button_profiles(self, window):
        window.set_state('profiles')

    def button_settings(self, window):
        window.set_state('settings')

    def button_exit(self, window):
        window.running = False


class ProfilesState(State):
    def __init__(self):
        self.profiles: list[Path] = []
        for path in Path.home().joinpath('spiritual', 'profiles').iterdir():
            if not path.is_file():
                continue
            try:
                with open(path) as file:
                    content = json_load(file)
            except JSONDecodeError:
                continue
            if Profile.is_valid(content):
                self.profiles.append(path)
        self.page = 0
        self.update_page()

    def button_new(self, window):
        window.set_state('new_profile')

    def button_back(self, window):
        window.set_state('menu')

    def button_up(self, window):
        if self.page > 0:
            self.page -= 1

    def button_down(self, window):
        if self.page < len(self.profiles) // 4:
            self.page += 1

    def update_page(self):
        self.elements = [
            Title('Profiles', 200, 60, 400, 100, font_size=64),
            Button('New', 20, 220, 160, 60, (255, 255, 255),
                   None, 32, (0, 0, 0), self.button_new),
            Button('Back', 20, 520, 160, 60, (255, 255, 255),
                   None, 32, (0, 0, 0), self.button_back),
            Button('Up', 620, 220, 160, 60, (255, 255, 255),
                   None, 32, (0, 0, 0), self.button_up),
            Button('Down', 620, 520, 160, 60, (255, 255, 255),
                   None, 32, (0, 0, 0), self.button_down),
        ]
        for i in range(4):
            if i + self.page * 4 >= len(self.profiles):
                break
            self.elements.append(
                Button(
                    self.profiles[i + self.page * 4].stem,
                    200, 220 + 100 * i, 400, 80, (192, 192, 192),
                    None, 32, (0, 0, 0), getattr(self, f'button_profile{i}')
                )
            )
        self.priorities = [0] * len(self.elements)

    def button_profile0(self, window):
        self.load_profile(self.profiles[self.page * 4], window)

    def button_profile1(self, window):
        self.load_profile(self.profiles[self.page * 4 + 1], window)

    def button_profile2(self, window):
        self.load_profile(self.profiles[self.page * 4 + 2], window)

    def button_profile3(self, window):
        self.load_profile(self.profiles[self.page * 4 + 3], window)

    def load_profile(self, path, window):
        with open(path) as file:
            data = json_load(file)
            if not Profile.is_valid(data):
                window.set_state('invalid_profile')
                return
            window.profile = Profile.loads(data)
            window.state.profile = window.profile
            window.set_state('game')


class NewProfileState(State):
    def __init__(self):
        self.elements = [
            Title('New Profile', 200, 60, 400, 100, font_size=64),
            TextPrompt('Player Name', 200, 220, 400, 80),
            Button('Cancel', 20, 520, 160, 60, (255, 255, 255),
                   None, 32, (0, 0, 0), self.button_cancel),
            Button('Confirm', 620, 520, 160, 60, (255, 255, 255),
                   None, 32, (0, 0, 0), self.button_confirm),
        ]
        self.priorities = [0, 0, 0, 0]

    def button_cancel(self, window):
        window.set_state('profiles')

    def button_confirm(self, window):
        if self.elements[1].value:
            profile = Profile.new(self.elements[1].value)
            profile.save()
            window.set_state('profiles')


class SettingsState(State):
    def __init__(self):
        self.elements = [
            Title('Settings', 200, 60, 400, 100, font_size=64),
            Button('Back', 200, 510, 400, 80, (255, 255, 255),
                   None, 32, (0, 0, 0), self.button_back),
        ]
        self.priorities = [0, 0]

    def button_back(self, window):
        window.set_state('menu')


class InvalidProfileState(State):
    def __init__(self):
        self.elements = [
            Title('Invalid Profile', 200, 60, 400, 100, font_size=64),
            Button('Back', 200, 510, 400, 80, (255, 255, 255),
                   None, 32, (0, 0, 0), self.button_back),
        ]
        self.priorities = [0, 0]

    def button_back(self, window):
        window.set_state('menu')


class GameState(State):
    def __init__(self):
        self.elements = [
            Title('Game', 200, 60, 400, 100, font_size=64),
            Button('Back', 200, 510, 400, 80, (255, 255, 255),
                   None, 32, (0, 0, 0), self.button_back),
            Sprite(PLAYER_DIRECTIONS[0], 400, 300, 16, 16, 8, True),
        ]
        self.priorities = [0, 0, 0]

        self.paused = False
        # self.position = [0, 0]
        self.position = [4, 3]
        self.velocity = [0, 0]
        self.profile = None
        self.chunksprites = {}

        self.direction = 0

    def init(self, window):
        self.set_location('spawn')
        self.update(window, 0)

    def button_back(self, window):
        window.set_state('menu')

    def on_event(self, event, window):
        for element in self.elements:
            element.on_event(event, window)

        if event.type == KEYDOWN:
            do_dir_check = True
            if event.key == K_w:
                direction_check = 0
            elif event.key == K_a:
                direction_check = 1
            elif event.key == K_s:
                direction_check = 2
            elif event.key == K_d:
                direction_check = 3
            else:
                do_dir_check = False
            if do_dir_check:
                self.direction = direction_check
                self.elements[2].image = PLAYER_DIRECTIONS[self.direction]

    def test_collision(self, dt):
        x_velocity, y_velocity = self.velocity
        original_x, original_y = self.position
        expected_x = original_x + x_velocity * dt
        expected_y = original_y + y_velocity * dt
        x_lower, x_upper = ((original_x, expected_x) if x_velocity > 0
                            else (expected_x, original_x))
        y_lower, y_upper = ((original_y, expected_y) if y_velocity > 0
                            else (expected_y, original_y))
        x_checkpoints = {*()}
        y_checkpoints = {*()}
        if x_velocity != 0:
            for x in frange(pf_ceil(x_lower), pf_floor(x_upper) + 1):
                x_checkpoints.add((x - original_x) / x_velocity)
        if y_velocity != 0:
            for y in frange(pf_ceil(y_lower), pf_floor(y_upper) + 1):
                y_checkpoints.add((y - original_y) / y_velocity)

        vx_pos = x_velocity > 0
        vy_pos = y_velocity > 0
        checkpoints = sorted({*x_checkpoints, *y_checkpoints})
        for elapsed in checkpoints:
            current_x = original_x + x_velocity * elapsed
            current_y = original_y + y_velocity * elapsed

            if x_velocity != 0 and elapsed in x_checkpoints:
                block_y = current_y - 0.5
                int_x = floor(current_x) + (1 if vx_pos else -1)
                for y in range(floor(block_y), ceil(block_y) + 1):
                    if self.tilemap[int_x, y] in COLLISSION_TILES:
                        x_velocity = 0
                        break
            if y_velocity != 0 and elapsed in y_checkpoints:
                block_x = current_x - 0.5
                int_y = floor(current_y) + (1 if vy_pos else -1)
                for x in range(floor(block_x), ceil(block_x) + 1):
                    if self.tilemap[x, int_y] in COLLISSION_TILES:
                        y_velocity = 0
                        break
            if x_velocity == 0 and y_velocity == 0:
                break
        else:
            elapsed = dt

        final_x = original_x + x_velocity * elapsed
        final_y = original_y + y_velocity * elapsed
        self.position = [final_x, final_y]

    def update(self, window, dt):
        wd_width, wd_height = window.screen.get_size()

        for element in self.elements:
            element.update(window, dt)

        pressed_keys = get_pressed()
        x_dir, y_dir = 0, 0
        if pressed_keys[K_a]:
            x_dir -= 1
        if pressed_keys[K_d]:
            x_dir += 1
        if pressed_keys[K_w]:
            y_dir -= 1
        if pressed_keys[K_s]:
            y_dir += 1

        max_velocity = DEFAULT_VELOCITY
        acceleration = DEFAULT_ACCELERATION
        vx, vy = self.velocity
        if x_dir == 0:
            if abs(vx) < acceleration * dt:
                vx = 0
            elif vx > 0:
                vx -= acceleration * dt
            else:
                vx += acceleration * dt
        else:
            vx += x_dir * acceleration * dt
            vx = min(max_velocity, max(-max_velocity, vx))
        if y_dir == 0:
            if abs(vy) < acceleration * dt:
                vy = 0
            elif vy > 0:
                vy -= acceleration * dt
            else:
                vy += acceleration * dt
        else:
            vy += y_dir * acceleration * dt
            vy = min(max_velocity, max(-max_velocity, vy))
        self.velocity = [vx, vy]
        if vx == 0 and vy == 0:
            return
        self.test_collision(dt)

        scale = min(wd_width / window.default_width,
                    wd_height / window.default_height)
        for pos, sprite in self.chunksprites.items():
            sprite.set_pos(
                wd_width * 0.5 + pos[0] * 1024 * scale - self.position[0] * 64 * scale,
                wd_height * 0.5 + pos[1] * 1024 * scale - self.position[1] * 64 * scale,
            )

    def set_location(self, location):
        if location not in TILEMAPS:
            raise ValueError(f'invalid location {location}')
        self.profile.location = location
        self.tilemap = TILEMAPS[location]
        width, height = self.tilemap.get_size()
        self.chunksprites = {}
        # render the chunks as sprites of 16x16 tiles with pygame surfaces
        for x in range(ceil(width / 16)):
            for y in range(ceil(height / 16)):
                chunk = Surface((256, 256), SRCALPHA).convert_alpha()
                chunk.fill((0, 0, 0, 0))
                for i in range(min(16, width - x * 16)):
                    for j in range(min(16, height - y * 16)):
                        chunk.blit(
                            TILES[self.tilemap[x * 16 + i, y * 16 + j]],
                            (i * 16, j * 16),
                        )
                self.chunksprites[x, y] = Sprite(
                    chunk, 400 + x * 1024, 300 + y * 1024,
                    256, 256, 4, False,
                )
        self.elements = self.elements[:3]
        for chunk_sprite in self.chunksprites.values():
            self.elements.append(chunk_sprite)
        self.priorities = [2, 2, 1] + [0] * (len(self.elements) - 3)


STATES = {
    'menu': MenuState,
    'profiles': ProfilesState,
    'new_profile': NewProfileState,
    'settings': SettingsState,
    'invalid_profile': InvalidProfileState,
    'game': GameState,
}
