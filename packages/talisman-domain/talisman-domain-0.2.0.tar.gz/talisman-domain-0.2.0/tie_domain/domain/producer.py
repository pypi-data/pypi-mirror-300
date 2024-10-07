import enum
import logging
import os
from typing import Iterable, TypeVar

from tdm.abstract.datamodel import AbstractDomainType
from tdm.datamodel.domain import CompositeValueType, ConceptType, DocumentType, Domain
from tdm.datamodel.values import DateTimeValue, DoubleValue, GeoPointValue, IntValue, LinkValue, StringValue, TimestampValue

from tie_domain.domain.updates_manager import AbstractDomainUpdatesManager, MANAGERS
from tie_domain.talisman_api import GQLClientConfig, TalismanAPIAdapter
from tp_interfaces.domain.hooks import DOMAIN_CHANGE_HOOKS
from tp_interfaces.domain.interfaces import AbstractDomainChangeHook, DomainProducer
from tp_interfaces.logging.time import log_time
from ._queries import paginate_types
from ._types import AtomValueType, ComponentValueType, IdentifyingPropertyType, PropertyType, RelationPropertyType, RelationType

logger = logging.getLogger(__name__)

_SYNTHETIC_TYPES = bool(os.getenv('SYNTHETIC_TYPES', True))


class ValueTypes(enum.Enum):
    Date = DateTimeValue
    Double = DoubleValue
    Geo = GeoPointValue
    Int = IntValue
    Timestamp = TimestampValue
    Link = LinkValue
    String = StringValue

    @classmethod
    def get(cls, key: str, default_value=None):
        if key in cls.__members__.keys():
            return cls[key].value
        return default_value


_T = TypeVar('_T', bound=AbstractDomainType)


class TalismanDomainProducer(DomainProducer):
    def __init__(
            self, adapter: TalismanAPIAdapter, updates_manager: AbstractDomainUpdatesManager,
            hooks: Iterable[AbstractDomainChangeHook] = tuple()
    ):
        super().__init__(hooks)
        self._adapter: TalismanAPIAdapter = adapter
        self._updates_manager = updates_manager

    async def __aenter__(self):
        await self._updates_manager.__aenter__()
        return self

    async def __aexit__(self, *exc):
        await self._updates_manager.__aexit__(*exc)

    @log_time(logger=logger)
    async def has_changed(self) -> bool:
        return await self._updates_manager.has_changed

    @log_time(logger=logger)
    async def _get_domain(self) -> Domain:
        await self._updates_manager.update()  # first we notify manager, that we reload domain

        types: dict[str, AbstractDomainType] = {}

        async for concept in paginate_types(self._adapter, 'paginationConceptTypeIE'):
            types[concept['id']] = ConceptType(name=concept['name'], id=concept['id'])

        async for document in paginate_types(self._adapter, 'paginationDocumentTypeIE'):
            types[document['id']] = DocumentType(name=document['name'], id=document['id'])

        async for value in paginate_types(self._adapter, 'paginationValueTypeIE'):
            types[value['id']] = AtomValueType(
                name=value['name'],
                value_type=ValueTypes.get(value['valueType'], value['valueType']),
                id=value['id'],
                value_restriction=tuple(value['valueRestriction']),
                _adapter=self._adapter
            )

        async for composite in paginate_types(self._adapter, 'paginationCompositeValueTypeIE'):
            c = CompositeValueType(name=composite['name'], id=composite['id'])
            types[c.id] = c

            for component in composite['componentValueTypes']:
                types[component['id']] = ComponentValueType(
                    name=component['name'],
                    source=c,
                    target=types[component['valueType']['id']],
                    id=component['id'],
                    isRequired=component['isRequired'],
                    _adapter=self._adapter
                )

        async for relation in paginate_types(self._adapter, 'paginationRelationTypeIE'):
            types[relation['id']] = RelationType(
                name=relation['name'],
                source=types[relation['source']['id']],
                target=types[relation['target']['id']],
                id=relation['id'],
                directed=relation['isDirected'],
                _adapter=self._adapter
            )

        async for prop in paginate_types(self._adapter, 'paginationConceptPropertyTypeIE'):
            if prop['isIdentifying']:
                types[prop['id']] = IdentifyingPropertyType(
                    name=prop['name'],
                    source=types[prop['source']['id']],
                    target=types[prop['target']['id']],
                    id=prop['id'],
                    _adapter=self._adapter
                )
            else:
                types[prop['id']] = PropertyType(
                    name=prop['name'],
                    source=types[prop['source']['id']],
                    target=types[prop['target']['id']],
                    id=prop['id'],
                    _adapter=self._adapter
                )

        async for prop in paginate_types(self._adapter, 'paginationRelationPropertyTypeIE'):
            types[prop['id']] = RelationPropertyType(
                name=prop['name'],
                source=types[prop['source']['id']],
                target=types[prop['target']['id']],
                id=prop['id'],
                _adapter=self._adapter
            )

        final_types = list(types.values())

        if _SYNTHETIC_TYPES:
            from ._synthetic import TYPES
            final_types.extend(TYPES)
        return Domain(final_types)

    @classmethod
    def from_config(cls, config: dict) -> 'TalismanDomainProducer':
        hooks = []
        for hook_cfg in config.get('hooks', []):
            if isinstance(hook_cfg, str):
                name, cfg = hook_cfg, {}
            elif isinstance(hook_cfg, dict):
                name, cfg = hook_cfg['name'], hook_cfg.get('config', {})
            else:
                raise ValueError
            hooks.append(DOMAIN_CHANGE_HOOKS[name].from_config(cfg))
        updates_cfg = config.get('updates', {})
        updates_manager = MANAGERS[updates_cfg.get('strategy', 'never')].from_config(updates_cfg.get('config', {}))
        return cls(TalismanAPIAdapter(GQLClientConfig(**config['adapter'])), updates_manager, hooks)
