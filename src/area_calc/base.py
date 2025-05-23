from decimal import Decimal
from typing import Union, Sequence, Generator

from area_calc.validation import validate_params
from area_calc.types_naming import FigureParamInp, FigureParamNum


class FigureBase:
    """
    Base class for geometric figures.

    Provides a basic implementation of the `area` method and a method
    `has_decimal` that detects whether any parameter is of type
    :class:`Decimal`.

    The `area` method raises a :class:`NotImplementedError` if not implemented
    by a subclass.

    :param args: The list of non-keyword arguments.
    :type args: tuple[Union[int, float, Decimal], ...]
    :param kwargs: The dictionary of keyword arguments.
    :type kwargs: dict[str, Union[int, float, Decimal]]
    """

    def __init__(self,
                 *args: FigureParamInp,
                 **kwargs: FigureParamInp) -> None:
        """
        Initialize the FigureBase.
        :param args: The list of non-keyword arguments.
        :type args: tuple[Union[int, float, Decimal], ...]
        :param kwargs: The dictionary of keyword arguments.
        :type kwargs: dict[str, Union[int, float, Decimal]]
        :raises ValueError: If no parameters are provided or if any parameter is non-positive number.
        """
        validated_params = validate_params(*args, **kwargs)
        if self.has_decimal(*validated_params[0], **validated_params[1]):
            self.precision: int = kwargs.get("precision", 100)
            self.args: tuple[Decimal, ...] = tuple(
                Decimal(arg) if not isinstance(arg, Decimal) else arg for arg in validated_params[0]
            )
            self.kwargs: dict[str, Decimal] = {
                k: Decimal(v) if not isinstance(v, Decimal) else v for k, v in validated_params[1].items()
            }
        else:
            self.args: tuple[FigureParamNum, ...] = validated_params[0]
            self.kwargs: dict[str, FigureParamNum] = validated_params[1]

    @staticmethod
    def has_decimal(*args: FigureParamNum,
                    **kwargs: FigureParamNum) -> bool:
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

    def area(self) -> FigureParamNum:
        """
        Calculates the area of the figure.

        :returns: The area of the figure.
        :rtype: Union[int, float, Decimal]

        :raises NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("Subclasses must implement method '.area()'.")
