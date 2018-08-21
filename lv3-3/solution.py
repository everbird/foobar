#!/usr/bin/eni python
# encoding: utf-8


import copy
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
    terminal_stats = OreTransitionMatrix.find_terminal_stats(m)
    M = OreTransitionMatrix(m)
    M.to_possibility()

    n = M.row_size
    eye = Matrix.eye(n)
    v = Matrix.fill(1, M.row_size)
    v[0][0] = 1

    # Neumann series
    # Ref:
    #   * https://en.wikipedia.org/wiki/Neumann_series
    #   * https://goo.gl/4yKc7h
    r = v * (eye - M).I

    possibilities = [r[0][s] for s in terminal_stats]
    possibilities.append(1)
    denominator = reduce(lcm,  [x.denominator for x in possibilities], 1)
    return [int(p * denominator) for p in possibilities]


class Matrix(object):

    def __init__(self, matrix_array, fraction_mode=True):
        self.col_size = len(matrix_array)
        self.row_size = len(matrix_array[0]) if matrix_array else 0
        self.fraction_mode = fraction_mode
        if fraction_mode:
            for j in xrange(self.col_size):
                for i in xrange(self.row_size):
                    matrix_array[j][i] = Fraction(matrix_array[j][i])
        self.matrix_array = matrix_array

    def __repr__(self):
        return (
            'Matrix({}, col_size={}, row_size={})'
            .format(self.matrix_array, self.col_size, self.row_size)
        )

    def __getitem__(self, key):
        return self.matrix_array[key]

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False

        if self.col_size != other.col_size or self.row_size != other.row_size:
            return False

        for j in xrange(self.col_size):
            for i in xrange(self.row_size):
                if self[j][i] != other[j][i]:
                    return False

        return True

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return MatrixOps.mul(self, other)

        return MatrixOps.mul_number(self, other)

    def __imul__(self, other):
        if isinstance(other, self.__class__):
            return MatrixOps.mul(self, other, inplace=True)

        return MatrixOps.mul_number(self, other, inplace=True)

    def __add__(self, other):
        return MatrixOps.add(self, other)

    def __iadd__(self, other):
        return MatrixOps.add(self, other, inplace=True)

    def __sub__(self, other):
        return MatrixOps.sub(self, other)

    def __isub__(self, other):
        return MatrixOps.sub(self, other, inplace=True)

    @property
    def I(self):
        ''' numpy style name for inverse matrix
        '''
        return MatrixOps.invert(self)

    @classmethod
    def eye(cls, size):
        ''' numpy styple name for identity matrix
        '''
        return MatrixOps.identity(size)

    def get_row(self, col_index):
        return self.matrix_array[col_index]

    def get_col(self, row_index):
        for j in xrange(self.col_size):
            yield self.matrix_array[j][row_index]

    @classmethod
    def fill(cls, col_size, row_size, default_value=0):
        return cls([[default_value] * row_size for i in xrange(col_size)])


class OreTransitionMatrix(Matrix):

    @property
    def size(self):
        assert self.row_size == self.col_size, 'Invalid ore transition matrix'

        return self.row_size

    def to_possibility(self):
        for j in xrange(self.size):
            denominator = sum(self[j]) or None  # Avoid ZeroDivisionError
            for i in xrange(self.size):
                self[j][i] = Fraction(self[j][i], denominator)

    @staticmethod
    def find_terminal_stats(m):
        return [s for s, row in enumerate(m) if not any(row)]


class MatrixOps(object):

    @staticmethod
    def identity(size):
        r = Matrix.fill(size, size)
        for i in xrange(size):
            r[i][i] = 1
        return r

    @staticmethod
    def add(a, b, inplace=False):
        assert \
            a.col_size == b.col_size and a.row_size == b.row_size, \
            'Invalid size for addition'

        r = a if inplace else Matrix.fill(a.col_size, a.row_size)
        for j in xrange(a.col_size):
            for i in xrange(a.row_size):
                r[j][i] = a[j][i] + b[j][i]

        return r

    @staticmethod
    def sub(a, b, inplace=False):
        r = MatrixOps.mul_number(b, -1, inplace=inplace)
        return MatrixOps.add(a, r, inplace=inplace)

    @staticmethod
    def mul_number(a, num, inplace=False):
        r = a if inplace else copy.deepcopy(a)
        for j in xrange(r.col_size):
            MatrixRowOps.mul(r, j, num)
        return r

    @staticmethod
    def mul(a, b):
        '''
            Ref: https://en.wikipedia.org/wiki/Matrix_multiplication#Definition
        '''
        assert a.row_size == b.col_size, 'Invalid size for multiplication'

        r = Matrix.fill(a.col_size, b.row_size)
        for j in xrange(a.col_size):
            for i in xrange(b.row_size):
                row_a = a.get_row(j)
                col_b = list(b.get_col(i))
                r[j][i] = sum(
                    row_a[k]*col_b[k]
                    for k in xrange(a.row_size)
                )
        return r

    @staticmethod
    def invert(m):
        ''' Gauss-Jordan method
        Ref:
            * https://goo.gl/HzeGfR  # Wikipedia
            * https://goo.gl/GGd3Gv  # A good example
        '''
        assert m.row_size == m.col_size, 'Invalid matrix size to invert'

        n = m.row_size
        r = Matrix.fill(n, n*2, default_value=Fraction(0))

        # STEP 1. concat
        eye = Matrix.eye(n)
        for j in xrange(n):
            for i in xrange(n):
                r[j][i] = m[j][i]
                r[j][i+n] = eye[j][i]

        # STEP 2. normalize
        for j in range(m.col_size):
            if r[j][j] == 0:  # why?
                for i in range(j+1, n):
                    if r[i][i] != 0:
                        MatrixRowOps.switch(r, i, j)
                    break

            assert r[j][j] != 0, 'Matrix is not invertable'
            v = r[j][j]

            MatrixRowOps.mul(r, j, 1 / v)

            for k in range(n):
                if k == j:  # 1 already
                    continue

                _v = r[k][j]
                if _v != 0:
                    MatrixRowOps.add(r, k, j, k=-_v)

        # STEP 3. cut
        _r = Matrix.fill(n, n)
        for j in xrange(n):
            for i in xrange(n):
                _r[j][i] = r[j][i+n]
        return _r


class MatrixRowOps(object):
    ''' Elementary Matrix Operations

    Ref: https://en.wikipedia.org/wiki/Elementary_matrix
    '''

    @staticmethod
    def mul(m, col_index, value):
        assert value != 0, '0 is invalid for elementry row multiplication'

        for i in xrange(m.row_size):
            m[col_index][i] *= value

    @staticmethod
    def switch(m, this_index, that_index):
        m[this_index], m[that_index] = m[that_index], m[this_index]

    @staticmethod
    def add(m, this_index, that_index, k=1):
        for i in xrange(m.row_size):
            m[this_index][i] = m[this_index][i] + (m[that_index][i] * k)


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
    test(MatrixOps.sub, [
        (
            (
                Matrix([
                    [1, 0, 1],
                    [1, 2, 1],
                    [2, 1, 1],
                ]),
                Matrix([
                    [2, 1, -1],
                    [0, -1, 2],
                    [2, -1, 0],
                ])
            ),
            Matrix([
                [-1, -1, 2],
                [1, 3, -1],
                [0, 2, 1],
            ])
        )
    ])
    test(MatrixOps.mul, [
        (
            (
                Matrix([
                    [1, 0, 1],
                    [1, 2, 1],
                    [2, 1, 1],
                ]),
                Matrix([
                    [2, 1, -1],
                    [0, -1, 2],
                    [2, -1, 0],
                ])
            ),
            Matrix([
                [4, 0, -1],
                [4, -2, 3],
                [6, 0, 0],
            ])
        ),
        (
            (
                Matrix([
                    [5, 7, 2],
                    [4, 3, 1],
                ]),
                Matrix([
                    [1],
                    [5],
                    [6],
                ])
            ),
            Matrix([
                [52],
                [25],
            ])
        ),
    ])
    test(MatrixOps.invert, [
        (
            Matrix([
                [5, 7],
                [3, 2]
            ]),
            Matrix([
                [Fraction(-2, 11), Fraction(7, 11)],
                [Fraction(3, 11), Fraction(-5, 11)]
            ]),
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
            [0, 3, 2, 9, 14]
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
