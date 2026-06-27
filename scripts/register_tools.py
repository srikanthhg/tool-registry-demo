# # %pip install unitycatalog-ai databricks-sdk

# import os
# import sys

# # Add the project root to Python path
# sys.path.append(os.getcwd())

# from databricks.sdk import WorkspaceClient
# from unitycatalog.ai.core.databricks import DatabricksFunctionClient

# from tools.weather_tool import get_weather


# def main():

#     # Connect to Databricks
#     workspace_client = WorkspaceClient()

#     # Create UC Function client
#     uc_client = DatabricksFunctionClient(workspace_client)

#     # Register the Python function
#     function_info = uc_client.create_python_function(
#         func=get_weather,
#         catalog="demo",
#         schema="tools",
#         replace=True
#     )

#     print("Registration Successful")
#     print(function_info)


# if __name__ == "__main__":
#     main()

import os
import sys

# Add the project root to Python path
sys.path.append(os.getcwd())

from databricks.sdk import WorkspaceClient
from unitycatalog.ai.core.databricks import DatabricksFunctionClient

# Import all your tools
from tools.weather_tool import get_weather
from tools.rest_api_tool import get_post
from tools.datetime_tool import get_current_datetime

def main():
    # Connect to Databricks
    workspace_client = WorkspaceClient()
    
    # Create UC Function client
    uc_client = DatabricksFunctionClient(workspace_client)

    # Get catalog and schema from environment variables (set by GitHub Actions)
    catalog = os.getenv("UC_CATALOG", "demo")
    schema = os.getenv("UC_SCHEMA", "tools")

    # List of tools to register
    tools_to_register = [
        # get_weather,
        # get_post,
        # get_current_datetime
        {"func": get_weather, "deps": ["requests"]},
        {"func": get_post, "deps": ["requests"]},
        {"func": get_current_datetime, "deps": ["pytz"]},
    ]

    # Register each tool
    for tool in tools_to_register:
        tool = tool["func"]
        deps = tool["deps"]
        print(f"--- Registering {tool.__name__} with dependencies: {deps} ---")
        try:
            function_info = uc_client.create_python_function(
                func=tool,
                catalog=catalog,
                schema=schema,
                replace=True
            )
            print(f"✅ Successfully registered: {function_info.full_name}\n")
        except Exception as e:
            print(f"❌ Failed to register {tool.__name__}: {e}\n")
            raise e

    print("🎉 All tools registered successfully!")


if __name__ == "__main__":
    main()