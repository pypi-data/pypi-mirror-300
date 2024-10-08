from enum import StrEnum
from typing import Any, Optional, Self


class BetterStrEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(
        name: str,
        start: int,  # noqa: ARG004
        count: int,  # noqa: ARG004
        last_values: list[Any],  # noqa: ARG004
    ) -> str:
        return name

    @classmethod
    def values(cls) -> list[str]:
        return [str(elt) for elt in cls]

    @classmethod
    def default(cls) -> Optional[Self]:
        return None

    @classmethod
    def _missing_(cls, value: str) -> Self:
        default = cls.default()
        if default is None:
            raise ValueError(f"'{value}' is not valid {cls.__name__}")
        return default
