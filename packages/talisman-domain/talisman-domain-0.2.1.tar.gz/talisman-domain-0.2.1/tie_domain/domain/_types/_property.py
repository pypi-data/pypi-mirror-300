from dataclasses import dataclass
from typing import Iterable, Iterator

from tdm.datamodel.domain import ConceptType, DocumentType

from tp_interfaces.domain.abstract import AbstractIdentifyingPropertyType, AbstractPropertyType, AbstractRelationPropertyType
from ._nerc import NERCBasedType
from ._relext import RelExtBasedType


@dataclass(frozen=True)
class PropertyType(RelExtBasedType, AbstractPropertyType):
    def __post_init__(self):
        RelExtBasedType.__post_init__(self)
        AbstractPropertyType.__post_init__(self)

    @property
    def _operation_name(self) -> str:
        return 'propertyTypeExtrasIE'

    @property
    def _variables(self) -> Iterator[dict]:
        yield {
            'source_type_id': self.source.id,
            'name': self.id
        }


@dataclass(frozen=True)
class IdentifyingPropertyType(NERCBasedType, AbstractIdentifyingPropertyType):

    @property
    def _operation_name(self) -> str:
        if isinstance(self.source, ConceptType):
            return 'conceptTypeExtrasIE'
        elif isinstance(self.source, DocumentType):
            return 'documentTypeExtrasIE'

    @property
    def _variables(self) -> Iterable[dict]:
        yield {
            'name': self.source.id
        }


@dataclass(frozen=True)
class RelationPropertyType(RelExtBasedType, AbstractRelationPropertyType):

    def __post_init__(self):
        RelExtBasedType.__post_init__(self)
        AbstractPropertyType.__post_init__(self)

    @property
    def _operation_name(self) -> str:
        return 'relationPropertyTypeExtrasIE'

    @property
    def _variables(self) -> Iterator[dict]:
        yield {
            "source_type_id": self.source.id,
            "name": self.id
        }
