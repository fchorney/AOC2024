import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Optional, Sequence

from icecream import ic

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

    print(f"Solution 1: {delta}")


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

    print(f"Solution 2: {similarity_score}")


def parse_input(input_path: Path, solution: int = 1) -> LOCATIONS_TYPE:
    # This might change based on the solution asked for

    locations: LOCATIONS_TYPE = ([], [])
    with input_path.open() as f:
        for line in map(str.strip, f.readlines()):
            if not (match := re.match(r"(?P<first>\d+)\s+(?P<second>\d+)", line)):
                ic(f"Could not parse '{line}'")
                sys.exit(-1)
            locations[0].append(int(match.group("first")))
            locations[1].append(int(match.group("second")))
    return locations


def main(args: Optional[Sequence[str]] = None) -> int:
    pargs = parse_args(args)
    test = pargs.test
    solution = pargs.solution

    input_path = Path("input.txt")
    if test:
        input_path = Path(f"test_input_{test}.txt")

    print(f"Using Input File: {input_path}")
    print(f"Running Solution: {solution}")

    if not input_path.exists():
        print("Input file does not exist")
        return -1

    if pargs.quiet:
        ic.disable()

    if solution == 1:
        solution1(input_path)
    elif solution == 2:
        solution2(input_path)
    else:
        print(f"Solution [{solution}] doesn't exist")
        return -1

    return 0


def parse_args(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", type=int)
    parser.add_argument("-s", "--solution", type=int, default=1, choices=[1, 2])
    parser.add_argument("-q", "--quiet", action="store_true")

    return parser.parse_args(args)


if __name__ == "__main__":
    main()
