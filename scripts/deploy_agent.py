# databricks-gpt-oss-20b

import os
import time
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import (
    EndpointCoreConfigInput,
    ServedEntityInput,
    AgentConfig,
    Tool,
    UCFunctionToolSpec
)

def main():
    # Connect to Databricks
    client = WorkspaceClient()
    
    catalog = os.getenv("UC_CATALOG", "demo")
    schema = os.getenv("UC_SCHEMA", "tools")
    endpoint_name = os.getenv("AGENT_ENDPOINT", "ai-tools-agent")
    
    tool_names = [
        f"{catalog}.{schema}.get_weather",
        f"{catalog}.{schema}.get_post",
        f"{catalog}.{schema}.get_current_datetime"
    ]
    
    print(f"🔧 Configuring agent with tools: {tool_names}")
    
    # Define the tools for the agent using UCFunctionToolSpec
    tools = [
        Tool(function_spec=UCFunctionToolSpec(name=name))
        for name in tool_names
    ]
    
    # Check if endpoint exists to avoid conflicts in CI/CD
    existing_endpoints = [e.name for e in client.serving_endpoints.list()]
    if endpoint_name in existing_endpoints:
        print(f"⚠️ Endpoint '{endpoint_name}' already exists. Deleting to recreate with latest tools...")
        client.serving_endpoints.delete(name=endpoint_name)
        # Wait a few seconds for the deletion to process
        time.sleep(15) 

    print(f"🚀 Deploying agent endpoint: {endpoint_name}")
    
    # Create the Agent Endpoint
    client.serving_endpoints.create(
        name=endpoint_name,
        endpoint_type="AGENT",
        config=EndpointCoreConfigInput(
            served_entities=[
                ServedEntityInput(
                    entity_name="databricks-gpt-oss-20b",
                    workload_size="Small",
                    scale_to_zero_enabled=True
                )
            ],
            agent_config=AgentConfig(tools=tools)
        )
    )
    
    print("✅ Agent deployed successfully!")
    print(f"📍 Endpoint: {endpoint_name}")
    print("🔗 Go to Playground -> Select 'ai-tools-agent' to chat with it (no manual tool setup needed!).")

if __name__ == "__main__":
    main()