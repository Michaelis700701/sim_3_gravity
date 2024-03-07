import pygame
from pygame import gfxdraw

WINDOW_WIDTH = (16 * 64) * 1.2
WINDOW_HEIGHT = (9 * 64) * 1.2

TILE_SIZE = 64

ACTIVE_STATE = {'active_state': 'sim'}

TEXT_FONT = 'assets/text/PoetsenOne-Regular.ttf'


MASS_AREA_RATIO = 2 * (10 ** 9)  # mass in kilograms to area in pixels
G = 6.67430 * (10 ** -11) # gravitational constant


masses = []

KEYS_PRESSED = {
    pygame.K_F3: False
}


# Colors

BACKGROUND_COLOR = (50, 50, 50)
LINE_COLOR = (0, 0, 0)

MASSES_COLOR = (
    (116, 122, 205),
    (117, 25, 34),
    (33, 61, 16),
    (122, 48, 29),
    (15, 51, 71)
)

# unused code for drawing an anti-analyzed circle
def draw_circle(surface: pygame.Surface, 
                color: pygame.Color,
                center: pygame.math.Vector2,
                radius: int
                ) -> None:
    
    gfxdraw.aacircle(surface, int(center.x), int(center.y), radius, color)
    gfxdraw.filled_circle(surface, int(center.x), int(center.y), radius, color)