import os
import mlflow
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ServedModelInput, EndpointCoreConfigInput

# LangChain imports for the real agent
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
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

    print(f"🔧 UC Tools: {tool_names}")

    # ----------------------------
    # 1. Build the REAL Agent
    # ----------------------------
    print(" Building real LLM agent...")
    toolkit = UCFunctionToolkit(function_names=tool_names)
    tools = toolkit.tools
    
    # Use Llama 3 as the brain
    llm = ChatDatabricks(model="databricks-meta-llama-3-3-70b-instruct")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant with access to real-time tools. Use them when needed."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create the agent that can actually call the tools
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

    # ----------------------------
    # 2. Log to MLflow
    # ----------------------------
    mlflow.set_registry_uri("databricks-uc")
    print("📦 Logging real agent to MLflow...")

    with mlflow.start_run():
        result = mlflow.langchain.log_model(
            lc_model=agent_executor,
            artifact_path="agent",
            registered_model_name=model_name,
            input_example={"input": "What is the weather in Bangalore?"}
        )

    version = result.registered_model_version
    print(f"✅ Registered real agent: {model_name} v{version}")

    # ----------------------------
    # 3. Deploy to Serving Endpoint
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