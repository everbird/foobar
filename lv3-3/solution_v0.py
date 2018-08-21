#!/usr/bin/eni python
# encoding: utf-8


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
    terminal_states = list(find_terminal_stats(m))
    possiability_map = get_possiability(m, terminal_states)

    rest_p = Fraction(1, 1) - sum(possiability_map.values())
    if rest_p == Fraction(1, 1):
        r = []
        for i, s in enumerate(terminal_states):
            r.append(1 if s == 0 else 0)
        return r

    sum_rest_p = Fraction(1, Fraction(1, 1) - rest_p)
    terminal_possibility_map = {
        s: p*sum_rest_p
        for s, p in possiability_map.iteritems()
    }

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


def get_possiability(m, terminal_states):
    size = len(m)
    cache = {}

    def dfs(start_state, p):
        row = m[start_state]
        s = sum(row)
        for i in range(start_state+1, size):
            w = row[i]
            if w > 0:
                _p = p * Fraction(w, s)
                if i in terminal_states:
                    cache[i] = _p
                else:
                    dfs(i, _p)

    dfs(0, Fraction(1, 1))
    return cache


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
            'TBD'
        ),
    ])
