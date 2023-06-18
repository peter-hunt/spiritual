from pygame.constants import QUIT, RESIZABLE, SRCALPHA, VIDEORESIZE
from pygame.display import set_caption, set_mode, flip
from pygame.event import get as get_events
from pygame.surface import Surface
from pygame.time import Clock

from pathlib import Path

from .profile import Profile
from .state import STATES, State

__all__ = ['SpiritualWindow']


class SpiritualWindow:
    screen: Surface
    state: State
    state_name: str
    profile_path: Path | None = None
    profile: Profile | None = None

    default_width: int = 800
    default_height: int = 600

    def __init__(self, window_size=(800, 600)):
        self.screen = set_mode(window_size, RESIZABLE | SRCALPHA)
        set_caption('Spiritual')
        self.set_state('menu')

    def on_event(self, event):
        if event.type == QUIT:
            self.running = False
        elif event.type == VIDEORESIZE:
            self.state.on_resize(event.size, self)
        else:
            self.state.on_event(event, self)

    def draw(self):
        self.screen.fill((92, 92, 92, 255))
        prio_map = {}
        if len(self.state.elements) != len(self.state.priorities):
            # print('WARNING: Element count does not match priority count!')
            for element in self.state.elements:
                element.draw(self.screen)
        else:
            for element, prio in zip(self.state.elements, self.state.priorities):
                if prio not in prio_map:
                    prio_map[prio] = []
                prio_map[prio].append(element)
            for prio in sorted(prio_map):
                for element in prio_map[prio]:
                    element.draw(self.screen)
        flip()

    def set_state(self, state_name):
        self.state_name = state_name
        self.state = STATES[state_name]()
        self.state.on_resize(self.screen.get_size(), self)
        if state_name == 'game':
            self.state.profile = self.profile
        self.state.init(self)

    def update(self, dt):
        self.state.update(self, dt)

    def run(self):
        self.running = True
        clock = Clock()
        while self.running:
            for event in get_events():
                self.on_event(event)
            self.draw()
            dt = clock.tick(60) / 1000
            self.update(dt)
