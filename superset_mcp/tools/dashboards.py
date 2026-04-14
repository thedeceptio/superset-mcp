"""Dashboard tools for Superset MCP."""

from superset_mcp.client import client


def list_dashboards(page: int = 0, page_size: int = 20, search: str = "") -> dict:
    """List dashboards. Optionally filter by title with `search`."""
    params: dict = {"q": f"(page:{page},page_size:{page_size})"}
    if search:
        params["q"] = f"(filters:!((col:dashboard_title,opr:DashboardTitleOrSlugFilter,val:'{search}')),page:{page},page_size:{page_size})"
    return client.get("/api/v1/dashboard/", params=params)


def get_dashboard(id_or_slug: str | int) -> dict:
    """Get a single dashboard by ID or slug."""
    return client.get(f"/api/v1/dashboard/{id_or_slug}")


def get_dashboard_charts(id_or_slug: str | int) -> dict:
    """Get all charts in a dashboard."""
    return client.get(f"/api/v1/dashboard/{id_or_slug}/charts")


def get_dashboard_datasets(id_or_slug: str | int) -> dict:
    """Get all datasets used by a dashboard."""
    return client.get(f"/api/v1/dashboard/{id_or_slug}/datasets")


def create_dashboard(
    title: str,
    slug: str = "",
    published: bool = False,
    json_metadata: str = "",
    position_json: str = "",
) -> dict:
    """Create a new dashboard."""
    payload: dict = {"dashboard_title": title, "published": published}
    if slug:
        payload["slug"] = slug
    if json_metadata:
        payload["json_metadata"] = json_metadata
    if position_json:
        payload["position_json"] = position_json
    return client.post("/api/v1/dashboard/", json=payload)


def update_dashboard(pk: int, title: str = "", published: bool | None = None, json_metadata: str = "", position_json: str = "") -> dict:
    """Update an existing dashboard."""
    payload: dict = {}
    if title:
        payload["dashboard_title"] = title
    if published is not None:
        payload["published"] = published
    if json_metadata:
        payload["json_metadata"] = json_metadata
    if position_json:
        payload["position_json"] = position_json
    return client.put(f"/api/v1/dashboard/{pk}", json=payload)


def delete_dashboard(pk: int) -> dict:
    """Delete a dashboard by ID."""
    return client.delete(f"/api/v1/dashboard/{pk}")


def copy_dashboard(id_or_slug: str | int) -> dict:
    """Create a copy of a dashboard."""
    return client.post(f"/api/v1/dashboard/{id_or_slug}/copy/")


def publish_dashboard(pk: int) -> dict:
    """Set a dashboard as published."""
    return client.put(f"/api/v1/dashboard/{pk}", json={"published": True})
