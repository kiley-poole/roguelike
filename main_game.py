# pylint: disable=no-member
import pygame
import tcod as libtcodpy
import constants
import string

#STRUCTS
class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False

class struc_Assets:
    def __init__(self):
        #Objects
        self.misc_items = obj_Spritesheet("assets/dg_misc32.gif")
        self.dead_monster = self.misc_items.get_image('a', 7, 32, 32,constants.COLOR_WHITE)

        self.reptiles_spritesheet = obj_Spritesheet("assets/reptile_sheet.png")
        self.A_PLAYER = self.reptiles_spritesheet.get_animation('c', 1, 2, 16, 16, constants.COLOR_BLACK, (32,32))
        self.A_ENEMY = self.reptiles_spritesheet.get_animation('c', 3, 2, 16, 16, constants.COLOR_BLACK, (32,32))

        #Sprites
        self.terrain = obj_Spritesheet("assets/dg_extra132.gif")
        self.S_WALL = self.terrain.get_image('a', 11, 32, 32,constants.COLOR_WHITE)
        self.S_FLOOR = self.terrain.get_image('c', 12, 32, 32,constants.COLOR_WHITE)
        self.S_WALLEXPLORED = self.terrain.get_image('e', 11, 32, 32,constants.COLOR_WHITE)
        self.S_FLOOREXPLORED = self.terrain.get_image('e', 12, 32, 32,constants.COLOR_WHITE)
        

#OBJECTS
class obj_Actor:
    def __init__(self, x, y, name_object, animation, animation_speed = .5, creature = None, ai = None, container = None, item = None):
        self.x = x
        self.y = y
        self.animation = animation
        self.name_object = name_object
        self.animation_speed = animation_speed / 1.0
        self.flicker = self.animation_speed/len(self.animation) 
        self.flicker_timer = 0.0
        self.sprite_image = 0
        
        self.creature = creature
        if creature:
            self.creature.owner = self
        
        self.ai = ai
        if ai:
            self.ai.owner = self
        
        self.container = container
        if container:
            self.container.owner = self
    
        self.item = item
        if item:
            self.item.owner = self


    def draw(self):
        is_visible = libtcodpy.map_is_in_fov(FOV_MAP, self.x, self.y)
        if is_visible:
            if len(self.animation) == 1:
                SURFACE_MAIN.blit(self.animation[0], ( self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))
            else:
                if CLOCK.get_fps() > 0.0:
                    self.flicker_timer += 1/CLOCK.get_fps()
                if self.flicker_timer >= self.flicker:
                    self.flicker_timer = 0.0
                    if self.sprite_image >= len(self.animation) - 1:
                        self.sprite_image = 0
                    else:
                        self.sprite_image += 1
                SURFACE_MAIN.blit(self.animation[self.sprite_image], ( self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))

class obj_Game:
    def __init__(self):
        self.current_map = map_create()
        self.current_objects = []
        self.message_history = []
        
class obj_Spritesheet:
    '''
    Classs used to grab images from Spritesheet.
    '''

    def __init__(self, filename):
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.tiledict = {char:index for index, char in enumerate(string.ascii_lowercase, 1)}
    ################################

    def get_image(self, column, row, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT, color_key = constants.COLOR_BLACK, scale = None):
        image_list = []
        
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0,0), (self.tiledict[column]*width, row*height, width, height))
        image.set_colorkey(color_key)
        if scale:
            (new_w, new_h) = scale
            image = pygame.transform.scale(image, (new_w, new_h))
        image_list.append(image)
        return image_list
        
    def get_animation(self, column, row, num_sprites = 1, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT, color_key = constants.COLOR_BLACK, scale = None):
        image_list = []

        for i in range(num_sprites):
            image = pygame.Surface([width, height]).convert()
            image.blit(self.sprite_sheet, (0,0), (self.tiledict[column]*width+(width*i), row*height, width, height))
            image.set_colorkey(color_key)

            if scale:
                (new_w, new_h) = scale
                image = pygame.transform.scale(image, (new_w, new_h))
            image_list.append(image)

        return image_list

#COMPONENTS
class com_Creature:
    '''Creatures have health, can dmg other objects. Can die.'''

    def __init__(self, name_instance, hp = 10, death_function = None):
        self.name = name_instance
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function

    def move(self, dx, dy):

        tile_is_wall = (GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path == True)

        target = map_check_for_creatures(self.owner.x + dx, self.owner.y + dy, self.owner)
         
        if target:
            self.attack(target, 3)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target, damage):
        game_message((self.name + " attacks " + target.creature.name + " for " + str(damage) + " damage!"), constants.COLOR_WHITE)
        target.creature.take_damage(damage)

    def take_damage(self,damage):
        self.hp -= damage
        game_message(self.name + "'s health is " + str(self.hp) + "/" + str(self.maxhp), constants.COLOR_RED)

        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

class com_Container:
    def __init__(self, volume = 10.0, inventory = None):
        if inventory is None:
            self.inventory = []
        else:
            self.inventory = inventory
        self.max_volume = volume
    
    @property
    def volume(self):
        return 0.0
    
class com_Item:
    def __init__(self, weight = 0.0, volume = 0.0):
        self.weight = weight
        self.volume = volume
    
    def pick_up(self, actor):
        if actor.container:
            if actor.container.volume + self.volume > actor.container.max_volume:
               game_message("Not enough space in your inventory!", constants.COLOR_RED)
            else:
                game_message("Picked Up", constants.COLOR_WHITE)
                actor.container.inventory.append(self.owner)
                GAME.current_objects.remove(self.owner)
                self.container = actor.container
    
    def drop(self, pos_x, pos_y):
        GAME.current_objects.append(self.owner)
        self.container.inventory.remove(self.owner)
        self.owner.x = pos_x
        self.owner.y = pos_y
        game_message("Item Dropped!", constants.COLOR_WHITE)
#AI
class ai_Test:
    '''Once per turn execute'''
    def take_turn(self):
        self.owner.creature.move(libtcodpy.random_get_int(0, -1, 1), libtcodpy.random_get_int(0, -1, 1))

def death_monster(monster):
    '''On death, monster stops'''

    game_message((monster.creature.name + " is dead!"), constants.COLOR_GREY)


    monster.animation = ASSETS.dead_monster
    monster.creature = None
    monster.ai = None

#MAP FUNCTIONS
def map_create():
    new_map = [[ struc_Tile(False) for y in range(0,constants.MAP_WIDTH)] for x in range(0, constants.MAP_HEIGHT)]

    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    for x in range(constants.MAP_WIDTH):
        new_map[x][0].block_path = True
        new_map[x][constants.MAP_HEIGHT-1].block_path = True
    
    for y in range(constants.MAP_HEIGHT):
        new_map[0][y].block_path = True
        new_map[constants.MAP_WIDTH-1][y].block_path = True

    map_make_fov(new_map)

    return new_map

def map_check_for_creatures(x, y, exclude_object = None):
    target = None
    if exclude_object:
        #check object list for all creatures except excluded
        for object in GAME.current_objects: 
            if (object is not exclude_object and 
                object.x == x and 
                object.y == y and 
                object.creature):

                target = object
                
            if target:
                return target
    
    else:
        #check object list for any creature at location
        for object in GAME.current_objects: 
            if (object.x == x and 
                object.y == y and 
                object.creature):

                target = object
                
            if target:
                return target

def map_make_fov(incoming_map):
    global FOV_MAP

    FOV_MAP = libtcodpy.map.Map(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            libtcodpy.map_set_properties(FOV_MAP, x ,y,
                not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)

def map_calc_fov():
    global FOV_CALC

    if FOV_CALC:
        FOV_CALC = False
        libtcodpy.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS, constants.FOV_ALGO)

def map_objects_at_coords(pos_x, pos_y):
    objects_options = [obj for obj in GAME.current_objects if obj.x == pos_x and obj.y == pos_y]
    return objects_options
#DRAW FUNCTIONS
def draw_game():

    global SURFACE_MAIN

    SURFACE_MAIN.fill(constants.BACKGROUND_COLOR)
    draw_map(GAME.current_map)
    for obj in GAME.current_objects:
        obj.draw()

    draw_debug()
    draw_messages()
    pygame.display.flip()

def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0,constants.MAP_HEIGHT):

            is_visible = libtcodpy.map_is_in_fov(FOV_MAP, x ,y)

            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path == True:
                    SURFACE_MAIN.blit(ASSETS.S_WALL[0], (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))
                else:
                    SURFACE_MAIN.blit(ASSETS.S_FLOOR[0], (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))
        
            elif map_to_draw[x][y].explored:
                
                if map_to_draw[x][y].block_path == True:
                    SURFACE_MAIN.blit(ASSETS.S_WALLEXPLORED[0], (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))
                else:
                    SURFACE_MAIN.blit(ASSETS.S_FLOOREXPLORED[0], (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))

def draw_text(display_surface, text_to_display, T_coords, text_color, back_color = None):
    '''This function takes in text and displays it on the referenced surface'''

    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)

    text_rect.topleft = T_coords

    display_surface.blit(text_surf, text_rect)

def draw_debug():
    draw_text(SURFACE_MAIN, "fps: " + str(int(CLOCK.get_fps())), (0,0), constants.COLOR_RED)

def draw_messages():
    if len(GAME.message_history) <= constants.NUM_MESSAGES:
        to_draw = GAME.message_history
    else:
        to_draw = GAME.message_history[-constants.NUM_MESSAGES:]

    text_height = helper_text_size(constants.MESSAGE_FONT)
    start_y = (constants.MAP_HEIGHT*constants.CELL_HEIGHT - (constants.NUM_MESSAGES * text_height)) - 15

    i = 0
    for message, color in to_draw:
        draw_text(SURFACE_MAIN, message, (0, start_y + (i * text_height)), color, constants.COLOR_BLACK) 
        i += 1

#HELPER FUNCTIONS
def helper_text_objects(incoming_text, incoming_color, incoming_bg):
    if incoming_bg:
        text_surface = constants.MENU_FONT.render(incoming_text, False, incoming_color, incoming_bg)
    else:
        text_surface = constants.MENU_FONT.render(incoming_text, False, incoming_color)
    return text_surface, text_surface.get_rect()

def helper_text_size(font):
    '''Returns height of font passed in'''
    font_obj = font.render('a', False, (0,0,0))
    font_rect = font_obj.get_rect()
    return font_rect.height

#MENUS
def menu_pause():
    '''
    Pauses Game and displays menu
    '''
    menu_close = False

    window_width = constants.MAP_WIDTH * constants.CELL_WIDTH
    window_height = constants.MAP_HEIGHT * constants.CELL_HEIGHT
    menu_text = "PAUSED"
    menu_font = constants.MESSAGE_FONT
    text_height = helper_text_size(menu_font)
    text_width = len(menu_text) * helper_text_size(menu_font)

    while not menu_close:
        events_list = pygame.event.get()
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True
        draw_text(SURFACE_MAIN, menu_text, ((window_width/2) - (text_width/2), (window_height/2) - (text_height/2)), constants.COLOR_WHITE, constants.COLOR_BLACK)
        CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()

def menu_inventory():
    window_width = constants.MAP_WIDTH * constants.CELL_WIDTH
    window_height = constants.MAP_HEIGHT * constants.CELL_HEIGHT

    menu_close = False

    menu_height = 200
    menu_width = 200
    menu_x = int(window_width/2)-int(menu_width/2)
    menu_y = int(window_height/2)-int(menu_height/2)

    menu_text_font = constants.MESSAGE_FONT
    menu_text_height = helper_text_size(menu_text_font)

    local_inventory_surface = pygame.Surface((menu_width, menu_height))

    while not menu_close:
        local_inventory_surface.fill(constants.COLOR_BLACK)

        print_list = [obj.name_object for obj in PLAYER.container.inventory]

        events_list = pygame.event.get()
        mouse_x,mouse_y = pygame.mouse.get_pos()
        
        mouse_x_rel = mouse_x - menu_x
        mouse_y_rel = mouse_y - menu_x

        mouse_in_window = mouse_x_rel > 0 and mouse_y_rel > 0 and mouse_x_rel < menu_width and mouse_y_rel < menu_height
        mouse_line_selection = int(mouse_y_rel) / int(menu_text_height)

        if mouse_in_window:
            print(int(mouse_line_selection))
            print(len(print_list))

        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    menu_close = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (int(mouse_in_window) and int(mouse_line_selection) <= int(len(print_list)) -1):
                        PLAYER.container.inventory[int(mouse_line_selection)].item.drop(PLAYER.x, PLAYER.y)
            
        for line, (name) in enumerate(print_list):
            if line == int(mouse_line_selection) and mouse_in_window:
                draw_text(local_inventory_surface, name, (0, 0 + (line * menu_text_height)), constants.COLOR_WHITE, constants.COLOR_GREY)
            else:
                draw_text(local_inventory_surface, name, (0, 0 + (line * menu_text_height)), constants.COLOR_WHITE, constants.COLOR_BLACK)

    
        SURFACE_MAIN.blit(local_inventory_surface, (menu_x,menu_y))
        CLOCK.tick(constants.GAME_FPS)
        pygame.display.update()

#GAME FUNCTIONS
def game_main_loop():
    '''Function loops through game logic'''
    game_quit = False
    player_action = "no-action"

    while not game_quit:
        player_action = game_handle_keys()
        map_calc_fov()
        if player_action == "QUIT":
            game_quit = True
        elif player_action != "no-action":
            for obj in GAME.current_objects:
                if obj.ai:
                    obj.ai.take_turn()
        draw_game()
        CLOCK.tick(constants.GAME_FPS)
    pygame.quit()

def game_init():
    '''Function inits the game window and pygame'''

    global SURFACE_MAIN, GAME, FOV_CALC, CLOCK, PLAYER, ENEMY, ASSETS

    #init pygame
    pygame.init()
    pygame.key.set_repeat(200,70)

    SURFACE_MAIN = pygame.display.set_mode( (constants.MAP_WIDTH*constants.CELL_WIDTH, 
                                             constants.MAP_HEIGHT*constants.CELL_HEIGHT) )

    GAME = obj_Game()

    FOV_CALC = True

    ASSETS = struc_Assets()

    CLOCK = pygame.time.Clock()

    item_com1 = com_Item()
    container_com1 = com_Container()
    creature_com1 = com_Creature("Snake")
    PLAYER = obj_Actor(1, 1, "Python", ASSETS.A_PLAYER, creature=creature_com1, container=container_com1)

    creature_com2 = com_Creature("Crab",  death_function = death_monster)
    ai_com = ai_Test()
    ENEMY = obj_Actor(12, 12, "Crab", ASSETS.A_ENEMY, creature=creature_com2, ai = ai_com, item = item_com1)

    GAME.current_objects = [ENEMY, PLAYER]

def game_handle_keys():
    global FOV_CALC
    events_list = pygame.event.get()
    for event in events_list:
        if event.type == pygame.QUIT:
            return "QUIT"
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PLAYER.creature.move(0,-1)
                FOV_CALC = True
                return "player_moved"
            if event.key == pygame.K_DOWN:
                PLAYER.creature.move(0,1)
                FOV_CALC = True
                return "player_moved"
            if event.key == pygame.K_LEFT:
                PLAYER.creature.move(-1,0)
                FOV_CALC = True
                return "player_moved"
            if event.key == pygame.K_RIGHT:
                PLAYER.creature.move(1,0)
                FOV_CALC = True
                return "player_moved"
            if event.key == pygame.K_g:
                objects_at_player = map_objects_at_coords(PLAYER.x, PLAYER.y)
                for obj in objects_at_player:
                    if obj.item:
                        obj.item.pick_up(PLAYER)
                return "player_moved"
            if event.key == pygame.K_d:
                if len(PLAYER.container.inventory) > 0:
                    PLAYER.container.inventory[-1].item.drop(PLAYER.x, PLAYER.y)
            if event.key == pygame.K_ESCAPE:
                menu_pause()
            if event.key == pygame.K_i:
                menu_inventory()
    return "no-action"

def game_message(game_msg, msg_color):
    GAME.message_history.append((game_msg, msg_color))

if __name__ == '__main__':
    game_init()
    game_main_loop()
