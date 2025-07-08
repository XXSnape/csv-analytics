import statistics
from collections.abc import Sequence
from operator import itemgetter

from common_types import Data, OperatorFunc
from exceptions import IncorrectDataException

from .base import BaseCommand, DataValidatorMixin, HandledData


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
    DataValidatorMixin[OperatorFunc],
    BaseCommand[OperatorFunc],
):
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
