# # databricks-gpt-oss-20b

# import os
# import mlflow
# from databricks.sdk import WorkspaceClient

# from databricks_langchain import ChatDatabricks, UCFunctionToolkit

# from langchain.agents import AgentExecutor, create_tool_calling_agent
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# def main():
#     catalog = os.getenv("UC_CATALOG", "demo")
#     schema = os.getenv("UC_SCHEMA", "tools")
#     endpoint_name = os.getenv("AGENT_ENDPOINT", "ai-tools-agent")

#     model_name = f"{catalog}.{schema}.tools_agent"

#     tool_names = [
#         f"{catalog}.{schema}.get_weather",
#         f"{catalog}.{schema}.get_post",
#         f"{catalog}.{schema}.get_current_datetime"
#     ]

#     print(f"🔧 Tools: {tool_names}")

#     # -------------------------
#     # 1. UC Tools
#     # -------------------------
#     toolkit = UCFunctionToolkit(function_names=tool_names)
#     tools = toolkit.tools

#     # -------------------------
#     # 2. LLM (Databricks model)
#     # -------------------------
#     llm = ChatDatabricks(model="databricks-gpt-oss-20b")

#     # -------------------------
#     # 3. Prompt (IMPORTANT FIX)
#     # -------------------------
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", "You are a helpful assistant that can use tools when needed."),
#         ("human", "{input}"),
#         MessagesPlaceholder(variable_name="agent_scratchpad")
#     ])

#     # -------------------------
#     # 4. Agent
#     # -------------------------
#     agent = create_tool_calling_agent(llm, tools, prompt)
#     agent_executor = AgentExecutor(agent=agent, tools=tools)

#     # -------------------------
#     # 5. MLflow logging
#     # -------------------------
#     mlflow.set_registry_uri("databricks-uc")

#     print("📦 Logging agent to MLflow...")

#     with mlflow.start_run():
#         result = mlflow.langchain.log_model(
#             lc_model=agent_executor,
#             artifact_path="agent",
#             registered_model_name=model_name
#         )

#     version = result.registered_model_version
#     print(f"✅ Registered model: {model_name} v{version}")

#     # -------------------------
#     # 6. Deploy to serving endpoint
#     # -------------------------
#     client = WorkspaceClient()

#     print(f"🚀 Deploying endpoint: {endpoint_name}")

#     client.serving_endpoints.create_or_update(
#         name=endpoint_name,
#         config={
#             "served_models": [
#                 {
#                     "model_name": model_name,
#                     "model_version": version,
#                     "workload_size": "Small",
#                     "scale_to_zero_enabled": True
#                 }
#             ]
#         }
#     )

#     print("🎉 Deployment complete!")
#     print(f"👉 Open Databricks Playground → select endpoint: {endpoint_name}")


# if __name__ == "__main__":
#     main()



# ===============
# logs:

# Run python scripts/deploy_agent.py
#   python scripts/deploy_agent.py
#   shell: /usr/bin/bash -e {0}
#   env:
#     pythonLocation: /opt/hostedtoolcache/Python/3.11.15/x64
#     PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib/pkgconfig
#     Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
#     Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
#     Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
#     LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
#     DATABRICKS_HOST: ***
#     DATABRICKS_TOKEN: ***
#     UC_CATALOG: ***
#     UC_SCHEMA: ***
#     AGENT_ENDPOINT: ai-***-agent
# 2026/06/27 10:31:41 INFO mlflow.store.db.utils: Creating initial MLflow database tables...
# 2026/06/27 10:31:41 INFO mlflow.store.db.utils: Updating database tables
# 2026/06/27 10:31:42 WARNING mlflow.models.model: `artifact_path` is deprecated. Please use `name` instead.
# /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/langgraph/checkpoint/base/__init__.py:18: LangChainPendingDeprecationWarning: The default value of `allowed_objects` will change in a future version. Pass an explicit value (e.g., allowed_objects='messages' or allowed_objects='core') to suppress this warning.
#   from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
# /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/mlflow/langchain/utils/logging.py:240: LangChainDeprecationWarning: Importing OpenAI from langchain.llms is deprecated. Please replace deprecated imports:
# >> from langchain.llms import OpenAI
# with new imports of:
# >> from langchain_community.llms import OpenAI
# You can use the langchain cli to **automatically** upgrade many imports. Please see documentation here <https://python.langchain.com/docs/versions/v0_2/>
#   if cls := getattr(module, class_name, None):
# /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/mlflow/langchain/utils/logging.py:240: LangChainDeprecationWarning: Importing LLMs from langchain is deprecated. Importing from langchain will no longer be supported as of langchain==0.2.0. Please import from langchain-community instead:
# `from langchain_community.llms import HuggingFacePipeline`.
# To install langchain-community run `pip install -U langchain-community`.
#   if cls := getattr(module, class_name, None):
# /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/mlflow/langchain/utils/logging.py:240: LangChainDeprecationWarning: Importing LLMs from langchain is deprecated. Importing from langchain will no longer be supported as of langchain==0.2.0. Please import from langchain-community instead:
# `from langchain_community.llms import Databricks`.
# To install langchain-community run `pip install -U langchain-community`.
#   if cls := getattr(module, class_name, None):
# /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/mlflow/langchain/utils/logging.py:240: LangChainDeprecationWarning: Importing LLMs from langchain is deprecated. Importing from langchain will no longer be supported as of langchain==0.2.0. Please import from langchain-community instead:
# `from langchain_community.llms import Mlflow`.
# To install langchain-community run `pip install -U langchain-community`.
#   if cls := getattr(module, class_name, None):
# /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/mlflow/langchain/utils/logging.py:240: LangChainDeprecationWarning: Importing chat models from langchain is deprecated. Importing from langchain will no longer be supported as of langchain==0.2.0. Please import from langchain-community instead:
# `from langchain_community.chat_models import ChatDatabricks`.
# To install langchain-community run `pip install -U langchain-community`.
#   if cls := getattr(module, class_name, None):
# /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/mlflow/langchain/utils/logging.py:240: LangChainDeprecationWarning: Importing chat models from langchain is deprecated. Importing from langchain will no longer be supported as of langchain==0.2.0. Please import from langchain-community instead:
# `from langchain_community.chat_models import ChatMlflow`.
# To install langchain-community run `pip install -U langchain-community`.
#   if cls := getattr(module, class_name, None):
# /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/mlflow/langchain/utils/logging.py:240: LangChainDeprecationWarning: Importing chat models from langchain is deprecated. Importing from langchain will no longer be supported as of langchain==0.2.0. Please import from langchain-community instead:
# `from langchain_community.chat_models import ChatOpenAI`.
# To install langchain-community run `pip install -U langchain-community`.
#   if cls := getattr(module, class_name, None):
# /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/mlflow/langchain/utils/logging.py:240: LangChainDeprecationWarning: Importing chat models from langchain is deprecated. Importing from langchain will no longer be supported as of langchain==0.2.0. Please import from langchain-community instead:
# `from langchain_community.chat_models import AzureChatOpenAI`.
# To install langchain-community run `pip install -U langchain-community`.
#   if cls := getattr(module, class_name, None):
# Traceback (most recent call last):
# 🔧 Tools: ['***.***.get_weather', '***.***.get_post', '***.***.get_current_datetime']
#   File "/home/runner/work/tool-registry-***/tool-registry-***/scripts/deploy_agent.py", line 97, in <module>
#     main()
#   File "/home/runner/work/tool-registry-***/tool-registry-***/scripts/deploy_agent.py", line 62, in main
# 📦 Logging agent to MLflow...
#     result = mlflow.langchain.log_model(
#              ^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/mlflow/tracing/provider.py", line 891, in wrapper
#     result = f(*args, **kwargs)
#              ^^^^^^^^^^^^^^^^^^
#   File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/mlflow/langchain/model.py", line 599, in log_model
#     return Model.log(
#            ^^^^^^^^^^
#   File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/mlflow/models/model.py", line 1218, in log
#     flavor.save_model(path=local_path, mlflow_model=mlflow_model, **kwargs)
#   File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/mlflow/tracing/provider.py", line 896, in wrapper
#     result = f(*args, **kwargs)
#              ^^^^^^^^^^^^^^^^^^
#   File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/mlflow/langchain/model.py", line 298, in save_model
#     input_schema = Schema(input_columns)
#                    ^^^^^^^^^^^^^^^^^^^^^
#   File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/mlflow/types/schema.py", line 970, in __init__
#     raise MlflowException.invalid_parameter_value(
# mlflow.exceptions.MlflowException: Creating Schema with empty inputs is not allowed.
# Error: Process completed with exit code 1.