# pyright: strict
from .. import ks
import typing

import math
import functools as ft
import dataclasses as dc


@dc.dataclass()
class Blueprint:
    index: int
    ore_ore: int
    clay_ore: int
    obs_ore: int
    obs_clay: int
    geode_ore: int
    geode_obs: int

    @ft.cached_property
    def max_ore(self) -> int:
        return max(self.ore_ore, self.clay_ore, self.obs_ore, self.geode_ore)


@dc.dataclass(frozen=True, kw_only=True)
class State:
    time: int
    ore: int = dc.field(default=0)
    clay: int = dc.field(default=0)
    obs: int = dc.field(default=0)
    bot_ore: int = dc.field(default=1)
    bot_clay: int = dc.field(default=0)
    bot_obs: int = dc.field(default=0)
    bot_geode: int = dc.field(default=0)

    def step(self) -> typing.Self:
        return dc.replace(
            self,
            time=self.time - 1,
            ore=self.ore + self.bot_ore,
            clay=self.clay + self.bot_clay,
            obs=self.obs + self.bot_obs,
        )

    def ore_cap(self, bp: Blueprint) -> int:
        return bp.max_ore + (self.time - 1) * (bp.max_ore - self.bot_ore)

    def clay_cap(self, bp: Blueprint) -> int:
        return bp.obs_clay + (self.time - 1) * (bp.obs_clay - self.bot_clay)

    def obs_cap(self, bp: Blueprint) -> int:
        return bp.geode_obs + (self.time - 1) * (bp.geode_obs - self.bot_obs)

    def cap(self, bp: Blueprint) -> typing.Self:

        """

        for each remaining round, we spend at most `bp.max_ore` ore and produce
        at least `self.bot_ore` ore. in other words, each round, we lose at most
        `bp.max_ore-self.bot_ore`.

        """

        return dc.replace(
            self,
            time=self.time,
            ore=min(self.ore, self.ore_cap(bp)),
            clay=min(self.clay, self.clay_cap(bp)),
            obs=min(self.obs, self.obs_cap(bp)),
        )

    def options(self, bp: Blueprint):
        yield (step := self.step()).cap(bp)

        if (
            self.time >= 8
            and self.bot_ore < bp.max_ore
            and bp.ore_ore <= self.ore
            and self.ore < self.ore_cap(bp)
        ):
            yield dc.replace(
                step, ore=step.ore - bp.ore_ore, bot_ore=self.bot_ore + 1
            ).cap(bp)

        if (
            self.time >= 6
            and self.bot_clay < bp.obs_clay
            and bp.clay_ore <= self.ore
            and self.clay < self.clay_cap(bp)
        ):
            yield dc.replace(
                step, ore=step.ore - bp.clay_ore, bot_clay=self.bot_clay + 1
            ).cap(bp)

        if (
            self.time >= 4
            and self.bot_obs < bp.geode_obs
            and bp.obs_ore <= self.ore
            and bp.obs_clay <= self.clay
            and self.obs < self.obs_cap(bp)
        ):
            yield dc.replace(
                step,
                ore=step.ore - bp.obs_ore,
                clay=step.clay - bp.obs_clay,
                bot_obs=self.bot_obs + 1,
            ).cap(bp)

        if self.time >= 2 and bp.geode_ore <= self.ore and bp.geode_obs <= self.obs:
            yield dc.replace(
                step,
                ore=step.ore - bp.geode_ore,
                obs=step.obs - bp.geode_obs,
                bot_geode=self.bot_geode + 1,
            ).cap(bp)


def parse(stdin: typing.TextIO):
    for n, ore, clay, oo, oc, gore, gobs in ks.parse.lines_pattern(
        stdin,
        "Blueprint %u: Each ore robot costs %u ore. "
        "Each clay robot costs %u ore. "
        "Each obsidian robot costs %u ore and %u clay. "
        "Each geode robot costs %u ore and %u obsidian.",
    ):
        yield Blueprint(n, ore, clay, oo, oc, gore, gobs)


def search(bp: Blueprint, total: int):
    @ft.cache
    def go(s: State) -> int:
        if s.time == 0:
            return 0
        if s.time == 1:
            return s.bot_geode
        if s.time == 2:
            return 2 * s.bot_geode + (s.ore >= bp.geode_ore and s.obs >= bp.geode_obs)
        return s.bot_geode + max(map(go, s.options(bp)))

    print(bp.index)
    return go(State(time=total))


def part1(stdin: typing.TextIO):
    return sum(bp.index * search(bp, 24) for bp in parse(stdin))


def part2(stdin: typing.TextIO):
    bps = parse(stdin)
    return math.prod(search(next(bps), 32) for _ in range(3))
