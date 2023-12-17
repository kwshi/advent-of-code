from ..point import P2

import typing
import collections.abc as cabc
import sys
import itertools


class Grid[T]:
    _data: list[T]

    _offset: int
    _step0: int
    _step1: int

    _size0: int

    def __init__(self, data: list[T], size0: int):
        self._data = data
        if len(data) % size0:
            raise ValueError(
                f"Grid `size0` {size0} does not evenly divide data length {len(data)}"
            )

        self._size0 = size0
        self._step0 = len(data) // size0
        self._step1 = 1
        self._offset = 0

    @property
    def shape(self):
        return P2(self.size0, self.size1)

    def _index(self, p: P2.Like):
        match p:
            case (i, j) | P2(i, j):
                if not (0 <= i < self.size0 and 0 <= j < self.size1):
                    raise IndexError(p)
                return self._offset + i * self._step0 + j * self._step1

    def keys(self, order: typing.Literal[0, 1] = 0) -> cabc.Iterator[P2]:
        match order:
            case 0:
                return (P2(i, j) for i in range(self.size0) for j in range(self.size1))
            case 1:
                return (P2(i, j) for j in range(self.size1) for i in range(self.size0))

    def values(self, order: typing.Literal[0, 1] = 0) -> cabc.Iterator[T]:
        return (self[p] for p in self.keys(order))

    def items(self, order: typing.Literal[0, 1] = 0) -> cabc.Iterator[tuple[P2, T]]:
        return ((p, self[p]) for p in self.keys(order))

    def find(self, value: T, order: typing.Literal[0, 1] = 0) -> P2 | None:
        for p, v in self.items(order):
            if v == value:
                return p

    def find_all(self, value: T, order: typing.Literal[0, 1] = 0) -> cabc.Iterator[P2]:
        for p, v in self.items(order):
            if v == value:
                yield p

    def __contains__(self, key: P2.Like):
        match key:
            case P2(i, j) | (i, j):
                return 0 <= i < self.size0 and 0 <= j < self.size1

    def _update_offset(self):
        self._offset = (self._step0 < 0) * (1 - self.size0) * self._step0 + (
            self._step1 < 0
        ) * (1 - self.size1) * self._step1

    def rot(self, n: int = 1):
        """
        starting from upright row-major m×n grid:
        rot0 index:      0,  n,  1, m
        rot1 index:    n-1, -1,  n, n
        rot2 index:   mn-1, -n, -1, m
        rot3 index: (m-1)n,  1, -n, n

        note: mn-1 = (m-1)n + (n-1).
        """
        match n % 4:
            case 1:
                self._size0 = self.size1
                self._step0, self._step1 = -self._step1, self._step0
                self._update_offset()
            case 2:
                self._step0, self._step1 = -self._step0, -self._step1
                self._update_offset()
            case 3:
                self._size0 = self.size1
                self._step0, self._step1 = self._step1, -self._step0
                self._update_offset()
            case _:
                pass
        return self

    def flip0(self):
        self._step0 = -self._step0
        self._update_offset()
        return self

    def flip1(self):
        self._step1 = -self._step1
        self._update_offset()
        return self

    def __getitem__(self, p: P2.Like):
        return self._data[self._index(p)]

    def __setitem__(self, p: P2.Like, value: T):
        self._data[self._index(p)] = value

    def transpose(self):
        self._step0, self._step1 = self._step1, self._step0
        self._size0 = self.size1
        self._update_offset()
        return self

    def transpose_anti(self):
        self.transpose()
        return self.rot(2)

    @property
    def size0(self):
        return self._size0

    @property
    def size1(self):
        return len(self._data) // self._size0

    def display(self, sep: str = "", file: typing.TextIO = sys.stdout):
        width = max(len(str(v)) for v in self._data)
        for i in range(self.size0):
            file.write(
                sep.join(str(self[i, j]).rjust(width) for j in range(self.size1))
            )
            file.write("\n")
        file.write("\n")
        file.flush()

    def iter0(self):
        return (self[i, j] for i in range(self.size0) for j in range(self.size1))

    def iter1(self):
        return (self[i, j] for j in range(self.size1) for i in range(self.size0))

    def clone(self):
        # return type(self)()
        pass


def from_lines(
    stdin: cabc.Iterable[str], split: str | None = None, rstrip: str = "\r\n"
):
    lines = (line.rstrip(rstrip) for line in stdin)
    lines = [line.split(split) for line in lines] if split is not None else [*lines]
    if not lines:
        raise ValueError("cannot read Grid from empty stdin")
    width = len(lines[0])
    for i, line in enumerate(lines):
        if len(line) != width:
            raise ValueError(
                "error while reading Grid from stdin: "
                f" first line has width {width}, but line {i} has width {len(line)}"
            )
    return Grid([*itertools.chain(*lines)], len(lines))


def blank[T](shape: int | P2.Like, value: T) -> Grid[T]:
    m, n = (shape, shape) if isinstance(shape, int) else shape
    return Grid([value] * (m * n), m)
