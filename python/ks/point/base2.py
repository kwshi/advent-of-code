import typing

from .base import PBase

type Like = PBase2 | tuple[int, int]
type Compatible = Like | int


class PBase2(PBase[Like, Compatible]):
    _x0: int
    _x1: int

    __match_args__ = "_x0", "_x1"
    __slots__ = "_x0", "_x1"

    @typing.overload
    def __init__(self) -> None:
        pass

    @typing.overload
    def __init__(self, x0: int, x1: int, /) -> None:
        pass

    @typing.overload
    def __init__(self, point: Like, /) -> None:
        pass

    def __init__(self, x0_or_point: Like | int = 0, x1: int = 0):
        match x0_or_point:
            case PBase2(x0, x1) | (x0, x1):
                object.__setattr__(self, "_x0", x0)
                object.__setattr__(self, "_x1", x1)
            case int():
                object.__setattr__(self, "_x0", x0_or_point)
                object.__setattr__(self, "_x1", x1)

    def __eq__(self, other: object):
        match other:
            case PBase2(x0, x1) | (int() as x0, int() as x1):
                return self._x0 == x0 and self._x1 == x1
            case _:
                return False

    def _bop(
        self, f: typing.Callable[[int, int], int], other: Compatible
    ) -> typing.Self:
        match other:
            case PBase2(x0, x1) | (x0, x1) | ((int() as x0) as x1):
                return type(self)(f(self._x0, x0), f(self._x1, x1))

    def _uop(self, f: typing.Callable[[int], int]) -> typing.Self:
        return type(self)(f(self._x0), f(self._x1))

    def __iter__(self) -> typing.Iterator[int]:
        yield self._x0
        yield self._x1

    @typing.overload
    def cross(self, other: Like) -> int:
        pass

    @typing.overload
    def cross(self, other: int) -> typing.Self:
        pass

    def cross(self, other: Like | int) -> int | typing.Self:
        match other:
            case PBase2(x0, x1) | (x0, x1):
                return self._x0 * x1 - self._x1 * x0
            case int():
                return type(self)(self._x1 * other, -self._x0 * other)

    def rot(self, n: int) -> typing.Self:
        match n % 4:
            case 0:
                return self
            case 1:
                return type(self)(-self._x1, self._x0)
            case 2:
                return type(self)(-self._x0, -self._x1)
            case 3:
                return type(self)(self._x1, -self._x0)
            case _:
                assert False, "unreachable by laws of modular arithmetic"

    def reflect(self, normal: Like):
        match normal:
            case (0, 0) | PBase2(0, 0):
                raise ValueError("cannot reflect across 0 normal")
            case (0, _) | PBase2(0, _):
                return type(self)(self._x0, -self._x1)
            case (_, 0) | PBase2(_, 0):
                return type(self)(-self._x0, self._x1)
            case (x, y) | P2(x, y) if x == y:
                return type(self)(-self.y, -self.x)
            case (x, y) | P2(x, y) if x == -y:
                return type(self)(self.y, self.x)
            case _:
                raise ValueError(
                    f"invalid reflection normal {normal}; "
                    "must be one of eight cardinal/ordinal directions"
                )

    def reflect_on(self, axis: Like):
        return self.reflect(type(self)(axis).rot1)

    @property
    def negx(self) -> typing.Self:
        return type(self)(-self.x, self.y)

    @property
    def negy(self) -> typing.Self:
        return type(self)(self.x, -self.y)

    @property
    def swap(self) -> typing.Self:
        return type(self)(self.y, self.x)

    def circ1(self, radius: int) -> typing.Iterator[typing.Self]:
        if not radius:
            yield self
            return
        for k in range(radius):
            yield self + (radius - k, k)
            yield self + (-k, radius - k)
            yield self + (k - radius, -k)
            yield self + (k, k - radius)

    def disk1(self, radius: int) -> typing.Iterator[typing.Self]:
        for r in range(radius + 1):
            yield from self.circ1(r)

    def circi(self, radius: int) -> typing.Iterator[typing.Self]:
        if not radius:
            yield self
            return
        for k in range(2 * radius):
            yield self + (radius - k, radius)
            yield self + (-radius, radius - k)
            yield self + (k - radius, -radius)
            yield self + (radius, k - radius)

    def diski(self, radius: int) -> typing.Iterator[typing.Self]:
        for r in range(radius + 1):
            yield from self.circ1(r)

    @property
    def adj1(self) -> typing.Iterable[typing.Self]:
        return [self + (1, 0), self + (0, 1), self + (-1, 0), self + (0, -1)]

    @property
    def adji(self) -> typing.Iterable[typing.Self]:
        return [
            self + (1, 0),
            self + (1, 1),
            self + (0, 1),
            self + (-1, 1),
            self + (-1, 0),
            self + (-1, -1),
            self + (0, -1),
            self + (1, -1),
        ]

    @property
    def east(self) -> typing.Self:
        return self + (1, 0)

    @property
    def ne(self) -> typing.Self:
        return self + (1, 1)

    @property
    def north(self) -> typing.Self:
        return self + (0, 1)

    @property
    def nw(self) -> typing.Self:
        return self + (-1, 1)

    @property
    def west(self) -> typing.Self:
        return self + (-1, 0)

    @property
    def sw(self) -> typing.Self:
        return self + (-1, -1)

    @property
    def south(self) -> typing.Self:
        return self + (0, -1)

    @property
    def se(self) -> typing.Self:
        return self + (1, -1)
