#!/usr/bin/eni python
# encoding: utf-8


def answer(s):
    if not s:
        return 1

    len_s = len(s)
    ch = s[0]
    next_index = 0
    while next_index <= len_s//2:
        next_index = s.find(ch, next_index+1)
        if next_index == -1 or next_index > len_s//2:
            break

        len_sub = next_index
        if is_loop(len_sub, len_s, s):
            return len_s // len_sub

    return 1


def is_loop(len_sub, len_s, s):
    if len_s % len_sub:
        return False

    subs = s[:len_sub]
    other_subs_list = [
        s[i:i+len_sub]
        for i in range(len_sub, len_s//2+1, len_sub)
    ]
    return all(subs == x for x in other_subs_list)


if __name__ == '__main__':

    tests = [
        (
            "abccbaabccba",
            2
        ),
        (
            "abcabcabcabc",
            4
        ),
        (
            "abcabcabcabca",
            1
        ),
        (
            "aaaaaaaaaaa",
            11
        ),
        (
            "abcdebaaaa",
            1
        ),
        (
            "a",
            1
        ),
        (
            "",
            1
        )
    ]
    f = answer
    for input_args, expected in tests:

        if isinstance(input_args, tuple):
            r = f(*input_args)
        else:
            r = f(input_args)
        print 'Result:{}\tInput:{}\tOutput:{}\tExpected:{}'.format(r == expected, input_args, r, expected)
