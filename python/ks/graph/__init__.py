import typing
import collections.abc as cabc
import heapq as hq
import dataclasses as dc


@dc.dataclass
class DijkstraEntry[T]:
    node: T
    distance: int
    parent: T | None

    def __lt__(self, other: typing.Self):
        return self.distance < other.distance


@dc.dataclass
class Neighbor[T]:
    node: T
    weight: int
