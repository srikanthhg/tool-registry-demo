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
    
    # Create the agent with Unity Catalog tools
    agent = agents.Agent(
        model="databricks-gpt-oss-20b",
        tools=[
            agents.UCFunctionToolkit(function_name=tool) 
            for tool in tool_names
        ]
    )
    
    # Deploy as a Model Serving endpoint
    endpoint_name = os.getenv("AGENT_ENDPOINT", "ai-tools-agent")
    
    print(f"🚀 Deploying agent to endpoint: {endpoint_name}")
    
    agent.deploy(
        endpoint_name=endpoint_name,
        tags={"team": "devops", "environment": "production"}
    )
    
    # Fixed: Removed unused 'client' variable and unnecessary 'f' prefixes
    print("✅ Agent deployed successfully!")
    print(f"📍 Endpoint: {endpoint_name}")
    print("🔗 You can now query it via API or Databricks Playground")


if __name__ == "__main__":
    main()