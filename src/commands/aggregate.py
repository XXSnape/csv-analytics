import statistics
from collections.abc import Callable, Sequence
from functools import partial

from common_types import Data, OperatorFunc
from exceptions import IncorrectDataException

from .base import (
    BaseCommand,
    DataValidatorMixin,
    HandledData,
    find_out_type,
)


def search_for(
    data: Data,
    field: str,
    func: Callable,
) -> HandledData:
    """Ищет единственное значение в данных поля по заданной функции."""
    type_of_field = find_out_type(
        current_data=data,
        field=field,
    )
    value = func(
        data,
        key=lambda item: type_of_field(item[field]),
    )
    name = func.__name__
    return HandledData(
        current_data=[{name: value[field]}],
        fieldnames=[name],
    )


def find_average(
    data: Data,
    field: str,
) -> HandledData:
    """Находит среднее значение в данных поля."""
    avg = round(
        statistics.mean(float(row[field]) for row in data), 2
    )
    name = "avg"
    return HandledData(
        current_data=[{name: str(avg)}],
        fieldnames=[name],
    )


find_maximum = partial(search_for, func=max)
find_minimum = partial(search_for, func=min)


class AggregateCommand(
    DataValidatorMixin[OperatorFunc],
    BaseCommand[OperatorFunc],
):
    """Команда для агрегирования данных в CSV файле."""

    command = "aggregate"
    help_text = "Функция для агрегирования данных"
    number_in_queue = 1
    raise_exception_if_there_is_no_data = True

    def handle_data(
        self,
        current_data: Data,
        fieldnames: Sequence[str],
        value: str,
    ) -> HandledData:
        """Обрабатывает данные в соответствии с командой агрегирования."""
        field = None
        try:
            func, field = self.validate_data(
                current_data=current_data,
                fieldnames=fieldnames,
                value=value,
            )
            return func(current_data, field)
        except IncorrectDataException:
            raise
        except ValueError:
            raise IncorrectDataException(
                f"Несовместимый тип для агрегировании поля {field}"
            )


aggregate_command = AggregateCommand()
aggregate_command.add_operator("min", find_minimum)
aggregate_command.add_operator("max", find_maximum)
aggregate_command.add_operator("avg", find_average)
