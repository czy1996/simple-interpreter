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

    def greater_than(self, l):
        return self.apply(l[1]) > self.apply(l[2])

    def less_than(self, l):
        return self.apply(l[1]) < self.apply(l[2])

    def equal(self, l):
        return self.apply(l[1]) == self.apply(l[2])

    def judge(self, l):
        if self.apply(l[1]) is True:
            return self.apply(l[2])
        else:
            return self.apply(l[3])

    def define_variable(self, l):
        self.var[l[1]] = self.apply(l[2])
        return 'N/A'

    def call_variable(self, l):
        return self.var.get(l)

    def apply(self, l):
        ops = {
            '+': self.plus,
            '-': self.minus,
            '*': self.times,
            '/': self.divide,
            '>': self.greater_than,
            '<': self.less_than,
            '=': self.equal,
            'if': self.judge,
        }

        if type(l) == list:
            op = l[0]
            r = ops[op](l)
        elif type(l) == str:
            return self.call_variable(l)
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


def test_greater_than():
    l1 = ['>', 2, 1]
    l2 = ['>', 1, 2]
    l3 = ['>', 1, ['+', 1, 1]]

    ensure(Apply().greater_than(l1), 'more 测试1')
    ensure(not Apply().greater_than(l2), 'more 测试2')
    ensure(not Apply().greater_than(l3), 'more 测试3')


def test_less_than():
    l1 = ['<', 2, 1]
    l2 = ['<', 1, 2]
    l3 = ['<', 1, ['+', 1, 1]]

    ensure(not Apply().less_than(l1), 'less 测试1')
    ensure(Apply().less_than(l2), 'less 测试2')
    ensure(Apply().less_than(l3), 'less 测试3')


def test_equal():
    l1 = ['=', 2, 1]
    l2 = ['=', 2, 2]
    l3 = ['=', 2, ['+', 1, 1]]

    ensure(not Apply().equal(l1), 'equal 测试1')
    ensure(Apply().equal(l2), 'equal 测试2')
    ensure(Apply().equal(l3), 'equal 测试3')


def test_judge():
    l1 = ['if', True, 1, 2]
    l2 = ['if', False, 2, ['+', 1, 2]]
    l3 = ['if', False, 2, ['if', True, 1, 2]]

    ensure(Apply().judge(l1) == 1, 'judge 测试1')
    ensure(Apply().judge(l2) == 3, 'judge 测试2')
    ensure(Apply().judge(l3) == 1, 'judge 测试3')


def test_judge_cmp():
    l1 = ['if', ['>', 3, 4], 1, 2]
    l2 = ['if', False, 2, ['+', 1, 2]]
    l3 = ['if', False, 2, ['if', True, 1, 2]]

    ensure(Apply().judge(l1) == 2, 'judge 测试1')
    ensure(Apply().judge(l2) == 3, 'judge 测试2')
    ensure(Apply().judge(l3) == 1, 'judge 测试3')


def test_define_variable():
    l1 = ['var', 'a', 2]
    l2 = ['var', 'a', ['-', 2, 1]]

    ensure(Apply().define_variable(l1) == 'N/A', 'define_variable 测试1')
    ensure(Apply().define_variable(l2) == 'N/A', 'define_variable 测试2')



def test():
    # test_plus()
    # test_minus()
    # test_times()
    # test_divide()
    # test_judge_cmp()
    test_define_variable()
if __name__ == '__main__':
    test()
