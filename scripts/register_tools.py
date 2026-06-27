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

sys.path.append(os.getcwd())

from databricks.sdk import WorkspaceClient
from unitycatalog.ai.core.databricks import DatabricksFunctionClient

from tools.weather_tool import get_weather
from tools.rest_api_tool import get_post
from tools.datetime_tool import get_current_datetime

def main():
    workspace_client = WorkspaceClient()
    uc_client = DatabricksFunctionClient(workspace_client)

    catalog = os.getenv("UC_CATALOG", "demo")
    schema = os.getenv("UC_SCHEMA", "tools")

    tools_to_register = [
        get_weather,
        get_post,
        get_current_datetime,
    ]

    for tool in tools_to_register:
        print(f"--- Registering {tool.__name__} ---")
        
        # Step 1: Try to drop the existing function first
        # try:
        #     print(f"🗑️  Dropping existing function {full_name}...")
        #     uc_client.delete_function(full_name)
        #     print(f"✅ Dropped {full_name}")
        # except Exception as e:
        #     print(f"ℹ️  Function {full_name} doesn't exist or already dropped: {e}")
        
        # Step 2: Create the function with dependencies
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

    print("🎉 All tools registered successfully with dependencies!")


if __name__ == "__main__":
    main()