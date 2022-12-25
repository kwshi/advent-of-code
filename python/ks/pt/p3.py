# pyright: strict

import typing
import dataclasses

from . import op


@dataclasses.dataclass(init=False, frozen=True, eq=False, slots=True)
class P3:
    x: int
    y: int
    z: int

    _P3Like = typing.Self | tuple[int, int, int]
    _P3Compatible = _P3Like | int

    @typing.overload
    def __init__(self):
        pass

    @typing.overload
    def __init__(self, x_or_p3: _P3Like):
        pass

    @typing.overload
    def __init__(self, x_or_p3: int, y: int, z: int):
        pass

    def __init__(self, x_or_p3: int | _P3Like = 0, y: int = 0, z: int = 0):
        match x_or_p3:
            case P3(x, y, z) | (x, y, z):
                object.__setattr__(self, "x", x)
                object.__setattr__(self, "y", y)
                object.__setattr__(self, "z", z)
            case x:
                object.__setattr__(self, "x", x)
                object.__setattr__(self, "y", y)
                object.__setattr__(self, "z", z)

    def _bop(
        self, f: typing.Callable[[int, int], int], other: _P3Compatible
    ) -> typing.Self:
        match other:
            case P3(x, y, z) | (x, y, z) | ((x as y) as z):
                return P3(f(self.x, x), f(self.y, y), f(self.z, z))

    def __add__(self, other: _P3Like) -> typing.Self:
        return self._bop(op.add, other)

    def __radd__(self, other: _P3Like) -> typing.Self:
        return self._bop(op.add, other)

    def __sub__(self, other: _P3Like) -> typing.Self:
        return self._bop(op.sub, other)

    def __rsub__(self, other: _P3Like) -> typing.Self:
        return self._bop(op.rsub, other)

    def __mul__(self, other: _P3Like) -> typing.Self:
        return self._bop(op.mul, other)

    def __rmul__(self, other: _P3Like) -> typing.Self:
        return self._bop(op.mul, other)

    def __matmul__(self, other: _P3Like) -> int:
        return sum(self._bop(op.mul, other))

    def __rmatmul__(self, other: _P3Like) -> int:
        return sum(self._bop(op.mul, other))

    def __iter__(self) -> typing.Iterator[int]:
        return iter((self.x, self.y, self.z))

    def __floordiv__(self, other: _P3Like) -> typing.Self:
        return self._bop(op.floordiv, other)

    def __mod__(self, other: _P3Like) -> typing.Self:
        return self._bop(op.mod, other)

    def __eq__(self, other: object):
        match other:
            case P3(x, y, z) | (x, y, z):
                return self.x == x and self.y == y and self.z == z
            case _:
                return False

    def __hash__(self):
        return hash((self.x, self.y, self.z))
