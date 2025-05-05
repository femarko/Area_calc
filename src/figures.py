import math

from typing import Union


class FigureBAse:

    def area(self) -> float:
        pass


class Circle(FigureBAse):

    def __init__(self, **params: Union[int, float]) -> None:
        if "radius" not in params:
            raise ValueError("Circle must have a radius.")
        if params["radius"] <= 0:
            raise ValueError("Circle radius must be positive.")
        self.params: dict[str, Union[int, float]] = params
        self.radius: Union[int, float] = params["radius"]
    """
    Represents a geometric Circle with method to calculate its area.

    :param params: A dictionary with the radius of the circle.
    :type params: dict
    :param radius: The radius of the circle.
    :type radius: Union[int, float]
    """
    def area(self) -> float:
        return math.pi * self.radius ** 2


class Triangle(FigureBAse):
    """
    Represents a geometric Triangle with methods to validate its properties
    and calculate its area.

    :param sides: Lengths of the three sides of the triangle. Must be positive numbers.
    :type sides: Union[int, float]
    :raises ValueError: If the number of sides is not equal to 3.
    :raises ValueError: If any side length is non-positive.
    :raises ValueError: If the sum of any two sides is not greater than the third side.
    """
    def __init__(self, *sides: Union[int, float]) -> None:
        """
        :param sides: Lengths of the three sides of the triangle. Must be positive numbers.
        :type sides: Union[int, float]
        :raises ValueError: If the number of sides is not 3.
        :raises ValueError: If any side is non-positive.
        :raises ValueError: If the sum of two sides is not greater than the third.
        """
        if len(sides) != 3:
            raise ValueError("Triangle must have 3 sides.")
        if any(side <= 0 for side in sides):
            raise ValueError("Triangle sides must be positive.")
        self.a, self.b, self.c = sorted(sides)
        if self.a + self.b <= self.c:
            raise ValueError("Triangle is not valid: sum of two sides must be greater than third.")
        self.p = (self.a + self.b + self.c) / 2  # half perimeter of sides

    def is_right(self) -> bool:
        """
        Check if the triangle is right-angled.

        :returns: True if the triangle is right-angled, False otherwise.
        :rtype: bool
        """
        return math.isclose(self.a ** 2 + self.b ** 2, self.c ** 2)

    def area(self) -> float:
        """
        Calculates the area of the triangle.

        If the triangle is right-angled, the area is calculated as
        (base * height) / 2.

        If the triangle is not right-angled, the area is calculated
        using Heron's formula.

        :returns: The area of the triangle.
        :rtype: float
        """
        if self.is_right():
            return (self.a * self.b) / 2
        return math.sqrt(self.p * (self.p - self.a) * (self.p - self.b) * (self.p - self.c))
