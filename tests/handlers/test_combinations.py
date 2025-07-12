import pytest

from common_types import Data
from handler import FileHandler
from tests.conftest import FILE_PATH, register_commands


@pytest.mark.parametrize(
    "values, expected",
    [
        (
            {
                "where": "brand=xiaomi",
                "aggregate": "rating=min",
            },
            [{"min": "4.1"}],
        ),
        (
            {
                "where": "brand=xiaomi",
                "aggregate": "rating=avg",
            },
            [{"avg": "4.37"}],
        ),
        (
            {
                "where": "brand=xiaomi",
                "order-by": "price=asc",
            },
            [
                {
                    "name": "redmi 10c",
                    "brand": "xiaomi",
                    "price": "149",
                    "rating": "4.1",
                },
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
            ],
        ),
        (
            {
                "where": "brand=xiaomi",
                "aggregate": "rating=min",
                "order-by": "min=desc",
            },
            [{"min": "4.1"}],
        ),
    ],
)
def test_handler(
    values: dict[str, str],
    expected: Data,
) -> None:
    handler = FileHandler(
        file_path=str(FILE_PATH),
        values=values,
    )
    register_commands(handler)
    result = handler.handle()
    assert result.current_data == expected
