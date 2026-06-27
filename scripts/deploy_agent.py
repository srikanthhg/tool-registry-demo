# databricks-gpt-oss-20b
import os

def main():
    catalog = os.getenv("UC_CATALOG", "demo")
    schema = os.getenv("UC_SCHEMA", "tools")
    endpoint_name = os.getenv("AGENT_ENDPOINT", "ai-tools-agent")
    
    # Create the agent configuration
    agent_config = {
        "model_serving_endpoint_config": {
            "name": endpoint_name,
            "config": {
                "served_models": [{
                    "model_name": "databricks-meta-llama-3-3-70b-instruct",
                    "workload_size": "Small",
                    "scale_to_zero_enabled": True
                }]
            }
        },
        "agent_config": {
            "functions": [
                {"function_name": f"{catalog}.{schema}.get_weather"},
                {"function_name": f"{catalog}.{schema}.get_post"},
                {"function_name": f"{catalog}.{schema}.get_current_datetime"}
            ]
        }
    }
    
    # Note: Direct agent creation via SDK might require specific permissions
    # The simplest approach is often to use the Databricks UI for initial setup
    # then manage via code
    
    print("✅ Agent configuration prepared!")
    print(f"📍 Manual deployment required for endpoint: {endpoint_name}")
    print("🔗 Use Databricks UI to create agent with these functions")
    print("🔧 Agent config:")
    print(agent_config)


if __name__ == "__main__":
    main()