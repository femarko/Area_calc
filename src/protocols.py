from typing import Protocol


class Figure(Protocol):

    def area(self) -> float:
        pass


