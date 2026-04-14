"""Chart tools for Superset MCP."""

from superset_mcp.client import client


def list_charts(page: int = 0, page_size: int = 20, search: str = "") -> dict:
    """List charts. Optionally filter by name."""
    params: dict = {"q": f"(page:{page},page_size:{page_size})"}
    if search:
        params["q"] = f"(filters:!((col:slice_name,opr:ChartAllTextSearch,val:'{search}')),page:{page},page_size:{page_size})"
    return client.get("/api/v1/chart/", params=params)


def get_chart(id_or_uuid: str | int) -> dict:
    """Get a chart by ID or UUID."""
    return client.get(f"/api/v1/chart/{id_or_uuid}")


def create_chart(
    slice_name: str,
    viz_type: str,
    datasource_id: int,
    datasource_type: str = "table",
    params: str = "{}",
    description: str = "",
    dashboards: list[int] | None = None,
) -> dict:
    """
    Create a new chart.

    Args:
        slice_name: Chart name
        viz_type: Visualization type (e.g. 'bar', 'line', 'pie', 'table', 'big_number_total')
        datasource_id: ID of the dataset to use
        datasource_type: 'table' for datasets (default)
        params: JSON string of chart parameters/query context
        description: Optional chart description
        dashboards: List of dashboard IDs to add the chart to
    """
    payload: dict = {
        "slice_name": slice_name,
        "viz_type": viz_type,
        "datasource_id": datasource_id,
        "datasource_type": datasource_type,
        "params": params,
    }
    if description:
        payload["description"] = description
    if dashboards:
        payload["dashboards"] = dashboards
    return client.post("/api/v1/chart/", json=payload)


def update_chart(
    pk: int,
    slice_name: str = "",
    description: str = "",
    viz_type: str = "",
    params: str = "",
    cache_timeout: int | None = None,
) -> dict:
    """Update a chart's properties."""
    payload: dict = {}
    if slice_name:
        payload["slice_name"] = slice_name
    if description:
        payload["description"] = description
    if viz_type:
        payload["viz_type"] = viz_type
    if params:
        payload["params"] = params
    if cache_timeout is not None:
        payload["cache_timeout"] = cache_timeout
    return client.put(f"/api/v1/chart/{pk}", json=payload)


def delete_chart(pk: int) -> dict:
    """Delete a chart by ID."""
    return client.delete(f"/api/v1/chart/{pk}")


def get_chart_data(pk: int) -> dict:
    """Fetch the latest data for a chart."""
    return client.get(f"/api/v1/chart/{pk}/data/")
