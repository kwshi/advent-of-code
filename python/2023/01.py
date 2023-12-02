from .. import ks
import typing

import math
import string
import re
import itertools as it
import bisect as bs
import functools as ft
import collections as co
import operator as op
import dataclasses as dc
import heapq as hq
import pprint as pp
import graphlib as gl

words = "one two three four five six seven eight nine".split()
decode = {
    **{word: i + 1 for i, word in enumerate(words)},
    **{str(n): n for n in range(10)},
}


def extract1(line: str):
    digits = re.findall(r"\d", line)
    return int(f"{digits[0]}{digits[-1]}")


def extract2(line: str):
    digits = re.findall(rf"(?=(\d|{'|'.join(words)}))", line)
    return int(f"{decode[digits[0]]}{decode[digits[-1]]}")


def part1(stdin: typing.TextIO):
    return sum(map(extract1, stdin))


def part2(stdin: typing.TextIO):
    return sum(map(extract2, stdin))
