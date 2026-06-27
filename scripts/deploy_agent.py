# databricks-gpt-oss-20b
import os
from databricks import agents
from databricks.sdk import WorkspaceClient

def main():
    client = WorkspaceClient()
    
    catalog = os.getenv("UC_CATALOG", "demo")
    schema = os.getenv("UC_SCHEMA", "tools")
    endpoint_name = os.getenv("AGENT_ENDPOINT", "ai-tools-agent")
    
    tool_names = [
        f"{catalog}.{schema}.get_weather",
        f"{catalog}.{schema}.get_post",
        f"{catalog}.{schema}.get_current_datetime"
    ]
    
    print(f"🔧 Creating agent with tools: {tool_names}")
    
    # Create UC Function Toolkit
    toolkit = agents.UCFunctionToolkit(function_names=tool_names)
    
    print(f"🚀 Deploying agent to endpoint: {endpoint_name}")
    
    # Deploy using the correct API
    deployment = agents.deploy(
        model_name="databricks-meta-llama-3-3-70b-instruct",
        endpoint_name=endpoint_name,
        tools=toolkit.tools
    )
    
    print("✅ Agent deployed successfully!")
    print(f"📍 Endpoint: {endpoint_name}")
    print(f"🔗 Deployment details: {deployment}")


if __name__ == "__main__":
    main()