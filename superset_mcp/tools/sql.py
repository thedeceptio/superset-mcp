"""SQL execution tools for Superset MCP."""

from superset_mcp.client import client


def execute_sql(
    database_id: int,
    sql: str,
    schema: str = "",
    limit: int = 100,
) -> dict:
    """
    Execute a SQL query and return results.

    Args:
        database_id: ID of the database to query
        sql: SQL query to execute
        schema: Schema/database to run the query in
        limit: Maximum number of rows to return (default 100)
    """
    payload: dict = {
        "database_id": database_id,
        "sql": sql,
        "runAsync": False,
        "select_as_cta": False,
        "limit": limit,
    }
    if schema:
        payload["schema"] = schema
    return client.post("/api/v1/sqllab/execute/", json=payload)


def format_sql(sql: str) -> dict:
    """Format/pretty-print a SQL query."""
    return client.post("/api/v1/sqllab/format_sql/", json={"sql": sql})


def estimate_query_cost(database_id: int, sql: str, schema: str = "") -> dict:
    """Estimate the cost of running a SQL query (supported databases only)."""
    payload: dict = {"database_id": database_id, "sql": sql}
    if schema:
        payload["schema"] = schema
    return client.post("/api/v1/sqllab/estimate/", json=payload)


def list_saved_queries(page: int = 0, page_size: int = 20) -> dict:
    """List saved SQL queries."""
    return client.get("/api/v1/saved_query/", params={"q": f"(page:{page},page_size:{page_size})"})


def save_query(
    label: str,
    sql: str,
    database_id: int,
    schema: str = "",
    description: str = "",
) -> dict:
    """Save a SQL query."""
    payload: dict = {
        "label": label,
        "sql": sql,
        "db_id": database_id,
    }
    if schema:
        payload["schema"] = schema
    if description:
        payload["description"] = description
    return client.post("/api/v1/saved_query/", json=payload)
