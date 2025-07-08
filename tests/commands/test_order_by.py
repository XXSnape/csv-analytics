import pytest
from exceptions import IncorrectDataException

from commands import order_by_command
from commands.base import HandledData


@pytest.mark.parametrize(
    "value, names",
    [
        (
            "price=asc",
            [
                "redmi 10c",
                "redmi note 12",
                "poco x5 pro",
                "galaxy a54",
                "iphone se",
                "iphone 13 mini",
                "iphone 14",
                "iphone 15 pro",
                "galaxy z flip 5",
                "galaxy s23 ultra",
            ],
        ),
        (
            "price=desc",
            [
                "galaxy s23 ultra",
                "iphone 15 pro",
                "galaxy z flip 5",
                "iphone 14",
                "iphone 13 mini",
                "iphone se",
                "galaxy a54",
                "poco x5 pro",
                "redmi note 12",
                "redmi 10c",
            ],
        ),
        (
            "name=asc",
            [
                "galaxy a54",
                "galaxy s23 ultra",
                "galaxy z flip 5",
                "iphone 13 mini",
                "iphone 14",
                "iphone 15 pro",
                "iphone se",
                "poco x5 pro",
                "redmi 10c",
                "redmi note 12",
            ],
        ),
    ],
)
def test_valid_value(
    products: HandledData,
    value: str,
    names: list[str],
) -> None:
    data, fieldnames = products
    result = order_by_command.handle_data(
        current_data=data,
        fieldnames=fieldnames,
        value=value,
    )
    assert [row["name"] for row in result.current_data] == names


@pytest.mark.parametrize(
    "value",
    ["ratin=desc", "rating=price", "rating"],
)
def test_invalid_value(products: HandledData, value: str) -> None:
    data, fieldnames = products
    with pytest.raises(IncorrectDataException):
        order_by_command.handle_data(
            current_data=data,
            fieldnames=fieldnames,
            value=value,
        )
