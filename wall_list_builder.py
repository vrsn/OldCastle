# Generate walls based on the given parameters and the maze.
def create_wall_list(vertical_start, horizontal_start, wall_tile_size, horizontal_walls, vertical_walls):
    coordinate_list = []
    vertical_offset = vertical_start

    # Create horizontal walls
    for horizontal_line in horizontal_walls:
        horizontal_offset = horizontal_start
        for path in horizontal_line:
            if path:
                for abscissa in range(1, 3):
                    coordinate_list.append([horizontal_offset + wall_tile_size * abscissa, vertical_offset])
                coordinate_list.append([horizontal_offset + wall_tile_size * 5, vertical_offset])
            else:
                for abscissa in range(1, 6):
                    coordinate_list.append([horizontal_offset + wall_tile_size * abscissa, vertical_offset])

            horizontal_offset += wall_tile_size * 5

        coordinate_list.append([horizontal_offset + wall_tile_size, vertical_offset])
        vertical_offset -= wall_tile_size * 5

    # Crete vertical walls
    vertical_offset = vertical_start
    for vertical_line in vertical_walls:
        horizontal_offset = horizontal_start + wall_tile_size
        for path in vertical_line:
            if path:
                coordinate_list.append([horizontal_offset, vertical_offset - wall_tile_size])
                coordinate_list.append([horizontal_offset, vertical_offset - wall_tile_size * 4])
            else:
                for ordinate in range(1, 5):
                    coordinate_list.append([horizontal_offset, vertical_offset - wall_tile_size * ordinate])
            horizontal_offset += wall_tile_size * 5
        vertical_offset -= wall_tile_size * 5

    return coordinate_list
