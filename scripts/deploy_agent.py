# databricks-gpt-oss-20b

import os
import mlflow
from databricks.sdk import WorkspaceClient

from databricks_langchain import ChatDatabricks, UCFunctionToolkit

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


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

    print(f"🔧 Tools: {tool_names}")

    # -------------------------
    # 1. UC Tools
    # -------------------------
    toolkit = UCFunctionToolkit(function_names=tool_names)
    tools = toolkit.tools

    # -------------------------
    # 2. LLM (Databricks model)
    # -------------------------
    llm = ChatDatabricks(model="databricks-gpt-oss-20b")

    # -------------------------
    # 3. Prompt (IMPORTANT FIX)
    # -------------------------
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that can use tools when needed."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    # -------------------------
    # 4. Agent
    # -------------------------
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    # -------------------------
    # 5. MLflow logging
    # -------------------------
    mlflow.set_registry_uri("databricks-uc")

    print("📦 Logging agent to MLflow...")

    with mlflow.start_run():
        result = mlflow.langchain.log_model(
            lc_model=agent_executor,
            artifact_path="agent",
            registered_model_name=model_name
        )

    version = result.registered_model_version
    print(f"✅ Registered model: {model_name} v{version}")

    # -------------------------
    # 6. Deploy to serving endpoint
    # -------------------------
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
    print(f"👉 Open Databricks Playground → select endpoint: {endpoint_name}")


if __name__ == "__main__":
    main()