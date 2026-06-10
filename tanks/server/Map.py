class Map:
    def __init__(map,
                 fon_image = '',
                 walls_list = list({
                     'coords': (x, y),
                     'image' : ''
                 }),
                 decorate_list = list({
                     'coords': (x, y),
                     'image' : ''
                 })
                 ):

        map.fon_image = fon_image
        map.walls_list = walls_list
        map.decorate_list = decorate_list