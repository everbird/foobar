#!/usr/bin/eni python
# encoding: utf-8


from time import sleep

import copy
from collections import defaultdict


def answer(times, time_limit):
    size = len(times)
    bunnies = size - 2
    bunny_indexes = range(1, bunnies+1)
    start = 0
    door = size - 1

    if has_negative_cycle(times):
        return range(bunnies)

    zero_cycles = find_zero_cycle(times)
    zero_cost_bunnies = set([])
    for i in zero_cycles.get(start, []):
        if i in bunny_indexes:
            zero_cost_bunnies.add(i)
    for i in zero_cycles.get(door, []):
        if i in bunny_indexes:
            zero_cost_bunnies.add(i)

    shorted_dis_to_door = find_shorted_from_door(times)
    print '>>>>', zero_cost_bunnies, zero_cycles
    save_plans = set([])
    # Time limit exceeded
    def bfs(start, time_limit):
        q = [(start, time_limit, set([]))]
        while q:
            # sleep(1)
            print 'q:', q
            n, time, visited = q.pop()
            if n in zero_cycles:
                visited |= set(zero_cycles[n])
            visited.add(n)
            cost_list = times[n]
            for i, cost in enumerate(cost_list):
                if i == n:
                    continue

                if i in zero_cycles.get(n, []):
                    print n, '->', i, zero_cycles[n], '!!'
                    continue

                print 'passed', n ,'->', i
                _visited = copy.deepcopy(visited)
                _time = time - cost

                if _time >= shorted_dis_to_door[i]:
                    if i == size-1:
                        print '>>>', n, '->', i, _time, _visited, save_plans
                        save_plans.add(tuple(sorted(list(_visited))))

                    # if i not in _visited:  # ?
                    print 'insert', i, _time, _visited
                    q.insert(0, (i, _time, _visited))

                    continue

                # print 'dropping:', n, '->', i, time, _time

    bfs(0, time_limit)

    # print '>>', save_plans
    _save_plans = []
    for p in save_plans:
        if 0 in p:
            p = p[1:]
        if (size-1) in p:
            p = p[:-1]
        _save_plans.append(p)

    # print '>>>', _save_plans
    max_bunnies = max(map(len, _save_plans))
    max_bunnies_plans = sorted([x for x in _save_plans if len(x) == max_bunnies])
    plan = max_bunnies_plans[0]
    return [x-1 for x in plan]


def find_shorted_from_door(times):
    ''' No negative cycle
    '''
    size = len(times)
    _times = [[0] * size for i in xrange(size)]
    for j in xrange(size):
        for i in xrange(size):
            x = size - 1 - i
            y = size - 1 - j
            _times[j][i] = times[x][y]

    print 'times:', times
    print '_times:', _times

    # STEP 1. init
    distances = [float('inf')] * size
    distances[0] = 0

    # STEP 2. relax each edge, repeat V-1 times
    for k in xrange(size-1):
        for u in xrange(size):
            for v in xrange(size):
                if u == v:
                    continue

                w = _times[u][v]
                distances[v] = min(distances[v], distances[u]+w)

    return distances[::-1]


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


def find_zero_cycle(times):
    ''' Bellman-Ford
    Ref: https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm
    '''
    edges = defaultdict(list)  # Adjacent list
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

    for u in xrange(size):
        for v in xrange(size):
            if u == v:
                continue

            w = times[u][v]
            if distances[v] == w + distances[u]:
                edges[u].append(v)

    # edges is an directed unweighted graph
    # print '>>>', edges
    def dfs(start):
        r = {}
        q = [(start, [start])]
        while q:
            s, path = q.pop()

            neighbors = edges[s]
            for n in neighbors:
                if n in path:
                    # print '>>>', s, '->', n, path, neighbors
                    # record
                    i = path.index(n)
                    r[n] = path[i:]
                    continue

                _path = path[:]
                q.append((n, _path+[n]))

        return r

    return dfs(0)


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
    test(find_zero_cycle, [
        (
            [[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]],
            {}
        ),
        (
            [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]],
            {}
        ),
        (
            [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -3], [9, 3, 2, 2, 0]],
            {}
        ),
        (
            [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -2], [9, 3, 2, 2, 0]],
            {4: [4, 3]}
        ),
        (
            [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, -1, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]],
            {4: [4, 2, 3]}
        ),
        (
            [[0, 1, 10, 10, 10, 10], [10, 0, -3, 10, 10, 10], [10, 10, 0, 1, 10, 10], [10, 10, 10, 0, 1, 10], [10, 1, 10, 10, 0, 10], [10, 10, 10, 10, 10, 0]],
            {1: [1, 2, 3, 4]}
        ),
    ])
    test(find_shorted_from_door, [
        (
            [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]],
            [-1, -1, -1, -1, 0]
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
    ])
