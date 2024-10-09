from dataclasses import dataclass
from typing import Iterator

from tp_interfaces.domain.abstract import AbstractRelationType
from ._relext import RelExtBasedType


@dataclass(frozen=True)
class RelationType(RelExtBasedType, AbstractRelationType):
    def __post_init__(self):
        RelExtBasedType.__post_init__(self)
        AbstractRelationType.__post_init__(self)

    @property
    def _operation_name(self) -> str:
        return 'relationTypeExtrasIE'

    @property
    def _variables(self) -> Iterator[dict]:
        yield {
            'source_type_id': self.source.id,
            'name': self.id
        }
        yield {
            'source_type_id': self.target.id,
            'name': self.id
        }
