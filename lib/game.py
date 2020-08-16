from lib import draw, game, globalvars, maps, generator, constants, menu

import _pickle as pickle
import gzip
import pygame

class obj_Game:
    def __init__(self):
        self.current_objects = []
        self.message_history = []
        self.maps_prev = []
        self.maps_next = []
    def transition_next(self):
        global FOV_CALC

        globalvars.FOV_CALC = True
        self.maps_prev.append((globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects))
        for obj in self.current_objects:
            obj.animation_destroy()
        if len(self.maps_next) == 0:
            self.current_objects = [globalvars.PLAYER]
            globalvars.PLAYER.animation_init()
            self.current_map, self.current_rooms = maps.map_create()
            maps.map_place_objects(self.current_rooms)
        else:  
            (globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects) = self.maps_next[-1]
            
            for obj in self.current_objects:
                obj.animation_init()

            maps.map_make_fov(self.current_map)

            globalvars.FOV_CALC = True
            
            del self.maps_next[-1]
    
    def transition_prev(self):
        global FOV_CALC

        if len(self.maps_prev) != 0:
            for obj in self.current_objects:
                obj.animation_destroy()
            self.maps_next.append((globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects))

            (globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects) = self.maps_prev[-1]

            for obj in self.current_objects:
                obj.animation_init()

            maps.map_make_fov(self.current_map)

            globalvars.FOV_CALC = True
        
            del self.maps_prev[-1]

def game_main_loop():
    '''Function loops through game logic'''
    game_quit = False
    player_action = "no-action"

    while not game_quit:
        player_action = game.game_handle_keys()
        maps.map_calc_fov()
        if player_action == "QUIT":
            game.game_exit()
        for obj in globalvars.GAME.current_objects:
            if obj.ai:
                if player_action != "no-action":
                    obj.ai.take_turn()
            if obj.exitportal:
                obj.exitportal.update()
    
        if globalvars.PLAYER.state == "DEAD" or globalvars.PLAYER.state == "STATUS_WIN":
            game_quit = True
        draw.draw_game()
        pygame.display.flip()
        globalvars.CLOCK.tick(constants.GAME_FPS)

def game_handle_keys():
    global FOV_CALC
    keys_list = pygame.key.get_pressed()
    events_list = pygame.event.get()
    MOD_KEY = keys_list[pygame.K_RSHIFT] or keys_list[pygame.K_LSHIFT]
    for event in events_list:
        if event.type == pygame.QUIT:
            return "QUIT"
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                globalvars.PLAYER.creature.move(0,-1)
                globalvars.FOV_CALC = True
                return "player_moved"
            if event.key == pygame.K_DOWN:
                globalvars.PLAYER.creature.move(0,1)
                globalvars.FOV_CALC = True
                return "player_moved"
            if event.key == pygame.K_LEFT:
                globalvars.PLAYER.creature.move(-1,0)
                globalvars.FOV_CALC = True
                return "player_moved"
            if event.key == pygame.K_RIGHT:
                globalvars.PLAYER.creature.move(1,0)
                globalvars.FOV_CALC = True
                return "player_moved"
            if event.key == pygame.K_g:
                objects_at_player = maps.map_objects_at_coords(globalvars.PLAYER.x, globalvars.PLAYER.y)
                for obj in objects_at_player:
                    if obj.item:
                        obj.item.pick_up(globalvars.PLAYER)
                return "player_moved"
            if event.key == pygame.K_d:
                if len(globalvars.PLAYER.container.inventory) > 0:
                    globalvars.PLAYER.container.inventory[-1].item.drop(globalvars.PLAYER.x, globalvars.PLAYER.y)
            if event.key == pygame.K_ESCAPE:
                menu.menu_pause()
            if event.key == pygame.K_i:
                menu.menu_inventory()
            if MOD_KEY and event.key == pygame.K_PERIOD:
                list_of_objs = maps.map_objects_at_coords(globalvars.PLAYER.x, globalvars.PLAYER.y)
                for obj in list_of_objs:
                    if obj.stairs:
                        obj.stairs.use()
                    if obj.exitportal:
                        obj.exitportal.use()
    return "no-action"

def game_message(game_msg, msg_color):
    globalvars.GAME.message_history.append((game_msg, msg_color))

def game_new():
    global GAME

    globalvars.GAME = obj_Game()

    generator.gen_player((0,0))

    globalvars.GAME.current_map, globalvars.GAME.current_rooms = maps.map_create()

    maps.map_place_objects(globalvars.GAME.current_rooms)

def game_exit():
    game.game_save()
    pygame.quit()
    exit()

def game_save():
    for obj in globalvars.GAME.current_objects:
        obj.animation_destroy()

    with gzip.open('data\savedata\savegame', 'wb') as file:
        pickle.dump([globalvars.GAME, globalvars.PLAYER],file)

def game_load():

    global GAME, PLAYER
    with gzip.open('data\savedata\savegame', 'rb') as file:
        globalvars.GAME, globalvars.PLAYER = pickle.load(file)
    for obj in globalvars.GAME.current_objects:
        obj.animation_init()
    maps.map_make_fov(globalvars.GAME.current_map)

def prefs_save():
    with gzip.open('data\savedata\prefs', 'wb') as file:
        pickle.dump(globalvars.PREFS,file)

def prefs_load():
    global PREFS
    with gzip.open('data\savedata\prefs', 'rb') as file:
        globalvars.PREFS = pickle.load(file)
