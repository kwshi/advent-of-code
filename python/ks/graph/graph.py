import typing
import collections.abc as cabc


class Graph[V, E](typing.Protocol):
    def neighbors(self, node: V, /) -> typing.Mapping[V, E]:
        ...


class GraphFinite[V, E](Graph[V, E], typing.Protocol):
    def nodes(self) -> typing.Iterable[V]:
        ...

    def edges(self) -> typing.Mapping[tuple[V, V], E]:
        return {(p, q): e for p in self.nodes() for q, e in self.neighbors(p).items()}


class FuncGraph[V, E](Graph[V, E]):
    _neighbors: cabc.Callable[[V], cabc.Iterable[tuple[V, E]]]

    def __init__(self, f: cabc.Callable[[V], cabc.Iterable[tuple[V, E]]]):
        self._neighbors = f

    def neighbors(self, node: V, /):
        return dict(self._neighbors(node))


class MappingGraph[V, E](GraphFinite[V, E]):
    _neighbors: cabc.Mapping[V, cabc.Mapping[V, E]]

    def __init__(self, m: cabc.Mapping[V, cabc.Mapping[V, E]]):
        self._neighbors = m

    def neighbors(self, node: V, /):
        return self._neighbors[node]

    def nodes(self):
        return self._neighbors.keys()
