#!/usr/bin/eni python
# encoding: utf-8


import copy

from collections import defaultdict


def answer(banana_list):
    size = len(banana_list)
    banana_list.sort()
    g = [[False] * size for i in xrange(size)]

    # STEP 1: Create wrestling graph
    for j in xrange(size):
        for i in xrange(j+1, size):
            b = banana_list[j]
            a = banana_list[i]
            if is_wrestling_infinite(a, b):
                g[j][i] = True
                g[i][j] = True

    # STEP 2: Maximum matching for general graph
    matching_cnt = find_maximum_matching_cnt(g)
    r = size - matching_cnt*2
    return r


def find_maximum_matching_cnt(g):
    '''
    Blossom Algorithm

    Ref:
        * https://en.wikipedia.org/wiki/Matching_(graph_theory)
        * https://en.wikipedia.org/wiki/Berge%27s_lemma
        * https://en.wikipedia.org/wiki/Blossom_algorithm
        * https://www.cs.dartmouth.edu/~ac/Teach/CS105-Winter05/Handouts/tarjan-blossom.pdf
            > proof of correctness:
            >   Blossom-shrinking preserves the existence or non-existence of an
            >   augmenting path.
        * http://www.csie.ntnu.edu.tw/~u91029/Matching.html#5
            > well explained blossom algorithm and stuffs around
        * https://stanford.edu/~rezab/classes/cme323/S16/projects_reports/shoemaker_vare.pdf
            > good paper about the blossom algorithm and further optimization.
        * https://github.com/networkx/networkx
            > python package that could be used in real world for such issue.
    '''
    match_map = {}
    cnt = 0
    size = len(g)

    def find_augmenting_path(root):
        alternating_paths = defaultdict(list)
        alternating_paths[root].append(root)
        state = {}
        state[root] = 0
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
                            # Found augmenting path, do the augmentation:
                            #   Toggle the edges of augmenting path, cardinality
                            #   is increased by 1
                            for i in xrange(0, len(alternating_paths[u])-1, 2):
                                match_map[alternating_paths[u][i]] = alternating_paths[u][i+1]
                                match_map[alternating_paths[u][i+1]] = alternating_paths[u][i]
                            match_map[u] = v
                            match_map[v] = u
                            return True
                        else:
                            # Expand alternating path
                            w = match_map[v]
                            # u is even already
                            alternating_paths[w] = copy.deepcopy(alternating_paths[u])
                            alternating_paths[w].append(v)
                            alternating_paths[w].append(w)
                            state[v] = 1
                            state[w] = 0
                            q.insert(0, w)
                    else:
                        if state.get(v) == 0:
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


def is_wrestling_infinite(a, b):
    ''' Here is the thought for proof:
        (DEF-1) [a, b] => (a (mod n), b (mod n)), n = a + b

            f(x, y) = {
                case 1 when x=y) [n/2, n/2]
                case 2 when y>x) [2x, y-x]
                case 3 when x<x) [x-y, 2y]
            }

        case 1 is the termial state when wrestling is not infinite, in that case
        f(x, y)**t = (n/2, n/2)

        As we know:
            * n = x + y => y = n - x
            * DEF-1 => a = a * An, b = b * Bn, A, B could be any integer
        case 2) [2x, y-x] => [2x, n-2x] => [2x, -2x] => [2x, 2y]
        case 3) [x-y, 2y] => [2x-n, 2n-2x] => [2x-n, n-(2x-n)] => [2x, -2x]
                          => [2x, 2y]

        So that f(x, y) could be simplified as:
            f(x, y) = {
                case 1 when x=y) [n/2, n/2]
                case 2 else) [2x, 2y]
            }

        When wrestling is infinate, there is no "case 1" in f(x, y), so that:
            f(x, y) = [2x, 2y] when wrestling is infinite

        For any t
        => f(x, y)**t = [(2**t)x, (2**t)y]
        => x[t] = (2**t)x[0] (mod n) != n/2
        => (2**(t+1))x[0] (mod n) != n
        => (2**t)x[0] (mod n) != 0

        (DEF-2) Say for any integer s, m = (2**s)n, for any t
        (2**t)x[0] (mod n) != 0
        => (2**(t-s))x[0] (mod m) != 0
        => (2**t)x[0] (mod m) != 0
        => As we know (2**t) mod m != 0 from DEF-2, so that x[0] (mod m) != 0

        So we only need to ensure a mod m != 0 to make wrestling infinite.

        Ref: https://yifan.lu/2017/09/13/foobar-blossoms-and-isomorphism/

    '''
    n = a + b
    while n % 2 == 0:
        n /= 2
    return (a % n) != 0


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
        (
            [1, 2, 1, 7, 3, 21, 13, 19],
            0
        ),
        (
            [100],
            1
        ),
    ])
