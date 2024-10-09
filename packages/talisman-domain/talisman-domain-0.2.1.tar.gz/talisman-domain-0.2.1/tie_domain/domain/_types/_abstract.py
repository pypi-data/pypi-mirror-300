from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from tdm.abstract.datamodel import AbstractDomainType

from tie_domain.talisman_api import TalismanAPIAdapter
from ._queries import DOMAIN_QUERIES


@dataclass(frozen=True)
class AbstractAdapterBasedType(AbstractDomainType, metaclass=ABCMeta):
    _adapter: TalismanAPIAdapter = None

    def __post_init__(self):
        if self._adapter is None:
            raise ValueError

    async def _load_object(self, *, operation_name: str = None, variables: Iterable[dict] = None) -> dict:
        if operation_name is None:
            operation_name = self._operation_name
        if variables is None:
            variables = self._variables
        async with self._adapter:
            for v in variables:
                result = await self._find_object(operation_name, v)
                if result is not None:
                    return result
        raise ValueError(f"no type found [operation: {operation_name}, variables: {v}]")

    async def _find_object(self, operation_name: str, variables: dict) -> dict | None:
        if 'offset' in variables:
            raise ValueError
        offset = 0
        total = 1
        while offset < total:
            vs = {"offset": offset}
            vs.update(variables)
            result = (await self._adapter.gql_call(DOMAIN_QUERIES, operation_name=operation_name, variables=vs))['result']
            if result['total'] == 0:
                return None
            total = result['total']
            for item in result['list']:
                if item['id'] == vs['name']:
                    return item
            offset += len(result['list'])

    @property
    @abstractmethod
    def _operation_name(self) -> str:
        pass

    @property
    @abstractmethod
    def _variables(self) -> Iterable[dict]:
        pass
