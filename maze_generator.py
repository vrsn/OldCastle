from random import shuffle


def make_maze(width, height):
    vis = [[0] * width + [1] for _ in range(height)] + [[1] * (width + 1)]
    ver = [[0] * width + [0] for _ in range(height)] + [[]]
    hor = [[0] * width for _ in range(height + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)

        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = 1
            if yy == y:
                ver[y][max(x, xx)] = 1

            walk(xx, yy)

    walk(0, 0)

    return hor, ver


if __name__ == '__main__':
    vertical, horizontal = make_maze(5,5)
    for vert, hori in zip(vertical, horizontal):
        print(hori)
        print(vert)
