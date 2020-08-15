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

