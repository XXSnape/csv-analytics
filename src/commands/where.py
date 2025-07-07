import re

from common_types import Data
from exceptions import IncorrectDataException

from .base import BaseCommand, HandledData


class WhereCommand(BaseCommand):

    def handle_data(
        self, current_data: Data, fieldnames: list[str], value: str
    ) -> HandledData:
        if not current_data:
            return HandledData(
                current_data=current_data, fieldnames=fieldnames
            )
        validated_data = []
        match = re.match(r"(.+)([<>=])(.+)", value)
        if not match:
            raise IncorrectDataException("Неверный формат условия")
        field, operator, condition = match.groups()
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

        for row in current_data:
            match operator:
                case "=":
                    if type_of_field(row[field]) == condition:
                        validated_data.append(row)
                case "<":
                    if type_of_field(row[field]) < condition:
                        validated_data.append(row)
                case ">":
                    if type_of_field(row[field]) > condition:
                        validated_data.append(row)
        return HandledData(
            current_data=validated_data,
            fieldnames=fieldnames,
        )


where_command = WhereCommand(
    command="where",
    help_text="Условие для фильтрации данных",
    number_in_queue=0,
)
