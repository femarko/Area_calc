from decimal import Decimal
from typing import Union


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
