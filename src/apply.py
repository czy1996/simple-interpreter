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
        log('var at plus', self.var)
        r = self.apply(l[1])
        log('plus r', r)
        for i, e in enumerate(l[2:]):
            log('plus e', self.apply(e))
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

    def define_func(self, l):
        # ['def', 'func', [,], [[]]]
        func_name = l[1]
        func_args = l[2]
        func_body = l[3]
        self.func[func_name] = (func_args, func_body)
        return 'N/A'

    def call_func(self, l):
        func_name = l[1]
        func_args, func_body = self.func[func_name]
        # log('func', self.func[func_name])
        func_params = l[2]
        new_var_dict = {}
        for i, arg in enumerate(func_args):
            new_var_dict[arg] = self.apply(func_params[i])
        # log('new_var_dict', new_var_dict)
        temp_dict = self.var.copy()
        temp_dict.update(new_var_dict)
        # log('new_var_dict', temp_dict)
        return Apply(new_var_dict, self.func).apply_trees(func_body)

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
            'var': self.define_variable,
            'def': self.define_func,
            'call': self.call_func,
        }

        if type(l) == list:
            op = l[0]
            r = ops[op](l)
        elif type(l) == str:
            return self.call_variable(l)
        else:
            r = l
        return r

    def apply_trees(self, l):
        r = []
        for i, e in enumerate(l):
            v = self.apply(e)
            r.append(v)
            log('var', self.var)
        return r[-1]


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


def test_call_function():
    d1 = [['def', 'f1', ['a', 'b'], [['if', ['<', 'a', 0], 3, 'b']]]]
    apply = Apply()
    apply.apply_trees(d1)
    # print('func', self.func)
    l1 = ['call', 'f1', [1, 2]]
    # log('var', apply.var)
    # log('func', apply.func)
    # log('func result', apply.call_func(l1))
    ensure(apply.call_func(l1) == 2, 'call_function 测试1')


def test_apply():
    l1 = ['+', 1, 2, ['-', 2, 1]]
    l2 = ['if', ['>', 1, 2], 1, 2]
    l3 = ['if', ['<', 1, 2], 1, 2]
    l4 = ['if', ['=', 1, 2], 1, 2]

    # print(apply(l1))
    # print(apply(l2))
    # print(apply(l3))
    # print(apply(l4))

    ensure(Apply().apply(l1) == 4, 'apply 测试1')
    ensure(Apply().apply(l2) == 2, 'apply 测试2')
    ensure(Apply().apply(l3) == 1, 'apply 测试3')
    ensure(Apply().apply(l4) == 2, 'apply 测试4')


def test_apply_trees():  # 这是最顶层的函数，传入抽象语法树
    l1 = [['+', 1, 2, ['-', 2, 1]]]
    l2 = [['-', 2, 2], ['-', 2, 1]]
    l3 = [['var', 'a', ['-', 2, 1]]]
    l4 = [['var', 'a', 1], ['var', 'b', ['+', 1, 1]], ['if', ['<', 'a', 0], 3, 'b']]
    l5 = [
        ['var', 'a', 3],
        ['var', 'b', 2],
        ['def', 'f1', ['a', 'b'], [['-', ['+', 'a', 2], 3, 'b']]],
        ['call', 'f1', ['a', 'b']]
    ]

    # ensure(Apply().apply_trees(l1) == 4, 'apply_trees 测试1')
    # ensure(Apply().apply_trees(l2) == 1, 'apply_trees 测试2')
    # ensure(Apply().apply_trees(l3) == 'N/A', 'apply_trees 测试3')
    # ensure(Apply().apply_trees(l4) == 2, 'apply_trees 测试4')
    ensure(Apply().apply_trees(l5) == 0, 'apply_trees 测试5')


def test():
    # test_plus()
    # test_minus()
    # test_times()
    # test_divide()
    # test_judge_cmp()
    # test_define_variable()
    # test_call_function()
    # test_apply()
    test_apply_trees()

if __name__ == '__main__':
    test()
