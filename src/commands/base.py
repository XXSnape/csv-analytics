from abc import ABC, abstractmethod
from typing import NamedTuple, Sequence

from common_types import Data


class HandledData(NamedTuple):
    current_data: Data
    fieldnames: Sequence[str]


class BaseCommand(ABC):

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

    @abstractmethod
    def handle_data(
        self,
        current_data: Data,
        fieldnames: Sequence[str],
        value: str,
    ) -> HandledData:
        raise NotImplementedError
