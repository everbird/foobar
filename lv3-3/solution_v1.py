#!/usr/bin/eni python
# encoding: utf-8


import copy
from collections import defaultdict
from fractions import Fraction


def gcd(a, b):
    if b > a:
        return gcd(b, a)

    if not b:
        return a
    return gcd(b, a % b)


def lcm(a, b):
    return a * b // gcd(a, b)


def answer(m):
    size = len(m)
    terminal_states = list(find_terminal_stats(m))
    if 0 in terminal_states:
        r = [0] * (size+1)
        r[0] = 1
        r[-1] = 1
        return r

    g_possibility = {}
    possibilty, loop_joint = get_possiability(0, m)
    for s in loop_joint.keys():
        if s == 0:
            g_possibility[0] = (possibilty, loop_joint)
        else:
            g_possibility[s] = get_possiability(s, m)

    access = {}
    for s in terminal_states:
        access[s] = get_accessible_states(m, s)

    access_terminals = defaultdict(list)
    for t_s, stats in access.iteritems():
        for s in stats:
            access_terminals[s].append(t_s)

    print '>>>', terminal_states, possibilty, loop_joint
    print '!!!', access
    print '***', access_terminals
    print 'ggg', g_possibility

    terminal_possibility_map = defaultdict(int)
    ## ?
    # for start_state, (p_map, l_joint) in g_possibility.iteritems():
    #     _p = l_joint[start_state]
    #     _sum_rest_p = Fraction(1, Fraction(1, 1) - _p)
    #     print '<><>', _sum_rest_p
    #     for accessible_terminal_state in access_terminals[s]:
    #         terminal_possibility_map[accessible_terminal_state] += (_sum_rest_p * p_map[accessible_terminal_state] * possibilty[start_state])

    terminal_possibility_map = {
        k: v for k, v in possibilty.iteritems() if k in terminal_states
    }
    for s, p in loop_joint.iteritems():
        _p = p / possibilty[s]
        _sum_rest_p = Fraction(1, Fraction(1, 1) - _p)
        print '<><>', _sum_rest_p
        for accessible_terminal_state in access_terminals[s]:
            terminal_possibility_map[accessible_terminal_state] *= _sum_rest_p  # ?

    ## ?

    denominators = [x.denominator for x in terminal_possibility_map.values()]
    denominator = reduce(lcm, denominators, 1)
    # print '>>', terminal_possibility_map, terminal_states, denominator, rest_p, sum_rest_p

    r = []
    for s in terminal_states:
        if s not in terminal_possibility_map:
            r.append(0)
            continue

        p = terminal_possibility_map[s]
        v = p * denominator
        r.append(v.numerator)

    r.append(denominator)
    return r


def get_possiability(start_state, m):
    '''
        "white-gray-black" DFS
    '''
    size = len(m)
    possibilty = {start_state: Fraction(1, 1)}
    color = defaultdict(int)
    loop_joint = defaultdict(int)

    def dfs(start_state, p):
        if color[start_state] != 0:
            loop_joint[start_state] += p  # ? += ?
            return

        color[start_state] = 1
        row = m[start_state]
        s = sum(row)
        for i in range(size):

            if color[i] == 2:
                continue

            w = row[i]
            if w > 0:
                _p = p * Fraction(w, s)
                if i not in possibilty:
                    possibilty[i] = _p
                dfs(i, _p)
        color[start_state] = 2

    dfs(start_state, Fraction(1, 1))
    return possibilty, loop_joint


def get_accessible_states(m, s):
    visited = set([])
    size = len(m)
    stack = [s]
    init_flag = True
    while stack:
        _s = stack.pop()
        if _s in visited:
            continue

        # Access self only if explicitly do so
        if init_flag:
            init_flag = False
        else:
            visited.add(_s)
        for i in range(size):
            if m[i][_s] > 0:
                stack.append(i)

    return visited


def find_terminal_stats(m):
    for i, row in enumerate(m):
        if not any(row):
            yield i


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
    test(gcd, [
        (
            (8, 12),
            4
        ),
        (
            (39, 26),
            13
        )
    ])
    test(lcm, [
        (
            (8, 12),
            24
        ),
        (
            (39, 26),
            78
        )
    ])
    test(get_possiability, [
        (
            (
                0,
                [
                    [0, 2, 1, 0, 0],
                    [0, 0, 0, 3, 4],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]
                ]
            ),
            None
        ),
        (
            (
                0,
                [
                    [0, 0, 1, 2, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 3, 0, 0, 4],
                    [0, 0, 0, 0, 0]
                ],
            ),
            None
        ),
    ])


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
                [0, 2, 1, 0, 0],
                [0, 0, 0, 3, 4],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ],
            [7, 6, 8, 21]
        ),
        (
            [
                [0, 0, 1, 2, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 3, 0, 0, 4],
                [0, 0, 0, 0, 0]
            ],
            [6, 7, 8, 21]
        ),
        (
            [
                [0, 1, 0, 0, 0, 1],
                [4, 0, 0, 3, 2, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]
            ],
            [0, 3, 2, 9, 14]
        ),
        (
            [
                [0, 1, 0, 0, 0, 1, 0],
                [4, 0, 0, 3, 2, 0, 1],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0]
            ],
            'TBD'
        ),
        (
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ],
            [1, 0, 0, 0, 0, 1]
        ),
        (  # A
            [
                [0, 1, 0, 0, 0, 1, 0],
                [0, 0, 2, 0, 3, 0, 0],
                [0, 0, 0, 1, 0, 0, 1],
                [0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]
            ],
            [3, 4, 1, 8]
        ),
    ])
