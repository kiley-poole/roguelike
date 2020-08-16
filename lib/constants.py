# pylint: disable=no-member
import pygame
import tcod as libtcodpy

pygame.init()

#Game defs
CAM_WIDTH = 1000
CAM_HEIGHT = 1000
CELL_WIDTH = 32
CELL_HEIGHT = 32

#MAP VARS
MAP_WIDTH = 200
MAP_HEIGHT = 200
MAP_MAX_NUM_ROOMS = 30
MAP_LEVELS = 35

#RANDOM WALK VARS
MAX_NUM_STEPS = 600
MAX_RAND_MONSTERS = 10
MAX_RAND_ITEMS = 20
RAND_DIR_CHANGE = .25

#ROOM VARS
ROOM_MAX_HEIGHT = 9
ROOM_MAX_WIDTH = 12
ROOM_MIN_HEIGHT = 3
ROOM_MIN_WIDTH = 3

#FPS LIMIT
GAME_FPS = 60

#Color Defs
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255,255,255)
COLOR_GREY = (100,100,100)
COLOR_RED = (255,0,0)
COLOR_BLUE = (0,0,255)
COLOR_GREEN = (0,255,0)

#Game Colors
BACKGROUND_COLOR = COLOR_GREY

#FOV SETTINGS
FOV_ALGO = libtcodpy.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10
MAIN_MENU_FONT = pygame.font.Font("assets/joystix monospace.ttf", 40)
MENU_FONT = pygame.font.Font("assets/joystix monospace.ttf", 16)
MESSAGE_FONT = pygame.font.Font("assets/joystix monospace.ttf", 12)
CURSOR_TEXT = pygame.font.Font("assets/joystix monospace.ttf", CELL_HEIGHT)
OPTIONS_FONT = pygame.font.Font("assets/kenvector_future.ttf", 16)


#MESSAGE DEFAULTS
NUM_MESSAGES = 4

#DEPTH
DEPTH_PLAYER = -100
DEPTH_CREATURE = 1
DEPTH_ITEM = 2
DEPTH_CORPSE = 100