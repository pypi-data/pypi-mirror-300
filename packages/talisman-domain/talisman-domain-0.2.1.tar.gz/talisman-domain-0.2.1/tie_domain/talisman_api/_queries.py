def get_pagination_query(pagination: str, query: str, limit: int, operation_name: str = None, filter_settings: str | None = None):
    if operation_name is None:
        operation_name = f"{pagination}IE"
    return f'''
    query {operation_name} {{
        {pagination}(filterSettings: {filter_settings if filter_settings else "{}"}, limit: {limit}) {{
            total
            {query if limit else ""}
        }}
    }}'''
