# pyright: strict
import typing
import dataclasses

from .base import PBase

Like = typing.Union["P2", tuple[int, int]]
Compatible = Like | int


@dataclasses.dataclass(init=False, frozen=True, eq=False, slots=True)
class P2(PBase[Like, Compatible]):
    Like = Like
    Compatible = Compatible

    x: int
    y: int

    @typing.overload
    def __init__(self) -> None:
        pass

    @typing.overload
    def __init__(self, x_or_pt: int, y: int) -> None:
        pass

    @typing.overload
    def __init__(self, x_or_pt: Like) -> None:
        pass

    def __init__(self, x_or_pt: Like | int = 0, y: int = 0):
        match x_or_pt:
            case P2(x, y) | (x, y):
                object.__setattr__(self, "x", x)
                object.__setattr__(self, "y", y)
            case int():
                object.__setattr__(self, "x", x_or_pt)
                object.__setattr__(self, "y", y)

    def _bop(
        self, f: typing.Callable[[int, int], int], other: Compatible
    ) -> typing.Self:
        match other:
            case P2(x, y) | (x, y) | ((int() as x) as y):
                return type(self)(f(self.x, x), f(self.y, y))

    def _uop(self, f: typing.Callable[[int], int]) -> typing.Self:
        return type(self)(f(self.x), f(self.y))

    def __iter__(self) -> typing.Iterator[int]:
        yield self.x
        yield self.y

    @typing.overload
    def cross(self, other: Like) -> int:
        pass

    @typing.overload
    def cross(self, other: int) -> typing.Self:
        pass

    def cross(self, other: Like | int) -> int | typing.Self:
        match other:
            case P2(x, y) | (x, y):
                return self.x * y - x * self.y
            case int():
                return type(self)(self.y * other, -self.x * other)

    @property
    def rot1(self) -> typing.Self:
        return type(self)(-self.y, self.x)

    @property
    def rot2(self) -> typing.Self:
        return type(self)(-self.x, -self.y)

    @property
    def rot3(self) -> typing.Self:
        return type(self)(self.y, -self.x)

    def rot(self, n: int) -> typing.Self:
        match n % 4:
            case 0:
                return self
            case 1:
                return self.rot1
            case 2:
                return self.rot2
            case 3:
                return self.rot3
            case _:
                assert False

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
