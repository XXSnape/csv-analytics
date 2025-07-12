import csv
import pathlib
from operator import attrgetter

from tabulate import tabulate

from commands.base import BaseCommand, HandledData
from common_types import Data
from exceptions import IncorrectDataException


class FileHandler:
    """Класс для обработки CSV файлов и
    выполнения команд над данными."""

    def __init__(
        self,
        file_path: str,
        values: dict[str, str],
    ) -> None:
        """Инициализирует обработчик файла."""
        self.path = pathlib.Path(file_path).resolve()
        if not self.path.exists():
            raise IncorrectDataException(
                message="Файл не найден. "
                "Пожалуйста, передайте полный путь."
            )
        self.values = values
        self.handlers = list[BaseCommand]()

    @staticmethod
    def output_data(
        handled_data: HandledData,
    ) -> None:
        """Выводит обработанные данные в виде таблицы."""
        print(
            tabulate(
                [row.values() for row in handled_data.current_data],
                headers=handled_data.fieldnames,
                tablefmt="psql",
            )
        )

    def handle(self) -> HandledData:
        """Обрабатывает данные в CSV файле"""
        data = Data()
        fieldnames = tuple[str]()
        with self.path.open() as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            data = list(reader)
        self.handlers.sort(key=attrgetter("number_in_queue"))
        for handler in self.handlers:
            value = self.values.get(handler.command, None)
            if value is not None:
                data, fieldnames = handler.handle_data(
                    current_data=data,
                    fieldnames=fieldnames,
                    value=value,
                )
        return HandledData(
            current_data=data,
            fieldnames=fieldnames,
        )

    def register_handler(
        self,
        command: BaseCommand,
    ) -> None:
        """Регистрирует команду для обработки данных."""
        if not isinstance(command, BaseCommand):
            raise TypeError(
                "Команда должна быть наследником BaseCommand"
            )
        self.handlers.append(command)
