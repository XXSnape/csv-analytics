from collections.abc import Callable
from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from commands.base import HandledData

Data: TypeAlias = list[dict[str, str]]
OperatorFunc: TypeAlias = Callable[
    [Data, str],
    "HandledData",
]
