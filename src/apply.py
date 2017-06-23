from ast import parser
from utils import log, ensure
from functools import reduce


class Apply(object):
    def __init__(self, var=None, func=None):
        if var is None:
            var = {}
        if func is None:
            func = {}

        self.var = var
        self.func = func

    def plus(self, l):
        r = self.apply(l[1])
        for i, e in enumerate(l[2:]):
            r += self.apply(e)
        return r

    def minus(self, l):
        r = self.apply(l[1])
        for i, e in enumerate(l[2:]):
            r -= self.apply(e)
        return r

    def times(self, l):
        values = map(self.apply, l[1:])
        return reduce(lambda x, y: x * y, values)

    def divide(self, l):
        values = map(self.apply, l[1:])
        return reduce(lambda x, y: x / y, values)

    def apply(self, l):
        ops = {
            '+': self.plus,
            '-': self.minus,
            '*': self.times,
            '/': self.divide,
        }

        if type(l) == list:
            op = l[0]
            r = ops[op](l)
        elif type(l) == str:
            pass
        else:
            r = l
        return r


def test_plus():
    l1 = ['+', 1, 2]
    l2 = ['+', 1, 2, ['+', 1, 2]]

    ensure(Apply().plus(l1) == 3, 'plus 测试1')
    ensure(Apply().plus(l2) == 6, 'plus 测试2')


def test_minus():
    l1 = ['-', 2, 1]
    l2 = ['-', 5, 2, ['+', 1, 2]]

    ensure(Apply().minus(l1) == 1, 'minus 测试1')
    ensure(Apply().minus(l2) == 0, 'minus 测试2')


def test_times():
    l1 = ['*', 2, 1]
    l2 = ['*', 5, 2, ['+', 1, 2]]

    ensure(Apply().times(l1) == 2, 'times 测试1')
    ensure(Apply().times(l2) == 30, 'times 测试2')


def test_divide():
    l1 = ['/', 2, 2]
    l2 = ['/', 30, 2, ['+', 1, 2]]

    log(Apply().divide(l1))
    log(Apply().divide(l2))
    ensure(Apply().divide(l1) == 1, 'divide 测试1')
    ensure(Apply().divide(l2) == 5, 'divide 测试2')


def test():
    test_plus()
    test_minus()
    test_times()
    test_divide()


if __name__ == '__main__':
    test()
