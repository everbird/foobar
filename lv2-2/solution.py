#!/usr/bin/eni python
# encoding: utf-8


import bisect


def answer(h, q):
    pivots = [2**i-1 for i in range(1, h+1)]
    r = []
    for n in q:
        if n == (2**h-1):
            p = -1
        else:
            p = find_parent(pivots, n)
        r.append(p)

    return r


def find_parent(pivots, n):
    index = bisect.bisect(pivots, n) - 1
    assert index >= 0  # Label starts from 1

    pivot = pivots[index]
    if n == pivot:
        return pivots[index+1]

    _n = n - pivot
    r = find_parent(pivots, _n)
    return r + pivot if _n < pivot else r


if __name__ == '__main__':

    tests = [
        (
            (
                3,
                [1, 2]
            ),
            [3, 3]
        ),
        (
            (
                3,
                [1, 4, 7]
            ),
            [3, 6, -1]
        ),
        (
            (
                3,
                [7, 3, 5, 1]
            ),
            [-1, 7, 6, 3]
        ),
        (
            (
                5,
                [19, 14, 28]
            ),
            [21, 15, 29]
        ),
        (
            (
                30,
                []
            ),
            []
        ),

    ]
    f = answer
    for input_args, expected in tests:

        if isinstance(input_args, tuple):
            r = f(*input_args)
        else:
            r = f(input_args)

        print 'Result:{}\tInput:{}\tOutput:{}\tExpected:{}'.format(r == expected, input_args, r, expected)
