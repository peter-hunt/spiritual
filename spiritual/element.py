from pygame.constants import (
    K_BACKSPACE, K_ESCAPE, K_RETURN, KEYDOWN,
    MOUSEBUTTONDOWN, MOUSEBUTTONUP,
)
from pygame.draw import rect as draw_rect
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.transform import scale as transform_scale

from .assets import FONTS, TITLE_FONTS

__all__ = ['Element', 'Title', 'TextPrompt', 'Button']


class Element:
    def update(self, window, dt):
        pass

    def draw(self, screen):
        pass

    def on_event(self, event, window):
        pass

    def on_resize(self, size, window):
        pass


class Title(Element):
    text: str
    x: int
    y: int
    width: int
    height: int
    font: Font
    font_size: int
    font_color: tuple[int, int, int]
    rect: Rect

    default_x: int
    default_y: int
    default_width: int
    default_height: int
    default_font_size: int

    def __init__(self, text, x, y, width, height,
                 font=None, font_size=24, font_color=(0, 0, 0)):
        self.default_x = x
        self.default_y = y
        self.default_width = width
        self.default_height = height
        self.default_font_size = font_size

        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = TITLE_FONTS if font is None else font
        self.font_size = font_size
        self.font_color = font_color
        self.rect = Rect(x, y, width, height)

    def draw(self, screen):
        text = self.font[self.font_size].render(
            self.text, True, self.font_color)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text, text_rect)

    def on_resize(self, size: tuple[int, int], window):
        self.x = self.default_x * size[0] / window.default_width
        self.y = self.default_y * size[1] / window.default_height
        self.width = self.default_width * size[0] / window.default_width
        self.height = self.default_height * size[1] / window.default_height
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.font_size = self.default_font_size * min(
            size[0] / window.default_width,
            size[1] / window.default_height)
        self.font_size = min(max(round(self.font_size), 8), 72)


class TextPrompt(Element):
    prompt: str
    x: int
    y: int
    width: int
    height: int
    font: Font
    font_size: int
    font_color: tuple[int, int, int]
    prompt_color: tuple[int, int, int]
    rect: Rect
    max_length: int

    default_x: int
    default_y: int
    default_width: int
    default_height: int
    default_font_size: int

    def __init__(self, prompt, x, y, width, height, max_length=32,
                 font=None, font_size=24,
                 font_color=(0, 0, 0), prompt_color=(192, 192, 192)):
        self.default_x = x
        self.default_y = y
        self.default_width = width
        self.default_height = height
        self.default_font_size = font_size

        self.prompt = prompt
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = FONTS if font is None else font
        self.font_size = font_size
        self.font_color = font_color
        self.prompt_color = prompt_color
        self.max_length = max_length
        self.rect = Rect(x, y, width, height)

        self.value = ''
        self.focus = False

    def draw(self, screen):
        color = tuple((c * 0.8 for c in self.prompt_color)
                      if self.focus else self.prompt_color)
        draw_rect(screen, color, self.rect)
        text = self.font[self.font_size].render(
            self.value or self.prompt, True, self.font_color)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text, text_rect)

    def on_resize(self, size: tuple[int, int], window):
        self.x = self.default_x * size[0] / window.default_width
        self.y = self.default_y * size[1] / window.default_height
        self.width = self.default_width * size[0] / window.default_width
        self.height = self.default_height * size[1] / window.default_height
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.font_size = self.default_font_size * min(
            size[0] / window.default_width,
            size[1] / window.default_height)
        self.font_size = min(max(round(self.font_size), 8), 72)

    def on_event(self, event, window):
        if event.type == MOUSEBUTTONDOWN:
            self.focus = self.rect.collidepoint(event.pos)
        elif event.type == KEYDOWN and self.focus:
            if event.key == K_BACKSPACE:
                self.value = self.value[:-1]
            elif event.key == K_RETURN:
                self.focus = False
            elif event.key == K_ESCAPE:
                self.focus = False
                self.value = ''
            elif len(self.value) < self.max_length:
                self.value += event.unicode


class Button(Element):
    text: str
    x: int
    y: int
    width: int
    height: int
    color: tuple[int, int, int]
    font: Font
    font_size: int
    font_color: tuple[int, int, int]
    action: callable
    rect: Rect
    pressed: bool

    default_x: int
    default_y: int
    default_width: int
    default_height: int
    default_font_size: int

    def __init__(self, text, x, y, width, height, color,
                 font=None, font_size=24, font_color=(0, 0, 0), action=None):
        self.default_x = x
        self.default_y = y
        self.default_width = width
        self.default_height = height
        self.default_font_size = font_size

        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.font = FONTS if font is None else font
        self.font_size = font_size
        self.font_color = font_color
        self.action = action if action is not None else lambda window: None
        self.rect = Rect(x, y, width, height)
        self.pressed = False

    def draw(self, screen):
        color = tuple((c * 0.8 for c in self.color)
                      if self.pressed else self.color)
        draw_rect(screen, color, self.rect)
        text = self.font[self.font_size].render(
            self.text, True, tuple((c * 0.8 for c in self.font_color)
                                   if self.pressed else self.font_color))
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text, text_rect)

    def on_resize(self, size: tuple[int, int], window):
        self.x = self.default_x * size[0] / window.default_width
        self.y = self.default_y * size[1] / window.default_height
        self.width = self.default_width * size[0] / window.default_width
        self.height = self.default_height * size[1] / window.default_height
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.font_size = self.default_font_size * min(
            size[0] / window.default_width,
            size[1] / window.default_height)
        self.font_size = min(max(round(self.font_size), 8), 72)

    def on_event(self, event, window):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        elif event.type == MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                if self.pressed:
                    self.action(window)
                    self.pressed = False
            else:
                self.pressed = False


class Sprite(Element):
    image: Surface
    x: int
    y: int
    width: int
    height: int
    scale: float
    use_center: bool

    default_x: int
    default_y: int
    default_width: int
    default_height: int

    def __init__(self, image, x, y, width, height, scale=1, use_center=False):
        self.default_x = x
        self.default_y = y
        self.default_width = width
        self.default_height = height
        self.scale = scale

        self.image = image
        self.x = x
        self.y = y
        self.width = width * scale
        self.height = height * scale
        self.use_center = use_center

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        wd_width, wd_height = screen.get_size()
        if self.x + self.width < 0 or self.x > wd_width:
            return
        if self.y + self.height < 0 or self.y > wd_height:
            return
        transformed = transform_scale(
            self.image, (self.width, self.height),
        )
        if self.use_center:
            screen.blit(transformed,
                        (self.x - self.width / 2, self.y - self.height / 2))
        else:
            screen.blit(transformed, (self.x, self.y))

    def on_resize(self, size: tuple[int, int], window):
        self.x = self.default_x * size[0] / window.default_width
        self.y = self.default_y * size[1] / window.default_height
        scale = self.scale * min(
            size[0] / window.default_width,
            size[1] / window.default_height)
        self.width = self.default_width * scale
        self.height = self.default_height * scale
