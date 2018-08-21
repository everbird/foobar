#!/usr/bin/eni python
# encoding: utf-8


moves = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


def answer(maze):
    len_y = len(maze)
    len_x = len(maze[0])

    def bfs(start_x, start_y):
        end_x, end_y = len_x-1, len_y-1
        q = [(start_x, start_y, 1, False)]
        while q:
            x, y, step, removed = q.pop()
            maze[y][x] = -1  # Never go back
            for dx, dy in moves:
                _x, _y = x+dx, y+dy
                if _x == end_x and _y == end_y:
                    return step+1

                if 0 <= _x < len_x and 0 <= _y < len_y:
                    if maze[_y][_x] == 0:
                        q.insert(0, (_x, _y, step+1, removed))
                    elif maze[_y][_x] == 1 and not removed:
                        q.insert(0, (_x, _y, step+1, True))

    return bfs(0, 0)


def test(f, testcases):
    for input_args, expected in testcases:
        if isinstance(input_args, tuple):
            r = f(*input_args)
        else:
            r = f(input_args)

        print (
            'Result:{}\tInput:{}\tOutput:{}\tExpected:{}'
            .format(
                r == expected,
                input_args,
                r,
                expected
            )
        )


def unit_test():
    pass


if __name__ == '__main__':
    import sys
    argv = sys.argv
    if len(argv) > 1:
        print 'unit test mode'
        unit_test()
        sys.exit()

    test(answer, [
        (
            [
                [0, 1, 1, 0],
                [0, 0, 0, 1],
                [1, 1, 0, 0],
                [1, 1, 1, 0]
            ],
            7
        ),
        (
            [
                [0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0]
            ],
            11
        ),
        (
            [[0] * 20 for i in range(20)],
            -1
        )
    ])
