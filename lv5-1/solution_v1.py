#!/usr/bin/eni python
# encoding: utf-8

from collections import Counter, defaultdict


def answer(w, h, s):
    '''
    Polya enumeration theorem
    Ref:
        * https://en.wikipedia.org/wiki/P%C3%B3lya_enumeration_theorem
            > Simplified, unweighted version
    '''
    polynomial_w = Polynomial.get_from_cycle_partitions(
        get_cycle_partitions(w),
        s
    )
    polynomial_h = Polynomial.get_from_cycle_partitions(
        get_cycle_partitions(h),
        s
    )
    polynomial = polynomial_w * polynomial_h
    G = factorial(w) * factorial(h)
    r = polynomial.val // G
    return str(r)


def gcd(a, b):
    if a < b:
        return gcd(b, a)

    if not b:
        return a
    return gcd(b, a % b)


def lcm(a, b):
    return a * b // gcd(a, b)


cache = {}
def memorize(func):
    def deco(*args, **kwargs):
        if args in cache:
            return cache[args]

        r = func(*args, **kwargs)
        cache[args] = r
        return r
    return deco


@memorize
def factorial(n):
    if n in (0, 1):
        return 1

    return n * factorial(n - 1)


def permutation(n, k):
    return factorial(n) // factorial(n - k)
P = permutation


def combination(n, k):
    return P(n, k) // factorial(k)
C = combination


def get_cycle_partitions(length, lower_bound=1):
    r = []

    # Partition is in asc order, when `length` of elements form into more than
    # one cycles, upper bound of the length of the first cycle is at most
    # `length//2`
    for cycle_len in xrange(lower_bound, length//2+1):
        for p in get_cycle_partitions(length-cycle_len, lower_bound=cycle_len):
            r.append([cycle_len] + p)

    # All the items are in only one cycle
    return r + [[length]]


def num_of_factorization_for_cycle_partition(partition):
    c = Counter(partition)
    r = 1
    n = sum(partition)
    for cycle_len in partition:
        # STEP 1) Select `cycle_len` elements out of `n` to form a cycle.
        a = C(n, cycle_len)

        # STEP 2) Ways to form a cycle that length is `cycle_len`.
        b = num_of_factorization_for_cycle(cycle_len)

        r *= a * b
        n -= cycle_len

    # STEP 3) The order of cycles doesn't matter when cycle length are the same.
    for cycle_len, cycle_cnt in c.iteritems():
        r //= factorial(cycle_cnt)

    return r

# For a cycle that length is `cycle_len`, You need to swap the 1st
# element with some one out of `cycle_len-1`, then swap that one with
# some other one excepted the swapped elements and so on.
# So that is permutation of `cyclen_len-1`.
def num_of_factorization_for_cycle(n):
    return P(n-1, n-1)


class CycleIndex(object):
    '''
    * Ref: https://www.whitman.edu/Documents/Academics/Mathematics/Huisinga.pdf
        > 3.1 - Definition 6
    '''
    def __init__(self, base, cycle_len, cycle_count):
        self.base = base
        self.cycle_len = cycle_len
        self.cycle_count = cycle_count

    @property
    def val(self):
        return self.base ** self.cycle_count

    def __mul__(self, other):
        '''
        Cycle index of direct product of permutation groups (2.8)
        '''
        cycle_len = lcm(self.cycle_len, other.cycle_len)
        cycle_count = (
            self.cycle_count
            * other.cycle_count
            * gcd(self.cycle_len, other.cycle_len)
        )
        return CycleIndex(
            self.base,
            cycle_len,
            cycle_count
        )

    def __repr__(self):
        return 'C({}, {}, {})'.format(
            self.base, self.cycle_len, self.cycle_count
        )


class PolynomialItem(object):

    def __init__(self, coefficent, cycle_indices):
        self.coefficent = coefficent
        self.cycle_indices = cycle_indices

    @classmethod
    def get_from_cycle_partition(cls, cycle_parition, base):
        coefficent = num_of_factorization_for_cycle_partition(cycle_parition)
        c = Counter(cycle_parition)
        max_cycle_len = sum(cycle_parition)
        return cls(
            coefficent,
            [
                CycleIndex(base, cycle_len, c.get(cycle_len, 0))
                for cycle_len in xrange(1, max_cycle_len+1)
            ]
        )

    def __mul__(self, other):
        '''
        Cycle index of direct product of permutation groups (2.7)
        '''
        coefficent = self.coefficent * other.coefficent
        cycle_counts = defaultdict(int)
        base = self.cycle_indices[0].base
        for cycle_index in self.cycle_indices:
            for other_cycle_index in other.cycle_indices:
                r = cycle_index * other_cycle_index
                cycle_counts[r.cycle_len] += r.cycle_count

        cycle_indices = [
            CycleIndex(base, cycle_len, cycle_count)
            for cycle_len, cycle_count in cycle_counts.iteritems()
        ]
        return PolynomialItem(coefficent, cycle_indices)

    @property
    def val(self):
        r = 1
        for cycle_index in self.cycle_indices:
            r *= cycle_index.val
        return self.coefficent * r

    def __repr__(self):
        return 'PI({}, {})'.format(
            self.coefficent,
            self.cycle_indices
        )


class Polynomial(object):

    def __init__(self, polynomial_items):
        self.polynomial_items = polynomial_items

    @classmethod
    def get_from_cycle_partitions(cls, cycle_paritions, base):
        return cls([
            PolynomialItem.get_from_cycle_partition(p, base)
            for p in cycle_paritions
        ])

    def __mul__(self, other):
        '''
        Cycle index of direct product of permutation groups (2.7)

        Ref: https://www.sciencedirect.com/science/article/pii/0012365X9390015L
        '''
        polynomial_items = []
        for item in self.polynomial_items:
            for other_item in other.polynomial_items:
                polynomial_items.append(item * other_item)

        return Polynomial(polynomial_items)

    @property
    def val(self):
        return sum(x.val for x in self.polynomial_items)

    def __repr__(self):
        return 'P({})'.format(self.polynomial_items)


def test(f, testcases, result_func=None):
    for input_args, expected in testcases:
        if isinstance(input_args, tuple):
            r = f(*input_args)
        else:
            r = f(input_args)

        if result_func:
            r = result_func(r)

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
    test(factorial, [
        (
            1,
            1
        ),
        (
            4,
            24
        ),
        (
            10,
            3628800
        )
    ])
    test(get_cycle_partitions, [
        (
            4,
            [[1, 1, 1, 1], [1, 1, 2], [1, 3], [2, 2], [4]]
        ),
        (
            5,
            [[1, 1, 1, 1, 1], [1, 1, 1, 2], [1, 1, 3], [1, 2, 2], [1, 4], [2, 3], [5]]
        ),
        (
            1,
            [[1]]
        ),
    ])
    test(num_of_factorization_for_cycle_partition, [
        (
            [1, 1, 1, 1],
            1
        ),
        (
            [2, 3],
            20
        ),
        (
            [1, 2],
            3
        ),
        (
            [3],
            2
        ),
        (
            [2],
            1
        ),
        (
            [4],
            6
        ),
        (
            [1, 2, 3, 4],
            151200
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
            (2, 2, 2),
            "7"
        ),
        (
            (2, 3, 4),
            "430"
        ),
        (
            (1, 2, 2),
            "3"
        ),
        (
            (1, 1, 2),
            "2"
        ),
        (
            (1, 2, 3),
            "6"
        ),
        (
            (1, 2, 4),
            "10"
        ),
    ])
