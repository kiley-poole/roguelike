# pylint: disable=no-member
import pygame
import tcod as libtcodpy

pygame.init()

#Game defs
CAM_WIDTH = 600
CAM_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32

#MAP VARS
MAP_WIDTH = 100
MAP_HEIGHT = 100
MAP_MAX_NUM_ROOMS = 50

#ROOM VARS
ROOM_MAX_HEIGHT = 8
ROOM_MAX_WIDTH = 7
ROOM_MIN_HEIGHT = 3
ROOM_MIN_WIDTH = 3

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
CURSOR_TEXT = pygame.font.Font("assets/joystix monospace.ttf", CELL_HEIGHT)
#MESSAGE DEFAULTS
NUM_MESSAGES = 4

#DEPTH
DEPTH_PLAYER = -100
DEPTH_CREATURE = 1
DEPTH_ITEM = 2
DEPTH_CORPSE = 100