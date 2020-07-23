import pygame
import tcod as libtcodpy
import constants
import string
import math

#STRUCTS
class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False

class struc_Assets:
    def __init__(self):
        #Sheets
        ##Character Sheets
        self.reptiles_spritesheet = obj_Spritesheet("assets/Characters/Reptile0.png", "assets/Characters/Reptile1.png")
        self.humanoids_spritesheet = obj_Spritesheet("assets/Characters/Humanoid0.png","assets/Characters/Humanoid1.png")
        self.player_spritesheet = obj_Spritesheet("assets/Characters/Player0.png","assets/Characters/Player1.png")
        self.demon_spritesheet = obj_Spritesheet("assets/Characters/Demon0.png","assets/Characters/Demon1.png")
        self.undead_spritesheet = obj_Spritesheet("assets/Characters/Undead0.png","assets/Characters/Undead1.png")
        #Object Sheets
        self.walls_spritesheet = obj_Spritesheet("assets/Objects/Wall.png")
        self.floors_spritesheet = obj_Spritesheet("assets/Objects/Floor.png")
        self.misc_items = obj_Spritesheet("assets/Objects/Decor0.png", "assets/Objects/Decor1.png")
        #Item Sheets
        self.longWep_spritesheet = obj_Spritesheet("assets/Items/LongWep.png")
        self.shield_spritesheet = obj_Spritesheet("assets/Items/Shield.png")
        self.scrolls_spritesheet = obj_Spritesheet("assets/Items/Scroll.png")

        #PC/NPCs
        self.dead_monster = self.misc_items.get_animation('a', 12, 2, 16, 16, constants.COLOR_BLACK, (32,32))
        self.A_PLAYER = self.player_spritesheet.get_animation('c', 8, 2, 16, 16, constants.COLOR_BLACK, (32,32))
        self.A_ENEMY = self.humanoids_spritesheet.get_animation('a', 0, 2, 16, 16, constants.COLOR_BLACK, (32,32))
        self.fire_elemental = self.demon_spritesheet.get_animation('a', 1, 2, 16, 16, constants.COLOR_BLACK, (32,32))
        self.skeleton = self.undead_spritesheet.get_animation('a', 2, 2, 16, 16, constants.COLOR_BLACK, (32,32))
        self.skeleton_mage = self.undead_spritesheet.get_animation('h', 2, 2, 16, 16, constants.COLOR_BLACK, (32,32))

        #Terrain
        self.S_WALL = self.walls_spritesheet.get_animation('d', 9, 1, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_FLOOR = self.floors_spritesheet.get_animation('i', 16, 1, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALLEXPLORED = self.walls_spritesheet.get_animation('d', 12, 1, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_FLOOREXPLORED = self.floors_spritesheet.get_animation('i', 22, 1, 16, 16,constants.COLOR_WHITE, (32,32))
        
        #Items
        self.sword = self.longWep_spritesheet.get_animation('a', 1, 1, 16, 16,constants.COLOR_BLACK, (32,32))
        self.shield = self.shield_spritesheet.get_animation('c', 0, 1, 16, 16,constants.COLOR_BLACK, (32,32))
        self.lightning_scroll = self.scrolls_spritesheet.get_animation('a', 0, 1, 16, 16,constants.COLOR_BLACK, (32,32))
        self.fireball_scroll = self.scrolls_spritesheet.get_animation('c', 2, 1, 16, 16,constants.COLOR_BLACK, (32,32))
        self.confusion_scroll = self.scrolls_spritesheet.get_animation('d', 5, 1, 16, 16,constants.COLOR_BLACK, (32,32))

#OBJECTS
class obj_Actor:
    def __init__(self, x, y, name_object, animation, animation_speed = .5, creature = None, ai = None, container = None, item = None, equipment = None):
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

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self
            self.item = com_Item()
            self.item.owner = self
    
    @property
    def display_name(self):
        if self.creature:
            return (self.creature.name + " the " + self.name_object)
        
        elif self.item:
            if self.equipment and self.equipment.equipped:
                return (self.name_object + " (E)")
            else:
                return self.name_object
    
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

    def distance_to(self, other):

        dx = other.x - self.x
        dy = other.y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    def move_towards(self,other):

        dx = other.x - self.x
        dy = other.y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx/distance))
        dy = int(round(dy/distance))

        self.creature.move(dx,dy)
        
class obj_Game:
    def __init__(self):
        self.current_map = map_create()
        self.current_objects = []
        self.message_history = []
        
class obj_Spritesheet:
    '''
    Classs used to grab images from Spritesheet.
    '''

    def __init__(self, filename1, filename2=None):
        self.sprite_sheet1 = pygame.image.load(filename1).convert()
        if filename2:
            self.sprite_sheet2 = pygame.image.load(filename2).convert()

        self.tiledict = {char:index for index, char in enumerate(string.ascii_lowercase, 0)}
    

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
            if num_sprites > 1:
                if i % 2 == 0:
                    image.blit(self.sprite_sheet1, (0,0), (self.tiledict[column]*width, row*height, width, height))
                else:
                    image.blit(self.sprite_sheet2, (0,0), (self.tiledict[column]*width, row*height, width, height))
            else:
                image.blit(self.sprite_sheet1, (0,0), (self.tiledict[column]*width, row*height, width, height))

            image.set_colorkey(color_key)

            if scale:
                (new_w, new_h) = scale
                image = pygame.transform.scale(image, (new_w, new_h))
            image_list.append(image)

        return image_list

#COMPONENTS
class com_Creature:
    '''Creatures have health, can dmg other objects. Can die.'''

    def __init__(self, name_instance, base_atk = 1, base_def = 0, hp = 10, death_function = None):
        self.name = name_instance
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function
        self.base_atk = base_atk
        self.base_def = base_def

    def move(self, dx, dy):

        tile_is_wall = (GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path == True)

        target = map_check_for_creatures(self.owner.x + dx, self.owner.y + dy, self.owner)
         
        if target:
            self.attack(target)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target):
        damage_dealt = self.power - target.creature.defense
        if damage_dealt < 0: damage_dealt = 0
        game_message((self.name + " attacks " + target.creature.name + " for " + str(damage_dealt) + " damage!"), constants.COLOR_WHITE)
        target.creature.take_damage(damage_dealt)

    def take_damage(self,damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
        game_message(self.owner.display_name + "'s health is " + str(self.hp) + "/" + str(self.maxhp), constants.COLOR_RED)

        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

    def heal(self, value):
        self.hp += value
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    @property
    def power(self):
        total_power = self.base_atk

        if self.owner.container:
            object_bonuses = [obj.equipment.attack_bonus for obj in self.owner.container.equipped]

            for bonus in object_bonuses:
                if bonus:
                    total_power += bonus

        return total_power
    
    @property
    def defense(self):
        total_defense = self.base_def

        if self.owner.container:
            object_bonuses = [obj.equipment.defense_bonus for obj in self.owner.container.equipped]
            for bonus in object_bonuses:
                if bonus:
                    total_defense += bonus

        return total_defense

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
    
    @property
    def equipped(self):
        return [obj for obj in self.inventory if obj.equipment and obj.equipment.equipped]   

class com_Equipment:

    def __init__(self, attack_bonus = None, defense_bonus = None, slot = None):
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.slot = slot
        self.equipped = False

    def toggle_equip(self):
        if self.equipped:
            self.unequip()
        else:
            self.equip()
    
    def equip(self):
        all_equiped_items = self.owner.item.container.equipped
        for item in all_equiped_items:
            if item.equipment.slot and (item.equipment.slot == self.slot):
                game_message("equipment slot is occupied", constants.COLOR_RED)
                return 
        self.equipped = True
        game_message("equipped", constants.COLOR_WHITE)
    def unequip(self):
        self.equipped = False
        game_message("unequipped", constants.COLOR_WHITE)

class com_Item:
    def __init__(self, weight = 0.0, volume = 0.0, use_function = None, value = None):
        self.weight = weight
        self.volume = volume
        self.value = value
        self.use_function = use_function
    
    def pick_up(self, actor):
        if actor.container:
            if actor.container.volume + self.volume > actor.container.max_volume:
               game_message("Not enough space in your inventory!", constants.COLOR_RED)
            else:
                game_message(self.owner.display_name + " Picked Up", constants.COLOR_WHITE)
                actor.container.inventory.append(self.owner)
                GAME.current_objects.remove(self.owner)
                self.container = actor.container
    
    def drop(self, pos_x, pos_y):
        GAME.current_objects.append(self.owner)
        self.container.inventory.remove(self.owner)
        self.owner.x = pos_x
        self.owner.y = pos_y
        game_message("Item Dropped!", constants.COLOR_WHITE)

    def use(self):
        '''Uses item 
            Currently only consumables        
        '''
        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return

        if self.use_function:
            result = self.use_function(self.container.owner, self.value)

            if result is not None:
                game_message("You're at full health. Healing would be pointless.", constants.COLOR_RED)
            else:
                self.container.inventory.remove(self.owner)
#AI
class ai_Confuse:
    '''Once per turn execute'''
    def __init__(self, old_ai, num_turns):
        self.old_ai = old_ai
        self.num_turns = num_turns
    def take_turn(self):
        if self.num_turns > 0:
            self.owner.creature.move(libtcodpy.random_get_int(0, -1, 1), libtcodpy.random_get_int(0, -1, 1))
            self.num_turns -= 1
        else:
            self.owner.ai = self.old_ai
            game_message(self.owner.display_name + " is no longer confused", constants.COLOR_WHITE)

class ai_Chase:
    '''
    A basic monster ai which chases and harms player
    '''

    def take_turn(self):
        monster = self.owner
        if libtcodpy.map_is_in_fov(FOV_MAP, monster.x, monster.y):
            if monster.distance_to(PLAYER) >= 2:
                self.owner.move_towards(PLAYER)
            elif PLAYER.creature.hp > 0:
                monster.creature.attack(PLAYER)

#DEATH
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

def map_find_line(coords1, coords2):
    '''Converts two x,y coords into list of tiles'''

    x1, y1 = coords1
    x2, y2 = coords2

    libtcodpy.line_init(x1,y1,x2,y2)

    cur_x, cur_y = libtcodpy.line_step()

    coord_list = []

    if x1 == x2 and y1 == y2:
        return [coords1]
    
    while(not cur_x is None):
        coord_list.append((cur_x, cur_y))
        
        cur_x, cur_y = libtcodpy.line_step()

    return coord_list

def map_find_radius(coords, radius):
    tile_x, tile_y = coords
    tile_list = []
    start_y = tile_y - radius
    start_x = tile_x - radius

    for x in range(radius*2+1):
        for y in range(radius*2+1):
            tile_list.append((start_x+y, start_y+x))

    return tile_list
#DRAW FUNCTIONS
def draw_game():

    global SURFACE_MAIN

    SURFACE_MAIN.fill(constants.BACKGROUND_COLOR)
    draw_map(GAME.current_map)
    for obj in GAME.current_objects:
        obj.draw()

    draw_debug()
    draw_messages()

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

def draw_text(display_surface, text_to_display, T_coords, text_color, font=constants.MENU_FONT, back_color = None, center = False):
    '''This function takes in text and displays it on the referenced surface'''

    text_surf, text_rect = helper_text_objects(text_to_display, font, text_color, back_color)

    if not center:
        text_rect.topleft = T_coords
    else:
        text_rect.center = T_coords

    display_surface.blit(text_surf, text_rect)

def draw_debug():
    draw_text(SURFACE_MAIN, "fps: " + str(int(CLOCK.get_fps())), font=constants.MENU_FONT, T_coords = (0,0), text_color = constants.COLOR_RED)

def draw_messages():
    if len(GAME.message_history) <= constants.NUM_MESSAGES:
        to_draw = GAME.message_history
    else:
        to_draw = GAME.message_history[-constants.NUM_MESSAGES:]

    text_height = helper_text_size(constants.MESSAGE_FONT)
    start_y = (constants.MAP_HEIGHT*constants.CELL_HEIGHT - (constants.NUM_MESSAGES * text_height)) - 15

    i = 0
    for message, color in to_draw:
        draw_text(SURFACE_MAIN, message, (0, start_y + (i * text_height)), color, constants.MESSAGE_FONT, constants.COLOR_BLACK) 
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
        draw_text(new_surface, mark, T_coords= (constants.CELL_WIDTH/2, constants.CELL_HEIGHT/2), text_color=constants.COLOR_BLACK, font = constants.CURSOR_TEXT, center=True )
    SURFACE_MAIN.blit(new_surface, (new_x, new_y))
    
#HELPER FUNCTIONS
def helper_text_objects(incoming_text, font, incoming_color, incoming_bg):
    if incoming_bg:
        text_surface = font.render(incoming_text, False, incoming_color, incoming_bg)
    else:
        text_surface = font.render(incoming_text, False, incoming_color)
    return text_surface, text_surface.get_rect()

def helper_text_size(font):
    '''Returns height of font passed in'''
    font_obj = font.render('a', False, (0,0,0))
    font_rect = font_obj.get_rect()
    return font_rect.height

def helper_random_coords():
    ran_x = libtcodpy.random_get_int(0,1,constants.MAP_WIDTH-1)
    ran_y = libtcodpy.random_get_int(0,1,constants.MAP_HEIGHT-1)
    return (ran_x, ran_y)
#MAGIC
def cast_heal(target, value):
    if target.creature.hp == target.creature.maxhp:
       game_message(target.creature.name + " the " + target.name_object + " is at full HP!", constants.COLOR_WHITE) 
       return "cancelled"
    else:    
       game_message(target.creature.name + " the " + target.name_object + " healed for " + str(value) + " HP!", constants.COLOR_WHITE)
       target.creature.heal(value)
       game_message("Current HP is " + str(target.creature.hp) + '/' + str(target.creature.maxhp), constants.COLOR_WHITE)
    return None

def cast_lightning(caster, T_damage_range):

    player_locat = (caster.x, caster.y)

    damage, m_range = T_damage_range

    tile_selected = menu_target_select(coords_origin = player_locat, range = m_range, pen_walls=False)
    if tile_selected:
        list_of_tiles = map_find_line(player_locat, tile_selected)

        for i, (x,y) in enumerate(list_of_tiles):
            target = map_check_for_creatures(x,y)
            if target:
                target.creature.take_damage(damage)

def cast_fireball(caster,T_damage_radius_range):

    damage, internal_radius , max_range = T_damage_radius_range
    player_locat = (caster.x, caster.y)

    tile_selected = menu_target_select(coords_origin = player_locat, range = max_range, pen_walls=False, pen_creature=False, radius=internal_radius)
    
    tiles_to_damage = map_find_radius(tile_selected, internal_radius)

    creature_hit = False

    for (x,y) in tiles_to_damage:
        creature_to_dmg = map_check_for_creatures(x,y)
        if creature_to_dmg:
            creature_to_dmg.creature.take_damage(damage)
            if creature_to_dmg is not PLAYER:
                creature_hit = True
    
    if creature_hit:
        game_message("The fireball fucks shit up hardcore!", constants.COLOR_RED)

def cast_confusion(caster, effect_length):
    tile_selected = menu_target_select()
    if tile_selected:
        x,y = tile_selected
        target=  map_check_for_creatures(x,y)
        if target:
            oldai = target.ai
            target.ai = ai_Confuse(old_ai = oldai, num_turns = effect_length)
            target.ai.owner = target
            game_message(target.display_name + " is confused", constants.COLOR_RED)

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
        draw_text(SURFACE_MAIN, menu_text, ((window_width/2) - (text_width/2), (window_height/2) - (text_height/2)), constants.COLOR_WHITE, constants.MENU_FONT, constants.COLOR_BLACK)
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

        print_list = [obj.display_name for obj in PLAYER.container.inventory]

        events_list = pygame.event.get()
        mouse_x,mouse_y = pygame.mouse.get_pos()
        
        mouse_x_rel = mouse_x - menu_x
        mouse_y_rel = mouse_y - menu_x

        mouse_in_window = mouse_x_rel > 0 and mouse_y_rel > 0 and mouse_x_rel < menu_width and mouse_y_rel < menu_height
        mouse_line_selection = int(mouse_y_rel) / int(menu_text_height)

        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    menu_close = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (int(mouse_in_window) and int(mouse_line_selection) <= int(len(print_list)) -1):
                        PLAYER.container.inventory[int(mouse_line_selection)].item.use()
                        menu_close = True
            
        for line, (name) in enumerate(print_list):
            if line == int(mouse_line_selection) and mouse_in_window:
                draw_text(local_inventory_surface, name, (0, 0 + (line * menu_text_height)), constants.COLOR_WHITE, constants.MENU_FONT, constants.COLOR_GREY)
            else:
                draw_text(local_inventory_surface, name, (0, 0 + (line * menu_text_height)), constants.COLOR_WHITE, constants.MENU_FONT, constants.COLOR_BLACK)

        draw_game()
        SURFACE_MAIN.blit(local_inventory_surface, (menu_x,menu_y))
        CLOCK.tick(constants.GAME_FPS)
        pygame.display.update()

def menu_target_select(coords_origin = None, range = None, pen_walls = True, pen_creature = True, radius = None):
    '''This menu lets the player select a tile.

    This function pauses, the game, produces an on screen square and when the player presses the left MB, will return map address.
    '''
    menu_close = False
    while not menu_close:

        mouse_x,mouse_y = pygame.mouse.get_pos()
        events_list = pygame.event.get()
        mouse_x_rel = mouse_x//constants.CELL_WIDTH
        mouse_y_rel = mouse_y//constants.CELL_HEIGHT
        valid_tiles=[]
        if coords_origin:
            list_of_tiles = map_find_line(coords_origin, (mouse_x_rel,mouse_y_rel))
            for i, (x, y) in enumerate(list_of_tiles):
                valid_tiles.append((x,y))
                if range and i == range-1:
                    break
                if pen_walls == False:
                     if GAME.current_map[x][y].block_path: break
                if pen_creature == False and map_check_for_creatures(x,y):
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
        draw_game()
        for (tile_x, tile_y) in valid_tiles:
            if (tile_x, tile_y) == valid_tiles[-1]:
                draw_tile_rect((tile_x, tile_y), mark='X')
            draw_tile_rect((tile_x, tile_y))
        if radius:
            area_effect = map_find_radius(valid_tiles[-1], radius)
            for (rad_x, rad_y) in area_effect:
                    draw_tile_rect((rad_x, rad_y))
        pygame.display.flip()
        CLOCK.tick(constants.GAME_FPS)

#GENERATORS
def gen_player(coords):
    x,y = coords

    container_com = com_Container()
    creature_com = com_Creature("Mingo", base_atk = 3)
    player = obj_Actor(x, y, "the Maravinchi", ASSETS.A_PLAYER, creature=creature_com, container=container_com)
    return player

def gen_item(coords):
    random_num = libtcodpy.random_get_int(0,1,5)

    if random_num == 1: new_item = gen_scroll_lightning(coords)
    elif random_num == 2: new_item = gen_scroll_fireball(coords)
    elif random_num == 3: new_item = gen_scroll_confusion(coords)
    elif random_num == 4: new_item = gen_weapon_sword(coords)
    elif random_num == 5: new_item = gen_armor_shield(coords)

    GAME.current_objects.append(new_item)

def gen_scroll_lightning(coords):
    x, y = coords

    damage = libtcodpy.random_get_int(0, 1, 10)
    m_range = libtcodpy.random_get_int(0, 3, 9)

    item_com = com_Item(use_function = cast_lightning, value=(damage, m_range))

    return_object = obj_Actor(x, y, "lightning scroll", ASSETS.lightning_scroll, item = item_com)

    return return_object 

def gen_scroll_fireball(coords):
    x, y = coords

    damage = libtcodpy.random_get_int(0, 1, 3)
    radius = libtcodpy.random_get_int(0, 1, 3)
    m_range = libtcodpy.random_get_int(0, 3, 9)

    item_com = com_Item(use_function = cast_fireball, value=(damage, radius, m_range))

    return_object = obj_Actor(x, y, "fireball scroll", ASSETS.fireball_scroll, item = item_com)

    return return_object 

def gen_scroll_confusion(coords):
    x, y = coords

    effect_length = libtcodpy.random_get_int(0, 3, 9)

    item_com = com_Item(use_function = cast_confusion, value=effect_length)

    return_object = obj_Actor(x, y, "confusion scroll", ASSETS.confusion_scroll, item = item_com)

    return return_object 

def gen_weapon_sword(coords):

    x,y = coords

    bonus = libtcodpy.random_get_int(0,1,2)

    equipment_com = com_Equipment(attack_bonus= bonus)

    return_object = obj_Actor(x,y,"sword", animation = ASSETS.sword, equipment=equipment_com)

    return return_object

def gen_armor_shield(coords):

    x,y = coords

    bonus = libtcodpy.random_get_int(0,1,2)

    equipment_com = com_Equipment(defense_bonus = bonus)

    return_object = obj_Actor(x,y,"shield", animation = ASSETS.shield, equipment=equipment_com)

    return return_object

def gen_enemy(coords):
    random_num = libtcodpy.random_get_int(0,1,100)

    if random_num <= 15: 
        new_enemy = gen_fire_elemental(coords)
    elif random_num <= 50 and random_num >15: 
        new_enemy = gen_skeleton(coords)
    else: 
        new_enemy = gen_skeleton_mage(coords)

    GAME.current_objects.append(new_enemy)


def gen_fire_elemental(coords):
    
    x,y = coords

    creature_name = libtcodpy.namegen_generate("demon male")
    creature_com = com_Creature(creature_name, base_atk =2 , base_def = 5, hp = 16, death_function = death_monster)
    ai_com = ai_Chase()
    fire = obj_Actor(x, y, "fire elemental", ASSETS.fire_elemental, creature=creature_com, ai = ai_com)
    return fire

def gen_skeleton(coords):
    x,y = coords
    creature_name = libtcodpy.namegen_generate("demon male")
    creature_com = com_Creature(creature_name, base_atk = 1 , base_def = 1, hp = 1, death_function = death_monster)
    ai_com = ai_Chase()
    skeleton = obj_Actor(x, y, "skeleton", ASSETS.skeleton, creature=creature_com, ai = ai_com)
    return skeleton

def gen_skeleton_mage(coords):
    x,y = coords
    creature_name = libtcodpy.namegen_generate("demon male")
    rnd_hp = libtcodpy.random_get_int(0,4,12)
    creature_com = com_Creature(creature_name,  base_atk = 3 , base_def = 1, hp = rnd_hp, death_function = death_monster)
    ai_com = ai_Chase()
    skeleton_mage = obj_Actor(x, y, "skeleton mage", ASSETS.skeleton_mage, creature=creature_com, ai = ai_com)
    return skeleton_mage

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
        pygame.display.flip()
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

    libtcodpy.namegen_parse('assets\\namegen\\mingos_demon.cfg')

    CLOCK = pygame.time.Clock()

    GAME.current_objects = []

    gen_item(helper_random_coords())
    gen_item(helper_random_coords())
    gen_item(helper_random_coords()) 

    gen_enemy(helper_random_coords())
    gen_enemy(helper_random_coords())

    PLAYER = gen_player((1,1))

    GAME.current_objects.append(PLAYER)

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
