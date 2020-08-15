import random
import string

import pygame
import tcod as libtcodpy

from lib import assets, camera, constants, data, globalvars


def game_init():
    '''Function inits the game window and pygame'''

    #init pygame
    pygame.init()
    pygame.key.set_repeat(200,70)
    libtcodpy.namegen_parse('assets\\namegen\\mingos_demon.cfg')
    try:
        game.prefs_load()
    except:
        globalvars.PREFS = data.struc_Prefs()

    globalvars.SURFACE_MAIN = pygame.display.set_mode((constants.CAM_WIDTH, constants.CAM_HEIGHT))
    globalvars.SURFACE_MAP = pygame.Surface((constants.MAP_WIDTH * constants.CELL_WIDTH, constants.MAP_HEIGHT * constants.CELL_HEIGHT))
    globalvars.CAMERA = camera.obj_Camera()
    globalvars.ASSETS = assets.obj_Assets()
    globalvars.RANDOM_ENGINE = random.SystemRandom()
    globalvars.FOV_CALC = True
    
    globalvars.CLOCK = pygame.time.Clock()
