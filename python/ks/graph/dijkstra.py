import typing
import heapq as hq
import dataclasses as dc

from .graph import Graph


@dc.dataclass
class DijkstraEntry[T]:
    node: T
    distance: int
    parent: T | None

    def __lt__(self, other: typing.Self):
        return self.distance < other.distance


def dijkstra_all[V](g: Graph[V, int], start: V) -> dict[V, DijkstraEntry[V]]:
    final: dict[V, DijkstraEntry[V]] | None = None
    for _, final in dijkstra_iter(g, start):
        pass
    assert final is not None
    return final


def dijkstra_iter[V](graph: Graph[V, int], start: V):
    final = dict[V, DijkstraEntry[V]]()
    priority = [DijkstraEntry(start, 0, None)]
    while priority:
        current = hq.heappop(priority)
        if current in final:
            continue
        final[current.node] = current
        yield current, final
        for node, edge in graph.neighbors(current.node).items():
            if node in final:
                # possibly unnecessary optimization
                continue
            hq.heappush(
                priority,
                DijkstraEntry(node, current.distance + edge, current.node),
            )
