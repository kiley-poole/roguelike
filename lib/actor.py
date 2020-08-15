import datetime
import math
import os
import os.path

import pygame
import tcod as libtcodpy

from lib import constants, draw, game, globalvars, maps


#OBJECTS
class obj_Actor:
    def __init__(self, x, y, name_object, animation_key, animation_speed = .5, depth = 0, state = None,
                creature = None, ai = None, container = None, item = None, equipment = None, stairs = None, exitportal = None):
        self.x = x
        self.y = y
        self.animation_key = animation_key
        self.animation = globalvars.ASSETS.animation_dict[self.animation_key]
        self.name_object = name_object
        self.animation_speed = animation_speed / 1.0
        self.flicker = self.animation_speed/len(self.animation) 
        self.flicker_timer = 0.0
        self.sprite_image = 0
        self.depth = depth
        self.state = state

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
            
        self.stairs = stairs
        if self.stairs:
            self.stairs.owner = self

        self.exitportal = exitportal
        if self.exitportal:
            self.exitportal.owner = self

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
        is_visible = libtcodpy.map_is_in_fov(globalvars.FOV_MAP, self.x, self.y)
        if is_visible:
            if len(self.animation) == 1:
                globalvars.SURFACE_MAP.blit(self.animation[0], ( self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))
            else:
                if globalvars.CLOCK.get_fps() > 0.0:
                    self.flicker_timer += 1/globalvars.CLOCK.get_fps()
                if self.flicker_timer >= self.flicker:
                    self.flicker_timer = 0.0
                    if self.sprite_image >= len(self.animation) - 1:
                        self.sprite_image = 0
                    else:
                        self.sprite_image += 1
                globalvars.SURFACE_MAP.blit(self.animation[self.sprite_image], ( self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))

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

    def move_away(self,other):

        dx = self.x - other.x 
        dy = self.y - other.y 

        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx/distance))
        dy = int(round(dy/distance))

        self.creature.move(dx,dy)
    def animation_destroy(self):
        self.animation = None    
    
    def animation_init(self):
        self.animation = globalvars.ASSETS.animation_dict[self.animation_key]
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

        tile_is_wall = (globalvars.GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path == True)

        target = maps.map_check_for_creatures(self.owner.x + dx, self.owner.y + dy, self.owner)
         
        if target:
            self.attack(target)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target):
        damage_dealt = self.power - target.creature.defense
        if damage_dealt < 0: damage_dealt = 0
        game.game_message((self.name + " attacks " + target.creature.name + " for " + str(damage_dealt) + " damage!"), constants.COLOR_WHITE)
        target.creature.take_damage(damage_dealt)

        if damage_dealt > 0 and self.owner is globalvars.PLAYER:
            pygame.mixer.Sound.play(globalvars.RANDOM_ENGINE.choice(globalvars.ASSETS.sfx_list_hit))



    def take_damage(self,damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
        game.game_message(self.owner.display_name + "'s health is " + str(self.hp) + "/" + str(self.maxhp), constants.COLOR_RED)

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
                game.game_message("equipment slot is occupied", constants.COLOR_RED)
                return 
        self.equipped = True
        game.game_message("equipped", constants.COLOR_WHITE)
    def unequip(self):
        self.equipped = False
        game.game_message("unequipped", constants.COLOR_WHITE)

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
                game.game_message(self.owner.display_name + " Picked Up", constants.COLOR_WHITE)
                actor.container.inventory.append(self.owner)
                self.owner.animation_destroy()
                globalvars.GAME.current_objects.remove(self.owner)
                self.container = actor.container
    
    def drop(self, pos_x, pos_y):
        globalvars.GAME.current_objects.append(self.owner)
        self.owner.animation_init()
        self.container.inventory.remove(self.owner)
        self.owner.x = pos_x
        self.owner.y = pos_y
        game.game_message("Item Dropped!", constants.COLOR_WHITE)

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
                game.game_message("You're at full health. Healing would be pointless.", constants.COLOR_RED)
            else:
                self.container.inventory.remove(self.owner)

class com_Stairs:
    def __init__(self, downwards = True):
        self.downwards = downwards
    
    def use(self):
        if self.downwards:
            globalvars.GAME.transition_next()
        else:
            globalvars.GAME.transition_prev()

class com_Portal:
    def __init__(self):
        self.open_animation = "S_PORTAL_OPEN"
        self.closed_animation = "S_PORTAL_CLOSED"
    
    def update(self):

        found_lamp = False

        portal_open = self.owner.state == "OPEN"

        for obj in globalvars.PLAYER.container.inventory:
            if obj.name_object == "DIAMOND":
                found_lamp = True
        
        if found_lamp and not portal_open:
            self.owner.state = "OPEN"
            self.owner.animation_key = "S_PORTAL_OPEN"
            self.owner.animation_init()
        
        if not found_lamp and portal_open:
            self.owner.state = "CLOSED"
            self.owner.animation_key = "S_PORTAL_CLOSED"
            self.owner.animation_init()

    def use(self):
        if self.owner.state == "OPEN":
            globalvars.PLAYER.state = "STATUS_WIN"

            globalvars.SURFACE_MAIN.fill(constants.COLOR_WHITE)

            draw.draw_text(globalvars.SURFACE_MAIN, "YOU WON!", (constants.CAM_WIDTH//2, constants.CAM_HEIGHT//2 ), constants.COLOR_BLACK,font=constants.MAIN_MENU_FONT, center=True)
            pygame.display.update()

            file_name =   "data\\win_"+globalvars.PLAYER.creature.name + "." + datetime.datetime.now().strftime("%Y%B%d%f") + ".txt"

            #if os.path.isFile("data\\savedate\\savegame"):
            #   os.remove("data\\savedate\\savegame")

            legacy_file = open(file_name, 'a+')
            legacy_file.write("WINNING GAME SHITHEAD!\n" )
            for message,color in globalvars.GAME.message_history:
                legacy_file.write(message + "\n")

            pygame.time.wait(2000)
