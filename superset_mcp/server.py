"""Superset MCP server — exposes Superset REST API as MCP tools."""

import os

from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

mcp = FastMCP(
    "superset",
    instructions=(
        "You are connected to an Apache Superset instance. "
        "Use these tools to manage dashboards, charts, datasets, databases, and run SQL queries. "
        f"Superset URL: {os.environ.get('SUPERSET_URL', 'not configured')}"
    ),
)

# --- Dashboards ---

from superset_mcp.tools.dashboards import (  # noqa: E402
    copy_dashboard,
    create_dashboard,
    delete_dashboard,
    get_dashboard,
    get_dashboard_charts,
    get_dashboard_datasets,
    list_dashboards,
    publish_dashboard,
    update_dashboard,
)

mcp.tool()(list_dashboards)
mcp.tool()(get_dashboard)
mcp.tool()(get_dashboard_charts)
mcp.tool()(get_dashboard_datasets)
mcp.tool()(create_dashboard)
mcp.tool()(update_dashboard)
mcp.tool()(delete_dashboard)
mcp.tool()(copy_dashboard)
mcp.tool()(publish_dashboard)

# --- Charts ---

from superset_mcp.tools.charts import (  # noqa: E402
    create_chart,
    delete_chart,
    get_chart,
    get_chart_data,
    list_charts,
    update_chart,
)

mcp.tool()(list_charts)
mcp.tool()(get_chart)
mcp.tool()(create_chart)
mcp.tool()(update_chart)
mcp.tool()(delete_chart)
mcp.tool()(get_chart_data)

# --- Datasets ---

from superset_mcp.tools.datasets import (  # noqa: E402
    create_dataset,
    delete_dataset,
    get_dataset,
    get_dataset_related_objects,
    get_or_create_dataset,
    list_datasets,
    refresh_dataset,
    update_dataset,
)

mcp.tool()(list_datasets)
mcp.tool()(get_dataset)
mcp.tool()(create_dataset)
mcp.tool()(get_or_create_dataset)
mcp.tool()(update_dataset)
mcp.tool()(refresh_dataset)
mcp.tool()(delete_dataset)
mcp.tool()(get_dataset_related_objects)

# --- Databases ---

from superset_mcp.tools.databases import (  # noqa: E402
    get_database,
    get_select_star,
    get_table_metadata,
    list_databases,
    list_schemas,
    list_tables,
)

mcp.tool()(list_databases)
mcp.tool()(get_database)
mcp.tool()(list_schemas)
mcp.tool()(list_tables)
mcp.tool()(get_table_metadata)
mcp.tool()(get_select_star)

# --- SQL ---

from superset_mcp.tools.sql import (  # noqa: E402
    estimate_query_cost,
    execute_sql,
    format_sql,
    list_saved_queries,
    save_query,
)

mcp.tool()(execute_sql)
mcp.tool()(format_sql)
mcp.tool()(estimate_query_cost)
mcp.tool()(list_saved_queries)
mcp.tool()(save_query)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
