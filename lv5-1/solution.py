#!/usr/bin/eni python
# encoding: utf-8

from collections import Counter, defaultdict


def answer(w, h, s):
    '''
    The result is actually the number of orbits.

    Burnside's lemma & Polya enumeration theorem

    Ref:
        * https://en.wikipedia.org/wiki/Burnside%27s_lemma
            >
        * https://en.wikipedia.org/wiki/P%C3%B3lya_enumeration_theorem
            > Simplified, unweighted version
        * https://en.wikipedia.org/wiki/Group_action#Orbits_and_stabilizers
            > The orbits are the equivalence classes under a relation
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

    # Number of all possible permutation for given w*h grid
    G = factorial(w) * factorial(h)
    r = polynomial.val // G

    # Python2 converts int to long automatically
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


def get_num_of_cycle_factorization(partition):
    '''
## TO GET THE CYCLE COUNT:

# STEP 1) Select `cycle_len` elements out of `n` to form a cycle.

 a = C(n, cycle_len)

# STEP 2) Ways to form a cycle that length is `cycle_len`.

    For a cycle that length is `cycle_len`, You need to swap the 1st
    element with some one out of `cycle_len-1`, then swap that one with
    some other one excepted the swapped elements and so on.
    So that is permutation of `cyclen_len-1`.

 b = P(cycle_len-1, cycle_len-1) = !(cycle_len-1)

 a * b == !n / (!cycle_len * !(n - cycle_len) * !(cycle_len-1)
       == !n / cycle_len * !(n - cycle_len)
       == get_cycle_count(n, cycle_len)

 Here a * b is only for one cycle (we suppose there are m cycles)
 To calculate counts for all the cycles, it should be as below:

     c = Counter(partition)
     r = 1
     n = sum(partition)
     for cycle_len in partition:
         r *= get_cycle_count(n, cycle_len)
         n -= cycle_len  # update n so it is the num of elements left

 Turns out that it could be further simplified.
 Expand the loop as below:

   f = get_cycle_count
   r = f(n, k0) * f(n-k0, k1) * f(n-k0-k1, k2) ... * f(n-k0-...-k{m-1}, k{m})
     = [!(n) / (k0 *!(n-k0))] * [!(n-k0) / (k1*!(n-k0-k1)) * ... *
       [!(n-k0-...-k{m-1}) / (k{m}*!(n-k0-...-k{m-1}-k{m}))]

 As we know n = k0+k1+...+k{m}, m is the number of cycles.

   r = !(n) / (k0*k1*...*k{m}*!(0))
     = !n / ∏k{i}          (0 <= i <= m, k{i} is then cycle length of cycle i)

   r = !n / ∏(k{j}**v)     (for j, v in c.items)

# STEP 3) The order of cycles doesn't matter when cycle length are the same.

 Say c is counter of cycle partition.
 which means key is the cycle length (denoted as j), value is the
 number of cycles for that length (denoted as v)
 d = ∏!v       (for j, v in c.items)

## TO GET THE NUM OF FACTORIZATION

 It obviously that STEP 1) and STEP 2) could be merged into the for loop in
 STEP 3)

 r = !n / ∏((k{j}**v)*!v)  (for j, v in c.items)
    '''
    c = Counter(partition)
    n = sum(partition)
    r = factorial(n)
    for cycle_len, cycle_cnt in c.iteritems():
        r //= (cycle_len**cycle_cnt) * factorial(cycle_cnt)
    return r

def get_cycle_count(n, k):
    return factorial(n) // (k * factorial(n - k))


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
        return Operator.mul_cycle_index(self, other)

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
        coefficent = get_num_of_cycle_factorization(cycle_parition)
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
        return Operator.mul_polynomial_item(self, other)

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
        return Operator.mul_polynomial(self, other)

    @property
    def val(self):
        return sum(x.val for x in self.polynomial_items)

    def __repr__(self):
        return 'P({})'.format(self.polynomial_items)


class Operator(object):
    '''
    Cycle index of direct product of permutation groups, Section 2.
    * (2.7) & (2.8) is the definition could be used here directly.
    * Going through the whole section 2 is pretty helpful to understand why we
      calculate like this.
    * A|B means A divies B  (B % A == 0)
    * [a, b, c] means lcm(a, b, c)

    Ref: https://www.sciencedirect.com/science/article/pii/0012365X9390015L
    '''

    @staticmethod
    def mul_polynomial(a, b):
        ''' (2.7)
        '''
        def _g_mul():
            for a_item in a.polynomial_items:
                for b_item in b.polynomial_items:
                    yield a_item * b_item
        return Polynomial(_g_mul())

    @staticmethod
    def mul_polynomial_item(a, b):
        ''' (2.7)
        '''
        coefficent = a.coefficent * b.coefficent
        cycle_counts = defaultdict(int)
        base = a.cycle_indices[0].base
        for a_ci in a.cycle_indices:
            for b_ci in b.cycle_indices:
                ci = a_ci* b_ci
                cycle_counts[ci.cycle_len] += ci.cycle_count

        cycle_indices = [
            CycleIndex(base, cycle_len, cycle_count)
            for cycle_len, cycle_count in cycle_counts.iteritems()
        ]
        return PolynomialItem(coefficent, cycle_indices)

    @staticmethod
    def mul_cycle_index(a, b):
        ''' (2.8)
        '''
        cycle_len = lcm(a.cycle_len, b.cycle_len)
        cycle_count = (
            a.cycle_count
            * b.cycle_count
            * gcd(a.cycle_len, b.cycle_len)
        )
        return CycleIndex(
            a.base,
            cycle_len,
            cycle_count
        )


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
    test(get_num_of_cycle_factorization, [
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
