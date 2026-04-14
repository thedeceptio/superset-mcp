"""Dataset tools for Superset MCP."""

from superset_mcp.client import client


def list_datasets(page: int = 0, page_size: int = 20, search: str = "") -> dict:
    """List datasets (virtual or physical tables)."""
    params: dict = {"q": f"(page:{page},page_size:{page_size})"}
    if search:
        params["q"] = f"(filters:!((col:table_name,opr:DatasetIsNullOrEmpty,val:'{search}')),page:{page},page_size:{page_size})"
    return client.get("/api/v1/dataset/", params=params)


def get_dataset(id_or_uuid: str | int) -> dict:
    """Get a dataset by ID or UUID."""
    return client.get(f"/api/v1/dataset/{id_or_uuid}")


def create_dataset(
    database_id: int,
    table_name: str,
    schema: str = "",
    sql: str = "",
    is_managed_externally: bool = False,
) -> dict:
    """
    Create a dataset from a table or SQL query.

    Args:
        database_id: ID of the database connection
        table_name: Table name (or virtual dataset name if sql provided)
        schema: Schema name
        sql: SQL query for virtual datasets (optional)
        is_managed_externally: Whether the dataset is managed externally
    """
    payload: dict = {
        "database": database_id,
        "table_name": table_name,
    }
    if schema:
        payload["schema"] = schema
    if sql:
        payload["sql"] = sql
    if is_managed_externally:
        payload["is_managed_externally"] = True
    return client.post("/api/v1/dataset/", json=payload)


def get_or_create_dataset(database_id: int, table_name: str, schema: str = "") -> dict:
    """Get an existing dataset or create it if it doesn't exist."""
    payload: dict = {"database_id": database_id, "table_name": table_name}
    if schema:
        payload["schema"] = schema
    return client.post("/api/v1/dataset/get_or_create/", json=payload)


def update_dataset(
    pk: int,
    table_name: str = "",
    description: str = "",
    sql: str = "",
    schema: str = "",
    cache_timeout: int | None = None,
    is_managed_externally: bool | None = None,
) -> dict:
    """Update a dataset's properties."""
    payload: dict = {}
    if table_name:
        payload["table_name"] = table_name
    if description:
        payload["description"] = description
    if sql:
        payload["sql"] = sql
    if schema:
        payload["schema"] = schema
    if cache_timeout is not None:
        payload["cache_timeout"] = cache_timeout
    if is_managed_externally is not None:
        payload["is_managed_externally"] = is_managed_externally
    return client.put(f"/api/v1/dataset/{pk}", json=payload)


def refresh_dataset(pk: int) -> dict:
    """Refresh the dataset's columns and metrics from the source."""
    return client.put(f"/api/v1/dataset/{pk}/refresh")


def delete_dataset(pk: int) -> dict:
    """Delete a dataset by ID."""
    return client.delete(f"/api/v1/dataset/{pk}")


def get_dataset_related_objects(id_or_uuid: str | int) -> dict:
    """Get charts and dashboards using this dataset."""
    return client.get(f"/api/v1/dataset/{id_or_uuid}/related_objects")
