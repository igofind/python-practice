# encoding=utf-8

# print兼容 python 2 和 python 3
from __future__ import print_function
import traceback


def test_exception():
    try:
        print(1 / 0)
    except ZeroDivisionError as z:
        traceback.print_exc()


def test_list():
    a = list(range(10))
    print(a)

    # List displays
    b = [x * x for x in sorted(a, reverse=True)[0::4]]
    print(b)


def test_set():
    a = set()
    b = set()
    b.add(1.0)
    b.add(0)
    a.add(0)
    a.add(1)
    print(a == b)


# string conversions
def test_string():
    a = 2.32
    print(type(a), type(`a`))

    a = [1, 2, 3, 'b']
    print(a, a[0], `a`, `a`[0])

    # str()
    print(str(a), str(a)[0])

    # repr()
    print(repr(a), repr(a)[0])


def test_operations():
    print((1, 23, 4) == {1, 23, 4})
    print(1 is 1)
    print(1 is not 1)
    print(hash(test_operations))
    print(set() is set(), set() == set())


def test_expresion():
    a = 1
    b = 2
    c = 3
    if a < b < c: print(a);print(b);print(c)


# i = raw_input("init i value")
# def test_arg(arg=i):
#     print(arg)


def test_fun(a, L=[]):
    L.append(a)
    print(L)


def main():
    # print('\n', "main(): Hello Python.", '\n')
    # print(type(object.__new__))
    # test_exception()
    # test_expresion()
    # test_arg()
    test_fun(1)
    test_fun(2)
    test_fun(3)


if '__main__' == __name__:
    main()
