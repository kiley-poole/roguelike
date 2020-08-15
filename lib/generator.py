from lib import globalvars, actor, constants, death, ai, magic

import tcod as libtcodpy

#GENERATORS
def gen_player(coords):
    global PLAYER
    x,y = coords
    container_com = actor.com_Container()
    creature_com = actor.com_Creature("Mingo", base_atk = 20, base_def=20, death_function=death.death_player)
    globalvars.PLAYER = actor.obj_Actor(x, y, "Maravinchi", animation_key= "A_PLAYER", depth=constants.DEPTH_PLAYER, creature=creature_com, container=container_com)
    globalvars.GAME.current_objects.append(globalvars.PLAYER)

def gen_item(coords):
    random_num = libtcodpy.random_get_int(0,1,5)

    if random_num == 1: new_item = gen_scroll_lightning(coords)
    elif random_num == 2: new_item = gen_scroll_fireball(coords)
    elif random_num == 3: new_item = gen_scroll_confusion(coords)
    elif random_num == 4: new_item = gen_weapon_sword(coords)
    elif random_num == 5: new_item = gen_armor_shield(coords)

    globalvars.GAME.current_objects.append(new_item)

def gen_scroll_lightning(coords):
    x, y = coords

    damage = libtcodpy.random_get_int(0, 1, 10)
    m_range = libtcodpy.random_get_int(0, 3, 9)

    item_com = actor.com_Item(use_function = magic.cast_lightning, value=(damage, m_range))

    return_object = actor.obj_Actor(x, y, "lightning scroll", animation_key= "lightning_scroll", depth=constants.DEPTH_ITEM, item = item_com)

    return return_object 

def gen_scroll_fireball(coords):
    x, y = coords

    damage = libtcodpy.random_get_int(0, 1, 3)
    radius = libtcodpy.random_get_int(0, 1, 3)
    m_range = libtcodpy.random_get_int(0, 3, 9)

    item_com = actor.com_Item(use_function = magic.cast_fireball, value=(damage, radius, m_range))

    return_object = actor.obj_Actor(x, y, "fireball scroll", animation_key= "fireball_scroll", depth=constants.DEPTH_ITEM, item = item_com)

    return return_object 

def gen_scroll_confusion(coords):
    x, y = coords

    effect_length = libtcodpy.random_get_int(0, 3, 9)

    item_com = actor.com_Item(use_function = magic.cast_confusion, value=effect_length)

    return_object = actor.obj_Actor(x, y, "confusion scroll", animation_key= "confusion_scroll", depth=constants.DEPTH_ITEM, item = item_com)

    return return_object 

def gen_weapon_sword(coords):

    x,y = coords

    bonus = libtcodpy.random_get_int(0,1,2)

    equipment_com = actor.com_Equipment(attack_bonus= bonus)

    return_object = actor.obj_Actor(x,y,"sword", animation_key= "sword", depth=constants.DEPTH_ITEM, equipment=equipment_com)

    return return_object

def gen_armor_shield(coords):

    x,y = coords

    bonus = libtcodpy.random_get_int(0,1,2)

    equipment_com = actor.com_Equipment(defense_bonus = bonus)

    return_object = actor.obj_Actor(x,y,"shield", animation_key= "shield", depth=constants.DEPTH_ITEM, equipment=equipment_com)

    return return_object

def gen_enemy(coords):
    random_num = libtcodpy.random_get_int(0,1,100)

    if random_num <= 15: 
        new_enemy = gen_skeleton_mage(coords)
    elif random_num <= 50: 
        new_enemy = gen_skeleton(coords)
    elif random_num <= 80:
        new_enemy = gen_fire_elemental(coords)
    else: 
        new_enemy = gen_healing_sprite(coords)

    globalvars.GAME.current_objects.append(new_enemy)

def gen_fire_elemental(coords):
    
    x,y = coords

    creature_name = libtcodpy.namegen_generate("demon male")
    creature_com = actor.com_Creature(creature_name, base_atk = 4 , base_def = 0, hp = 4, death_function = death.death_monster)
    ai_com = ai.ai_Chase()
    fire = actor.obj_Actor(x, y, "fire elemental", animation_key= "fire_elemental", depth=constants.DEPTH_CREATURE, creature=creature_com, ai = ai_com)
    return fire

def gen_skeleton(coords):
    x,y = coords
    creature_name = libtcodpy.namegen_generate("demon male")
    creature_com = actor.com_Creature(creature_name, base_atk = 1 , base_def = 1, hp = 1, death_function = death.death_monster)
    ai_com = ai.ai_Chase()
    skeleton = actor.obj_Actor(x, y, "skeleton", animation_key= "skeleton", depth=constants.DEPTH_CREATURE, creature=creature_com, ai = ai_com)
    return skeleton

def gen_skeleton_mage(coords):
    x,y = coords
    creature_name = libtcodpy.namegen_generate("demon male")
    rnd_hp = libtcodpy.random_get_int(0,4,12)
    creature_com = actor.com_Creature(creature_name,  base_atk = 3 , base_def = 1, hp = rnd_hp, death_function = death.death_monster)
    ai_com = ai.ai_Chase()
    skeleton_mage = actor.obj_Actor(x, y, "skeleton mage", animation_key= "skeleton_mage", depth=constants.DEPTH_CREATURE, creature=creature_com, ai = ai_com)
    return skeleton_mage

def gen_healing_sprite(coords):
    x,y = coords
    creature_name = libtcodpy.namegen_generate("demon female")
    creature_com = actor.com_Creature(creature_name,  base_atk = 0 , base_def = 0, hp = 1, death_function = death.death_healing_sprite)
    ai_com = ai.ai_Flee()
    item_com = actor.com_Item(use_function=magic.cast_heal, value=2)
    healing_sprite = actor.obj_Actor(x, y, "healing sprite", animation_key= "healing_sprite", depth=constants.DEPTH_CREATURE, creature=creature_com, ai = ai_com, item=item_com)
    return healing_sprite

def gen_stairs(coords, downwards = True):
    x, y = coords

    if downwards:
        stairs_com = actor.com_Stairs()
        stairs = actor.obj_Actor(x, y, "stairs", animation_key = "S_DOWNSTAIRS", stairs = stairs_com)
    else:
        stairs_com = actor.com_Stairs(downwards)
        stairs = actor.obj_Actor(x, y, "stairs", animation_key = "S_UPSTAIRS", stairs = stairs_com)

    globalvars.GAME.current_objects.append(stairs)

def gen_portal(coords):
    x,y = coords

    port_com = actor.com_Portal()
    portal = actor.obj_Actor(x,y, "exit port", animation_key="S_PORTAL_CLOSED", depth= constants.DEPTH_CORPSE, exitportal=port_com)

    globalvars.GAME.current_objects.append(portal)

def gen_lamp(coords):
    x, y = coords

    item_com = actor.com_Item()
    return_object = actor.obj_Actor(x,y,"DIAMOND", animation_key = "diamond", depth= constants.DEPTH_ITEM, item = item_com)
    globalvars.GAME.current_objects.append(return_object)
