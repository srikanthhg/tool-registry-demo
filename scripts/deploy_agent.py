# databricks-gpt-oss-20b

import os
import mlflow
from databricks.sdk import WorkspaceClient

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

    print(f"🔧 Registering UC tools: {tool_names}")

    # -------------------------------------------------------
    # 1. UC Tools (Databricks-native tool binding)
    # -------------------------------------------------------
    toolkit = UCFunctionToolkit(function_names=tool_names)

    # -------------------------------------------------------
    # 2. LLM (Databricks Foundation Model)
    # -------------------------------------------------------
    llm = ChatDatabricks(model="databricks-gpt-oss-20b")

    # -------------------------------------------------------
    # 3. Databricks Agent (NO LangChain, NO LangGraph)
    # -------------------------------------------------------
    from databricks.agents import Agent

    agent = Agent(
        name=model_name,
        model=llm,
        tools=toolkit.tools,
        instructions=(
            "You are a helpful assistant. "
            "Use available tools when needed to answer user questions."
        )
    )

    # -------------------------------------------------------
    # 4. MLflow logging (Databricks Agents flavor)
    # -------------------------------------------------------
    mlflow.set_registry_uri("databricks-uc")

    print("📦 Logging Databricks Agent to MLflow...")

    with mlflow.start_run():
        result = mlflow.pyfunc.log_model(
            artifact_path="agent",
            python_model=agent,
            registered_model_name=model_name
        )

    version = result.registered_model_version
    print(f"✅ Registered model: {model_name} v{version}")

    # -------------------------------------------------------
    # 5. Deploy to Serving Endpoint
    # -------------------------------------------------------
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

    print("🎉 Deployment complete!")
    print(f"👉 Open Databricks Playground → select: {endpoint_name}")


if __name__ == "__main__":
    main()