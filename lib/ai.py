from lib import game, globalvars, constants
import tcod as libtcodpy
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
            game.game_message(self.owner.display_name + " is no longer confused", constants.COLOR_WHITE)

class ai_Chase:
    '''
    A basic monster ai which chases and harms player
    '''

    def take_turn(self):
        monster = self.owner
        if libtcodpy.map_is_in_fov(globalvars.FOV_MAP, monster.x, monster.y):
            if monster.distance_to(globalvars.PLAYER) >= 2:
                self.owner.move_towards(globalvars.PLAYER)
            elif globalvars.PLAYER.creature.hp > 0:
                monster.creature.attack(globalvars.PLAYER)

class ai_Flee:
    '''
    A basic monster ai which chases and harms player
    '''

    def take_turn(self):
        monster = self.owner
        if libtcodpy.map_is_in_fov(globalvars.FOV_MAP, monster.x, monster.y):
            self.owner.move_away(globalvars.PLAYER)
