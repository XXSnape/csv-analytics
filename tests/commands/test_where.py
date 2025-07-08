from commands.base import HandledData
from common_types import Data
from exceptions import IncorrectDataException
from src.commands import where_command
import pytest


@pytest.mark.parametrize(
    "value, expected",
    [
        (
            "rating=4.1",
            [
                {
                    "name": "iphone se",
                    "brand": "apple",
                    "price": "429",
                    "rating": "4.1",
                },
                {
                    "name": "redmi 10c",
                    "brand": "xiaomi",
                    "price": "149",
                    "rating": "4.1",
                },
            ],
        ),
        (
            "brand=xiaomi",
            [
                {
                    "name": "redmi note 12",
                    "brand": "xiaomi",
                    "price": "199",
                    "rating": "4.6",
                },
                {
                    "name": "poco x5 pro",
                    "brand": "xiaomi",
                    "price": "299",
                    "rating": "4.4",
                },
                {
                    "name": "redmi 10c",
                    "brand": "xiaomi",
                    "price": "149",
                    "rating": "4.1",
                },
            ],
        ),
        ("name=NoName", []),
        (
            "rating>4.7",
            [
                {
                    "name": "iphone 15 pro",
                    "brand": "apple",
                    "price": "999",
                    "rating": "4.9",
                },
                {
                    "name": "galaxy s23 ultra",
                    "brand": "samsung",
                    "price": "1199",
                    "rating": "4.8",
                },
            ],
        ),
        (
            "rating<4.2",
            [
                {
                    "name": "iphone se",
                    "brand": "apple",
                    "price": "429",
                    "rating": "4.1",
                },
                {
                    "name": "redmi 10c",
                    "brand": "xiaomi",
                    "price": "149",
                    "rating": "4.1",
                },
            ],
        ),
        (
            "name>q",
            [
                {
                    "name": "redmi note 12",
                    "brand": "xiaomi",
                    "price": "199",
                    "rating": "4.6",
                },
                {
                    "name": "redmi 10c",
                    "brand": "xiaomi",
                    "price": "149",
                    "rating": "4.1",
                },
            ],
        ),
        ("price>1200", []),
    ],
)
def test_valid_value(
    products: HandledData,
    value: str,
    expected: Data,
) -> None:
    data, fieldnames = products
    result = where_command.handle_data(
        current_data=data,
        fieldnames=fieldnames,
        value=value,
    )
    assert result.current_data == expected


@pytest.mark.parametrize(
    "value",
    ["ratin=4.1", "rating==4.1", "rating>abc", "rating"],
)
def test_invalid_value(products: HandledData, value: str) -> None:
    data, fieldnames = products
    with pytest.raises(IncorrectDataException):
        where_command.handle_data(
            current_data=data,
            fieldnames=fieldnames,
            value=value,
        )
