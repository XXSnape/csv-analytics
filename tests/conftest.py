import pytest
import csv
import pathlib

from commands.base import HandledData


@pytest.fixture()
def products() -> HandledData:
    path = (
        pathlib.Path(__file__).resolve().parent
        / "files"
        / "products.csv"
    )
    with path.open() as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        products = list(reader)
    return HandledData(current_data=products, fieldnames=fieldnames)
