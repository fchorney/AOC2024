from typing import TypeVar

T = TypeVar('T', default=int)


def chunks(lst: list[T], size: int) -> list[T]:
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def counted(f):
    """Decorate a function that adds a "calls" field which holds the number of times it's been called"""

    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        return f(*args, **kwargs)

    wrapped.calls = 0
    return wrapped
