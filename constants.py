import pygame

pygame.init()

#Game defs
GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32

#MAP VARS
MAP_WIDTH = 30
MAP_HEIGHT = 30

#Color Defs
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255,255,255)
COLOR_GREY = (100,100,100)

#Game Colors
BACKGROUND_COLOR = COLOR_GREY

#SPRITES
S_PLAYER = pygame.image.load("assets/snake.png")
S_WALL = pygame.image.load("assets/wall.png")
S_FLOOR = pygame.image.load("assets/floor.jpg")