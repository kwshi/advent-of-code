# pyright: strict
import typing
import dataclasses

from .p2 import P2
from ..interval import Interval


@dataclasses.dataclass(frozen=True, eq=True)
class Rect:
    sw: P2
    ne: P2

    @property
    def nw(self) -> P2:
        return P2(self.sw.x, self.ne.y)

    @property
    def se(self) -> P2:
        return P2(self.ne.x, self.sw.y)

    @property
    def x(self) -> Interval:
        return Interval(self.sw.x, self.ne.x)

    @property
    def y(self) -> Interval:
        return Interval(self.sw.y, self.ne.y)

    def __or__(self, other: typing.Self) -> typing.Self:
        return Rect(self.sw.min(other.sw), self.ne.max(other.ne))

    def __and__(self, other: typing.Self) -> typing.Self | None:
        sw, ne = self.sw.max(other.sw), self.ne.max(other.ne)
        return Rect(sw, ne) if sw.x <= ne.x and sw.y <= ne.y else None
