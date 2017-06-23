from utils import log


def string_element(s):
    """
    提取字符串元素
    :param s:
    :return:
    """
    r = '"'
    ec = False
    for i, e in enumerate(s[1:]):
        r += e
        if ec:
            ec = False
            continue
        elif e == '\\':
            ec = True
        elif e == '"':
            break
    return r


def common_element(s):
    """
    提取元素
    :param s:
    :return:
    """
    for i, e in enumerate(s):
        if e == '"':
            return string_element(s[i:])
        elif e in ') ':
            return s[:i]


def formatted_token(token):
    """
    数字转换为数字，替他不变
    :param token:
    :return:
    """
    num = '012345678'
    if token[0] in num:
        if '.' in token:
            return float(token)
        else:
            return int(token)
    else:
        return token


def tokenizer(s):
    """
    string to tokens
    :param s:
    :return:
    """
    l = []
    count = 0
    for i, e in enumerate(s):
        if count > 0:
            count -= 1
            continue
        elif e in '()':
            l.append(e)
        elif e == ' ':
            pass
        else:
            token = common_element(s[i:])
            count = len(token) - 1
            token = formatted_token(token)
            l.append(token)
    return l


def parser(tokens):
    """
    tokens to ast
    :param l:
    :return:
    """
    token = tokens.pop()
    l = []
    if token == ')':
        while tokens[-1] != '(':
            l.append(analyze_eles(tokens))
        tokens.pop()
        l.reverse()
        return l


def analyze_eles(tokens):
    token = tokens[-1]
    if token == ')':
        return parser(tokens)
    else:
        return tokens.pop()


def tree(s):
    """
    string to ast
    :param s:
    :return:
    """
    tokens = tokenizer(s)
    ast = parser(tokens)
    return ast


def test_tree():
    s1 = '(+ 1 2)'
    s2 = '(+ 12 2.34 (- 345 45))'
    s3 = '(+ foo 2.34 (- 3 bar))'
    s4 = '(+ foo 2.34 (- 3 "hi(\\" )"))'
    s5 = '(+ foo 2.34 (- 3 bar) (- 3 bar))'

    print(s1, '>>>', tree(s1))
    print(s2, '>>>', tree(s2))
    print(s3, '>>>', tree(s3))
    print(s4, '>>>', tree(s4))
    print(s5, '>>>', tree(s5))


def test_common_element():
    st1 = 'foo 2.34 (- 3 bar))'
    st2 = 'bar))'
    log(common_element(st1))  # foo
    log(common_element(st2))  # bar


def test_tokenizer():
    s1 = '(+ 1 2 (- 3 4))'
    s2 = '(+ 12 2.34 (- 345 45))'
    s3 = '(+ foo 2.34 (- 3 bar))'
    s4 = '(+ foo 2.34 (- 3 "hi(\\" )"))'

    log(s1, tokenizer(s1))
    log(s2, tokenizer(s2))
    log(s3, tokenizer(s3))
    log(s4, tokenizer(s4))


if __name__ == '__main__':
    # test_common_element()
    # test_tokenizer()
    test_tree()
