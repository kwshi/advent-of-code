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


def parse(stdin: typing.TextIO):
    return map(int, ks.parse.lines(stdin))


@dc.dataclass
class Node:
    value: int
    left: typing.Self
    right: typing.Self

    def __init__(self, value: int):
        self.value = value
        self.left = self
        self.right = self

    def append()


def part1(stdin: typing.TextIO):
    nums = [*parse(stdin)]
    nodes = []
    for n in nums:
        if not nodes:
            node = Node(n, None, None)
            node.left = node
            node.right = node
            nodes.append(node)
            continue

        node = Node(n, nodes[-1], nodes[0])
        nodes[-1].right = node
        nodes[0].left = node
        nodes.append(node)

    zero = None
    for node in nodes:
        if node.value > 0:
            for _ in range(node.value):
                r = node.right
                node.left.right = r
                r.left = node.left
                r.right.left = node
                node.right = r.right
                r.right, node.left = node, r
        elif node.value < 0:
            for _ in range(-node.value):
                l = node.left
                node.right.left = l
                l.right = node.right
                l.left.right = node
                node.left = l.left
                node.right, l.left = l, node
        else:
            zero = node

    s = 0
    node = zero
    for _ in range(3):
        for _ in range(1000):
            node = node.right
        s += node.value

    return s


def part2(stdin: typing.TextIO):
    decryption = 811589153

    nums = [*parse(stdin)]
    nodes = []
    for n in nums:
        if not nodes:
            node = Node(n * decryption, None, None)
            node.left = node
            node.right = node
            nodes.append(node)
            continue

        node = Node(n * decryption, nodes[-1], nodes[0])
        nodes[-1].right = node
        nodes[0].left = node
        nodes.append(node)

    zero = None
    for _ in range(10):
        for node in nodes:
            moves = node.value % (len(nodes) - 1)
            if moves > 0:
                for _ in range(moves):
                    r = node.right
                    node.left.right = r
                    r.left = node.left
                    r.right.left = node
                    node.right = r.right
                    r.right, node.left = node, r
            elif moves < 0:
                for _ in range(-moves):
                    l = node.left
                    node.right.left = l
                    l.right = node.right
                    l.left.right = node
                    node.left = l.left
                    node.right, l.left = l, node
            else:
                zero = node
    s = 0
    node = zero
    for _ in range(3):
        for _ in range(1000):
            node = node.right
        s += node.value
    return s
