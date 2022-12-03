# pyright: strict
from .. import ks
import typing

import math
import collections as co
import dataclasses as dc

import re

re_log = re.compile(r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.*)")
re_start = re.compile(r"Guard #(\d+) begins shift")


@dc.dataclass(order=True, frozen=True)
class Timestamp:
    year: int
    month: int
    day: int
    hour: int
    minute: int

    def minutes(self):
        return self.hour * 60 + self.minute


Interval = tuple[Timestamp, Timestamp]


def parse(stdin: typing.TextIO):
    entries: list[tuple[Timestamp, str]] = []

    for line in ks.parse.lines(stdin):
        match = re_log.fullmatch(line)
        assert match

        *times, msg = match.groups()
        timestamp = Timestamp(*map(int, times))
        entries.append((timestamp, msg))

    entries.sort()

    records: co.defaultdict[int, list[Interval]] = co.defaultdict(list)
    guard = None
    asleep = None
    for timestamp, msg in entries:
        match_start = re_start.match(msg)
        if match_start:
            guard = int(match_start.group(1))
            assert asleep is None
            continue

        assert guard is not None
        match msg:
            case "falls asleep":
                asleep = timestamp
            case "wakes up":
                assert asleep is not None
                records[guard].append((asleep, timestamp))
                asleep = None
            case _:
                assert False, f"invalid update {msg!r}"
    return records


def tally(intervals: list[Interval]):
    endpoints: list[tuple[int, bool]] = []
    for sleep, wake in intervals:
        endpoints.append((sleep.minutes(), True))
        endpoints.append((wake.minutes(), False))
    endpoints.sort()

    count = 0
    for time, status in endpoints:
        count += 2 * status - 1
        yield time, count


def part1(stdin: typing.TextIO):
    records = parse(stdin)

    counts: co.defaultdict[int, int] = co.defaultdict(int)
    for guard, intervals in records.items():
        for sleep, wake in intervals:
            counts[guard] += wake.minutes() - sleep.minutes()
    sleepiest = max(counts.keys(), key=counts.__getitem__)

    times = dict(tally(records[sleepiest]))
    return sleepiest * max(times, key=times.__getitem__)


def part2(stdin: typing.TextIO):
    records = parse(stdin)

    overall: dict[tuple[int, int], int] = {}
    for guard, intervals in records.items():
        for time, count in tally(intervals):
            overall[guard, time] = count

    return math.prod(max(overall, key=overall.__getitem__))
