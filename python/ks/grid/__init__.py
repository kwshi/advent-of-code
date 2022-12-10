# pyright: strict

import typing

import sys
from .. import parse


__all__ = ["Key", "Grid", "from_rows", "parse_digits", "parse_chars"]

A = typing.TypeVar("A")

Key = tuple[int, int]


class RowKeys:
    _row: int
    _width: int
    _reverse: bool

    def __init__(self, row: int, width: int, reverse: bool):
        self._row = row
        self._width = width
        self._reverse = reverse

    def __len__(self) -> int:
        return self._width

    def __getitem__(self, j: int) -> Key:
        if not (0 <= j < self._width):
            raise IndexError(f"column {j} out of bounds (width {self._width})")
        return self._row, j

    def __contains__(self, pos: Key) -> bool:
        i, j = pos
        return i == self._row and 0 <= j < self._width

    def __iter__(self) -> typing.Iterator[Key]:
        cols = range(self._width - 1, -1, -1) if self._reverse else range(self._width)
        return ((self._row, j) for j in cols)

    def __reversed__(self) -> typing.Self:
        return RowKeys(self._row, self._width, not self._reverse)


class ColumnKeys:
    _column: int
    _height: int
    _reverse: bool

    def __init__(self, column: int, height: int, reverse: bool):
        self._column = column
        self._height = height
        self._reverse = reverse

    def __len__(self) -> int:
        return self._height

    def __getitem__(self, i: int) -> Key:
        if not (0 <= i < self._height):
            raise IndexError(f"row {i} out of bounds (height {self._height})")
        return i, self._height

    def __contains__(self, pos: Key) -> bool:
        i, j = pos
        return j == self._column and 0 <= i < self._height

    def __iter__(self) -> typing.Iterator[Key]:
        rows = range(self._height - 1, -1, -1) if self._reverse else range(self._height)
        return ((i, self._column) for i in rows)

    def __reversed__(self) -> typing.Self:
        return ColumnKeys(self._column, self._height, not self._reverse)


class Keys:
    _height: int
    _width: int

    def __init__(self, height: int, width: int):
        self._height = height
        self._width = width

    def __len__(self) -> int:
        return self._height * self._width

    def __contains__(self, pos: Key) -> bool:
        i, j = pos
        return 0 <= i < self._height and 0 <= j < self._width

    def __iter__(self) -> typing.Iterator[Key]:
        for i in range(self._height):
            for j in range(self._width):
                yield i, j


class Values(typing.Generic[A]):
    _values: list[A]

    def __init__(self, values: list[A]):
        self._values = values

    def __len__(self) -> int:
        return len(self._values)

    def __contains__(self, value: A) -> bool:
        return value in self._values

    def __iter__(self) -> typing.Iterator[A]:
        return iter(self._values)


class Grid(typing.Generic[A]):
    _values: list[A]
    _height: int
    _width: int

    def __init__(self, values: typing.Iterable[A], height: int, width: int):
        self._values = [*values]
        self._height = height
        self._width = width

        if height * width != len(self._values):
            raise ValueError(
                f"attempted to initialize grid with invalid dimensions ({height} * {width} != {len(self._values)})"
            )

    @property
    def dimensions(self) -> tuple[int, int]:
        return self._height, self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    def _index(self, pos: Key) -> int:
        i, j = pos
        return i * self._width + j

    def __len__(self) -> int:
        return self._height * self._width

    def __getitem__(self, pos: Key) -> A:
        if not pos in self:
            raise IndexError(
                f"grid index {pos} out of bounds (dimensions {self.dimensions})"
            )
        return self._values[self._index(pos)]

    def __setitem__(self, pos: Key, value: A) -> None:
        if not pos in self:
            raise IndexError(
                f"grid index {pos} out of bounds (dimensions {self.dimensions})"
            )
        self._values[self._index(pos)] = value

    def __contains__(self, pos: Key) -> bool:
        i, j = pos
        return 0 <= i < self._height and 0 <= j < self._width

    def row_keys(self, i: int, *, reverse: bool = False) -> RowKeys:
        if not (0 <= i < self._height):
            raise IndexError(f"row {i} out of bounds (height {self.height})")
        return RowKeys(i, self._width, reverse)

    def column_keys(self, j: int, *, reverse: bool = False) -> ColumnKeys:
        if not (0 <= j < self._width):
            raise IndexError(f"column {j} out of bounds (width {self.width})")
        return ColumnKeys(j, self._height, reverse)

    def ray_keys(
        self, start: Key, offset: tuple[int, int], *, include_start: bool = True
    ) -> typing.Iterator[Key]:
        i, j = start
        di, dj = offset
        if not include_start:
            i += di
            j += dj
        while 0 <= i < self._height and 0 <= j < self._width:
            yield i, j
            i += di
            j += dj

    def rays_keys(
        self, start: Key, *, include_start: bool = True, diagonal: bool = False
    ) -> typing.Iterator[typing.Iterator[Key]]:
        offsets = (
            [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
            if diagonal
            else [(1, 0), (0, 1), (-1, 0), (0, -1)]
        )
        return (
            self.ray_keys(start, offset, include_start=include_start)
            for offset in offsets
        )

    def neighbor_keys(
        self, pos: Key, *, diagonal: bool = False
    ) -> typing.Iterator[Key]:
        i, j = pos
        neighbors = (
            [
                (i + 1, j),
                (i + 1, j + 1),
                (i, j + 1),
                (i - 1, j + 1),
                (i - 1, j),
                (i - 1, j - 1),
                (i, j - 1),
                (i + 1, j - 1),
            ]
            if diagonal
            else [(i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1)]
        )
        return (p for p in neighbors if p in self)

    def keys(self) -> Keys:
        return Keys(self._height, self._width)

    def values(self) -> Values[A]:
        return Values(self._values)

    def items(self) -> typing.Iterator[tuple[Key, A]]:
        return (
            ((k // self._height, k % self._width), value)
            for k, value in enumerate(self._values)
        )

    def render(
        self,
        *,
        render_cell: typing.Callable[[A], str] = str,
        out: typing.TextIO = sys.stderr,
    ) -> None:
        # TODO: add options to customize display to make it more readable
        # TODO: automatic OCR :)
        max_width = max(len(render_cell(c)) for c in self._values)
        sep = "" if max_width == 1 else " "
        for i in range(self._height):
            out.write(
                sep.join(
                    map(
                        render_cell,
                        self._values[i * self._width : (i + 1) * self._width],
                    )
                )
            )
            out.write("\n")
        out.flush()


def from_constant(value: A, height: int, width: int) -> Grid[A]:
    return Grid([value] * (height * width), height, width)


def from_rows(rows: typing.Iterable[typing.Iterable[A]]) -> Grid[A]:
    values: list[A] = []
    height = 0
    width = None
    for row in rows:
        height += 1
        last_len = len(values)
        values.extend(row)
        row_width = len(values) - last_len
        if width is None:
            width = row_width
        elif width != row_width:
            raise ValueError(
                f"inconsistent row lengths; expecting {width} but got {row_width}"
            )
    return Grid(values, height, width or 0)


def parse_digits(stdin: typing.TextIO):
    return from_rows(map(int, line) for line in parse.lines(stdin))


def parse_chars(stdin: typing.TextIO):
    return from_rows(parse.lines(stdin))
