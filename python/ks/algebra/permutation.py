import typing
import collections.abc as cabc


class Permutation:
    _perm: list[int]
    _inv: list[int]

    def __init__(self, len_or_perm: int | cabc.Iterable[int]):
        match len_or_perm:
            case int():
                perm = [*range(len_or_perm)]
                inv = [*perm]
            case _:
                perm = [*len_or_perm]
                inv = [0] * len(perm)
                for i, j in enumerate(perm):
                    inv[j] = i
                if {*perm} != {*range(len(perm))}:
                    raise ValueError(
                        f"constructing permutation with a non-bijection: {perm}"
                    )
        object.__setattr__(self, "_perm", perm)
        object.__setattr__(self, "_inv", inv)

    @classmethod
    def identity(cls, n: int):
        return cls(range(n))

    def invert(self):
        self._perm, self._inv = self._inv, self._perm

    def clone(self):
        return Permutation(self._perm)

    def sign(self):
        raise ValueError("TODO")

    def swap_before(self, i: int, j: int):
        """
        i ↦ j ↦ π(j), j ↦ i ↦ π(i)
        inverse: π(j) ↦ i, π(i) ↦ j
        """
        x, y = self._perm[i], self._perm[j]
        self._perm[i], self._perm[j] = y, x
        self._inv[x], self._inv[y] = j, i
        return self

    def swap_after(self, i: int, j: int):
        """
        π(x) = i ↦ j, π(y) = j ↦ i
        inverse: j ↦ x, i ↦ y
        """
        x, y = self._inv[i], self._inv[j]
        self._perm[x], self._perm[y] = j, i
        self._inv[i], self._inv[j] = y, x
        return self

    def __eq__(self, other: typing.Self):
        return self._perm == other._perm

    def __matmul__(self, other: typing.Self):
        if len(self) != len(other):
            raise ValueError(
                f"cannot compose permutations of different sizes:"
                f" {len(self)} and {len(other)}"
            )
        return type(self)(self(other(i)) for i in range(len(self)))

    def __len__(self):
        return len(self._perm)

    def __call__(self, i: int, invert: bool = False):
        return (self._inv if invert else self._perm)[i]
