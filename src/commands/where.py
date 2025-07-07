from typing import Callable, Sequence, TypeVar

from common_types import Data
from exceptions import IncorrectDataException

from .base import BaseCommand, HandledData

T = TypeVar("T", str, float)

predicate = Callable[
    [T, T],
    bool,
]


def equal(a: T, b: T) -> bool:
    return a == b


def less_than(a: T, b: T) -> bool:
    return a < b


def greater_than(a: T, b: T) -> bool:
    return a > b


class WhereCommand(BaseCommand):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.operators = dict[str, predicate]()

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
        validated_data = []
        for operator in sorted(
            self.operators,
            key=len,
            reverse=True,
        ):  # Сортируем по длине оператора,
            # чтобы менее длинные операторы не
            # перекрывали более длинные
            groups = value.split(operator)
            if len(groups) == 2:
                field, condition = groups
                break
        else:
            raise IncorrectDataException(
                "Неверный формат условия или оператор есть в данных"
            )
        if field not in fieldnames:
            raise IncorrectDataException(
                f"Ошибка при обработке аргумента {self.command}: "
                f"Поле {field} не найдено в {fieldnames}"
            )

        try:
            float(current_data[0][field])
            type_of_field = float
        except ValueError:
            type_of_field = str
        try:
            condition = type_of_field(condition)
        except ValueError:
            raise IncorrectDataException(
                f"Неверный тип данных для условия: {condition!r}"
            )

        func = self.operators[operator]

        for row in current_data:
            if func(type_of_field(row[field]), condition):
                validated_data.append(row)

        return HandledData(
            current_data=validated_data,
            fieldnames=fieldnames,
        )

    def add_operator(
        self,
        operator: str,
        func: predicate,
    ) -> None:
        if operator in self.operators:
            raise ValueError(f"Оператор {operator} уже существует")
        self.operators[operator] = func


where_command = WhereCommand(
    command="where",
    help_text="Условие для фильтрации данных",
    number_in_queue=0,
)
where_command.add_operator("=", equal)
where_command.add_operator("<", less_than)
where_command.add_operator(">", greater_than)
