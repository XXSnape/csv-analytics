import csv
import pathlib

import pytest

from commands import (
    aggregate_command,
    order_by_command,
    where_command,
)
from commands.base import HandledData
from handler import FileHandler


FILE_PATH = (
    pathlib.Path(__file__).resolve().parent
    / "files"
    / "products.csv"
)


@pytest.fixture()
def products() -> HandledData:
    with FILE_PATH.open() as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        products = list(reader)
    return HandledData(
        current_data=products,
        fieldnames=fieldnames,
    )


def register_commands(
    file_handler: FileHandler,
) -> None:
    commands = [
        where_command,
        aggregate_command,
        order_by_command,
    ]
    for command in commands:
        file_handler.register_handler(command)
