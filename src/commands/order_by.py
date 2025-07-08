from collections.abc import Sequence
from functools import partial

from common_types import Data, OperatorFunc

from .base import (
    BaseCommand,
    DataValidatorMixin,
    HandledData,
    find_out_type,
)


def sorting(
    data: Data,
    field: str,
    reverse: bool,
) -> HandledData:
    type_of_field = find_out_type(
        current_data=data,
        field=field,
    )
    sorted_data = sorted(
        data,
        key=lambda item: type_of_field(item[field]),
        reverse=reverse,
    )
    return HandledData(
        current_data=sorted_data,
        fieldnames=list(data[0].keys()),
    )


sorting_asc = partial(sorting, reverse=False)
sorting_desc = partial(sorting, reverse=True)


class OrderByCommand(
    DataValidatorMixin[OperatorFunc],
    BaseCommand[OperatorFunc],
):
    command = "order-by"
    help_text = "Команда для сортировки по полю"
    number_in_queue = 2
    raise_exception_if_there_is_no_data = False

    def handle_data(
        self,
        current_data: Data,
        fieldnames: Sequence[str],
        value: str,
    ) -> HandledData:
        result = self.validate_data(
            current_data=current_data,
            fieldnames=fieldnames,
            value=value,
        )
        if result is None:
            return HandledData(
                current_data=current_data,
                fieldnames=fieldnames,
            )
        func, field = result
        return func(current_data, field)


order_by_command = OrderByCommand()
order_by_command.add_operator("asc", sorting_asc)
order_by_command.add_operator("desc", sorting_desc)
