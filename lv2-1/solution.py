#!/usr/bin/eni python
# encoding: utf-8


SIZE = 8

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
    dest_x, dest_y = i2xy(dest)
    src_x, src_y = i2xy(src)
    if src_x == dest_x and src_y == dest_y:
        return 0

    return bfs(src_x, src_y, dest_x, dest_y)


def bfs(src_x, src_y, dest_x, dest_y):
    q = [(src_x, src_y, 0)]
    while q:
        x, y, step = q.pop()
        for dx, dy in kinght_moves:
            # Always heading to dest direction
            if (dest_x > x and dx < 0) or (dest_x < x and dx > 0):
                continue
            elif (dest_y > y and dy < 0) or (dest_y < y and dy > 0):
                continue

            _x, _y = x+dx, y+dy
            if dest_x == _x and dest_y == _y:
                return step+1

            if 0 <= _x < SIZE and 0 <= _y < SIZE:
                q.insert(0, (_x, _y, step+1))

    return -1


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
    f = answer
    for input_args, expected in tests:

        if isinstance(input_args, tuple):
            r = f(*input_args)
        else:
            r = f(input_args)

        print 'Result:{}\tInput:{}\tOutput:{}\tExpected:{}'.format(r == expected, input_args, r, expected)
