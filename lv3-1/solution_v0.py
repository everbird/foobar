#!/usr/bin/eni python
# encoding: utf-8


def answer(n):
    if n == '0':
        return 1

    return _answer(long(n))


def _answer(n, step=0):
    if n == 1:
        return step

    if n % 2 == 0:
        return _answer(n >> 1, step+1)

    if (n//2) % 2 == 1:
        return _answer(n+1, step+1)

    return _answer(n-1, step+1)


def test(f, tests):
    for input_args, expected in tests:
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


if __name__ == '__main__':
    import sys
    argv = sys.argv
    if len(argv) > 1:
        print 'test mode'
        test_all()
        sys.exit()

    test(answer, [
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
            '21123481763481637846871263487613827648716387426872136487612836487263846',
            310
        ),
        (
            '1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
            -1
        )
    ])
