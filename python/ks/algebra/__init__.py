import typing
import collections.abc as cabc

from ..num import bezout


class Ring[Compatible](typing.Protocol):
    @classmethod
    def construct(cls, c: typing.Self | Compatible, /) -> typing.Self:
        ...

    def __add__(self, other: typing.Self | Compatible) -> typing.Self:
        ...

    def __mul__(self, other: typing.Self | Compatible) -> typing.Self:
        ...

    def __eq__(self, other: object, /) -> bool:
        ...


class Field[Compatible](Ring[Compatible], typing.Protocol):
    def inverse(self) -> typing.Self:
        ...

    def __truediv__(self, other: typing.Self | Compatible) -> typing.Self:
        return self * self.construct(other).inverse()


def zmod(n: int):
    class ZMod(Field[int]):
        _value: int
        __match_args__ = ("_value",)

        def __init__(self, value: int = 0, /):
            object.__setattr__(self, "_value", value)

        def __setattr__(self, *_):
            raise TypeError("ZMod is immutable")

        @classmethod
        def construct(cls, value: typing.Self | int = 0):
            match value:
                case int(v) | ZMod(v):
                    return cls(v)

        @classmethod
        def _get_value(cls, value: typing.Self | int) -> int:
            match value:
                case int(v) | ZMod(v):
                    return v

        def _bop_int(
            self, f: cabc.Callable[[int, int], int], other: int | typing.Self
        ) -> typing.Self:
            return type(self)(f(self._value, self._get_value(other)))

        def _rbop_int(
            self, f: cabc.Callable[[int, int], int], other: int | typing.Self
        ) -> typing.Self:
            return type(self)(f(self._value, self._get_value(other)))

        def __add__(self, other: int | typing.Self) -> typing.Self:
            return self._bop_int(int.__add__, other)

        def __mul__(self, other: int | typing.Self) -> typing.Self:
            return self._bop_int(int.__mul__, other)

        def inverse(self):
            # a ⋅ value + _ ⋅ n = d
            d, a, _ = bezout(self._value, n)
            if d != 1:
                raise ZeroDivisionError(
                    f"{self._value} has no inverse mod {n} (gcd={d})"
                )
            return self.construct(a)

    return ZMod
