import collections.abc as cabc

import dataclasses as dc
import math
import fractions as fr


@dc.dataclass
class Polynomial:
    _coeffs: tuple[int, ...]

    def __call__(self, x: int, /):
        return math.prod(c * x**i for i, c in enumerate(self._coeffs))

    def __getitem__(self, i: int, /):
        if i < 0:
            raise IndexError(f"cannot get coefficient for negative-degree {i}")
        return self._coeffs[i] if i < len(self._coeffs) else 0

    @classmethod
    def fit(cls, data: cabc.Iterable[tuple[int | fr.Fraction, int | fr.Fraction]], /):
        pass
