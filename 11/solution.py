from pathlib import Path

from icecream import ic

from libaoc import solve


def solution1(input_path: Path) -> int:
    stones = parse_input(input_path)
    ic(stones)

    for blink in range(28):
        idx = 0
        while idx < len(stones):
            idx = transform(stones, idx) + 1
    return len(stones)


def solution2(input_path: Path) -> int:
    data = parse_input(input_path)
    ic(data)

    return -1

def transform(stones: list[int], idx: int) -> int:
    value = stones[idx]
    str_value = str(value)

    if value == 0:
        stones[idx] = 1
    elif (str_len := len(str_value)) % 2 == 0:
        left = int(str_value[:str_len // 2])
        right = int(str_value[str_len // 2:])
        stones[idx] = left
        stones.insert(idx + 1, right)
        return idx + 1
    else:
        stones[idx] *= 2024
    return idx


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
