#!/usr/bin/eni python
# encoding: utf-8


from collections import defaultdict
from itertools import chain


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
    graph = Graph(g)
    matching = graph.find_maximum_matching()
    return size - len(matching)


class Graph(object):
    def __init__(self, g):
        self.g = g
        self.size = len(g)

    def find_maximum_matching(self):
        '''
        Go through each unmatched vertex, find any augmenting path and augment
        until there is no augmenting path.

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
        matching = GraphMatching({})
        # No augmenting vetices.
        # if u->v has no augmenting path, then v-> must has no augmenting path.
        # So that we could skip such vetices to speed up a little bit.
        visited = set([])

        for i in xrange(self.size):
            if i not in matching:
                if not self.find_augmenting_path(i, matching, visited):
                    visited.add(i)

        return matching


    def find_augmenting_path(self, root, matching, visited):
        '''
        Blossom Algorithm, label blossom instead of shrinking

        * BFS to find any other unmatched vertex.
        * Otherwise expand alternating tree from root via existing matching.
        * When there is blossom, label the odd vertices to even and update the
        alternating tree.
        * Whenever new an even vertex been found, BFS from there to continue
        the search.
        '''
        tree = GraphAlternatingTree(root)
        q = [root]  # only for even node, since only even node could be expanded

        while q:
            u = q.pop()
            for v in xrange(self.size):
                if not self.g[u][v] or v in visited or v == root:
                    continue

                # When v has parity and v not in matching, v must be root
                # So it could be a blossom as CASE 3
                # Except root, any v has parity, it must be matched already.
                if v not in matching and v != root:
                    # CASE 1)
                    # Found augmenting path, do the augmentation:
                    #   Toggle the edges of augmenting path, cardinality
                    #   is increased by 1
                    # Matching is only updated in this branch.
                    tree.augment(u, matching)
                    matching.match(u, v)
                    return True

                if v not in tree.parity:
                    # CASE 2)
                    # Expand alternating path via exising matching
                    # u is even already, because it's either root or
                    # node in q that already been marked as even.
                    # v must be matched here.
                    w = matching[v]
                    tree.expand_via_matched_edge(u, (v, w))
                    q.insert(0, w)
                elif tree.is_even(v):
                    # CASE 3)
                    # Found blossom, change odd node to even and BFS to expand
                    # Label each side of blossom to find new expandable vertices
                    for new_even_vertex in tree.label_blossom(u, v):
                        q.insert(0, new_even_vertex)
                elif tree.is_odd(v):
                    # CASE 4)
                    # It's a alternating path that already been expanded
                    # previously. Just skip.
                    pass
        return False


class GraphMatching(dict):

    def match(self, u, v):
        self[u] = v
        self[v] = u

    @property
    def is_valid(self):
        if not self:
            return True

        visited = set([])
        for k, v in self.iteritems():
            if k in visited:
                continue

            if self[v] != k:
                return False
            visited.add(k)
            visited.add(v)

        return True


class GraphAlternatingTree(object):
    PARITY_EVEN = 0
    PARITY_ODD = 1

    def __init__(self, root):
        self.d = defaultdict(list)
        self.d[root].append(root)
        self.parity = {root: self.PARITY_EVEN}

    def expand_via_matched_edge(self, u, matched_edge):
        matched_v, matched_w = matched_edge
        self[matched_w] = self[u] + [matched_v, matched_w]
        self.parity[matched_v] = self.PARITY_ODD
        self.parity[matched_w] = self.PARITY_EVEN

    def set_path(self, vertex, new_path):
        assert isinstance(new_path, list), "new_path must be a list"
        self.d[vertex] = new_path

    def get_path(self, dest):
        return self.d[dest]

    def __getitem__(self, k):
        return self.get_path(k)

    def __setitem__(self, k, v):
        self.set_path(k, v)

    def lca(self, u, v):
        bi = 0
        while (
            bi < len(self[u])
            and bi < len(self[v])
            and self[u][bi] == self[v][bi]
        ):
            bi += 1
        return bi - 1

    def is_even(self, vertex):
        return self.parity[vertex] == self.PARITY_EVEN

    def is_odd(self, vertex):
        return self.parity[vertex] == self.PARITY_ODD


    def label_blossom(self, u, v):
        bi = self.lca(u, v)
        return chain(
            self.label_blossom_one_side(u, v, bi),
            self.label_blossom_one_side(v, u, bi)
        )

    def label_blossom_one_side(self, u, v, bi):
        # (u, v) is cross edge, bi is base
        path2u = self[u]
        for i in xrange(bi+1, len(path2u)):
            w = path2u[i]
            if self.is_odd(w):
                # Extend alternating path, go across the cross edge from v
                # to reach to w, such as [root -> v --> u -> w]
                path_u2w = path2u[i:][::-1]
                self[w] = self[v] + path_u2w
                self.parity[w] = self.PARITY_EVEN
                yield w  # New even vetices which is expandable potentially

    def augment(self, u, matching):
        path2u = self[u]
        for i in xrange(0, len(path2u)-1, 2):
            matching.match(path2u[i], path2u[i+1])


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
        (
            (1, 4),
            True
        ),
        (
            (4, 5),
            True
        ),
        (
            (1, 5),
            True
        ),
    ])
    g = [
        [False, True, False],
        [False, False, True],
        [True, False, False],
    ]
    graph = Graph(g)
    test(graph.find_augmenting_path, [
        (
            (
                0,
                {1: 2, 2: 1},
                set([])
            ),
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
        (
            [1, 4, 5],
            1
        ),
    ])
