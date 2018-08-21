#!/usr/bin/eni python
# encoding: utf-8


import copy

from collections import defaultdict


def answer(banana_list):
    size = len(banana_list)
    pair_candidates = defaultdict(list)
    banana_list.sort()
    adj = [[False] * size for i in xrange(size)]

    for j in xrange(size):
        for i in xrange(j+1, size):
            b = banana_list[j]
            a = banana_list[i]
            if is_wrestling_infinite(a, b):
                pair_candidates[b].append(a)
                adj[j][i] = True
                adj[i][j] = True

    # print '>>>', pair_candidates
    # print '>>>', adj
    matching_cnt = find_maximum_matching_cnt(adj)
    r = size - matching_cnt*2
    return r


def find_maximum_matching_cnt(g):
    match_map = {}
    cnt = 0
    size = len(g)

    def find_augmenting_path(root):
        alternating_paths = defaultdict(list)
        state = {}
        q = [root]

        def label_one_side(u, v, bi):
            path = alternating_paths[u]
            for i in xrange(bi+1, len(path)):
                w = path[i]
                if state[w] == 1:
                    # go around from v to become an even node
                    alternating_paths[w] = copy.deepcopy(alternating_paths[v])
                    alternating_paths[w].extend(path[i:][::-1])
                    state[w] = 0
                    q.insert(0, w)

        while q:
            u = q.pop()
            for v in xrange(size):
                if g[u][v] and match_map.get(v) != v:
                    if v not in state:
                        if v not in match_map:
                            # augmenting path
                            for i in xrange(0, len(alternating_paths[u]), 2):
                                match_map[alternating_paths[u][i]] = alternating_paths[u][i+1]
                                match_map[alternating_paths[u][i+1]] = alternating_paths[u][i]
                            match_map[u] = v
                            match_map[v] = u
                            return True
                        else:
                            # alternating path
                            w = match_map[v]
                            # u is even already
                            alternating_paths[w] = copy.deepcopy(alternating_paths[u])
                            alternating_paths[w].append(v)
                            alternating_paths[w].append(w)
                            # ?
                            state[v] = 1
                            state[w] = 0
                            q.insert(0, w)
                    else:
                        if state.get(v) == 0:  # u is start point of augmenting path, which is even node already
                            bi = 0
                            while (
                                bi < len(alternating_paths[u])
                                and bi < len(alternating_paths[v])
                                and alternating_paths[u][bi] == alternating_paths[v][bi]
                            ):
                                bi += 1
                            bi -= 1
                            label_one_side(u, v, bi)
                            label_one_side(v, u, bi)
        return False

    for i in xrange(size):
        if i not in match_map:
            if find_augmenting_path(i):
                cnt += 1
            else:
                match_map[i] = i

    return cnt


def gcd(a, b):
    if b > a:
        return gcd(b, a)

    if not b:
        return a
    return gcd(b, a % b)


def normalize(a, b):
    _gcd = gcd(a, b)
    _a = a // _gcd
    _b = b // _gcd
    return _a, _b


def is_wrestling_infinite(a, b):
    ''' TODO: some math to speedup?
    '''
    if a < b:
        return is_wrestling_infinite(b, a)
    elif a == b:
        return False

    c = (a + b) / gcd(a, b)
    return bool((c - 1) & c)


cache = {}

def is_wrestling_infinite_x(a, b):
    ''' TODO: some math to speedup?
    '''
    if a < b:
        return is_wrestling_infinite(b, a)
    elif a == b:
        return False

    _a, _b = normalize(a, b)

    if (_a + _b) % 2:
        return True

    visited = set([])
    while _a != _b and (_a, _b) not in cache and (_a, _b) not in visited:
        visited.add((_a, _b))
        _a, _b = _a - _b, _b * 2
        _a, _b = normalize(_a, _b)
        if _a < _b:
            _a, _b = _b, _a

    if _a == _b:
        r = False
    else:
        r = cache.get((_a, _b), True)
    # print '>>>', visited, cache, _a, _b, cache.get((_a, _b)), r
    for t in visited:
        cache[t] = r
    return r


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
    test(is_wrestling_infinite, [
        (
            (9, 1),
            True
        ),
        (
            (8, 1),
            True
        ),
        (
            (7, 1),
            False
        ),
        (
            (6, 1),
            True
        ),
        (
            (5, 1),
            True
        ),
        (
            (4, 1),
            True
        ),
        (
            (3, 1),
            False
        ),
        (
            (2, 1),
            True
        ),
        (
            (1, 1),
            False
        ),
        (
            (21, 7),
            False
        ),
        (
            (3, 7),
            True
        ),
        (
            (1073741823, 7),
            True
        ),
        (
            (5, 3),
            False
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
            [1, 1],
            2
        ),
        (
            [1, 7, 3, 21, 13, 19],
            0
        ),
    ])
