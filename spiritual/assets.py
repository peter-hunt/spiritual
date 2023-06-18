from pygame.font import Font, init as init_font
from pygame.image import load as image_load

__all__ = [
    'FONT', 'FONTS', 'TITLE_FONT', 'TITLE_FONTS',
    'PLAYER_DIRECTIONS',
]

init_font()

FONT = Font('./assets/Bakemono-Stereo-Regular.ttf', 24)
FONTS = {}
for size in range(8, 73):
    FONTS[size] = Font('./assets/Bakemono-Stereo-Regular.ttf', size)
TITLE_FONT = Font('./assets/Bakemono-Stereo-Bold.ttf', 24)
TITLE_FONTS = {}
for size in range(8, 73):
    TITLE_FONTS[size] = Font('./assets/Bakemono-Stereo-Bold.ttf', size)

PLAYER_DIRECTIONS = [
    image_load('./assets/player_back.png'),
    image_load('./assets/player_left.png'),
    image_load('./assets/player_front.png'),
    image_load('./assets/player_right.png'),
]
