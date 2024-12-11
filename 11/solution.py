from pathlib import Path

from icecream import ic

from libaoc import solve


def solution1(input_path: Path) -> int:
    stones = parse_input(input_path)
    ic(stones)

    for _ in range(25):
        idx = 0
        while idx < len(stones):
            idx = blink(stones, idx) + 1
    return len(stones)


def solution2(input_path: Path) -> int:
    stones = parse_input(input_path)
    ic(stones)

    count = 0
    idx = 0

    for _ in range(25):
        pass

    return -1

def transform(stone: int) -> tuple[int, ...]:
    stone_str = str(stone)
    stone_len = len(stone_str)

    if stone == 0:
        return (1,)
    elif stone_len % 2 == 0:
        left = int(stone_str[:stone_len // 2])
        right = int(stone_str[stone_len // 2:])
        return (left, right,)

    return (stone * 2024,)

def blink(stones: list[int], idx: int) -> int:
    result = transform(stones[idx])

    if len(result) == 1:
        stones[idx] = result[0]
        return idx

    stones[idx] = result[0]
    stones.insert(idx + 1, result[1])
    return idx + 1


def parse_input(input_path: Path) -> list[int]:
    data: list[int] = []
    with input_path.open() as f:
        for line in map(str.strip, f.readlines()):
            data.extend(map(int, line.split()))
    return data


if __name__ == '__main__':
    answer1 = 185894
    answer2 = -999
    solve(solution1, solution2, (answer1, answer2))
