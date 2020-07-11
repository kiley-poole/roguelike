import pygame
import tcod as libtcodpy

import constants

def draw_game():

    global SURFACE_MAIN

    #TODO clear the surface
    SURFACE_MAIN.fill(constants.BACKGROUND_COLOR)
    #TODO draw the map
    #TODO draw the character
    SURFACE_MAIN.blit(constants.S_PLAYER, (200,200))
    #TODO update the display
    pygame.display.flip()


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

    #init pygame
    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode( (constants.GAME_WIDTH, constants.GAME_HEIGHT) )

if __name__ == '__main__':
    game_init()
    game_main_loop()
