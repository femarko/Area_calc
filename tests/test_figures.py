import pytest

from src.figures import Circle, Triangle


@pytest.mark.parametrize("figure,area", [(Circle(radius=5), 78.53981633974483), (Triangle(3, 4, 5), 6.0,)])
def test_figures_calculates_area(figure, area):
    assert figure.area() == pytest.approx(area)


@pytest.mark.parametrize("factory,message", [
    (lambda: Circle(radius=-5), "Circle radius must be positive."),
    (lambda: Circle(radius=0), "Circle radius must be positive."),
    (lambda: Circle(), "Circle must have a radius."),
    (lambda: Triangle(-3, 4, 5), "Triangle sides must be positive."),
    (lambda: Triangle(3, -4, 5), "Triangle sides must be positive."),
    (lambda: Triangle(3, 4, -5), "Triangle sides must be positive."),
    (lambda: Triangle(3, 4), "Triangle must have 3 sides."),
    (lambda: Triangle(3), "Triangle must have 3 sides."),
    (lambda: Triangle(), "Triangle must have 3 sides."),
    (lambda: Triangle(3, 4, 5, 6), "Triangle must have 3 sides."),
    (lambda: Triangle(1, 2, 10), "Triangle is not valid: sum of two sides must be greater than third."),])
def test_figures_constructors_raise_value_errors(factory, message):
    with pytest.raises(ValueError) as e:
        factory()
    assert e.value.args[0] == message


@pytest.mark.parametrize("triangle,result", [(Triangle(3, 4, 5), True), (Triangle(5, 12, 11), False)])
def test_triangle_is_right(triangle, result):
    assert triangle.is_right() == result
