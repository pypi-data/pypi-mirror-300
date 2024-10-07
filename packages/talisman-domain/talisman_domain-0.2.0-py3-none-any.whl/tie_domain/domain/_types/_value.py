from dataclasses import dataclass
from typing import Iterable

from tp_interfaces.domain.abstract import AbstractLiteralValueType
from ._nerc import NERCBasedType


@dataclass(frozen=True)
class AtomValueType(NERCBasedType, AbstractLiteralValueType):
    def __post_init__(self):
        NERCBasedType.__post_init__(self)
        AbstractLiteralValueType.__post_init__(self)

    @property
    def _operation_name(self) -> str:
        return 'valueTypeExtrasIE'

    @property
    def _variables(self) -> Iterable[dict]:
        yield {
            'name': self.id
        }
