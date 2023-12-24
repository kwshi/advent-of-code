from .. import ks
import typing

import z3

import itertools as it

import dataclasses as dc


@dc.dataclass(frozen=True)
class Particle:
    pos: ks.P2
    vel: ks.P2


def parse_p2(s: str):
    x, y, _ = map(int, s.split(", "))
    return ks.P2(x, y)


def parse_p3(s: str):
    x, y, z = map(int, s.split(", "))
    return x, y, z


def parse(stdin: typing.TextIO):
    for line in stdin:
        p, v = line.strip().split(" @ ")
        yield Particle(parse_p2(p), parse_p2(v))


def parse3(stdin: typing.TextIO):
    for line in stdin:
        p, v = line.strip().split(" @ ")
        yield parse_p3(p), parse_p3(v)


def intersect(p1: Particle, p2: Particle):
    assert p1.pos != p2.pos
    # if not p1.vel.cross(p2.vel):
    #    return None

    # p1 + v1 t = p2 + v2 s
    # v1 t - v2 s = p2 - p1
    #

    a, b, c, d = [p1.vel.x, -p2.vel.x, p1.vel.y, -p2.vel.y]
    x = p2.pos.x - p1.pos.x
    y = p2.pos.y - p1.pos.y

    det = a * d - b * c

    # assert det
    if not det:
        print("what")
        return None

    t = (d * x - b * y) / det
    s = (-c * x + a * y) / det

    if t < 0 or s < 0:
        return None  # past

    assert t
    assert s

    return p1.pos.x + t * p1.vel.x, p1.pos.y + t * p1.vel.y


@ks.func.sum
def part1(stdin: typing.TextIO):
    lower, upper = 7, 27
    lower, upper = 200000000000000, 400000000000000

    points = [*parse(stdin)]
    for p, q in it.combinations(points, 2):
        r = intersect(p, q)
        if not r:
            continue
        x, y = r

        if lower <= x <= upper and lower <= y <= upper:
            yield 1


def parallel2(u: tuple[int, int, int], v: tuple[int, int, int]):
    x, y, _ = u
    a, b, _ = v
    return x * b - y * a == 0


def parallel3(u: tuple[int, int, int], v: tuple[int, int, int]):
    a, b, c = ks.P3(u).cross(ks.P3(v))
    return a == b == c == 0


def part2(stdin: typing.TextIO):
    points = [*parse3(stdin)]

    # solving for x, y, z, vx, vy, vz, and tᵢ such that
    # for each particle i:
    #   x + vx * tᵢ = xᵢ + tᵢ * vxᵢ, etc.
    x, y, z, u, v, w = z3.Reals("x y z u v w")
    s = z3.Solver()
    for i, ((xi, yi, zi), (ui, vi, wi)) in enumerate(points):
        ti = z3.Real(f"t{i}")
        s.add(x + u * ti == xi + ui * ti)
        s.add(y + v * ti == yi + vi * ti)
        s.add(z + w * ti == zi + wi * ti)

    print(s.check())
    m = s.model()
    print(m)

    coords = m[x], m[y], m[z]
    return sum(c.as_long() for c in coords)
