#STRUCTS
class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False
        self.assignment = 0
class struc_Prefs:
    def __init__(self):
        self.vol_sound = .5
        self.vol_music = .25
