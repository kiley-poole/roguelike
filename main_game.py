# pylint: disable=no-member
import pygame
import tcod as libtcodpy
import constants

#STRUCTS
class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False

#OBJECTS
class obj_Actor:
    def __init__(self, x, y, name_object, sprite, creature = None, ai = None):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.name_object = name_object
        
        self.creature = creature
        if creature:
            creature.owner = self
        
        self.ai = ai
        if ai:
            ai.owner = self

    def draw(self):
        is_visible = libtcodpy.map_is_in_fov(FOV_MAP, self.x, self.y)
        if is_visible:
            SURFACE_MAIN.blit(self.sprite, ( self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))
    

#COMPONENTS
class com_Creature:
    '''Creatures have health, can dmg other objects. Can die.'''

    def __init__(self, name_instance, hp = 10, death_function = None):
        self.name = name_instance
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function

    def move(self, dx, dy):

        tile_is_wall = (GAME_MAP[self.owner.x + dx][self.owner.y + dy].block_path == True)

        target = map_check_for_creatures(self.owner.x + dx, self.owner.y + dy, self.owner)
         
        if target:
            self.attack(target, 3)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target, damage):
        print(self.name + " attacks " + target.creature.name + " for " + str(damage) + " damage!")
        target.creature.take_damage(damage)

    def take_damage(self,damage):
        self.hp -= damage
        print(self.name + "'s health is " + str(self.hp) + "/" + str(self.maxhp))

        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

#class com_Item:

#class com_Container:

#AI
class ai_Test:
    '''Once per turn execute'''
    def take_turn(self):
        self.owner.creature.move(libtcodpy.random_get_int(0, -1, 1), libtcodpy.random_get_int(0, -1, 1))

def death_monster(monster):
    '''On death, monster stops'''

    print(monster.creature.name + " is dead!")

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
        for object in GAME_OBJECTS: 
            if (object is not exclude_object and 
                object.x == x and 
                object.y == y and 
                object.creature):

                target = object
                
            if target:
                return target
    
    else:
        #check object list for any creature at location
        for object in GAME_OBJECTS: 
            if (object.x == x and 
                object.y == y and 
                object.creature):

                target = object
                
            if target:
                return target

def map_make_fov(incoming_map):
    global FOV_MAP

    FOV_MAP = libtcodpy.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            libtcodpy.map_set_properties(FOV_MAP, x ,y,
                not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)

def map_calc_fov():
    global FOV_CALC

    if FOV_CALC:
        FOV_CALC = False
        libtcodpy.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS, constants.FOV_ALGO)
#DRAW FUNCTIONS
def draw_game():

    global SURFACE_MAIN

    SURFACE_MAIN.fill(constants.BACKGROUND_COLOR)
    draw_map(GAME_MAP)
    for obj in GAME_OBJECTS:
        obj.draw()
    pygame.display.flip()

def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0,constants.MAP_HEIGHT):

            is_visible = libtcodpy.map_is_in_fov(FOV_MAP, x ,y)

            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path == True:
                    SURFACE_MAIN.blit(constants.S_WALL, (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))
                else:
                    SURFACE_MAIN.blit(constants.S_FLOOR, (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))
        
            elif map_to_draw[x][y].explored:
                
                if map_to_draw[x][y].block_path == True:
                    SURFACE_MAIN.blit(constants.S_WALLEXPLORED, (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))
                else:
                    SURFACE_MAIN.blit(constants.S_FLOOREXPLORED, (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))


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
            for obj in GAME_OBJECTS:
                if obj.ai:
                    obj.ai.take_turn()
        draw_game()
    pygame.quit()

def game_init():
    '''Function inits the game window and pygame'''

    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS, FOV_CALC

    #init pygame
    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode( (constants.MAP_WIDTH*constants.CELL_WIDTH, 
                                             constants.MAP_HEIGHT*constants.CELL_HEIGHT) )

    GAME_MAP = map_create()

    FOV_CALC = True

    creature_com1 = com_Creature("Tom")
    PLAYER = obj_Actor(1, 1, "Python", constants.S_PLAYER, creature=creature_com1)

    creature_com2 = com_Creature("Dave",  death_function = death_monster)
    ai_com = ai_Test()
    ENEMY = obj_Actor(12, 12, "Crab", constants.S_CRAB, creature=creature_com2, ai = ai_com)

    GAME_OBJECTS = [ENEMY, PLAYER]

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
    return "no-action"

if __name__ == '__main__':
    game_init()
    game_main_loop()
