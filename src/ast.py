from utils import log


def string_element(s):
    r = ''
    ec = False
    for i, e in enumerate(s[1:]):
        r += e
        if ec:
            continue
        elif e == '\\':
            ec = True
        elif e == '"':
            break
    return r


def common_element(s):
    for i, e in enumerate(s):
        if e == '"':
            return string_element[i:]
        elif e in ') ':
            return s[:i]


def tonkenizer(s):
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
            ele = common_element(s[i:])
            count = len(ele) - 1
            l.append(ele)


def test_common_element():
    st1 = 'foo 2.34 (- 3 bar))'
    st2 = 'bar))'
    log(common_element(st1))  # foo
    log(common_element(st2))  # bar


if __name__ == '__main__':
    test_common_element()
