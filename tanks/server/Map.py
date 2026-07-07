class Map:
    def __init__(map,
                 fon_images,       # = list({'image': image, 'x_coord': x_coord, 'y_coord': y_coord, 'rotate': float}),
                 decorations_list, # = list({'image': image, 'x_coord': x_coord, 'y_coord': y_coord, 'rotate': float}),
                 walls_list       # = list({'image': image, 'x_coord': x_coord, 'y_coord': y_coord, 'rotate': int})
                 ):

        map.fon_images       = fon_images
        map.decorations_list = decorations_list
        map.walls_list       = walls_list



    def getData(map):
        return {
            'fon_images'      : map.fon_images,
            'decorations_list': map.decorations_list
            # 'walls_list'      : map.walls_list
        }