# %pip install unitycatalog-ai databricks-sdk

import os
import sys

# Add the project root to Python path
sys.path.append(os.getcwd())

from databricks.sdk import WorkspaceClient
from unitycatalog.ai.core.databricks import DatabricksFunctionClient

from tools.weather_tool import get_weather


def main():

    # Connect to Databricks
    workspace_client = WorkspaceClient()

    # Create UC Function client
    uc_client = DatabricksFunctionClient(workspace_client)

    # Register the Python function
    function_info = uc_client.create_python_function(
        func=get_weather,
        catalog="demo",
        schema="tools",
        replace=True
    )

    print("Registration Successful")
    print(function_info)


if __name__ == "__main__":
    main()