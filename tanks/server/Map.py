class Map:
    def __init__(map,
                 fon_images       = list(dict),
                 walls_list       = list(dict),
                 decorations_list = list(dict)
                 ):

        map.fon_images       = fon_images
        map.walls_list       = walls_list
        map.decorations_list = decorations_list



    def getData(map):
        return {
            'fon_images'      : map.fon_images,
            'walls_list'      : map.walls_list,
            'decorations_list': map.decorations_list
        }