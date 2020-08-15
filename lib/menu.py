import pygame

from lib import constants, draw, globalvars, startup, game, menu, text, maps

class ui_Button:

    def __init__(self, surface, button_text, size, center_coords, 
                color_box_mouseover = constants.COLOR_GREY, 
                color_box_default = constants.COLOR_BLACK, 
                color_text_mouseover = constants.COLOR_WHITE, 
                color_text_default = constants.COLOR_WHITE):
        
        self.surface = surface
        self.text = button_text
        self.size = size
        self.center_coords = center_coords
        self.c_box_mo = color_box_mouseover
        self.c_box_def = color_box_default
        self.c_text_mo = color_text_mouseover
        self.c_text_def = color_text_default
        self.current_c_box = color_box_default
        self.current_c_text = color_text_default

        self.rect = pygame.Rect((0,0), size)
        self.rect.center = center_coords

    def update(self, player_input):
        local_events, local_mouse_pos = player_input
        mouse_x, mouse_y = local_mouse_pos
        mouse_clicked = False
        mouse_over = (mouse_x > self.rect.left 
                    and mouse_x <= self.rect.right
                    and mouse_y >= self.rect.top
                    and mouse_y <= self.rect.bottom)
        for event in local_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
        
        if mouse_over and mouse_clicked:
            return True
        
        if mouse_over:
            self.current_c_box = self.c_box_mo
            self.current_c_text = self.c_text_mo
        else:
            self.current_c_box = self.c_box_def
            self.current_c_text = self.c_text_def
        
    def draw(self):
        pygame.draw.rect(self.surface, self.current_c_box, self.rect)
        draw.draw_text(self.surface, self.text, self.center_coords, self.current_c_text, center=True)

class ui_Slider:

    def __init__(self, surface, size, center_coords, bg_color, fg_color, parameter_value):
        
        self.surface = surface
        self.size = size
        self.center_coords = center_coords
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.current_val = parameter_value

        self.bg_rect = pygame.Rect((0,0), size)
        self.bg_rect.center = center_coords
        self.fg_rect = pygame.Rect((0,0), (self.bg_rect.width * self.current_val, self.bg_rect.height))
        self.fg_rect.topleft = self.bg_rect.topleft 
        
        self.grip_tab = pygame.Rect((0,0), (20,self.bg_rect.height+4))
        self.grip_tab.center = (self.fg_rect.right, self.bg_rect.centery)

    def update(self, player_input):

        mouse_down = pygame.mouse.get_pressed()[0]

        local_events, local_mouse_pos = player_input
        mouse_x, mouse_y = local_mouse_pos

        mouse_over = (mouse_x > self.bg_rect.left 
                    and mouse_x <= self.bg_rect.right
                    and mouse_y >= self.bg_rect.top
                    and mouse_y <= self.bg_rect.bottom)
        
        if mouse_down and mouse_over:
            self.current_val = (mouse_x - self.bg_rect.left)/self.bg_rect.width 

            self.fg_rect.width = self.bg_rect.width * self.current_val
            self.grip_tab.center = (self.fg_rect.right, self.bg_rect.centery)

    def draw(self):
        #draw bg
        pygame.draw.rect(self.surface, self.bg_color, self.bg_rect)
        globalvars.SURFACE_MAIN.blit(globalvars.ASSETS.sfx_slider_bg, self.bg_rect.topleft)
        #draw fg
        pygame.draw.rect(self.surface, self.fg_color, self.fg_rect)
        #draw tab
        pygame.draw.rect(self.surface, constants.COLOR_GREY , self.grip_tab)
        globalvars.SURFACE_MAIN.blit(globalvars.ASSETS.sfx_slider_tab, self.grip_tab.topleft)
   
#MENUS
def menu_main():

    startup.game_init()

    menu_running = True

    title_y =  constants.CAM_HEIGHT//2 - 40
    title_x = constants.CAM_WIDTH//2
    title_text = "Mingo's House of Horrors" 

    #Button Loctaions
    continue_button_y = title_y + 40
    start_button_y = continue_button_y + 40
    options_button_y = start_button_y + 40
    quit_button_y = options_button_y + 40

    #Buttons 
    continue_button = ui_Button(globalvars.SURFACE_MAIN, "Continue", (150,35), (title_x,continue_button_y)) 
    start_button = ui_Button(globalvars.SURFACE_MAIN, "New Game", (150,35), (title_x,start_button_y)) 
    options_button = ui_Button(globalvars.SURFACE_MAIN, "Options", (150,35), (title_x,options_button_y)) 
    quit_button = ui_Button(globalvars.SURFACE_MAIN, "Quit", (100,35), (title_x,quit_button_y)) 


    #Main Menu Music
    pygame.mixer.music.load(globalvars.ASSETS.music_bg)
    pygame.mixer.music.play(-1)

    while menu_running:
        list_of_events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()

        game_input = (list_of_events, mouse_pos)

        for event in list_of_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if continue_button.update(game_input):
            pygame.mixer.music.stop()
            try:
                game.game_load()
            except:
                game.game_new()
            
            game.game_main_loop()

        if  start_button.update(game_input):
            pygame.mixer.music.stop()
            game.game_new()
            game.game_main_loop()
            startup.game_init()

        if  options_button.update(game_input):
            menu.menu_options()
            
        if  quit_button.update(game_input):
            pygame.mixer.music.stop()
            pygame.quit()
            exit()
        
        #Draw Menu
        globalvars.SURFACE_MAIN.blit(globalvars.ASSETS.MAIN_MENU_BG, (0,0))
        draw.draw_text(globalvars.SURFACE_MAIN, title_text, (title_x, title_y-200), constants.COLOR_WHITE, font=constants.MAIN_MENU_FONT, back_color=constants.COLOR_BLACK, center=True)
    
        start_button.draw()
        continue_button.draw()
        options_button.draw()
        quit_button.draw()

        pygame.display.update()

def menu_options():
    settings_menu_width = 200
    settings_menu_height = 200
    settings_menu_bgcolor = constants.COLOR_BLACK

    sfx_slider_x = constants.CAM_WIDTH//2
    sfx_slider_y = constants.CAM_HEIGHT//2 - 50
    sfx_volume = .5

    window_center = (constants.CAM_WIDTH//2 , constants.CAM_HEIGHT//2)

    settings_menu_surface = pygame.Surface((settings_menu_width, settings_menu_height))
    settings_menu_rect = pygame.Rect(0,0, settings_menu_width, settings_menu_height)
    settings_menu_rect.center = window_center

    menu_close = False
    
    sound_sfx_slider = ui_Slider(globalvars.SURFACE_MAIN, (125,15), (sfx_slider_x, sfx_slider_y), constants.COLOR_GREY, constants.COLOR_GREEN, globalvars.PREFS.vol_sound)

    music_sfx_slider = ui_Slider(globalvars.SURFACE_MAIN, (125,15), (sfx_slider_x, sfx_slider_y + 50), constants.COLOR_GREY, constants.COLOR_GREEN, globalvars.PREFS.vol_music)

    save_button = ui_Button(globalvars.SURFACE_MAIN, "SAVE", (100,50), (sfx_slider_x, sfx_slider_y +100),)

    while not menu_close:
        
        list_of_events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()

        game_input = (list_of_events, mouse_pos)

        for event in list_of_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True

        cur_sound_vol = globalvars.PREFS.vol_sound
        cur_music_vol = globalvars.PREFS.vol_music

        if cur_sound_vol is not sound_sfx_slider.current_val:
            globalvars.PREFS.vol_sound = sound_sfx_slider.current_val
            globalvars.ASSETS.adjust_sound()
        
        if cur_music_vol is not music_sfx_slider.current_val:
            globalvars.PREFS.vol_music = music_sfx_slider.current_val
            globalvars.ASSETS.adjust_sound()

        if save_button.update(game_input):
            game.prefs_save()
            menu_close = True

        sound_sfx_slider.update(game_input)
        music_sfx_slider.update(game_input)
        globalvars.SURFACE_MAIN.blit(globalvars.ASSETS.settings_menu_bg, settings_menu_rect.topleft)
        draw.draw_text(globalvars.SURFACE_MAIN, "SFX Volume", (sfx_slider_x, sfx_slider_y - 20), constants.COLOR_WHITE, font=constants.OPTIONS_FONT, center=True)
        draw.draw_text(globalvars.SURFACE_MAIN, "Music Volume", (sfx_slider_x, sfx_slider_y + 30), constants.COLOR_WHITE, font=constants.OPTIONS_FONT, center=True)

        sound_sfx_slider.draw() 
        music_sfx_slider.draw() 
        save_button.draw() 

        pygame.display.update()

def menu_pause():
    '''
    Pauses Game and displays menu
    '''
    menu_close = False

    window_width = constants.CAM_WIDTH
    window_height = constants.CAM_HEIGHT
    menu_text = "PAUSED"
    menu_font = constants.MESSAGE_FONT
    text_height = text.helper_text_size(menu_font)
    text_width = len(menu_text) * text.helper_text_size(menu_font)

    while not menu_close:
        events_list = pygame.event.get()
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True
        draw.draw_text(globalvars.SURFACE_MAIN, menu_text, ((window_width/2) - (text_width/2), (window_height/2) - (text_height/2)), constants.COLOR_WHITE, constants.MENU_FONT, constants.COLOR_BLACK)
        globalvars.CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()

def menu_inventory():
    
    window_width = constants.CAM_WIDTH
    window_height = constants.CAM_HEIGHT
    
    menu_close = False

    menu_height = 200
    menu_width = 200
    menu_x = (window_width//2)-(menu_width//2)
    menu_y = (window_height//2)-(menu_height//2)

    menu_text_font = constants.MESSAGE_FONT
    menu_text_height = text.helper_text_size(menu_text_font)

    local_inventory_surface = pygame.Surface((menu_width, menu_height))

    while not menu_close:
        local_inventory_surface.fill(constants.COLOR_BLACK)

        print_list = [obj.display_name for obj in globalvars.PLAYER.container.inventory]

        events_list = pygame.event.get()
        mouse_x,mouse_y = pygame.mouse.get_pos()
        
        mouse_x_rel = mouse_x - menu_x
        mouse_y_rel = mouse_y - menu_x

        mouse_in_window = mouse_x_rel > 0 and mouse_y_rel > 0 and mouse_x_rel < menu_width and mouse_y_rel < menu_height
        mouse_line_selection = mouse_y_rel//menu_text_height

        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    menu_close = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (int(mouse_in_window) and int(mouse_line_selection) <= int(len(print_list)) -1):
                        globalvars.PLAYER.container.inventory[int(mouse_line_selection)].item.use()
                        menu_close = True
                if event.button == 3:
                    if (int(mouse_in_window) and int(mouse_line_selection) <= int(len(print_list)) -1):
                        globalvars.PLAYER.container.inventory[int(mouse_line_selection)].item.drop(globalvars.PLAYER.x, globalvars.PLAYER.y)
                        menu_close = True
        for line, (name) in enumerate(print_list):
            if line == mouse_line_selection and mouse_in_window:
                draw.draw_text(local_inventory_surface, name, (0, 0 + (line * menu_text_height)), constants.COLOR_WHITE, constants.MENU_FONT, constants.COLOR_GREY)
            else:
                draw.draw_text(local_inventory_surface, name, (0, 0 + (line * menu_text_height)), constants.COLOR_WHITE, constants.MENU_FONT, constants.COLOR_BLACK)

        draw.draw_game()
        globalvars.SURFACE_MAIN.blit(local_inventory_surface, (menu_x,menu_y))
        globalvars.CLOCK.tick(constants.GAME_FPS)
        pygame.display.update()

def menu_target_select(coords_origin = None, range = None, pen_walls = True, pen_creature = True, radius = None):
    '''This menu lets the player select a tile.

    This function pauses, the game, produces an on screen square and when the player presses the left MB, will return map address.
    '''
    menu_close = False
    while not menu_close:

        mouse_x,mouse_y = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        mapx_pixel, mapy_pixel = globalvars.CAMERA.win_to_map((mouse_x, mouse_y))
        mouse_x_rel = mapx_pixel//constants.CELL_WIDTH
        mouse_y_rel = mapy_pixel//constants.CELL_HEIGHT

        valid_tiles=[]
        if coords_origin:
            list_of_tiles = maps.map_find_line(coords_origin, (mouse_x_rel,mouse_y_rel))
            for i, (x, y) in enumerate(list_of_tiles):
                valid_tiles.append((x,y))
                if range and i == range-1:
                    break
                if pen_walls == False:
                     if globalvars.GAME.current_map[x][y].block_path: break
                if pen_creature == False and maps.map_check_for_creatures(x,y):
                    break
        else:
            valid_tiles = [(mouse_x_rel, mouse_y_rel)]
            
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    menu_close = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return(valid_tiles[-1])

        globalvars.SURFACE_MAIN.fill(constants.BACKGROUND_COLOR)
        globalvars.SURFACE_MAP.fill(constants.COLOR_BLACK)
        globalvars.CAMERA.update()
        draw.draw_map(globalvars.GAME.current_map)

        for obj in sorted(globalvars.GAME.current_objects, key = lambda obj: obj.depth, reverse = True ):
            obj.draw()

        for (tile_x, tile_y) in valid_tiles:
            if (tile_x, tile_y) == valid_tiles[-1]:
                draw.draw_tile_rect((tile_x, tile_y), mark='X')
            draw.draw_tile_rect((tile_x, tile_y))
        if radius:
            area_effect = maps.map_find_radius(valid_tiles[-1], radius)
            for (rad_x, rad_y) in area_effect:
                    draw.draw_tile_rect((rad_x, rad_y))

        globalvars.SURFACE_MAIN.blit(globalvars.SURFACE_MAP, (0, 0), globalvars.CAMERA.rect)
        draw.draw_debug()
        draw.draw_messages()
        pygame.display.flip()
        globalvars.CLOCK.tick(constants.GAME_FPS)
