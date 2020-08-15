from lib import constants, draw, game, globalvars, text

import tcod as libtcodpy
import pygame

#DRAW FUNCTIONS
def draw_game():

    global SURFACE_MAIN

    globalvars.SURFACE_MAIN.fill(constants.BACKGROUND_COLOR)
    globalvars.SURFACE_MAP.fill(constants.COLOR_BLACK)
    globalvars.CAMERA.update()
    draw_map(globalvars.GAME.current_map)
    
    disp_rect = pygame.Rect((0,0), (constants.CAM_WIDTH, constants.CAM_HEIGHT))


    for obj in sorted(globalvars.GAME.current_objects, key = lambda obj: obj.depth, reverse = True ):
        obj.draw()
    globalvars.SURFACE_MAIN.blit(globalvars.SURFACE_MAP, (0, 0), globalvars.CAMERA.rect)
    draw_debug()
    draw_messages()

def draw_map(map_to_draw):

    cam_x, cam_y = globalvars.CAMERA.map_address
    display_map_w = constants.CAM_WIDTH // constants.CELL_WIDTH
    display_map_h = constants.CAM_HEIGHT // constants.CELL_HEIGHT

    render_w_min = cam_x - (display_map_w//2)
    render_h_min = cam_y - (display_map_h//2)
    
    render_w_max = cam_x + (display_map_w//2)
    render_h_max = cam_y + (display_map_h//2)

    if render_w_min < 0: render_w_min = 0
    if render_h_min < 0: render_h_min = 0

    if render_w_max > constants.MAP_WIDTH: render_w_max = constants.MAP_WIDTH
    if render_h_max > constants.MAP_HEIGHT: render_h_max = constants.MAP_HEIGHT

    for x in range(render_w_min, render_w_max):
        for y in range(render_h_min, render_h_max):

            tile_assignment = map_to_draw[x][y].assignment

            is_visible = libtcodpy.map_is_in_fov(globalvars.FOV_MAP, x ,y)

            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path == True:
                    globalvars.SURFACE_MAP.blit(globalvars.ASSETS.wall_dict[tile_assignment], (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))
                else:
                    globalvars.SURFACE_MAP.blit(globalvars.ASSETS.S_FLOOR[0], (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))
        
            elif map_to_draw[x][y].explored:
                
                if map_to_draw[x][y].block_path == True:
                    globalvars.SURFACE_MAP.blit(globalvars.ASSETS.wall_ex_dict[tile_assignment], (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))
                else:
                    globalvars.SURFACE_MAP.blit(globalvars.ASSETS.S_FLOOREXPLORED[0], (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))

def draw_text(display_surface, text_to_display, T_coords, text_color, font=constants.MENU_FONT, back_color = None, center = False):
    '''This function takes in text and displays it on the referenced surface'''

    text_surf, text_rect = text.helper_text_objects(text_to_display, font, text_color, back_color)

    if not center:
        text_rect.topleft = T_coords
    else:
        text_rect.center = T_coords

    display_surface.blit(text_surf, text_rect)

def draw_debug():
    draw.draw_text(globalvars.SURFACE_MAIN, "fps: " + str(int(globalvars.CLOCK.get_fps())), font=constants.MENU_FONT, T_coords = (0,0), text_color = constants.COLOR_RED)

def draw_messages():
    if len(globalvars.GAME.message_history) <= constants.NUM_MESSAGES:
        to_draw = globalvars.GAME.message_history
    else:
        to_draw = globalvars.GAME.message_history[-constants.NUM_MESSAGES:]

    text_height = text.helper_text_size(constants.MESSAGE_FONT)
    start_y = (constants.CAM_HEIGHT - (constants.NUM_MESSAGES * text_height)) - 15

    i = 0
    for message, color in to_draw:
        draw.draw_text(globalvars.SURFACE_MAIN, message, (0, start_y + (i * text_height)), color, constants.MESSAGE_FONT, constants.COLOR_BLACK) 
        i += 1

def draw_tile_rect(coords, tile_color = None, tile_alpha = None, mark = None):
    x, y = coords

    if tile_color: local_color = tile_color
    else: local_color = constants.COLOR_WHITE

    if tile_alpha: local_alpha = tile_alpha
    else: local_alpha = 200

    new_x = x * constants.CELL_WIDTH
    new_y = y * constants.CELL_HEIGHT
    new_surface = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))
    new_surface.fill(local_color)
    new_surface.set_alpha(local_alpha)

    if mark:
        draw.draw_text(new_surface, mark, T_coords= (constants.CELL_WIDTH/2, constants.CELL_HEIGHT/2), text_color=constants.COLOR_BLACK, font = constants.CURSOR_TEXT, center=True )
    globalvars.SURFACE_MAP.blit(new_surface, (new_x, new_y))
