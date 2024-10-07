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
                result = (await self._adapter.gql_call(DOMAIN_QUERIES, operation_name=operation_name, variables=v))['result']
                if result['total'] == 1:
                    break
                elif result['total'] > 1:
                    raise ValueError("operation returned multiple types")
            else:
                raise ValueError(f"no type found [operation: {operation_name}, variables: {v}]")
        return result['list'][0]

    @property
    @abstractmethod
    def _operation_name(self) -> str:
        pass

    @property
    @abstractmethod
    def _variables(self) -> Iterable[dict]:
        pass
