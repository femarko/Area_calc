"""
Package `area_calc`.

This package provides classes and methods for calculating areas of geometric figures such as circles and triangles.

Modules:
- `circle`: Contains the `Circle` class for calculating the area of a circle.
- `triangle`: Contains the `Triangle` class for calculating the area of a triangle using Heron's formula
or the right triangle formula.

Classes:
- `Circle`: Represents a geometric circle with methods to calculate its area.
- `Triangle`: Represents a geometric triangle with methods to calculate its area and check if it is right-angled.

The package is extendable by adding other classes for other figures, inheriting from
the `area_calc.base.FigureBase` class.

Usage:

    from area_calc import Circle, Triangle

    circle = Circle(5)
    print(circle.area())  # Output: 78.53981633974483

    triangle = Triangle(3, 4, 5)
    print(triangle.area())  # Output: 6.0

"""

from area_calc.circle import Circle
from area_calc.triangle import Triangle
from area_calc.types_naming import FigureParamInp, FigureParamNum, ValidParams


__all__ = ["Circle", "Triangle", "FigureParamInp", "FigureParamNum", "ValidParams"]
