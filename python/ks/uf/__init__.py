# pyright: strict

import typing
import dataclasses

A = typing.TypeVar("A")

__all__ = ["Uf"]


@dataclasses.dataclass(frozen=True)
class Root(typing.Generic[A]):
    key: A
    size: int
    rank: int


class _Node(typing.Generic[A]):
    key: A
    parent: typing.Self
    size: int
    rank: int

    def __init__(self, key: A):
        self.key = key
        self.parent = self
        self.size = 1
        self.rank = 0

    def find(self) -> typing.Self:
        node = self
        while node.parent is not node:
            node, node.parent = node.parent, node.parent.parent
        return node

    def as_root(self) -> Root[A]:
        return Root(key=self.key, size=self.size, rank=self.rank)


class Uf(typing.Generic[A]):
    """
    Union-find data structure.
    """

    Root = Root

    _nodes: dict[A, _Node[A]]
    _components: int

    def __init__(self, keys: typing.Iterable[A] = ()):
        self._nodes = {key: _Node(key) for key in keys}
        self._components = len(self._nodes)

    def add(self, key: A) -> bool:
        if key in self._nodes:
            return False

        self._nodes[key] = _Node(key)
        self._components += 1
        return True

    def merge(self, key1: A, key2: A) -> bool:
        root1, root2 = self._nodes[key1].find(), self._nodes[key2].find()

        if root1 is root2:
            return False

        if root1.rank < root2.rank:
            root1.parent = root2
            root2.size += root1.size
        else:
            root2.parent = root1
            root1.size += root2.size
            root1.rank += root1.rank == root2.rank

        self._components -= 1
        return True

    def __getitem__(self, key: A) -> Root[A]:
        return self._nodes[key].find().as_root()

    def __contains__(self, key: A) -> bool:
        return key in self._nodes

    @property
    def nkeys(self) -> int:
        return len(self._nodes)

    @property
    def ncomponents(self) -> int:
        return self._components

    def keys(self) -> typing.Iterable[A]:
        return self._nodes.keys()

    def components(self) -> dict[A, set[A]]:
        components: dict[A, set[A]] = {}
        for node in self._nodes.values():
            root = node.find().key
            if root not in components:
                components[root] = {root}
            components[root].add(node.key)
        return components
