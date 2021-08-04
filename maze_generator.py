from random import shuffle


def make_maze(width, height):
    # Keep track of visited cells
    visited = [[0] * width + [1] for _ in range(height)] + [[1] * (width + 1)]
    # Where in the vertical walls we need to have open path. 0 is solid wall, 1 is path.
    vertical_paths = [[0] * width + [0] for _ in range(height)] + [[]]
    # Where in the horizontal walls we need to have open path. 0 is solid wall, 1 is path.
    horizontal_paths = [[0] * width for _ in range(height + 1)]

    def walk(x, y):
        visited[y][x] = 1

        neighbour_cells = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(neighbour_cells)

        for (xx, yy) in neighbour_cells:
            if visited[yy][xx]:
                continue
            if xx == x:
                horizontal_paths[max(y, yy)][x] = 1
            if yy == y:
                vertical_paths[y][max(x, xx)] = 1

            # Recursive call
            walk(xx, yy)

    walk(0, 0)

    return horizontal_paths, vertical_paths
