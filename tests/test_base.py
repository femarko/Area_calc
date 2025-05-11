import pytest
from decimal import Decimal

from area_calc.base import FigureBase


@pytest.mark.parametrize("figure,error_type,error_message", [
    (lambda: FigureBase(), ValueError, "No parameters provided."),
    (lambda: FigureBase(-1, 2), ValueError,"All parameters must be positive."),
    (lambda: FigureBase(0, 2), ValueError, "All parameters must be positive.")
])
def test_base_figure_init_raises_value_error(figure, error_type, error_message):
    if error_type == ValueError:
        with pytest.raises(ValueError) as e:
            figure()
        assert e.value.args[0] == error_message
    elif error_type == TypeError:
        with pytest.raises(TypeError) as e:
            figure()
        assert e.value.args[0] == error_message


def test_base_figure_detect_decimal():
    assert FigureBase.detect_decimal(1) is False
    assert FigureBase.detect_decimal(Decimal(1)) is True


def test_base_figure_area_raises_not_implemented_error():
    class FakeFigure(FigureBase): pass
    with pytest.raises(NotImplementedError) as e:
        FakeFigure(1).area()
    assert e.value.args[0] == "Subclasses must implement method '.area()'."