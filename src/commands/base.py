from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from typing import ClassVar, NamedTuple

from common_types import Data
from exceptions import IncorrectDataException


class HandledData(NamedTuple):
    """Класс для хранения обработанных данных и полей."""

    current_data: Data
    fieldnames: Sequence[str]


class BaseCommand[T: Callable](ABC):
    """Базовый класс для команд обработки данных.

    Атрибуты:

    command - Название команды, которое будет использоваться в CLI
    help_text - Описание команды, которое будет использоваться в CLI
    number_in_queue - Порядок выполнения команды в очереди
    required - Флаг, указывающий, является ли команда обязательной

    """

    command: ClassVar[str]
    help_text: ClassVar[str]
    number_in_queue: ClassVar[int]
    required: ClassVar[bool] = False

    def __init__(self) -> None:
        """Инициализирует операторы для команды."""
        self.operators = dict[str, T]()

    @abstractmethod
    def handle_data(
        self,
        current_data: Data,
        fieldnames: Sequence[str],
        value: str,
    ) -> HandledData:
        """Обрабатывает данные в соответствии с командой."""
        raise NotImplementedError

    def add_operator(
        self,
        operator: str,
        func: T,
    ) -> None:
        """Добавляет оператор для обработки данных."""
        if operator in self.operators:
            raise ValueError(f"Оператор {operator} уже существует")
        self.operators[operator] = func

    def get_operator_names(self) -> str:
        """Возвращает строку с именами доступных операторов."""
        return (
            ", ".join(self.operators.keys())
            if self.operators
            else "Нет доступных операторов"
        )


class DataValidatorMixin[T: Callable]:
    """Миксин для валидации данных перед обработкой.

    Атрибуты:
    raise_exception_if_there_is_no_data - Флаг, указывающий,
    нужно ли выбрасывать исключение, если нет данных для обработки.

    """

    raise_exception_if_there_is_no_data: ClassVar[bool]

    def validate_data(
        self,
        current_data: Data,
        fieldnames: Sequence[str],
        value: str,
    ) -> tuple[T, str] | None:
        if not current_data:
            if self.raise_exception_if_there_is_no_data:
                raise IncorrectDataException(
                    f"Нет данных для обработки команды {self.command}"
                )
            return None

        groups = value.split("=")
        if len(groups) != 2:
            raise IncorrectDataException(
                f"Неверный формат для команды {self.command}. "
                "Ожидается 'поле=оператор'"
            )
        field, operator = groups
        func = self.operators.get(operator)
        if func is None:
            raise IncorrectDataException(
                f"Неизвестный оператор для команды "
                f"{self.command!r} — {operator}. "
                f"Возможные операторы: {self.get_operator_names()}"
            )

        if field not in fieldnames:
            raise IncorrectDataException(
                f"Поле {field} не найдено в {fieldnames}"
            )
        return func, field


def find_out_type(
    current_data: Data,
    field: str,
) -> type:
    """Определяет тип данных в указанном поле."""
    try:
        float(current_data[0][field])
        return float
    except ValueError:
        return str
