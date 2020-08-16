import string
import pygame
from lib import constants, data, globalvars


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

        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet1, (0,0), (self.tiledict[column]*width, row*height, width, height))
        image.set_colorkey(color_key)
        if scale:
            (new_w, new_h) = scale
            image = pygame.transform.scale(image, (new_w, new_h))
        return image
        
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

class obj_Assets:
    def __init__(self):
        self.load_assets()
        self.adjust_sound()

    def load_assets(self):
        #Sheets
        ##Character Sheets
        self.reptiles_spritesheet = obj_Spritesheet("assets/Characters/Reptile0.png", "assets/Characters/Reptile1.png")
        self.humanoids_spritesheet = obj_Spritesheet("assets/Characters/Humanoid0.png","assets/Characters/Humanoid1.png")
        self.player_spritesheet = obj_Spritesheet("assets/Characters/Player0.png","assets/Characters/Player1.png")
        self.demon_spritesheet = obj_Spritesheet("assets/Characters/Demon0.png","assets/Characters/Demon1.png")
        self.undead_spritesheet = obj_Spritesheet("assets/Characters/Undead0.png","assets/Characters/Undead1.png")
        self.elemental_spritesheet = obj_Spritesheet("assets/Characters/Elemental0.png","assets/Characters/Elemental1.png")
        #Object Sheets
        self.walls_spritesheet = obj_Spritesheet("assets/Objects/Wall.png")
        self.floors_spritesheet = obj_Spritesheet("assets/Objects/Floor.png")
        self.stairs_spritesheet = obj_Spritesheet("assets/Objects/Tile.png")
        self.doors_spritesheet = obj_Spritesheet("assets/Objects/Door0.png", "assets/Objects/Door1.png")
        self.misc_items = obj_Spritesheet("assets/Objects/Decor0.png", "assets/Objects/Decor1.png")
        self.effects_spritesheet = obj_Spritesheet("assets/Objects/Effect0.png", "assets/Objects/Effect1.png")
        #Item Sheets
        self.longWep_spritesheet = obj_Spritesheet("assets/Items/LongWep.png")
        self.shield_spritesheet = obj_Spritesheet("assets/Items/Shield.png")
        self.scrolls_spritesheet = obj_Spritesheet("assets/Items/Scroll.png")
        self.treasure_spritesheet = obj_Spritesheet("assets/Items/Money.png")

        #PC/NPCs
        self.dead_monster = self.misc_items.get_animation('a', 12, 2, 16, 16, constants.COLOR_BLACK, (32,32))
        self.A_PLAYER = self.player_spritesheet.get_animation('c', 8, 2, 16, 16, constants.COLOR_BLACK, (32,32))
        self.A_ENEMY = self.humanoids_spritesheet.get_animation('a', 0, 2, 16, 16, constants.COLOR_BLACK, (32,32))
        self.fire_elemental = self.demon_spritesheet.get_animation('a', 1, 2, 16, 16, constants.COLOR_BLACK, (32,32))
        self.skeleton = self.undead_spritesheet.get_animation('a', 2, 2, 16, 16, constants.COLOR_BLACK, (32,32))
        self.skeleton_mage = self.undead_spritesheet.get_animation('h', 2, 2, 16, 16, constants.COLOR_BLACK, (32,32))
        self.healing_sprite = self.elemental_spritesheet.get_animation('a', 10, 2, 16, 16, constants.COLOR_BLACK, (32,32))

        #Terrain
        self.S_FLOOR = self.floors_spritesheet.get_animation('i', 16, 1, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALLEXPLORED = self.walls_spritesheet.get_animation('d', 12, 1, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_FLOOREXPLORED = self.floors_spritesheet.get_animation('i', 22, 1, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_UPSTAIRS = self.stairs_spritesheet.get_animation('e', 1, 1, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_DOWNSTAIRS = self.stairs_spritesheet.get_animation('f', 1, 1, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_PORTAL_OPEN = self.doors_spritesheet.get_animation('f', 5, 2, 16, 16,constants.COLOR_BLACK, (32,32))
        self.S_PORTAL_CLOSED = self.doors_spritesheet.get_animation('e', 5, 2, 16, 16,constants.COLOR_BLACK, (32,32))
        
        #UI
        self.MAIN_MENU_BG = pygame.image.load("assets/main_menu.jpg")
        self.MAIN_MENU_BG = pygame.transform.scale(self.MAIN_MENU_BG, (constants.CAM_WIDTH, constants.CAM_HEIGHT))
        self.settings_menu_bg = pygame.image.load("assets/UI/red_panel.png")
        self.settings_menu_bg = pygame.transform.scale(self.settings_menu_bg, (200,200))
        self.sfx_slider_bg = pygame.image.load("assets/UI/grey_button06.png")
        self.sfx_slider_bg = pygame.transform.scale(self.sfx_slider_bg, (125,15))
        self.sfx_slider_tab = pygame.image.load("assets/UI/green_button12.png")
        self.sfx_slider_tab = pygame.transform.scale(self.sfx_slider_tab, (20,20))

        #Items
        self.sword = self.longWep_spritesheet.get_animation('a', 1, 1, 16, 16,constants.COLOR_BLACK, (32,32))
        self.shield = self.shield_spritesheet.get_animation('c', 0, 1, 16, 16,constants.COLOR_BLACK, (32,32))
        self.lightning_scroll = self.scrolls_spritesheet.get_animation('a', 0, 1, 16, 16,constants.COLOR_BLACK, (32,32))
        self.fireball_scroll = self.scrolls_spritesheet.get_animation('c', 2, 1, 16, 16,constants.COLOR_BLACK, (32,32))
        self.confusion_scroll = self.scrolls_spritesheet.get_animation('d', 5, 1, 16, 16,constants.COLOR_BLACK, (32,32))
        self.healing_drop = self.effects_spritesheet.get_animation('h', 23, 2, 16, 16,constants.COLOR_BLACK, (32,32))
        self.diamond = self.treasure_spritesheet.get_animation('b', 2, 1, 16, 16,constants.COLOR_BLACK, (32,32))

        #WALL SET 1
        self.S_WALL00 = self.walls_spritesheet.get_image('a', 10, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL01 = self.walls_spritesheet.get_image('b', 10, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL02 = self.walls_spritesheet.get_image('b', 9, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL03 = self.walls_spritesheet.get_image('a', 11, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL04 = self.walls_spritesheet.get_image('a', 10, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL05 = self.walls_spritesheet.get_image('a', 10, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL06 = self.walls_spritesheet.get_image('a', 9, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL07 = self.walls_spritesheet.get_image('d', 10, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL08 = self.walls_spritesheet.get_image('b', 9, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL09 = self.walls_spritesheet.get_image('c', 11, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL10 = self.walls_spritesheet.get_image('b', 9, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL11 = self.walls_spritesheet.get_image('e', 11, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL12 = self.walls_spritesheet.get_image('c', 9, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL13 = self.walls_spritesheet.get_image('f', 10, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL14 = self.walls_spritesheet.get_image('e', 9, 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL15 = self.walls_spritesheet.get_image('e', 10, 16, 16,constants.COLOR_WHITE, (32,32))

        #WALL SET 1 EXPLORED
        self.S_WALL00_EX = self.walls_spritesheet.get_image('b', (10+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL01_EX = self.walls_spritesheet.get_image('b', (10+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL02_EX = self.walls_spritesheet.get_image('b', (9+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL03_EX = self.walls_spritesheet.get_image('a', (11+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL04_EX = self.walls_spritesheet.get_image('a', (10+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL05_EX = self.walls_spritesheet.get_image('a', (10+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL06_EX = self.walls_spritesheet.get_image('a', (9+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL07_EX = self.walls_spritesheet.get_image('d', (10+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL08_EX = self.walls_spritesheet.get_image('b', (9+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL09_EX = self.walls_spritesheet.get_image('c', (11+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL10_EX = self.walls_spritesheet.get_image('b', (9+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL11_EX = self.walls_spritesheet.get_image('e', (11+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL12_EX = self.walls_spritesheet.get_image('c', (9+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL13_EX = self.walls_spritesheet.get_image('f', (10+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL14_EX = self.walls_spritesheet.get_image('e', (9+3), 16, 16,constants.COLOR_WHITE, (32,32))
        self.S_WALL15_EX = self.walls_spritesheet.get_image('e', (10+3), 16, 16,constants.COLOR_WHITE, (32,32))
        
        self.wall_dict = {
            0 : self.S_WALL00,
            1 : self.S_WALL01,
            2 : self.S_WALL02,
            3 : self.S_WALL03,
            4 : self.S_WALL04,
            5 : self.S_WALL05,
            6 : self.S_WALL06,
            7 : self.S_WALL07,
            8 : self.S_WALL08,
            9 : self.S_WALL09,
            10 : self.S_WALL10,
            11 : self.S_WALL11,
            12 : self.S_WALL12,
            13 : self.S_WALL13,
            14 : self.S_WALL14,
            15 : self.S_WALL15,
        }
        
        self.wall_ex_dict = {
            0 : self.S_WALL00_EX,
            1 : self.S_WALL01_EX,
            2 : self.S_WALL02_EX,
            3 : self.S_WALL03_EX,
            4 : self.S_WALL04_EX,
            5 : self.S_WALL05_EX,
            6 : self.S_WALL06_EX,
            7 : self.S_WALL07_EX,
            8 : self.S_WALL08_EX,
            9 : self.S_WALL09_EX,
            10 : self.S_WALL10_EX,
            11 : self.S_WALL11_EX,
            12 : self.S_WALL12_EX,
            13 : self.S_WALL13_EX,
            14 : self.S_WALL14_EX,
            15 : self.S_WALL15_EX,
        }

        self.animation_dict = {
            "dead_monster": self.dead_monster,
            "A_PLAYER": self.A_PLAYER,
            "A_ENEMY": self.A_ENEMY,
            "fire_elemental": self.fire_elemental,
            "skeleton": self.skeleton,
            "skeleton_mage": self.skeleton_mage,
            "sword": self.sword,
            "shield": self.shield,
            "lightning_scroll": self.lightning_scroll,
            "fireball_scroll": self.fireball_scroll,
            "confusion_scroll": self.confusion_scroll,
            "S_UPSTAIRS": self.S_UPSTAIRS,
            "S_DOWNSTAIRS": self.S_DOWNSTAIRS,
            "S_PORTAL_OPEN": self.S_PORTAL_OPEN,
            "S_PORTAL_CLOSED": self.S_PORTAL_CLOSED,
            "healing_drop": self.healing_drop,
            "healing_sprite": self.healing_sprite,
            "diamond": self.diamond
        }

        self.snd_list = []

        self.music_bg = "assets/audio/music/lost-control.mp3"
        self.hit_1 = self.add_sound("assets/audio/sfx/hit_hurt.wav")
        self.hit_2 = self.add_sound("assets/audio/sfx/hit_hurt2.wav")
        self.hit_3 = self.add_sound("assets/audio/sfx/hit_hurt3.wav")
        self.hit_4 = self.add_sound("assets/audio/sfx/hit_hurt4.wav")
        self.hit_5 = self.add_sound("assets/audio/sfx/hit_hurt5.wav")
        self.hit_6 = self.add_sound("assets/audio/sfx/hit_hurt6.wav")
        self.hit_7 = self.add_sound("assets/audio/sfx/hit_hurt7.wav")
        self.hit_8 = self.add_sound("assets/audio/sfx/hit_hurt8.wav")

        self.sfx_list_hit = [
            self.hit_1,
            self.hit_2,
            self.hit_3, 
            self.hit_4, 
            self.hit_5, 
            self.hit_6, 
            self.hit_7, 
            self.hit_8 
        ]

    def add_sound(self, file_address):

        new_sound = pygame.mixer.Sound("assets/audio/sfx/hit_hurt.wav")
        
        self.snd_list.append(new_sound)

        return new_sound
    
    def adjust_sound(self):
        for sound in self.snd_list:
            sound.set_volume(globalvars.PREFS.vol_sound)
        pygame.mixer.music.set_volume(globalvars.PREFS.vol_music)
