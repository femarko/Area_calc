import math

from typing import Union
from decimal import Decimal, localcontext


class FigureBase:
    """
    Base class for geometric figures.

    Provides a basic implementation of the `area` method and a method
    `_detect_decimal` that detects whether any parameter is of type
    :class:`Decimal`.

    The `area` method raises a :class:`NotImplementedError` if not implemented
    by a subclass.

    :param args: The list of non-keyword arguments.
    :type args: tuple[Union[int, float, Decimal], ...]
    :param kwargs: The dictionary of keyword arguments.
    :type kwargs: dict[str, Union[int, float, Decimal]]
    """

    def __init__(self, *args: Union[int, float, Decimal], **kwargs: Union[int, float, Decimal]) -> None:
        """
        Initialize the FigureBase.
        :param args: The list of non-keyword arguments.
        :type args: tuple[Union[int, float, Decimal], ...]
        :param kwargs: The dictionary of keyword arguments.
        :type kwargs: dict[str, Union[int, float, Decimal]]
        :raises ValueError: If no parameters are provided or if any parameter is non-positive number.
        :ivar use_decimal: Indicates whether any parameter is of type Decimal, default is False.
        :vartype use_decimal: bool
        """

        if not any((args, kwargs)):
            raise ValueError("No parameters provided.")
        if any(arg <= 0 for arg in args) or any(v <= 0 for v in kwargs.values()):
            raise ValueError("All parameters must be positive.")

    @staticmethod
    def detect_decimal(*args, **kwargs) -> bool:
        """
        Detect whether any parameter is of type Decimal.

        :param args: The list of non-keyword arguments.
        :type args: tuple[Union[int, float, Decimal], ...]
        :param kwargs: The dictionary of keyword arguments.
        :type kwargs: dict[str, Union[int, float, Decimal]]
        :returns: True if any parameter is of type Decimal, False otherwise.
        :rtype: bool
        """
        return any(isinstance(arg, Decimal) for arg in args) or any(isinstance(v, Decimal) for v in kwargs.values())

    def area(self) -> Union[int, float, Decimal]:
        """
        Calculates the area of the figure.

        :returns: The area of the figure.
        :rtype: Union[int, float, Decimal]

        :raises NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("Subclasses must implement method '.area()'.")


class Circle(FigureBase):
    """
    Represents a geometric Circle with method to calculate its area.

    :param params: A dictionary with the radius of the circle.
    :type params: dict
    :param radius: The radius of the circle.
    :type radius: Union[int, float, Decimal]
    """

    def __init__(self, radius: Union[int, float, Decimal]) -> None:
        """
        Initialize the Circle.

        :param radius: The radius of the circle.
        :type radius: Union[int, float, Decimal]
        """
        super().__init__(radius)
        self.radius: Union[int, float, Decimal] = radius

    def area(self) -> Union[int, float, Decimal]:
        """
        Calculates the area of the Circle.

        The area is calculated as :math:`\pi r^2` using the `math.pi` constant
        or with 100 decimal precision using the `decimal` module, depending on
        whether any parameter is of type `Decimal`.

        :returns: The area of the Circle.
        :rtype: Union[int, float, Decimal]
        """
        if self.detect_decimal(self.radius):
            with localcontext() as ctx:
                ctx.prec = 100
                pi_101 = Decimal(
                    '3.141592653589793238462643383279502884197169399375105'
                    '8209749445923078164062862089986280348253421170679'
                )
                return pi_101 * self.radius ** 2
        return math.pi * self.radius ** 2


class Triangle(FigureBase):
    """
    Represents a geometric Triangle with methods to validate its properties
    and calculate its area.

    :param sides: Lengths of the three sides of the triangle. Must be positive numbers.
    :type sides: Union[int, float, Decimal]
    :raises ValueError: If the number of sides is not equal to 3.
    :raises ValueError: If any side length is non-positive.
    :raises ValueError: If the sum of any two sides is not greater than the third side.
    """

    def __init__(self, *sides: Union[int, float, Decimal]) -> None:
        """
        Initialize the Triangle.

        :param sides: Lengths of the three sides of the triangle. Must be positive numbers.
        :type sides: Union[int, float, Decimal]
        :raises ValueError: If the number of sides is not equal to 3.
        :raises ValueError: If any side length is non-positive.
        :raises ValueError: If the sum of any two sides is not greater than the third side.
        """

        super().__init__(*sides)
        if len(sides) != 3:
            raise ValueError("Triangle must have 3 sides.")
        self.sides: list[Union[int, float, Decimal]] = sorted(sides)
        if self.sides[0] + self.sides[1] <= self.sides[2]:
            raise ValueError("Triangle is not valid: sum of two sides must be greater than third.")

    def is_right(self) -> bool:
        """
        Check if the triangle is right-angled.

        :returns: True if the triangle is right-angled, False otherwise.
        :rtype: bool
        """
        return math.isclose(self.sides[0] ** 2 + self.sides[1] ** 2, self.sides[2] ** 2)

    @staticmethod
    def _get_right_triangle_area(sides: list[Union[int, float, Decimal]],
                                 denominator: Union[int, float, Decimal]) -> Union[int, float, Decimal]:
        return sides[0] * sides[1] / denominator

    @staticmethod
    def _squared_herons_area(sides: list[Union[int, float, Decimal]],
                             half_perimeter: Union[int, float, Decimal]) -> Union[int, float, Decimal]:
        return (
                half_perimeter * (half_perimeter - sides[0]) * (half_perimeter - sides[1]) * (half_perimeter - sides[2])
        )

    def area(self) -> Union[int, float, Decimal]:
        if self.detect_decimal(*self.sides):
            with localcontext() as ctx:
                ctx.prec = 100
                sides: list[Decimal] = [Decimal(side) if not isinstance(side, Decimal) else side for side in self.sides]
                if self.is_right():
                    return self._get_right_triangle_area(sides=sides, denominator=Decimal(2))
                return self._squared_herons_area(sides=sides, half_perimeter=sum(self.sides) / Decimal(2)).sqrt()
        if self.is_right():
            return self._get_right_triangle_area(sides=self.sides, denominator=2)
        return math.sqrt(self._squared_herons_area(sides=self.sides, half_perimeter=sum(self.sides) / 2))
