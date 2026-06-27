# databricks-gpt-oss-20b

import os
import mlflow
from databricks.sdk import WorkspaceClient
from mlflow.models import infer_signature
from databricks_langchain import ChatDatabricks


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
    # LLM (Databricks model)
    # ----------------------------
    llm = ChatDatabricks(model="databricks-gpt-oss-20b")

    # ----------------------------
    # MLflow PyFunc Model
    # ----------------------------
    class DatabricksAgent(mlflow.pyfunc.PythonModel):
        def predict(self, context, model_input: dict) -> dict:
            messages = model_input.get("messages", [])
            user_input = messages[-1]["content"] if messages else ""

            response = llm.invoke(user_input)

            return {
                "response": response,
                "tools_available": tool_names
            }

    # ----------------------------
    # MLflow Signature (REQUIRED for UC)
    # ----------------------------
    input_example = {
        "messages": [
            {"role": "user", "content": "What is the weather in Bangalore?"}
        ]
    }

    output_example = {
        "response": "sample response",
        "tools_available": tool_names
    }

    signature = infer_signature(input_example, output_example)

    mlflow.set_registry_uri("databricks-uc")

    print("📦 Logging model to MLflow...")

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
    # Deploy to Serving Endpoint
    # ----------------------------
    client = WorkspaceClient()

    print(f"🚀 Deploying endpoint: {endpoint_name}")

    client.serving_endpoints.create_or_update(
        name=endpoint_name,
        config={
            "served_models": [
                {
                    "model_name": model_name,
                    "model_version": version,
                    "workload_size": "Small",
                    "scale_to_zero_enabled": True
                }
            ]
        }
    )

    print("🎉 DONE")
    print(f"👉 Open Databricks Playground → {endpoint_name}")


if __name__ == "__main__":
    main()