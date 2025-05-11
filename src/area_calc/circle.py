import math
from decimal import Decimal, localcontext
from typing import Union

from area_calc.base import FigureBase
from area_calc.types_naming import FigureParamInp, FigureParamNum


class Circle(FigureBase):
    """
    Represents a geometric Circle with a method to calculate its area.

    :param radius: The radius of the circle. Must be a positive number.
    :type radius: Union[int, float, Decimal]
    :raises ValueError: If the radius is not a positive number.
    """

    def __init__(self, radius: FigureParamInp) -> None:
        """
        Initialize the Circle.

        :param radius: The radius of the circle. Must be a positive number.
        :type radius: Union[int, float, Decimal]
        :raises ValueError: If the radius is not a positive number.
        """
        super().__init__(radius)
        self.radius: FigureParamNum = self.args[0] if self.args else self.kwargs.get('radius', {})

    def area(self) -> FigureParamNum:
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
