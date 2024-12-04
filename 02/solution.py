from pathlib import Path
from typing import Any

from icecream import ic

from libaoc import solve


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
    print(f'Solution 1: {safe}')


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

    print(f'Solution 2: {safe}')


def parse_input(input_path: Path) -> Any:
    reports: list[list[int]] = []
    with input_path.open() as f:
        for line in map(str.strip, f.readlines()):
            reports.append(list(map(int, line.split(' '))))
    return reports


if __name__ == '__main__':
    solve(solution1, solution2)
