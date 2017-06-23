from ast import tree
from apply import Apply


def repl():
    while True:
        ast = tree(input('helion> '))
        print(Apply().apply(ast))


if __name__ == '__main__':
    repl()
