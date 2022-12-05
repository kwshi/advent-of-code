# pyright: strict
import typing
import itertools

# many recipes taken from here with slight modification (e.g. better typing):
# <https://docs.python.org/3/library/itertools.html#itertools-recipes>

A = typing.TypeVar("A")


def grouper(
    iterable: typing.Iterable[A],
    n: int,
    *,
    incomplete: typing.Literal["fill", "strict", "ignore"] = "fill",
    fillvalue: A = None
) -> typing.Iterator[tuple[A, ...]]:
    """

    Groups elements in `iterable` into (disjoint, consecutive) runs of length
    `n`. The `incomplete` argument specifies what happens if `n` does not
    exactly divide the number of elements in `iterable`:

    - `"fill"`: pad the last group to length `n` using `fillvalue` (default `None`).
    - `"strict"`: raise a `ValueError`.
    - `"ignore"`: truncate remainder elements.

    ```python
    grouper('ABCDEFG', 3, fillvalue='x')       # -> ABC DEF Gxx
    grouper('ABCDEFG', 3, incomplete='strict') # -> ABC DEF ValueError
    grouper('ABCDEFG', 3, incomplete='ignore') # -> ABC DEF
    ```
    """
    iters = [iter(iterable)] * n
    match incomplete:
        case "fill":
            return itertools.zip_longest(*iters, fillvalue=fillvalue)
        case "strict":
            return zip(*iters, strict=True)
        case "ignore":
            return zip(*iters)
