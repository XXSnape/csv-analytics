import pytest
from common_types import Data
from exceptions import IncorrectDataException

from commands import aggregate_command
from commands.base import HandledData


@pytest.mark.parametrize(
    "value, expected",
    [
        ("rating=avg", [{"avg": "4.49"}]),
        ("rating=min", [{"min": "4.1"}]),
        ("rating=max", [{"max": "4.9"}]),
        ("price=avg", [{"avg": "602.0"}]),
        ("price=min", [{"min": "149"}]),
        ("price=max", [{"max": "1199"}]),
        ("name=min", [{"min": "galaxy a54"}]),
    ],
)
def test_valid_value(
    products: HandledData,
    value: str,
    expected: Data,
) -> None:
    data, fieldnames = products
    result = aggregate_command.handle_data(
        current_data=data,
        fieldnames=fieldnames,
        value=value,
    )
    assert result.current_data == expected


@pytest.mark.parametrize(
    "value",
    ["ratin=avg", "rating=sum", "name=avg", "rating"],
)
def test_invalid_value(products: HandledData, value: str) -> None:
    data, fieldnames = products
    with pytest.raises(IncorrectDataException):
        aggregate_command.handle_data(
            current_data=data,
            fieldnames=fieldnames,
            value=value,
        )
