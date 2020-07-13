# pylint: disable=no-member
import pygame
import tcod as libtcodpy

pygame.init()

#Game defs
GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32

#MAP VARS
MAP_WIDTH = 20
MAP_HEIGHT = 20

#FPS LIMIT
GAME_FPS = 60

#Color Defs
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255,255,255)
COLOR_GREY = (100,100,100)
COLOR_RED = (255,0,0)

#Game Colors
BACKGROUND_COLOR = COLOR_GREY

#FOV SETTINGS
FOV_ALGO = libtcodpy.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10
MENU_FONT = pygame.font.Font("assets/joystix monospace.ttf", 16)
MESSAGE_FONT = pygame.font.Font("assets/joystix monospace.ttf", 12)
#MESSAGE DEFAULTS
NUM_MESSAGES = 4
