# pyright: strict
import typing

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


def listify(f: Fn[P, typing.Iterable[A]]) -> Fn[P, list[A]]:
    return postprocess(list, f)


def setify(f: Fn[P, typing.Iterable[A]]) -> Fn[P, set[A]]:
    return postprocess(set, f)


def dictify(f: Fn[P, typing.Iterable[tuple[A, B]]]) -> Fn[P, dict[A, B]]:
    return postprocess(dict, f)
