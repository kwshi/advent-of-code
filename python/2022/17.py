from .. import ks
import typing

Shape = frozenset[ks.coord.Coord]

rocks = [
    frozenset(map(ks.coord.Coord, pts))
    for pts in [
        {(0, 0), (1, 0), (2, 0), (3, 0)},
        {(0, 1), (1, 1), (2, 1), (1, 0), (1, 2)},
        {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
        {(0, 0), (0, 1), (0, 2), (0, 3)},
        {(0, 0), (1, 0), (0, 1), (1, 1)},
    ]
]

displace = {">": ks.coord.Coord(1, 0), "<": ks.coord.Coord(-1, 0)}


def parse(stdin: typing.TextIO):
    return ks.parse.line(stdin)


def move(filled: set[ks.coord.Coord], shape: Shape, disp: ks.coord.Coord):
    new = frozenset(p + disp for p in shape)
    return new, all(0 <= p.x <= 6 and p.y > -1 and p not in filled for p in new)


def drop(
    prefilled: typing.Iterable[ks.coord.Coord], wind: str, until: int, i: int, w: int
):
    filled = {*prefilled}
    top = 1 + max((p.y for p in filled), default=-1)

    while i < until:
        rock = frozenset(p + (2, top + 3) for p in rocks[i % len(rocks)])
        while True:
            gust, w = wind[w], (w + 1) % len(wind)
            push, ok = move(filled, rock, displace[gust])
            rock = push if ok else rock
            fall, ok = move(filled, rock, ks.coord.Coord(0, -1))
            if not ok:
                break
            rock = fall

        top = max(top, max(p.y for p in rock) + 1)
        filled |= rock
        i += 1

    return top


def part1(stdin: typing.TextIO):
    return drop([], parse(stdin), 2022, 0, 0)


def move_detect(filled: dict[ks.coord.Coord, int], shape: Shape, disp: ks.coord.Coord):
    new = frozenset(p + disp for p in shape)
    return (
        new,
        all(0 <= p.x <= 6 and p.y > -1 for p in new),
        min((filled[p] for p in new if p in filled), default=None),
    )


def part2(stdin: typing.TextIO):
    filled: dict[ks.coord.Coord, int] = {}
    combos: dict[tuple[int, int], int] = {}
    hits: dict[int, int] = {}
    tops: dict[int, int] = {}
    prev: dict[int, int] = {}
    top = 0

    total = 1000000000000

    wind, i, w = parse(stdin), 0, 0
    while i < total:

        rock = frozenset(p + (2, top + 3) for p in rocks[i % len(rocks)])
        while True:
            gust, w = wind[w], (w + 1) % len(wind)

            push, ok, hit = move_detect(filled, rock, displace[gust])
            if hit is not None:
                hits[i] = hit
            rock = push if ok and hit is None else rock

            fall, ok, hit = move_detect(filled, rock, ks.coord.Coord(0, -1))
            if hit is not None:
                hits[i] = min(hits.get(i, hit), hit)
                break
            if not ok:
                hits[i] = 0
                break
            rock = fall

        top = max(top, max(p.y for p in rock) + 1)
        filled.update((p, i) for p in rock)
        i += 1

        tops[i] = top

        j, combos[key] = combos.get(key := (i % len(rocks), w)), i
        if j is None:
            continue

        prev[i] = j
        if (k := prev.get(j, None)) is None or any(hits[l] < k for l in range(j, i)):
            continue

        n = (total - i) // (i - j)
        return drop(
            {p + (0, n * (tops[i] - tops[j])) for p in filled},
            wind,
            1000000000000,
            i + n * (i - j),
            w,
        )

    return top
