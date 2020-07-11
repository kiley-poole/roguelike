import pygame
import tcod as libtcodpy
import constants

#STRUCTS
class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path

#MAP FUNCTIONS
def map_create():
    new_map = [[ struc_Tile(False) for y in range(0,constants.MAP_WIDTH)] for x in range(0, constants.MAP_HEIGHT) ]

    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    return new_map

#DRAW FUNCTIONS
def draw_game():

    global SURFACE_MAIN

    #TODO clear the surface
    SURFACE_MAIN.fill(constants.BACKGROUND_COLOR)
    #TODO draw the map
    draw_map(GAME_MAP)
    #TODO draw the character
    SURFACE_MAIN.blit(constants.S_PLAYER, (200,200))
    #TODO update the display
    pygame.display.flip()

def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0,constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path == True:
               SURFACE_MAIN.blit(constants.S_WALL, (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))
            else:
               SURFACE_MAIN.blit(constants.S_FLOOR, (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))


#GAME FUNCTIONS
def game_main_loop():
    '''Function loops through game logic'''
    game_quit = False

    while not game_quit:
        #TODO get player input
        events_list = pygame.event.get()
        #TODO process input
        for event in events_list:
            if event.type == pygame.QUIT:
                game_quit = True
        #TODO draw the game
        draw_game()
    #TODO quit the game
    pygame.quit()

def game_init():
    '''Function inits the game window and pygame'''

    global SURFACE_MAIN
    global GAME_MAP

    #init pygame
    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode( (constants.GAME_WIDTH, constants.GAME_HEIGHT) )

    GAME_MAP = map_create()

if __name__ == '__main__':
    game_init()
    game_main_loop()
