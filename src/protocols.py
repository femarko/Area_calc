from typing import Protocol


class Figure(Protocol):
    name: str
    params: dict[str, float]
    def area(self) -> float:
        pass


