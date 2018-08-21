#!/usr/bin/eni python
# encoding: utf-8


SIZE = 8
board = [[0] * SIZE for i in range(SIZE)]

kinght_moves = [
    (1, 2),
    (1, -2),
    (-1, 2),
    (-1, -2),
    (2, 1),
    (2, -1),
    (-2, 1),
    (-2, -1),
]


def i2xy(index):
    y = index // SIZE
    x = index % SIZE
    return x, y


def answer(src, dest):
    global board
    board = [[0] * SIZE for i in range(SIZE)]
    dest_x, dest_y = i2xy(dest)
    src_x, src_y = i2xy(src)
    if src_x == dest_x and src_y == dest_y:
        return 0

    return bfs(src_x, src_y, dest_x, dest_y)


def bfs(src_x, src_y, dest_x, dest_y):
    q = [(src_x, src_y, 0)]
    while q:
        x, y, step = q.pop()
        board[y][x] = step
        for dx, dy in kinght_moves:
            # Always heading to dest direction
            if (dest_x > x and dx < 0) or (dest_x < x and dx > 0):
                continue
            elif (dest_y > y and dy < 0) or (dest_y < y and dy > 0):
                continue

            _x, _y = x+dx, y+dy
            if dest_x == _x and dest_y == _y:
                return step+1

            if 0 <= x+dx < SIZE and 0 <= y+dy < SIZE:
                q.insert(0, (x+dx, y+dy, step+1))

    return r


if __name__ == '__main__':

    tests = [
        (
            (
                19,
                36
            ),
            1
        ),
        (
            (
                0,
                1
            ),
            3
        ),
        (
            (
                0,
                63
            ),
            6
        ),
        (
            (
                0,
                0
            ),
            0
        ),
        (
            (
                53,
                13
            ),
            3
        ),
        (
            (
                53,
                5
            ),
            4
        )
    ]
    for n in range(64):
        for x in range(64):
            tests.append(((n, x), None))
    f = answer
    for input_args, expected in tests:

        if isinstance(input_args, tuple):
            r = f(*input_args)
        else:
            r = f(input_args)

        for j in range(SIZE):
            print '>>>', board[j]

        print 'Result:{}\tInput:{}\tOutput:{}\tExpected:{}'.format(r == expected, input_args, r, expected)
