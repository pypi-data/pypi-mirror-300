from dataclasses import dataclass
from typing import Iterator

from tp_interfaces.domain.abstract import AbstractComponentValueType
from ._relext import RelExtBasedType


@dataclass(frozen=True)
class ComponentValueType(RelExtBasedType, AbstractComponentValueType):

    @property
    def _operation_name(self) -> str:
        raise NotImplementedError  # talisman KB API has no relext models for composite value components

    @property
    def _variables(self) -> Iterator[dict]:
        raise NotImplementedError
