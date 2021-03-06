#!/usr/bin/eni python
# encoding: utf-8


import copy


moves = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


def answer(maze):
    len_y = len(maze)
    len_x = len(maze[0])

    min_steps = {
        '_': float('inf')
    }

    end_x, end_y = len_x-1, len_y-1

    def dfs(start_x, start_y):
        q = [(start_x, start_y, 1, False)]
        while q:
            x, y, step, removed = q.pop()
            maze[y][x] = -1  # Never go back
            for dx, dy in moves:
                _x, _y = x+dx, y+dy
                if _x == end_x and _y == end_y:
                    min_steps['_'] = min(min_steps['_'], step+1)
                    continue

                if 0 <= _x < len_x and 0 <= _y < len_y:
                    if maze[_y][_x] == 0:
                        q.append((_x, _y, step+1, removed))
                    elif maze[_y][_x] == 1 and not removed:
                        q.append((_x, _y, step+1, True))

    _maze = copy.deepcopy(maze)

    def dfs2(x, y, removed):
        maze[y][x] = -1  # Never go back
        min_steps = float('inf')
        for dx, dy in moves:
            _x, _y = x+dx, y+dy
            if _x == end_x and _y == end_y:
                return 1

            if 0 <= _x < len_x and 0 <= _y < len_y:
                if maze[_y][_x] == 0:
                    steps = dfs2(_x, _y, removed) + 1
                    min_steps = min(min_steps, steps)
                    maze[y][x] = _maze[y][x]  # Recover
                elif maze[_y][_x] == 1 and not removed:
                    steps = dfs2(_x, _y, True) + 1
                    min_steps = min(min_steps, steps)
                    maze[y][x] = _maze[y][x]  # Recover
        return min_steps

    dfs(0, 0)
    return min_steps['_']


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
