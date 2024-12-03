import argparse
from pathlib import Path
from typing import Any, Optional, Sequence

from icecream import ic


def is_safe(report: list[int]) -> bool:
    prev, curr = report[0:2]

    # If curr and prev are the same, this is unsafe
    if curr == prev:
        return False

    # Check if we are increasing or decreasing
    increasing = curr > prev

    idx = 2
    r_len = len(report)
    while (idx <= r_len) and ((increasing and curr > prev) or (not increasing and curr < prev)):
        delta = abs(curr - prev)
        if delta < 1 or delta > 3:
            return False

        if idx < r_len:
            prev = curr
            curr = report[idx]
        idx += 1

    if idx <= r_len:
        return False

    ic(report)
    return True


def solution1(input_path: Path) -> None:
    reports = parse_input(input_path)
    safe = sum(1 for report in reports if is_safe(report))
    print(f"Solution 1: {safe}")


def solution2(input_path: Path) -> None:
    reports = parse_input(input_path)

    safe = 0
    for report in reports:
        # If this report is traditionally safe, just add it to the list
        if is_safe(report):
            safe += 1
            continue

        # Systematically remove 1 level from each report to see if it's safe
        # If it ever returns as safe, then we're safe, else if we exhaust the levels
        # with no safe return, then the report was unsafe.
        idx = 0
        r_len = len(report)
        while idx < r_len:

            if is_safe(report[0:idx] + report[idx + 1 :]):
                safe += 1
                break

            idx += 1

    print(f"Solution 2: {safe}")


def parse_input(input_path: Path, solution: int = 1) -> Any:
    reports: list[list[int]] = []
    with input_path.open() as f:
        for line in map(str.strip, f.readlines()):
            reports.append(list(map(int, line.split(" "))))
    return reports


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
