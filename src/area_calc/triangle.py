import math
from decimal import Decimal, localcontext
from typing import Union

from area_calc.base import FigureBase
from area_calc.types_naming import FigureParamInp, FigureParamNum


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

    def __init__(self, *sides: FigureParamInp) -> None:
        """
        Initializes the Triangle with given side lengths and validates them.

        :param sides: lengths of the three sides of the triangle. must be positive numbers.
        :type sides: union[int, float, decimal]
        :raises ValueError: if the number of sides is not equal to 3.
        :raises ValueError: if any side length is non-positive.
        :raises ValueError: if the sum of any two sides is not greater than the third side.
        """

        super().__init__(*sides)
        if len(self.args) != 3:
            raise ValueError("Triangle must have 3 sides.")
        self.sides: list[FigureParamNum] = sorted(self.args)
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
    def _get_right_triangle_area(catheti: list[FigureParamNum],
                                 denominator: FigureParamNum) -> FigureParamNum:
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
    def _squared_herons_area(sides: list[FigureParamNum],
                             half_perimeter: FigureParamNum) -> FigureParamNum:

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

    def area(self) -> FigureParamNum:
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
