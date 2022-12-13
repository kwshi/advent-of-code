# pyright: strict
import typing

import math

A = typing.TypeVar("A")
B = typing.TypeVar("B")

P = typing.ParamSpec("P")

Fn = typing.Callable


def postprocess(p: Fn[[A], B], f: Fn[P, A]) -> Fn[P, B]:
    def wrapped(*args: P.args, **kwargs: P.kwargs):
        return p(f(*args, **kwargs))

    return wrapped


def sumify(f: Fn[P, typing.Iterable[int]]) -> Fn[P, int]:
    return postprocess(sum, f)


def prodify(f: Fn[P, typing.Iterable[int]]) -> Fn[P, int]:
    return postprocess(math.prod, f)


def listify(f: Fn[P, typing.Iterable[A]]) -> Fn[P, list[A]]:
    return postprocess(list, f)


def setify(f: Fn[P, typing.Iterable[A]]) -> Fn[P, set[A]]:
    return postprocess(set, f)


def dictify(f: Fn[P, typing.Iterable[tuple[A, B]]]) -> Fn[P, dict[A, B]]:
    return postprocess(dict, f)


def maxify(f: Fn[P, typing.Iterable[int]]) -> Fn[P, int]:
    return postprocess(max, f)


def minify(f: Fn[P, typing.Iterable[int]]) -> Fn[P, int]:
    return postprocess(min, f)


def joinify(sep: str = "") -> Fn[[Fn[P, typing.Iterable[str]]], Fn[P, str]]:
    def wrap(f: Fn[P, typing.Iterable[str]]) -> Fn[P, str]:
        return postprocess(sep.join, f)

    return wrap


def count_unique(f: Fn[P, typing.Iterable[object]]) -> Fn[P, int]:
    def wrapped(*args: P.args, **kwargs: P.kwargs):
        return len({*f(*args, **kwargs)})

    return wrapped
