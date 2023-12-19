from .. import ks
import typing

import math
import re
import itertools as it
import dataclasses as dc


type Item = dict[str, int]
type Op = typing.Literal["<", ">"]
type Rule = tuple[Condition | None, str]


@dc.dataclass
class Condition:
    name: str
    operator: Op
    value: int


@dc.dataclass
class Workflow:
    name: str
    rules: list[Rule]


def parse(stdin: typing.TextIO):
    top, bottom = stdin.read().strip().split("\n\n")
    bottom.split("\n")

    workflows = dict[str, Workflow]()
    for line in top.strip().split("\n"):
        i = line.index("{")  # }
        name = line[:i]
        rest = line[i:].strip("{}").split(",")
        rules = list[Rule]()
        for term in rest:
            if ":" in term:
                left, right = term.split(":")
                m = re.fullmatch(r"(\w+)([<>])(\d+)", left)
                assert m is not None
                var, op, val = m.groups()
                condition = Condition(var, typing.cast(Op, op), int(val))
                rules.append((condition, right))
            else:
                # unconditional
                rules.append((None, term))
        workflows[name] = Workflow(name, rules)

    items = list[Item]()
    for line in bottom.strip().split("\n"):
        mapping = dict(k.split("=") for k in line.strip("{}").split(","))
        mapping = {k: int(v) for k, v in mapping.items()}
        items.append(mapping)

    return workflows, items


def evaluate(condition: Condition, item: Item):
    match condition.operator:
        case "<":
            return item[condition.name] < condition.value
        case ">":
            return item[condition.name] > condition.value


def run(item: Item, workflows: dict[str, Workflow]):
    current = "in"
    while True:
        workflow = workflows[current]
        for condition, target in workflow.rules:
            if condition is None:
                current = target
                break
            if evaluate(condition, item):
                current = target
                break

        if current == "A":
            return True
        elif current == "R":
            return False


@ks.func.sum
def part1(stdin: typing.TextIO):
    workflows, items = parse(stdin)

    for item in items:
        if run(item, workflows):
            yield sum(item.values())


@dc.dataclass(frozen=True)
class State:
    workflow: str
    constraints: tuple[ks.Interval, ks.Interval, ks.Interval, ks.Interval]


def apply(condition: Condition, cs: dict[str, ks.Interval]):
    cs = {**cs}
    match condition.operator:
        case "<":
            cs[condition.name] = cs[condition.name].truncate(r=condition.value - 1)
        case ">":
            cs[condition.name] = cs[condition.name].truncate(l=condition.value + 1)
    return cs


def negate(condition: Condition):
    match condition.operator:
        case "<":
            return Condition(condition.name, ">", condition.value - 1)
        case ">":
            return Condition(condition.name, "<", condition.value + 1)


def collect(c: dict[str, ks.Interval]):
    return (c["x"], c["m"], c["a"], c["s"])


type CC = tuple[
    ks.Interval,
    ks.Interval,
    ks.Interval,
    ks.Interval,
]


@ks.func.sum
def part2(stdin: typing.TextIO):
    workflows, _ = parse(stdin)

    start = State(
        "in",
        (
            ks.Interval(1, 4000),
            ks.Interval(1, 4000),
            ks.Interval(1, 4000),
            ks.Interval(1, 4000),
        ),
    )
    frontier = [start]
    seen = {start}
    accepting = set[CC]()
    while frontier:
        current = frontier.pop()
        if current.workflow == "A":
            accepting.add(current.constraints)
            continue
        elif current.workflow == "R":
            continue
        workflow = workflows[current.workflow]
        x, m, a, s = current.constraints
        constraints = {"x": x, "m": m, "a": a, "s": s}
        candidates = list[State]()
        for condition, target in workflow.rules:
            if not condition:
                candidates.append(
                    State(
                        target,
                        collect(constraints),
                    )
                )
                break
            candidates.append(State(target, collect(apply(condition, constraints))))
            constraints = apply(negate(condition), constraints)

        for candidate in candidates:
            assert candidate not in seen
            frontier.append(candidate)

    for p, q in it.combinations(accepting, 2):
        assert any((i & j) is None for i, j in zip(p, q))

    for p in accepting:
        yield math.prod((i.r - i.l + 1) for i in p)
        pass
