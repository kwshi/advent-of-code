import typing
import sys
import collections.abc as cabc
import fractions as fr

from .permutation import Permutation


class FracMatrix:
    _data: list[fr.Fraction]
    _nrows: int

    def __init__(self, data: cabc.Iterable[int | fr.Fraction], nrows: int):
        self._data = [*map(fr.Fraction, data)]
        self._nrows = nrows
        if len(self._data) % self._nrows:
            raise ValueError(
                f"bad matrix row count:"
                f" data length {len(self._data)},"
                f" row count {self._nrows}"
            )

    @classmethod
    def identity(cls, n: int, /):
        return cls([int(i == j) for i in range(n) for j in range(n)], n)

    @property
    def nrows(self):
        return self._nrows

    @property
    def ncols(self):
        return len(self._data) // self._nrows

    @property
    def shape(self):
        return (self.nrows, self.ncols)

    def _index(self, p: tuple[int, int]):
        i, j = p
        return i * self.ncols + j

    def _check_bounds(self, p: tuple[int, int]):
        i, j = p
        if not (0 <= i < self.nrows and 0 <= j < self.ncols):
            raise IndexError(p)

    def __getitem__(self, p: tuple[int, int]):
        self._check_bounds(p)
        return self._data[self._index(p)]

    def __setitem__(self, p: tuple[int, int], value: int | fr.Fraction):
        self._check_bounds(p)
        self._data[self._index(p)] = fr.Fraction(value)

    def row_add(self, i1: int, i2: int, s: int | fr.Fraction = 1):
        """
        row operation of the form `r₁↦r₁+s⋅r₂`.
        """
        if not s:
            return
        for j in range(self.ncols):
            self[i1, j] += s * self[i2, j]
        return self

    def row_scale(self, i: int, s: int | fr.Fraction):
        """
        row operation of the form `r₁↦s⋅r₁`.
        """
        if s == 1:
            return
        for j in range(self.ncols):
            self[i, j] *= s
        return self

    def row_swap(self, i1: int, i2: int):
        """
        swap rows at `i₁` and `i₂`.
        """
        if i1 == i2:
            return
        for j in range(self.ncols):
            self[i1, j], self[i2, j] = self[i2, j], self[i1, j]
        return self

    def __matmul__(self, other: typing.Self):
        if self.ncols != other.nrows:
            raise ValueError(
                f"matrix multiplication size mismatch: {self.shape} and {other.shape}"
            )
        return type(self)(
            (
                sum(self[i, k] * other[k, j] for k in range(self.ncols))
                for i in range(self.nrows)
                for j in range(other.ncols)
            ),
            self.nrows,
        )

    def factor_lup(self):
        lower = self.identity(self.nrows)
        upper = self.clone()
        perm = Permutation(self.nrows)
        row = col = 0
        while row < upper.nrows and col < upper.ncols:
            leading = 0
            pivot = None
            for p in range(row, upper.nrows):
                if leading := upper[p, col]:
                    pivot = p
                    break
            if pivot is None:
                col += 1
                continue
            perm.swap_after(row, pivot)
            upper.row_swap(row, pivot)

            assert leading

            for k in range(row + 1, upper.nrows):
                scale = upper[k, col] / leading
                lower[k, row] = scale
                upper.row_add(k, row, -scale)
            row += 1

        return lower, upper, perm

    def solve_lup(self, out: typing.Self):
        """
        TODO: deal with non-rectangular matrices? in particular wide, underdetermined systems.
        """
        if self.nrows != out.nrows:
            raise ValueError(
                f"solve system size mismatch:"
                f" coeff nrows={self.nrows}, out nrows={out.nrows}"
            )
        l, u, p = self.factor_lup()
        if any(not u[i, i] for i in range(self.nrows)):
            raise ZeroDivisionError(f"matrix is singular")
        out = out.clone().permute_rows(p)
        for i in range(1, self.nrows):
            for j in range(i):
                out.row_add(i, j, -l[i, j])
        for i in range(self.nrows - 1, -1, -1):
            for j in range(i + 1, self.nrows):
                out.row_add(i, j, -u[i, j])
            out.row_scale(i, 1 / u[i, i])
        return out

    def permute_rows(self, perm: Permutation, invert: bool = False):
        if len(perm) != self.nrows:
            raise ValueError(
                f"row permutation size mismatch:"
                f" nrows={self.nrows}, len(perm)={len(perm)}"
            )
        for j in range(self.ncols):
            replace = [self[perm(i, invert=not invert), j] for i in range(self.nrows)]
            for i, c in enumerate(replace):
                self[i, j] = c
        return self

    def clone(self):
        return type(self)([*self._data], self._nrows)

    def display(self, file: typing.TextIO = sys.stdout):
        width = max(len(str(c)) for c in self._data)
        for i in range(self.nrows):
            file.write(
                " ".join(str(self[i, j]).rjust(width, " ") for j in range(self.ncols))
            )
            file.write("\n")
        file.write("\n")
        file.flush()

    def __eq__(self, other: typing.Self):
        return self.shape == other.shape and self._data == other._data
