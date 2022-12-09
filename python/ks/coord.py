# pyright: strict
import typing
import dataclasses


@dataclasses.dataclass(init=False, frozen=True, eq=True, slots=True)
class Coord:
    x: int
    y: int

    _CoordLike = typing.Self | tuple[int, int]
    _Compatible = _CoordLike | int

    @typing.overload
    def __init__(self):
        pass

    @typing.overload
    def __init__(self, x_or_pt: int, y: int):
        pass

    @typing.overload
    def __init__(self, x_or_pt: _CoordLike):
        pass

    def __init__(self, x_or_pt: _CoordLike | int = 0, y: int = 0):
        match x_or_pt:
            case Coord(x, y) | (x, y):
                object.__setattr__(self, "x", x)
                object.__setattr__(self, "y", y)
            case int():
                object.__setattr__(self, "x", x_or_pt)
                object.__setattr__(self, "y", y)

    def __add__(self, other: _Compatible) -> typing.Self:
        match other:
            case Coord(x, y) | (x, y) | ((int() as x) as y):
                return Coord(self.x + x, self.y + y)

    def __radd__(self, other: _Compatible) -> typing.Self:
        return self + other

    def __sub__(self, other: _Compatible) -> typing.Self:
        match other:
            case Coord(x, y) | (x, y) | ((int() as x) as y):
                return Coord(self.x - x, self.y - y)

    def __rsub__(self, other: _Compatible) -> typing.Self:
        match other:
            case Coord(x, y) | (x, y) | ((int() as x) as y):
                return Coord(x - self.x, y - self.y)

    def __mul__(self, other: _Compatible) -> typing.Self:
        match other:
            case Coord(x, y) | (x, y) | ((int() as x) as y):
                return Coord(self.x * x, self.y * y)

    def __rmul__(self, other: _Compatible) -> typing.Self:
        return self * other

    def __matmul__(self, other: _Compatible) -> int:
        match other:
            case Coord(x, y) | (x, y) | ((int() as x) as y):
                return self.x * x + self.y * y

    def __lt__(self, other: _Compatible) -> typing.Self:
        match other:
            case Coord(x, y) | (x, y) | ((int() as x) as y):
                return Coord(self.x < x, self.y < y)

    def __le__(self, other: _Compatible) -> typing.Self:
        match other:
            case Coord(x, y) | (x, y) | ((int() as x) as y):
                return Coord(self.x <= x, self.y <= y)

    def __gt__(self, other: _Compatible) -> typing.Self:
        match other:
            case Coord(x, y) | (x, y) | ((int() as x) as y):
                return Coord(self.x > x, self.y > y)

    def __ge__(self, other: _Compatible) -> typing.Self:
        match other:
            case Coord(x, y) | (x, y) | ((int() as x) as y):
                return Coord(self.x >= x, self.y >= y)

    def __neg__(self) -> typing.Self:
        return Coord(-self.x, -self.y)

    def __pos__(self) -> typing.Self:
        return self

    def __abs__(self) -> typing.Self:
        return Coord(abs(self.x), abs(self.y))

    def __iter__(self) -> typing.Iterator[int]:
        yield self.x
        yield self.y

    def sign(self) -> typing.Self:
        return (self > 0) - (0 > self)

    def norm_taxicab(self) -> int:
        return abs(self.x) + abs(self.y)

    def norm_max(self) -> int:
        return max(abs(self.x), abs(self.y))

    def dist_taxicab(self, other: _CoordLike) -> int:
        return (self - other).norm_taxicab()

    def dist_max(self, other: _CoordLike) -> int:
        return (self - other).norm_max()
