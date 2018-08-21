#!/usr/bin/eni python
# encoding: utf-8


from itertools import permutations


def answer(times, time_limit):
    size = len(times)
    bunnies = size - 2

    # We could gain as much time as we need to escape if there is negative cycle
    if has_negative_cycle(times):
        return range(bunnies)

    bunny_indexes = range(1, bunnies+1)
    start = 0
    bulkhead = size - 1

    find_shortest_paths_inplace(times)

    def does_plan_work(plan):
        t = time_limit
        _plan = (start,) + plan + (bulkhead,)
        for u, v in zip(_plan[:-1], _plan[1:]):
            t -= times[u][v]
        return t >= 0

    # Instead of searching graph, we just simply verify each plan, since there are
    # only 5 bunnies at most. p5+p4+p3+p2+p1 = 120+120+60+20+5 = 325 which is
    # still a small number in the worst case.
    for cnt in xrange(bunnies, 0, -1):
        plans = permutations(bunny_indexes, cnt)
        for plan in plans:
            if does_plan_work(plan):
                # Result should be sorted by ID, not bunny pick-up order
                # (or Test 10 would fail)
                return sorted([x-1 for x in plan])

    # Oops ... no way to escape
    return []


def has_negative_cycle(times):
    ''' Bellman-Ford
    Ref: https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm
    '''
    # STEP 1. init
    size = len(times)
    distances = [float('inf')] * size
    distances[0] = 0

    # STEP 2. relax each edge, repeat V-1 times
    for k in xrange(size-1):
        for u in xrange(size):
            for v in xrange(size):
                if u == v:
                    continue

                w = times[u][v]
                distances[v] = min(distances[v], distances[u]+w)

    # STEP 3. check negative cycle
    for u in xrange(size):
        for v in xrange(size):
            if u == v:
                continue

            w = times[u][v]
            if distances[v] > w + distances[u]:
                return True

    return False


def find_shortest_paths_inplace(times):
    ''' Floyd-Warshall, inplace
    Ref: https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
    '''
    size = len(times)
    for k in xrange(size):
        for j in xrange(size):
            for i in xrange(size):
                times[j][i] = min(times[j][i], times[j][k]+times[k][i])
    return times


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
    test(has_negative_cycle, [
        (
            [[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]],
            False
        ),
        (
            [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]],
            False
        ),
        (
            [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -3], [9, 3, 2, 2, 0]],
            True
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
            (
                [[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]],
                3
            ),
            [0, 1]
        ),
        (
            (
                [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]],
                1
            ),
            [1, 2]
        ),
        (
            (
                [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -2], [9, 3, 2, 2, 0]],
                1
            ),
            [0, 2]
        ),
        (
            (
                [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -2], [9, 3, 2, 2, 0]],
                2
            ),
            [0, 1, 2]
        ),
        (
            (
                [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -3], [9, 3, 2, 2, 0]],
                1
            ),
            [0, 1, 2]
        ),
        (
            (
                [[0, 1, 10, 10, 10, 10], [10, 0, -3, 10, 10, 2], [10, 10, 0, 1, 10, 10], [10, 10, 10, 0, 1, 10], [10, 1, 10, 10, 0, 10], [10, 10, 10, 10, 10, 0]],
                3
            ),
            [0, 1, 2, 3]
        ),
        (
            (
                [[0, 1, 10, 10, 10, 10], [10, 0, -2, 10, 10, 2], [10, 10, 0, 1, 10, 10], [10, 10, 10, 0, 1, 10], [10, 1, 10, 10, 0, 10], [10, 10, 10, 10, 10, 0]],
                3
            ),
            [0]
        ),
        (
            (
                [[0, 1, 10, 10, 10, 10], [10, 0, -2, 10, 10, 2], [10, 10, 0, 1, 10, 10], [10, 10, 10, 0, 1, 10], [10, 1, 10, 10, 0, 10], [10, 10, 10, 10, 10, 0]],
                2
            ),
            []
        ),
        (
            (
                [[0, 1, 10, 10, 10, 10], [10, 0, -4, 10, 10, 2], [10, 10, 0, 1, 10, 10], [10, 10, 10, 0, 1, 10], [1, 10, 10, 10, 0, 10], [10, 10, 10, 10, 10, 0]],
                10
            ),
            [0, 1, 2, 3]
        ),
        (
            (
                [[0, 1, 1, 1, 1, 1], [1, 0, 1, 1, 1, 1], [1, 1, 0, 1, 1, 1], [1, 1, 1, 0, 1, 1], [1, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 0]],
                4
            ),
            [0, 1, 2]
        ),
    ])
