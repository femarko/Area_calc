from decimal import Decimal
from typing import Union, Any

from area_calc.types_naming import FigureParamNum, ValidParams


def validate_params(*args: Any, **kwargs: Any) -> ValidParams:
    """
    Validate that parameters are provided and are valid numbers.

    This function checks if any parameters are provided. If not, it raises a
    :class:`ValueError`. It also validates that all provided parameters are of
    type :class:`int`, :class:`float`, :class:`Decimal` or :class:`str` and
    that all characters in a string are digits. If any parameter is
    not a number a :class:`TypeError` is raised. If any parametor is
    a non-positive number, a :class:`ValueError` is raised.

    :param args: The tuple of non-keyword arguments.
    :type args: tuple[Union[int, float, Decimal, str], ...]
    :param kwargs: The dictionary of keyword arguments.
    :type kwargs: dict[str, Union[int, float, Decimal, str]]
    :raises ValueError: If no parameters are provided, or if any parameter
    is a non-positive number
    :raises TypeError: If any parameter is not a number
    """
    if not args and not kwargs:
        raise ValueError("No parameters provided.")

    if (
            any(
                type(arg) not in (int, float, Decimal, str)
                or
                (isinstance(arg, str) and not arg.isdigit())
                for arg in args
            )
            or
            any(
                type(v) not in (int, float, Decimal, str)
                or
                (isinstance(v, str) and not v.isdigit())
                for v in kwargs.values())
    ):
        raise TypeError("All parameters must be: int, float, Decimal or string where all characters are digits.")

    if any(isinstance(arg, str) for arg in args) or any(isinstance(v, str) for v in kwargs.values()):
        args: tuple[FigureParamNum, ...] = tuple(float(arg) if isinstance(arg, str) else arg for arg in args)
        kwargs: dict[str, FigureParamNum] = {k: float(v) for k, v in kwargs.items() if isinstance(v, str)}

    if any(arg <= 0 for arg in args) or any(v <= 0 for v in kwargs.values()):
        raise ValueError("All parameters must be positive.")

    return args, kwargs
