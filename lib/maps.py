from lib import constants, maps, actor, globalvars, data, generator
import tcod as libtcodpy


#MAP FUNCTIONS
def map_create():
    new_map = [[ data.struc_Tile(True) for y in range(0,constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    room_list = []

    for i in range(constants.MAP_MAX_NUM_ROOMS):
        w = libtcodpy.random_get_int(0, constants.ROOM_MIN_WIDTH, constants.ROOM_MAX_WIDTH)
        h = libtcodpy.random_get_int(0, constants.ROOM_MIN_HEIGHT, constants.ROOM_MAX_HEIGHT)
        x = libtcodpy.random_get_int(0, 2, constants.MAP_WIDTH - w -2)
        y = libtcodpy.random_get_int(0, 2, constants.MAP_HEIGHT - h -2)
        
        new_room = maps.obj_Room((x,y), (w,h))
        failed = False

        for other_room in room_list:
            if new_room.intercept(other_room):
                failed = True
                break
        if not failed:
            maps.map_create_room(new_map, new_room)
            center = new_room.center

            if len(room_list) != 0:
                prev_center = room_list[-1].center
                maps.map_create_tunnels(center, prev_center, new_map)
            
            room_list.append(new_room)

    maps.assign_tiles(new_map)

    maps.map_make_fov(new_map)

    return (new_map, room_list)

def map_place_objects(room_list):
    cur_level = len(globalvars.GAME.maps_prev) + 1
    top_level = (cur_level == 1)
    final_level = (cur_level == constants.MAP_LEVELS)
    for room in room_list:
        first_room = (room == room_list[0])
        last_room = (room == room_list[-1])

        if first_room: globalvars.PLAYER.x, globalvars.PLAYER.y = room.center    
        
        if first_room and top_level:
            generator.gen_portal(room.center)

        if first_room and not top_level:
             generator.gen_stairs((globalvars.PLAYER.x, globalvars.PLAYER.y), downwards=False)

        if last_room:
            if final_level: 
                generator.gen_lamp(room.center)
            else:
                generator.gen_stairs(room.center)


        x = libtcodpy.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcodpy.random_get_int(0, room.y1+1, room.y2-1)

        generator.gen_enemy((x,y))

        x = libtcodpy.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcodpy.random_get_int(0, room.y1+1, room.y2-1)

        generator.gen_item((x,y))

def map_create_room(new_map, new_room):
    for x in range(new_room.x1, new_room.x2):
        for y in range(new_room.y1, new_room.y2):
            new_map[x][y].block_path = False

def map_create_tunnels(coords1, coords2, new_map):
    coin_flip = (libtcodpy.random_get_int(0,0,1) ==1)
    x1,y1 = coords1
    x2,y2 = coords2
    if coin_flip:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            new_map[x][y1].block_path = False
        for y in range(min(y1, y2), max(y1, y2) + 1):
            new_map[x2][y].block_path = False
    else:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            new_map[x1][y].block_path = False
        for x in range(min(x1, x2), max(x1, x2) + 1):
            new_map[x][y2].block_path = False

def map_check_for_creatures(x, y, exclude_object = None):
    target = None
    if exclude_object:
        #check object list for all creatures except excluded
        for object in globalvars.GAME.current_objects: 
            if (object is not exclude_object and 
                object.x == x and 
                object.y == y and 
                object.creature):

                target = object
                
            if target:
                return target
    
    else:
        #check object list for any creature at location
        for object in globalvars.GAME.current_objects: 
            if (object.x == x and 
                object.y == y and 
                object.creature):

                target = object
                
            if target:
                return target

def map_make_fov(incoming_map):
    global FOV_MAP

    globalvars.FOV_MAP = libtcodpy.map.Map(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            libtcodpy.map_set_properties(globalvars.FOV_MAP, x ,y,
                not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)

def map_calc_fov():
    global FOV_CALC

    if globalvars.FOV_CALC:
        globalvars.FOV_CALC = False
        libtcodpy.map_compute_fov(globalvars.FOV_MAP, globalvars.PLAYER.x, globalvars.PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS, constants.FOV_ALGO)


def checkForWall(tile_map, x, y):

    if (x < 0 or
        y < 0 or
        x >= constants.MAP_WIDTH or
        y >= constants.MAP_HEIGHT):
        return False

    else: return tile_map[x][y].block_path

def map_objects_at_coords(pos_x, pos_y):
    objects_options = [obj for obj in globalvars.GAME.current_objects if obj.x == pos_x and obj.y == pos_y]
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

def assign_tiles(tile_map):
    for x in range(len(tile_map)):
        for y in range(len(tile_map[0])):

            tile_is_wall = maps.checkForWall(tile_map, x, y)

            if tile_is_wall:
                tile_assignment = 0 

                if maps.checkForWall(tile_map, x, y-1): tile_assignment += 1
                if maps.checkForWall(tile_map, x+1, y): tile_assignment += 2
                if maps.checkForWall(tile_map, x, y+1): tile_assignment += 4
                if maps.checkForWall(tile_map, x-1, y): tile_assignment += 8

                tile_map[x][y].assignment = tile_assignment
 
class obj_Room:
    '''
    Rectangle that lives in on the map
    '''
    def __init__(self,coords,size):
        self.x1,self.y1 = coords
        self.w, self.h = size

        self.x2 = self.x1 +self.w
        self.y2 = self.y1 + self.h
        
    @property
    def center(self):
        center_x = (self.x1 + self.x2)//2
        center_y = (self.y1 + self.y2)//2
        return (center_x, center_y)

    def intercept(self,other):
        objects_intersect = (self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)
        return objects_intersect
