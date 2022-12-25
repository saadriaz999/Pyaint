import pygame
pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
MAROON = (255, 0, 0)
LIME = (0, 255, 0)
BLUE = (0, 0, 255)
NAVY = (0, 0, 128)
GRAY = (128, 128, 128)
SILVER = (192, 192, 192)
DARKGRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
AQUA = (0, 255, 255)
PURPLE = (128, 0, 128)
OLIVE = (128, 128, 0)
TEAL = (0, 128, 128)
GREEN = (0, 128, 0)
FUCHSIA = (255, 0, 255)
LIGHT_ORANGE = (255, 219, 176)

COLORS = [
    WHITE,
    BLACK,
    DARKGRAY,
    GRAY,
    SILVER,
    RED,
    MAROON,
    ORANGE,
    YELLOW,
    BLUE,
    NAVY,
    AQUA,
    OLIVE,
    TEAL,
    GREEN,
    LIME,
    FUCHSIA,
    PURPLE
]


def get_font(size):
    return pygame.font.SysFont("arial", size)


FPS = 240

WIDTH, HEIGHT = 600, 700

ROWS = COLS = 25   # increase to have smaller pixels

TOOLBAR_HEIGHT = HEIGHT - WIDTH

RIGHT_TOOLBAR_WIDTH = 100

PIXEL_SIZE = WIDTH // COLS

BG_COLOR = WHITE

DRAW_GRID_LINES = True

MOUSE_POSITION_TEXT_SIZE = 12

SMALL_BUTTON_HEIGHT = 14
SMALL_BUTTON_WIDTH = 14

MEDIUM_BUTTON_HEIGHT = 30
MEDIUM_BUTTON_WIDTH = 30
MEDIUM_BUTTON_SPACE = 32

BUTTON_Y_TOP_ROW = HEIGHT - TOOLBAR_HEIGHT / 2 - MEDIUM_BUTTON_HEIGHT - 1
BUTTON_Y_BOT_ROW = HEIGHT - TOOLBAR_HEIGHT / 2 + 1

LARGE_BUTTON_WIDTH = 40
LARGE_BUTTON_HEIGHT = 40
LARGE_BUTTON_SPACE = 42

SIZE_SMALL = 25
SIZE_MEDIUM = 35
SIZE_LARGE = 50

RIGHT_TOOLBAR_CENTER = WIDTH + RIGHT_TOOLBAR_WIDTH / 2

#TODO
# movev up and down button down clearing when pressing clear
# when deleting and merging, current layer frontend and backend not working
