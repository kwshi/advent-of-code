# pyright: strict
import typing
import sys
from .p2 import P2
from .rect import Rect


class P2Set:
    _ps: set[P2]

    def __init__(self, ps: typing.Iterable[P2.Like] = ()):
        self._ps = {P2(p) for p in ps}

    @classmethod
    def parse_grid(cls, c: str | None = None):
        pass

    @property
    def bounds(self) -> Rect:
        pass

    def render(self, file: typing.TextIO = sys.stderr):
        if not self._ps:
            return

    def __add__(self, other: P2.Compatible):
        return P2Set(p + other for p in self._ps)

    def __contains__(self, p: P2.Like) -> bool:
        return p in self._ps
