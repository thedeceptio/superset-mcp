# superset-mcp

MCP (Model Context Protocol) server for Apache Superset. Gives AI assistants full access to your Superset instance — dashboards, charts, datasets, databases, and SQL execution.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package manager
- Access to a running Apache Superset instance

## Setup (takes ~1 minute)

### 1. Clone the repo

```bash
git clone <repo-url>
cd superset-mcp
```

### 2. Configure credentials

```bash
cp .env.example .env
```

Edit `.env`:

```env
SUPERSET_URL=http://your-superset-host:8088
SUPERSET_USERNAME=your-username
SUPERSET_PASSWORD=your-password
```

### 3. Test it works

```bash
uv run superset-mcp
```

You should see the MCP server start without errors. Press `Ctrl+C` to stop.

---

## Connect to your AI client

Replace `/ABSOLUTE/PATH/TO/superset-mcp` with the actual path where you cloned the repo.

### Claude Code

Add to `~/.claude/settings.json` (or project-level `.claude/settings.json`):

```json
{
  "mcpServers": {
    "superset": {
      "command": "uv",
      "args": ["--directory", "/ABSOLUTE/PATH/TO/superset-mcp", "run", "superset-mcp"],
      "env": {
        "SUPERSET_URL": "http://your-superset-host:8088",
        "SUPERSET_USERNAME": "your-username",
        "SUPERSET_PASSWORD": "your-password"
      }
    }
  }
}
```

Or run in terminal:
```bash
claude mcp add superset -- uv --directory /ABSOLUTE/PATH/TO/superset-mcp run superset-mcp
```

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)  
or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "superset": {
      "command": "uv",
      "args": ["--directory", "/ABSOLUTE/PATH/TO/superset-mcp", "run", "superset-mcp"],
      "env": {
        "SUPERSET_URL": "http://your-superset-host:8088",
        "SUPERSET_USERNAME": "your-username",
        "SUPERSET_PASSWORD": "your-password"
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json` in your project or `~/.cursor/mcp.json` globally:

```json
{
  "mcpServers": {
    "superset": {
      "command": "uv",
      "args": ["--directory", "/ABSOLUTE/PATH/TO/superset-mcp", "run", "superset-mcp"],
      "env": {
        "SUPERSET_URL": "http://your-superset-host:8088",
        "SUPERSET_USERNAME": "your-username",
        "SUPERSET_PASSWORD": "your-password"
      }
    }
  }
}
```

---

## Available Tools

### Dashboards
| Tool | Description |
|---|---|
| `list_dashboards` | List all dashboards (with optional search) |
| `get_dashboard` | Get a dashboard by ID or slug |
| `get_dashboard_charts` | Get all charts in a dashboard |
| `get_dashboard_datasets` | Get all datasets used by a dashboard |
| `create_dashboard` | Create a new dashboard |
| `update_dashboard` | Update title, layout, metadata |
| `publish_dashboard` | Publish a draft dashboard |
| `copy_dashboard` | Duplicate a dashboard |
| `delete_dashboard` | Delete a dashboard |

### Charts
| Tool | Description |
|---|---|
| `list_charts` | List all charts (with optional search) |
| `get_chart` | Get a chart by ID or UUID |
| `get_chart_data` | Fetch the latest data for a chart |
| `create_chart` | Create a new chart |
| `update_chart` | Update chart properties |
| `delete_chart` | Delete a chart |

### Datasets
| Tool | Description |
|---|---|
| `list_datasets` | List all datasets |
| `get_dataset` | Get a dataset by ID or UUID |
| `create_dataset` | Create from a table or SQL query |
| `get_or_create_dataset` | Get existing or create new |
| `refresh_dataset` | Sync columns from source table |
| `update_dataset` | Update dataset properties |
| `get_dataset_related_objects` | See which charts/dashboards use it |
| `delete_dataset` | Delete a dataset |

### Databases
| Tool | Description |
|---|---|
| `list_databases` | List all database connections |
| `get_database` | Get a database connection by ID |
| `list_schemas` | List schemas in a database |
| `list_tables` | List tables in a schema |
| `get_table_metadata` | Get column info for a table |
| `get_select_star` | Get a SELECT * template for a table |

### SQL
| Tool | Description |
|---|---|
| `execute_sql` | Run a SQL query and get results |
| `format_sql` | Pretty-print a SQL query |
| `estimate_query_cost` | Estimate query cost (if supported) |
| `list_saved_queries` | List saved SQL queries |
| `save_query` | Save a SQL query |

---

## Example prompts

Once connected to your AI assistant:

- *"List all published dashboards"*
- *"Create a new dashboard called 'Sales Overview'"*
- *"Show me all charts in dashboard 11"*
- *"Run a SQL query on database 2: SELECT count(*) FROM orders"*
- *"What datasets are used by the 'Revenue' dashboard?"*
- *"Create a bar chart using dataset 5 showing sales by region"*
