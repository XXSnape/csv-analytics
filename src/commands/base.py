from abc import ABC, abstractmethod
from typing import NamedTuple, Sequence, Callable, ClassVar

from common_types import Data


class HandledData(NamedTuple):
    current_data: Data
    fieldnames: Sequence[str]


class BaseCommand[T: Callable](ABC):
    command: ClassVar[str]
    help_text: ClassVar[str]
    number_in_queue: ClassVar[int]
    required: ClassVar[bool] = False

    def __init__(self) -> None:
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
