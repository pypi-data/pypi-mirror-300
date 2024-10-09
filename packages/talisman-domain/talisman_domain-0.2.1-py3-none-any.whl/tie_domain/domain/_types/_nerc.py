from abc import ABCMeta
from dataclasses import dataclass, field
from itertools import chain
from typing import Iterator

from tp_interfaces.domain.abstract import AbstractNERCBasedType, NERCRegexp
from ._abstract import AbstractAdapterBasedType
from ._cached import CachedValue, cached


@dataclass(frozen=True)
class NERCBasedType(AbstractAdapterBasedType, AbstractNERCBasedType, metaclass=ABCMeta):
    _regexp: CachedValue[tuple[NERCRegexp, ...]] = field(default_factory=CachedValue)
    _black_regexp: CachedValue[tuple[NERCRegexp, ...]] = field(default_factory=CachedValue)
    _pretrained_nerc_models: CachedValue[tuple[str, ...]] = field(default_factory=CachedValue)
    _dictionary: CachedValue[tuple[str, ...]] = field(default_factory=CachedValue)
    _black_list: CachedValue[tuple[str, ...]] = field(default_factory=CachedValue)

    def __post_init__(self):
        AbstractAdapterBasedType.__post_init__(self)
        AbstractNERCBasedType.__post_init__(self)
        if any(not isinstance(getattr(self, field), CachedValue) for field in [
            '_regexp', '_black_regexp', '_pretrained_nerc_models', '_dictionary', '_black_list'
        ]):
            raise ValueError

    @property
    @cached
    async def regexp(self) -> tuple[NERCRegexp, ...]:
        type_ = await self._load_object(variables=self._variables_with_extras({'regexp': True}))
        return tuple(NERCRegexp(**data) for data in type_['regexp'])

    @property
    @cached
    async def black_regexp(self) -> tuple[NERCRegexp, ...]:
        type_ = await self._load_object(variables=self._variables_with_extras({'black_regexp': True}))
        return tuple(NERCRegexp(**data) for data in type_['black_regexp'])

    @property
    @cached
    async def pretrained_nerc_models(self) -> tuple[str, ...]:
        type_ = await self._load_object(variables=self._variables_with_extras({'pretrained_models': True}))
        return tuple(type_['pretrained_models'])

    @property
    @cached
    async def dictionary(self) -> tuple[str, ...]:
        type_ = await self._load_object(variables=self._variables_with_extras({'dictionary': True}))
        return tuple(chain(type_.get('dictionary', ()), type_.get('names_dictionary', ())))

    @property
    @cached
    async def black_list(self) -> tuple[str, ...]:
        type_ = await self._load_object(variables=self._variables_with_extras({'black_list': True}))
        return tuple(type_['black_list'])

    def _variables_with_extras(self, extra: dict) -> Iterator[dict]:
        for variables in self._variables:
            yield {**variables, **extra}
