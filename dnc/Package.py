from typing import Generic, TypeVar

T = TypeVar('T')


class Package(Generic[T]):
    def __init__(self) -> None:
        self.pack: dict[int, T] = dict()

    def set(self, index: int, item: T) -> None:
        self.pack[index] = item

    def get(self, index: int) -> T:
        return self.pack[index]

    def array(self):
        return self.pack.values()
