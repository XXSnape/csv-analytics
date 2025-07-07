from abc import ABC, abstractmethod
from typing import NamedTuple, Sequence, Callable

from common_types import Data


class HandledData(NamedTuple):
    current_data: Data
    fieldnames: Sequence[str]


class BaseCommand[T: Callable](ABC):

    def __init__(
        self,
        command: str,
        help_text: str,
        number_in_queue: int,
        required: bool = False,
    ) -> None:
        self.command = command
        self.help_text = help_text
        self.required = required
        self.number_in_queue = number_in_queue
        self.operators = dict[str, T]()

    @abstractmethod
    def handle_data(
        self,
        current_data: Data,
        fieldnames: Sequence[str],
        value: str,
    ) -> HandledData:
        raise NotImplementedError

    def add_operator(
        self,
        operator: str,
        func: T,
    ) -> None:
        if operator in self.operators:
            raise ValueError(f"Оператор {operator} уже существует")
        self.operators[operator] = func
