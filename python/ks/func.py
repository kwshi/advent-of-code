# pyright: strict
import typing

import math

Fn = typing.Callable


def postprocess[**P, A, B](p: Fn[[A], B]) -> Fn[[Fn[P, A]], Fn[P, B]]:
    def wrap(f: Fn[P, A]):
        def wrapped(*args: P.args, **kwargs: P.kwargs):
            return p(f(*args, **kwargs))

        return wrapped

    return wrap


sum = postprocess(sum)
prod = postprocess(math.prod)
list = postprocess(list)
set = postprocess(set)
dict = postprocess(dict)
max = postprocess(max)
min = postprocess(min)


def join(sep: str):
    return postprocess(sep.join)


def count_unique(f: Fn[P, typing.Iterable[object]]) -> Fn[P, int]:
    def wrapped(*args: P.args, **kwargs: P.kwargs):
        return len({*f(*args, **kwargs)})

    return wrapped
