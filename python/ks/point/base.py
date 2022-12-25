# pyright: strict

import abc
import typing

from . import op

Like = typing.TypeVar("Like")
Compatible = typing.TypeVar("Compatible")


class PBase(abc.ABC, typing.Generic[Like, Compatible]):
    Like = Like

    @abc.abstractmethod
    def __iter__(self) -> typing.Iterator[int]:
        pass

    @abc.abstractmethod
    def _uop(self, f: typing.Callable[[int], int]) -> typing.Self:
        pass

    @abc.abstractmethod
    def _bop(
        self, f: typing.Callable[[int, int], int], other: Compatible
    ) -> typing.Self:
        pass

    def __abs__(self) -> typing.Self:
        return self._uop(abs)

    def __pos__(self) -> typing.Self:
        return self

    def __neg__(self) -> typing.Self:
        return self._uop(op.neg)

    def __invert__(self) -> typing.Self:
        return self._uop(op.invert)

    def __add__(self, other: Compatible) -> typing.Self:
        return self._bop(op.add, other)

    def __radd__(self, other: Compatible) -> typing.Self:
        return self._bop(op.add, other)

    def __sub__(self, other: Compatible) -> typing.Self:
        return self._bop(op.sub, other)

    def __rsub__(self, other: Compatible) -> typing.Self:
        return self._bop(op.rsub, other)

    def __mul__(self, other: Compatible) -> typing.Self:
        return self._bop(op.mul, other)

    def __rmul__(self, other: Compatible) -> typing.Self:
        return self._bop(op.mul, other)

    def __floordiv__(self, other: Compatible) -> typing.Self:
        return self._bop(op.floordiv, other)

    def __rfloordiv__(self, other: Compatible) -> typing.Self:
        return self._bop(op.rfloordiv, other)

    def __mod__(self, other: Compatible) -> typing.Self:
        return self._bop(op.mod, other)

    def __rmod__(self, other: Compatible) -> typing.Self:
        return self._bop(op.rmod, other)

    def __matmul__(self, other: Compatible) -> int:
        return sum(self._bop(op.mul, other))

    def __rmatmul__(self, other: Compatible) -> int:
        return sum(self._bop(op.mul, other))

    def __lt__(self, other: Compatible) -> typing.Self:
        return self._bop(op.lt, other)

    def __le__(self, other: Compatible) -> typing.Self:
        return self._bop(op.le, other)

    def __gt__(self, other: Compatible) -> typing.Self:
        return self._bop(op.gt, other)

    def __ge__(self, other: Compatible) -> typing.Self:
        return self._bop(op.ge, other)

    @property
    def sign(self) -> typing.Self:
        return self._uop(op.sign)

    @property
    def norm1(self) -> int:
        return sum(abs(self))

    @property
    def normi(self) -> int:
        return sum(abs(self))

    def dist1(self, other: Compatible) -> int:
        return (self - other).norm1

    def disti(self, other: Compatible) -> int:
        return (self - other).normi

    def __str__(self) -> str:
        return f"{type(self).__name__}({','.join(map(str, self))})"
