from lib import game, constants, globalvars, menu, maps, ai

#MAGIC
def cast_heal(target, value):
    if target.creature.hp == target.creature.maxhp:
       game.game_message(target.creature.name + " the " + target.name_object + " is at full HP!", constants.COLOR_WHITE) 
       return "cancelled"
    else:    
       game.game_message(target.creature.name + " the " + target.name_object + " healed for " + str(value) + " HP!", constants.COLOR_WHITE)
       target.creature.heal(value)
       game.game_message("Current HP is " + str(target.creature.hp) + '/' + str(target.creature.maxhp), constants.COLOR_WHITE)
    return None

def cast_lightning(caster, T_damage_range):

    player_locat = (caster.x, caster.y)

    damage, m_range = T_damage_range

    tile_selected = menu.menu_target_select(coords_origin = player_locat, range = m_range, pen_walls=False)
    if tile_selected:
        list_of_tiles = maps.map_find_line(player_locat, tile_selected)

        for i, (x,y) in enumerate(list_of_tiles):
            target = maps.map_check_for_creatures(x,y)
            if target:
                target.creature.take_damage(damage)

def cast_fireball(caster,T_damage_radius_range):

    damage, internal_radius , max_range = T_damage_radius_range
    player_locat = (caster.x, caster.y)

    tile_selected = menu.menu_target_select(coords_origin = player_locat, range = max_range, pen_walls=False, pen_creature=False, radius=internal_radius)
    
    tiles_to_damage = maps.map_find_radius(tile_selected, internal_radius)

    creature_hit = False

    for (x,y) in tiles_to_damage:
        creature_to_dmg = maps.map_check_for_creatures(x,y)
        if creature_to_dmg:
            creature_to_dmg.creature.take_damage(damage)
            if creature_to_dmg is not globalvars.PLAYER:
                creature_hit = True
    
    if creature_hit:
        game.game_message("The fireball fucks shit up hardcore!", constants.COLOR_RED)

def cast_confusion(caster, effect_length):
    tile_selected = menu.menu_target_select()
    if tile_selected:
        x,y = tile_selected
        target=  maps.map_check_for_creatures(x,y)
        if target:
            oldai = target.ai
            target.ai = ai.ai_Confuse(old_ai = oldai, num_turns = effect_length)
            target.ai.owner = target
            game.game_message(target.display_name + " is confused", constants.COLOR_RED)
