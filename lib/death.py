import datetime
from lib import game, globalvars, constants

#DEATH
def death_monster(monster):
    '''On death, monster stops'''
    game.game_message((monster.creature.name + " is dead!"), constants.COLOR_GREY)
    monster.animation = globalvars.ASSETS.dead_monster
    monster.animation_key = "dead_monster"
    monster.depth = constants.DEPTH_CORPSE
    monster.creature = None
    monster.ai = None

def death_healing_sprite(monster):
    '''On death, monster stops'''
    game.game_message((monster.creature.name + " is dead! Gather his essence to heal!"), constants.COLOR_GREEN)
    monster.animation = globalvars.ASSETS.healing_drop
    monster.animation_key = "healing_drop"
    monster.depth = constants.DEPTH_ITEM
    monster.creature = None
    monster.ai = None

def death_player(player):
    player.state = "DEAD"

    globalvars.SURFACE_MAIN.fill(constants.COLOR_BLACK)

    draw_text(SURFACE_MAIN, "YOU DEAD!", (constants.CAM_WIDTH//2, constants.CAM_HEIGHT//2 ), constants.COLOR_WHITE,font=constants.MAIN_MENU_FONT, center=True)
    pygame.display.update()

    file_name =   "data\\"+ globalvars.PLAYER.creature.name + "." + datetime.datetime.now().strftime("%Y%B%d%f") + ".txt"
    legacy_file = open(file_name, 'a+')
    for message,color in GAME.message_history:
        legacy_file.write(message + "\n")

    pygame.time.wait(2000)
