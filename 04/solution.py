import argparse
import re
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Optional, Sequence

from icecream import ic


def rotate_matrix_45(matrix: list[list[str]], right: bool = True) -> list[list[str]]:
    """
    Rotate matrix by 45 degrees right or left
    :param matrix: matrix to rotate
    :param right: If this is false, we rotate left
    :return: new altered matrix
    """
    if right:
        matrix = flip_matrix(matrix)

    rows = len(matrix)
    cols = len(matrix[0])

    new_matrix: list[list[str]] = []
    for i in range(rows):
        new_row: list[str] = []
        element_count = min(rows - 1, min(i, cols - 1))
        curr_col = 0

        while i <= rows - 1 and element_count != -1:
            new_row.append(matrix[i - curr_col][curr_col])
            curr_col += 1
            element_count -= 1
        new_matrix.append(new_row)

    for i in range(1, cols):
        new_row: list[str] = []
        element_count = min(rows - 1, cols - i - 1)
        curr_col = 0

        while i <= cols - 1 and element_count != -1:
            new_row.append(matrix[rows - 1 - curr_col][i + curr_col])
            curr_col += 1
            element_count -= 1
        new_matrix.append(new_row)

    if right:
        new_matrix = flip_matrix(new_matrix)

    return new_matrix


def rotate_matrix_90(matrix: list[list[str]]) -> list[list[str]]:
    new_matrix = deepcopy(matrix)
    return list(zip(*new_matrix))[::-1]


def flip_matrix(matrix: list[list[str]], horizontal: bool = True) -> list[list[str]]:
    """
    Flip a matrix vertically or horizontally
    :param matrix: matrix to flip
    :param horizontal: If this is false, we flip vertically
    :return: new altered matrix
    """
    new_matrix = deepcopy(matrix)
    if horizontal:
        for i in range(0, len(new_matrix)):
            new_matrix[i].reverse()
    else:
        new_matrix.reverse()
    return new_matrix


def condense_matrix(matrix: list[list[str]]) -> list[str]:
    return ["".join(row) for row in matrix]


def solution1(input_path: Path) -> None:
    data = parse_input(input_path)

    # Regular matrix
    matrix = condense_matrix(data)
    # 90 Degree matrix
    matrix_90 = condense_matrix(rotate_matrix_90(data))
    # 45 Degree Right Matrix
    matrix_45r = condense_matrix(rotate_matrix_45(data))
    # 45 Degree Left Matrix
    matrix_45l = condense_matrix(rotate_matrix_45(data, right=False))

    occurrences = 0
    for matrix in [matrix, matrix_90, matrix_45r, matrix_45l]:
        for i, row in enumerate(matrix):
            for search_term in [r"XMAS", r"SAMX"]:
                all_items = re.findall(search_term, row)
                occurrences += len(all_items)
                ic(i, row, all_items, len(all_items))

    print(f"Solution 1: {occurrences}")


def solution2(input_path: Path) -> None:
    data = parse_input(input_path)

    # 45 Degree Right Matrix
    matrix_45r = condense_matrix(rotate_matrix_45(data))
    # 45 Degree Left Matrix
    matrix_45l = condense_matrix(rotate_matrix_45(data, right=False))

    rows = len(data)
    cols = len(data[0])

    mapping: dict[tuple[int, int], int] = defaultdict(int)

    a_45r: list[tuple[int, int]] = []
    ic(matrix_45r)
    for i, row in enumerate(matrix_45r):
        for search_term in [r"MAS", r"SAM"]:
            if not (match := re.finditer(search_term, row)):
                continue
            for item in match:
                s = item.span()
                a_idx = s[1] - 2
                a_45r.append((i, a_idx))
                ic(i, row, a_idx)
    ic(a_45r)

    ic(rows, cols)
    for r, c in a_45r:
        if r < rows:
            orig_r = c
            orig_c = (rows - 1) - r + c
        else:
            orig_r = r - (rows - 1) + c
            orig_c = c

        mapping[(orig_r, orig_c)] += 1
        ic(r, c, orig_r, orig_c, data[orig_r][orig_c])

    a_45l: list[tuple[int, int]] = []
    ic(matrix_45l)
    for i, row in enumerate(matrix_45l):
        for search_term in [r"MAS", r"SAM"]:
            if not (match := re.finditer(search_term, row)):
                continue
            for item in match:
                s = item.span()
                a_idx = s[1] - 2
                a_45l.append((i, a_idx))
                ic(i, row, a_idx)
    ic(a_45l)

    ic(rows, cols)
    for r, c in a_45l:
        if r < rows:
            orig_r = r - c
            orig_c = c
        else:
            orig_r = (rows - 1) - c
            orig_c = r - (rows - 1) + c

        mapping[(orig_r, orig_c)] += 1
        ic(r, c, orig_r, orig_c, data[orig_r][orig_c])

    ic(mapping)

    occurrence = sum(1 for v in mapping.values() if v > 1)
    print(f"Solution 2: {occurrence}")


def parse_input(input_path: Path, solution: int = 1) -> list[list[str]]:
    data: list[list[str]] = []
    with input_path.open() as f:
        for line in map(str.strip, f.readlines()):
            data.append(list(line))

    return data


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