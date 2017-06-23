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


def tonkenizer(s):
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

    log(s1, tonkenizer(s1))
    log(s2, tonkenizer(s2))
    log(s3, tonkenizer(s3))
    log(s4, tonkenizer(s4))


if __name__ == '__main__':
# test_common_element()
# test_tokenizer()
