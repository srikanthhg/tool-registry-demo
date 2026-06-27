import os
from databricks import agents

def main():
    # Your tool function names in Unity Catalog
    catalog = os.getenv("UC_CATALOG", "demo")
    schema = os.getenv("UC_SCHEMA", "tools")
    
    tool_names = [
        f"{catalog}.{schema}.get_weather",
        f"{catalog}.{schema}.get_post",
        f"{catalog}.{schema}.get_current_datetime"
    ]
    
    print(f"🔧 Creating agent with tools: {tool_names}")
    
    # Create UC Function Toolkit (correct way)
    toolkit = agents.UCFunctionToolkit(
        function_names=tool_names
    )
    
    # Create and deploy the agent
    endpoint_name = os.getenv("AGENT_ENDPOINT", "ai-tools-agent")
    
    print(f"🚀 Deploying agent to endpoint: {endpoint_name}")
    
    # Deploy the agent with the toolkit
    agents.deploy(
        model="databricks-gpt-oss-20b",
        tools=toolkit.tools,
        endpoint_name=endpoint_name,
        tags={"team": "devops", "environment": "production"}
    )
    
    print("✅ Agent deployed successfully!")
    print(f"📍 Endpoint: {endpoint_name}")
    print("🔗 You can now query it via API or Databricks Playground")


if __name__ == "__main__":
    main()