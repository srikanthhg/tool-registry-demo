# databricks-gpt-oss-20b

import os
import mlflow
from databricks.sdk import WorkspaceClient
from langgraph.prebuilt import create_react_agent
from databricks_langchain import ChatDatabricks, UCFunctionToolkit

def main():
    catalog = os.getenv("UC_CATALOG", "demo")
    schema = os.getenv("UC_SCHEMA", "tools")
    endpoint_name = os.getenv("AGENT_ENDPOINT", "ai-tools-agent")
    model_name = f"{catalog}.{schema}.tools_agent"
    
    tool_names = [
        f"{catalog}.{schema}.get_weather",
        f"{catalog}.{schema}.get_post",
        f"{catalog}.{schema}.get_current_datetime"
    ]
    
    print(f"🔧 Building agent with tools: {tool_names}")
    
    # 1. Setup Tools & LLM
    toolkit = UCFunctionToolkit(function_names=tool_names)
    tools = toolkit.tools
    llm = ChatDatabricks(model="databricks-gpt-oss-20b")
    
    # 2. Create Agent using LangGraph (Modern approach)
    agent = create_react_agent(llm, tools)
    
    # 3. Log to MLflow
    print("📦 Logging agent to MLflow...")
    mlflow.set_registry_uri("databricks-uc")
    
    with mlflow.start_run():
        model_info = mlflow.langchain.log_model(
            lc_model=agent,
            artifact_path="model",
            input_example={"messages": [{"role": "user", "content": "What is the weather in Bangalore?"}]},
            registered_model_name=model_name
        )
        
    latest_version = model_info.registered_model_version
    print(f"✅ Model logged: {model_name} version {latest_version}")
    
    # 4. Deploy to Model Serving
    print(f"🚀 Deploying to endpoint: {endpoint_name}")
    client = WorkspaceClient()
    
    existing = [e.name for e in client.serving_endpoints.list()]
    
    served_model_config = {
        "model_name": model_name,
        "model_version": latest_version,
        "workload_size": "Small",
        "scale_to_zero_enabled": True
    }
    
    if endpoint_name in existing:
        print("Updating existing endpoint...")
        client.serving_endpoints.update_config(
            name=endpoint_name,
            served_models=[served_model_config]
        )
    else:
        print("Creating new endpoint...")
        client.serving_endpoints.create(
            name=endpoint_name,
            config={"served_models": [served_model_config]}
        )
        
    print("🎉 Agent deployed successfully!")
    print("🔗 Go to Playground -> Select 'ai-tools-agent' from the Model Serving Endpoints dropdown.")

if __name__ == "__main__":
    main()