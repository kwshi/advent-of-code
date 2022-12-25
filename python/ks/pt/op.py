# basically the built-in `operators` library, but with better typing and also
# flipped-operand variants


def add(a: int, b: int) -> int:
    return a + b


def sub(a: int, b: int) -> int:
    return a - b


def mul(a: int, b: int) -> int:
    return a * b


def floordiv(a: int, b: int) -> int:
    return a // b


def rfloordiv(a: int, b: int) -> int:
    return b // a


def rsub(a: int, b: int) -> int:
    return b - a


def mod(a: int, b: int) -> int:
    return a % b


def rmod(a: int, b: int) -> int:
    return b % a


def lt(a: int, b: int) -> int:
    return a < b


def le(a: int, b: int) -> int:
    return a <= b


def gt(a: int, b: int) -> int:
    return a > b


def ge(a: int, b: int) -> int:
    return a >= b
