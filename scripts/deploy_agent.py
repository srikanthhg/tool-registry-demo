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

    print("🔧 Tools:", tool_names)

    toolkit = UCFunctionToolkit(function_names=tool_names)
    tools = toolkit.tools

    llm = ChatDatabricks(model="databricks-gpt-oss-20b")

    # IMPORTANT: NO LangGraph, NO pyfunc wrapper
    from langchain.agents import AgentExecutor, create_tool_calling_agent
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "{input}")
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    mlflow.set_registry_uri("databricks-uc")

    print("📦 Logging model...")

    with mlflow.start_run():
        result = mlflow.langchain.log_model(
            lc_model=agent_executor,
            artifact_path="agent",
            registered_model_name=model_name
        )

    version = result.registered_model_version

    client = WorkspaceClient()

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

    print("✅ Ready for Playground:", endpoint_name)

if __name__ == "__main__":
    main()