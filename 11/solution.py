from collections import Counter, defaultdict
from functools import cache
from pathlib import Path

from libaoc import solve

STONE_T: type = list[int]


def solution1(input_path: Path) -> int:
    stones = parse_input(input_path)
    return process_stones(stones, 25)


def solution2(input_path: Path) -> int:
    stones = parse_input(input_path)
    return process_stones(stones, 75)


# I'm ashamed to say I caved after not being able to get this running in a reasonable time.
# Grabbed the idea for this from: https://github.com/brass75/AdventOfCode/blob/main/aoc_2024/day11.py
def process_stones(stones: STONE_T, iterations: int) -> int:
    counts = Counter(stones)
    for _ in range(iterations):
        results = defaultdict(int)
        for stone, count in counts.items():
            for transformed in transform(stone):
                results[transformed] += count
        counts = results
    return sum(counts.values())


@cache
def transform(stone: int) -> STONE_T:
    if stone == 0:
        return [1]

    stone_str = str(stone)
    stone_len = len(stone_str)
    if stone_len % 2 == 0:
        split = stone_len // 2
        return [int(stone_str[:split]), int(stone_str[split:])]

    return [stone * 2024]


def parse_input(input_path: Path) -> STONE_T:
    data: list[int] = []
    with input_path.open() as f:
        for line in map(str.strip, f.readlines()):
            data.extend(map(int, line.split()))
    return data


if __name__ == '__main__':
    answer1 = 185894
    answer2 = 221632504974231
    solve(solution1, solution2, (answer1, answer2))
