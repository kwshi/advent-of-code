import sys
import collections as co


def part1():
    twos = threes = 0
    for line in sys.stdin:
        counts = {*co.Counter(line.rstrip()).values()}
        twos += 2 in counts
        threes += 3 in counts
    return twos * threes


def part2():
    words = [word.rstrip() for word in sys.stdin]
    for i in range(len(words[0])):
        seen = set()
        for word in words:
            chop = word[:i] + word[i + 1 :]
            if chop in seen:
                return chop
            seen.add(chop)
