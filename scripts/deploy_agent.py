# databricks-gpt-oss-20b

import os
import mlflow
from databricks.sdk import WorkspaceClient
from mlflow.models import infer_signature
from databricks.sdk.service.serving import (
    ServedModelInput,
    EndpointCoreConfigInput
)

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

    print(f"🔧 UC Tools: {tool_names}")

    # ----------------------------
    # MLflow Model (simple PyFunc)
    # ----------------------------
    class DatabricksAgent(mlflow.pyfunc.PythonModel):
        def predict(self, context, model_input: dict) -> dict:
            user_input = model_input.get("input", "")
            return {
                "response": f"You asked: {user_input}",
                "tools_available": tool_names
            }

    # ----------------------------
    # MLflow Signature (REQUIRED)
    # ----------------------------
    input_example = {"input": "What is the weather in Bangalore?"}

    output_example = {
        "response": "sample response",
        "tools_available": tool_names
    }

    signature = infer_signature(input_example, output_example)

    mlflow.set_registry_uri("databricks-uc")

    print("📦 Logging MLflow model...")

    with mlflow.start_run():
        result = mlflow.pyfunc.log_model(
            artifact_path="agent",
            python_model=DatabricksAgent(),
            registered_model_name=model_name,
            input_example=input_example,
            signature=signature
        )

    version = result.registered_model_version
    print(f"✅ Registered model: {model_name} v{version}")

    # ----------------------------
    # Serving Endpoint (FIXED API)
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

    print("🎉 DONE")
    print(f"👉 Open Databricks Playground → {endpoint_name}")


if __name__ == "__main__":
    main()