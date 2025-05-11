from typing import TypeAlias, Union
from decimal import Decimal


FigureParamInp: TypeAlias = Union[int, float, Decimal, str]
FigureParamNum: TypeAlias = Union[int, float, Decimal]
ValidParams = tuple[tuple[FigureParamNum, ...], dict[str, FigureParamNum]]