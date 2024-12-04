import re
import sys
from collections import Counter
from pathlib import Path

from icecream import ic

from libaoc import solve

LOCATIONS_TYPE = tuple[list[int], list[int]]


def solution1(input_path: Path) -> None:
    locations = parse_input(input_path)

    # Sort both lists
    locations[0].sort()
    locations[1].sort()

    delta = 0
    idx_b = 0
    for loc_a in locations[0]:
        loc_b = locations[1][idx_b]
        ic(loc_a, loc_b, abs(loc_b - loc_a))
        delta += abs(loc_b - loc_a)
        idx_b += 1

    print(f'Solution 1: {delta}')


def solution2(input_path: Path) -> None:
    locations = parse_input(input_path)

    # Sort both lists
    locations[0].sort()
    locations[1].sort()

    # Make a mapping of each number in the 2nd list and how often it appears
    count_map = Counter(locations[1])

    similarity_score = 0
    for loc_a in locations[0]:
        count = count_map.get(loc_a, 0)
        similarity_score += loc_a * count

    print(f'Solution 2: {similarity_score}')


def parse_input(input_path: Path) -> LOCATIONS_TYPE:
    locations: LOCATIONS_TYPE = ([], [])
    with input_path.open() as f:
        for line in map(str.strip, f.readlines()):
            if not (match := re.match(r'(?P<first>\d+)\s+(?P<second>\d+)', line)):
                ic(f"Could not parse '{line}'")
                sys.exit(-1)
            locations[0].append(int(match.group('first')))
            locations[1].append(int(match.group('second')))
    return locations


if __name__ == '__main__':
    solve(solution1, solution2)
