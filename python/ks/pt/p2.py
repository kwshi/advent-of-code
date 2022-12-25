# pyright: strict
import typing
import dataclasses

from . import op


@dataclasses.dataclass(init=False, frozen=True, eq=False, slots=True)
class P2:

    Like = typing.Self | tuple[int, int]
    _Compatible = Like | int

    x: int
    y: int

    @typing.overload
    def __init__(self):
        pass

    @typing.overload
    def __init__(self, x_or_pt: int, y: int):
        pass

    @typing.overload
    def __init__(self, x_or_pt: Like):
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
        self, f: typing.Callable[[int, int], int], other: _Compatible
    ) -> typing.Self:
        match other:
            case P2(x, y) | (x, y) | ((int() as x) as y):
                return P2(f(self.x, x), f(self.y, y))

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

    def __floordiv__(self, other: _Compatible) -> typing.Self:
        return self._bop(op.floordiv, other)

    def __rfloordiv__(self, other: _Compatible) -> typing.Self:
        return self._bop(op.rfloordiv, other)

    def __mod__(self, other: _Compatible) -> typing.Self:
        return self._bop(op.mod, other)

    def __rmod__(self, other: _Compatible) -> typing.Self:
        return self._bop(op.rmod, other)

    def __lt__(self, other: _Compatible) -> typing.Self:
        return self._bop(op.lt, other)

    def __le__(self, other: _Compatible) -> typing.Self:
        return self._bop(op.le, other)

    def __gt__(self, other: _Compatible) -> typing.Self:
        return self._bop(op.gt, other)

    def __ge__(self, other: _Compatible) -> typing.Self:
        return self._bop(op.ge, other)

    def __matmul__(self, other: _Compatible) -> int:
        return sum(self._bop(op.mul, other))

    def __rmatmul__(self, other: _Compatible) -> int:
        return sum(self._bop(op.mul, other))

    def __neg__(self) -> typing.Self:
        return P2(-self.x, -self.y)

    def __pos__(self) -> typing.Self:
        return self

    def __abs__(self) -> typing.Self:
        return P2(abs(self.x), abs(self.y))

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
                return P2(self.y * other, -self.x * other)

    @property
    def sign(self) -> typing.Self:
        return (self > 0) - (0 > self)

    @property
    def norm1(self) -> int:
        return abs(self.x) + abs(self.y)

    @property
    def normi(self) -> int:
        return max(abs(self.x), abs(self.y))

    @property
    def rot1(self) -> typing.Self:
        return P2(-self.y, self.x)

    @property
    def rot2(self) -> typing.Self:
        return P2(-self.x, -self.y)

    @property
    def rot3(self) -> typing.Self:
        return P2(self.y, -self.x)

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
        return P2(-self.x, self.y)

    @property
    def negy(self) -> typing.Self:
        return P2(self.x, -self.y)

    @property
    def swap(self) -> typing.Self:
        return P2(self.y, self.x)

    def dist1(self, other: Like) -> int:
        return (self - other).norm1

    def disti(self, other: Like) -> int:
        return (self - other).normi

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

    def __str__(self) -> str:
        return f"P2({self.x:d},{self.y:d})"

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
