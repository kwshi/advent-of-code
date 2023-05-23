# pyright: strict
import typing
import dataclasses

from .interval import Interval


@dataclasses.dataclass
class _Node:
    interval: Interval
    left: typing.Self | None = dataclasses.field(default=None)
    right: typing.Self | None = dataclasses.field(default=None)

    def union(self, interval: Interval) -> None:
        # disjoint with current node, strictly less; union with left subtree
        if interval.r < self.interval.l - 1:
            if self.left is None:
                self.left = type(self)(interval)
                return
            self.left.union(interval)
            return

        # disjoint, strictly greater than current node
        if interval.l > self.interval.r + 1:
            if self.right is None:
                self.right = type(self)(interval)
                return
            self.right.union(interval)
            return

        # overlaps current interval
        self.left, l = self._extend_l(interval.l)
        self.right, r = self._extend_r(interval.r)
        self.interval = Interval(l, r)

    def _extend_l(self, l: int) -> tuple[typing.Self | None, int]:
        if l >= self.interval.l:
            return self.left, self.interval.l
        if self.left is None:
            return None, l
        return self.left._merge_l(l)

    def _extend_r(self, r: int) -> tuple[typing.Self | None, int]:
        if r <= self.interval.r:
            return self.right, self.interval.r
        if self.right is None:
            return None, r
        return self.right._merge_r(r)

    def _merge_l(self, l: int) -> tuple[typing.Self | None, int]:
        if l < self.interval.l:
            if self.left is None:
                return None, l
            return self.left._merge_l(l)

        if l <= self.interval.r + 1:
            self.right = None
            return self.left, self.interval.l

        if self.right is None:
            return self, l
        self.right, new_l = self.right._merge_l(l)
        return self, new_l

    def _merge_r(self, r: int) -> tuple[typing.Self | None, int]:
        if r > self.interval.r:
            if self.right is None:
                return None, r
            return self.right._merge_r(r)

        if r >= self.interval.l - 1:
            self.left = None
            return self.right, self.interval.r

        if self.left is None:
            return self, r
        self.left, new_r = self.left._merge_r(r)
        return self, new_r

    def traverse(self) -> typing.Iterator[Interval]:
        if self.left is not None:
            yield from self.left.traverse()
        yield self.interval
        if self.right is not None:
            yield from self.right.traverse()

    def has_interval(self, interval: Interval) -> bool:
        if interval == self.interval:
            return True
        if interval.r < self.interval.l - 1:
            return self.left is not None and self.left.has_interval(interval)
        if interval.l > self.interval.r + 1:
            return self.right is not None and self.right.has_interval(interval)
        return False

    def contains_interval(self, interval: Interval) -> bool:
        if interval in self.interval:
            return True
        if interval.r < self.interval.l - 1:
            return self.left is not None and self.left.contains_interval(interval)
        if interval.l > self.interval.r + 1:
            return self.right is not None and self.right.has_interval(interval)
        return False

    def contains_int(self, n: int) -> bool:
        if n < self.interval.l:
            return self.left is not None and self.left.contains_int(n)
        if n > self.interval.r:
            return self.right is not None and self.right.contains_int(n)
        return True


class Dis:
    """
    Disjoint interval set.
    """

    _root: _Node | None

    def __init__(self):
        self._root = None

    def add(self, interval: Interval):
        if self._root is None:
            self._root = _Node(interval)
            return
        self._root.union(interval)

    def __contains__(self, n: int):
        return self._root is not None and self._root.contains_int(n)

    def has(self, interval: Interval):
        return self._root is not None and self._root.has_interval(interval)

    def contains(self, interval: Interval):
        return self._root is not None and self._root.contains_interval(interval)

    def intervals(self) -> typing.Iterator[Interval]:
        if self._root is not None:
            yield from self._root.traverse()

    def ints(self) -> typing.Iterator[int]:
        if self._root is not None:
            for interval in self._root.traverse():
                yield from interval.ints()
