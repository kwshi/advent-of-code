# pyright: strict

import typing
import dataclasses

from . import op
from .p2 import P2


@dataclasses.dataclass(init=False, frozen=True, eq=False, slots=True)
class P3:
    x: int
    y: int
    z: int

    Like = typing.Self | tuple[int, int, int] | P2.Like
    _Compatible = Like | int

    @typing.overload
    def __init__(self):
        pass

    @typing.overload
    def __init__(self, x_or_pt: Like):
        pass

    @typing.overload
    def __init__(self, x_or_pt: int, y: int, z: int):
        pass

    def __init__(self, x_or_pt: int | Like = 0, y: int = 0, z: int = 0):
        match x_or_pt:
            case P3(x, y, z) | (x, y, z):
                object.__setattr__(self, "x", x)
                object.__setattr__(self, "y", y)
                object.__setattr__(self, "z", z)
            case P2(x, y) | (x, y):
                object.__setattr__(self, "x", x)
                object.__setattr__(self, "y", y)
                object.__setattr__(self, "z", 0)
            case int():
                object.__setattr__(self, "x", x_or_pt)
                object.__setattr__(self, "y", y)
                object.__setattr__(self, "z", z)

    def _bop(
        self, f: typing.Callable[[int, int], int], other: _Compatible
    ) -> typing.Self:
        match other:
            case P3(x, y, z) | (x, y, z) | (((int() as x) as y) as z):
                return P3(f(self.x, x), f(self.y, y), f(self.z, z))
            case P2(x, y) | (x, y):
                return P3(f(self.x, x), f(self.y, y), f(self.z, 0))

    def _uop(self, f: typing.Callable[[int], int]) -> typing.Self:
        return P3(f(self.x), f(self.y), f(self.z))

    def __add__(self, other: _Compatible) -> typing.Self:
        return self._bop(op.add, other)

    def __radd__(self, other: _Compatible) -> typing.Self:
        return self._bop(op.add, other)

    def __sub__(self, other: _Compatible) -> typing.Self:
        return self._bop(op.sub, other)

    def __rsub__(self, other: _Compatible) -> typing.Self:
        return self._bop(op.rsub, other)

    def __mul__(self, other: _Compatible) -> typing.Self:
        return self._bop(op.mul, other)

    def __rmul__(self, other: _Compatible) -> typing.Self:
        return self._bop(op.mul, other)

    def __matmul__(self, other: _Compatible) -> int:
        return sum(self._bop(op.mul, other))

    def __rmatmul__(self, other: _Compatible) -> int:
        return sum(self._bop(op.mul, other))

    def cross(self, other: _Compatible) -> typing.Self:
        match other:
            case P3(x, y, z) | (x, y, z):
                return P3(
                    self.y * z - self.z * y,
                    self.z * x - self.x * z,
                    self.x * y - self.y * x,
                )
            case P2(x, y) | (x, y):
                return P3(
                    self.y * 0 - self.z * y,
                    self.z * x - self.x * 0,
                    self.x * y - self.y * x,
                )
            case int():
                return P3(self.y * other, -self.x * other, 0)

    def __neg__(self) -> typing.Self:
        return self._uop(op.neg)

    def __invert__(self) -> typing.Self:
        return self._uop(op.invert)

    def __pos__(self) -> typing.Self:
        return self

    def __abs__(self) -> typing.Self:
        return self._uop(abs)

    def __iter__(self) -> typing.Iterator[int]:
        yield self.x
        yield self.y
        yield self.z

    def __floordiv__(self, other: Like) -> typing.Self:
        return self._bop(op.floordiv, other)

    def __mod__(self, other: Like) -> typing.Self:
        return self._bop(op.mod, other)

    def __rfloordiv__(self, other: Like) -> typing.Self:
        return self._bop(op.rfloordiv, other)

    def __rmod__(self, other: Like) -> typing.Self:
        return self._bop(op.rmod, other)

    @property
    def norm1(self) -> int:
        return sum(abs(self))

    @property
    def normi(self) -> int:
        return max(abs(self))

    def dist1(self, other: Like) -> int:
        return (self - other).norm1

    def disti(self, other: Like) -> int:
        return (self - other).normi

    @property
    def adj1(self) -> typing.Iterable[typing.Self]:
        return [
            self + (1, 0, 0),
            self + (0, 1, 0),
            self + (0, 0, 1),
            self + (-1, 0, 0),
            self + (0, -1, 0),
            self + (0, 0, -1),
        ]

    @property
    def adji(self) -> typing.Iterable[typing.Self]:
        return NotImplemented

    def __eq__(self, other: object):
        match other:
            case P3(x, y, z) | (x, y, z):
                return self.x == x and self.y == y and self.z == z
            case _:
                return False

    def __hash__(self):
        return hash((self.x, self.y, self.z))
