# pyright: strict

import typing

from .. import coord

A = typing.TypeVar("A")


class InfGrid(typing.Generic[A]):
    __slots__ = ["_grid"]
    _grid: dict[coord.Coord, A]

    def __init__(self):
        self._grid = {}

    def __getitem__(self, pos: coord.CoordLike) -> A:
        match pos:
            case (int(), int()):
                return self._grid[coord.Coord(pos)]
            case coord.Coord():
                return self._grid[pos]

    def __setitem__(self, pos: coord.CoordLike, value: A) -> None:
        match pos:
            case (int(), int()):
                self._grid[coord.Coord(pos)] = value
            case coord.Coord():
                self._grid[pos] = value

    def __contains__(self, pos: coord.CoordLike):
        return pos in self._grid
