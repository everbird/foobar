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
    end_x, end_y = len_x-1, len_y-1
    min_steps = {'_': float('inf')}

    map_from_pod = copy.deepcopy(maze)
    walk_from_pod(map_from_pod)

    def bfs(start_x, start_y):
        q = [(start_x, start_y, 1, False)]
        while q:
            x, y, step, removed = q.pop()
            maze[y][x] = 'X'  # Never go back
            for dx, dy in moves:
                _x, _y = x+dx, y+dy
                if _x == end_x and _y == end_y:
                    min_steps['_'] = min(
                        min_steps['_'],
                        step+1
                    )

                if 0 <= _x < len_x and 0 <= _y < len_y:
                    if removed:
                        if map_from_pod[_y][_x] < 0:
                            min_steps['_'] = min(
                                min_steps['_'],
                                step-map_from_pod[_y][_x]
                            )
                    elif maze[_y][_x] == 0:
                        q.insert(0, (_x, _y, step+1, removed))
                        maze[_y][_x] = 'N'  # Avoid duplicates
                    elif maze[_y][_x] == 1:
                        q.insert(0, (_x, _y, step+1, True))

    bfs(0, 0)
    return min_steps['_']


def walk_from_pod(maze):
    len_y = len(maze)
    len_x = len(maze[0])

    def bfs(start_x, start_y):
        q = [(start_x, start_y, 1)]
        while q:
            x, y, step = q.pop()
            maze[y][x] = -step  # Never go back
            for dx, dy in moves:
                _x, _y = x+dx, y+dy

                if 0 <= _x < len_x and 0 <= _y < len_y:
                    if maze[_y][_x] == 0:
                        q.insert(0, (_x, _y, step+1))
                        maze[_y][_x] = 'N'

    bfs(len_x-1, len_y-1)
    return maze


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
    x = [[0] * 20 for i in range(20)]
    for i in range(20):
        x[1][i] = 1
    x[1][5] = 0
    test(walk_from_pod, [
        (
            [[0] * 20 for i in range(20)],
            39
        ),
        (
            x,
            -1
        )
    ])


if __name__ == '__main__':
    import sys
    argv = sys.argv
    if len(argv) > 1:
        print 'unit test mode'
        unit_test()
        sys.exit()

    x = [[0] * 20 for i in range(20)]
    for i in range(20):
        x[1][i] = 1
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
            39
        ),
        (
            x,
            39
        )
    ])
