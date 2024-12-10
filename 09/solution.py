import itertools
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from icecream import ic

from libaoc import solve
from libaoc.utils import chunks


def find_next_space(ptr: int, data: list[int]) -> int:
    for idx, item in enumerate(data[ptr:], ptr):
        if item == -1:
            return idx

def find_next_file(ptr: int, data: list[int]) -> int:
    for idx, item in enumerate(data[0:ptr + 1][::-1]):
        if item != -1:
            return ptr - idx


def calc_checksum(data: list[int]) -> int:
    return sum(idx * value for idx, value in enumerate(data) if value != -1)


def solution1(input_path: Path) -> int:
    data, *_ = parse_input(input_path)
    ic(data_str(data))

    s_ptr = find_next_space(0, data)
    f_ptr = find_next_file(len(data) - 1, data)

    # Test Input:
    # 00...111...2...333.44.5555.6666.777.888899
    # 0099811188827773336446555566..............

    while s_ptr < f_ptr:
        data[s_ptr], data[f_ptr] = data[f_ptr], data[s_ptr]
        s_ptr = find_next_space(s_ptr + 1, data)
        f_ptr = find_next_file(f_ptr - 1, data)

    ic(data_str(data))

    return calc_checksum(data)

@dataclass
class File:
    fid: int
    size: int
    idx: int

    def __lt__(self, other: Self) -> bool:
        return self.fid < other.fid

    def __eq__(self, other: Self) -> bool:
        return self.fid == other.fid

    def __repr__(self) -> str:
        return f"File(fid={self.fid}, size={self.size}, idx={self.idx})"

@dataclass
class Space:
    size: int
    idx: int

    def __lt__(self, other: Self) -> bool:
        return self.idx < other.idx

    def __eq__(self, other: Self) -> bool:
        return self.idx == other.idx

    def __repr__(self) -> str:
        return f"Space(size={self.size}, idx={self.idx})"

def swap(data: list[int], space: Space, file: File) -> None:
    data[space.idx : space.idx + file.size], data[file.idx : file.idx + file.size] = data[file.idx : file.idx + file.size], data[space.idx : space.idx + file.size]

def solution2(input_path: Path) -> int:
    data, space_map, space_idx_map, files = parse_input(input_path)
    ic(data_str(data))

    # 00...111...2...333.44.5555.6666.777.888899
    # 00992111777.44.333....5555.6666.....8888..

    for file in files:
        # If we don't actually have any spaces that can fit our file, then just move on
        if file.size > max(space_map.keys()):
            continue

        candidates = sorted(
            filter(
                lambda c: c.idx < file.idx,
                itertools.chain(*[space_map[k] for k in space_map.keys() if k >= file.size])
            ),
            key=lambda k: k.idx,
        )

        if len(candidates) == 0:
            continue

        space = candidates[0]
        swap(data, space, file)

        # Remove the space from the maps
        space_map[space.size].remove(space)
        del space_idx_map[space.idx]

        # Clean up space_map if we've removed all items for a key
        if len(space_map[space.size]) == 0:
            del space_map[space.size]

        # Modify the space based on the file
        space.size -= file.size
        space.idx += file.size

        if space.size == 0:
            continue

        # Put the space back into the maps
        space_map[space.size].append(space)
        space_map[space.size].sort()
        space_idx_map[space.idx] = space

    ic(data_str(data))

    return calc_checksum(data)


def data_str(data: list[int]) -> str:
    return ''.join('.' if x == -1 else str(x) for x in data)

def parse_input(input_path: Path) -> tuple[list[int], dict[int, list[Space]], dict[int, Space], list[File]]:
    data: list[int] = []
    space_map: dict[int, list[Space]] = defaultdict(list)
    space_idx_map: dict[int, Space] = {}
    files: list[File] = []
    idx = 0

    fid = 0
    with input_path.open() as f:
        for count, *space in chunks(list(map(int, list(f.read().strip()))), 2):
            space = (space or [0])[0]

            files.append(File(fid, count, idx))

            if space != 0:
                s = Space(space, idx + count)
                space_map[space].append(s)
                space_idx_map[s.idx] = s

            data.extend(fid for _ in range(count))
            data.extend(-1 for _ in range(space))

            fid += 1
            idx += count + space

    # Sort internal space lists by size
    [space_map[k].sort() for k in space_map.keys()]
    return data, space_map, space_idx_map, sorted(files, reverse=True)


if __name__ == '__main__':
    answer1 = 6337921897505
    answer2 = 6362722604045
    solve(solution1, solution2, (answer1, answer2))
