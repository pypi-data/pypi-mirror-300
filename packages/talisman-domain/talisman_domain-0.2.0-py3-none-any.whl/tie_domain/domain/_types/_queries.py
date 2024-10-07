import importlib.resources

from gql import gql

with importlib.resources.open_text('tie_domain.domain._types', 'queries.graphql') as f:
    queries = f.read()

DOMAIN_QUERIES = gql(queries)
