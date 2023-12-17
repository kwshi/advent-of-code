from .. import ks
import typing

import dataclasses as dc
import heapq as hq
import pprint as pp


def parse(stdin: typing.TextIO):
    grid = ks.grid.from_lines(stdin)
    intgrid = ks.grid.blank(grid.shape, 0)
    for p, v in grid.items():
        intgrid[p] = int(v)
    return intgrid


@dc.dataclass(frozen=True)
class Node:
    position: ks.P2
    facing: ks.P2
    count: int


@dc.dataclass(frozen=True)
class Entry:
    cost: int
    node: Node
    parent: Node | None

    def __lt__(self, other: typing.Self):
        return self.cost < other.cost


def part(min_straight: int, max_straight: int):
    def solve(stdin: typing.TextIO):
        grid = parse(stdin)
        dest = grid.shape - 1

        done = dict[Node, Node | None]()
        frontier: list[Entry] = [Entry(0, Node(ks.P2(), ks.P2(0, 1), 0), None)]
        while frontier:
            current = hq.heappop(frontier)
            if current.node in done:
                continue
            done[current.node] = current.parent
            if current.node.position == dest and current.node.count >= min_straight:
                print(current.node)
                path = [(node := current.node)]
                while True:
                    prev = done[node]
                    if prev is None:
                        break
                    path.append(node := prev)
                pp.pprint(path)
                return current.cost

            candidates = list[ks.P2]()
            if current.node.count < max_straight:
                # can move forward
                candidates.append(current.node.facing)
            if min_straight <= current.node.count:
                # can turn
                candidates.append(current.node.facing.rot(1))
                candidates.append(current.node.facing.rot(-1))
            for facing in candidates:
                pos = current.node.position + facing
                count = 1 + (facing == current.node.facing) * current.node.count
                node = Node(pos, facing, count)
                if pos not in grid or node in done:
                    continue
                hq.heappush(
                    frontier, Entry(current.cost + grid[pos], node, current.node)
                )

    return solve


part1 = part(0, 3)
part2 = part(4, 10)
