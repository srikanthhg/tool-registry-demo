from databricks.sdk import WorkspaceClient
from unitycatalog.ai.core.databricks import DatabricksFunctionClient

from tools.weather_tool import get_weather

workspace_client = WorkspaceClient()

client = DatabricksFunctionClient(workspace_client)
