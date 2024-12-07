from typing import TypeVar

T = TypeVar("T", default=int)

def chunks(lst: list[T], size: int) -> list[T]:
    for i in range(0, len(lst), size):
        yield lst[i:i + size]
