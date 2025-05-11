import pytest
import math
from decimal import Decimal

from area_calc.triangle import Triangle
from area_calc.circle import Circle


@pytest.mark.parametrize("figure,area", [(Circle(radius=5), 78.53981633974483),
                                         (Triangle(3, 4, 5), 6.0,),
                                         (Triangle(0.0001, 0.0001, 0.0001), 4.330127018922195e-09)])
def test_figures_calculates_area(figure, area):
    assert figure.area() == pytest.approx(area)


@pytest.mark.parametrize("radius", [Decimal(1e-10), Decimal(1e100), Decimal(1e-100)])
def test_circle_calculates_area_with_decimals(radius, pi_101):
    area = Circle(radius=radius).area()
    expected = Decimal(pi_101) * radius ** 2
    assert  area == pytest.approx(expected)


@pytest.mark.parametrize("factory,message", [
    (lambda: Circle(radius=-5), "All parameters must be positive."),
    (lambda: Circle(radius=0), "All parameters must be positive."),
    (lambda: Triangle(-3, 4, 5), "All parameters must be positive."),
    (lambda: Triangle(3, -4, 5), "All parameters must be positive."),
    (lambda: Triangle(3, 4, -5), "All parameters must be positive."),
    (lambda: Triangle(3, 4), "Triangle must have 3 sides."),
    (lambda: Triangle(3), "Triangle must have 3 sides."),
    (lambda: Triangle(), "No parameters provided."),
    (lambda: Triangle(3, 4, 5, 6), "Triangle must have 3 sides."),
    (lambda: Triangle(1, 2, 10), "Triangle is not valid: sum of two sides must be greater than third."),
    (lambda: Triangle(1, 1, 2), "Triangle is not valid: sum of two sides must be greater than third.")])
def test_figures_constructors_raise_value_errors(factory, message):
    with pytest.raises(ValueError) as e:
        factory()
    assert e.value.args[0] == message


def test_circle_init_raises_type_error_when_radius_passed_as_string():
    with pytest.raises(TypeError) as e:
        Circle("radius")
    assert str(e.value) == "All parameters must be: int, float, Decimal or string where all characters are digits."

def test_circle_init_raises_type_error_when_no_radius_passed():
    with pytest.raises(TypeError) as e:
        Circle()
    assert "missing 1 required positional argument: 'radius'" in str(e.value)

@pytest.mark.parametrize(
    "triangle,expected", [
        (Triangle(3, 4, 5), True),
        (Triangle(5, 3, 4), True),
        (Triangle(5, 12, 11), False),
        (Triangle(5, 12, 13), True),
        (Triangle(6, 8, 10), True),
        (Triangle(1.5, 2.0, 2.5), True),
        (Triangle(7, 24, 25), True),
        (Triangle(5, 12, 11), False),
        (Triangle(2, 2, 3), False),
        (Triangle(10, 10, 14.1421356237), True),
        (Triangle(Decimal(1.5), 2.0, 2.5), True),
    ]
)
def test_triangle_is_right(triangle, expected):
    assert triangle.is_right() == expected
