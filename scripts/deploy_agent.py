import os
import mlflow
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ServedModelInput, EndpointCoreConfigInput

def main():
    catalog = os.getenv("UC_CATALOG", "demo")
    schema = os.getenv("UC_SCHEMA", "tools")
    endpoint_name = os.getenv("AGENT_ENDPOINT", "ai-tools-agent")
    model_name = f"{catalog}.{schema}.tools_agent"

    print("🔧 UC Tools will be loaded from scripts/agent_code.py")

    # ----------------------------
    # 1. Log to MLflow using "Models from Code"
    # ----------------------------
    mlflow.set_registry_uri("databricks-uc")
    print("📦 Logging agent code to MLflow...")

    with mlflow.start_run():
        # We pass the path to the python file as 'lc_model'
        result = mlflow.langchain.log_model(
            lc_model="scripts/agent_code.py", 
            artifact_path="agent",
            registered_model_name=model_name,
            # CRITICAL FIX: Provide an input example so MLflow can infer the schema
            input_example={"input": "What is the weather in Bangalore?"},
            pip_requirements=[
                "langchain==0.3.14",
                "langchain-core==0.3.29",
                "langgraph==0.2.62",
                "databricks-langchain==0.6.0"
            ]
        )

    version = result.registered_model_version
    print(f"✅ Registered real agent: {model_name} v{version}")

    # ----------------------------
    # 2. Deploy to Serving Endpoint
    # ----------------------------
    client = WorkspaceClient()
    print(f"🚀 Deploying endpoint: {endpoint_name}")

    served_model = ServedModelInput(
        model_name=model_name,
        model_version=version,
        workload_size="Small",
        scale_to_zero_enabled=True
    )

    config = EndpointCoreConfigInput(
        name=endpoint_name,
        served_models=[served_model]
    )

    existing = [e.name for e in client.serving_endpoints.list()]

    if endpoint_name in existing:
        print("🔄 Updating endpoint...")
        client.serving_endpoints.update_config(
            name=endpoint_name,
            served_models=[served_model]
        )
    else:
        print("🆕 Creating endpoint...")
        client.serving_endpoints.create(
            name=endpoint_name,
            config=config
        )

    print("🎉 DONE. Your agent will now actually call the tools!")
    print(f"👉 Open Databricks Playground → Select '{endpoint_name}' from the Model Serving Endpoints dropdown.")

if __name__ == "__main__":
    main()