import pytest
from decimal import Decimal

from area_calc.validation import validate_params


@pytest.mark.parametrize("args,kwargs,error,message", [
    ((), {}, ValueError, "No parameters provided."),
    ((-1,), {}, ValueError, "All parameters must be positive."),
    ((), {"example_param": -1}, ValueError, "All parameters must be positive."),
    ((0,), {}, ValueError, "All parameters must be positive."),
    ((), {"example_param": 0}, ValueError, "All parameters must be positive."),
    ((True,), {}, TypeError, "All parameters must be: int, float, Decimal or sring where all characters are digits."),
    ((), {"example_param": True}, TypeError, "All parameters must be: int, float, Decimal or sring where all "
                                             "characters are digits."),
    (("non-digit string",), {}, TypeError, "All parameters must be: int, float, Decimal or sring where "
                                           "all characters are digits."),
    ((), {"example_param": "non-digit string"}, TypeError, "All parameters must be: int, float, Decimal or sring "
                                                            "where all characters are digits.")
])
def test_validate_params_raises_errors_for_invalid_params(args, kwargs, error, message):
    if error == ValueError:
        with pytest.raises(ValueError) as e:
            validate_params(*args, **kwargs)
    elif error == TypeError:
        with pytest.raises(TypeError) as e:
            validate_params(*args, **kwargs)
    assert e.value.args[0] == message


@pytest.mark.parametrize(
    "args,kwargs,result", [
        ((1,), {}, ((1,), {})),
        ((), {"example_param": 1}, ((), {"example_param": 1})),
        ((1.0,), {}, ((1.0,), {})),
        ((), {"example_param": 1.0}, ((), {"example_param": 1.0})),
        ((Decimal(1),), {}, ((Decimal(1),), {})),
        ((), {"example_param": Decimal(1)}, ((), {"example_param": Decimal(1)}))
    ]
)
def test_validate_params_returns_valid_params(args, kwargs, result):
    assert validate_params(*args, **kwargs) == result