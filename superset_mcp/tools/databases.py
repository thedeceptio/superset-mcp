"""Database connection tools for Superset MCP."""

from superset_mcp.client import client


def list_databases(page: int = 0, page_size: int = 50) -> dict:
    """List all database connections configured in Superset."""
    return client.get("/api/v1/database/", params={"q": f"(page:{page},page_size:{page_size})"})


def get_database(pk: int) -> dict:
    """Get a database connection by ID."""
    return client.get(f"/api/v1/database/{pk}")


def list_schemas(database_id: int) -> dict:
    """List all schemas in a database."""
    return client.get(f"/api/v1/database/{database_id}/schemas/")


def list_tables(database_id: int, schema: str = "") -> dict:
    """List tables in a database schema."""
    params = {}
    if schema:
        params["q"] = f"(schema_name:'{schema}')"
    return client.get(f"/api/v1/database/{database_id}/tables/", params=params or None)


def get_table_metadata(database_id: int, table_name: str, schema: str = "default") -> dict:
    """Get column metadata for a table."""
    return client.get(f"/api/v1/database/{database_id}/table/{table_name}/{schema}/")


def get_select_star(database_id: int, table_name: str, schema: str = "") -> dict:
    """Get a SELECT * query for a table (with schema)."""
    if schema:
        return client.get(f"/api/v1/database/{database_id}/select_star/{table_name}/{schema}/")
    return client.get(f"/api/v1/database/{database_id}/select_star/{table_name}/")
