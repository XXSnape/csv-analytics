from collections.abc import Callable, Sequence
from typing import TypeVar

from common_types import Data
from exceptions import IncorrectDataException
import operator

from .base import (
    BaseCommand,
    HandledData,
    find_out_type,
)

T = TypeVar("T", str, float)

predicate = Callable[
    [T, T],
    bool,
]


class WhereCommand(
    BaseCommand[predicate],
):
    command = "where"
    help_text = "Условие для фильтрации данных"
    number_in_queue = 0

    def handle_data(
        self,
        current_data: Data,
        fieldnames: Sequence[str],
        value: str,
    ) -> HandledData:
        if not current_data:
            return HandledData(
                current_data=current_data,
                fieldnames=fieldnames,
            )
        for op in sorted(
            self.operators,
            key=len,
            reverse=True,
        ):  # Сортируем по длине оператора,
            # чтобы менее длинные операторы не
            # перекрывали более длинные
            groups = value.split(op)
            if len(groups) == 2:
                field, condition = groups
                break
        else:
            raise IncorrectDataException(
                "Неверный формат условия или оператор есть в данных. "
                f"Возможные операторы: {self.get_operator_names()}"
            )
        if field not in fieldnames:
            raise IncorrectDataException(
                f"Ошибка при обработке аргумента {self.command}: "
                f"Поле {field} не найдено в {fieldnames}"
            )

        type_of_field = find_out_type(
            current_data=current_data,
            field=field,
        )

        try:
            condition = type_of_field(condition)
        except ValueError:
            raise IncorrectDataException(
                f"Неверный тип данных для условия: {condition!r}"
            )

        func = self.operators[op]

        return HandledData(
            current_data=[
                row
                for row in current_data
                if func(type_of_field(row[field]), condition)
            ],
            fieldnames=fieldnames,
        )


where_command = WhereCommand()
where_command.add_operator("=", operator.eq)
where_command.add_operator("<", operator.lt)
where_command.add_operator(">", operator.gt)
