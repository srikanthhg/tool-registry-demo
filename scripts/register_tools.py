# %pip install unitycatalog-ai databricks-sdk

import sys
import os

# Ensure "tools" folder is importable
sys.path.append(os.path.dirname(__file__))

from tools.weather_tool import get_weather

from databricks.sdk import WorkspaceClient
from unitycatalog.ai.core.databricks import DatabricksFunctionClient


def main():

    # Step 1: Create Databricks clients
    w = WorkspaceClient()
    client = DatabricksFunctionClient(w)

    # Step 2: Register function into Unity Catalog
    client.create_python_function(
        func=get_weather,
        catalog="demo",
        schema="tools",
        name="get_weather"
    )

    print("✅ Function registered successfully in Unity Catalog")


if __name__ == "__main__":
    main()