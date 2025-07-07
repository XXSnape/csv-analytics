import statistics
from operator import itemgetter
from typing import Callable, Sequence

from common_types import Data
from exceptions import IncorrectDataException

from .base import BaseCommand, HandledData

type aggregation_function = Callable[
    [Data, str],
    HandledData,
]


def find_minimum(data: Data, field: str) -> HandledData:
    min_value = min(data, key=itemgetter(field))
    name = "min"
    return HandledData(
        current_data=[{name: min_value[field]}],
        fieldnames=[name],
    )


def find_maximum(data: Data, field: str) -> HandledData:
    min_value = max(data, key=itemgetter(field))
    name = "max"
    return HandledData(
        current_data=[{name: min_value[field]}],
        fieldnames=[name],
    )


def find_average(data: Data, field: str) -> HandledData:
    avg = round(
        statistics.mean(float(row[field]) for row in data), 2
    )
    name = "avg"
    return HandledData(
        current_data=[{name: str(avg)}],
        fieldnames=[name],
    )


class AggregateCommand(
    BaseCommand[aggregation_function],
):

    def handle_data(
        self,
        current_data: Data,
        fieldnames: Sequence[str],
        value: str,
    ) -> HandledData:
        if not current_data:
            raise IncorrectDataException(
                "Нет данных для агрегирования"
            )
        groups = value.split("=")
        if len(groups) != 2:
            raise IncorrectDataException(
                "Неверный формат агрегирования. "
                "Ожидается 'поле=агрегатор'"
            )
        field, aggregator = groups
        func = self.operators.get(aggregator)
        if func is None:
            raise IncorrectDataException(
                f"Неизвестный агрегатор: {aggregator}"
            )
        if field not in fieldnames:
            raise IncorrectDataException(
                f"Поле {field} не найдено в {fieldnames}"
            )
        try:
            return func(current_data, field)
        except ValueError:
            raise IncorrectDataException(
                f"Ошибка при агрегировании поля {field}"
            )


aggregate_command = AggregateCommand(
    command="aggregate",
    help_text="Функция для агрегирования данных",
    number_in_queue=1,
)
aggregate_command.add_operator("min", find_minimum)
aggregate_command.add_operator("max", find_maximum)
aggregate_command.add_operator("avg", find_average)
