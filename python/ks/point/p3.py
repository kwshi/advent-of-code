# pyright: strict

import typing
import dataclasses

from .base import PBase
from .p2 import P2

Like = typing.Union["P3", P2, tuple[int, int, int], tuple[int, int]]
Compatible = Like | int


@dataclasses.dataclass(init=False, frozen=True, eq=False, slots=True)
class P3(PBase[Like, Compatible]):
    x: int
    y: int
    z: int

    Like = Like
    Compatible = Compatible

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
        self, f: typing.Callable[[int, int], int], other: Compatible
    ) -> typing.Self:
        match other:
            case P3(x, y, z) | (x, y, z) | (((int() as x) as y) as z):
                return P3(f(self.x, x), f(self.y, y), f(self.z, z))
            case P2(x, y) | (x, y):
                return P3(f(self.x, x), f(self.y, y), f(self.z, 0))

    def _uop(self, f: typing.Callable[[int], int]) -> typing.Self:
        return P3(f(self.x), f(self.y), f(self.z))

    def cross(self, other: Compatible) -> typing.Self:
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

    def __iter__(self) -> typing.Iterator[int]:
        yield self.x
        yield self.y
        yield self.z

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
