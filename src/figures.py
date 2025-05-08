import math

from typing import Union
from decimal import Decimal, localcontext

"""
Module implementing classes for geometric figures such as a circle and a triangle.

The :class:`Circle` class calculates the area of a circle using the formula
A = pi * r^2, where r is the radius of the circle, and the precision of the
result is 100 decimal places if the radius is of type :class:`Decimal`.

The :class:`Triangle` class calculates the area of a triangle using Heron's
formula, if the triangle is not right-angled, and the formula for right
triangles otherwise. The precision of the result is 100 decimal places if
any of the side lengths are of type :class:`Decimal`.

"""

class FigureBase:
    """
    Base class for geometric figures.

    Provides a basic implementation of the `area` method and a method
    `detect_decimal` that detects whether any parameter is of type
    :class:`Decimal`.

    The `area` method raises a :class:`NotImplementedError` if not implemented
    by a subclass.

    :param args: The list of non-keyword arguments.
    :type args: tuple[Union[int, float, Decimal], ...]
    :param kwargs: The dictionary of keyword arguments.
    :type kwargs: dict[str, Union[int, float, Decimal]]
    """

    def __init__(self,
                 *args: Union[int, float, Decimal],
                 **kwargs: Union[int, float, Decimal]) -> None:
        """
        Initialize the FigureBase.
        :param args: The list of non-keyword arguments.
        :type args: tuple[Union[int, float, Decimal], ...]
        :param kwargs: The dictionary of keyword arguments.
        :type kwargs: dict[str, Union[int, float, Decimal]]
        :raises ValueError: If no parameters are provided or if any parameter is non-positive number.
        """

        if not any((args, kwargs)):
            raise ValueError("No parameters provided.")
        if any(arg <= 0 for arg in args) or any(v <= 0 for v in kwargs.values()):
            raise ValueError("All parameters must be positive.")

    @staticmethod
    def detect_decimal(*args: Union[int, float, Decimal],
                       **kwargs: Union[int, float, Decimal]) -> bool:
        """
        Detects whether any parameter is of type :class:`Decimal`.

        :param args: The list of non-keyword arguments.
        :type args: tuple[Union[int, float, Decimal], ...]
        :param kwargs: The dictionary of keyword arguments.
        :type kwargs: dict[str, Union[int, float, Decimal]]
        :returns: True if any parameter is of type :class:`Decimal`, False otherwise.
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
    Represents a geometric Circle with a method to calculate its area.

    :param radius: The radius of the circle. Must be a positive number.
    :type radius: Union[int, float, Decimal]
    :raises ValueError: If the radius is not a positive number.
    """

    def __init__(self, radius: Union[int, float, Decimal]) -> None:
        """
        Initialize the Circle.

        :param radius: The radius of the circle. Must be a positive number.
        :type radius: Union[int, float, Decimal]
        :raises ValueError: If the radius is not a positive number.
        """

        super().__init__(radius)
        self.radius: Union[int, float, Decimal] = radius

    def area(self) -> Union[int, float, Decimal]:
        """
        Calculates the area of the circle.

        The area is calculated using the formula: A = pi * r^2,
        where r is the radius of the circle.

        If the radius is of type :class:`int` or :class:`float`,
        the area is calculated using the :class:`math` module and
        the result is of the same type as the radius.

        If the radius is of type :class:`Decimal`,
        the area is calculated using the :class:`decimal` module
        and the result is of type :class:`Decimal`.
        The precision of the result is 100 decimal places.

        :returns: The area of the circle.
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
    represents a geometric triangle with methods
    to calculate its area and to check if it is right-angled.

    :param sides: lengths of the three sides of the triangle. must be positive numbers.
    :type sides: union[int, float, decimal]
    :raises ValueError: if the number of sides is not equal to 3.
    :raises ValueError: if any side length is non-positive.
    :raises ValueError: if the sum of any two sides is not greater than the third side.

    methods
    -------
    __init__(self, *sides: union[int, float, decimal]) -> none
        initializes the triangle with given side lengths and validates them.

    area(self) -> union[int, float, decimal]
        calculates the area of the triangle using heron's formula
        or the formula for right triangles.

    is_right(self) -> bool
        checks if the triangle is right-angled.

    _get_right_triangle_area(
        sides: list[union[int, float, decimal]],
        denominator: union[int, float, decimal]
        ) -> union[int, float, decimal]  [staticmethod]
        calculates the area of a right triangle given its sides.

    _squared_herons_area(
        sides: list[union[int, float, decimal]],
        half_perimeter: union[int, float, decimal]
    ) -> union[int, float, decimal]  [staticmethod]
        calculates the squared area of the triangle using heron's formula.
    """

    def __init__(self, *sides: Union[int, float, Decimal]) -> None:
        """
        Initializes the Triangle with given side lengths and validates them.

        :param sides: lengths of the three sides of the triangle. must be positive numbers.
        :type sides: union[int, float, decimal]
        :raises ValueError: if the number of sides is not equal to 3.
        :raises ValueError: if any side length is non-positive.
        :raises ValueError: if the sum of any two sides is not greater than the third side.
        """

        super().__init__(*sides)
        if len(sides) != 3:
            raise ValueError("Triangle must have 3 sides.")
        self.sides: list[Union[int, float, Decimal]] = sorted(sides)
        if self.sides[0] + self.sides[1] <= self.sides[2]:
            raise ValueError("Triangle is not valid: sum of two sides must be greater than third.")

    def is_right(self) -> bool:
        """
        Check if the triangle is right-angled, based on the Pythagorean theorem.

        :returns: True if the triangle is right-angled, False otherwise.
        :rtype: bool
        """

        return math.isclose(self.sides[0] ** 2 + self.sides[1] ** 2, self.sides[2] ** 2)

    @staticmethod
    def _get_right_triangle_area(catheti: list[Union[int, float, Decimal]],
                                 denominator: Union[int, float, Decimal]) -> Union[int, float, Decimal]:
        """
        Static method.

        Calculate the area of a right triangle.
        Incapsulation of these calculations in a separate static method
        gives the possibility to vary the parameters and the result types,
        passing ``catheti`` and ``denominator`` as parameters with
        ``int``, ``float`` or ``Decimal`` types, depending on the context, where
        this method is utilized.
        As this method is static, it can be used without changing the triangle
        parameters saved as the instance attributes.

        :param catheti: The lengths of the two sides of the right triangle.
        :type catheti: list[Union[int, float, Decimal]]
        :param denominator: The denominator for the area calculation.
        :type denominator: Union[int, float, Decimal]
        :returns: The area of the right triangle.
        :rtype: Union[int, float, Decimal]
        """

        return catheti[0] * catheti[1] / denominator

    @staticmethod
    def _squared_herons_area(sides: list[Union[int, float, Decimal]],
                             half_perimeter: Union[int, float, Decimal]) -> Union[int, float, Decimal]:

        """
        Static method.

        Calculate the squared area of the triangle using Heron's formula.
        Incapsulation of these calculations in a separate static method
        gives the possibility to vary the parameters and the result types,
        passing ``sides`` and ``half_perimeter`` as parameters with
        ``int``, ``float`` or ``Decimal`` types, depending on the context, where
        this method is utilized.
        As this method is static, it can be used without changing the triangle
        parameters saved as the instance attributes.

        :param sides: The lengths of the three sides of the triangle.
        :type sides: list[Union[int, float, Decimal]]
        :param half_perimeter: The half of the perimeter of the triangle.
        :type half_perimeter: Union[int, float, Decimal]
        :returns: The squared area of the triangle.
        :rtype: Union[int, float, Decimal]
        """

        return (
                half_perimeter * (half_perimeter - sides[0]) * (half_perimeter - sides[1]) * (half_perimeter - sides[2])
        )

    def area(self) -> Union[int, float, Decimal]:
        """
        Calculates the area of the triangle.

        If any of the sides are of type Decimal, the calculations are done with
        the precision of 100 decimal places. If the triangle is right-angled,
        the area is calculated using the formula for right triangles. Otherwise,
        Heron's formula is used.

        :returns: The area of the triangle.
        :rtype: Union[int, float, Decimal]

        The method uses the following auxiliary methods:

        - :meth:`_get_right_triangle_area` to calculate the area of a right triangle.
        - :meth:`_squared_herons_area` to calculate the squared area of the triangle using Heron's formula.
        """

        is_right = self.is_right()

        if self.detect_decimal(*self.sides):
            with localcontext() as ctx:
                ctx.prec = 100
                sides: list[Decimal] = [Decimal(side) if not isinstance(side, Decimal) else side for side in self.sides]
                if is_right:
                    return self._get_right_triangle_area(catheti=sides, denominator=Decimal(2))
                return self._squared_herons_area(sides=sides, half_perimeter=sum(self.sides) / Decimal(2)).sqrt()
        if is_right:
            return self._get_right_triangle_area(catheti=self.sides, denominator=2)
        return math.sqrt(self._squared_herons_area(sides=self.sides, half_perimeter=sum(self.sides) / 2))
