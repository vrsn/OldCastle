import maze_generator


def create_wall_list(width, height, vertical_start, horizontal_start, wall_tile_size):

    horizontal_walls, vertical_walls = maze_generator.make_maze(width, height)

    coordinate_list = []
    vertical_offset = vertical_start

    for horisontal_line in horizontal_walls:
        horisontal_offset = horizontal_start
        for path in horisontal_line:
            if path:
                for abscissa in range(1, 3):
                    coordinate_list.append([horisontal_offset + wall_tile_size * abscissa, vertical_offset])
                coordinate_list.append([horisontal_offset + wall_tile_size * 5, vertical_offset])
            else:
                for abscissa in range(1, 6):
                    coordinate_list.append([horisontal_offset + wall_tile_size * abscissa, vertical_offset])

            horisontal_offset += wall_tile_size * 5

        coordinate_list.append([horisontal_offset + wall_tile_size, vertical_offset])
        vertical_offset -= wall_tile_size * 5

    vertical_offset = vertical_start
    for vertical_line in vertical_walls:
        horisontal_offset = horizontal_start + wall_tile_size
        for path in vertical_line:
            if path:
                coordinate_list.append([horisontal_offset, vertical_offset - wall_tile_size])
                coordinate_list.append([horisontal_offset, vertical_offset - wall_tile_size * 4])
            else:
                for ordinate in range(1, 5):
                    coordinate_list.append([horisontal_offset, vertical_offset - wall_tile_size * ordinate])
            horisontal_offset += wall_tile_size * 5
        vertical_offset -= wall_tile_size * 5

    return coordinate_list