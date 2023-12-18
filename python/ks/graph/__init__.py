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


class Graph[T](typing.Protocol):
    def neighbors(self, node: T, /) -> typing.Iterable[Neighbor[T]]:
        ...

    def dijkstra_all(self, start: T) -> dict[T, DijkstraEntry[T]]:
        final: dict[T, DijkstraEntry[T]] | None = None
        for _, final in self.dijkstra_iter(start):
            pass
        assert final is not None
        return final

    def dijkstra_iter(self, start: T):
        final = dict[T, DijkstraEntry[T]]()
        priority = [DijkstraEntry(start, 0, None)]
        while priority:
            current = hq.heappop(priority)
            if current in final:
                continue
            final[current.node] = current
            yield current, final
            for neighbor in self.neighbors(current.node):
                if neighbor in final:
                    # possibly unnecessary optimization
                    continue
                hq.heappush(
                    priority,
                    DijkstraEntry(
                        neighbor.node, current.distance + neighbor.weight, current.node
                    ),
                )


@dc.dataclass
class FuncGraph[T](Graph[T]):
    _neighbors: cabc.Callable[[T], cabc.Iterable[Neighbor[T]]]

    def neighbors(self, node: T, /):
        return self._neighbors(node)


@dc.dataclass
class MappingGraph[T](Graph[T]):
    _neighbors: cabc.Mapping[T, cabc.Iterable[Neighbor[T]]]

    def neighbors(self, node: T, /):
        return self._neighbors[node]
