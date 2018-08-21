#!/usr/bin/eni python
# encoding: utf-8


def answer(n):
    if n == '0':
        return 1

    step = 0
    _n = long(n)
    while _n > 1:
        if _n % 2 == 0:
            _n >>= 1
        elif (_n // 2) % 2 == 1 and _n != 3:
            _n += 1
        else:
            _n -= 1

        step += 1

    return step


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
    r = []
    for i in range(1000):
        r.append(answer(str(i)))

    for i in range(1, 1000):
        if r[i] - r[i-1] not in (1, 0, -1):
            print '!!!', i, i-1, r[i], r[i-1]



if __name__ == '__main__':
    import sys
    argv = sys.argv
    if len(argv) > 1:
        print 'unit test mode'
        unit_test()
        sys.exit()

    test(answer, [
        (
            '3',
            2
        ),
        (
            '4',
            2
        ),
        (
            '15',
            5
        ),
        (
            '62',
            7
        ),
        (
            '0',
            1
        ),
        (
            '1',
            0
        ),
        (
            '21123481763481637846871263487613827648716387426872136487612836487263846',
            309
        ),
        (
            '1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
            1231
        )
    ])
