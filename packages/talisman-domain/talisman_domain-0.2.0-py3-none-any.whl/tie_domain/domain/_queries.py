import importlib.resources
from typing import AsyncIterator

from gql import gql

from tie_domain.talisman_api import TalismanAPIAdapter

with importlib.resources.open_text('tie_domain.domain', 'queries.graphql') as f:
    queries = f.read()

DOMAIN_QUERIES = gql(queries)


async def paginate_types(adapter: TalismanAPIAdapter, operation_name: str, variables: dict = None) -> AsyncIterator[dict]:
    if variables is None:
        variables = {}
    async with adapter:
        # get total
        result = await adapter.gql_call(DOMAIN_QUERIES, operation_name, {**variables, "limit": 0, "offset": 0})
        total = result['pagination']['total']

        result = await adapter.gql_call(DOMAIN_QUERIES, operation_name, {**variables, "limit": total, "offset": 0})
    for item in result['pagination']['list']:
        yield item
