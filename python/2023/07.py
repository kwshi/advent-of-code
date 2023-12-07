from .. import ks
import typing

import enum
import collections as co



class CardType(enum.Enum):
    FIVE = 6
    FOUR = 5
    HOUSE = 4
    THREE = 3
    PAIR2 = 2
    PAIR1 = 1
    HIGH = 0




def classify1(card: str):
    counts = co.Counter(card)
    match sorted(counts.values(), reverse=True):
        case [5]: return CardType.FIVE
        case [4, 1]: return CardType.FOUR
        case [3, 2]: return CardType.HOUSE
        case [3, 1, 1]: return CardType.THREE
        case [2, 2, 1]: return CardType.PAIR2
        case [2, 1, 1, 1]: return CardType.PAIR1
        case [1, 1, 1, 1, 1]: return CardType.HIGH
        case p: assert False, p



def classify2(card: str):
    counts = co.Counter(card)
    j = counts.pop('J', 0)
    match (sorted(counts.values(), reverse=True), j):
        case ([], 5) | ([5], 0) | ([_],_):
            return CardType.FIVE
        case ([4, 1], 0) | ([_, 1], _):
            return CardType.FOUR
        case ([3, 2], 0) | ([2, 2], 1):
            return CardType.HOUSE
        case ([_, 1, 1], _):
            return CardType.THREE
        case ([2, 2, 1], 0):
            return CardType.PAIR2
        case ([_, 1, 1, 1], _):
            return CardType.PAIR1
        case ([1, 1, 1, 1, 1], 0):
            return CardType.HIGH
        case p:
            assert False, p


def parse(stdin: typing.TextIO):
    for line in stdin:
        a, b = line.strip().split()
        yield a, int(b)


def make(strength: list[str], classify: typing.Callable[[str],CardType]):
    def tiebreaker(card: str):
        return (*(-strength.index(c) for c in card),)
    def score(pair: tuple[str, int]):
        card, _ = pair
        return classify(card).value, tiebreaker(card)
    def solve(stdin: typing.TextIO):
        cards = sorted(parse(stdin), key=score)
        return sum((i+1)*n for i, (_, n) in enumerate(cards))
    return solve

strength1 = 'A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2'.split(', ')
strength2 = [*strength1]
strength2.remove('J')
strength2.append('J')

part1 = make(strength1, classify1)
part2 = make(strength2, classify2)
