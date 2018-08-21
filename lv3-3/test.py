import numpy as np
from fractions import Fraction

m1 = [
    [0, 2, 1, 0, 0],
    [0, 0, 0, 3, 4],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

m2 = [
    [0, 1, 0, 0, 0, 1],
    [4, 0, 0, 3, 2, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

m3 = [
    [0, 1, 0, 0, 0, 1],
    [4, 0, 3, 2, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

m4 = [
    [0, 1, 0, 0, 0, 1, 0],
    [0, 0, 2, 0, 3, 0, 0],
    [0, 0, 0, 1, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

m5 = [
    [0, 1, 0, 0, 0, 1, 0],
    [4, 0, 0, 3, 2, 0, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0]
]


def to_fractions(m, to_float=False):
    r = []
    for row in m:
        _row = []
        s = sum(row) or None
        for i in row:
            x = Fraction(i, s)
            if to_float:
                x = float(x)
            _row.append(x)
        r.append(_row)
    return r


def fraction_eye(size):
    r = [[Fraction(0, 1)] * size for i in range(size)]
    for i in range(size):
        r[i][i] = Fraction(1, 1)
    return r


def main():
    # m = to_fractions(m3, to_float=True)
    # size = len(m3)
    # m = to_fractions(m2, to_float=True)
    # size = len(m2)
    # m = to_fractions(m1, to_float=True)
    # size = len(m1)
    # m = to_fractions(m4, to_float=True)
    # size = len(m4)
    m = to_fractions(m5, to_float=True)
    size = len(m5)

    M = np.asmatrix(m)
    v_array = [0] * size
    v_array[0] = 1
    v = np.asmatrix(v_array)

    # i = fraction_eye(size)
    # I = np.asmatrix(i)
    I = np.eye(size)
    print 'I', I
    print 'M', M

    x = I-M
    print x

    x = x.I
    print x

    y = v * x
    print y





if __name__ == '__main__':
    main()
